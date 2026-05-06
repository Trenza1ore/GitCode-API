"""LLM tool adapters for the GitCode SDK."""

from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .mcp import GitCodeMCP, create_mcp_gitcode_api_tool, create_mcp_server, register_mcp_gitcode_api_tool
    from .openai import GitCodeOpenAITool


_IMPORT_MAP = {
    "GitCodeMCP": ".mcp",
    "create_mcp_gitcode_api_tool": ".mcp",
    "create_mcp_server": ".mcp",
    "register_mcp_gitcode_api_tool": ".mcp",
    "GitCodeOpenAITool": ".openai",
}

_IMPORT_CACHE = {}


def __getattr__(name: str) -> object:
    """Lazily import LLM adapter class / helper functions."""
    value = _IMPORT_CACHE.get(name)
    if value is not None:
        return value
    try:
        module_name = _IMPORT_MAP[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name, __name__)
    for attr in module.__all__:
        _IMPORT_CACHE[attr] = getattr(module, attr)
    return _IMPORT_CACHE[name]


def __dir__() -> list[str]:
    """Return module attributes."""
    return __all__


__all__ = [
    "GitCodeOpenAITool",
    "GitCodeMCP",
    "create_mcp_gitcode_api_tool",
    "create_mcp_server",
    "register_mcp_gitcode_api_tool",
]
