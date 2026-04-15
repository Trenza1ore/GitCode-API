"""Public package exports for the GitCode SDK."""

from pathlib import Path

from ._client import AsyncGitCode, GitCode
from ._exceptions import (
    GitCodeAPIError,
    GitCodeConfigurationError,
    GitCodeError,
    GitCodeHTTPStatusError,
)

__version__ = (Path(__file__).parent / "version.txt").read_text().strip()

__all__ = [
    "__version__",
    "AsyncGitCode",
    "GitCode",
    "GitCodeAPIError",
    "GitCodeConfigurationError",
    "GitCodeError",
    "GitCodeHTTPStatusError",
]
