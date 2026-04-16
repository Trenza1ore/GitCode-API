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
