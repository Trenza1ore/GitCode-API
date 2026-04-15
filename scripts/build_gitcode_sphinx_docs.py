#!/usr/bin/env python3
"""Download https://docs.gitcode.com/en/docs/* pages and generate Sphinx RST under docs/."""

import argparse
import re
import shutil
import subprocess
import sys
from collections import deque
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

BASE = "https://docs.gitcode.com"
DOCS_PREFIX = "/en/docs"

# Hugo often emits unquoted href attributes.
HREF_RE = re.compile(
    r"""href\s*=\s*(?:"([^"]+)"|'([^']+)'|([^\s<>"']+))""",
    re.IGNORECASE,
)


def _normalize_doc_url(href: str) -> Optional[str]:
    href = href.split("#", 1)[0].strip()
    if not href:
        return None
    if href.startswith("http://"):
        href = "https://" + href[len("http://") :]
    if href.startswith(BASE):
        path = urlparse(href).path
    elif href.startswith("/"):
        path = href
    else:
        return None
    if path.endswith("/index.html"):
        path = path[: -len("index.html")].rstrip("/")
    if not (path == DOCS_PREFIX or path.startswith(DOCS_PREFIX + "/")):
        return None
    lower = path.lower()
    if lower.endswith(".xml") or ".xml/" in lower:
        return None
    if not path.endswith("/"):
        path = path + "/"
    return BASE + path


def crawl_doc_urls(client: httpx.Client) -> list[str]:
    seeds = [BASE + DOCS_PREFIX + "/"]
    seen: set[str] = set()
    q: deque[str] = deque(seeds)
    while q:
        url = q.popleft()
        if url in seen:
            continue
        seen.add(url)
        response = client.get(url)
        if response.status_code != 200:
            sys.stderr.write(f"skip (HTTP {response.status_code}): {url}\n")
            continue
        for match in HREF_RE.finditer(response.text):
            raw = next(g for g in match.groups() if g is not None)
            normalized = _normalize_doc_url(raw)
            if normalized and normalized not in seen:
                q.append(normalized)
    return sorted(seen)


