"""Offline tests for ``scripts/build_manifest.py``."""

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_BUILD_MANIFEST_PATH = ROOT / "scripts" / "build_manifest.py"
_spec = importlib.util.spec_from_file_location("build_manifest", _BUILD_MANIFEST_PATH)
assert _spec and _spec.loader
_build_manifest = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_build_manifest)


MINIMAL_PYPROJECT = b"""\
[project]
name = "demo-pkg"
version = "9.8.7"
description = "Demo description line."
keywords = ["alpha", "beta"]
license = "MIT"
authors = [{ name = "Alice Example", email = "alice@example.com" }]

[project.urls]
homepage = "https://example.com/home"
documentation = "https://example.com/docs"
github = "https://github.com/org/demo"
author = "https://example.com/~alice"
issues = "https://github.com/org/demo/issues"
"""

MINIMAL_TEMPLATE = {
    "version": "{{VERSION}}",
    "description": "Static manifest description (not from pyproject placeholders).",
    "author": {
        "name": "{{AUTHOR_NAME}}",
        "email": "{{AUTHOR_EMAIL}}",
        "url": "{{AUTHOR_URL}}",
    },
    "homepage": "{{HOMEPAGE}}",
    "documentation": "{{DOCUMENTATION}}",
    "support": "{{SUPPORT}}",
    "repository": {"type": "git", "url": "{{REPOSITORY_URL}}"},
    "keywords": [],
    "license": "",
}


def test_build_manifest_dict_substitutes_and_lists(tmp_path: Path) -> None:
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_bytes(MINIMAL_PYPROJECT)
    template_path = tmp_path / "manifest.in.json"
    template_path.write_text(json.dumps(MINIMAL_TEMPLATE), encoding="utf-8")

    manifest = _build_manifest.build_manifest_dict(pyproject_path, template_path)

    assert manifest["version"] == "9.8.7"
    assert manifest["description"] == "Static manifest description (not from pyproject placeholders)."
    assert manifest["author"]["name"] == "Alice Example"
    assert manifest["author"]["email"] == "alice@example.com"
    assert manifest["author"]["url"] == "https://example.com/~alice"
    assert manifest["homepage"] == "https://example.com/home"
    assert manifest["documentation"] == "https://example.com/docs"
    assert manifest["support"] == "https://github.com/org/demo/issues"
    assert manifest["repository"]["url"] == "https://github.com/org/demo"
    assert manifest["keywords"] == ["alpha", "beta"]
    assert manifest["license"] == "MIT"


def test_write_manifest_ensure_ascii_utf8(tmp_path: Path) -> None:
    out = tmp_path / "out.json"
    _build_manifest.write_manifest({"note": "café"}, out)
    text = out.read_text(encoding="utf-8")
    assert "café" in text
    assert text.endswith("\n")


def test_missing_github_raises(tmp_path: Path) -> None:
    bad = b"""\
[project]
name = "x"
version = "1"
description = "d"
authors = [{ name = "A", email = "a@b.c" }]
"""
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_bytes(bad)
    template_path = tmp_path / "manifest.in.json"
    template_path.write_text(json.dumps(MINIMAL_TEMPLATE), encoding="utf-8")

    with pytest.raises(ValueError, match="github"):
        _build_manifest.build_manifest_dict(pyproject_path, template_path)
