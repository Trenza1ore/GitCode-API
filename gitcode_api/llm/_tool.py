"""Shared GitCode API tool logic for LLM integrations."""

import base64
import inspect
import logging
from collections.abc import Mapping
from functools import lru_cache
import os
from typing import Any, Callable, Dict, Optional, Tuple

from gitcode_api import (
    AsyncGitCode,
    GitCode,
    GitCodeConfigurationError,
    GitCodeError,
    GitCodeHTTPStatusError,
)
from gitcode_api._base_client import DEFAULT_BASE_URL, DEFAULT_TOKEN_ENV
from gitcode_api.resources._shared import AsyncResource, SyncResource

logger = logging.getLogger(__name__)

OP_TYPES = frozenset(
    name
    for name, annotation in GitCode.__annotations__.items()
    if inspect.isclass(annotation) and issubclass(annotation, SyncResource)
)
OP_TYPE_ENUM = sorted(OP_TYPES)

MCP_SERVER_INSTRUCTIONS = (
    "This MCP server exposes the GitCode REST API through the gitcode-api Python SDK.\n\n"
    "Use the single tool gitcode_api_tool with:\n"
    "- op_type (required): the SDK resource groups.\n"
    "- action: the method on that resource (for example get, list).\n"
    "- params: keyword arguments for that method as a JSON object; omit or null means {}.\n"
    "- help: when true, returns formatted help (available methods or a method signature) instead of "
    "calling the API where applicable.\n\n"
    "Successful results are JSON-serializable. Raw bytes from endpoints such as contents.get_raw are "
    'returned as {"encoding": "base64", "data": "<ascii>"}.\n'
    'Failures are objects with "error": true and a "message" string.\n\n'
    "Valid op_type values for this SDK build:\n- "
    + "\n- ".join(OP_TYPE_ENUM)
)

TOOL_NAME = "gitcode_api_tool"
TOOL_DESCRIPTION = (
    "Call the GitCode REST API through the gitcode-api SDK. Use op_type to choose a client resource group, "
    "action as the resource method name, and params as the keyword arguments for that method. Set help=true to "
    "inspect available resource methods or a target method signature without sending an API request."
)
TOOL_PARAMETERS = {
    "type": "object",
    "properties": {
        "op_type": {
            "type": "string",
            "enum": OP_TYPE_ENUM,
            "description": "SDK resource group matching client.<op_type>, such as repos, issues, or pulls.",
        },
        "action": {
            "type": "string",
            "description": "Method name on the selected resource, such as get or list. Omit for method help.",
        },
        "params": {
            "type": "object",
            "description": "Keyword arguments passed to the SDK method. Omitted or null is treated as {}.",
        },
        "help": {
            "type": "boolean",
            "description": "When true, return dynamic SDK help instead of sending a request.",
            "default": False,
        },
    },
    "required": ["op_type"],
}
HELP_MESSAGE_TEMPLATE = """This is a help message, pass in help=false for normal usage.
{header}
Resource: {op_type}

{actions_block}
{footer}""".strip()
_INTROSPECT_API_KEY = "introspection-only"


def error_dict(message: str, **extra: Any) -> Dict[str, Any]:
    """Return a normalized tool error payload."""
    out = {"error": True, "message": message}
    out.update(extra)
    return out


