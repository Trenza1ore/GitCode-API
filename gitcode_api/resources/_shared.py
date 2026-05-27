"""Shared resource base classes for the GitCode SDK."""

from typing import Any, Dict, List, Optional, Pattern, Tuple, Union

from .._base_client import AsyncAPIClient, SyncAPIClient
from .._base_resource import BaseResource
from .._exceptions import GitCodeHTTPStatusError
from .._models import APIObject, ModelT, as_model, as_model_list
from ..constants import GITCODE_TEMPLATE_REPO


def _parse_parent_owner_repo(repo_obj: Any) -> Optional[Tuple[str, str]]:
    parent = getattr(repo_obj, "parent", None)
    if parent is None and hasattr(repo_obj, "get"):
        parent = repo_obj.get("parent")
    if not isinstance(parent, dict):
        return None
    full = str(parent.get("full_name") or "").strip()
    if "/" not in full:
        return None
    owner_path, name = full.rsplit("/", 1)
    owner_path, name = owner_path.strip(), name.strip()
    if not owner_path or not name:
        return None
    return owner_path, name


def _resolution_sources_sync(client: SyncAPIClient, owner: str, repo: str) -> List[Tuple[str, str]]:
    """Build ordered repo candidates.

    Starts with ``(owner, repo)`` and ``(owner, ".gitcode")``. For every candidate that is a
    fork (per ``GET /repos/{owner}/{repo}``), appends that repository's parent main repo and
    ``(parent_owner, ".gitcode")`` when not already listed (deduplicated, breadth-first).
    """
    from .repositories import ReposResource

    sources: List[Tuple[str, str]] = []
    seen: set[Tuple[str, str]] = set()

    def add(pair: Tuple[str, str]) -> None:
        if pair not in seen:
            seen.add(pair)
            sources.append(pair)

    add((owner, repo))
    add((owner, GITCODE_TEMPLATE_REPO))

    max_candidates = 64
    index = 0
    while index < len(sources) and len(sources) < max_candidates:
        so, sr = sources[index]
        index += 1
        try:
            meta = ReposResource(client).get(owner=so, repo=sr)
        except GitCodeHTTPStatusError:
            continue
        if not getattr(meta, "fork", None):
            continue
        parsed = _parse_parent_owner_repo(meta)
        if not parsed:
            continue
        po, pr = parsed
        add((po, pr))
        add((po, GITCODE_TEMPLATE_REPO))

    return sources


async def _resolution_sources_async(client: AsyncAPIClient, owner: str, repo: str) -> List[Tuple[str, str]]:
    """Async counterpart of :func:`_resolution_sources_sync`."""
    from .repositories import AsyncReposResource

    sources: List[Tuple[str, str]] = []
    seen: set[Tuple[str, str]] = set()

    def add(pair: Tuple[str, str]) -> None:
        if pair not in seen:
            seen.add(pair)
            sources.append(pair)

    add((owner, repo))
    add((owner, GITCODE_TEMPLATE_REPO))

    max_candidates = 64
    index = 0
    while index < len(sources) and len(sources) < max_candidates:
        so, sr = sources[index]
        index += 1
        try:
            meta = await AsyncReposResource(client).get(owner=so, repo=sr)
        except GitCodeHTTPStatusError:
            continue
        if not getattr(meta, "fork", None):
            continue
        parsed = _parse_parent_owner_repo(meta)
        if not parsed:
            continue
        po, pr = parsed
        add((po, pr))
        add((po, GITCODE_TEMPLATE_REPO))

    return sources


def _walk_dot_gitcode_contents_sync(
    client: SyncAPIClient,
    template_owner: str,
    template_repo: str,
    path: str,
    acc: List[Tuple[str, str, str, str]],
) -> None:
    try:
        data = client.request(
            "GET",
            client._repo_file_path("contents", path, owner=template_owner, repo=template_repo),
        )
    except GitCodeHTTPStatusError as exc:
        if exc.status_code == 404:
            return
        raise

    if isinstance(data, dict):
        t = (data.get("type") or "").lower()
        if t == "file":
            sha = data.get("sha") or ""
            pth = data.get("path") or path
            if sha and pth:
                acc.append((template_owner, template_repo, str(pth), str(sha)))
            return
        if t in ("dir", "directory", "tree"):
            pth = data.get("path") or path
            _walk_dot_gitcode_contents_sync(client, template_owner, template_repo, pth, acc)
            return
        return

    if isinstance(data, list):
        for item in data:
            if not isinstance(item, dict):
                continue
            t = (item.get("type") or "").lower()
            pth = item.get("path") or ""
            if t == "file":
                sha = item.get("sha") or ""
                if sha and pth:
                    acc.append((template_owner, template_repo, str(pth), str(sha)))
            elif t in ("dir", "directory", "tree") and pth:
                _walk_dot_gitcode_contents_sync(client, template_owner, template_repo, str(pth), acc)


