"""Tests for issue/PR ``.gitcode`` template resolution helpers."""

import httpx
import pytest
from typing import Optional

from gitcode_api import AsyncGitCode
from gitcode_api._exceptions import GitCodeHTTPStatusError

# ``_resolution_sources_*`` probes ``GET /repos/{owner}/{repo}`` for every candidate; stub these.
_REPO_METADATA_NONFORK_PATHS = frozenset(
    {
        "/api/v5/repos/acme/.gitcode",
        "/api/v5/repos/upstream/parent",
        "/api/v5/repos/upstream/.gitcode",
        "/api/v5/repos/o/.gitcode",
    }
)


def _repo_metadata_nonfork_stub(request: httpx.Request, path: str) -> Optional[httpx.Response]:
    if (
        request.method == "GET"
        and "/contents/" not in path
        and "/raw/" not in path
        and path in _REPO_METADATA_NONFORK_PATHS
    ):
        return httpx.Response(200, json={"fork": False})
    return None


def test_list_templates_fallback_to_dot_gitcode_repo(sync_client_factory):
    def handler(request: httpx.Request) -> httpx.Response:
        p = request.url.path
        stub = _repo_metadata_nonfork_stub(request, p)
        if stub is not None:
            return stub
        if p == "/api/v5/repos/acme/proj" and request.method == "GET":
            return httpx.Response(200, json={"fork": False, "id": 1})
        if p == "/api/v5/repos/acme/proj/contents/.gitcode":
            return httpx.Response(404, json={"message": "missing"})
        if p == "/api/v5/repos/acme/.gitcode/contents/.gitcode":
            return httpx.Response(
                200,
                json=[
                    {
                        "type": "file",
                        "name": "ISSUE_TEMPLATE_bug.md",
                        "path": ".gitcode/ISSUE_TEMPLATE_bug.md",
                        "sha": "sha1abc",
                    }
                ],
            )
        raise AssertionError(f"unexpected {request.method} {p}")

    client, _ = sync_client_factory(handler, owner="acme", repo="proj")
    items = client.issues.list_templates()
    assert len(items) == 1
    assert items[0].path == ".gitcode/ISSUE_TEMPLATE_bug.md"
    assert items[0].sha == "sha1abc"
    assert items[0].template_owner == "acme"
    assert items[0].template_repo == ".gitcode"


def test_list_templates_fork_parent_source(sync_client_factory):
    def handler(request: httpx.Request) -> httpx.Response:
        p = request.url.path
        stub = _repo_metadata_nonfork_stub(request, p)
        if stub is not None:
            return stub
        if p == "/api/v5/repos/acme/proj" and request.method == "GET":
            return httpx.Response(
                200,
                json={
                    "fork": True,
                    "id": 2,
                    "parent": {"full_name": "upstream/parent"},
                },
            )
        if p == "/api/v5/repos/acme/proj/contents/.gitcode":
            return httpx.Response(200, json=[])
        if p == "/api/v5/repos/acme/.gitcode/contents/.gitcode":
            return httpx.Response(200, json=[])
        if p == "/api/v5/repos/upstream/parent/contents/.gitcode":
            return httpx.Response(
                200,
                json=[
                    {
                        "type": "file",
                        "name": "ISSUE_TEMPLATE.md",
                        "path": ".gitcode/ISSUE_TEMPLATE.md",
                        "sha": "parentsha",
                    }
                ],
            )
        raise AssertionError(f"unexpected {request.method} {p}")

    client, _ = sync_client_factory(handler, owner="acme", repo="proj")
    items = client.issues.list_templates()
    assert len(items) == 1
    assert items[0].template_owner == "upstream"
    assert items[0].template_repo == "parent"
    assert items[0].path == ".gitcode/ISSUE_TEMPLATE.md"


def test_list_templates_fork_parent_dot_gitcode_repo(sync_client_factory):
    """Templates only under parent's ``.gitcode`` repo (``upstream/.gitcode``)."""

    def handler(request: httpx.Request) -> httpx.Response:
        p = request.url.path
        stub = _repo_metadata_nonfork_stub(request, p)
        if stub is not None:
            return stub
        if p == "/api/v5/repos/acme/proj" and request.method == "GET":
            return httpx.Response(
                200,
                json={
                    "fork": True,
                    "id": 2,
                    "parent": {"full_name": "upstream/parent"},
                },
            )
        if p == "/api/v5/repos/acme/proj/contents/.gitcode":
            return httpx.Response(200, json=[])
        if p == "/api/v5/repos/acme/.gitcode/contents/.gitcode":
            return httpx.Response(200, json=[])
        if p == "/api/v5/repos/upstream/parent/contents/.gitcode":
            return httpx.Response(200, json=[])
        if p == "/api/v5/repos/upstream/.gitcode/contents/.gitcode":
            return httpx.Response(
                200,
                json=[
                    {
                        "type": "file",
                        "path": ".gitcode/ISSUE_TEMPLATE_upstream_dot.md",
                        "sha": "dotsha",
                    }
                ],
            )
        raise AssertionError(f"unexpected {request.method} {p}")

    client, _ = sync_client_factory(handler, owner="acme", repo="proj")
    items = client.issues.list_templates()
    assert len(items) == 1
    assert items[0].template_owner == "upstream"
    assert items[0].template_repo == ".gitcode"
    assert items[0].path == ".gitcode/ISSUE_TEMPLATE_upstream_dot.md"


