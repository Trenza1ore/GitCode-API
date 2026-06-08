"""AbstractOrgsResource, OrgsResource, and AsyncOrgsResource resource group."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..._models import (
    APIObject,
    EmptyResponse,
    EnterpriseMember,
    Organization,
    OrganizationMembership,
    OrganizationSummary,
    Repository,
    User,
)
from .._shared import AsyncResource, SyncResource

# mypy: disable-error-code=override
# pylint: disable=invalid-overridden-method,protected-access,redefined-builtin


class AbstractOrgsResource(ABC):
    """Interface for Orgs resource endpoints."""

    @abstractmethod
    def list_for_user(
        self, *, username: str, page: Optional[int] = None, per_page: Optional[int] = None
    ) -> List[OrganizationSummary]:
        """List organizations for a user.

        :param username: GitCode username or login.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Organizations the user belongs to.
        """

    @abstractmethod
    def list_authenticated(
        self, *, page: Optional[int] = None, per_page: Optional[int] = None, admin: Optional[bool] = None
    ) -> List[OrganizationSummary]:
        """List organizations for the authenticated user.

        :param page: Page number.
        :param per_page: Page size.
        :param admin: Optional admin-only filter.
        :returns: Organizations visible to the authorized user.
        """

    @abstractmethod
    def get_member(self, *, org: str, username: str) -> OrganizationMembership:
        """Get an organization member profile.

        :param org: Organization path or login.
        :param username: Member username or login.
        :returns: Organization membership details.
        """

    @abstractmethod
    def get(self, *, org: str) -> Organization:
        """Get an organization.

        :param org: Organization path or login.
        :returns: Organization details.
        """

    @abstractmethod
    def list_repos(
        self, *, org: str, type: Optional[str] = None, page: Optional[int] = None, per_page: Optional[int] = None
    ) -> List[Repository]:
        """List repositories for an organization.

        :param org: Organization path or login.
        :param type: Repository type filter such as ``all``, ``public``, or ``private``.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Matching repositories.
        """

    @abstractmethod
    def create_repo(self, *, org: str, name: str, **payload) -> Repository:
        """Create an organization repository.

        Additional payload fields match the organization repository creation
        endpoint, such as ``description``, ``homepage``, ``private``,
        ``public``, ``auto_init``, and ``default_branch``.

        :param org: Organization path or login.
        :param name: Repository name.
        :param payload: Additional repository creation fields.
        :returns: Created repository metadata.
        """

    @abstractmethod
    def get_enterprise_member(self, *, enterprise: str, username: str) -> EnterpriseMember:
        """Get a member profile for an enterprise.

        :param enterprise: Enterprise path or login.
        :param username: Member username or login.
        :returns: Enterprise membership details.
        """

    @abstractmethod
    def get_membership(self, *, org: str) -> OrganizationMembership:
        """Get the authenticated user's membership in an organization.

        :param org: Organization path or login.
        :returns: Membership details for the current user.
        """

    @abstractmethod
    def list_members(
        self, *, org: str, page: Optional[int] = None, per_page: Optional[int] = None, role: Optional[str] = None
    ) -> List[User]:
        """List members of an organization.

        :param org: Organization path or login.
        :param page: Page number.
        :param per_page: Page size.
        :param role: Optional role filter such as ``all``, ``admin``, or ``member``.
        :returns: Organization members.
        """

    @abstractmethod
    def list_enterprise_members(
        self, *, enterprise: str, page: Optional[int] = None, per_page: Optional[int] = None, role: Optional[str] = None
    ) -> List[EnterpriseMember]:
        """List members of an enterprise.

        :param enterprise: Enterprise path or login.
        :param page: Page number.
        :param per_page: Page size.
        :param role: Optional role filter.
        :returns: Enterprise members.
        """

    @abstractmethod
    def remove_member(self, *, org: str, username: str) -> EmptyResponse:
        """Remove a member from an organization.

        :param org: Organization path or login.
        :param username: Member username or login.
        :returns: API response payload, if any.
        """

    @abstractmethod
    def list_followers(self, *, owner: str, page: Optional[int] = None, per_page: Optional[int] = None) -> List[User]:
        """List followers of an organization.

        :param owner: Organization path.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Followers of the organization.
        """

    @abstractmethod
    def get_issue_extend_settings(self, *, org: str) -> List[APIObject]:
        """Get extended issue type and status settings for an organization.

        :param org: Organization path or login.
        :returns: Extended issue configuration entries.
        """

    @abstractmethod
    def invite_member(
        self, *, org: str, username: str, permission: Optional[str] = None, role_id: Optional[str] = None
    ) -> User:
        """Invite a user to an organization.

        :param org: Organization path or login.
        :param username: Member username or login.
        :param permission: Permission level such as ``pull``, ``push``, or ``admin``.
        :param role_id: Custom role identifier when using a customized permission.
        :returns: Invited user information with permissions.
        """

    @abstractmethod
    def update_enterprise_member(self, *, enterprise: str, username: str, role: str) -> EnterpriseMember:
        """Update the role of an enterprise member.

        :param enterprise: Enterprise path or login.
        :param username: Member username or login.
        :param role: Enterprise role such as ``viewer``, ``developer``, or ``admin``.
        :returns: Updated enterprise membership.
        """

    @abstractmethod
    def update(self, *, org: str, **payload) -> Organization:
        """Update organization metadata.

        :param org: Organization path or login.
        :param payload: Updatable fields such as ``name``, ``email``, or ``description``.
        :returns: Updated organization details.
        """

    @abstractmethod
    def leave(self, *, org: str) -> None:
        """Leave an organization as the authenticated user.

        :param org: Organization path or login.
        """


class OrgsResource(SyncResource, AbstractOrgsResource):
    """Synchronous organization and enterprise endpoints."""

    def list_for_user(
        self, *, username: str, page: Optional[int] = None, per_page: Optional[int] = None
    ) -> List[OrganizationSummary]:
        return self._models(
            "GET",
            self._client._path("users", username, "orgs"),
            OrganizationSummary,
            params={"page": page, "per_page": per_page},
        )

    def list_authenticated(
        self, *, page: Optional[int] = None, per_page: Optional[int] = None, admin: Optional[bool] = None
    ) -> List[OrganizationSummary]:
        return self._models(
            "GET",
            self._client._path("users", "orgs"),
            OrganizationSummary,
            params={"page": page, "per_page": per_page, "admin": admin},
        )

    def get_member(self, *, org: str, username: str) -> OrganizationMembership:
        return self._model("GET", self._client._path("orgs", org, "members", username), OrganizationMembership)

    def get(self, *, org: str) -> Organization:
        return self._model("GET", self._client._path("orgs", org), Organization)

    def list_repos(
        self, *, org: str, type: Optional[str] = None, page: Optional[int] = None, per_page: Optional[int] = None
    ) -> List[Repository]:
        return self._models(
            "GET",
            self._client._path("orgs", org, "repos"),
            Repository,
            params={"type": type, "page": page, "per_page": per_page},
        )

    def create_repo(self, *, org: str, name: str, **payload) -> Repository:
        payload["name"] = name
        return self._model("POST", self._client._path("orgs", org, "repos"), Repository, json=payload)

    def get_enterprise_member(self, *, enterprise: str, username: str) -> EnterpriseMember:
        return self._model("GET", self._client._path("enterprises", enterprise, "members", username), EnterpriseMember)

    def get_membership(self, *, org: str) -> OrganizationMembership:
        return self._model("GET", self._client._path("user", "memberships", "orgs", org), OrganizationMembership)

    def list_members(
        self, *, org: str, page: Optional[int] = None, per_page: Optional[int] = None, role: Optional[str] = None
    ) -> List[User]:
        return self._models(
            "GET",
            self._client._path("orgs", org, "members"),
            User,
            params={"page": page, "per_page": per_page, "role": role},
        )

    def list_enterprise_members(
        self, *, enterprise: str, page: Optional[int] = None, per_page: Optional[int] = None, role: Optional[str] = None
    ) -> List[EnterpriseMember]:
        return self._models(
            "GET",
            self._client._path("enterprises", enterprise, "members"),
            EnterpriseMember,
            params={"page": page, "per_page": per_page, "role": role},
        )

    def remove_member(self, *, org: str, username: str) -> EmptyResponse:
        return self._model("DELETE", self._client._path("orgs", org, "memberships", username), EmptyResponse)

    def list_followers(self, *, owner: str, page: Optional[int] = None, per_page: Optional[int] = None) -> List[User]:
        return self._models(
            "GET",
            self._client._path("orgs", owner, "followers"),
            User,
            params={"page": page, "per_page": per_page},
        )

    def get_issue_extend_settings(self, *, org: str) -> List[APIObject]:
        data = self._request("GET", self._client._path("orgs", org, "issue", "extend", "settings"))
        return [APIObject(dict(item)) for item in data]

    def invite_member(
        self, *, org: str, username: str, permission: Optional[str] = None, role_id: Optional[str] = None
    ) -> User:
        return self._model(
            "POST",
            self._client._path("orgs", org, "memberships", username),
            User,
            json={"permission": permission, "role_id": role_id},
        )

    def update_enterprise_member(self, *, enterprise: str, username: str, role: str) -> EnterpriseMember:
        return self._model(
            "PUT",
            self._client._path("enterprises", enterprise, "members", username),
            EnterpriseMember,
            json={"role": role},
        )

    def update(self, *, org: str, **payload) -> Organization:
        return self._model("PATCH", self._client._path("orgs", org), Organization, json=payload)

    def leave(self, *, org: str) -> None:
        self._request("DELETE", self._client._path("user", "memberships", "orgs", org))


class AsyncOrgsResource(AsyncResource, AbstractOrgsResource):
    """Asynchronous organization and enterprise endpoints.

    Mirrors :class:`OrgsResource`; see that class for parameters (``docs/rest_api/orgs``).
    """

    async def list_for_user(
        self, *, username: str, page: Optional[int] = None, per_page: Optional[int] = None
    ) -> List[OrganizationSummary]:
        return await self._models(
            "GET",
            self._client._path("users", username, "orgs"),
            OrganizationSummary,
            params={"page": page, "per_page": per_page},
        )

    async def list_authenticated(
        self, *, page: Optional[int] = None, per_page: Optional[int] = None, admin: Optional[bool] = None
    ) -> List[OrganizationSummary]:
        return await self._models(
            "GET",
            self._client._path("users", "orgs"),
            OrganizationSummary,
            params={"page": page, "per_page": per_page, "admin": admin},
        )

    async def get_member(self, *, org: str, username: str) -> OrganizationMembership:
        return await self._model("GET", self._client._path("orgs", org, "members", username), OrganizationMembership)

    async def get(self, *, org: str) -> Organization:
        return await self._model("GET", self._client._path("orgs", org), Organization)

    async def list_repos(
        self, *, org: str, type: Optional[str] = None, page: Optional[int] = None, per_page: Optional[int] = None
    ) -> List[Repository]:
        return await self._models(
            "GET",
            self._client._path("orgs", org, "repos"),
            Repository,
            params={"type": type, "page": page, "per_page": per_page},
        )

    async def create_repo(self, *, org: str, name: str, **payload) -> Repository:
        payload["name"] = name
        return await self._model("POST", self._client._path("orgs", org, "repos"), Repository, json=payload)

    async def get_enterprise_member(self, *, enterprise: str, username: str) -> EnterpriseMember:
        return await self._model(
            "GET", self._client._path("enterprises", enterprise, "members", username), EnterpriseMember
        )

    async def get_membership(self, *, org: str) -> OrganizationMembership:
        return await self._model("GET", self._client._path("user", "memberships", "orgs", org), OrganizationMembership)

    async def list_members(
        self, *, org: str, page: Optional[int] = None, per_page: Optional[int] = None, role: Optional[str] = None
    ) -> List[User]:
        return await self._models(
            "GET",
            self._client._path("orgs", org, "members"),
            User,
            params={"page": page, "per_page": per_page, "role": role},
        )

    async def list_enterprise_members(
        self, *, enterprise: str, page: Optional[int] = None, per_page: Optional[int] = None, role: Optional[str] = None
    ) -> List[EnterpriseMember]:
        return await self._models(
            "GET",
            self._client._path("enterprises", enterprise, "members"),
            EnterpriseMember,
            params={"page": page, "per_page": per_page, "role": role},
        )

    async def remove_member(self, *, org: str, username: str) -> EmptyResponse:
        return await self._model("DELETE", self._client._path("orgs", org, "memberships", username), EmptyResponse)

    async def list_followers(
        self, *, owner: str, page: Optional[int] = None, per_page: Optional[int] = None
    ) -> List[User]:
        return await self._models(
            "GET", self._client._path("orgs", owner, "followers"), User, params={"page": page, "per_page": per_page}
        )

    async def get_issue_extend_settings(self, *, org: str) -> List[APIObject]:
        data = await self._request("GET", self._client._path("orgs", org, "issue", "extend", "settings"))
        return [APIObject(dict(item)) for item in data]

    async def invite_member(
        self, *, org: str, username: str, permission: Optional[str] = None, role_id: Optional[str] = None
    ) -> User:
        return await self._model(
            "POST",
            self._client._path("orgs", org, "memberships", username),
            User,
            json={"permission": permission, "role_id": role_id},
        )

    async def update_enterprise_member(self, *, enterprise: str, username: str, role: str) -> EnterpriseMember:
        return await self._model(
            "PUT",
            self._client._path("enterprises", enterprise, "members", username),
            EnterpriseMember,
            json={"role": role},
        )

    async def update(self, *, org: str, **payload) -> Organization:
        return await self._model("PATCH", self._client._path("orgs", org), Organization, json=payload)

    async def leave(self, *, org: str) -> None:
        await self._request("DELETE", self._client._path("user", "memberships", "orgs", org))