def serialize(value: Any) -> Any:
    """Convert SDK responses into JSON-serializable values for tool clients."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, bytes):
        return {
            "encoding": "base64",
            "data": base64.b64encode(value).decode("ascii"),
        }
    if isinstance(value, dict):
        return {key: serialize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize(item) for item in value]
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        return serialize(to_dict())
    if isinstance(value, Mapping):
        return {key: serialize(item) for key, item in dict(value).items()}
    return str(value)


def _actions_block(resource: Any) -> str:
    lines = [resource.method_signature(name) for name in resource.methods]
    return "\n".join(lines) if lines else "(no public methods)"


def _format_help(*, op_type: str, resource: Any, header: str, footer: str = "") -> str:
    block = _actions_block(resource) if resource is not None else ""
    return HELP_MESSAGE_TEMPLATE.format(
        header=header,
        op_type=op_type,
        actions_block=block,
        footer=footer,
    ).strip()


@lru_cache(maxsize=1)
def introspection_client() -> GitCode:
    """Return a no-network client used only to inspect resource signatures."""
    return GitCode(api_key=_INTROSPECT_API_KEY)


@lru_cache(maxsize=None)
def resource_for_op_type(op_type: str) -> SyncResource:
    """Return the sync resource used for signature and method discovery."""
    return getattr(introspection_client(), op_type)


def _format_action_help(*, op_type: str, resource: Any, action: str) -> str:
    try:
        sig_line = resource.method_signature(action)
    except (TypeError, ValueError, AttributeError):
        sig_line = f"{action}(...)"
    header = f"Target signature:\n{sig_line}"
    return _format_help(op_type=op_type, resource=None, header=header)


def validate_call_kwargs(
    fn: Callable[..., Any], params: Optional[Dict[str, Any]]
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Return validated keyword arguments and an optional error message."""
    raw = dict(params) if params else {}
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError) as exc:
        return None, f"Cannot inspect signature: {exc}"

    allowed = set()
    required = []
    accepts_var_kwargs = False
    for name, param in sig.parameters.items():
        if param.kind is inspect.Parameter.VAR_POSITIONAL:
            continue
        if param.kind is inspect.Parameter.VAR_KEYWORD:
            accepts_var_kwargs = True
            continue
        allowed.add(name)
        if param.default is inspect.Parameter.empty:
            required.append(name)

    unknown = sorted(key for key in raw if key not in allowed)
    if unknown and not accepts_var_kwargs:
        return None, f"Unknown parameter(s): {', '.join(unknown)}. Allowed: {', '.join(sorted(allowed))}"

    missing = [key for key in required if key not in raw]
    if missing:
        return None, f"Missing required parameter(s): {', '.join(missing)}"

    if accepts_var_kwargs:
        return raw, None
    return {key: value for key, value in raw.items() if key in allowed}, None


