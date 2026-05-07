"""openJiuwen ``LocalFunction`` adapter for the GitCode LLM tool."""

from importlib import import_module
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional

from gitcode_api import AsyncGitCode, GitCode
from gitcode_api._base_client import DEFAULT_BASE_URL

from ._tool import TOOL_DESCRIPTION, TOOL_NAME, TOOL_PARAMETERS, GitCodeLLMTool

if TYPE_CHECKING:
    from openjiuwen.core.foundation.tool import LocalFunction


def _missing_openjiuwen_error() -> ImportError:
    return ImportError(
        "The openJiuwen tool support requires the optional dependency: pip install openjiuwen. "
        "Note: Python 3.11+ is required for openjiuwen."
    )


def _openjiuwen_tool_decorator() -> Callable[..., Any]:
    try:
        mod = import_module("openjiuwen.core.foundation.tool")
    except ImportError as exc:
        raise _missing_openjiuwen_error() from exc
    return getattr(mod, "tool")  # type: ignore[no-any-return]


class _GitCodeJiuwenTool(GitCodeLLMTool):
    """Build an openJiuwen ``LocalFunction`` bound to :class:`GitCodeLLMTool` (async invoke only)."""

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        client: Optional[GitCode] = None,
        async_client: Optional[AsyncGitCode] = None,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: Optional[float] = None,
        decrypt: Optional[Callable[..., Any]] = None,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> None:
        super().__init__(
            client=client,
            async_client=async_client,
            api_key=api_key,
            owner=owner,
            repo=repo,
            base_url=base_url,
            timeout=timeout,
            decrypt=decrypt,
        )
        tool_name = name if name is not None else TOOL_NAME
        tool_description = description if description is not None else TOOL_DESCRIPTION
        oj_tool = _openjiuwen_tool_decorator()

        async def _async_impl(
            op_type: str,
            action: str = "",
            params: Optional[Dict[str, Any]] = None,
            help: bool = False,
        ) -> Any:
            return await self.__async_call__(op_type=op_type, action=action, params=params, help=help)

        self.local_function = oj_tool(
            _async_impl,
            name=tool_name,
            description=tool_description,
            input_params=TOOL_PARAMETERS,
            auto_extract=False,
        )


def create_openjiuwen_gitcode_api_tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    *,
    client: Optional[GitCode] = None,
    async_client: Optional[AsyncGitCode] = None,
    api_key: Optional[str] = None,
    base_url: str = DEFAULT_BASE_URL,
    timeout: Optional[float] = None,
    decrypt: Optional[Callable[..., Any]] = None,
    owner: Optional[str] = None,
    repo: Optional[str] = None,
) -> "LocalFunction":
    """Create an openJiuwen ``LocalFunction`` for the GitCode API tool.

    :param name: Tool name on the ``LocalFunction`` card; defaults to ``gitcode_api_tool``.
    :param description: Tool description on the card; defaults to the shared GitCode tool description.
    :param client: Optional synchronous GitCode client.
    :param async_client: Optional asynchronous GitCode client.
    :param api_key: Personal access token when clients are not supplied.
    :param base_url: Base URL for generated clients.
    :param timeout: Request timeout for generated clients.
    :param decrypt: Optional decryption function for encrypted access tokens.
    :param owner: Default repository owner for generated clients.
    :param repo: Default repository name for generated clients.
    :returns: openJiuwen ``LocalFunction`` with the standard parameter schema.
    """
    adapter = _GitCodeJiuwenTool(
        client=client,
        async_client=async_client,
        api_key=api_key,
        owner=owner,
        repo=repo,
        base_url=base_url,
        timeout=timeout,
        decrypt=decrypt,
        name=name,
        description=description,
    )
    return adapter.local_function


__all__ = ["create_openjiuwen_gitcode_api_tool"]
