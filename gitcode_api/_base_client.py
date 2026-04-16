"""Shared transport helpers for the GitCode SDK.

The classes in this module normalize authentication, URL construction,
payload cleanup, and response parsing for both sync and async clients.
"""

import os
from typing import Any, Callable, Dict, Optional, Tuple, Union
from urllib.parse import quote

import httpx

from ._exceptions import GitCodeConfigurationError, GitCodeHTTPStatusError

DEFAULT_BASE_URL = "https://api.gitcode.com/api/v5"
DEFAULT_TIMEOUT = 30.0
DEFAULT_TOKEN_ENV = "GITCODE_ACCESS_TOKEN"


def _drop_none_values(mapping: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of ``mapping`` without keys that have ``None`` values."""
    return {key: value for key, value in mapping.items() if value is not None}


class BaseGitCodeClient:
    """Base configuration shared by synchronous and asynchronous clients.

    :param api_key: Personal access token for the GitCode API.
    :param owner: Default repository owner for repository-scoped calls.
    :param repo: Default repository name for repository-scoped calls.
    :param base_url: Base URL for the GitCode REST API.
    :param timeout: Request timeout in seconds.
    :param decrypt: Optional decryption function for encrypted access token.
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: Optional[float] = None,
        decrypt: Optional[Callable] = None,
    ) -> None:
        """Store client configuration and resolve authentication."""
        self.api_key = self._resolve_api_key(api_key, decrypt)
        self.owner = owner
        self.repo = repo
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout if timeout is not None else DEFAULT_TIMEOUT

    def _resolve_api_key(self, api_key: Optional[str], decrypt: Optional[Callable] = None) -> str:
        """Resolve the access token from an argument or environment variable."""
        token = api_key or os.getenv(DEFAULT_TOKEN_ENV)
        if callable(decrypt):
            token = decrypt(token)
        if not token:
            raise GitCodeConfigurationError("No API key provided. Pass api_key=... or set GITCODE_ACCESS_TOKEN.")
        return str(token)

    def _resolve_repo_context(
        self,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> Tuple[str, str]:
        """Return the effective repository owner and name for a request."""
        resolved_owner = owner or self.owner
        resolved_repo = repo or self.repo
        if not resolved_owner or not resolved_repo:
            raise GitCodeConfigurationError(
                "Repository methods require owner and repo, either per-call or on the client."
            )
        return resolved_owner, resolved_repo

    def _headers(self, extra_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Build request headers for authenticated JSON API calls."""
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def _encode_segment(self, value: Union[int, str]) -> str:
        """Percent-encode a single URL path segment."""
        return quote(str(value), safe="")

    def _encode_path_value(self, value: str) -> str:
        """Percent-encode a repository path while preserving slashes."""
        return quote(value, safe="/")

    def _join_path(self, *segments: Union[int, str]) -> str:
        """Join URL path segments into an API path."""
        return "/" + "/".join(self._encode_segment(segment) for segment in segments)

    def _repo_path(
        self,
        *segments: Union[int, str],
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> str:
        """Build a path under ``/repos/{owner}/{repo}``."""
        resolved_owner, resolved_repo = self._resolve_repo_context(owner, repo)
        return self._join_path("repos", resolved_owner, resolved_repo, *segments)

    def _repo_file_path(
        self,
        prefix: str,
        file_path: str,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> str:
        """Build a file-oriented repository path such as ``contents`` or ``raw``."""
        resolved_owner, resolved_repo = self._resolve_repo_context(owner, repo)
        return (
            f"/repos/{self._encode_segment(resolved_owner)}/"
            f"{self._encode_segment(resolved_repo)}/{self._encode_segment(prefix)}/"
            f"{self._encode_path_value(file_path)}"
        )

    def _path(self, *segments: Union[int, str]) -> str:
        """Build a non-repository API path."""
        return self._join_path(*segments)

    def _full_url(self, path: str) -> str:
        """Return an absolute URL for a relative API path."""
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self.base_url}{path}"

    def _coerce_payload(
        self,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Optional[Dict[str, Any]], Any, Optional[Dict[str, Any]]]:
        """Drop ``None`` values from params and form payloads before sending."""
        clean_params = _drop_none_values(params or {}) or None
        clean_data = _drop_none_values(data or {}) or None
        return clean_params, json, clean_data

    def _raise_for_error(self, response: httpx.Response) -> None:
        """Raise a typed SDK error for non-successful HTTP responses."""
        if response.is_success:
            return

        payload: Any
        message = response.text
        try:
            payload = response.json()
            if isinstance(payload, dict) and payload.get("message"):
                message = str(payload["message"])
        except ValueError:
            payload = response.text

        raise GitCodeHTTPStatusError(
            message or f"GitCode API request failed with status {response.status_code}.",
            status_code=response.status_code,
            request_id=response.headers.get("X-Request-Id"),
            payload=payload,
        )

    def _parse_response(self, response: httpx.Response, *, raw: bool = False) -> Any:
        """Parse a GitCode API response as raw bytes, JSON, text, or ``None``."""
        self._raise_for_error(response)
        if response.status_code == 204:
            return None
        if raw:
            return response.content
        if not response.content:
            return None
        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type or "text/json" in content_type:
            return response.json()
        try:
            return response.json()
        except ValueError:
            return response.text


class SyncAPIClient(BaseGitCodeClient):
    """Low-level synchronous HTTP transport used by resource classes.

    :param api_key: Personal access token for the GitCode API.
    :param owner: Default repository owner for repository-scoped calls.
    :param repo: Default repository name for repository-scoped calls.
    :param base_url: Base URL for the GitCode REST API.
    :param timeout: Request timeout in seconds.
    :param http_client: Optional pre-configured ``httpx.Client`` instance.
    :param decrypt: Optional decryption function for encrypted access token.
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: Optional[float] = None,
        http_client: Optional[httpx.Client] = None,
        decrypt: Optional[Callable] = None,
    ) -> None:
        """Create or reuse an ``httpx.Client`` for synchronous requests."""
        super().__init__(api_key=api_key, owner=owner, repo=repo, base_url=base_url, timeout=timeout, decrypt=decrypt)
        self._owns_client = http_client is None
        self._client = http_client or httpx.Client(timeout=self.timeout)

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        raw: bool = False,
    ) -> Any:
        """Send an HTTP request to the GitCode API and parse the response.

        :param method: HTTP method such as ``"GET"`` or ``"POST"``.
        :param path: Relative API path or absolute URL.
        :param params: Optional query parameters.
        :param json: Optional JSON request body.
        :param data: Optional form payload.
        :param headers: Optional extra HTTP headers.
        :param raw: When ``True``, return response bytes instead of parsed JSON.
        :returns: Parsed JSON payload, raw bytes, text, or ``None``.
        """
        clean_params, clean_json, clean_data = self._coerce_payload(params=params, json=json, data=data)
        response = self._client.request(
            method,
            self._full_url(path),
            params=clean_params,
            json=clean_json,
            data=clean_data,
            headers=self._headers(headers),
        )
        return self._parse_response(response, raw=raw)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> "SyncAPIClient":
        """Enter a context manager and return the client instance."""
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        """Close the client when leaving a context manager."""
        self.close()


