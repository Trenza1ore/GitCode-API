"""AbstractOAuthResource, OAuthResource, and AsyncOAuthResource resource group."""

from abc import ABC, abstractmethod
from typing import Optional
from urllib.parse import urlencode

import httpx

from ..._models import OAuthToken
from .._shared import AsyncResource, SyncResource

# mypy: disable-error-code=override
# pylint: disable=invalid-overridden-method,protected-access,redefined-builtin

OAUTH_BASE_URL = "https://gitcode.com"


class AbstractOAuthResource(ABC):
    """Interface for OAuth resource endpoints."""

    @abstractmethod
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

    @abstractmethod
    def exchange_token(self, *, code: str, client_id: str, client_secret: str) -> OAuthToken:
        """Exchange an authorization code for an OAuth token.

        :param code: Authorization code returned by GitCode.
        :param client_id: OAuth application client ID.
        :param client_secret: OAuth application client secret.
        :returns: OAuth access token payload.
        """

    @abstractmethod
    def refresh_token(self, *, refresh_token: str) -> OAuthToken:
        """Refresh an OAuth token.

        :param refresh_token: Refresh token previously issued by GitCode.
        :returns: Refreshed OAuth token payload.
        """


class OAuthResource(SyncResource, AbstractOAuthResource):
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
        response = httpx.post(
            f"{OAUTH_BASE_URL}/oauth/token",
            params={"grant_type": "refresh_token", "refresh_token": refresh_token},
            headers={"Accept": "application/json"},
            timeout=self._client.timeout,
        )
        response.raise_for_status()
        return OAuthToken(dict(response.json()))


class AsyncOAuthResource(AsyncResource, AbstractOAuthResource):
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
