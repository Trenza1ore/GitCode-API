"""Public package exports for the GitCode SDK."""

import re
from importlib.metadata import PackageNotFoundError, metadata, version
from typing import cast

from . import constants
from ._client import AsyncGitCode, GitCode
from ._exceptions import (
    GitCodeAPIError,
    GitCodeConfigurationError,
    GitCodeError,
    GitCodeHTTPStatusError,
)
from .utils import as_dict

_README_UUIDS = []
_VERSION_STR = "unknown"

try:
    package_meta = metadata("gitcode_api")
    package_desc = cast(str, package_meta.get("Description"))
    _README_UUIDS = re.findall(r"\&uuid=(\w+)", package_desc, flags=re.ASCII)
    _VERSION_STR = version("gitcode_api")
except PackageNotFoundError:
    from pathlib import Path

    import tomllib

    pyproject_toml = Path(__file__).parent.parent / "pyproject.toml"
    if pyproject_toml.exists():
        _VERSION_STR = tomllib.loads(pyproject_toml.read_text(encoding="utf-8")).get("project", {}).get("version", "")
    else:
        version_file = Path(__file__).with_name("version.txt")
        if version_file.exists():
            _VERSION_STR = version_file.read_text(encoding="utf-8").strip()
    read_me_file = pyproject_toml.with_name("README.md")
    if read_me_file.exists():
        _README_UUIDS = re.findall(r"\&uuid=(\w+)", read_me_file.read_text(encoding="utf-8").strip(), flags=re.ASCII)

__build_hash__ = _README_UUIDS[0] if _README_UUIDS else "unknown"
__version__ = _VERSION_STR.strip()

__all__ = [
    "constants",
    "__version__",
    "__build_hash__",
    "AsyncGitCode",
    "GitCode",
    "GitCodeAPIError",
    "GitCodeConfigurationError",
    "GitCodeError",
    "GitCodeHTTPStatusError",
    "as_dict",
]
