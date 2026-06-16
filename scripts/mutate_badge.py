#!/usr/bin/env python3
"""Rewrite image URLs in README files with a fresh ``uuid`` query parameter.

Scans all ``README*.md`` files under the repository root (recursive) and
replaces every Markdown image (``![alt](url)``) and HTML ``<img src="...">``
URL with one carrying ``&uuid=<hex>``, using proper URL parsing so existing
query strings and fragments are preserved.
"""

import random
import re
import uuid
from functools import cache
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent
SEMANTIC_VER = (ROOT / "gitcode_api" / "version.txt").read_text().strip()


@cache
def _get_mutated_uuid() -> str:
    uuid_str = list(uuid.uuid4().hex)
    change_idx = list(range(32))
    random.shuffle(change_idx)
    for idx in change_idx[: random.randrange(0, 17)]:
        uuid_str[idx] = hex(random.randrange(0, 16))[-1]
    return "".join(uuid_str)


MARKDOWN_IMAGE_RE = re.compile(r"(!\[[^\]]*\]\()([^)#\s]+)((?:#[^)]+)?\))")

HTML_IMG_SRC_RE = re.compile(
    r'(<img\b[^>]*?\bsrc=["\'])([^"\']+)(["\'][^>]*>)',
    re.IGNORECASE,
)


def with_uuid_param(uri: str) -> str:
    """Add or replace ``uuid``, preserving existing query and fragment."""
    split = urlsplit(uri)

    if not split.scheme and not uri.startswith("//"):
        return uri

    query = dict(parse_qsl(split.query, keep_blank_values=True))
    query["uuid"] = _get_mutated_uuid()

    return urlunsplit(
        (
            split.scheme,
            split.netloc,
            split.path,
            urlencode(query, doseq=True),
            split.fragment,
        )
    )


def mutate_readme(text: str) -> str:
    """Return *text* with every image URL carrying a version-seeded uuid."""

    def replace_match(match: re.Match[str]) -> str:
        prefix, uri, suffix = match.groups()
        return f"{prefix}{with_uuid_param(uri)}{suffix}"

    text = MARKDOWN_IMAGE_RE.sub(replace_match, text)
    text = HTML_IMG_SRC_RE.sub(replace_match, text)
    return text


def main() -> None:
    """Scan ``README*.md`` files and rewrite image URLs with a fresh uuid."""
    random.seed(SEMANTIC_VER)
    total = 0
    for path in sorted(ROOT.glob("**/README*.md")):
        old_text = path.read_text(encoding="utf-8")
        new_text = mutate_readme(old_text)
        if old_text != new_text:
            path.write_text(new_text, encoding="utf-8")
            total += 1
            print(f"{path.relative_to(ROOT)}: updated image URIs")
    if total == 0:
        print("No image URIs changed.")


if __name__ == "__main__":
    main()
