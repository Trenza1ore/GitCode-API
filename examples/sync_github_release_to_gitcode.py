"""
My actual code for syncing releases from GitHub to GitCode mirror.
The githubkit library is used for its similarity in design philosophy to our gitcode-api:
- Code: https://github.com/yanyongyu/githubkit
- Docs: https://yanyongyu.github.io/githubkit/
"""

import concurrent.futures
import os
import re
import time
import warnings
from typing import Dict, Optional

import httpx
from _shared import load_config
from githubkit import GitHub
from githubkit.versions.v2026_03_10.models import Release as GHRelease
from tqdm.rich import tqdm
from tqdm.std import TqdmExperimentalWarning

from gitcode_api import GitCode, GitCodeError
from gitcode_api._cli_banner import CBLU, CEND, CGRN, CRED
from gitcode_api._models import Release as GCRelease


def _sort_semantic_version(version: str) -> int:
    """A heuristic for sorting semantic version."""
    ver_list = version.removeprefix("v").split(".")[:3]
    ver_list = ver_list + ["0"] * (3 - len(ver_list))
    patch_ver = re.match(r"[0-9]+", ver_list[2])
    if patch_ver:
        ver_list[2] = patch_ver.group(0)
    return int(ver_list[2]) + 1_000 * int(ver_list[1]) + 1_000_000 * int(ver_list[0])


GITCODE_USER, GITHUB_USER = "SushiNinja", "Trenza1ore"  # Don't judge, plz
GITCODE_REPO = GITHUB_REPO = "GitCode-API"  # For my case, mirror repo has the same name
PAGE_SIZE = 50  # Just an arbitrary number
UPLOAD_TIMEOUT = 1800  # 30 minutes, server will probably cancel the put request by now
ASSETS_PATTERN = re.compile(r".*")  # Pattern for valid asset file name, others are ignored
MAX_UPLOAD_THREADS: Optional[int] = None  # Max worker in the thread pool, None = default
GH_TAGS_RELEASED: Dict[str, GHRelease] = {}  # Mapping of [tag] -> [release] for GitHub
GC_TAGS_RELEASED: Dict[str, GCRelease] = {}  # Mapping of [tag] -> [release] for GitCode
GC_TAG_TO_HASH: Dict[str, str] = {}  # Mapping of [tag] -> [commit hash] for GitCode

cfg = load_config()
gh = GitHub(auth=os.getenv("GITHUB_ACCESS_TOKEN"))
gh_client = gh.rest(version="2026-03-10")
gc_client = GitCode(api_key=cfg.api_key, owner=GITCODE_USER, repo=GITCODE_REPO)

# Fetch all releases from GitHub
page_idx, new_tags = 1, [None] * PAGE_SIZE
while len(new_tags) == PAGE_SIZE:
    new_tags = gh_client.repos.list_releases(GITHUB_USER, GITHUB_REPO, per_page=PAGE_SIZE, page=page_idx).parsed_data
    GH_TAGS_RELEASED |= {rel.tag_name: rel for rel in new_tags}
    page_idx += 1

# Fetch all releases from GitCode
page_idx, new_tags = 1, [None] * PAGE_SIZE
while len(new_tags) == PAGE_SIZE:
    new_tags = gc_client.releases.list(per_page=PAGE_SIZE, page=page_idx)
    GC_TAGS_RELEASED |= {rel.tag_name: rel for rel in new_tags}
    page_idx += 1

# Fetch all tags (including unreleased) from GitCode
page_idx, new_tags = 1, [None] * PAGE_SIZE
while len(new_tags) == PAGE_SIZE:
    new_tags = gc_client.tags.list(per_page=PAGE_SIZE, page=page_idx)
    GC_TAG_TO_HASH |= {tag.name: tag.commit.sha for tag in new_tags}
    page_idx += 1

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", message="rich is experimental", category=TqdmExperimentalWarning)
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_UPLOAD_THREADS) as pool:
        asset_upload_jobs = {}

        # Go through all tags that exist in GitCode and are releases on GitHub, create upload jobs for artefacts
        for r in tqdm(sorted(GC_TAG_TO_HASH, key=_sort_semantic_version)):
            if r not in GH_TAGS_RELEASED:
                continue
            release_name = GH_TAGS_RELEASED[r].name.removeprefix("v")
            body = GH_TAGS_RELEASED[r].body.replace(
                f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}", f"https://gitcode.com/{GITCODE_USER}/{GITCODE_REPO}"
            )
            if r not in GC_TAGS_RELEASED:
                gc_client.releases.create(
                    owner=GITCODE_USER,
                    repo=GITCODE_REPO,
                    name=release_name,
                    tag=r,
                    body=body,
                    target_commitish=GC_TAG_TO_HASH[r],
                    release_status="pre" if GH_TAGS_RELEASED[r].prerelease else "latest",
                )
                print(f"{CGRN}- {release_name}: created{CEND}", flush=True)
                gc_uploaded_assets = {}
            else:
                gc_uploaded_assets = {a.name for a in GC_TAGS_RELEASED[r].assets}

            for asset in GH_TAGS_RELEASED[r].assets:
                file_name: str = asset.name
                if file_name in gc_uploaded_assets or not ASSETS_PATTERN.search(file_name):
                    continue
                resp = gh_client.repos.get_release_asset(
                    GITHUB_USER, GITHUB_REPO, asset.id, headers={"Accept": "application/octet-stream"}
                ).content
                future = pool.submit(
                    GitCode(api_key=cfg.api_key, owner=GITCODE_USER, repo=GITCODE_REPO).releases.upload,
                    tag=r,
                    file_name=file_name,
                    content=resp,
                    upload_timeout=UPLOAD_TIMEOUT,
                )
                asset_upload_jobs[future] = (file_name, time.time(), len(resp))
                print(f"{CBLU}\t+ uploading: {file_name}{CEND}", flush=True)

        for future in tqdm(concurrent.futures.as_completed(asset_upload_jobs), total=len(asset_upload_jobs)):
            file_name, start_time, file_size = asset_upload_jobs[future]
            minutes = (time.time() - start_time) / 60
            for unit in ["B", "KB", "MB", "GB"]:
                _file_size = file_size // 1024
                if _file_size:
                    file_size = _file_size
                else:
                    break
            try:
                future.result()
                print(f"{CGRN}\t> uploaded: {file_name} ({file_size} {unit}, {minutes:g} min){CEND}", flush=True)
            except (httpx.TimeoutException, GitCodeError) as e:
                print(
                    f"{CRED}\tx fail to upload {file_name} ({file_size} {unit}, {minutes:g} min):{CEND} {e}", flush=True
                )
