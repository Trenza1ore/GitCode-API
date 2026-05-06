from typing import Any, Dict

import httpx
import pytest

from gitcode_api.llm import (
    GitCodeOpenAITool,
    create_mcp_gitcode_api_tool,
    register_mcp_gitcode_api_tool,
)
from gitcode_api.llm._tool import GitCodeLLMTool


def test_openai_tool_exposes_function_schema() -> None:
    tool = GitCodeOpenAITool(api_key="test-token")

    assert tool.tool["type"] == "function"
    assert tool.tool["function"]["name"] == "gitcode_api_tool"
    assert "op_type" in tool.tool["function"]["parameters"]["properties"]
    assert "repos" in tool.tool["function"]["parameters"]["properties"]["op_type"]["enum"]


def test_openai_tool_invokes_sync_client(sync_client_factory: Any) -> None:
    captured: Dict[str, Any] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        return httpx.Response(200, json={"full_name": "SushiNinja/GitCode-API"})

    client, http_client = sync_client_factory(handler)
    try:
        tool = GitCodeOpenAITool(client=client)
        result = tool("repos", "get", params={"owner": "SushiNinja", "repo": "GitCode-API"})
    finally:
        http_client.close()

    assert "/repos/SushiNinja/GitCode-API" in captured["url"]
    assert result == {"full_name": "SushiNinja/GitCode-API"}


@pytest.mark.asyncio
async def test_openai_tool_invokes_async_client(async_client_factory: Any) -> None:
    captured: Dict[str, Any] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        return httpx.Response(200, json={"login": "octocat"})

    client, http_client = async_client_factory(handler)
    try:
        tool = GitCodeOpenAITool(async_client=client, async_mode=True)
        result = await tool("users", "get", params={"username": "octocat"})
    finally:
        await http_client.aclose()

    assert "/users/octocat" in captured["url"]
    assert result == {"login": "octocat"}


def test_tool_help_does_not_require_api_key(monkeypatch: Any) -> None:
    monkeypatch.delenv("GITCODE_ACCESS_TOKEN", raising=False)

    result = GitCodeLLMTool()("pulls", help=True)

    assert "Available methods:" in result
    assert "Resource: pulls" in result


@pytest.mark.asyncio
async def test_mcp_tool_callable_uses_shared_tool(async_client_factory: Any) -> None:
    captured: Dict[str, Any] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        return httpx.Response(200, json={"full_name": "SushiNinja/GitCode-API"})

    client, http_client = async_client_factory(handler)
    try:
        callable_tool = create_mcp_gitcode_api_tool(GitCodeLLMTool(async_client=client))
        result = await callable_tool("repos", "get", params={"owner": "SushiNinja", "repo": "GitCode-API"})
    finally:
        await http_client.aclose()

    assert callable_tool.__name__ == "gitcode_api_tool"
    assert "/repos/SushiNinja/GitCode-API" in captured["url"]
    assert result == {"full_name": "SushiNinja/GitCode-API"}


def test_mcp_registers_with_existing_server() -> None:
    class DummyMCP:
        def __init__(self) -> None:
            self.registered = None

        def tool(self, **metadata: Any) -> Any:
            def decorator(fn: Any) -> Any:
                self.registered = (metadata, fn)
                return fn

            return decorator

    server = DummyMCP()
    registered = register_mcp_gitcode_api_tool(server, GitCodeLLMTool(api_key="test-token"))

    assert registered.__name__ == "gitcode_api_tool"
    assert server.registered[0]["name"] == "gitcode_api_tool"
