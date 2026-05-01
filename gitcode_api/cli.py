"""Command-line interface for the GitCode SDK."""

import argparse
import inspect
import json
import re
import sys
import textwrap
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, List, Optional, Union, get_args, get_origin

import httpx

from . import GitCode, __version__
from ._base_client import DEFAULT_BASE_URL, DEFAULT_TOKEN_ENV
from ._cli_banner import format_default_welcome
from ._exceptions import GitCodeError
from .resources._shared import SyncResource


class _CLIHelpFormatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    """Preserve paragraph breaks in descriptions; wider columns for signatures."""

    def __init__(self, prog: str) -> None:
        super().__init__(prog, width=108, max_help_position=32)


def _plain_cli_inline(text: str) -> str:
    """Strip Sphinx-style inline markup (roles, doubled literals) for terminal text."""
    if not text:
        return ""
    t = re.sub(r"``\s*([^`]+?)\s*``", r"\1", text)
    t = re.sub(r":\w+:`([^`]*)`", r"\1", t)
    t = re.sub(r"`([^`]+)`", r"\1", t)
    return t


def _unwrap_optional(annotation: Any) -> Any:
    origin = get_origin(annotation)
    if origin is Union:
        args = [arg for arg in get_args(annotation) if arg is not type(None)]
        if len(args) == 1:
            return args[0]
    return annotation


def _is_list_annotation(annotation: Any) -> bool:
    annotation = _unwrap_optional(annotation)
    return get_origin(annotation) in (list, List)


def _list_item_type(annotation: Any) -> Any:
    annotation = _unwrap_optional(annotation)
    args = get_args(annotation)
    if not args:
        return str
    item_type = _unwrap_optional(args[0])
    if item_type in (int, float):
        return item_type
    return str


def _argument_kwargs(parameter: inspect.Parameter) -> dict[str, Any]:
    annotation = _unwrap_optional(parameter.annotation)
    if annotation is bool:
        return {"action": argparse.BooleanOptionalAction, "default": parameter.default}
    if _is_list_annotation(parameter.annotation):
        return {"nargs": "+", "type": _list_item_type(parameter.annotation), "default": None}
    if annotation in (int, float):
        return {"type": annotation}
    return {"type": str}


def _first_doc_line(obj: Any) -> str:
    doc = inspect.getdoc(obj).removeprefix("Synchronous ").capitalize() or ""
    for line in doc.splitlines():
        stripped = line.strip()
        if stripped:
            return _plain_cli_inline(stripped)
    return ""


def _method_cli_summary(doc: str) -> str:
    """Text before the first ':param' in the docstring, collapsed to one line for CLI help."""
    return doc.split(":param", 1)[0].strip().replace("\n", " ")


def _resource_types() -> dict[str, type[SyncResource]]:
    resources: dict[str, type[SyncResource]] = {}
    for name, annotation in GitCode.__annotations__.items():
        if inspect.isclass(annotation) and issubclass(annotation, SyncResource):
            resources[name] = annotation
    return resources


def _probe_gitcode() -> GitCode:
    """Lightweight client used only while building -h/--help metadata (no network)."""
    transport = httpx.MockTransport(lambda _request: httpx.Response(200, json={}))
    return GitCode(api_key="__cli_help__", http_client=httpx.Client(transport=transport))


def _resource_commands_epilog(resource: SyncResource) -> str:
    """List CLI subcommand names in the same order as resource.methods on the client."""
    kebab_names = [_kebab_case(name) for name in resource.methods]
    joined = ", ".join(kebab_names)
    wrapped = textwrap.fill(
        joined,
        width=120,
        initial_indent="  ",
        subsequent_indent="  ",
        break_long_words=False,
        break_on_hyphens=False,
    )
    return "Subcommands (stable SDK order, same as resource.methods):\n" + wrapped


def _kebab_case(value: str) -> str:
    return value.replace("_", "-")


def _load_json_value(raw: str) -> Any:
    if raw.startswith("@"):
        return json.loads(Path(raw[1:]).read_text(encoding="utf-8"))
    return json.loads(raw)


def _parse_scalar(raw: str) -> Any:
    try:
        return _load_json_value(raw)
    except (OSError, ValueError, json.JSONDecodeError):
        return raw


