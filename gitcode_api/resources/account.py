"""Account, organization, search, and OAuth resource groups."""

from typing import List, Optional, Union
from urllib.parse import urlencode

import httpx

from .._models import (
    APIObject,
    Email,
    EmptyResponse,
    EnterpriseMember,
    Namespace,
    OAuthToken,
    Organization,
    OrganizationMembership,
    OrganizationSummary,
    PublicKey,
    Repository,
    SearchIssue,
    SearchRepository,
    SearchUser,
    User,
    UserEventsResponse,
)
from ._shared import AsyncResource, SyncResource

OAUTH_BASE_URL = "https://gitcode.com"


class UsersResource(SyncResource):
    """Synchronous user and account endpoints."""

    def get(self, *, username: str) -> User:
        """Get a user profile.

        :param username: GitCode username or login.
        :returns: User profile details.
        """
        return self._model("GET", self._client._path("users", username), User)

    def me(self) -> User:
        """Get the profile of the authenticated user.

        :returns: Authorized user profile.
        """
        return self._model("GET", self._client._path("user"), User)

    def list_emails(self) -> List[Email]:
        """List email addresses for the authenticated user.

        :returns: Email records associated with the current account.
        """
        return self._models("GET", self._client._path("emails"), Email)

    def list_events(
        self, *, username: str, year: Optional[str] = None, next: Optional[str] = None
    ) -> UserEventsResponse:
        """List activity events for a user.

        :param username: GitCode username or login (path segment, see User API).
        :param year: Optional start year filter (query ``year``, e.g. ``2024`` per documentation).
        :param next: Optional end date / pagination cursor (query ``next``; often an ISO timestamp from a prior page).
        :returns: Event payload grouped by date.
        """
        return self._model(
            "GET",
            self._client._path("users", username, "events"),
            UserEventsResponse,
            params={"year": year, "next": next},
        )

    def list_repos(self, *, username: str, **params) -> List[Repository]:
        """List public repositories owned by a user.

        Supported filters follow the user repository API documentation, such as
        ``type``, ``sort``, ``direction``, ``page``, and ``per_page``.

        :param username: GitCode username or login.
        :param params: Query parameters accepted by the REST endpoint.
        :returns: Matching repositories.
        """
        return self._models("GET", self._client._path("users", username, "repos"), Repository, params=params)

    def create_key(self, *, key: str, title: str) -> PublicKey:
        """Add a public SSH key for the authenticated user.

        :param key: Public key material.
        :param title: Human-readable key name.
        :returns: Created key metadata.
        """
        return self._model("POST", self._client._path("user", "keys"), PublicKey, json={"key": key, "title": title})

    def list_keys(self, *, page: Optional[int] = None, per_page: Optional[int] = None) -> List[APIObject]:
        """List public SSH keys for the authenticated user.

        :param page: Page number.
        :param per_page: Page size.
        :returns: Public key records.
        """
        data = self._request("GET", self._client._path("user", "keys"), params={"page": page, "per_page": per_page})
        return [APIObject(dict(item)) for item in data]

    def delete_key(self, *, key_id: Union[int, str]) -> None:
        """Delete a public SSH key.

        :param key_id: Public key identifier.
        """
        self._request("DELETE", self._client._path("user", "keys", key_id))

    def get_key(self, *, key_id: Union[int, str]) -> PublicKey:
        """Get a single public SSH key.

        :param key_id: Public key identifier.
        :returns: Public key metadata.
        """
        return self._model("GET", self._client._path("user", "keys", key_id), PublicKey)

    def get_namespace(self, *, path: str) -> Namespace:
        """Resolve namespace information for the authenticated user.

        :param path: Namespace path to look up.
        :returns: Namespace details.
        """
        return self._model("GET", self._client._path("user", "namespace"), Namespace, params={"path": path})

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
        return self._models(
            "GET",
            self._client._path("user", "starred"),
            Repository,
            params={"sort": sort, "direction": direction, "page": page, "per_page": per_page},
        )


