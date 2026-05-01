"""CLI entry for PyInstaller (top-level script; package __main__ uses relative imports)."""

from gitcode_api.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
