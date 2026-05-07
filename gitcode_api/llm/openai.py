"""OpenAI tool adapter for the GitCode SDK."""

import json
from functools import cached_property
from typing import Any, Coroutine, Dict, Optional, Union

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
        self.indent = kwargs.pop("indent", 2)
        self.async_mode = bool(async_mode)
        super().__init__(**kwargs)

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
        result = await super().__async_call__(*args, **kwargs)
        return json.dumps(result, ensure_ascii=False, indent=self.indent)

    def __call__(self, *args, **kwargs) -> Union[str, Coroutine[Any, Any, str]]:
        """Invoke the configured sync or async tool callable."""
        if self.async_mode:
            return self.__async_call__(*args, **kwargs)
        return json.dumps(super().__call__(*args, **kwargs), ensure_ascii=False, indent=self.indent)


__all__ = ["GitCodeOpenAITool"]
