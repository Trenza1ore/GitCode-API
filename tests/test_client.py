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
