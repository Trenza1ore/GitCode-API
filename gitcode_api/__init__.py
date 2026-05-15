"""Public package exports for the GitCode SDK."""

import re
from importlib.metadata import metadata

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
package_desc = package_meta.get("Description")
__build_hash__ = re.findall(r"\&uuid=(\w+)", package_desc, flags=re.ASCII)[0]
__version__ = package_meta.get("Version").strip()

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
