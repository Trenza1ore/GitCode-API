import json

import httpx
import pytest

from gitcode_api._models import PullRequestCount, RepoCollaborator


def test_sync_pull_create_uses_default_owner_repo(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v5/repos/SushiNinja/GitCode-API/pulls"
        assert request.headers["Authorization"] == "Bearer test-token"
        payload = {
            "number": 7,
            "title": "Add feature",
            "state": "opened",
            "head": {"ref": "feature"},
            "base": {"ref": "main"},
        }
        return httpx.Response(200, json=payload)

    client, http_client = sync_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        pull = client.pulls.create(title="Add feature", head="feature", base="main")
        assert pull.title == "Add feature"
        assert pull.number == 7
    finally:
        client.close()
        http_client.close()


def test_issues_create_uses_client_default_repo_and_joins_labels(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v5/repos/SushiNinja/issues"
        assert request.headers["Authorization"] == "Bearer test-token"
        payload = request.read().decode()
        assert '"repo":"GitCode-API"' in payload
        assert '"labels":"bug,docs"' in payload
        return httpx.Response(200, json={"number": 15, "title": "Test issue"})

    client, http_client = sync_client_factory(handler, repo="GitCode-API")
    try:
        issue = client.issues.create(owner="SushiNinja", title="Test issue", labels=["bug", "docs"])
        assert issue.number == 15
        assert issue.title == "Test issue"
    finally:
        client.close()
        http_client.close()


def test_pulls_list_returns_count_model_for_only_count_mode(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["only_count"] == "true"
        return httpx.Response(200, json={"all": 10, "opened": 4, "merged": 6})

    client, http_client = sync_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        counts = client.pulls.list(only_count=True)
        assert isinstance(counts, PullRequestCount)
        assert counts.all == 10
        assert counts.opened == 4
    finally:
        client.close()
        http_client.close()


def test_delete_operations_return_none_for_204(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "DELETE"
        return httpx.Response(204)

    client, http_client = sync_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        result = client.members.remove(username="octo")
        assert result is None
    finally:
        client.close()
        http_client.close()


@pytest.mark.asyncio
async def test_async_issues_create_joins_labels_and_uses_default_repo(async_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v5/repos/SushiNinja/issues"
        payload = request.read().decode()
        assert '"repo":"GitCode-API"' in payload
        assert '"labels":"bug,feature"' in payload
        return httpx.Response(200, json={"number": 12, "title": "Async issue"})

    client, http_client = async_client_factory(handler, repo="GitCode-API")
    try:
        issue = await client.issues.create(owner="SushiNinja", title="Async issue", labels=["bug", "feature"])
        assert issue.number == 12
    finally:
        await client.close()
        await http_client.aclose()


def test_members_list_uses_collaborator_model(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v5/repos/SushiNinja/GitCode-API/collaborators"
        return httpx.Response(200, json=[{"username": "octo", "permissions": {"admin": True}}])

    client, http_client = sync_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        members = client.members.list()
        assert isinstance(members[0], RepoCollaborator)
        assert members[0].username == "octo"
        assert members[0].permissions.admin is True
    finally:
        client.close()
        http_client.close()


def test_pull_review_and_test_requests_return_none_for_no_content(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path in {
            "/api/v5/repos/SushiNinja/GitCode-API/pulls/7/review",
            "/api/v5/repos/SushiNinja/GitCode-API/pulls/7/test",
        }
        return httpx.Response(204)

    client, http_client = sync_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        assert client.pulls.request_review(number=7, event="APPROVE") is None
        assert client.pulls.request_test(number=7, env="ci") is None
    finally:
        client.close()
        http_client.close()


def test_pulls_create_comment_sends_path_position_and_position_type(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/v5/repos/SushiNinja/GitCode-API/pulls/7/comments"
        payload = json.loads(request.read().decode())
        assert payload == {
            "body": "line note",
            "path": "src/main.py",
            "position": 12,
            "position_type": "text",
        }
        return httpx.Response(200, json={"id": 1, "body": "line note", "path": "src/main.py", "position": 12})

    client, http_client = sync_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        comment = client.pulls.create_comment(
            number=7,
            body="line note",
            path="src/main.py",
            position=12,
        )
        assert comment.id == 1
        assert comment.body == "line note"
    finally:
        client.close()
        http_client.close()


def test_pulls_create_comment_binary_position_type(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.read().decode())
        assert payload["position_type"] == "binary"
        assert payload["path"] == "assets/logo.png"
        assert payload["body"] == "file note"
        assert "commit_id" not in payload
        return httpx.Response(200, json={"id": 2, "body": "file note", "path": "assets/logo.png"})

    client, http_client = sync_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        comment = client.pulls.create_comment(
            number=7,
            body="file note",
            path="assets/logo.png",
            position_type="binary",
        )
        assert comment.id == 2
    finally:
        client.close()
        http_client.close()


@pytest.mark.asyncio
async def test_async_pulls_create_comment_sends_position_type(async_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v5/repos/SushiNinja/GitCode-API/pulls/3/comments"
        payload = json.loads(request.read().decode())
        assert payload == {
            "body": "async note",
            "path": "README.md",
            "position": 4,
            "position_type": "text",
        }
        return httpx.Response(200, json={"id": 9, "body": "async note"})

    client, http_client = async_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        comment = await client.pulls.create_comment(
            number=3,
            body="async note",
            path="README.md",
            position=4,
        )
        assert comment.id == 9
    finally:
        await client.close()
        await http_client.aclose()
