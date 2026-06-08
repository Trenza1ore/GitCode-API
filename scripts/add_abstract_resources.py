#!/usr/bin/env python3
"""Add abstract base classes to resource group files.

For each ``*_resource_group.py``, creates an ``AbstractXResource(ABC)`` class
whose ``@abstractmethod`` stubs carry the docstrings and parameter signatures.
``XResource`` and ``AsyncXResource`` then inherit from the abstract class
alongside their transport base, so the method implementations no longer need
their own docstrings.
"""

import ast
import re
from pathlib import Path

RESOURCE_DIR = Path("gitcode_api/resources")
DISABLE_COMMENTS = "# mypy: disable-error-code=override\n# pylint: disable=invalid-overridden-method\n"


def find_files():
    return sorted(RESOURCE_DIR.glob("*/*_resource_group.py"))


def _docstring_range(node):
    """Return ``(start, end)`` 0-based inclusive line indices of a docstring, or *None*."""
    if not node.body:
        return None
    first = node.body[0]
    if isinstance(first, ast.Expr) and isinstance(getattr(first, "value", None), ast.Constant):
        if isinstance(first.value.value, str):
            return (first.lineno - 1, first.end_lineno - 1)
    return None


def _signature_lines(method, lines):
    """Return the ``def …:`` lines (may span multiple lines for long signatures)."""
    start = method.lineno - 1
    body_start = method.body[0].lineno - 1
    return lines[start:body_start]


def _build_abstract_method(method, lines):
    """Build an ``@abstractmethod`` stub from a sync method."""
    sig = _signature_lines(method, lines)
    ds = _docstring_range(method)
    parts = ["    @abstractmethod\n"]
    parts.extend(sig)
    if ds:
        parts.extend(lines[ds[0] : ds[1] + 1])
    else:
        parts.append("        ...\n")
    return parts


def _method_without_docstring(method, lines):
    """Return the method source with its docstring removed."""
    start = method.lineno - 1
    end = method.end_lineno
    ds = _docstring_range(method)
    if ds:
        return lines[start : ds[0]] + lines[ds[1] + 1 : end]
    return lines[start:end]


def _class_body_without_method_docstrings(cls_node, lines):
    """Emit the class body: keep the class docstring, strip method docstrings."""
    parts = []
    class_ds = _docstring_range(cls_node)
    if class_ds:
        parts.extend(lines[class_ds[0] : class_ds[1] + 1])
    for node in cls_node.body:
        if class_ds and node.lineno - 1 == class_ds[0]:
            continue
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            parts.append("\n")
            parts.extend(_method_without_docstring(node, lines))
        else:
            parts.extend(lines[node.lineno - 1 : node.end_lineno])
    return parts


def process_file(filepath):
    source = filepath.read_text()
    lines = source.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"

    tree = ast.parse(source, filename=str(filepath))

    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    if len(classes) != 2:
        print(f"SKIP: {filepath} ({len(classes)} classes)")
        return

    sync_cls = next((c for c in classes if not c.name.startswith("Async")), None)
    async_cls = next((c for c in classes if c.name.startswith("Async")), None)
    if not sync_cls or not async_cls:
        print(f"SKIP: {filepath}")
        return

    abstract_name = f"Abstract{sync_cls.name}"
    sync_methods = [n for n in sync_cls.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]

    output = []

    # ── 1. Module docstring ─────────────────────────────────────────────
    mod_ds = ast.get_docstring(tree)
    if mod_ds:
        new_ds = mod_ds.replace(
            f"{sync_cls.name} and {async_cls.name}",
            f"{abstract_name}, {sync_cls.name}, and {async_cls.name}",
        )
        output.append(f'"""{new_ds}"""\n')

    # ── 2. Imports ──────────────────────────────────────────────────────
    import_nodes = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    has_abc = any(isinstance(n, ast.ImportFrom) and n.module == "abc" for n in import_nodes)

    if import_nodes:
        import_start = import_nodes[0].lineno - 1
        import_end = import_nodes[-1].end_lineno
        output.append("\n")
        if not has_abc:
            output.append("from abc import ABC, abstractmethod\n")
        output.extend(lines[import_start:import_end])

    # ── 3. Disable comments ────────────────────────────────────────────
    output.append("\n")
    output.append(DISABLE_COMMENTS)

    # ── 4. Module-level code between imports and first class ────────────
    between_start = import_nodes[-1].end_lineno if import_nodes else 0
    first_class_line = sync_cls.lineno - 1
    between_text = "".join(lines[between_start:first_class_line]).strip()
    if between_text:
        output.append("\n")
        output.append(between_text + "\n")

    # ── 5. Abstract class ──────────────────────────────────────────────
    resource_label = sync_cls.name.replace("Resource", "")
    output.append(f"\n\nclass {abstract_name}(ABC):\n")
    output.append(f'    """Interface for {resource_label} resource endpoints."""\n')
    for method in sync_methods:
        output.append("\n")
        output.extend(_build_abstract_method(method, lines))

    # ── 6. Sync class ──────────────────────────────────────────────────
    output.append(f"\n\nclass {sync_cls.name}(SyncResource, {abstract_name}):\n")
    output.extend(_class_body_without_method_docstrings(sync_cls, lines))

    # ── 7. Async class ─────────────────────────────────────────────────
    output.append(f"\n\nclass {async_cls.name}(AsyncResource, {abstract_name}):\n")
    output.extend(_class_body_without_method_docstrings(async_cls, lines))

    result = "".join(output)
    result = re.sub(r"\n{4,}", "\n\n\n", result)
    result = result.rstrip("\n") + "\n"

    filepath.write_text(result)
    print(f"OK: {filepath}")


def main():
    files = find_files()
    print(f"Found {len(files)} files")
    for f in files:
        process_file(f)


if __name__ == "__main__":
    main()
