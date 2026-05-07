import importlib.util
from typing import Any, Dict

import httpx
import pytest

from gitcode_api.llm import (
    GitCodeOpenAITool,
    create_mcp_gitcode_api_tool,
    create_mcp_server,
    create_openjiuwen_gitcode_api_tool,
    register_mcp_gitcode_api_tool,
)
from gitcode_api.llm._tool import (
    MCP_SERVER_INSTRUCTIONS,
    OP_TYPE_ENUM,
    GitCodeLLMTool,
    help_resource_index_body,
    op_type_help_resource_body,
)


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


def test_create_mcp_server_default_instructions() -> None:
    server = create_mcp_server()
    assert server.instructions
    assert "gitcode_api_tool" in server.instructions
    assert "op_type" in server.instructions
    for name in OP_TYPE_ENUM:
        assert name in server.instructions
    assert server.instructions == MCP_SERVER_INSTRUCTIONS


def test_create_mcp_server_custom_instructions() -> None:
    server = create_mcp_server(instructions="Custom host copy.")
    assert server.instructions == "Custom host copy."


def test_op_type_help_resource_body_unknown() -> None:
    body = op_type_help_resource_body("not-a-real-op")
    assert "Unknown op_type" in body
    assert "not-a-real-op" in body


def test_op_type_help_resource_body_pulls() -> None:
    body = op_type_help_resource_body("pulls")
    assert "Resource: pulls" in body
    assert "list(" in body


def test_help_resource_index_body() -> None:
    body = help_resource_index_body()
    assert "gitcode-api://help/pulls" in body
    for name in OP_TYPE_ENUM:
        assert f"gitcode-api://help/{name}" in body


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


@pytest.mark.skipif(importlib.util.find_spec("openjiuwen") is not None, reason="openjiuwen is installed")
def test_create_openjiuwen_gitcode_api_tool_raises_when_openjiuwen_missing() -> None:
    with pytest.raises(ImportError, match="openjiuwen|openJiuwen"):
        create_openjiuwen_gitcode_api_tool(api_key="test-token")


@pytest.mark.skipif(importlib.util.find_spec("openjiuwen") is None, reason="openjiuwen not installed")
def test_create_openjiuwen_gitcode_api_tool_exposes_tool_card() -> None:
    jiuwen_tool = create_openjiuwen_gitcode_api_tool(api_key="test-token")
    assert jiuwen_tool.card.name == "gitcode_api_tool"
    assert "op_type" in jiuwen_tool.card.input_params.get("properties", {})


@pytest.mark.skipif(importlib.util.find_spec("openjiuwen") is None, reason="openjiuwen not installed")
def test_create_openjiuwen_gitcode_api_tool_custom_name_and_description() -> None:
    jiuwen_tool = create_openjiuwen_gitcode_api_tool(
        api_key="test-token",
        name="my_gitcode",
        description="Custom GitCode tool copy.",
    )
    assert jiuwen_tool.card.name == "my_gitcode"
    assert jiuwen_tool.card.description == "Custom GitCode tool copy."


@pytest.mark.skipif(importlib.util.find_spec("openjiuwen") is None, reason="openjiuwen not installed")
@pytest.mark.asyncio
async def test_create_openjiuwen_gitcode_api_tool_invoke(async_client_factory: Any) -> None:
    captured: Dict[str, Any] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        return httpx.Response(200, json={"full_name": "SushiNinja/GitCode-API"})

    client, http_client = async_client_factory(handler)
    try:
        jiuwen_tool = create_openjiuwen_gitcode_api_tool(async_client=client)
        result = await jiuwen_tool.invoke(
            {
                "op_type": "repos",
                "action": "get",
                "params": {"owner": "SushiNinja", "repo": "GitCode-API"},
            }
        )
    finally:
        await http_client.aclose()

    assert "/repos/SushiNinja/GitCode-API" in captured["url"]
    assert result == {"full_name": "SushiNinja/GitCode-API"}
