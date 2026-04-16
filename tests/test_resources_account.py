from typing import Any, Dict

import httpx
import pytest

from gitcode_api import AsyncGitCode
from gitcode_api.resources import account as account_resources


def test_oauth_authorize_url_omits_none_values(sync_client_factory) -> None:
    client, http_client = sync_client_factory(lambda request: httpx.Response(200, json={}))
    try:
        url = client.oauth.build_authorize_url(client_id="abc", redirect_uri="https://example.com/callback")
    finally:
        client.close()
        http_client.close()

    assert "scope=" not in url
    assert "state=" not in url
    assert "client_id=abc" in url


def test_search_repositories_passes_expected_query_params(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v5/search/repositories"
        assert request.url.params["q"] == "sdk"
        assert request.url.params["owner"] == "SushiNinja"
        assert request.url.params["language"] == "Python"
        return httpx.Response(200, json=[{"full_name": "SushiNinja/sdk"}])

    client, http_client = sync_client_factory(handler)
    try:
        results = client.search.repositories(q="sdk", owner="SushiNinja", language="Python")
        assert results[0].full_name == "SushiNinja/sdk"
    finally:
        client.close()
        http_client.close()


def test_oauth_exchange_token_uses_expected_request(monkeypatch: pytest.MonkeyPatch, sync_client_factory) -> None:
    captured: Dict[str, Any] = {}

    def fake_post(url: str, **kwargs) -> httpx.Response:
        captured["url"] = url
        captured["kwargs"] = kwargs
        return httpx.Response(
            200,
            json={"access_token": "token-123"},
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(account_resources.httpx, "post", fake_post)

    client, http_client = sync_client_factory(lambda request: httpx.Response(200, json={}))
    try:
        token = client.oauth.exchange_token(code="abc", client_id="cid", client_secret="secret")
        assert token.access_token == "token-123"
        assert captured["url"] == "https://gitcode.com/oauth/token"
        assert captured["kwargs"]["params"]["grant_type"] == "authorization_code"
        assert captured["kwargs"]["data"]["client_secret"] == "secret"
    finally:
        client.close()
        http_client.close()


@pytest.mark.asyncio
async def test_async_oauth_refresh_token_uses_async_http_client(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: Dict[str, Any] = {}
    http_client = httpx.AsyncClient(transport=httpx.MockTransport(lambda request: httpx.Response(200, json={})))

    class FakeAsyncClient:
        def __init__(self, **kwargs) -> None:
            captured["init"] = kwargs

        async def __aenter__(self) -> "FakeAsyncClient":
            return self

        async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
            return None

        async def post(self, url: str, **kwargs) -> httpx.Response:
            captured["url"] = url
            captured["kwargs"] = kwargs
            return httpx.Response(
                200,
                json={"refresh_token": "new-refresh"},
                request=httpx.Request("POST", url),
            )

    monkeypatch.setattr(account_resources.httpx, "AsyncClient", FakeAsyncClient)

    client = AsyncGitCode(api_key="test-token", http_client=http_client)
    try:
        token = await client.oauth.refresh_token(refresh_token="refresh-123")
        assert token.refresh_token == "new-refresh"
        assert captured["url"] == "https://gitcode.com/oauth/token"
        assert captured["kwargs"]["params"]["grant_type"] == "refresh_token"
        assert captured["kwargs"]["params"]["refresh_token"] == "refresh-123"
    finally:
        await client.close()
        await http_client.aclose()