def url_tail(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    assert path.startswith(DOCS_PREFIX)
    tail = path[len(DOCS_PREFIX) :].lstrip("/")
    return tail


def url_to_docname(url: str) -> str:
    tail = url_tail(url)
    if not tail:
        return "rest_api/quickstart"
    return "rest_api/" + tail.replace("/", "/")


def download_path_for_url(repo_root: Path, url: str) -> Path:
    rel = urlparse(url).path.lstrip("/")
    return repo_root / "docs" / "_downloads" / "gitcode-en-docs" / rel / "index.html"


def rst_path_for_docname(docs_dir: Path, docname: str) -> Path:
    return docs_dir / (docname + ".rst")


def extract_main_content_html(page_html: str) -> str:
    soup = BeautifulSoup(page_html, "html.parser")
    main = soup.select_one("main.prose div.content") or soup.select_one("div.content")
    if main is None:
        raise ValueError("Could not find main content div (.content)")
    parts: list[str] = []
    for child in main.children:
        name = getattr(child, "name", None)
        if name is not None:
            parts.append(str(child))
    if not parts:
        return str(main)
    return "".join(parts)


def _strip_empty_highlight_code_blocks(lines: list[str]) -> list[str]:
    out: list[str] = []
    idx = 0
    while idx < len(lines):
        if lines[idx].strip() == ".. container:: highlight" and idx + 1 < len(lines) and lines[idx + 1] == "":
            j = idx + 2
            if j < len(lines) and lines[j].lstrip().startswith(".. code::"):
                code_indent = len(lines[j]) - len(lines[j].lstrip())
                k = j + 1
                while k < len(lines) and lines[k].strip() == "":
                    k += 1
                if k >= len(lines):
                    idx = k
                    continue
                next_indent = len(lines[k]) - len(lines[k].lstrip())
                if lines[k].strip() and next_indent <= code_indent:
                    idx = k
                    continue
        out.append(lines[idx])
        idx += 1
    return out


def repair_rst(rst: str) -> str:
    """Fix pandoc RST patterns that break docutils (nested rubrics with body text)."""
    rst = rst.replace(".. code:: chroma", ".. code:: text")
    lines = _strip_empty_highlight_code_blocks(rst.splitlines())
    out: list[str] = []
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        stripped = line.lstrip()
        if stripped.startswith(".. rubric::"):
            title = stripped[len(".. rubric::") :].strip()
            j = idx + 1
            if j < len(lines) and lines[j].strip().startswith(":name:"):
                j += 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            base_indent = len(line) - len(line.lstrip())
            body_lines: list[str] = []
            while j < len(lines):
                nxt = lines[j]
                if nxt.strip() == "":
                    if body_lines:
                        peek = j + 1
                        if peek < len(lines) and (len(lines[peek]) - len(lines[peek].lstrip())) > base_indent:
                            body_lines.append(nxt)
                            j += 1
                            continue
                    break
                indent = len(nxt) - len(nxt.lstrip())
                if indent <= base_indent and nxt.strip() and not nxt.lstrip().startswith("."):
                    break
                if indent > base_indent and body_lines == [] and nxt.lstrip().startswith(".."):
                    break
                if indent > base_indent:
                    body_lines.append(nxt[base_indent + 4 :] if len(nxt) > base_indent + 4 else nxt.lstrip())
                j += 1
            if body_lines:
                pad = " " * base_indent
                out.append(f"{pad}**{title}**")
                out.append("")
                out.extend(body_lines)
                if out and out[-1].strip() != "":
                    out.append("")
                idx = j
                continue
            out.append(line)
            idx = j
            continue
        out.append(line)
        idx += 1
    cleaned: list[str] = []
    for line in out:
        if re.match(r"^\.\. _[A-Za-z0-9_.-]+:\s*$", line):
            continue
        cleaned.append(line)
    cleaned = _strip_empty_highlight_code_blocks(cleaned)
    return "\n".join(cleaned).strip() + "\n"


def html_to_rst(html_fragment: str) -> str:
    pandoc = shutil.which("pandoc")
    if pandoc is None:
        raise RuntimeError("pandoc is required on PATH to convert HTML fragments to RST")
    wrapped = "<!DOCTYPE html><html><head><meta charset=utf-8></head><body>" + html_fragment + "</body></html>"
    completed = subprocess.run(
        [pandoc, "-f", "html", "-t", "rst"],
        input=wrapped,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr or "pandoc failed")
    return repair_rst(completed.stdout.strip() + "\n")


def write_rst(
    *,
    docs_dir: Path,
    docname: str,
    source_url: str,
    body_rst: str,
) -> None:
    path = rst_path_for_docname(docs_dir, docname)
    path.parent.mkdir(parents=True, exist_ok=True)
    footer = (
        "\n\n.. This page was generated from upstream GitCode Help documentation.\n"
        f".. Source URL: {source_url}\n"
        ".. Do not edit by hand; re-run scripts/build_gitcode_sphinx_docs.py\n"
    )
    path.write_text(body_rst.rstrip() + footer, encoding="utf-8")


def write_master_index(docs_dir: Path, docnames: list[str]) -> None:
    lines = [
        "GitCode REST API",
        "================",
        "",
        "This Sphinx project mirrors the public English REST API documentation published at",
        "`GitCode Help Docs <https://docs.gitcode.com/en/docs/>`__.",
        "",
        "Upstream guide (authentication, versioning, status codes):",
        "`GitCode REST API Guide <https://docs.gitcode.com/en/docs/guide/>`__.",
        "",
        ".. toctree::",
        "   :maxdepth: 3",
        "   :caption: API reference",
        "",
    ]
    for name in docnames:
        lines.append(f"   {name}")
    lines.extend(["", "Indices and tables", "==================", "", "* :ref:`genindex`", ""])
    (docs_dir / "index.rst").write_text("\n".join(lines), encoding="utf-8")


def write_conf(docs_dir: Path) -> None:
    text = """import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

project = "GitCode REST API"
author = "GitCode (upstream documentation); mirrored for Sphinx"
copyright = "2025, GitCode"

extensions = [
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "_downloads"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

language = "en"

nitpicky = False
"""
    (docs_dir / "conf.py").write_text(text, encoding="utf-8")
    static = docs_dir / "_static"
    static.mkdir(parents=True, exist_ok=True)
    tmpl = docs_dir / "_templates"
    tmpl.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (default: parent of scripts/)",
    )
    args = parser.parse_args()
    repo_root: Path = args.repo_root
    docs_dir = repo_root / "docs"

    if shutil.which("pandoc") is None:
        sys.stderr.write("error: pandoc not found on PATH\n")
        return 1

    client = httpx.Client(follow_redirects=True, timeout=60.0)
    try:
        urls = crawl_doc_urls(client)
    finally:
        client.close()

    if not urls:
        sys.stderr.write("error: no documentation URLs discovered\n")
        return 1

    sys.stderr.write(f"Discovered {len(urls)} documentation URLs.\n")

    rest_dir = docs_dir / "rest_api"
    if rest_dir.exists():
        shutil.rmtree(rest_dir)
    rest_dir.mkdir(parents=True, exist_ok=True)

    docnames: list[str] = []
    for url in urls:
        docname = url_to_docname(url)
        docnames.append(docname)
        response = httpx.get(url, follow_redirects=True, timeout=60.0)
        response.raise_for_status()
        raw_path = download_path_for_url(repo_root, url)
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_text(response.text, encoding="utf-8")
        fragment = extract_main_content_html(response.text)
        rst_body = html_to_rst(fragment)
        write_rst(docs_dir=docs_dir, docname=docname, source_url=url, body_rst=rst_body)

    docnames = sorted(set(docnames))
    write_conf(docs_dir)
    write_master_index(docs_dir, docnames)
    sys.stderr.write(f"Wrote {len(docnames)} RST files under {docs_dir / 'rest_api'}.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