class GitCodeLLMTool:
    """Callable GitCode API tool shared by OpenAI and MCP adapters.

    :param client: Optional synchronous GitCode client.
    :param async_client: Optional asynchronous GitCode client.
    :param api_key: Personal access token used when clients are not supplied.
    :param owner: Default repository owner for generated clients.
    :param repo: Default repository name for generated clients.
    :param base_url: Base URL for generated clients.
    :param timeout: Request timeout for generated clients.
    :param decrypt: Optional decryption function for encrypted access tokens.
    """

    def __init__(
        self,
        *,
        client: Optional[GitCode] = None,
        async_client: Optional[AsyncGitCode] = None,
        api_key: Optional[str] = None,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: Optional[float] = None,
        decrypt: Optional[Callable] = None,
    ) -> None:
        """Create a reusable tool with lazy sync and async clients."""
        if not (api_key or os.getenv(DEFAULT_TOKEN_ENV)):
            raise GitCodeConfigurationError("No API key provided. Pass api_key=... or set GITCODE_ACCESS_TOKEN.")
        self._client = client
        self._async_client = async_client
        self._client_kwargs = {
            "api_key": api_key,
            "owner": owner,
            "repo": repo,
            "base_url": base_url,
            "timeout": timeout,
            "decrypt": decrypt,
        }

    @property
    def client(self) -> GitCode:
        """Return the synchronous client, creating it lazily when needed."""
        if self._client is None:
            self._client = GitCode(**self._client_kwargs)  # type: ignore[arg-type]
        return self._client

    @property
    def async_client(self) -> AsyncGitCode:
        """Return the asynchronous client, creating it lazily when needed."""
        if self._async_client is None:
            self._async_client = AsyncGitCode(**self._client_kwargs)  # type: ignore[arg-type]
        return self._async_client

    def __call__(
        self,
        op_type: str,
        action: str = "",
        params: Optional[Dict[str, Any]] = None,
        help: bool = False,
        **kwargs,
    ) -> Any:
        """Invoke a synchronous GitCode SDK method through the tool contract."""
        if kwargs:
            return error_dict('Invalid tool invoke, API parameters should go into "params"')
        return self._invoke(op_type=op_type, action=action, params=params, help=help)

    async def __async_call__(
        self,
        op_type: str,
        action: str = "",
        params: Optional[Dict[str, Any]] = None,
        help: bool = False,
        **kwargs,
    ) -> Any:
        """Invoke an asynchronous GitCode SDK method through the tool contract."""
        if kwargs:
            return error_dict('Invalid tool invoke, API parameters should go into "params"')
        return await self._ainvoke(op_type=op_type, action=action, params=params, help=help)

    def _validate_action(
        self,
        *,
        op_type: str,
        action: str,
        params: Optional[Dict[str, Any]],
        help: bool,
    ) -> Tuple[Optional[str], Optional[Dict[str, Any]], Any]:
        if op_type not in OP_TYPES:
            allowed = ", ".join(OP_TYPE_ENUM)
            msg = f"Invalid op_type {op_type!r}. Allowed: {allowed}"
            if help:
                return (
                    HELP_MESSAGE_TEMPLATE.format(
                        header=msg,
                        op_type="(invalid)",
                        actions_block="",
                        footer="",
                    ).strip(),
                    None,
                    None,
                )
            return str(error_dict(msg, op_type=op_type)), None, None

        resource = resource_for_op_type(op_type)
        action = (action or "").strip()
        if not action:
            header = "Specify non-empty action to invoke a method. Available methods:"
            return _format_help(op_type=op_type, resource=resource, header=header), None, None

        if action not in resource.methods:
            msg = f"Unknown action {action!r} for op_type={op_type!r}."
            if help:
                footer = f"\n({msg})"
                return (
                    _format_help(op_type=op_type, resource=resource, header="Available methods:", footer=footer),
                    None,
                    None,
                )
            return str(error_dict(msg, op_type=op_type, action=action)), None, None

        if help:
            return _format_action_help(op_type=op_type, resource=resource, action=action), None, None

        method = getattr(resource, action)
        call_kwargs, verr = validate_call_kwargs(method, params)
        if verr is not None:
            if help:
                try:
                    sig_line = resource.method_signature(action)
                except (TypeError, ValueError, AttributeError):
                    sig_line = f"{action}(...)"
                header = f"{verr}\n\nTarget signature:\n{sig_line}"
                return _format_help(op_type=op_type, resource=None, header=header), None, None
            return str(error_dict(verr, op_type=op_type, action=action)), None, None

        return None, call_kwargs or {}, resource

    def _handle_exception(self, exc: Exception, *, op_type: str, resource: Any, help: bool) -> Dict[str, Any]:
        if isinstance(exc, GitCodeConfigurationError):
            return error_dict(str(exc), kind="configuration")
        if isinstance(exc, GitCodeHTTPStatusError):
            return error_dict(
                str(exc),
                kind="http",
                status_code=getattr(exc, "status_code", None),
                payload=getattr(exc, "payload", None),
            )
        if isinstance(exc, GitCodeError):
            return error_dict(str(exc), kind="gitcode_api")

        logger.exception("gitcode_api_tool: unexpected error")
        return error_dict(f"Unexpected error: {exc}", kind="unexpected")

    def _invoke(
        self,
        *,
        op_type: str,
        action: str,
        params: Optional[Dict[str, Any]],
        help: bool,
    ) -> Any:
        validation_result, call_kwargs, resource = self._validate_action(
            op_type=op_type,
            action=action,
            params=params,
            help=help,
        )
        if validation_result is not None:
            return validation_result

        try:
            result = getattr(getattr(self.client, op_type), action)(**(call_kwargs or {}))
        except Exception as exc:  # pylint: disable=broad-exception-caught
            return self._handle_exception(exc, op_type=op_type, resource=resource, help=help)
        return serialize(result)

    async def _ainvoke(
        self,
        *,
        op_type: str,
        action: str,
        params: Optional[Dict[str, Any]],
        help: bool,
    ) -> Any:
        validation_result, call_kwargs, resource = self._validate_action(
            op_type=op_type,
            action=action,
            params=params,
            help=help,
        )
        if validation_result is not None:
            return validation_result

        try:
            async_resource = getattr(self.async_client, op_type)
            if not isinstance(async_resource, AsyncResource):
                raise TypeError(f"client.{op_type} is not an async resource")
            result = await getattr(async_resource, action)(**(call_kwargs or {}))
        except Exception as exc:  # pylint: disable=broad-exception-caught
            return self._handle_exception(exc, op_type=op_type, resource=resource, help=help)
        return serialize(result)
