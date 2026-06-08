"""AbstractUsersResource, UsersResource, and AsyncUsersResource resource group."""

from abc import ABC, abstractmethod
from typing import List, Optional, Union

from ..._models import (
    APIObject,
    Email,
    Namespace,
    PublicKey,
    Repository,
    User,
    UserEventsResponse,
)
from .._shared import AsyncResource, SyncResource

# mypy: disable-error-code=override
# pylint: disable=invalid-overridden-method,protected-access,redefined-builtin


class AbstractUsersResource(ABC):
    """Interface for Users resource endpoints."""

    @abstractmethod
    def get(self, *, username: str) -> User:
        """Get a user profile.

        :param username: GitCode username or login.
        :returns: User profile details.
        """

    @abstractmethod
    def me(self) -> User:
        """Get the profile of the authenticated user.

        :returns: Authorized user profile.
        """

    @abstractmethod
    def list_emails(self) -> List[Email]:
        """List email addresses for the authenticated user.

        :returns: Email records associated with the current account.
        """

    @abstractmethod
    def list_events(
        self, *, username: str, year: Optional[str] = None, next: Optional[str] = None
    ) -> UserEventsResponse:
        """List activity events for a user.

        :param username: GitCode username or login (path segment, see User API).
        :param year: Optional start year filter (query ``year``, e.g. ``2024`` per documentation).
        :param next: Optional end date / pagination cursor (query ``next``; often an ISO timestamp from a prior page).
        :returns: Event payload grouped by date.
        """

    @abstractmethod
    def list_repos(self, *, username: str, **params) -> List[Repository]:
        """List public repositories owned by a user.

        Supported filters follow the user repository API documentation, such as
        ``type``, ``sort``, ``direction``, ``page``, and ``per_page``.

        :param username: GitCode username or login.
        :param params: Query parameters accepted by the REST endpoint.
        :returns: Matching repositories.
        """

    @abstractmethod
    def create_key(self, *, key: str, title: str) -> PublicKey:
        """Add a public SSH key for the authenticated user.

        :param key: Public key material.
        :param title: Human-readable key name.
        :returns: Created key metadata.
        """

    @abstractmethod
    def list_keys(self, *, page: Optional[int] = None, per_page: Optional[int] = None) -> List[APIObject]:
        """List public SSH keys for the authenticated user.

        :param page: Page number.
        :param per_page: Page size.
        :returns: Public key records.
        """

    @abstractmethod
    def delete_key(self, *, key_id: Union[int, str]) -> None:
        """Delete a public SSH key.

        :param key_id: Public key identifier.
        """

    @abstractmethod
    def get_key(self, *, key_id: Union[int, str]) -> PublicKey:
        """Get a single public SSH key.

        :param key_id: Public key identifier.
        :returns: Public key metadata.
        """

    @abstractmethod
    def get_namespace(self, *, path: str) -> Namespace:
        """Resolve namespace information for the authenticated user.

        :param path: Namespace path to look up.
        :returns: Namespace details.
        """

    @abstractmethod
    def list_starred(
        self,
        *,
        sort: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Repository]:
        """List repositories starred by the authenticated user.

        :param sort: Sort field such as ``created`` or ``updated``.
        :param direction: Sort direction, usually ``asc`` or ``desc``.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Starred repositories.
        """


class UsersResource(SyncResource, AbstractUsersResource):
    """Synchronous user and account endpoints."""

    def get(self, *, username: str) -> User:
        return self._model("GET", self._client._path("users", username), User)

    def me(self) -> User:
        return self._model("GET", self._client._path("user"), User)

    def list_emails(self) -> List[Email]:
        return self._models("GET", self._client._path("emails"), Email)

    def list_events(
        self, *, username: str, year: Optional[str] = None, next: Optional[str] = None
    ) -> UserEventsResponse:
        return self._model(
            "GET",
            self._client._path("users", username, "events"),
            UserEventsResponse,
            params={"year": year, "next": next},
        )

    def list_repos(self, *, username: str, **params) -> List[Repository]:
        return self._models("GET", self._client._path("users", username, "repos"), Repository, params=params)

    def create_key(self, *, key: str, title: str) -> PublicKey:
        return self._model("POST", self._client._path("user", "keys"), PublicKey, json={"key": key, "title": title})

    def list_keys(self, *, page: Optional[int] = None, per_page: Optional[int] = None) -> List[APIObject]:
        data = self._request("GET", self._client._path("user", "keys"), params={"page": page, "per_page": per_page})
        return [APIObject(dict(item)) for item in data]

    def delete_key(self, *, key_id: Union[int, str]) -> None:
        self._request("DELETE", self._client._path("user", "keys", key_id))

    def get_key(self, *, key_id: Union[int, str]) -> PublicKey:
        return self._model("GET", self._client._path("user", "keys", key_id), PublicKey)

    def get_namespace(self, *, path: str) -> Namespace:
        return self._model("GET", self._client._path("user", "namespace"), Namespace, params={"path": path})

    def list_starred(
        self,
        *,
        sort: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Repository]:
        return self._models(
            "GET",
            self._client._path("user", "starred"),
            Repository,
            params={"sort": sort, "direction": direction, "page": page, "per_page": per_page},
        )


class AsyncUsersResource(AsyncResource, AbstractUsersResource):
    """Asynchronous user and account endpoints.

    Mirrors :class:`UsersResource`; see that class for full parameter descriptions
    (``docs/rest_api/users`` and related guides).
    """

    async def get(self, *, username: str) -> User:
        return await self._model("GET", self._client._path("users", username), User)

    async def me(self) -> User:
        return await self._model("GET", self._client._path("user"), User)

    async def list_emails(self) -> List[Email]:
        return await self._models("GET", self._client._path("emails"), Email)

    async def list_events(
        self, *, username: str, year: Optional[str] = None, next: Optional[str] = None
    ) -> UserEventsResponse:
        return await self._model(
            "GET",
            self._client._path("users", username, "events"),
            UserEventsResponse,
            params={"year": year, "next": next},
        )

    async def list_repos(self, *, username: str, **params) -> List[Repository]:
        return await self._models("GET", self._client._path("users", username, "repos"), Repository, params=params)

    async def create_key(self, *, key: str, title: str) -> PublicKey:
        return await self._model(
            "POST", self._client._path("user", "keys"), PublicKey, json={"key": key, "title": title}
        )

    async def list_keys(self, *, page: Optional[int] = None, per_page: Optional[int] = None) -> List[APIObject]:
        data = await self._request(
            "GET", self._client._path("user", "keys"), params={"page": page, "per_page": per_page}
        )
        return [APIObject(dict(item)) for item in data]

    async def delete_key(self, *, key_id: Union[int, str]) -> None:
        await self._request("DELETE", self._client._path("user", "keys", key_id))

    async def get_key(self, *, key_id: Union[int, str]) -> PublicKey:
        return await self._model("GET", self._client._path("user", "keys", key_id), PublicKey)

    async def get_namespace(self, *, path: str) -> Namespace:
        return await self._model("GET", self._client._path("user", "namespace"), Namespace, params={"path": path})

    async def list_starred(
        self,
        *,
        sort: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Repository]:
        return await self._models(
            "GET",
            self._client._path("user", "starred"),
            Repository,
            params={"sort": sort, "direction": direction, "page": page, "per_page": per_page},
        )
