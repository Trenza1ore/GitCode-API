"""FastMCP integration for the GitCode LLM tool."""

from typing import TYPE_CHECKING, Any, Callable, Optional, Union, cast

from ._tool import (
    MCP_SERVER_INSTRUCTIONS,
    TOOL_DESCRIPTION,
    TOOL_NAME,
    GitCodeLLMTool,
    help_resource_index_body,
    op_type_help_resource_body,
)

if TYPE_CHECKING:
    from fastmcp import FastMCP
    from fastmcp.tools import Tool


def _missing_fastmcp_error() -> ImportError:
    return ImportError(
        "FastMCP support requires the optional dependency: pip install 'gitcode-api[mcp]' "
        "Note: Python 3.10+ is required for FastMCP."
    )


def _load_fastmcp() -> tuple["type[FastMCP]", Callable[..., "Tool"]]:
    try:
        from fastmcp import FastMCP  # pylint: disable=import-outside-toplevel
        from fastmcp.tools import tool as fastmcp_tool  # pylint: disable=import-outside-toplevel
    except ImportError as exc:
        raise _missing_fastmcp_error() from exc
    return FastMCP, fastmcp_tool  # type: ignore[return-value]


def create_mcp_gitcode_api_tool(tool: Optional[GitCodeLLMTool] = None) -> Callable:
    """Return the async callable that can be registered with an MCP server.

    :param tool: Optional preconfigured shared GitCode LLM tool.
    :returns: Async callable using the standard GitCode tool parameters.
    """
    wrapped = tool or GitCodeLLMTool()

    async def gitcode_api_tool(
        op_type: str, action: str = "", params: Optional[dict[str, Any]] = None, help: bool = False
    ) -> Any:
        """Call GitCode client resources using op_type, action, and params."""
        return await wrapped.__async_call__(op_type=op_type, action=action, params=params, help=help)

    gitcode_api_tool.__name__ = TOOL_NAME
    gitcode_api_tool.__doc__ = TOOL_DESCRIPTION
    return gitcode_api_tool


def register_mcp_gitcode_api_tool(mcp: Union["FastMCP", Any], tool: Optional[GitCodeLLMTool] = None) -> "Tool":
    """Register the GitCode API tool with an existing FastMCP-compatible server.

    :param mcp: FastMCP server instance.
    :param tool: Optional preconfigured shared GitCode LLM tool.
    :returns: The registered tool callable.
    """
    callable_tool = create_mcp_gitcode_api_tool(tool)
    if hasattr(mcp, "tool"):
        try:
            return cast("Tool", mcp.tool(name=TOOL_NAME, description=TOOL_DESCRIPTION)(callable_tool))
        except TypeError:
            return cast("Tool", mcp.tool()(callable_tool))
    if hasattr(mcp, "add_tool"):
        _, fastmcp_tool = _load_fastmcp()
        mcp_tool = fastmcp_tool(callable_tool, name=TOOL_NAME, description=TOOL_DESCRIPTION)
        return mcp.add_tool(mcp_tool)
    raise TypeError("mcp must provide a tool decorator or add_tool method")


def register_mcp_help_resources(mcp: Union["FastMCP", Any]) -> None:
    """Register optional MCP resources that mirror ``gitcode_api_tool`` help text.

    Registers:

    * ``gitcode-api://help`` — markdown index of per-``op_type`` URIs.
    * ``gitcode-api://help/{op_type}`` — plain-text method list for one resource.

    No-op when ``mcp`` does not expose FastMCP's ``resource`` decorator.

    :param mcp: FastMCP server instance (or compatible object).
    """
    if not hasattr(mcp, "resource"):
        return

    @mcp.resource(
        "gitcode-api://help/{op_type}",
        name="gitcode_api_op_type_help",
        description=("Method list for one op_type (same as gitcode_api_tool with help=true and empty action)."),
        mime_type="text/plain",
    )
    async def _op_type_help_resource(op_type: str) -> str:
        return op_type_help_resource_body(op_type)

    @mcp.resource(
        "gitcode-api://help",
        name="gitcode_api_help_index",
        description="Markdown index of gitcode-api://help/{op_type} help resources.",
        mime_type="text/markdown",
    )
    async def _help_index_resource() -> str:
        return help_resource_index_body()

    _ = (_op_type_help_resource, _help_index_resource)


class GitCodeMCP:
    """Small FastMCP server wrapper exposing the GitCode API tool.

    :param name: MCP server name.
    :param tool: Optional preconfigured shared GitCode LLM tool.
    :param kwargs: Forwarded to ``fastmcp.FastMCP``. If ``instructions`` is omitted, a default overview
        of the tool (parameters, byte encoding, and valid ``op_type`` values) is supplied.
    """

    def __init__(self, name: str = "GitCode API", tool: Optional[GitCodeLLMTool] = None, **kwargs: Any) -> None:
        """Create a FastMCP server and register the GitCode API tool."""
        fastmcp, *_ = _load_fastmcp()
        if "instructions" not in kwargs:
            kwargs["instructions"] = MCP_SERVER_INSTRUCTIONS
        self.mcp = fastmcp(name, **kwargs)
        self.gitcode_api_tool = register_mcp_gitcode_api_tool(self.mcp, tool)
        register_mcp_help_resources(self.mcp)

    def __getattr__(self, name: str) -> Any:
        """Delegate unknown attributes to the wrapped FastMCP server."""
        return getattr(self.mcp, name)


def create_mcp_server(name: str = "GitCode API", tool: Optional[GitCodeLLMTool] = None, **kwargs: Any) -> "FastMCP":
    """Create a FastMCP server with the GitCode API tool already registered.

    :param name: MCP server display name.
    :param tool: Optional preconfigured :class:`~gitcode_api.llm._tool.GitCodeLLMTool`.
    :param kwargs: Forwarded to :class:`GitCodeMCP` and then to ``fastmcp.FastMCP`` (for example
        ``instructions`` to override the default server instructions).
    :returns: Configured ``FastMCP`` instance with ``gitcode_api_tool`` registered.
    """
    return GitCodeMCP(name=name, tool=tool, **kwargs).mcp


__all__ = [
    "GitCodeMCP",
    "create_mcp_gitcode_api_tool",
    "create_mcp_server",
    "register_mcp_gitcode_api_tool",
    "register_mcp_help_resources",
]
