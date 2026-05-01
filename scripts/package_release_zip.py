#!/usr/bin/env python3
"""Build a release zip: PyInstaller binary, ``.claude/``, and README files."""

import argparse
import sys
import zipfile
from pathlib import Path
from zlib import Z_BEST_COMPRESSION

# Paths relative to repository root.
README_REL_PATHS = ("README.md", "README.zh.md")


def main() -> int:
    """Parse CLI arguments and write the release zip.

    :returns: Exit status (0 on success).
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True, help="Path to the built executable.")
    parser.add_argument("--zip", type=Path, required=True, help="Output .zip path.")
    parser.add_argument("--repo-root", type=Path, default=Path("."), help="Repository root.")
    parser.add_argument(
        "--arcname-binary",
        required=True,
        help="Archive member name for the binary (e.g. gitcode-api or gitcode-api.exe).",
    )
    args = parser.parse_args()

    root = args.repo_root.resolve()
    binary = args.binary.resolve()
    if not binary.is_file():
        print(f"error: binary not found: {binary}", file=sys.stderr)
        return 1

    claude = root / ".claude"
    if not claude.is_dir():
        print(f"error: .claude directory not found: {claude}", file=sys.stderr)
        return 1

    args.zip = args.zip.resolve()
    args.zip.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(args.zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=Z_BEST_COMPRESSION) as zf:
        zf.write(binary, arcname=args.arcname_binary)
        for path in sorted(claude.rglob("*")):
            if not path.is_file():
                continue
            if path.name == ".DS_Store" or "__pycache__" in path.parts:
                continue
            arc = path.relative_to(root)
            zf.write(path, arcname=str(arc).replace("\\", "/"))
        for rel in README_REL_PATHS:
            p = root / rel
            if p.is_file():
                zf.write(p, arcname=rel.replace("\\", "/"))
            else:
                print(f"warning: skipping missing {rel}", file=sys.stderr)

    print(f"wrote {args.zip}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
