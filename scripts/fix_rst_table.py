#!/usr/bin/env python3
"""Fix alignment for reStructuredText grid tables in a file."""

import argparse
import glob
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple, Union


@dataclass
class SeparatorLine:
    marker: str
    widths: List[int]


@dataclass
class RowLine:
    cells: List[str]


TableLine = Union[SeparatorLine, RowLine]


def _line_indent(line: str) -> str:
    return line[: len(line) - len(line.lstrip(" "))]


def _strip_indent(line: str, indent: str) -> str:
    if indent and line.startswith(indent):
        return line[len(indent) :]
    return line


def _without_newline(line: str) -> str:
    return line.rstrip("\n\r")


def _display_width(text: str) -> int:
    width = 0
    for char in text:
        if unicodedata.combining(char):
            continue
        width += 2 if unicodedata.east_asian_width(char) in {"F", "W"} else 1
    return width


def _is_separator_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped.startswith("+") or not stripped.endswith("+"):
        return False
    if stripped.count("+") < 2:
        return False
    allowed = set("+-= ")
    if any(char not in allowed for char in stripped):
        return False
    return any(char in "-=" for char in stripped)


def _is_row_line(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2


def _is_table_line(line: str) -> bool:
    return _is_separator_line(line) or _is_row_line(line)


def _parse_row(line: str) -> List[str]:
    """Split a row by column boundaries and trim padding around content."""
    stripped = line.strip()
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def _separator_column_count(line: str) -> int:
    return line.strip().count("+") - 1


def _separator_widths(line: str) -> List[int]:
    stripped = line.strip()
    return [len(cell) for cell in stripped[1:-1].split("+")]


def _boundary_columns(line: str, boundary: str) -> List[int]:
    columns: List[int] = []
    column = 0
    for char in line.strip():
        if char == boundary:
            columns.append(column)
        column += _display_width(char)
    return columns


def _table_is_aligned(lines: Sequence[str], indent: str) -> bool:
    stripped_lines = [_strip_indent(_without_newline(line), indent) for line in lines]
    expected: Optional[List[int]] = None
    for line in stripped_lines:
        if _is_separator_line(line):
            columns = _boundary_columns(line, "+")
            if expected is None:
                expected = columns
            elif columns != expected:
                return False
        elif _is_row_line(line):
            if expected is None or _boundary_columns(line, "|") != expected:
                return False
    return expected is not None


def _parse_table(lines: Sequence[str]) -> Optional[Tuple[str, List[TableLine], int]]:
    if len(lines) < 3:
        return None

    indents = [_line_indent(line) for line in lines if line.strip()]
    indent = min(indents, key=len) if indents else ""
    stripped_lines = [_strip_indent(_without_newline(line), indent) for line in lines]

    if not _is_separator_line(stripped_lines[0]) or not _is_separator_line(stripped_lines[-1]):
        return None

    ncols: Optional[int] = None
    parsed: List[TableLine] = []
    has_row = False

    for line in stripped_lines:
        if _is_separator_line(line):
            count = _separator_column_count(line)
            if ncols is None:
                ncols = count
            elif count != ncols:
                return None
            marker = "=" if "=" in line else "-"
            parsed.append(SeparatorLine(marker=marker, widths=_separator_widths(line)))
            continue

        if not _is_row_line(line):
            return None

        cells = _parse_row(line)
        if ncols is None:
            ncols = len(cells)
        elif len(cells) != ncols:
            return None
        has_row = True
        parsed.append(RowLine(cells=cells))

    if not has_row or ncols is None:
        return None
    return indent, parsed, ncols


def _compute_widths(parsed: Sequence[TableLine], ncols: int) -> List[int]:
    widths = [0] * ncols
    for line in parsed:
        if isinstance(line, RowLine):
            for index, cell in enumerate(line.cells):
                widths[index] = max(widths[index], _display_width(cell) + 2)
        else:
            for index, width in enumerate(line.widths):
                widths[index] = max(widths[index], width)
    return [max(width, 3) for width in widths]


def _format_separator(widths: Sequence[int], marker: str) -> str:
    return "+" + "+".join(marker * width for width in widths) + "+"


def _format_row(widths: Sequence[int], cells: Sequence[str]) -> str:
    parts: List[str] = []
    for width, cell in zip(widths, cells):
        col_width = width - 2
        display_adjustment = _display_width(cell) - len(cell)
        parts.append(" %-*s " % (col_width - display_adjustment, cell))
    return "|" + "|".join(parts) + "|"


def _format_table(indent: str, parsed: Sequence[TableLine], ncols: int) -> List[str]:
    widths = _compute_widths(parsed, ncols)
    out: List[str] = []
    for line in parsed:
        if isinstance(line, SeparatorLine):
            out.append(indent + _format_separator(widths, line.marker))
        else:
            out.append(indent + _format_row(widths, line.cells))
    return out


def _find_table_blocks(lines: Sequence[str]) -> List[Tuple[int, int]]:
    blocks: List[Tuple[int, int]] = []
    index = 0
    while index < len(lines):
        if not _is_separator_line(_without_newline(lines[index])):
            index += 1
            continue

        end = index + 1
        while end < len(lines) and _is_table_line(_without_newline(lines[end])):
            end += 1

        if _parse_table(lines[index:end]) is not None:
            blocks.append((index, end))
            index = end
        else:
            index += 1

    return blocks


def fix_rst_tables(text: str) -> Tuple[str, int]:
    """Return ``text`` with grid tables realigned and the number of rewrites."""
    ends_with_newline = text.endswith("\n")
    lines = text.splitlines()
    blocks = _find_table_blocks(lines)
    if not blocks:
        return text, 0

    out = list(lines)
    changed = 0
    for start, end in reversed(blocks):
        parsed = _parse_table(out[start:end])
        if parsed is None:
            continue
        indent, table_lines, ncols = parsed
        if _table_is_aligned(out[start:end], indent):
            continue
        fixed = _format_table(indent, table_lines, ncols)
        if fixed != out[start:end]:
            changed += 1
            out[start:end] = fixed

    fixed_text = "\n".join(out)
    if ends_with_newline:
        fixed_text += "\n"
    return fixed_text, changed


def fix_file(path: Path, *, check: bool = False) -> int:
    original = path.read_text(encoding="utf-8")
    fixed, changed = fix_rst_tables(original)

    if check:
        if changed:
            print(f"{path}: {changed} table(s) need alignment")
            return 1
        print(f"{path}: all tables aligned")
        return 0

    if changed:
        path.write_text(fixed, encoding="utf-8", newline="\n")
    print(f"{path}: fixed {changed} table(s)")
    return 0


def _expand_paths(patterns: Sequence[str]) -> List[Path]:
    paths: List[Path] = []
    seen = set()

    for pattern in patterns:
        matches = sorted(glob.glob(pattern, recursive=True)) if glob.has_magic(pattern) else [pattern]
        if not matches:
            raise ValueError(f"{pattern} did not match any files")

        for match in matches:
            path = Path(match)
            if not path.is_file():
                raise ValueError(f"{path} is not a file")
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                paths.append(path)

    return paths


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="reStructuredText files or glob patterns to update")
    parser.add_argument(
        "--check",
        action="store_true",
        help="report whether tables need changes without writing the file",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        paths = _expand_paths(args.paths)
    except ValueError as exc:
        parser.error(str(exc))

    exit_code = 0
    try:
        for path in paths:
            exit_code = max(exit_code, fix_file(path, check=args.check))
    except UnicodeDecodeError as exc:
        print(f"failed to read as UTF-8: {exc}", file=sys.stderr)
        return 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
