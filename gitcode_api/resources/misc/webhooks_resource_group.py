"""AbstractWebhooksResource, WebhooksResource, and AsyncWebhooksResource resource group."""

from abc import ABC, abstractmethod
from typing import List, Optional, Union

from ..._models import Webhook
from .._shared import AsyncResource, SyncResource

# mypy: disable-error-code=override
# pylint: disable=invalid-overridden-method,protected-access,redefined-builtin


class AbstractWebhooksResource(ABC):
    """Interface for Webhooks resource endpoints."""

    @abstractmethod
    def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Webhook]:
        """List webhooks for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Hook configurations.
        """

    @abstractmethod
    def create(self, *, url: str, owner: Optional[str] = None, repo: Optional[str] = None, **payload) -> Webhook:
        """Create a repository webhook.

        :param url: Payload URL GitCode should POST events to.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param payload: Additional fields from the Webhooks API (events list, secret, content type, etc.).
        :returns: Created webhook.
        """

    @abstractmethod
    def get(self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> Webhook:
        """Get a repository webhook by identifier.

        :param hook_id: Webhook id from the API.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Webhook configuration.
        """

    @abstractmethod
    def update(
        self,
        *,
        hook_id: Union[int, str],
        url: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        **payload,
    ) -> Webhook:
        """Update a repository webhook.

        :param hook_id: Webhook id.
        :param url: New payload URL (merged into the JSON body).
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param payload: Other mutable webhook fields accepted by the API.
        :returns: Updated webhook.
        """

    @abstractmethod
    def delete(self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Delete a repository webhook.

        :param hook_id: Webhook id.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """

    @abstractmethod
    def test(self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Send a test delivery for a repository webhook.

        :param hook_id: Webhook id.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """


class WebhooksResource(SyncResource, AbstractWebhooksResource):
    """Synchronous webhook endpoints."""

    def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Webhook]:
        return self._models(
            "GET",
            self._client._repo_path("hooks", owner=owner, repo=repo),
            Webhook,
            params={"page": page, "per_page": per_page},
        )

    def create(self, *, url: str, owner: Optional[str] = None, repo: Optional[str] = None, **payload) -> Webhook:
        payload["url"] = url
        return self._model("POST", self._client._repo_path("hooks", owner=owner, repo=repo), Webhook, json=payload)

    def get(self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> Webhook:
        return self._model("GET", self._client._repo_path("hooks", hook_id, owner=owner, repo=repo), Webhook)

    def update(
        self,
        *,
        hook_id: Union[int, str],
        url: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        **payload,
    ) -> Webhook:
        payload["url"] = url
        return self._model(
            "PATCH", self._client._repo_path("hooks", hook_id, owner=owner, repo=repo), Webhook, json=payload
        )

    def delete(self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        self._request("DELETE", self._client._repo_path("hooks", hook_id, owner=owner, repo=repo))

    def test(self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        self._request("POST", self._client._repo_path("hooks", hook_id, "tests", owner=owner, repo=repo))


class AsyncWebhooksResource(AsyncResource, AbstractWebhooksResource):
    """Asynchronous webhook endpoints.

    Mirrors :class:`WebhooksResource`; see that class and ``docs/rest_api/repos/webhooks``.
    """

    async def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Webhook]:
        return await self._models(
            "GET",
            self._client._repo_path("hooks", owner=owner, repo=repo),
            Webhook,
            params={"page": page, "per_page": per_page},
        )

    async def create(self, *, url: str, owner: Optional[str] = None, repo: Optional[str] = None, **payload) -> Webhook:
        payload["url"] = url
        return await self._model(
            "POST", self._client._repo_path("hooks", owner=owner, repo=repo), Webhook, json=payload
        )

    async def get(
        self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> Webhook:
        return await self._model("GET", self._client._repo_path("hooks", hook_id, owner=owner, repo=repo), Webhook)

    async def update(
        self,
        *,
        hook_id: Union[int, str],
        url: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        **payload,
    ) -> Webhook:
        payload["url"] = url
        return await self._model(
            "PATCH", self._client._repo_path("hooks", hook_id, owner=owner, repo=repo), Webhook, json=payload
        )

    async def delete(
        self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        await self._request("DELETE", self._client._repo_path("hooks", hook_id, owner=owner, repo=repo))

    async def test(self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        await self._request("POST", self._client._repo_path("hooks", hook_id, "tests", owner=owner, repo=repo))
