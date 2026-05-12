import concurrent.futures
import json
import os
import re
import time
import warnings

from _shared import load_config
from githubkit import GitHub
from tqdm.rich import tqdm
from tqdm.std import TqdmExperimentalWarning

from gitcode_api import GitCode

GITCODE_USER, GITHUB_USER = "SushiNinja", "Trenza1ore"
GITCODE_REPO = GITHUB_REPO = "GitCode-API"
PAGE_SIZE = 50
UPLOAD_TIMEOUT = 6000  # 100 minutes
SKIP_ASSETS = True


def _sort_semantic_version(version: str) -> int:
    ver_list = version.removeprefix("v").split(".")[:3]
    ver_list = ver_list + ["0"] * (3 - len(ver_list))
    patch_ver = re.match(r"[0-9]+", ver_list[2])
    if patch_ver:
        ver_list[2] = patch_ver.group(0)
    return int(ver_list[2]) + 1_000 * int(ver_list[1]) + 1_000_000 * int(ver_list[0])


cfg = load_config()
gh = GitHub(auth=os.getenv("GITHUB_ACCESS_TOKEN"))
gh_client = gh.rest(version="2026-03-10")
gc_client = GitCode(api_key=cfg.api_key, owner=GITCODE_USER, repo=GITCODE_REPO)
all_gh_tags, all_gc_tags, tag2hash = {}, {}, {}
page_idx, new_tags = 1, [None] * PAGE_SIZE

gc_client.releases.list(owner=GITCODE_USER, repo=GITCODE_REPO)

while len(new_tags) == PAGE_SIZE:
    new_tags = json.loads(
        gh_client.repos.list_releases(GITHUB_USER, GITHUB_REPO, per_page=PAGE_SIZE, page=page_idx).content
    )
    all_gh_tags |= {rel["tag_name"]: rel for rel in new_tags}
    page_idx += 1

page_idx, new_tags = 1, [None] * PAGE_SIZE
while len(new_tags) == PAGE_SIZE:
    new_tags = gc_client.releases.list(per_page=PAGE_SIZE, page=page_idx)
    all_gc_tags |= {rel.tag_name: rel for rel in new_tags}
    page_idx += 1

page_idx, new_tags = 1, [None] * PAGE_SIZE
while len(new_tags) == PAGE_SIZE:
    new_tags = gc_client.tags.list(per_page=PAGE_SIZE, page=page_idx)
    tag2hash |= {tag.name: tag.commit.sha for tag in new_tags}
    page_idx += 1

tags_pending_release = set(all_gh_tags) - set(all_gc_tags)

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", message="rich is experimental", category=TqdmExperimentalWarning)
    with concurrent.futures.ThreadPoolExecutor() as pool:
        asset_uploads = {}
        for r in tqdm(sorted(tags_pending_release, key=_sort_semantic_version)):
            release_name = all_gh_tags[r]["name"].removeprefix("v")
            body = all_gh_tags[r]["body"].replace(
                f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}", f"https://gitcode.com/{GITCODE_USER}/{GITCODE_REPO}"
            )
            gc_client.releases.create(
                owner=GITCODE_USER,
                repo=GITCODE_REPO,
                name=release_name,
                tag=r,
                body=body,
                target_commitish=tag2hash[r],
                release_status="pre" if all_gh_tags[r]["prerelease"] else "latest",
            )
            print(f"- {release_name}: created", flush=True)
            if SKIP_ASSETS:
                continue
            t = time.time()
            for asset in all_gh_tags[r]["assets"]:
                asset: dict
                file_name = asset["name"]
                resp = gh_client.repos.get_release_asset(
                    GITHUB_USER, GITHUB_REPO, asset["id"], headers={"Accept": "application/octet-stream"}
                ).content
                future = pool.submit(
                    gc_client.releases.upload,
                    tag=r,
                    file_name=file_name,
                    content=resp,
                    upload_timeout=UPLOAD_TIMEOUT,
                )
                asset_uploads[future] = (file_name, t)

        for future in tqdm(concurrent.futures.as_completed(asset_uploads), total=len(asset_uploads)):
            file_name, t = asset_uploads[future]
            print(f"\t> uploaded: {file_name} ({time.time() - t:g}s)", flush=True)
            future.result()
