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
    def create(
        self,
        *,
        url: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        encryption_type: Optional[int] = None,
        password: Optional[str] = None,
        push_events: Optional[bool] = None,
        tag_push_events: Optional[bool] = None,
        issues_events: Optional[bool] = None,
        note_events: Optional[bool] = None,
        merge_requests_events: Optional[bool] = None,
        **kwargs,
    ) -> Webhook:
        """Create a repository webhook.

        :param url: Payload URL GitCode should POST events to.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param encryption_type: Encryption type: ``0`` (password), ``1`` (signature key).
        :param password: Secret included in requests to prevent malicious calls.
        :param push_events: Trigger on push events.
        :param tag_push_events: Trigger on tag push events.
        :param issues_events: Trigger on issue creation/closure events.
        :param note_events: Trigger on comment events (issue/PR/commit).
        :param merge_requests_events: Trigger on merge request events.
        :param kwargs: Additional arguments forwarded directly in request.
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
        encryption_type: Optional[int] = None,
        password: Optional[str] = None,
        push_events: Optional[bool] = None,
        tag_push_events: Optional[bool] = None,
        issues_events: Optional[bool] = None,
        note_events: Optional[bool] = None,
        merge_requests_events: Optional[bool] = None,
        **kwargs,
    ) -> Webhook:
        """Update a repository webhook.

        :param hook_id: Webhook id.
        :param url: New payload URL GitCode should POST events to.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param encryption_type: Encryption type: ``0`` (password), ``1`` (signature key).
        :param password: Secret included in requests to prevent malicious calls.
        :param push_events: Trigger on push events.
        :param tag_push_events: Trigger on tag push events.
        :param issues_events: Trigger on issue creation/closure events.
        :param note_events: Trigger on comment events (issue/PR/commit).
        :param merge_requests_events: Trigger on merge request events.
        :param kwargs: Additional arguments forwarded directly in request.
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

    def create(
        self,
        *,
        url: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        encryption_type: Optional[int] = None,
        password: Optional[str] = None,
        push_events: Optional[bool] = None,
        tag_push_events: Optional[bool] = None,
        issues_events: Optional[bool] = None,
        note_events: Optional[bool] = None,
        merge_requests_events: Optional[bool] = None,
        **kwargs,
    ) -> Webhook:
        return self._model(
            "POST",
            self._client._repo_path("hooks", owner=owner, repo=repo),
            Webhook,
            json={
                "url": url,
                "encryption_type": encryption_type,
                "password": password,
                "push_events": push_events,
                "tag_push_events": tag_push_events,
                "issues_events": issues_events,
                "note_events": note_events,
                "merge_requests_events": merge_requests_events,
                **kwargs,
            },
        )

    def get(self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> Webhook:
        return self._model("GET", self._client._repo_path("hooks", hook_id, owner=owner, repo=repo), Webhook)

    def update(
        self,
        *,
        hook_id: Union[int, str],
        url: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        encryption_type: Optional[int] = None,
        password: Optional[str] = None,
        push_events: Optional[bool] = None,
        tag_push_events: Optional[bool] = None,
        issues_events: Optional[bool] = None,
        note_events: Optional[bool] = None,
        merge_requests_events: Optional[bool] = None,
        **kwargs,
    ) -> Webhook:
        return self._model(
            "PATCH",
            self._client._repo_path("hooks", hook_id, owner=owner, repo=repo),
            Webhook,
            json={
                "url": url,
                "encryption_type": encryption_type,
                "password": password,
                "push_events": push_events,
                "tag_push_events": tag_push_events,
                "issues_events": issues_events,
                "note_events": note_events,
                "merge_requests_events": merge_requests_events,
                **kwargs,
            },
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

    async def create(
        self,
        *,
        url: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        encryption_type: Optional[int] = None,
        password: Optional[str] = None,
        push_events: Optional[bool] = None,
        tag_push_events: Optional[bool] = None,
        issues_events: Optional[bool] = None,
        note_events: Optional[bool] = None,
        merge_requests_events: Optional[bool] = None,
        **kwargs,
    ) -> Webhook:
        return await self._model(
            "POST",
            self._client._repo_path("hooks", owner=owner, repo=repo),
            Webhook,
            json={
                "url": url,
                "encryption_type": encryption_type,
                "password": password,
                "push_events": push_events,
                "tag_push_events": tag_push_events,
                "issues_events": issues_events,
                "note_events": note_events,
                "merge_requests_events": merge_requests_events,
                **kwargs,
            },
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
        encryption_type: Optional[int] = None,
        password: Optional[str] = None,
        push_events: Optional[bool] = None,
        tag_push_events: Optional[bool] = None,
        issues_events: Optional[bool] = None,
        note_events: Optional[bool] = None,
        merge_requests_events: Optional[bool] = None,
        **kwargs,
    ) -> Webhook:
        return await self._model(
            "PATCH",
            self._client._repo_path("hooks", hook_id, owner=owner, repo=repo),
            Webhook,
            json={
                "url": url,
                "encryption_type": encryption_type,
                "password": password,
                "push_events": push_events,
                "tag_push_events": tag_push_events,
                "issues_events": issues_events,
                "note_events": note_events,
                "merge_requests_events": merge_requests_events,
                **kwargs,
            },
        )

    async def delete(
        self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        await self._request("DELETE", self._client._repo_path("hooks", hook_id, owner=owner, repo=repo))

    async def test(self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        await self._request("POST", self._client._repo_path("hooks", hook_id, "tests", owner=owner, repo=repo))