async def _walk_dot_gitcode_contents_async(
    client: AsyncAPIClient,
    template_owner: str,
    template_repo: str,
    path: str,
    acc: List[Tuple[str, str, str, str]],
) -> None:
    try:
        data = await client.request(
            "GET",
            client._repo_file_path("contents", path, owner=template_owner, repo=template_repo),
        )
    except GitCodeHTTPStatusError as exc:
        if exc.status_code == 404:
            return
        raise

    if isinstance(data, dict):
        t = (data.get("type") or "").lower()
        if t == "file":
            sha = data.get("sha") or ""
            pth = data.get("path") or path
            if sha and pth:
                acc.append((template_owner, template_repo, str(pth), str(sha)))
            return
        if t in ("dir", "directory", "tree"):
            pth = data.get("path") or path
            await _walk_dot_gitcode_contents_async(client, template_owner, template_repo, pth, acc)
            return
        return

    if isinstance(data, list):
        for item in data:
            if not isinstance(item, dict):
                continue
            t = (item.get("type") or "").lower()
            pth = item.get("path") or ""
            if t == "file":
                sha = item.get("sha") or ""
                if sha and pth:
                    acc.append((template_owner, template_repo, str(pth), str(sha)))
            elif t in ("dir", "directory", "tree") and pth:
                await _walk_dot_gitcode_contents_async(client, template_owner, template_repo, str(pth), acc)


def list_gitcode_template_rows_sync(
    client: SyncAPIClient,
    owner: str,
    repo: str,
    path_pattern: Pattern[str],
) -> List[Tuple[str, str, str, str]]:
    """Return ``(template_owner, template_repo, path, sha)`` from the first resolution source with matches."""
    for so, sr in _resolution_sources_sync(client, owner, repo):
        acc: List[Tuple[str, str, str, str]] = []
        try:
            _walk_dot_gitcode_contents_sync(client, so, sr, ".gitcode", acc)
            if sr != GITCODE_TEMPLATE_REPO:
                _walk_dot_gitcode_contents_sync(client, so, sr, ".github", acc)
        except GitCodeHTTPStatusError:
            continue
        rows = [(t_o, t_r, p, s) for t_o, t_r, p, s in acc if path_pattern.match(p)]
        if rows:
            return rows
    return []


async def list_gitcode_template_rows_async(
    client: AsyncAPIClient,
    owner: str,
    repo: str,
    path_pattern: Pattern[str],
) -> List[Tuple[str, str, str, str]]:
    """Return ``(template_owner, template_repo, path, sha)`` from the first resolution source with matches."""
    for so, sr in await _resolution_sources_async(client, owner, repo):
        acc: List[Tuple[str, str, str, str]] = []
        try:
            await _walk_dot_gitcode_contents_async(client, so, sr, ".gitcode", acc)
            if sr != GITCODE_TEMPLATE_REPO:
                await _walk_dot_gitcode_contents_async(client, so, sr, ".github", acc)
        except GitCodeHTTPStatusError:
            continue
        rows = [(t_o, t_r, p, s) for t_o, t_r, p, s in acc if path_pattern.match(p)]
        if rows:
            return rows
    return []


def get_gitcode_template_body_sync(
    client: SyncAPIClient,
    path: str,
    path_pattern: Pattern[str],
    owner: str,
    repo: str,
    encoding: str = "utf-8",
    **decoding_kwargs,
) -> str:
    """Fetch raw template text from the first resolution source that serves ``path``."""
    if not path_pattern.match(path):
        raise GitCodeHTTPStatusError(
            "Path does not match the expected GitCode template pattern for this resource.",
            status_code=404,
            payload=None,
        )
    last_error: Optional[GitCodeHTTPStatusError] = None
    for so, sr in _resolution_sources_sync(client, owner, repo):
        try:
            raw = client.request(
                "GET",
                client._repo_file_path("raw", path, owner=so, repo=sr),
                raw=True,
            )
        except GitCodeHTTPStatusError as exc:
            last_error = exc
            continue
        if isinstance(raw, bytes):
            return raw.decode(encoding=encoding, **decoding_kwargs)
        if isinstance(raw, str):
            return raw
        return str(raw)
    if last_error is not None:
        raise last_error
    raise GitCodeHTTPStatusError(
        "No template found for the given path.",
        status_code=404,
        payload=None,
    )