def _parse_key_value(raw: str) -> tuple[str, Any]:
    if "=" not in raw:
        raise ValueError(f"Expected KEY=VALUE, got: {raw}")
    key, value = raw.split("=", maxsplit=1)
    if not key:
        raise ValueError(f"Expected KEY=VALUE, got: {raw}")
    return key, _parse_scalar(value)


def _to_data(value: Any) -> Any:
    if hasattr(value, "to_dict") and callable(value.to_dict):
        return _to_data(value.to_dict())
    if isinstance(value, Mapping):
        return {key: _to_data(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_to_data(item) for item in value]
    return value


def _write_output(value: Any, *, output_file: Optional[str], compact: bool) -> None:
    if value is None:
        return
    if isinstance(value, bytes):
        if output_file:
            Path(output_file).write_bytes(value)
        else:
            sys.stdout.buffer.write(value)
        return

    payload = _to_data(value)
    if isinstance(payload, str):
        text = payload
    else:
        text = json.dumps(payload, indent=None if compact else 2, ensure_ascii=True, sort_keys=True)

    if output_file:
        Path(output_file).write_text(text + ("\n" if not text.endswith("\n") else ""), encoding="utf-8")
    else:
        print(text)


def _invocation_parent_parser() -> argparse.ArgumentParser:
    """Parser with flags for real API calls (attached only to leaf METHOD parsers, not top-level usage)."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--api-key", help=f"GitCode access token. Defaults to {DEFAULT_TOKEN_ENV}.")
    parser.add_argument("--owner", help="Default repository owner.")
    parser.add_argument("--repo", help="Default repository name.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Base URL for the REST API.")
    parser.add_argument("--timeout", type=float, default=None, help="Request timeout in seconds.")
    parser.add_argument("--output-file", help="Write the response to a file instead of stdout.")
    parser.add_argument("--compact", action="store_true", help="Print JSON without indentation.")
    return parser


def _root_banner() -> str:
    return "Connection and defaults are documented on each method's help: %(prog)s RESOURCE METHOD -h."


def build_parser() -> argparse.ArgumentParser:
    """Build main parser."""
    common = _invocation_parent_parser()
    epilog = """\
Examples:
  %(prog)s pulls list --api-key "$GITCODE_ACCESS_TOKEN" --owner my-org --repo my-repo
  %(prog)s users me --api-key "$GITCODE_ACCESS_TOKEN"
  %(prog)s pulls list --set only_count=true --set reviewer=demo

Extra keyword arguments (**params / **payload on some methods):
  Repeat --set key=value (value is JSON if it parses as JSON; otherwise a string).
  --set-json merges one JSON object (or @path/to/file.json) into those kwargs.

Each resource -h lists subcommands in SDK order (resource.methods).
Each method -h opens with resource.method_signature("<name>") from the Python SDK.
"""
    parser = argparse.ArgumentParser(
        prog="gitcode-api",
        usage="%(prog)s [-h] [--version] RESOURCE ...",
        description=_root_banner(),
        epilog=epilog,
        formatter_class=_CLIHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    client = _probe_gitcode()
    try:
        resource_parsers = parser.add_subparsers(
            dest="resource",
            required=True,
            metavar="RESOURCE",
            title="resources",
            description="Pick a resource group (same attribute names as on GitCode, e.g. pulls, repos).",
        )
        for resource_name, resource_type in _resource_types().items():
            resource = getattr(client, resource_name)
            class_doc = inspect.getdoc(resource_type).removeprefix("Synchronous ").capitalize() or ""
            class_lead = class_doc.split("\n\n", maxsplit=1)[0].strip() if class_doc else ""
            class_lead = _plain_cli_inline(class_lead) if class_lead else ""
            resource_desc_parts = [
                class_lead or _first_doc_line(resource_type),
                "",
                _resource_commands_epilog(resource),
            ]
            resource_parser = resource_parsers.add_parser(
                _kebab_case(resource_name),
                help=_first_doc_line(resource_type) or f"GitCode {resource_name} endpoints.",
                description="\n".join(resource_desc_parts),
                formatter_class=_CLIHelpFormatter,
            )
            method_parsers = resource_parser.add_subparsers(
                dest="method",
                required=True,
                title="methods",
                metavar="METHOD",
                description=(
                    "Method names use kebab-case. The opening line of each command's help matches "
                    "resource.method_signature('<name>') on the Python client."
                ),
            )

            for method_name in resource.methods:
                method = getattr(resource, method_name)
                sig_line = resource.method_signature(method_name)
                doc = inspect.getdoc(method).removeprefix("Synchronous ").capitalize() or ""
                summary = _method_cli_summary(doc)
                if summary and len(summary) > 90:
                    method_help = summary[:87] + "..."
                else:
                    method_help = summary or (sig_line if len(sig_line) <= 90 else sig_line[:87] + "...")
                method_description = f"{summary}\n\n{sig_line}" if summary else sig_line

                method_parser = method_parsers.add_parser(
                    _kebab_case(method_name),
                    help=method_help,
                    description=method_description,
                    formatter_class=_CLIHelpFormatter,
                    parents=[common],
                )
                signature = inspect.signature(method)
                for parameter in signature.parameters.values():
                    if parameter.name == "self":
                        continue
                    if parameter.kind == inspect.Parameter.VAR_KEYWORD:
                        method_parser.add_argument(
                            "--set",
                            dest="extra_items",
                            action="append",
                            default=None,
                            metavar="KEY=VALUE",
                            help="Extra keyword argument (merged into **params / **payload).",
                        )
                        method_parser.add_argument(
                            "--set-json",
                            dest="extra_json",
                            default=None,
                            metavar="JSON_OR_@FILE",
                            help="JSON object merged into extra keyword arguments.",
                        )
                        continue

                    flag = f"--{parameter.name.replace('_', '-')}"
                    if flag in method_parser._option_string_actions:
                        continue
                    kwargs = _argument_kwargs(parameter)
                    kwargs["dest"] = parameter.name
                    kwargs["required"] = parameter.default is inspect.Signature.empty
                    method_parser.add_argument(flag, **kwargs)

                method_parser.set_defaults(resource_name=resource_name, method_name=method_name)
    finally:
        client.close()

    return parser


def _collect_kwargs(args: argparse.Namespace, method: Any) -> dict[str, Any]:
    signature = inspect.signature(method)
    kwargs: dict[str, Any] = {}
    for parameter in signature.parameters.values():
        if parameter.name == "self":
            continue
        if parameter.kind == inspect.Parameter.VAR_KEYWORD:
            extra_kwargs: dict[str, Any] = {}
            if getattr(args, "extra_json", None):
                raw_extra = _load_json_value(args.extra_json)
                if not isinstance(raw_extra, dict):
                    raise ValueError("--set-json must decode to a JSON object.")
                extra_kwargs.update(raw_extra)
            for item in getattr(args, "extra_items", []) or []:
                key, value = _parse_key_value(item)
                extra_kwargs[key] = value
            kwargs.update(extra_kwargs)
            continue

        value = getattr(args, parameter.name)
        if value is None:
            if parameter.default is inspect.Signature.empty:
                raise ValueError(f"--{parameter.name.replace('_', '-')} is required.")
            continue
        kwargs[parameter.name] = value
    return kwargs


def main(argv: Optional[Sequence[str]] = None) -> int:
    """CLI entry point."""
    parser = build_parser()
    effective = list(sys.argv[1:] if argv is None else argv)
    if not effective:
        print(format_default_welcome(__version__), end="")
        saved_epilog = parser.epilog
        parser.epilog = None
        try:
            parser.print_help()
        finally:
            parser.epilog = saved_epilog
        return 0
    args = parser.parse_args(effective)

    try:
        with GitCode(
            api_key=args.api_key,
            owner=args.owner,
            repo=args.repo,
            base_url=args.base_url,
            timeout=args.timeout,
        ) as client:
            resource = getattr(client, args.resource_name)
            method = getattr(resource, args.method_name)
            result = method(**_collect_kwargs(args, method))
    except (GitCodeError, OSError, TypeError, ValueError) as exc:  # pragma: no cover - integration style
        print(f"error: {exc}", file=sys.stderr)
        return 1

    _write_output(result, output_file=args.output_file, compact=args.compact)
    return 0