class AsyncAPIClient(BaseGitCodeClient):
    """Low-level asynchronous HTTP transport used by async resource classes.

    :param api_key: Personal access token for the GitCode API.
    :param owner: Default repository owner for repository-scoped calls.
    :param repo: Default repository name for repository-scoped calls.
    :param base_url: Base URL for the GitCode REST API.
    :param timeout: Request timeout in seconds.
    :param http_client: Optional pre-configured ``httpx.AsyncClient`` instance.
    :param decrypt: Optional decryption function for encrypted access token.
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: Optional[float] = None,
        http_client: Optional[httpx.AsyncClient] = None,
        decrypt: Optional[Callable] = None,
    ) -> None:
        """Create or reuse an ``httpx.AsyncClient`` for asynchronous requests."""
        super().__init__(api_key=api_key, owner=owner, repo=repo, base_url=base_url, timeout=timeout, decrypt=decrypt)
        self._owns_client = http_client is None
        self._client = http_client or httpx.AsyncClient(timeout=self.timeout)

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        raw: bool = False,
    ) -> Any:
        """Send an asynchronous HTTP request to the GitCode API.

        :param method: HTTP method such as ``"GET"`` or ``"POST"``.
        :param path: Relative API path or absolute URL.
        :param params: Optional query parameters.
        :param json: Optional JSON request body.
        :param data: Optional form payload.
        :param headers: Optional extra HTTP headers.
        :param raw: When ``True``, return response bytes instead of parsed JSON.
        :returns: Parsed JSON payload, raw bytes, text, or ``None``.
        """
        clean_params, clean_json, clean_data = self._coerce_payload(params=params, json=json, data=data)
        response = await self._client.request(
            method,
            self._full_url(path),
            params=clean_params,
            json=clean_json,
            data=clean_data,
            headers=self._headers(headers),
        )
        return self._parse_response(response, raw=raw)

    async def close(self) -> None:
        """Close the underlying async HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncAPIClient":
        """Enter an async context manager and return the client instance."""
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        """Close the client when leaving an async context manager."""
        await self.close()
