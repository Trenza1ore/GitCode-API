"""AbstractTagsResource, TagsResource, and AsyncTagsResource resource group."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..._models import ProtectedTag, Tag
from .._shared import AsyncResource, SyncResource

# mypy: disable-error-code=override
# pylint: disable=invalid-overridden-method,protected-access,redefined-builtin


class AbstractTagsResource(ABC):
    """Interface for Tags resource endpoints."""

    @abstractmethod
    def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Tag]:
        """List tags for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Tags.
        """

    @abstractmethod
    def create(
        self,
        *,
        refs: str,
        tag_name: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        tag_message: Optional[str] = None,
    ) -> Tag:
        """Create a tag for a repository.

        :param refs: Object SHA or ref the tag should point to.
        :param tag_name: Name of the new tag.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param tag_message: Optional annotated tag message.
        :returns: Created tag.
        """

    @abstractmethod
    def list_protected(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[ProtectedTag]:
        """List protected tags for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Protected tag rules.
        """

    @abstractmethod
    def delete_protected(self, *, tag_name: str, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Delete a protected tag rule.

        :param tag_name: Protected tag name in the URL path.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """

    @abstractmethod
    def get_protected(self, *, tag_name: str, owner: Optional[str] = None, repo: Optional[str] = None) -> ProtectedTag:
        """Get details for a protected tag rule.

        :param tag_name: Tag name in the path.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Protected tag configuration.
        """

    @abstractmethod
    def create_protected(
        self,
        *,
        name: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        create_access_level: Optional[int] = None,
    ) -> ProtectedTag:
        """Create a protected tag rule.

        :param name: Tag name or pattern to protect.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param create_access_level: Minimum access level required to create matching tags (API-specific integer).
        :returns: Created rule.
        """

    @abstractmethod
    def update_protected(
        self, *, name: str, create_access_level: int, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> ProtectedTag:
        """Update a protected tag rule."""


class TagsResource(SyncResource, AbstractTagsResource):
    """Synchronous tag endpoints."""

    def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Tag]:
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
        return self._models(
            "GET",
            self._client._repo_path("protected_tags", owner=owner, repo=repo),
            ProtectedTag,
            params={"page": page, "per_page": per_page},
        )

    def delete_protected(self, *, tag_name: str, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        self._request("DELETE", self._client._repo_path("protected_tags", tag_name, owner=owner, repo=repo))

    def get_protected(self, *, tag_name: str, owner: Optional[str] = None, repo: Optional[str] = None) -> ProtectedTag:
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
        return self._model(
            "POST",
            self._client._repo_path("protected_tags", owner=owner, repo=repo),
            ProtectedTag,
            json={"name": name, "create_access_level": create_access_level},
        )

    def update_protected(
        self, *, name: str, create_access_level: int, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> ProtectedTag:
        return self._model(
            "PUT",
            self._client._repo_path("protected_tags", owner=owner, repo=repo),
            ProtectedTag,
            json={"name": name, "create_access_level": create_access_level},
        )


class AsyncTagsResource(AsyncResource, AbstractTagsResource):
    """Asynchronous tag endpoints.

    Mirrors :class:`TagsResource`; see that class and ``docs/rest_api/repos/tag`` for semantics.
    """

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
