"""Public package exports for the GitCode SDK."""

import re
from importlib.metadata import metadata
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

package_meta = metadata("gitcode_api")
package_desc = cast(str, package_meta.get("Description"))
readme_uuids = re.findall(r"\&uuid=(\w+)", package_desc, flags=re.ASCII)
__build_hash__ = readme_uuids[0] if readme_uuids else "unknown"
__version__ = cast(str, package_meta.get("Version")).strip()

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