class OrgsResource(SyncResource):
    """Synchronous organization and enterprise endpoints."""

    def list_for_user(
        self, *, username: str, page: Optional[int] = None, per_page: Optional[int] = None
    ) -> List[OrganizationSummary]:
        """List organizations for a user.

        :param username: GitCode username or login.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Organizations the user belongs to.
        """
        return self._models(
            "GET",
            self._client._path("users", username, "orgs"),
            OrganizationSummary,
            params={"page": page, "per_page": per_page},
        )

    def list_authenticated(
        self, *, page: Optional[int] = None, per_page: Optional[int] = None, admin: Optional[bool] = None
    ) -> List[OrganizationSummary]:
        """List organizations for the authenticated user.

        :param page: Page number.
        :param per_page: Page size.
        :param admin: Optional admin-only filter.
        :returns: Organizations visible to the authorized user.
        """
        return self._models(
            "GET",
            self._client._path("users", "orgs"),
            OrganizationSummary,
            params={"page": page, "per_page": per_page, "admin": admin},
        )

    def get_member(self, *, org: str, username: str) -> OrganizationMembership:
        """Get an organization member profile.

        :param org: Organization path or login.
        :param username: Member username or login.
        :returns: Organization membership details.
        """
        return self._model("GET", self._client._path("orgs", org, "members", username), OrganizationMembership)

    def get(self, *, org: str) -> Organization:
        """Get an organization.

        :param org: Organization path or login.
        :returns: Organization details.
        """
        return self._model("GET", self._client._path("orgs", org), Organization)

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
        return self._models(
            "GET",
            self._client._path("orgs", org, "repos"),
            Repository,
            params={"type": type, "page": page, "per_page": per_page},
        )

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
        payload["name"] = name
        return self._model("POST", self._client._path("orgs", org, "repos"), Repository, json=payload)

    def get_enterprise_member(self, *, enterprise: str, username: str) -> EnterpriseMember:
        """Get a member profile for an enterprise.

        :param enterprise: Enterprise path or login.
        :param username: Member username or login.
        :returns: Enterprise membership details.
        """
        return self._model("GET", self._client._path("enterprises", enterprise, "members", username), EnterpriseMember)

    def get_membership(self, *, org: str) -> OrganizationMembership:
        """Get the authenticated user's membership in an organization.

        :param org: Organization path or login.
        :returns: Membership details for the current user.
        """
        return self._model("GET", self._client._path("user", "memberships", "orgs", org), OrganizationMembership)

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
        return self._models(
            "GET",
            self._client._path("orgs", org, "members"),
            User,
            params={"page": page, "per_page": per_page, "role": role},
        )

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
        return self._models(
            "GET",
            self._client._path("enterprises", enterprise, "members"),
            EnterpriseMember,
            params={"page": page, "per_page": per_page, "role": role},
        )

    def remove_member(self, *, org: str, username: str) -> EmptyResponse:
        """Remove a member from an organization.

        :param org: Organization path or login.
        :param username: Member username or login.
        :returns: API response payload, if any.
        """
        return self._model("DELETE", self._client._path("orgs", org, "memberships", username), EmptyResponse)

    def list_followers(self, *, owner: str, page: Optional[int] = None, per_page: Optional[int] = None) -> List[User]:
        """List followers of an organization.

        :param owner: Organization path.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Followers of the organization.
        """
        return self._models(
            "GET",
            self._client._path("orgs", owner, "followers"),
            User,
            params={"page": page, "per_page": per_page},
        )

    def get_issue_extend_settings(self, *, org: str) -> List[APIObject]:
        """Get extended issue type and status settings for an organization.

        :param org: Organization path or login.
        :returns: Extended issue configuration entries.
        """
        data = self._request("GET", self._client._path("orgs", org, "issue", "extend", "settings"))
        return [APIObject(dict(item)) for item in data]

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
        return self._model(
            "POST",
            self._client._path("orgs", org, "memberships", username),
            User,
            json={"permission": permission, "role_id": role_id},
        )

    def update_enterprise_member(self, *, enterprise: str, username: str, role: str) -> EnterpriseMember:
        """Update the role of an enterprise member.

        :param enterprise: Enterprise path or login.
        :param username: Member username or login.
        :param role: Enterprise role such as ``viewer``, ``developer``, or ``admin``.
        :returns: Updated enterprise membership.
        """
        return self._model(
            "PUT",
            self._client._path("enterprises", enterprise, "members", username),
            EnterpriseMember,
            json={"role": role},
        )

    def update(self, *, org: str, **payload) -> Organization:
        """Update organization metadata.

        :param org: Organization path or login.
        :param payload: Updatable fields such as ``name``, ``email``, or ``description``.
        :returns: Updated organization details.
        """
        return self._model("PATCH", self._client._path("orgs", org), Organization, json=payload)

    def leave(self, *, org: str) -> None:
        """Leave an organization as the authenticated user.

        :param org: Organization path or login.
        """
        self._request("DELETE", self._client._path("user", "memberships", "orgs", org))