async def get_gitcode_template_body_async(
    client: AsyncAPIClient,
    path: str,
    path_pattern: Pattern[str],
    owner: str,
    repo: str,
    encoding: str = "utf-8",
    **decoding_kwargs,
) -> str:
    """Fetch raw template text from the first resolution source that serves ``path``."""
    if not path_pattern.match(path):
        raise GitCodeHTTPStatusError(
            "Path does not match the expected GitCode template pattern for this resource.",
            status_code=404,
            payload=None,
        )
    last_error: Optional[GitCodeHTTPStatusError] = None
    for so, sr in await _resolution_sources_async(client, owner, repo):
        try:
            raw = await client.request(
                "GET",
                client._repo_file_path("raw", path, owner=so, repo=sr),
                raw=True,
            )
        except GitCodeHTTPStatusError as exc:
            last_error = exc
            continue
        if isinstance(raw, bytes):
            return raw.decode(encoding=encoding, **decoding_kwargs)
        if isinstance(raw, str):
            return raw
        return str(raw)
    if last_error is not None:
        raise last_error
    raise GitCodeHTTPStatusError(
        "No template found for the given path.",
        status_code=404,
        payload=None,
    )


class SyncResource(BaseResource):
    """Base class for synchronous resource groups."""

    def __init__(self, client: SyncAPIClient) -> None:
        """Bind the resource to a synchronous API client."""
        self._client = client

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
        data: Optional[Dict[str, Any]] = None,
        raw: bool = False,
    ) -> Any:
        """Dispatch a low-level request through the owning client.

        :param method: HTTP verb (for example ``GET`` or ``POST``).
        :param path: Absolute or root-relative URL path.
        :param params: Optional query string parameters.
        :param json: Optional JSON-serializable request body.
        :param data: Optional form or body fields.
        :param raw: When ``True``, return the raw response body (for example bytes).
        :returns: Parsed JSON, raw body, or other value from the client.
        """
        return self._client.request(method, path, params=params, json=json, data=data, raw=raw)

    def _model(self, method: str, path: str, model_type: type[ModelT], **kwargs) -> ModelT:
        """Send a request and wrap a JSON object in ``model_type``.

        :param method: HTTP verb.
        :param path: Request path.
        :param model_type: Model class for the top-level JSON object.
        :param kwargs: Forwarded to :meth:`_request` (``params``, ``json``, ``data``, ``raw``, etc.).
        :returns: An instance of ``model_type``.
        """
        data = self._request(method, path, **kwargs)
        return as_model(data, model_type)

    def _models(self, method: str, path: str, model_type: type[ModelT], **kwargs) -> List[ModelT]:
        """Send a request and wrap a JSON array in ``model_type`` instances.

        :param method: HTTP verb.
        :param path: Request path.
        :param model_type: Model class for each element of the JSON array.
        :param kwargs: Forwarded to :meth:`_request`.
        :returns: A list of ``model_type`` instances.
        """
        data = self._request(method, path, **kwargs)
        return as_model_list(data, model_type)

    def _maybe_model(self, method: str, path: str, model_type: type[ModelT], **kwargs) -> Union[ModelT, APIObject]:
        """Wrap dict responses as models and scalar responses as ``APIObject``.

        :param method: HTTP verb.
        :param path: Request path.
        :param model_type: Model class when the response is a JSON object.
        :param kwargs: Forwarded to :meth:`_request`.
        :returns: ``model_type`` for dict bodies; otherwise ``APIObject`` wrapping a ``value`` field.
        """
        data = self._request(method, path, **kwargs)
        if isinstance(data, dict):
            return as_model(data, model_type)
        return APIObject({"value": data})


class AsyncResource(BaseResource):
    """Base class for asynchronous resource groups."""

    def __init__(self, client: AsyncAPIClient) -> None:
        """Bind the resource to an asynchronous API client."""
        self._client = client

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
        data: Optional[Dict[str, Any]] = None,
        raw: bool = False,
    ) -> Any:
        """Dispatch a low-level async request through the owning client.

        :param method: HTTP verb (for example ``GET`` or ``POST``).
        :param path: Absolute or root-relative URL path.
        :param params: Optional query string parameters.
        :param json: Optional JSON-serializable request body.
        :param data: Optional form or body fields.
        :param raw: When ``True``, return the raw response body (for example bytes).
        :returns: Parsed JSON, raw body, or other value from the client.
        """
        return await self._client.request(method, path, params=params, json=json, data=data, raw=raw)

    async def _model(self, method: str, path: str, model_type: type[ModelT], **kwargs) -> ModelT:
        """Send a request and wrap a JSON object in ``model_type``.

        :param method: HTTP verb.
        :param path: Request path.
        :param model_type: Model class for the top-level JSON object.
        :param kwargs: Forwarded to :meth:`_request`.
        :returns: An instance of ``model_type``.
        """
        data = await self._request(method, path, **kwargs)
        return as_model(data, model_type)

    async def _models(self, method: str, path: str, model_type: type[ModelT], **kwargs) -> List[ModelT]:
        """Send a request and wrap a JSON array in ``model_type`` instances.

        :param method: HTTP verb.
        :param path: Request path.
        :param model_type: Model class for each element of the JSON array.
        :param kwargs: Forwarded to :meth:`_request`.
        :returns: A list of ``model_type`` instances.
        """
        data = await self._request(method, path, **kwargs)
        return as_model_list(data, model_type)
