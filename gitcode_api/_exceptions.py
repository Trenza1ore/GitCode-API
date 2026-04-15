"""Custom exceptions raised by the GitCode SDK."""

from typing import Any, Optional


class GitCodeError(Exception):
    """Base exception for all GitCode SDK errors."""


class GitCodeConfigurationError(GitCodeError):
    """Raised when client configuration is incomplete or invalid."""


class GitCodeAPIError(GitCodeError):
    """Raised when the GitCode API returns an error response.

    :param message: Human-readable error message.
    :param status_code: HTTP status code returned by the API.
    :param request_id: Optional GitCode request identifier.
    :param payload: Parsed error payload when available.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        request_id: Optional[str] = None,
        payload: Any = None,
    ) -> None:
        """Store structured error metadata from a failed API response."""
        super().__init__(message)
        self.status_code = status_code
        self.request_id = request_id
        self.payload = payload


class GitCodeHTTPStatusError(GitCodeAPIError):
    """Raised for non-success HTTP responses from the GitCode API."""
