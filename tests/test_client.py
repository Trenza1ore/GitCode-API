import httpx
import pytest

from gitcode_api import AsyncGitCode, GitCode


def test_client_reads_api_key_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITCODE_ACCESS_TOKEN", "env-token")
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={"login": "octo"}))

    with httpx.Client(transport=transport) as http_client:
        client = GitCode(http_client=http_client)
        assert client.api_key == "env-token"


def test_sync_client_exposes_resource_namespaces() -> None:
    with httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(200, json={}))) as http_client:
        client = GitCode(api_key="test-token", http_client=http_client)
        assert client.repos is not None
        assert client.pulls is not None
        assert client.users is not None
        assert client.oauth is not None


@pytest.mark.asyncio
async def test_async_client_exposes_resource_namespaces() -> None:
    async_client = httpx.AsyncClient(transport=httpx.MockTransport(lambda request: httpx.Response(200, json={})))
    client = AsyncGitCode(api_key="test-token", http_client=async_client)
    try:
        assert client.repos is not None
        assert client.pulls is not None
        assert client.users is not None
        assert client.oauth is not None
    finally:
        await async_client.aclose()


def test_sync_client_context_manager_closes_owned_http_client(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_transport = httpx.MockTransport(lambda request: httpx.Response(200, json={}))
    real_client = httpx.Client

    def client_with_mock_transport(*args: object, **kwargs: object) -> httpx.Client:
        merged = dict(kwargs)
        merged.setdefault("transport", mock_transport)
        return real_client(*args, **merged)

    monkeypatch.setattr(httpx, "Client", client_with_mock_transport)
    with GitCode(api_key="test-token", owner="o", repo="r") as client:
        assert client._client.is_closed is False
    assert client._client.is_closed is True


def test_sync_client_context_manager_does_not_close_injected_http_client() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={}))
    http_client = httpx.Client(transport=transport)
    try:
        with GitCode(api_key="test-token", http_client=http_client, owner="o", repo="r"):
            pass
        assert http_client.is_closed is False
    finally:
        http_client.close()


@pytest.mark.asyncio
async def test_async_client_context_manager_closes_owned_http_client(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_transport = httpx.MockTransport(lambda request: httpx.Response(200, json={}))
    real_async_client = httpx.AsyncClient

    def async_client_with_mock_transport(*args: object, **kwargs: object) -> httpx.AsyncClient:
        merged = dict(kwargs)
        merged.setdefault("transport", mock_transport)
        return real_async_client(*args, **merged)

    monkeypatch.setattr(httpx, "AsyncClient", async_client_with_mock_transport)
    async with AsyncGitCode(api_key="test-token", owner="o", repo="r") as client:
        assert client._client.is_closed is False
    assert client._client.is_closed is True


@pytest.mark.asyncio
async def test_async_client_context_manager_does_not_close_injected_http_client() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={}))
    http_client = httpx.AsyncClient(transport=transport)
    try:
        async with AsyncGitCode(api_key="test-token", http_client=http_client, owner="o", repo="r"):
            pass
        assert http_client.is_closed is False
    finally:
        await http_client.aclose()
