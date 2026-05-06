"""OpenAI tool adapter for the GitCode SDK."""

from functools import cached_property
from typing import Any, Dict, Optional

from ._tool import TOOL_DESCRIPTION, TOOL_NAME, TOOL_PARAMETERS, GitCodeLLMTool


class GitCodeOpenAITool(GitCodeLLMTool):
    """OpenAI-compatible callable tool for invoking GitCode SDK resources.

    :param async_mode: When true, calling the instance returns the async tool coroutine.
    :param kwargs: Forwarded to :class:`gitcode_api.llm.GitCodeLLMTool`. ``{"async": True}``
        is also accepted for frameworks that construct tools from dictionaries.
    """

    name = TOOL_NAME
    description = TOOL_DESCRIPTION
    parameters = TOOL_PARAMETERS

    def __init__(self, async_mode: Optional[bool] = None, **kwargs) -> None:
        """Create an OpenAI tool wrapper."""
        async_kw = kwargs.pop("async", None)
        if async_mode is None:
            async_mode = bool(async_kw)
        elif async_kw is not None:
            raise TypeError("Pass only one of async_mode or async")
        self.async_mode = bool(async_mode)
        super().__init__(**kwargs)
        if self.async_mode:
            self.__call__ = self.__async_call__  # type: ignore[method-assign]

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

    def __call__(self, *args: Any, **kwargs) -> Any:
        """Invoke the configured sync or async tool callable."""
        if self.async_mode:
            return self.__async_call__(*args, **kwargs)
        return super().__call__(*args, **kwargs)


__all__ = ["GitCodeOpenAITool"]
