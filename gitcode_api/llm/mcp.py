"""FastMCP integration for the GitCode SDK LLM tool."""

from typing import TYPE_CHECKING, Any, Callable, Optional, Union

from ._tool import TOOL_DESCRIPTION, TOOL_NAME, GitCodeLLMTool

if TYPE_CHECKING:
    from fastmcp import FastMCP
    from fastmcp.tools import Tool


def _missing_fastmcp_error() -> ImportError:
    return ImportError("FastMCP support requires the optional dependency: pip install 'gitcode-api[mcp]'")


def _load_fastmcp() -> tuple["type[FastMCP]", Callable[..., "Tool"]]:
    try:
        from fastmcp import FastMCP
        from fastmcp.tools import tool as fastmcp_tool
    except ImportError as exc:
        raise _missing_fastmcp_error() from exc
    return FastMCP, fastmcp_tool  # type: ignore[return-value]


def create_mcp_gitcode_api_tool(tool: Optional[GitCodeLLMTool] = None) -> Any:
    """Return the async callable that can be registered with an MCP server.

    :param tool: Optional preconfigured shared GitCode LLM tool.
    :returns: Async callable using the standard GitCode tool parameters.
    """
    wrapped = tool or GitCodeLLMTool()

    async def gitcode_api_tool(
        op_type: str, action: str = "", params: Optional[dict[str, Any]] = None, help: bool = False
    ) -> Any:
        """Call GitCode SDK resources using op_type, action, and params."""
        return await wrapped.__async_call__(op_type=op_type, action=action, params=params, help=help)

    gitcode_api_tool.__name__ = TOOL_NAME
    gitcode_api_tool.__doc__ = TOOL_DESCRIPTION
    return gitcode_api_tool


def register_mcp_gitcode_api_tool(mcp: Union["FastMCP", Any], tool: Optional[GitCodeLLMTool] = None) -> Any:
    """Register the GitCode API tool with an existing FastMCP-compatible server.

    :param mcp: FastMCP server instance.
    :param tool: Optional preconfigured shared GitCode LLM tool.
    :returns: The registered tool callable.
    """
    callable_tool = create_mcp_gitcode_api_tool(tool)
    if hasattr(mcp, "tool"):
        try:
            return mcp.tool(name=TOOL_NAME, description=TOOL_DESCRIPTION)(callable_tool)
        except TypeError:
            return mcp.tool()(callable_tool)
    if hasattr(mcp, "add_tool"):
        _, fastmcp_tool = _load_fastmcp()
        mcp_tool = fastmcp_tool(callable_tool, name=TOOL_NAME, description=TOOL_DESCRIPTION)
        return mcp.add_tool(mcp_tool)
    raise TypeError("mcp must provide a tool decorator or add_tool method")


class GitCodeMCP:
    """Small FastMCP server wrapper exposing the GitCode API tool.

    :param name: MCP server name.
    :param tool: Optional preconfigured shared GitCode LLM tool.
    :param kwargs: Forwarded to ``fastmcp.FastMCP``.
    """

    def __init__(self, name: str = "GitCode API", tool: Optional[GitCodeLLMTool] = None, **kwargs) -> None:
        """Create a FastMCP server and register the GitCode API tool."""
        fastmcp, *_ = _load_fastmcp()
        self.mcp = fastmcp(name, **kwargs)
        self.gitcode_api_tool = register_mcp_gitcode_api_tool(self.mcp, tool)

    def __getattr__(self, name: str) -> Any:
        """Delegate unknown attributes to the wrapped FastMCP server."""
        return getattr(self.mcp, name)


def create_mcp_server(name: str = "GitCode API", tool: Optional[GitCodeLLMTool] = None, **kwargs) -> "FastMCP":
    """Create a FastMCP server with the GitCode API tool already registered."""
    return GitCodeMCP(name=name, tool=tool, **kwargs).mcp


__all__ = [
    "GitCodeMCP",
    "create_mcp_gitcode_api_tool",
    "create_mcp_server",
    "register_mcp_gitcode_api_tool",
]
