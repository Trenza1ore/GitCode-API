import json
from typing import Optional

import httpx
import pytest

from gitcode_api._models import ReleaseAsset, ReleaseUploadURL

RELEASE_PAYLOAD = {
    "tag_name": "v1.0.0",
    "target_commitish": "main",
    "prerelease": False,
    "name": "v1.0.0",
    "body": "Release notes",
    "author": {"id": "1", "login": "octo", "name": "Octo", "avatar_url": "https://example.com/a.png"},
    "created_at": "2026-05-12T10:00:00+08:00",
    "assets": [
        {"browser_download_url": "https://example.com/checksums.txt", "name": "checksums.txt", "type": "text/plain"}
    ],
    "release_status": "latest",
}


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
        assert seen_url == "https://api.gitcode.com/api/v8/enterprises/SushiNinja/labels?search=bug"
    finally:
        client.close()
        http_client.close()


@pytest.mark.asyncio
async def test_async_webhooks_test_hits_expected_endpoint(async_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/v5/repos/SushiNinja/GitCode-API/hooks/44/tests"
        return httpx.Response(204)

    client, http_client = async_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        result = await client.webhooks.test(hook_id=44)
        assert result is None
    finally:
        await client.close()
        await http_client.aclose()


def test_releases_create_posts_documented_payload_and_models_assets(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/v5/repos/SushiNinja/GitCode-API/releases"
        assert json.loads(request.content) == {
            "tag_name": "v1.0.0",
            "name": "v1.0.0",
            "body": "Release notes",
            "target_commitish": "main",
            "release_status": "latest",
        }
        return httpx.Response(200, json=RELEASE_PAYLOAD, request=request)

    client, http_client = sync_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        release = client.releases.create(
            tag="v1.0.0",
            name="v1.0.0",
            body="Release notes",
            target_commitish="main",
            release_status="latest",
        )
    finally:
        client.close()
        http_client.close()

    assert release.target_commitish == "main"
    assert release.prerelease is False
    assert release.release_status == "latest"
    assert release.assets is not None
    assert isinstance(release.assets[0], ReleaseAsset)
    assert release.assets[0].browser_download_url == "https://example.com/checksums.txt"


def test_releases_update_uses_tag_path_and_documented_payload(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "PATCH"
        assert request.url.path == "/api/v5/repos/SushiNinja/GitCode-API/releases/v1.0.0"
        assert json.loads(request.content) == {
            "name": "v1.0.0",
            "body": "Updated notes",
            "release_status": "pre",
        }
        return httpx.Response(200, json={**RELEASE_PAYLOAD, "body": "Updated notes", "release_status": "pre"})

    client, http_client = sync_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        release = client.releases.update(tag="v1.0.0", name="v1.0.0", body="Updated notes", release_status="pre")
    finally:
        client.close()
        http_client.close()

    assert release.body == "Updated notes"
    assert release.release_status == "pre"


def test_releases_list_sends_documented_query_params(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/v5/repos/SushiNinja/GitCode-API/releases"
        assert request.url.params["direction"] == "desc"
        assert request.url.params["page"] == "2"
        assert request.url.params["per_page"] == "50"
        return httpx.Response(200, json=[RELEASE_PAYLOAD], request=request)

    client, http_client = sync_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        releases = client.releases.list(direction="desc", page=2, per_page=50)
    finally:
        client.close()
        http_client.close()

    assert releases[0].tag_name == "v1.0.0"


def test_releases_get_upload_url_returns_model(sync_client_factory) -> None:
    payload = {
        "url": "https://obs.example.com/upload",
        "headers": {"x-obs-acl": "public-read", "Content-Type": "application/pdf"},
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/v5/repos/SushiNinja/GitCode-API/releases/v1.0.0/upload_url"
        assert request.url.params["file_name"] == "notes.pdf"
        return httpx.Response(200, json=payload, request=request)

    client, http_client = sync_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        upload_url = client.releases.get_upload_url(tag="v1.0.0", file_name="notes.pdf")
    finally:
        client.close()
        http_client.close()

    assert isinstance(upload_url, ReleaseUploadURL)
    assert upload_url.url == "https://obs.example.com/upload"
    assert upload_url.headers == payload["headers"]


def test_releases_upload_puts_file_content_to_presigned_url(sync_client_factory, tmp_path) -> None:
    upload_path = tmp_path / "notes.pdf"
    upload_path.write_bytes(b"pdf-bytes")
    seen_upload = False

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal seen_upload
        if request.method == "GET":
            assert request.url.path == "/api/v5/repos/SushiNinja/GitCode-API/releases/v1.0.0/upload_url"
            assert request.url.params["file_name"] == "notes.pdf"
            upload_path.write_bytes(b"mutated-after-upload-url-request")
            return httpx.Response(
                200,
                json={
                    "url": "https://obs.example.com/upload",
                    "headers": {"x-obs-acl": "public-read", "Content-Type": "application/pdf"},
                },
                request=request,
            )

        assert request.method == "PUT"
        assert str(request.url) == "https://obs.example.com/upload"
        assert "authorization" not in request.headers
        assert request.headers["x-obs-acl"] == "public-read"
        assert request.headers["content-type"] == "application/pdf"
        assert request.content == b"pdf-bytes"
        seen_upload = True
        return httpx.Response(200, request=request)

    client, http_client = sync_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        result = client.releases.upload(tag="v1.0.0", file_name="notes.pdf", content=str(upload_path))
    finally:
        client.close()
        http_client.close()

    assert result is None
    assert seen_upload is True


def test_releases_upload_rejects_non_bytes_content_before_request(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError(f"Unexpected request: {request.method} {request.url}")

    client, http_client = sync_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        with pytest.raises(TypeError, match="content must be bytes or a file path string"):
            client.releases.upload(tag="v1.0.0", file_name="notes.pdf", content=object())  # type: ignore[arg-type]
    finally:
        client.close()
        http_client.close()


def test_releases_download_attachment_returns_raw_bytes(sync_client_factory) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == (
            "/api/v5/repos/SushiNinja/GitCode-API/releases/v1.0.0/attach_files/checksums.txt/download"
        )
        return httpx.Response(200, content=b"checksum-bytes", request=request)

    client, http_client = sync_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        content = client.releases.download_attachment(tag="v1.0.0", file_name="checksums.txt")
    finally:
        client.close()
        http_client.close()

    assert content == b"checksum-bytes"


@pytest.mark.asyncio
async def test_async_releases_get_upload_and_download_attachment(async_client_factory, tmp_path) -> None:
    upload_path = tmp_path / "async-notes.pdf"
    upload_path.write_bytes(b"async-pdf-bytes")
    seen_upload = False

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal seen_upload
        if request.url.path.endswith("/download"):
            assert request.method == "GET"
            assert request.url.path == (
                "/api/v5/repos/SushiNinja/GitCode-API/releases/v1.0.0/attach_files/checksums.txt/download"
            )
            return httpx.Response(200, content=b"async-checksum-bytes", request=request)

        if request.method == "PUT":
            assert str(request.url) == "https://obs.example.com/async-upload"
            assert "authorization" not in request.headers
            assert request.headers["x-obs-acl"] == "public-read"
            assert request.content == b"async-pdf-bytes"
            seen_upload = True
            return httpx.Response(204, request=request)

        if request.url.path.endswith("/upload_url"):
            assert request.method == "GET"
            upload_path.write_bytes(b"mutated-async-pdf-bytes")
            return httpx.Response(
                200,
                json={
                    "url": "https://obs.example.com/async-upload",
                    "headers": {"x-obs-acl": "public-read", "Content-Type": "application/pdf"},
                },
                request=request,
            )

        assert request.method == "GET"
        assert request.url.path == "/api/v5/repos/SushiNinja/GitCode-API/releases/v1.0.0"
        assert request.url.params["temp_download_url"] == "true"
        return httpx.Response(200, json=RELEASE_PAYLOAD, request=request)

    client, http_client = async_client_factory(handler, owner="SushiNinja", repo="GitCode-API")
    try:
        release = await client.releases.get(tag="v1.0.0", temp_download_url="true")
        result = await client.releases.upload(tag="v1.0.0", file_name="notes.pdf", content=str(upload_path))
        content = await client.releases.download_attachment(tag="v1.0.0", file_name="checksums.txt")
    finally:
        await client.close()
        await http_client.aclose()

    assert release.tag_name == "v1.0.0"
    assert result is None
    assert seen_upload is True
    assert content == b"async-checksum-bytes"
