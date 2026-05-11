import argparse
import sys
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Any, Dict

import httpx
import pytest

from gitcode_api.cli import _kebab_case, _probe_gitcode, _run_mcp_server, build_parser, main


def _mock_sync_client(monkeypatch: Any, handler: Any) -> None:
    mock_transport = httpx.MockTransport(handler)
    real_client = httpx.Client

    def client_with_mock_transport(*args: object, **kwargs: object) -> httpx.Client:
        merged = dict(kwargs)
        merged.setdefault("transport", mock_transport)
        return real_client(*args, **merged)

    monkeypatch.setattr(httpx, "Client", client_with_mock_transport)


def test_cli_no_args_prints_help_and_exits_zero(capsys: Any, monkeypatch: Any) -> None:
    monkeypatch.setattr(sys, "argv", ["gitcode-api"])
    assert main() == 0
    out = capsys.readouterr().out
    assert "usage:" in out.lower()
    assert "gitcode-api" in out
    assert "_____" in out
    assert "Examples:" not in out


def test_cli_empty_argv_prints_help(capsys: Any) -> None:
    assert main([]) == 0
    out = capsys.readouterr().out.lower()
    assert "usage:" in out
    assert "examples:" not in out


def test_cli_root_explicit_help_includes_epilog() -> None:
    buf = StringIO()
    with redirect_stdout(buf):
        with pytest.raises(SystemExit) as exc_info:
            build_parser().parse_args(["--help"])
    assert exc_info.value.code == 0
    assert "Examples:" in buf.getvalue()


def test_cli_method_subcommands_follow_resource_methods_order() -> None:
    """CLI lists methods in the same order as client.<resource>.methods."""
    parser = build_parser()
    client = _probe_gitcode()
    try:
        resources_action = next(
            action for action in parser._actions if getattr(action, "choices", None) and "pulls" in action.choices
        )
        pulls_parser = resources_action.choices["pulls"]
        methods_action = next(action for action in pulls_parser._actions if getattr(action, "choices", None))
        cli_kebab_order = list(methods_action.choices.keys())
        assert cli_kebab_order == [_kebab_case(name) for name in client.pulls.methods]
    finally:
        client.close()


def test_cli_method_help_description_has_summary_then_signature() -> None:
    client = _probe_gitcode()
    try:
        parser = build_parser()
        resources_action = next(
            action for action in parser._actions if getattr(action, "choices", None) and "pulls" in action.choices
        )
        pulls_parser = resources_action.choices["pulls"]
        methods_action = next(action for action in pulls_parser._actions if getattr(action, "choices", None))
        list_parser = methods_action.choices["list"]
        sig = client.pulls.method_signature("list")
        assert list_parser.description is not None
        assert list_parser.description.startswith("List pull requests for a repository.")
        assert list_parser.description.endswith(sig)
    finally:
        client.close()


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


def test_cli_build_parser_exposes_serve_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "serve",
            "--api-key",
            "test-token",
            "--transport",
            "http",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ]
    )

    assert args.command == "serve"
    assert args.api_key == "test-token"
    assert args.transport == "http"
    assert args.host == "127.0.0.1"
    assert args.port == 8000


def test_cli_serve_routes_to_mcp_runner(monkeypatch: Any) -> None:
    captured: Dict[str, Any] = {}

    def fake_run(args: Any) -> int:
        captured["transport"] = args.transport
        return 0

    monkeypatch.setattr("gitcode_api.cli._run_mcp_server", fake_run)

    assert main(["serve", "--transport", "stdio"]) == 0
    assert captured["transport"] == "stdio"


def test_run_mcp_server_passes_fastmcp_options(monkeypatch: Any) -> None:
    captured: Dict[str, Any] = {}

    class DummyServer:
        def run(self, **kwargs) -> None:
            captured["run_kwargs"] = kwargs

    def fake_create_mcp_server(**kwargs) -> DummyServer:
        captured["server_kwargs"] = kwargs
        return DummyServer()

    monkeypatch.setattr("gitcode_api.llm.create_mcp_server", fake_create_mcp_server)
    args = argparse.Namespace(
        name="GitCode API",
        api_key="test-token",
        owner="SushiNinja",
        repo="GitCode-API",
        base_url="https://api.gitcode.com/api/v5",
        timeout=60.0,
        transport="http",
        host="127.0.0.1",
        port=8000,
        path="/mcp",
        show_banner=None,
    )

    assert _run_mcp_server(args) == 0
    assert captured["server_kwargs"]["name"] == "GitCode API"
    assert captured["server_kwargs"]["tool"]._client_kwargs["api_key"] == "test-token"
    assert captured["run_kwargs"] == {
        "show_banner": None,
        "transport": "http",
        "host": "127.0.0.1",
        "port": 8000,
        "path": "/mcp",
    }


def test_cli_invokes_resource_methods_and_prints_json(capsys: Any, monkeypatch: Any) -> None:
    captured: Dict[str, Any] = {}

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
    captured: Dict[str, Any] = {}

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
