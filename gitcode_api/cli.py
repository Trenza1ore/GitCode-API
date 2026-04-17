"""Command-line interface for the GitCode SDK."""

import argparse
import inspect
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, List, Optional, Union, get_args, get_origin

from . import GitCode, __version__
from ._base_client import DEFAULT_BASE_URL, DEFAULT_TOKEN_ENV
from ._exceptions import GitCodeError
from .resources._shared import SyncResource


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
    doc = inspect.getdoc(obj) or ""
    return doc.splitlines()[0] if doc else ""


def _resource_types() -> dict[str, type[SyncResource]]:
    resources: dict[str, type[SyncResource]] = {}
    for name, annotation in GitCode.__annotations__.items():
        if inspect.isclass(annotation) and issubclass(annotation, SyncResource):
            resources[name] = annotation
    return resources


def _iter_resource_methods(resource_type: type[SyncResource]) -> list[tuple[str, Any]]:
    methods: list[tuple[str, Any]] = []
    for name, value in resource_type.__dict__.items():
        if name.startswith("_") or not inspect.isfunction(value):
            continue
        methods.append((name, value))
    return methods


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


def _global_parent_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--api-key", help=f"GitCode access token. Defaults to {DEFAULT_TOKEN_ENV}.")
    parser.add_argument("--owner", help="Default repository owner.")
    parser.add_argument("--repo", help="Default repository name.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Base URL for the GitCode REST API.")
    parser.add_argument("--timeout", type=float, default=None, help="Request timeout in seconds.")
    parser.add_argument("--output-file", help="Write the response to a file instead of stdout.")
    parser.add_argument("--compact", action="store_true", help="Print JSON without indentation.")
    return parser


def build_parser() -> argparse.ArgumentParser:
    common = _global_parent_parser()
    parser = argparse.ArgumentParser(
        prog="gitcode-api",
        description="Invoke any synchronous gitcode-api resource method from the command line.",
        epilog='Use `--set key=value` and `--set-json \'{"key": "value"}\'` for methods with `**params` or `**payload`.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        parents=[common],
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    resource_parsers = parser.add_subparsers(dest="resource", required=True)
    for resource_name, resource_type in _resource_types().items():
        resource_parser = resource_parsers.add_parser(
            _kebab_case(resource_name),
            help=_first_doc_line(resource_type),
        )
        method_parsers = resource_parser.add_subparsers(dest="method", required=True)

        for method_name, method in _iter_resource_methods(resource_type):
            method_parser = method_parsers.add_parser(
                _kebab_case(method_name),
                help=_first_doc_line(method),
                description=inspect.getdoc(method),
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
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
                        help="Additional keyword arguments for `**params` or `**payload`.",
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
    parser = build_parser()
    args = parser.parse_args(argv)

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
