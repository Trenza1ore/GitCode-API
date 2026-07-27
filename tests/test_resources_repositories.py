import json

import httpx
import pytest


def test_sync_raw_contents_path_keeps_nested_file_segments(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v5/repos/SushiNinja/GitCode-API/raw/src/module.py"
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
        return httpx.Response(200, json=[{"full_name": "SushiNinja/GitCode-API"}])

    client, http_client = sync_client_factory(handler)
    try:
        repos = client.repos.list_user(page=2, per_page=10)
        assert repos[0].full_name == "SushiNinja/GitCode-API"
    finally:
        client.close()
        http_client.close()


def test_repos_check_sync_repo(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/v5/repos/o/r/sync_repo"
        assert request.url.params.get("branch") == "main"
        return httpx.Response(200, json={"repo_sync_result": True, "repo_sync_message": "success"})

    client, http_client = sync_client_factory(handler, owner="o", repo="r")
    try:
        result = client.repos.check_sync_repo(branch="main")
        assert result.repo_sync_result is True
        assert result.repo_sync_message == "success"
    finally:
        client.close()
        http_client.close()


def test_repos_sync_repo(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "PUT"
        assert request.url.path == "/api/v5/repos/o/r/sync_repo"
        assert json.loads(request.content.decode()) == {"branch": "main"}
        return httpx.Response(200, json={"repo_sync_result": True, "repo_sync_message": "sync success"})

    client, http_client = sync_client_factory(handler, owner="o", repo="r")
    try:
        result = client.repos.sync_repo(branch="main")
        assert result.repo_sync_result is True
        assert result.repo_sync_message == "sync success"
    finally:
        client.close()
        http_client.close()


@pytest.mark.asyncio
async def test_async_repos_check_sync_repo(async_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/v5/repos/o/r/sync_repo"
        return httpx.Response(200, json={"repo_sync_result": False, "repo_sync_message": "pending"})

    client, http_client = async_client_factory(handler, owner="o", repo="r")
    try:
        result = await client.repos.check_sync_repo()
        assert result.repo_sync_result is False
        assert result.repo_sync_message == "pending"
    finally:
        await client.close()
        await http_client.aclose()


@pytest.mark.asyncio
async def test_async_branch_list_and_model_access(async_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v5/repos/SushiNinja/GitCode-API/branches"
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
