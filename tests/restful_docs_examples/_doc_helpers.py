from pathlib import Path
from typing import Any

import httpx
import json_repair

DOCS_ROOT = Path(__file__).resolve().parents[2] / "docs" / "rest_api"


def load_response_payload(doc_relative_path: str, section_title: str) -> Any:
    lines = (DOCS_ROOT / doc_relative_path).read_text(encoding="utf-8").splitlines()
    section_index = _find_line(lines, section_title)
    response_index = _find_line(lines, "Response", start=section_index)
    code_index = _find_line(lines, "   .. code:: text", start=response_index)
    block_lines = _read_code_block(lines, code_index + 1)
    raw_json = "\n".join(block_lines).strip()
    result = json_repair.loads(raw_json)
    if result and isinstance(result, list) and raw_json.startswith("{") and raw_json.endswith("}"):
        return result[0]
    return result


def make_json_handler(expected_path: str, payload: Any, method: str = "GET") -> Any:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == method
        assert request.url.path == expected_path
        return httpx.Response(200, json=payload, request=request)

    return handler


def get_value(target: Any, path: str) -> Any:
    value = target
    for part in path.split("."):
        if isinstance(value, list):
            value = value[int(part)]
        elif isinstance(value, dict):
            value = value[part]
        else:
            value = getattr(value, part)
    return value


def assert_payload_matches_object(payload: Any, result: Any, path: str = "root") -> None:
    if isinstance(payload, dict):
        for key, expected_value in payload.items():
            if isinstance(result, dict):
                assert key in result, f"Missing key {path}.{key}"
                actual_value = result[key]
            else:
                assert hasattr(result, key), f"Missing attribute {path}.{key}"
                actual_value = getattr(result, key)
            assert_payload_matches_object(expected_value, actual_value, f"{path}.{key}")
        return

    if isinstance(payload, list):
        assert isinstance(result, list), f"Expected list at {path}"
        assert len(result) == len(payload), f"List length mismatch at {path}"
        for index, expected_item in enumerate(payload):
            assert_payload_matches_object(expected_item, result[index], f"{path}[{index}]")
        return

    assert result == payload, f"Value mismatch at {path}: {result!r} != {payload!r}"


def _find_line(lines: list[str], needle: str, start: int = 0) -> int:
    for index in range(start, len(lines)):
        if lines[index] == needle:
            return index
    raise AssertionError(f"Could not find {needle!r}")


def _read_code_block(lines: list[str], start: int) -> list[str]:
    block: list[str] = []
    in_block = False

    for index in range(start, len(lines)):
        line = lines[index]
        if not in_block:
            if line.startswith("      "):
                in_block = True
                block.append(line[6:])
            continue

        if line.startswith("      "):
            block.append(line[6:])
            continue

        if line == "":
            block.append("")
            continue

        break

    if not block:
        raise AssertionError("No response code block found")

    return block
