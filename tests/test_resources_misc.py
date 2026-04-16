from typing import Optional

import httpx
import pytest


def test_labels_list_enterprise_v8_uses_absolute_versioned_url(sync_client_factory) -> None:
    seen_url: Optional[str] = None

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal seen_url
        seen_url = str(request.url)
        return httpx.Response(200, json=[{"name": "bug", "color": "#f00"}])

    client, http_client = sync_client_factory(handler, base_url="https://api.gitcode.com/api/v5")
    try:
        labels = client.labels.list_enterprise(enterprise="SushiNinja", api_version="v8", search="bug")
        assert labels[0].name == "bug"
        assert seen_url == "https://api.gitcode.com/api/v8/enterprises/acme/labels?search=bug"
    finally:
        client.close()
        http_client.close()


@pytest.mark.asyncio
async def test_async_webhooks_test_hits_expected_endpoint(async_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/v5/repos/acme/demo/hooks/44/tests"
        return httpx.Response(204)

    client, http_client = async_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        result = await client.webhooks.test(hook_id=44)
        assert result is None
    finally:
        await client.close()
        await http_client.aclose()
