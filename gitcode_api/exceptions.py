"""Exception classes for the GitCode SDK."""

from gitcode_api._exceptions import (
    GitCodeAPIError,
    GitCodeConfigurationError,
    GitCodeError,
    GitCodeHTTPStatusError,
    GitCodeTokenError,
    GitCodeUnauthorizedError,
)

__all__ = [
    "GitCodeAPIError",
    "GitCodeConfigurationError",
    "GitCodeError",
    "GitCodeHTTPStatusError",
    "GitCodeTokenError",
    "GitCodeUnauthorizedError",
]
