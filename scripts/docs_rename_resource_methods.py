#!/usr/bin/env python3
"""Rename resource method signatures in sdk/client_api.html for readability."""

import os
import re
import shutil
import sys
import zipfile
from pathlib import Path


def _replace_method_signature(match: re.Match) -> str:
    async_prefix = match.group(2) or ""
    return f"{match.group(1)}{async_prefix}GitCode.{CLS2ATTR[match.group(3)]}{match.group(4)}"


ROOT_DIR = Path(__file__).parent.parent.absolute()
RESOURCE_PATTERN = re.compile(r'(<span class="pre">)(Async)?(\w+Resource)(\.</span>)')
CLS2ATTR = {}
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

if __name__ == "__main__":
    from gitcode_api import GitCode
    from gitcode_api._cli_banner import CBLU, CEND, CGRN

    if not sys.stdout.isatty():
        CBLU = CGRN = CEND = ""

    for attr, val in GitCode(api_key="dummy").__dict__.items():
        CLS2ATTR[type(val).__name__] = attr

    rtd_root = os.getenv("READTHEDOCS_OUTPUT")
    if rtd_root:
        build_root = Path(rtd_root)
    else:
        build_root = ROOT_DIR / "docs/_build"

    for html_path in ["html/sdk/client_api.html", "singlehtml/index.html", "epub/sdk/client_api.xhtml"]:
        client_api = build_root / html_path
        if not client_api.is_file():
            continue
        original_content = client_api.read_text(encoding="utf-8")
        optimized_content = RESOURCE_PATTERN.sub(_replace_method_signature, original_content)
        if original_content == optimized_content:
            continue
        replace_count = len(RESOURCE_PATTERN.findall(original_content))
        client_api.write_text(optimized_content, encoding="utf-8")
        if html_path.startswith("epub"):
            epub_dir = build_root / "epub"
            tmp_zip = build_root / "tmp_epub.zip"
            for epub_file in epub_dir.glob("**/*.epub"):
                os.remove(str(epub_file.absolute()))
            with zipfile.ZipFile(
                build_root / "tmp_epub.zip", "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
            ) as zipf:
                for path in epub_dir.rglob("*"):
                    if path.is_file():
                        zipf.write(path, arcname=path.relative_to(epub_dir))
            shutil.move(tmp_zip, epub_dir / (ROOT_DIR.name + ".epub"))
        changed_file = client_api.relative_to(ROOT_DIR)
        print(f"{CGRN}Successfully changed {replace_count:3d} resource method signatures in {CBLU}{changed_file}{CEND}")
