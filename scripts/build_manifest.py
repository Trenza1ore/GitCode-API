"""Fill ``scripts/manifest.json`` from ``pyproject.toml`` using a JSON template with placeholders.

Template string fields use ``{{TOKEN}}`` markers (see ``PLACEHOLDER_SOURCES``). ``keywords`` and
``license`` are overwritten from pyproject after placeholder substitution.

Requires Python 3.11+ for stdlib ``tomllib``, or install ``tomli`` for 3.9–3.10.
"""

import json
from pathlib import Path
from typing import Any, Dict, Mapping, MutableMapping, Tuple

import tomllib

SCRIPT_DIR = Path(__file__).resolve().parent
BUILD_DIR = SCRIPT_DIR.parent
PYPROJECT_PATH = BUILD_DIR / "pyproject.toml"
MANIFEST_TEMPLATE_PATH = SCRIPT_DIR / "manifest.json"
MANIFEST_PATH = BUILD_DIR / "manifest.json"

# Maps placeholder token -> key path: ``(section, key)`` where section is ``project``,
# ``urls`` (under ``[project.urls]``), or ``author`` (first ``[project.authors]`` entry).
PLACEHOLDER_SOURCES: Dict[str, Tuple[str, str]] = {
    "{{VERSION}}": ("project", "version"),
    "{{AUTHOR_NAME}}": ("author", "name"),
    "{{AUTHOR_EMAIL}}": ("author", "email"),
    "{{AUTHOR_URL}}": ("urls", "author"),
    "{{HOMEPAGE}}": ("urls", "homepage"),
    "{{DOCUMENTATION}}": ("urls", "documentation"),
    "{{SUPPORT}}": ("urls", "issues"),
    "{{REPOSITORY_URL}}": ("urls", "github"),
}

MCPB_IGNORE_CONTENT = """
.*/
.*
**/__pycache__/

# Build
build/
dist/
gitcode_api.egg-info/

# Scaffoldings, I guess?
docs/
examples/
tests/
scripts/
Makefile
*.md
*.mcpb
*.spec
test.py
uv.lock
"""


def normalize_license(license_obj: Any) -> str:
    """Coerce PEP 621 ``license`` to a string for JSON."""
    if isinstance(license_obj, str):
        return license_obj
    if isinstance(license_obj, dict):
        text = license_obj.get("text")
        if isinstance(text, str):
            return text
    return ""


def load_pyproject(path: Path) -> Dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def _first_author(project: Mapping[str, Any]) -> Mapping[str, Any]:
    authors = project.get("authors")
    if not isinstance(authors, list) or not authors:
        raise ValueError("pyproject.toml [project] must include at least one [[project.authors]] entry")
    first = authors[0]
    if not isinstance(first, dict):
        raise ValueError("project.authors[0] must be a TOML inline table")
    return first


def build_replacements(pyproject: Mapping[str, Any]) -> Dict[str, str]:
    project = pyproject.get("project")
    if not isinstance(project, dict):
        raise ValueError("pyproject.toml must contain a [project] table")

    urls = project.get("urls")
    if not isinstance(urls, dict):
        urls = {}

    first_author = _first_author(project)
    github = urls.get("github")
    if not isinstance(github, str) or not github.strip():
        raise ValueError('pyproject.toml [project.urls] must define github = "..."')

    out: Dict[str, str] = {}
    for token, spec in PLACEHOLDER_SOURCES.items():
        section, key = spec
        if section == "project":
            value = project.get(key)
        elif section == "urls":
            value = urls.get(key)
        elif section == "author":
            value = first_author.get(key)
        else:
            value = None
        if value is None:
            raise ValueError(f"Missing pyproject value for placeholder {token} ({section}.{key})")
        if not isinstance(value, str):
            raise ValueError(f"Expected string for {token}, got {type(value).__name__}")
        out[token] = value
    return out


def substitute_placeholders(obj: Any, replacements: Mapping[str, str]) -> Any:
    if isinstance(obj, str):
        result = obj
        for token, value in replacements.items():
            result = result.replace(token, value)
        return result
    if isinstance(obj, list):
        return [substitute_placeholders(item, replacements) for item in obj]
    if isinstance(obj, dict):
        return {k: substitute_placeholders(v, replacements) for k, v in obj.items()}
    return obj


def apply_project_lists(manifest: MutableMapping[str, Any], project: Mapping[str, Any]) -> None:
    keywords = project.get("keywords", [])
    if not isinstance(keywords, list):
        raise ValueError("project.keywords must be a TOML array of strings")
    for i, item in enumerate(keywords):
        if not isinstance(item, str):
            raise ValueError(f"project.keywords[{i}] must be a string")
    manifest["keywords"] = list(keywords)

    manifest["license"] = normalize_license(project.get("license"))


def build_manifest_dict(pyproject_path: Path, template_path: Path) -> Dict[str, Any]:
    pyproject = load_pyproject(pyproject_path)
    project = pyproject["project"]
    if not isinstance(project, dict):
        raise ValueError("pyproject.toml must contain a [project] table")

    with template_path.open(encoding="utf-8") as handle:
        manifest: Dict[str, Any] = json.load(handle)

    replacements = build_replacements(pyproject)
    manifest = substitute_placeholders(manifest, replacements)
    apply_project_lists(manifest, project)
    return manifest


def write_manifest(manifest: Mapping[str, Any], output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    (output_path.parent / ".mcpbignore").write_text(MCPB_IGNORE_CONTENT, encoding="utf-8", newline="\n")


def main() -> None:
    manifest = build_manifest_dict(PYPROJECT_PATH, MANIFEST_TEMPLATE_PATH)
    write_manifest(manifest, MANIFEST_PATH)


if __name__ == "__main__":
    main()
