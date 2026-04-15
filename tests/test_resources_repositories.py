import httpx
import pytest


def test_sync_raw_contents_path_keeps_nested_file_segments(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v5/repos/acme/demo/raw/src/module.py"
        assert request.url.params["ref"] == "main"
        return httpx.Response(200, content=b"print('ok')", headers={"Content-Type": "text/plain"})

    client, http_client = sync_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        content = client.contents.get_raw(path="src/module.py", ref="main")
        assert content == b"print('ok')"
    finally:
        client.close()
        http_client.close()


def test_repos_list_user_strips_none_query_params(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v5/user/repos"
        assert "visibility" not in request.url.params
        assert request.url.params["page"] == "2"
        assert request.url.params["per_page"] == "10"
        return httpx.Response(200, json=[{"full_name": "acme/demo"}])

    client, http_client = sync_client_factory(handler)
    try:
        repos = client.repos.list_user(page=2, per_page=10)
        assert repos[0].full_name == "acme/demo"
    finally:
        client.close()
        http_client.close()


@pytest.mark.asyncio
async def test_async_branch_list_and_model_access(async_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v5/repos/acme/demo/branches"
        return httpx.Response(
            200,
            json=[
                {
                    "name": "main",
                    "protected": True,
                    "commit": {"sha": "abc123"},
                }
            ],
        )

    client, http_client = async_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        branches = await client.branches.list()
        assert branches[0].name == "main"
        assert branches[0].commit.sha == "abc123"
    finally:
        await client.close()
        await http_client.aclose()