def test_list_templates_includes_yaml_issue_forms(sync_client_factory):
    def handler(request: httpx.Request) -> httpx.Response:
        p = request.url.path
        stub = _repo_metadata_nonfork_stub(request, p)
        if stub is not None:
            return stub
        if p == "/api/v5/repos/acme/proj" and request.method == "GET":
            return httpx.Response(200, json={"fork": False})
        if p == "/api/v5/repos/acme/proj/contents/.gitcode":
            return httpx.Response(
                200,
                json=[
                    {
                        "type": "file",
                        "path": ".gitcode/ISSUE_TEMPLATE/config.yaml",
                        "sha": "yamsha",
                    },
                    {
                        "type": "file",
                        "path": ".gitcode/ISSUE_TEMPLATE/unrelated.txt",
                        "sha": "x",
                    },
                ],
            )
        raise AssertionError(f"unexpected {request.method} {p}")

    client, _ = sync_client_factory(handler, owner="acme", repo="proj")
    items = client.issues.list_templates()
    paths = {i.path for i in items}
    assert paths == {".gitcode/ISSUE_TEMPLATE/config.yaml"}


def test_get_template_returns_str(sync_client_factory):
    path = ".gitcode/ISSUE_TEMPLATE_bug.md"

    def handler(request: httpx.Request) -> httpx.Response:
        p = request.url.path
        stub = _repo_metadata_nonfork_stub(request, p)
        if stub is not None:
            return stub
        if p == "/api/v5/repos/acme/proj" and request.method == "GET" and "contents" not in p and "raw" not in p:
            return httpx.Response(200, json={"fork": False})
        if p == f"/api/v5/repos/acme/proj/raw/{path}":
            return httpx.Response(404, json={"message": "missing"})
        if p == f"/api/v5/repos/acme/.gitcode/raw/{path}":
            return httpx.Response(200, content=b"# Title\n\nbody")
        raise AssertionError(f"unexpected {request.method} {p}")

    client, _ = sync_client_factory(handler, owner="acme", repo="proj")
    text = client.issues.get_template(path=path)
    assert text == "# Title\n\nbody"


def test_get_template_rejects_non_matching_path(sync_client_factory):
    def handler(request: httpx.Request) -> httpx.Response:
        p = request.url.path
        stub = _repo_metadata_nonfork_stub(request, p)
        if stub is not None:
            return stub
        if p == "/api/v5/repos/acme/proj" and "contents" not in p and "raw" not in p:
            return httpx.Response(200, json={"fork": False})
        raise AssertionError(f"unexpected {request.method} {p}")

    client, _ = sync_client_factory(handler, owner="acme", repo="proj")
    with pytest.raises(GitCodeHTTPStatusError) as exc:
        client.issues.get_template(path=".gitcode/README.md")
    assert exc.value.status_code == 404


def test_pulls_list_and_get_template(sync_client_factory):
    pr_path = ".gitcode/PULL_REQUEST_TEMPLATE.md"

    def handler(request: httpx.Request) -> httpx.Response:
        p = request.url.path
        stub = _repo_metadata_nonfork_stub(request, p)
        if stub is not None:
            return stub
        if p == "/api/v5/repos/o/r" and request.method == "GET" and "contents" not in p and "raw" not in p:
            return httpx.Response(200, json={"fork": False})
        if p == "/api/v5/repos/o/r/contents/.gitcode":
            return httpx.Response(
                200,
                json=[
                    {
                        "type": "file",
                        "name": "PULL_REQUEST_TEMPLATE.md",
                        "path": pr_path,
                        "sha": "xyz",
                    }
                ],
            )
        if p == f"/api/v5/repos/o/r/raw/{pr_path}":
            return httpx.Response(200, content=b"pr template")
        raise AssertionError(f"unexpected {request.method} {p}")

    client, _ = sync_client_factory(handler, owner="o", repo="r")
    listed = client.pulls.list_templates()
    assert len(listed) == 1
    assert listed[0].path == pr_path
    body = client.pulls.get_template(path=pr_path)
    assert body == "pr template"


@pytest.mark.asyncio
async def test_async_issues_list_templates(async_client_factory):
    def handler(request: httpx.Request) -> httpx.Response:
        p = request.url.path
        stub = _repo_metadata_nonfork_stub(request, p)
        if stub is not None:
            return stub
        if p == "/api/v5/repos/acme/proj" and request.method == "GET":
            return httpx.Response(200, json={"fork": False})
        if p == "/api/v5/repos/acme/proj/contents/.gitcode":
            return httpx.Response(200, json=[])
        if p == "/api/v5/repos/acme/.gitcode/contents/.gitcode":
            return httpx.Response(
                200,
                json=[
                    {
                        "type": "file",
                        "path": ".gitcode/ISSUE_TEMPLATE_x.md",
                        "sha": "asyncsha",
                    }
                ],
            )
        raise AssertionError(f"unexpected {request.method} {p}")

    client, http = async_client_factory(handler, owner="acme", repo="proj")
    async with client:
        items = await client.issues.list_templates()
    await http.aclose()
    assert len(items) == 1
    assert items[0].sha == "asyncsha"