class SearchResource(SyncResource):
    """Synchronous search endpoints."""

    def users(
        self,
        *,
        q: str,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
    ) -> List[SearchUser]:
        """Search users.

        :param q: Search keywords.
        :param page: Page number.
        :param per_page: Page size.
        :param sort: Optional sort field such as ``joined_at``.
        :param order: Sort order, usually ``asc`` or ``desc``.
        :returns: Matching user search results.
        """
        return self._models(
            "GET",
            self._client._path("search", "users"),
            SearchUser,
            params={"q": q, "page": page, "per_page": per_page, "sort": sort, "order": order},
        )

    def issues(
        self,
        *,
        q: str,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
        repo: Optional[str] = None,
        state: Optional[str] = None,
    ) -> List[SearchIssue]:
        """Search issues.

        :param q: Search keywords.
        :param page: Page number.
        :param per_page: Page size.
        :param sort: Optional sort field.
        :param order: Sort order, usually ``asc`` or ``desc``.
        :param repo: Optional repository path filter.
        :param state: Optional issue state filter.
        :returns: Matching issue search results.
        """
        return self._models(
            "GET",
            self._client._path("search", "issues"),
            SearchIssue,
            params={
                "q": q,
                "page": page,
                "per_page": per_page,
                "sort": sort,
                "order": order,
                "repo": repo,
                "state": state,
            },
        )

    def repositories(
        self,
        *,
        q: str,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
        owner: Optional[str] = None,
        fork: Optional[str] = None,
        language: Optional[str] = None,
    ) -> List[SearchRepository]:
        """Search repositories.

        :param q: Search keywords.
        :param page: Page number.
        :param per_page: Page size.
        :param sort: Optional sort field such as ``stars_count``.
        :param order: Sort order, usually ``asc`` or ``desc``.
        :param owner: Optional owner path filter.
        :param fork: Optional fork visibility filter.
        :param language: Optional programming language filter.
        :returns: Matching repository search results.
        """
        return self._models(
            "GET",
            self._client._path("search", "repositories"),
            SearchRepository,
            params={
                "q": q,
                "page": page,
                "per_page": per_page,
                "sort": sort,
                "order": order,
                "owner": owner,
                "fork": fork,
                "language": language,
            },
        )


