# Changelog

All notable changes to this project are documented here. Release ranges link to the GitHub compare view. Tag names follow the repository (`v1.0.x` through `v1.0.3`, then `1.1.0` onward).

## [1.2.8](https://github.com/Trenza1ore/GitCode-API/compare/1.2.7...1.2.8) — 2026-05-07

Changes since `1.2.7`…`1.2.8`.

### Feature

- **MCPB:** We now provide [MCPB bundle](https://claude.com/docs/connectors/building/mcpb) for Claude Desktop App.

### CI

- **MCPB:** `.github/workflows/release-mcpb.yml` builds and uploads `gitcode-<version>.mcpb` to published GitHub Releases.

### Chore

- **MCPB:** `scripts/build_manifest.py`, tracked `scripts/manifest.json`, `.mcpbignore`, and **`make mcpb`** (manifest build plus `mcpb pack`); `tests/test_build_manifest.py` covers the manifest step.
- **GitHub:** bug report and feature request issue templates, with wording and metadata follow-ups.

### Docs

- **MCP / Claude Desktop:** README, `install_mcp_server.md`, `docs/sdk/llm_tools.rst`, and `AGENTS.md` point to Anthropic’s [Build a desktop extension with MCPB](https://claude.com/docs/connectors/building/mcpb) guide for the `.mcpb` install flow.

---

## [1.2.7](https://github.com/Trenza1ore/GitCode-API/compare/1.2.6...1.2.7) — 2026-05-06

Changes since `1.2.6`…`1.2.7`.

### Feature

- **MCP:** default instructions on the FastMCP server, plus **help resources** so clients can discover usage without calling the GitCode tool first.

### Fix

- **MCP / LLM tools:** API-key validation no longer requires a configured key for help-oriented behavior (aligned with the new help surface).
- **MCP / LLM tools:** tightened return types by removing a few unnecessary `Any` annotations.

### Docs

- **MCP:** setup guidance for IDEs and agents, including badges/pointers for editors such as VS Code and Cursor.
- Sphinx: fixed a spot that mixed Markdown-style markup with reST; `AGENTS.md` now warns against that pattern.
- `AGENTS.md`: brought agent guidance in line with post-1.2.5 behavior.

---

## [1.2.6](https://github.com/Trenza1ore/GitCode-API/compare/1.2.5...1.2.6) — 2026-05-06

Changes since `1.2.5`…`1.2.6`.

### Fix

- **PyInstaller / `make binary`:** the uv `binary` dependency group now includes the `mcp` group so frozen CLI builds install FastMCP (Python **3.10+**) and optional MCP code paths resolve correctly during the build.

---

## [1.2.5](https://github.com/Trenza1ore/GitCode-API/compare/1.2.4...1.2.5) — 2026-05-06

Changes since `1.2.4`…`1.2.5`.

### Feature

- **LLM integrations:** optional adapters under `gitcode_api.llm` for agent workflows — `GitCodeOpenAITool` (OpenAI Chat Completions tool shape) and **MCP** helpers (`GitCodeMCP`, `create_mcp_gitcode_api_tool`, `register_mcp_gitcode_api_tool`, `create_mcp_server`) built on FastMCP when the `mcp` extra is installed (`pip install 'gitcode-api[mcp]'`; requires Python **3.10+** for FastMCP). Heavy dependencies load lazily via `gitcode_api.llm.__getattr__`.

### Refactor

- Tightened typing across the package so `mypy -p gitcode_api` passes cleanly.

### Chore

- Expanded PyPI metadata (description, keywords, classifiers) to mention CLI and optional LLM/MCP integration.
- Added a `changelog` URL entry in `[project.urls]` pointing at this file.
- **`make docs`** now also builds Sphinx **epub** and **singlehtml** outputs (alongside **html**), using a shared doctree cache to avoid EPUB mimetype warnings.

### Docs

- README updates for MCP and OpenAI tool usage, plus an FAQ section aligned with the bundled skill.
- Sphinx SDK guide `docs/sdk/llm_tools.rst` (OpenAI `GitCodeOpenAITool`, MCP / FastMCP helpers, shared `GitCodeLLMTool`, TLS notes) linked from `docs/sdk/index.rst` and the docs landing page; `gitcode_api.llm` modules added to the autosummary reference.
- Added a CodeFactor badge; fixed a broken link in `README.zh.md`.
- `AGENTS.md`: documented the preferred git commit message convention.
- README Makefile section refreshed for the current targets.

---

## [1.2.4](https://github.com/Trenza1ore/GitCode-API/compare/1.2.3...1.2.4) — 2026-05-01

Changes since `1.2.3`…`1.2.4`.

### Fix

- **Release zip contents:** GitHub Release zips built by `scripts/package_release_zip.py` no longer include `examples/README.md`; they still bundle the PyInstaller CLI, `.claude/`, and the repository root `README.md` / `README.zh.md`.

### Docs

- Corrected `AGENTS.md` and the `1.2.3` changelog bullets so they describe the same zip layout as the packager.

---

## [1.2.3](https://github.com/Trenza1ore/GitCode-API/compare/1.2.2...1.2.3) — 2026-05-01

Changes since `1.2.2`…`1.2.3`.

### CI

- **Release binaries:** uploads are now versioned `.zip` files (`gitcode-api-<tag>-<platform>.zip`) that bundle the PyInstaller CLI with the `.claude/` skill tree and `README.md` / `README.zh.md` (not `examples/README.md`), assembled by `scripts/package_release_zip.py`.
- Pinned build matrix to `ubuntu-22.04`, `ubuntu-24.04`, `macos-14` (arm64), and `windows-2022`, and builds with Python **3.12** (replacing `*-latest` / 3.13) for more predictable release artifacts.

### Chore

- Added `scripts/package_release_zip.py` to create the release zip layout with best-effort compression.

### Docs

- Updated `AGENTS.md` to describe the zip-based GitHub Release assets.

---

## [1.2.2](https://github.com/Trenza1ore/GitCode-API/compare/1.2.1...1.2.2) — 2026-05-01

Changes since `1.2.1`…`1.2.2`.

### Feature

- Added a PyInstaller **one-file** build for the `gitcode-api` CLI (`gitcode-api.spec`, entry script under `scripts/`), installable via a new uv dependency group `binary` and the `make binary` target (output under `dist/`).

### CI

- Added a **Release binaries** workflow that runs on published GitHub Releases, builds the CLI on Linux (x86_64), Windows (x86_64), and macOS (Apple Silicon), and uploads versioned release assets.

### Chore

- Tracked `gitcode-api.spec` in git while keeping other `*.spec` ignored.

### Docs

- Documented the standalone binary workflow in `AGENTS.md`.

---

## [1.2.1](https://github.com/Trenza1ore/GitCode-API/compare/1.2.0...1.2.1) — 2026-05-01

Changes since `1.2.0`…`1.2.1`.

### Feature

- Added `AGENTS.md` as repository guidance for AI-assisted development workflows.
- Improved the bundled GitCode API skill: tighter workflow patterns, SKILL updates, and enhancements to the skill’s `gitcode_api_cli` helper script.

### Chore

- Extended the `Makefile` with `docstring` (pydocstyle) and `amend` helpers, and broadened `.PHONY` coverage for existing targets.

### Style

- Aligned package docstrings with reStructuredText field conventions for pydocstyle checks.

### Docs

- Expanded and refreshed CLI documentation (`docs/sdk/cli.rst`).
- Simplified README and Sphinx quickstart examples by removing `try`/`finally` boilerplate around the client.
- Minor README improvements (English and Chinese).

---

## [1.2.0](https://github.com/Trenza1ore/GitCode-API/compare/1.1.3...1.2.0) — 2026-05-01

Changes since `1.1.3`…`1.2.0`.

### Feature

- Exposed a `methods` property on resource namespaces so callers can discover available API methods at runtime.
- Exposed `method_signature` on resource groups to inspect method parameters and return shape.
- Added the `examples/inspect_resource_group_methods.py` example script demonstrating introspection helpers.

### Fix

- **Client:** Removed leftover legacy behavior around closing `httpx` clients so shutdown matches current usage.
- Switched LRU-cached properties to `functools.cached_property` for correct semantics and compatibility.
- Avoided using the builtin `collections` name as a generic type alias in examples and tests (Python compatibility).
- Reworked resource group lifecycle so garbage collection and client teardown behave predictably.

### Style

- Polished CLI presentation.
- Added Pylint format configuration.
- Removed a redundant README badge.

### Docs

- Documented CLI usage in the main docs.
- Removed the REST API quickstart page.
- Updated `pulls.create` docstring for fork-based pull request flows.
- Standardized documentation terminology to **resource group**.
- Updated the bundled skill README for `methods`, `method_signature`, and related workflow.

---

## [1.1.3](https://github.com/Trenza1ore/GitCode-API/compare/1.1.2...1.1.3) — 2026-04-18

### Feature

- Experimental CLI support (`gitcode-api` entry point).

### Docs

- Changed pip installation examples to use the `-U` option.
- Minor index and copy tweaks (including capitalization of “GitHub”).

---

## [1.1.2](https://github.com/Trenza1ore/GitCode-API/compare/1.1.1...1.1.2) — 2026-04-16

### Feature

- Bundled Cursor/agent skill for GitCode API workflows.
- Support for encrypted GitCode tokens.

### Fix

- Clients now close their `httpx` client whether a custom client was supplied or not.

### Docs

- Updated documentation and skill for token encryption.
- Added project links to the docs site.

### Style

- README and Chinese README badge updates and link styling; more compact code blocks in README.

---

## [1.1.1](https://github.com/Trenza1ore/GitCode-API/compare/1.1.0...1.1.1) — 2026-04-16

### Feature

- Stronger response model typing and annotations across the client.
- Redefined context manager `__enter__` on synchronous and asynchronous client classes for clearer type annotations.

### Fix

- Corrected mirrored official REST API documentation (`docs/rest_api/orgs.rst`).
- Pytest configuration adjustments.

### Style

- Examples switched to attribute-style access where appropriate.

---

## [1.1.0](https://github.com/Trenza1ore/GitCode-API/compare/v1.0.3...1.1.0) — 2026-04-16

### Feature

- Refreshed examples; removed `python-dotenv` from package dependencies.

### Fix

- Makefile `format` target repair.

### Style

- Expanded docstring coverage; codebase formatted with Ruff.
- PyPI badge updated to include a link.

### Test

- Added unit tests for context manager usage.

### Docs

- Documentation refresh and context manager usage called out explicitly.

---

## [1.0.3](https://github.com/Trenza1ore/GitCode-API/compare/v1.0.2...v1.0.3) — 2026-04-16

### Chore

- Removed redundant PyPI license classifier from package metadata.

---

## [1.0.2](https://github.com/Trenza1ore/GitCode-API/compare/v1.0.1...v1.0.2) — 2026-04-16

### Fix

- Ensured Read the Docs installs the `gitcode-api` package in the docs environment.

### Chore

- Read the Docs configuration updates for hosted builds.

---

## [1.0.1](https://github.com/Trenza1ore/GitCode-API/compare/v1.0.0...v1.0.1) — 2026-04-16

### Fix

- Corrected the example for listing commits.
- Restored Python 3.9 compatibility where it had regressed.

### Docs

- README updates alongside the version bump.

---

## [1.0.0](https://github.com/Trenza1ore/GitCode-API/releases/tag/v1.0.0) — 2026-04-15

Initial published release on PyPI.

### Feature

- Initial `gitcode-api` Python SDK for the GitCode REST API (HTTPX-based client).

### Chore

- CI/workflow: PyPI project URL correction in publishing configuration.

### Docs

- README updates for the first public release.
