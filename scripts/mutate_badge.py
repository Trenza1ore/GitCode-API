#!/usr/bin/env python3
"""Rewrite pepy.tech personalized badge URLs with a new uuid query segment.

Scans all ``README*.md`` files under the repository root (recursive) and applies
``re.sub`` so each matched badge URL ends with ``&uuid=<new hex>`` before the
closing parenthesis in Markdown links.
"""

import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BADGES = [
    re.compile(
        r"(https://static\.pepy\.tech/personalized-badge/gitcode-api\?"
        r"period=total&units=INTERNATIONAL_SYSTEM&left_color=GRAY&right_color=RED&left_text=downloads)"
        r"[^)]*"
        r"(\))",
    ),
    re.compile(
        r"(https://img\.shields\.io/pypi/v/gitcode-api\?"
        r"link=https%3A%2F%2Fpypi\.org%2Fproject%2Fgitcode-api%2F)"
        r"[^)]*"
        r"(\))",
    )
]


def main() -> None:
    total = 0
    for path in sorted(ROOT.glob("**/README*.md")):
        new_text = path.read_text(encoding="utf-8")
        n_total = 0
        for badge in BADGES:
            new_text, n = badge.subn(
                lambda m: m.group(1) + "&uuid=" + uuid.uuid4().hex + m.group(2),
                new_text,
            )
            n_total += n
        if n_total:
            path.write_text(new_text, encoding="utf-8")
            total += n_total
            print(f"{path.relative_to(ROOT)}: {n_total} replacement(s)")
    if total == 0:
        print("No matches.")


if __name__ == "__main__":
    main()
