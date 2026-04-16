"""Release, tag, and webhook resource groups."""

from typing import Any, List, Optional, Union

from .._models import ProtectedTag, Release, Tag, Webhook
from ._shared import AsyncResource, SyncResource


class ReleasesResource(SyncResource):
    """Synchronous release endpoints."""

    def update(
        self,
        *,
        release_id: Union[int, str],
        tag_name: str,
        name: str,
        body: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> Release:
        """Update a repository release.

        :param release_id: Release identifier.
        :param tag_name: Tag name for the release.
        :param name: Release name.
        :param body: Release description.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Updated release payload.
        """
        return self._model(
            "PATCH",
            self._client._repo_path("releases", release_id, owner=owner, repo=repo),
            Release,
            json={"tag_name": tag_name, "name": name, "body": body},
        )

    def get_by_tag(self, *, tag: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Release:
        """Get a repository release by tag name."""
        return self._model(
            "GET",
            self._client._repo_path("releases", "tags", tag, owner=owner, repo=repo),
            Release,
        )

    def list(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> List[Release]:
        """List releases for a repository."""
        return self._models("GET", self._client._repo_path("releases", owner=owner, repo=repo), Release)


class TagsResource(SyncResource):
    """Synchronous tag endpoints."""

    def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Tag]:
        """List tags for a repository."""
        return self._models(
            "GET",
            self._client._repo_path("tags", owner=owner, repo=repo),
            Tag,
            params={"page": page, "per_page": per_page},
        )

    def create(
        self,
        *,
        refs: str,
        tag_name: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        tag_message: Optional[str] = None,
    ) -> Tag:
        """Create a tag for a repository."""
        return self._model(
            "POST",
            self._client._repo_path("tags", owner=owner, repo=repo),
            Tag,
            json={"refs": refs, "tag_name": tag_name, "tag_message": tag_message},
        )

    def list_protected(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[ProtectedTag]:
        """List protected tags for a repository."""
        return self._models(
            "GET",
            self._client._repo_path("protected_tags", owner=owner, repo=repo),
            ProtectedTag,
            params={"page": page, "per_page": per_page},
        )

    def delete_protected(self, *, tag_name: str, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Delete a protected tag rule."""
        self._request("DELETE", self._client._repo_path("protected_tags", tag_name, owner=owner, repo=repo))

    def get_protected(self, *, tag_name: str, owner: Optional[str] = None, repo: Optional[str] = None) -> ProtectedTag:
        """Get details for a protected tag rule."""
        return self._model(
            "GET",
            self._client._repo_path("protected_tags", tag_name, owner=owner, repo=repo),
            ProtectedTag,
        )

    def create_protected(
        self,
        *,
        name: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        create_access_level: Optional[int] = None,
    ) -> ProtectedTag:
        """Create a protected tag rule."""
        return self._model(
            "POST",
            self._client._repo_path("protected_tags", owner=owner, repo=repo),
            ProtectedTag,
            json={"name": name, "create_access_level": create_access_level},
        )

    def update_protected(
        self, *, name: str, create_access_level: int, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> ProtectedTag:
        """Update a protected tag rule."""
        return self._model(
            "PUT",
            self._client._repo_path("protected_tags", owner=owner, repo=repo),
            ProtectedTag,
            json={"name": name, "create_access_level": create_access_level},
        )


class WebhooksResource(SyncResource):
    """Synchronous webhook endpoints."""

    def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Webhook]:
        """List webhooks for a repository."""
        return self._models(
            "GET",
            self._client._repo_path("hooks", owner=owner, repo=repo),
            Webhook,
            params={"page": page, "per_page": per_page},
        )

    def create(self, *, url: str, owner: Optional[str] = None, repo: Optional[str] = None, **payload: Any) -> Webhook:
        """Create a repository webhook."""
        payload["url"] = url
        return self._model("POST", self._client._repo_path("hooks", owner=owner, repo=repo), Webhook, json=payload)

    def get(self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> Webhook:
        """Get a repository webhook by identifier."""
        return self._model("GET", self._client._repo_path("hooks", hook_id, owner=owner, repo=repo), Webhook)

    def update(
        self,
        *,
        hook_id: Union[int, str],
        url: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        **payload: Any,
    ) -> Webhook:
        """Update a repository webhook."""
        payload["url"] = url
        return self._model(
            "PATCH", self._client._repo_path("hooks", hook_id, owner=owner, repo=repo), Webhook, json=payload
        )

    def delete(self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Delete a repository webhook."""
        self._request("DELETE", self._client._repo_path("hooks", hook_id, owner=owner, repo=repo))

    def test(self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Send a test delivery for a repository webhook."""
        self._request("POST", self._client._repo_path("hooks", hook_id, "tests", owner=owner, repo=repo))


class AsyncReleasesResource(AsyncResource):
    """Asynchronous release endpoints."""

    async def update(
        self,
        *,
        release_id: Union[int, str],
        tag_name: str,
        name: str,
        body: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> Release:
        return await self._model(
            "PATCH",
            self._client._repo_path("releases", release_id, owner=owner, repo=repo),
            Release,
            json={"tag_name": tag_name, "name": name, "body": body},
        )

    async def get_by_tag(self, *, tag: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Release:
        return await self._model(
            "GET", self._client._repo_path("releases", "tags", tag, owner=owner, repo=repo), Release
        )

    async def list(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> List[Release]:
        return await self._models("GET", self._client._repo_path("releases", owner=owner, repo=repo), Release)


class AsyncTagsResource(AsyncResource):
    """Asynchronous tag endpoints."""

    async def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Tag]:
        return await self._models(
            "GET",
            self._client._repo_path("tags", owner=owner, repo=repo),
            Tag,
            params={"page": page, "per_page": per_page},
        )

    async def create(
        self,
        *,
        refs: str,
        tag_name: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        tag_message: Optional[str] = None,
    ) -> Tag:
        return await self._model(
            "POST",
            self._client._repo_path("tags", owner=owner, repo=repo),
            Tag,
            json={"refs": refs, "tag_name": tag_name, "tag_message": tag_message},
        )

    async def list_protected(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[ProtectedTag]:
        return await self._models(
            "GET",
            self._client._repo_path("protected_tags", owner=owner, repo=repo),
            ProtectedTag,
            params={"page": page, "per_page": per_page},
        )

    async def delete_protected(self, *, tag_name: str, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        await self._request("DELETE", self._client._repo_path("protected_tags", tag_name, owner=owner, repo=repo))

    async def get_protected(
        self, *, tag_name: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> ProtectedTag:
        return await self._model(
            "GET", self._client._repo_path("protected_tags", tag_name, owner=owner, repo=repo), ProtectedTag
        )

    async def create_protected(
        self,
        *,
        name: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        create_access_level: Optional[int] = None,
    ) -> ProtectedTag:
        return await self._model(
            "POST",
            self._client._repo_path("protected_tags", owner=owner, repo=repo),
            ProtectedTag,
            json={"name": name, "create_access_level": create_access_level},
        )

    async def update_protected(
        self, *, name: str, create_access_level: int, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> ProtectedTag:
        return await self._model(
            "PUT",
            self._client._repo_path("protected_tags", owner=owner, repo=repo),
            ProtectedTag,
            json={"name": name, "create_access_level": create_access_level},
        )


class AsyncWebhooksResource(AsyncResource):
    """Asynchronous webhook endpoints."""

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
        self, *, url: str, owner: Optional[str] = None, repo: Optional[str] = None, **payload: Any
    ) -> Webhook:
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
        **payload: Any,
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
