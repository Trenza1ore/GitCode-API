"""Shared resource base classes for the GitCode SDK."""

from typing import Any, Dict, List, Optional, Union

from .._base_client import AsyncAPIClient, SyncAPIClient
from .._models import APIObject, ModelT, as_model, as_model_list


class SyncResource:
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
        """Dispatch a low-level request through the owning client."""
        return self._client.request(method, path, params=params, json=json, data=data, raw=raw)

    def _model(self, method: str, path: str, model_type: type[ModelT], **kwargs: Any) -> ModelT:
        """Send a request and wrap a JSON object in ``model_type``."""
        data = self._request(method, path, **kwargs)
        return as_model(data, model_type)

    def _models(self, method: str, path: str, model_type: type[ModelT], **kwargs: Any) -> List[ModelT]:
        """Send a request and wrap a JSON array in ``model_type`` instances."""
        data = self._request(method, path, **kwargs)
        return as_model_list(data, model_type)

    def _maybe_model(self, method: str, path: str, model_type: type[ModelT], **kwargs: Any) -> Union[ModelT, APIObject]:
        """Wrap dict responses as models and scalar responses as ``APIObject``."""
        data = self._request(method, path, **kwargs)
        if isinstance(data, dict):
            return as_model(data, model_type)
        return APIObject({"value": data})


class AsyncResource:
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
        """Dispatch a low-level async request through the owning client."""
        return await self._client.request(method, path, params=params, json=json, data=data, raw=raw)

    async def _model(self, method: str, path: str, model_type: type[ModelT], **kwargs: Any) -> ModelT:
        """Send a request and wrap a JSON object in ``model_type``."""
        data = await self._request(method, path, **kwargs)
        return as_model(data, model_type)

    async def _models(self, method: str, path: str, model_type: type[ModelT], **kwargs: Any) -> List[ModelT]:
        """Send a request and wrap a JSON array in ``model_type`` instances."""
        data = await self._request(method, path, **kwargs)
        return as_model_list(data, model_type)
