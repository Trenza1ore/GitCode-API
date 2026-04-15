import httpx
import pytest

from gitcode_api._exceptions import GitCodeConfigurationError, GitCodeHTTPStatusError


def test_client_requires_api_key_when_not_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GITCODE_ACCESS_TOKEN", raising=False)

    with pytest.raises(GitCodeConfigurationError):
        from gitcode_api import GitCode

        GitCode(api_key=None)


def test_missing_repo_context_raises_for_repo_resource(sync_client_factory) -> None:
    client, http_client = sync_client_factory(lambda request: httpx.Response(200, json={}))
    try:
        with pytest.raises(GitCodeConfigurationError):
            client.repos.get()
    finally:
        client.close()
        http_client.close()


def test_http_error_exposes_status_payload_and_request_id(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            404,
            json={"message": "404 Not Found"},
            headers={"X-Request-Id": "req-123"},
        )

    client, http_client = sync_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        with pytest.raises(GitCodeHTTPStatusError) as exc_info:
            client.repos.get()
        assert exc_info.value.status_code == 404
        assert exc_info.value.request_id == "req-123"
        assert exc_info.value.payload == {"message": "404 Not Found"}
    finally:
        client.close()
        http_client.close()


def test_parse_response_returns_plain_text_when_json_decoding_fails(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="plain-text", headers={"Content-Type": "text/plain"})

    client, http_client = sync_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        result = client.request("GET", "/plain-text")
        assert result == "plain-text"
    finally:
        client.close()
        http_client.close()


@pytest.mark.asyncio
async def test_async_client_surfaces_http_errors(async_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(422, json={"message": "bad payload"})

    client, http_client = async_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        with pytest.raises(GitCodeHTTPStatusError) as exc_info:
            await client.repos.get()
        assert exc_info.value.status_code == 422
        assert exc_info.value.payload == {"message": "bad payload"}
    finally:
        await client.close()
        await http_client.aclose()
