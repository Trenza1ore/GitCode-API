"""Account, organization, search, and OAuth resource groups."""

from typing import Any, List, Optional, Union
from urllib.parse import urlencode

import httpx

from .._models import (
    APIObject,
    Email,
    EnterpriseMember,
    Namespace,
    OAuthToken,
    Organization,
    OrganizationMembership,
    Repository,
    SearchResult,
    User,
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

    def list_events(self, *, username: str, year: Optional[str] = None, next: Optional[str] = None) -> APIObject:
        """List activity events for a user.

        :param username: GitCode username or login.
        :param year: Optional start year filter.
        :param next: Optional pagination cursor from a previous response.
        :returns: Event payload grouped by date.
        """
        return self._model(
            "GET", self._client._path("users", username, "events"), APIObject, params={"year": year, "next": next}
        )

    def list_repos(self, *, username: str, **params: Any) -> List[Repository]:
        """List public repositories owned by a user.

        Supported filters follow the user repository API documentation, such as
        ``type``, ``sort``, ``direction``, ``page``, and ``per_page``.

        :param username: GitCode username or login.
        :param params: Query parameters accepted by the REST endpoint.
        :returns: Matching repositories.
        """
        return self._models("GET", self._client._path("users", username, "repos"), Repository, params=params)

    def create_key(self, *, key: str, title: str) -> APIObject:
        """Add a public SSH key for the authenticated user.

        :param key: Public key material.
        :param title: Human-readable key name.
        :returns: Created key metadata.
        """
        return self._model("POST", self._client._path("user", "keys"), APIObject, json={"key": key, "title": title})

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

    def get_key(self, *, key_id: Union[int, str]) -> APIObject:
        """Get a single public SSH key.

        :param key_id: Public key identifier.
        :returns: Public key metadata.
        """
        return self._model("GET", self._client._path("user", "keys", key_id), APIObject)

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
    ) -> List[Organization]:
        """List organizations for a user.

        :param username: GitCode username or login.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Organizations the user belongs to.
        """
        return self._models(
            "GET",
            self._client._path("users", username, "orgs"),
            Organization,
            params={"page": page, "per_page": per_page},
        )

    def list_authenticated(
        self, *, page: Optional[int] = None, per_page: Optional[int] = None, admin: Optional[bool] = None
    ) -> List[Organization]:
        """List organizations for the authenticated user.

        :param page: Page number.
        :param per_page: Page size.
        :param admin: Optional admin-only filter.
        :returns: Organizations visible to the authorized user.
        """
        return self._models(
            "GET",
            self._client._path("users", "orgs"),
            Organization,
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

    def create_repo(self, *, org: str, name: str, **payload: Any) -> Repository:
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

    def remove_member(self, *, org: str, username: str) -> APIObject:
        """Remove a member from an organization.

        :param org: Organization path or login.
        :param username: Member username or login.
        :returns: API response payload, if any.
        """
        return self._model("DELETE", self._client._path("orgs", org, "memberships", username), APIObject)

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

    def update(self, *, org: str, **payload: Any) -> Organization:
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
    ) -> List[SearchResult]:
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
            SearchResult,
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
    ) -> List[SearchResult]:
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
            SearchResult,
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
    ) -> List[SearchResult]:
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
            SearchResult,
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
    """Asynchronous user and account endpoints."""

    async def get(self, *, username: str) -> User:
        return await self._model("GET", self._client._path("users", username), User)

    async def me(self) -> User:
        return await self._model("GET", self._client._path("user"), User)

    async def list_emails(self) -> List[Email]:
        return await self._models("GET", self._client._path("emails"), Email)

    async def list_events(self, *, username: str, year: Optional[str] = None, next: Optional[str] = None) -> APIObject:
        return await self._model(
            "GET", self._client._path("users", username, "events"), APIObject, params={"year": year, "next": next}
        )

    async def list_repos(self, *, username: str, **params: Any) -> List[Repository]:
        return await self._models("GET", self._client._path("users", username, "repos"), Repository, params=params)

    async def create_key(self, *, key: str, title: str) -> APIObject:
        return await self._model(
            "POST", self._client._path("user", "keys"), APIObject, json={"key": key, "title": title}
        )

    async def list_keys(self, *, page: Optional[int] = None, per_page: Optional[int] = None) -> List[APIObject]:
        data = await self._request(
            "GET", self._client._path("user", "keys"), params={"page": page, "per_page": per_page}
        )
        return [APIObject(dict(item)) for item in data]

    async def delete_key(self, *, key_id: Union[int, str]) -> None:
        await self._request("DELETE", self._client._path("user", "keys", key_id))

    async def get_key(self, *, key_id: Union[int, str]) -> APIObject:
        return await self._model("GET", self._client._path("user", "keys", key_id), APIObject)

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


class AsyncOrgsResource(AsyncResource):
    """Asynchronous organization and enterprise endpoints."""

    async def list_for_user(
        self, *, username: str, page: Optional[int] = None, per_page: Optional[int] = None
    ) -> List[Organization]:
        return await self._models(
            "GET",
            self._client._path("users", username, "orgs"),
            Organization,
            params={"page": page, "per_page": per_page},
        )

    async def list_authenticated(
        self, *, page: Optional[int] = None, per_page: Optional[int] = None, admin: Optional[bool] = None
    ) -> List[Organization]:
        return await self._models(
            "GET",
            self._client._path("users", "orgs"),
            Organization,
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

    async def create_repo(self, *, org: str, name: str, **payload: Any) -> Repository:
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

    async def remove_member(self, *, org: str, username: str) -> APIObject:
        return await self._model("DELETE", self._client._path("orgs", org, "memberships", username), APIObject)

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

    async def update(self, *, org: str, **payload: Any) -> Organization:
        return await self._model("PATCH", self._client._path("orgs", org), Organization, json=payload)

    async def leave(self, *, org: str) -> None:
        await self._request("DELETE", self._client._path("user", "memberships", "orgs", org))


class AsyncSearchResource(AsyncResource):
    """Asynchronous search endpoints."""

    async def users(self, *, q: str, **params: Any) -> List[SearchResult]:
        return await self._models("GET", self._client._path("search", "users"), SearchResult, params={"q": q, **params})

    async def issues(self, *, q: str, **params: Any) -> List[SearchResult]:
        return await self._models(
            "GET", self._client._path("search", "issues"), SearchResult, params={"q": q, **params}
        )

    async def repositories(self, *, q: str, **params: Any) -> List[SearchResult]:
        return await self._models(
            "GET", self._client._path("search", "repositories"), SearchResult, params={"q": q, **params}
        )


class AsyncOAuthResource(AsyncResource):
    """Asynchronous helpers for GitCode OAuth flows."""

    def build_authorize_url(
        self,
        *,
        client_id: str,
        redirect_uri: str,
        scope: Optional[str] = None,
        state: Optional[str] = None,
        response_type: str = "code",
    ) -> str:
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
        async with httpx.AsyncClient(timeout=self._client.timeout) as client:
            response = await client.post(
                f"{OAUTH_BASE_URL}/oauth/token",
                params={"grant_type": "refresh_token", "refresh_token": refresh_token},
                headers={"Accept": "application/json"},
            )
        response.raise_for_status()
        return OAuthToken(dict(response.json()))
