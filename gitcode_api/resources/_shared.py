"""Shared resource base classes for the GitCode SDK."""

from functools import cached_property, lru_cache
from typing import Any, Dict, List, Optional, Union

from .._base_client import AsyncAPIClient, SyncAPIClient
from .._models import APIObject, ModelT, as_model, as_model_list

_UTILITY_METHODS = {"methods", "method_signature"}
_DATA_MODEL_PATH = "gitcode_api._models."


class SyncResource:
    """Base class for synchronous resource groups."""

    def __init__(self, client: SyncAPIClient) -> None:
        """Bind the resource to a synchronous API client."""
        self._client = client

    @cached_property
    def methods(self) -> tuple[str, ...]:
        """Public callable names on this resource group in stable SDK order.

        Ordering uses :func:`sorted` with a key derived from each name's
        underscore-separated segments (for example two-part names are ordered
        as if ``second_first``). This is not plain lexicographic order on the
        full method string. Excludes ``methods``, names starting with ``_``,
        and non-callables. The result is cached on first access.

        :returns: Tuple of method names in that order.
        """

        def _is_valid_func(name: str):
            return not (name.startswith("_") or name in _UTILITY_METHODS) and callable(getattr(self, name))

        def _sort_helper(method_name: str):
            name_parts = method_name.split("_")
            num_part = len(name_parts)
            if num_part == 2:
                return f"{name_parts[1]}_{name_parts[0]}"
            if num_part == 3:
                return f"{{{name_parts[0]}_"
            return "_" + method_name

        return tuple(
            sorted(
                (func for func in dir(self) if _is_valid_func(func)),
                key=_sort_helper,
            )
        )

    @lru_cache(maxsize=50)
    def method_signature(self, method_name: str) -> str:
        """Return signature for a method in this resource group, result is cached.

        For example ``client.pulls.method_signature("list_issues")`` would return:
        list_issues(*, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> List[Issue]

        :param method_name: Attribute name of a callable on this resource.
        :returns: Formatted signature.
        """
        import inspect

        return method_name + str(inspect.signature(getattr(self, method_name))).replace(_DATA_MODEL_PATH, "")

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


class AsyncResource:
    """Base class for asynchronous resource groups."""

    def __init__(self, client: AsyncAPIClient) -> None:
        """Bind the resource to an asynchronous API client."""
        self._client = client

    @cached_property
    def methods(self) -> tuple[str, ...]:
        """Public callable names on this resource group in stable SDK order.

        Ordering uses :func:`sorted` with a key derived from each name's
        underscore-separated segments (for example two-part names are ordered
        as if ``second_first``). This is not plain lexicographic order on the
        full method string. Excludes ``methods``, names starting with ``_``,
        and non-callables. The result is cached on first access.

        :returns: Tuple of method names in that order.
        """

        def _is_valid_func(name: str):
            return not (name.startswith("_") or name in _UTILITY_METHODS) and callable(getattr(self, name))

        def _sort_helper(method_name: str):
            name_parts = method_name.split("_")
            num_part = len(name_parts)
            if num_part == 2:
                return f"{name_parts[1]}_{name_parts[0]}"
            if num_part == 3:
                return f"{{{name_parts[0]}_"
            return "_" + method_name

        return tuple(
            sorted(
                (func for func in dir(self) if _is_valid_func(func)),
                key=_sort_helper,
            )
        )

    @lru_cache(maxsize=50)
    def method_signature(self, method_name: str) -> str:
        """Return signature for a method in this resource group, result is cached.

        For example ``client.pulls.method_signature("list_issues")`` would return:
        list_issues(*, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> List[Issue]

        :param method_name: Attribute name of a callable on this resource.
        :returns: Formatted signature.
        """
        import inspect

        return method_name + str(inspect.signature(getattr(self, method_name))).replace(_DATA_MODEL_PATH, "")

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
