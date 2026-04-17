from pathlib import Path
from typing import Any

import httpx

from gitcode_api.cli import build_parser, main


def _mock_sync_client(monkeypatch: Any, handler: Any) -> None:
    mock_transport = httpx.MockTransport(handler)
    real_client = httpx.Client

    def client_with_mock_transport(*args: object, **kwargs: object) -> httpx.Client:
        merged = dict(kwargs)
        merged.setdefault("transport", mock_transport)
        return real_client(*args, **merged)

    monkeypatch.setattr(httpx, "Client", client_with_mock_transport)


def test_cli_build_parser_exposes_generated_commands() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "oauth",
            "build-authorize-url",
            "--api-key",
            "test-token",
            "--client-id",
            "cid",
            "--redirect-uri",
            "https://example.com/callback",
        ]
    )

    assert args.resource_name == "oauth"
    assert args.method_name == "build_authorize_url"


def test_cli_invokes_resource_methods_and_prints_json(capsys: Any, monkeypatch: Any) -> None:
    captured: dict[str, Any] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        return httpx.Response(200, json={"full_name": "SushiNinja/GitCode-API"})

    _mock_sync_client(monkeypatch, handler)

    exit_code = main(
        [
            "repos",
            "get",
            "--api-key",
            "test-token",
            "--owner",
            "SushiNinja",
            "--repo",
            "GitCode-API",
        ]
    )

    stdout = capsys.readouterr().out
    assert exit_code == 0
    assert "/repos/SushiNinja/GitCode-API" in captured["url"]
    assert '"full_name": "SushiNinja/GitCode-API"' in stdout


def test_cli_supports_extra_kwargs_via_set_flags(capsys: Any, monkeypatch: Any) -> None:
    captured: dict[str, Any] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json={"open": 3, "closed": 1})

    _mock_sync_client(monkeypatch, handler)

    exit_code = main(
        [
            "pulls",
            "list",
            "--api-key",
            "test-token",
            "--owner",
            "SushiNinja",
            "--repo",
            "GitCode-API",
            "--set",
            "only_count=true",
            "--set",
            "reviewer=octocat",
        ]
    )

    stdout = capsys.readouterr().out
    assert exit_code == 0
    assert captured["params"]["only_count"] == "true"
    assert captured["params"]["reviewer"] == "octocat"
    assert '"open": 3' in stdout


def test_cli_writes_raw_bytes_to_output_file(tmp_path: Path, monkeypatch: Any) -> None:
    output_path = tmp_path / "README.txt"

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"hello from gitcode")

    _mock_sync_client(monkeypatch, handler)

    exit_code = main(
        [
            "contents",
            "get-raw",
            "--api-key",
            "test-token",
            "--owner",
            "SushiNinja",
            "--repo",
            "GitCode-API",
            "--path",
            "README.md",
            "--output-file",
            str(output_path),
        ]
    )

    assert exit_code == 0
    assert output_path.read_bytes() == b"hello from gitcode"
