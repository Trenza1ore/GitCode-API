"""OpenAI tool adapter for the GitCode SDK."""

import json
from functools import cached_property
from typing import Any, Callable, Coroutine, Dict, Optional, Union

from gitcode_api import AsyncGitCode, GitCode
from gitcode_api._base_client import DEFAULT_BASE_URL

from ._tool import TOOL_DESCRIPTION, TOOL_NAME, TOOL_PARAMETERS, GitCodeLLMTool


class GitCodeOpenAITool(GitCodeLLMTool):
    """OpenAI-compatible callable tool for invoking GitCode SDK resources.

    :param async_mode: When true, calling the instance returns the async tool coroutine.
    :param indent: ``indent`` argument passed to :func:`json.dumps` when serializing
        invocation results (default ``2``).
    :param client: Optional synchronous GitCode client.
    :param async_client: Optional asynchronous GitCode client.
    :param api_key: Personal access token used when clients are not supplied.
    :param base_url: Base URL for generated clients.
    :param timeout: Request timeout for generated clients.
    :param decrypt: Optional decryption function for encrypted access tokens.
    :param owner: Default repository owner for generated clients.
    :param repo: Default repository name for generated clients.
    """

    name = TOOL_NAME
    description = TOOL_DESCRIPTION
    parameters = TOOL_PARAMETERS

    def __init__(
        self,
        async_mode: bool = False,
        indent: int = 2,
        *,
        client: Optional[GitCode] = None,
        async_client: Optional[AsyncGitCode] = None,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: Optional[float] = None,
        decrypt: Optional[Callable] = None,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> None:
        """Create an OpenAI tool wrapper."""
        self.indent = indent
        self.async_mode = bool(async_mode)
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

    @cached_property
    def tool(self) -> Dict[str, Any]:
        """Return this tool in OpenAI Chat Completions tool format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def to_dict(self) -> Dict[str, Any]:
        """Return this tool in OpenAI Chat Completions tool format."""
        return self.tool

    async def __async_call__(self, *args, **kwargs) -> str:
        """Invoke the configured async tool callable."""
        result = await super().__async_call__(*args, **kwargs)
        return json.dumps(result, ensure_ascii=False, indent=self.indent)

    def __call__(self, *args, **kwargs) -> Union[str, Coroutine[Any, Any, str]]:
        """Invoke the configured sync or async tool callable."""
        if self.async_mode:
            return self.__async_call__(*args, **kwargs)
        return json.dumps(super().__call__(*args, **kwargs), ensure_ascii=False, indent=self.indent)


__all__ = ["GitCodeOpenAITool"]