class OAuthResource(SyncResource):
    """Helpers for GitCode OAuth URLs and token exchange."""

    def build_authorize_url(
        self,
        *,
        client_id: str,
        redirect_uri: str,
        scope: Optional[str] = None,
        state: Optional[str] = None,
        response_type: str = "code",
    ) -> str:
        """Build the GitCode OAuth authorization URL.

        :param client_id: OAuth application client ID.
        :param redirect_uri: Registered redirect URI.
        :param scope: Optional OAuth scopes.
        :param state: Optional CSRF protection value.
        :param response_type: OAuth response type, defaults to ``"code"``.
        :returns: Browser URL for the authorization step.
        """
        query = urlencode(
            {
                key: value
                for key, value in {
                    "client_id": client_id,
                    "redirect_uri": redirect_uri,
                    "response_type": response_type,
                    "scope": scope,
                    "state": state,
                }.items()
                if value is not None
            }
        )
        return f"{OAUTH_BASE_URL}/oauth/authorize?{query}"

    def exchange_token(self, *, code: str, client_id: str, client_secret: str) -> OAuthToken:
        """Exchange an authorization code for an OAuth token.

        :param code: Authorization code returned by GitCode.
        :param client_id: OAuth application client ID.
        :param client_secret: OAuth application client secret.
        :returns: OAuth access token payload.
        """
        response = httpx.post(
            f"{OAUTH_BASE_URL}/oauth/token",
            params={"grant_type": "authorization_code", "code": code, "client_id": client_id},
            data={"client_secret": client_secret},
            headers={"Accept": "application/json"},
            timeout=self._client.timeout,
        )
        response.raise_for_status()
        return OAuthToken(dict(response.json()))

    def refresh_token(self, *, refresh_token: str) -> OAuthToken:
        """Refresh an OAuth token.

        :param refresh_token: Refresh token previously issued by GitCode.
        :returns: Refreshed OAuth token payload.
        """
        response = httpx.post(
            f"{OAUTH_BASE_URL}/oauth/token",
            params={"grant_type": "refresh_token", "refresh_token": refresh_token},
            headers={"Accept": "application/json"},
            timeout=self._client.timeout,
        )
        response.raise_for_status()
        return OAuthToken(dict(response.json()))


class AsyncUsersResource(AsyncResource):
    """Asynchronous user and account endpoints.

    Mirrors :class:`UsersResource`; see that class for full parameter descriptions
    (``docs/rest_api/users`` and related guides).
    """

    async def get(self, *, username: str) -> User:
        """Get a user profile.

        :param username: GitCode username or login.
        :returns: User profile details.
        """
        return await self._model("GET", self._client._path("users", username), User)

    async def me(self) -> User:
        """Get the profile of the authenticated user.

        :returns: Authorized user profile.
        """
        return await self._model("GET", self._client._path("user"), User)

    async def list_emails(self) -> List[Email]:
        """List email addresses for the authenticated user.

        :returns: Email records associated with the current account.
        """
        return await self._models("GET", self._client._path("emails"), Email)

    async def list_events(
        self, *, username: str, year: Optional[str] = None, next: Optional[str] = None
    ) -> UserEventsResponse:
        """List activity events for a user.

        :param username: GitCode username or login (path segment, see User API).
        :param year: Optional start year filter (query ``year``, e.g. ``2024`` per documentation).
        :param next: Optional end date / pagination cursor (query ``next``; often an ISO timestamp from a prior page).
        :returns: Event payload grouped by date.
        """
        return await self._model(
            "GET",
            self._client._path("users", username, "events"),
            UserEventsResponse,
            params={"year": year, "next": next},
        )

    async def list_repos(self, *, username: str, **params) -> List[Repository]:
        """List public repositories owned by a user.

        Supported filters follow the user repository API documentation, such as
        ``type``, ``sort``, ``direction``, ``page``, and ``per_page``.

        :param username: GitCode username or login.
        :param params: Query parameters accepted by the REST endpoint.
        :returns: Matching repositories.
        """
        return await self._models("GET", self._client._path("users", username, "repos"), Repository, params=params)

    async def create_key(self, *, key: str, title: str) -> PublicKey:
        """Add a public SSH key for the authenticated user.

        :param key: Public key material.
        :param title: Human-readable key name.
        :returns: Created key metadata.
        """
        return await self._model(
            "POST", self._client._path("user", "keys"), PublicKey, json={"key": key, "title": title}
        )

    async def list_keys(self, *, page: Optional[int] = None, per_page: Optional[int] = None) -> List[APIObject]:
        """List public SSH keys for the authenticated user.

        :param page: Page number.
        :param per_page: Page size.
        :returns: Public key records.
        """
        data = await self._request(
            "GET", self._client._path("user", "keys"), params={"page": page, "per_page": per_page}
        )
        return [APIObject(dict(item)) for item in data]

    async def delete_key(self, *, key_id: Union[int, str]) -> None:
        """Delete a public SSH key.

        :param key_id: Public key identifier.
        """
        await self._request("DELETE", self._client._path("user", "keys", key_id))

    async def get_key(self, *, key_id: Union[int, str]) -> PublicKey:
        """Get a single public SSH key.

        :param key_id: Public key identifier.
        :returns: Public key metadata.
        """
        return await self._model("GET", self._client._path("user", "keys", key_id), PublicKey)

    async def get_namespace(self, *, path: str) -> Namespace:
        """Resolve namespace information for the authenticated user.

        :param path: Namespace path to look up.
        :returns: Namespace details.
        """
        return await self._model("GET", self._client._path("user", "namespace"), Namespace, params={"path": path})

    async def list_starred(
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
        return await self._models(
            "GET",
            self._client._path("user", "starred"),
            Repository,
            params={"sort": sort, "direction": direction, "page": page, "per_page": per_page},
        )


class AsyncOrgsResource(AsyncResource):
    """Asynchronous organization and enterprise endpoints.

    Mirrors :class:`OrgsResource`; see that class for parameters (``docs/rest_api/orgs``).
    """

    async def list_for_user(
        self, *, username: str, page: Optional[int] = None, per_page: Optional[int] = None
    ) -> List[OrganizationSummary]:
        """List organizations for a user.

        :param username: GitCode username or login.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Organizations the user belongs to.
        """
        return await self._models(
            "GET",
            self._client._path("users", username, "orgs"),
            OrganizationSummary,
            params={"page": page, "per_page": per_page},
        )

    async def list_authenticated(
        self, *, page: Optional[int] = None, per_page: Optional[int] = None, admin: Optional[bool] = None
    ) -> List[OrganizationSummary]:
        """List organizations for the authenticated user.

        :param page: Page number.
        :param per_page: Page size.
        :param admin: Optional admin-only filter.
        :returns: Organizations visible to the authorized user.
        """
        return await self._models(
            "GET",
            self._client._path("users", "orgs"),
            OrganizationSummary,
            params={"page": page, "per_page": per_page, "admin": admin},
        )

    async def get_member(self, *, org: str, username: str) -> OrganizationMembership:
        """Get an organization member profile.

        :param org: Organization path or login.
        :param username: Member username or login.
        :returns: Organization membership details.
        """
        return await self._model("GET", self._client._path("orgs", org, "members", username), OrganizationMembership)

    async def get(self, *, org: str) -> Organization:
        """Get an organization.

        :param org: Organization path or login.
        :returns: Organization details.
        """
        return await self._model("GET", self._client._path("orgs", org), Organization)

    async def list_repos(
        self, *, org: str, type: Optional[str] = None, page: Optional[int] = None, per_page: Optional[int] = None
    ) -> List[Repository]:
        """List repositories for an organization.

        :param org: Organization path or login.
        :param type: Repository type filter such as ``all``, ``public``, or ``private``.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Matching repositories.
        """
        return await self._models(
            "GET",
            self._client._path("orgs", org, "repos"),
            Repository,
            params={"type": type, "page": page, "per_page": per_page},
        )

    async def create_repo(self, *, org: str, name: str, **payload) -> Repository:
        """Create an organization repository.

        Additional payload fields match the organization repository creation
        endpoint, such as ``description``, ``homepage``, ``private``,
        ``public``, ``auto_init``, and ``default_branch``.

        :param org: Organization path or login.
        :param name: Repository name.
        :param payload: Additional repository creation fields.
        :returns: Created repository metadata.
        """
        payload["name"] = name
        return await self._model("POST", self._client._path("orgs", org, "repos"), Repository, json=payload)

    async def get_enterprise_member(self, *, enterprise: str, username: str) -> EnterpriseMember:
        """Get a member profile for an enterprise.

        :param enterprise: Enterprise path or login.
        :param username: Member username or login.
        :returns: Enterprise membership details.
        """
        return await self._model(
            "GET", self._client._path("enterprises", enterprise, "members", username), EnterpriseMember
        )

    async def get_membership(self, *, org: str) -> OrganizationMembership:
        """Get the authenticated user's membership in an organization.

        :param org: Organization path or login.
        :returns: Membership details for the current user.
        """
        return await self._model("GET", self._client._path("user", "memberships", "orgs", org), OrganizationMembership)

    async def list_members(
        self, *, org: str, page: Optional[int] = None, per_page: Optional[int] = None, role: Optional[str] = None
    ) -> List[User]:
        """List members of an organization.

        :param org: Organization path or login.
        :param page: Page number.
        :param per_page: Page size.
        :param role: Optional role filter such as ``all``, ``admin``, or ``member``.
        :returns: Organization members.
        """
        return await self._models(
            "GET",
            self._client._path("orgs", org, "members"),
            User,
            params={"page": page, "per_page": per_page, "role": role},
        )

    async def list_enterprise_members(
        self, *, enterprise: str, page: Optional[int] = None, per_page: Optional[int] = None, role: Optional[str] = None
    ) -> List[EnterpriseMember]:
        """List members of an enterprise.

        :param enterprise: Enterprise path or login.
        :param page: Page number.
        :param per_page: Page size.
        :param role: Optional role filter.
        :returns: Enterprise members.
        """
        return await self._models(
            "GET",
            self._client._path("enterprises", enterprise, "members"),
            EnterpriseMember,
            params={"page": page, "per_page": per_page, "role": role},
        )

    async def remove_member(self, *, org: str, username: str) -> EmptyResponse:
        """Remove a member from an organization.

        :param org: Organization path or login.
        :param username: Member username or login.
        :returns: API response payload, if any.
        """
        return await self._model("DELETE", self._client._path("orgs", org, "memberships", username), EmptyResponse)

    async def list_followers(
        self, *, owner: str, page: Optional[int] = None, per_page: Optional[int] = None
    ) -> List[User]:
        """List followers of an organization.

        :param owner: Organization path.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Followers of the organization.
        """
        return await self._models(
            "GET", self._client._path("orgs", owner, "followers"), User, params={"page": page, "per_page": per_page}
        )

    async def get_issue_extend_settings(self, *, org: str) -> List[APIObject]:
        """Get extended issue type and status settings for an organization.

        :param org: Organization path or login.
        :returns: Extended issue configuration entries.
        """
        data = await self._request("GET", self._client._path("orgs", org, "issue", "extend", "settings"))
        return [APIObject(dict(item)) for item in data]

    async def invite_member(
        self, *, org: str, username: str, permission: Optional[str] = None, role_id: Optional[str] = None
    ) -> User:
        """Invite a user to an organization.

        :param org: Organization path or login.
        :param username: Member username or login.
        :param permission: Permission level such as ``pull``, ``push``, or ``admin``.
        :param role_id: Custom role identifier when using a customized permission.
        :returns: Invited user information with permissions.
        """
        return await self._model(
            "POST",
            self._client._path("orgs", org, "memberships", username),
            User,
            json={"permission": permission, "role_id": role_id},
        )

    async def update_enterprise_member(self, *, enterprise: str, username: str, role: str) -> EnterpriseMember:
        """Update the role of an enterprise member.

        :param enterprise: Enterprise path or login.
        :param username: Member username or login.
        :param role: Enterprise role such as ``viewer``, ``developer``, or ``admin``.
        :returns: Updated enterprise membership.
        """
        return await self._model(
            "PUT",
            self._client._path("enterprises", enterprise, "members", username),
            EnterpriseMember,
            json={"role": role},
        )

    async def update(self, *, org: str, **payload) -> Organization:
        """Update organization metadata.

        :param org: Organization path or login.
        :param payload: Updatable fields such as ``name``, ``email``, or ``description``.
        :returns: Updated organization details.
        """
        return await self._model("PATCH", self._client._path("orgs", org), Organization, json=payload)

    async def leave(self, *, org: str) -> None:
        """Leave an organization as the authenticated user.

        :param org: Organization path or login.
        """
        await self._request("DELETE", self._client._path("user", "memberships", "orgs", org))


class AsyncSearchResource(AsyncResource):
    """Asynchronous search endpoints.

    Query parameters match :class:`SearchResource` (``page``, ``per_page``, ``sort``, ``order``, etc.);
    see ``docs/rest_api/search`` and the synchronous methods for field meanings.
    """

    async def users(self, *, q: str, **params) -> List[SearchUser]:
        """Search users.

        :param q: Search keywords (required).
        :param params: Optional query parameters merged into the request, such as ``page``,
            ``per_page``, ``sort``, and ``order`` (same meanings as :meth:`SearchResource.users`).
        :returns: Matching user search results.
        """
        return await self._models("GET", self._client._path("search", "users"), SearchUser, params={"q": q, **params})

    async def issues(self, *, q: str, **params) -> List[SearchIssue]:
        """Search issues.

        :param q: Search keywords (required).
        :param params: Optional query parameters merged into the request, such as ``page``,
            ``per_page``, ``sort``, ``order``, ``repo``, and ``state`` (see :meth:`SearchResource.issues`).
        :returns: Matching issue search results.
        """
        return await self._models("GET", self._client._path("search", "issues"), SearchIssue, params={"q": q, **params})

    async def repositories(self, *, q: str, **params) -> List[SearchRepository]:
        """Search repositories.

        :param q: Search keywords (required).
        :param params: Optional query parameters merged into the request, such as ``page``,
            ``per_page``, ``sort``, ``order``, ``owner``, ``fork``, and ``language``
            (see :meth:`SearchResource.repositories`).
        :returns: Matching repository search results.
        """
        return await self._models(
            "GET", self._client._path("search", "repositories"), SearchRepository, params={"q": q, **params}
        )


class AsyncOAuthResource(AsyncResource):
    """Asynchronous helpers for GitCode OAuth flows.

    ``build_authorize_url`` matches :class:`OAuthResource` exactly. Token helpers mirror
    :meth:`OAuthResource.exchange_token` and :meth:`OAuthResource.refresh_token` (see ``docs/rest_api/oauth``).
    """

    def build_authorize_url(
        self,
        *,
        client_id: str,
        redirect_uri: str,
        scope: Optional[str] = None,
        state: Optional[str] = None,
        response_type: str = "code",
    ) -> str:
        """Build the GitCode OAuth authorization URL.

        :param client_id: OAuth application client ID.
        :param redirect_uri: Registered redirect URI.
        :param scope: Optional OAuth scopes.
        :param state: Optional CSRF protection value.
        :param response_type: OAuth response type, defaults to ``"code"``.
        :returns: Browser URL for the authorization step.
        """
        query = urlencode(
            {
                key: value
                for key, value in {
                    "client_id": client_id,
                    "redirect_uri": redirect_uri,
                    "response_type": response_type,
                    "scope": scope,
                    "state": state,
                }.items()
                if value is not None
            }
        )
        return f"{OAUTH_BASE_URL}/oauth/authorize?{query}"

    async def exchange_token(self, *, code: str, client_id: str, client_secret: str) -> OAuthToken:
        """Exchange an authorization code for an OAuth token.

        :param code: Authorization code returned by GitCode.
        :param client_id: OAuth application client ID.
        :param client_secret: OAuth application client secret.
        :returns: OAuth access token payload.
        """
        async with httpx.AsyncClient(timeout=self._client.timeout) as client:
            response = await client.post(
                f"{OAUTH_BASE_URL}/oauth/token",
                params={"grant_type": "authorization_code", "code": code, "client_id": client_id},
                data={"client_secret": client_secret},
                headers={"Accept": "application/json"},
            )
        response.raise_for_status()
        return OAuthToken(dict(response.json()))

    async def refresh_token(self, *, refresh_token: str) -> OAuthToken:
        """Refresh an OAuth token.

        :param refresh_token: Refresh token previously issued by GitCode.
        :returns: Refreshed OAuth token payload.
        """
        async with httpx.AsyncClient(timeout=self._client.timeout) as client:
            response = await client.post(
                f"{OAUTH_BASE_URL}/oauth/token",
                params={"grant_type": "refresh_token", "refresh_token": refresh_token},
                headers={"Accept": "application/json"},
            )
        response.raise_for_status()
        return OAuthToken(dict(response.json()))
