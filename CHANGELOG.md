# Changelog

All notable changes to this project are documented here. Release ranges link to the GitHub compare view. Tag names follow the repository (`v1.0.x` through `v1.0.3`, then `1.1.0` onward).

## [1.2.10](https://github.com/Trenza1ore/GitCode-API/compare/1.2.9...1.2.10) — 2026-05-07

Changes since `1.2.9`…`1.2.10`.

### Feature

- **OpenAI tool (**`GitCodeOpenAITool`**):** Invocation results are now **JSON strings** (`str`) from `json.dumps` with `ensure_ascii=False`, so payloads fit Chat Completions **tool** message `content` without extra serialization. `**indent`** controls formatting (default `**2**`; pass `**None**` for compact single-line JSON).
- **OpenAI tool constructor:** `**async_mode`** defaults to `**False**`. Use `**async_mode=True**` and `**await**` the coroutine returned from the instance — the `**async**` keyword alias for async mode is no longer accepted on `GitCodeOpenAITool`.

### Docs

- README (English and Chinese), SDK LLM guide, and new runnable example `**examples/openai_tool_call.py**` updated for string tool results and a multi-turn Chat Completions loop.

---

## [1.2.9](https://github.com/Trenza1ore/GitCode-API/compare/1.2.8...1.2.9) — 2026-05-07

Changes since `1.2.8`…`1.2.9`.

### Feature

- **LLM tools:** Optional [openJiuwen](https://openjiuwen.com) integration — install `openjiuwen` (Python **3.11+**), then use `create_openjiuwen_gitcode_api_tool` from `gitcode_api.llm` with the same GitCode tool contract as the OpenAI and MCP adapters.

### Docs

- README (English and Chinese), SDK LLM guide, and PyPI description updated for openJiuwen.

---

## [1.2.8](https://github.com/Trenza1ore/GitCode-API/compare/1.2.7...1.2.8) — 2026-05-07

Changes since `1.2.7`…`1.2.8`.

### Feature

- **Claude Desktop:** Install the GitCode MCP server as an [MCPB](https://claude.com/docs/connectors/building/mcpb) bundle; each GitHub Release ships a matching `gitcode-<version>.mcpb` you can add in Claude Desktop.

### Docs

- README, MCP install notes, and the SDK LLM guide link to Anthropic’s MCPB guide for the `.mcpb` flow.
- To build the same bundle yourself, run `**make mcpb`** with the official `mcpb` CLI on your `PATH`.

### Contributing

- GitHub issue templates for bug reports and feature requests.

---

## [1.2.7](https://github.com/Trenza1ore/GitCode-API/compare/1.2.6...1.2.7) — 2026-05-06

Changes since `1.2.6`…`1.2.7`.

### Feature

- **MCP server:** Built-in instructions and **help** responses so clients can learn how to use the tool before any GitCode API call.

### Fix

- **MCP / LLM tools:** Help and discovery responses work even when no API key is configured yet.

### Docs

- MCP setup notes for common IDEs and agents (including VS Code and Cursor).

---

## [1.2.6](https://github.com/Trenza1ore/GitCode-API/compare/1.2.5...1.2.6) — 2026-05-06

### Fix

- **Standalone CLI (`make binary`):** PyInstaller builds again bundle FastMCP correctly on Python **3.10+**, so the frozen `gitcode-api` binary can run MCP-related code paths when you use that workflow.

---

## [1.2.5](https://github.com/Trenza1ore/GitCode-API/compare/1.2.4...1.2.5) — 2026-05-06

Changes since `1.2.4`…`1.2.5`.

### Feature

- **LLM tools:** Optional OpenAI-style tool (`GitCodeOpenAITool`) and **MCP** server helpers for agents — install with `pip install 'gitcode-api[mcp]'` (FastMCP requires Python **3.10+**). Optional LLM pieces stay off the import path until you use them.

### Docs

- README and FAQ cover MCP and OpenAI tool usage; new SDK page documents both, shared tool behavior, and TLS notes. PyPI description highlights the CLI and LLM/MCP options.
- The docs build also publishes **EPUB** and **single-page HTML** alongside the main HTML site, for offline or single-file reading.
- PyPI project links include this changelog.

---

## [1.2.4](https://github.com/Trenza1ore/GitCode-API/compare/1.2.3...1.2.4) — 2026-05-01

### Fix

- **GitHub Release zips:** Each platform zip contains the standalone CLI, the bundled `.claude/` skill, and the root English and Chinese READMEs — no longer a stray `examples/README.md` inside the archive.

---

## [1.2.3](https://github.com/Trenza1ore/GitCode-API/compare/1.2.2...1.2.3) — 2026-05-01

### Feature

- **GitHub Releases:** CLI binaries ship as **versioned zips per platform** (`gitcode-api-<version>-<platform>.zip`) with predictable Linux, Windows, and macOS (Apple Silicon) builds (Python **3.12**), each bundling the CLI, skill tree, and root READMEs.

---

## [1.2.2](https://github.com/Trenza1ore/GitCode-API/compare/1.2.1...1.2.2) — 2026-05-01

Changes since `1.2.1`…`1.2.2`.

### Feature

- **Standalone CLI:** Build a single-file `gitcode-api` executable with `make binary` (output under `dist/`), using the documented PyInstaller setup.
- **GitHub Releases:** Published releases automatically attach matching CLI builds for Linux (x86_64), Windows (x86_64), and macOS (Apple Silicon).

### Docs

- Documentation explains how to build the standalone CLI and what each GitHub Release download contains.

---

## [1.2.1](https://github.com/Trenza1ore/GitCode-API/compare/1.2.0...1.2.1) — 2026-05-01

Changes since `1.2.0`…`1.2.1`.

### Feature

- `**AGENTS.md`:** In-repo guidance for AI-assisted work on this SDK.
- **Bundled skill:** Clearer GitCode API workflows for Cursor and similar tools; improved helper script for skill-driven CLI use.

### Docs

- Expanded CLI chapter in the docs; README quickstarts use simpler `with GitCode(...)` examples without extra `try`/`finally` noise.

---

## [1.2.0](https://github.com/Trenza1ore/GitCode-API/compare/1.1.3...1.2.0) — 2026-05-01

Changes since `1.1.3`…`1.2.0`.

### Feature

- **Discovery:** Resource namespaces expose `**methods`** (list callable API operations) and `**method_signature`** (inspect parameters and returns) for runtime introspection.
- **Example:** `examples/inspect_resource_group_methods.py` shows how to use those helpers.

### Fix

- **Client lifecycle:** Closing the SDK client and tearing down resource groups behaves consistently whether you rely on garbage collection or explicit shutdown.

### Docs

- CLI usage documented in the main docs site; REST “quickstart” page removed in favor of SDK-first navigation.
- `**pulls.create`:** Docstring clarified for fork-based pull requests.
- **Terminology:** Docs and bundled skill use **resource group** consistently.

---

## [1.1.3](https://github.com/Trenza1ore/GitCode-API/compare/1.1.2...1.1.3) — 2026-04-18

### Feature

- `**gitcode-api` CLI** (experimental): command-line access to SDK operations.

### Docs

- Installation examples use `pip install -U` for upgrades.

---

## [1.1.2](https://github.com/Trenza1ore/GitCode-API/compare/1.1.1...1.1.2) — 2026-04-16

### Feature

- **Bundled skill** for Cursor and other agents to follow GitCode API workflows from the editor.
- **Tokens:** Optional support for **encrypted** GitCode access tokens.

### Fix

- **Clients:** `GitCode` / `AsyncGitCode` always shut down the underlying HTTP client on close, including when you pass a custom `httpx` client.

### Docs

- Token encryption documented alongside the skill; docs site lists more project links.

---

## [1.1.1](https://github.com/Trenza1ore/GitCode-API/compare/1.1.0...1.1.1) — 2026-04-16

### Feature

- **Typing:** Richer annotations on response models and clients for better editor hints and static checking.

### Fix

- **Docs mirror:** Corrected the Organizations page in the mirrored REST reference.

### Style

- Examples favor straightforward attribute access on response objects.

---

## [1.1.0](https://github.com/Trenza1ore/GitCode-API/compare/v1.0.3...1.1.0) — 2026-04-16

Changes since `v1.0.3`…`1.1.0`.

### Feature

- **Examples:** Refreshed; `**python-dotenv` is no longer a required dependency** of the package (load env in your own app or examples as you prefer).

### Style

- Broader docstring coverage; consistent formatting with Ruff.

### Docs

- Documentation refresh; context manager usage for clients called out explicitly.

---

## [1.0.3](https://github.com/Trenza1ore/GitCode-API/compare/v1.0.2...v1.0.3) — 2026-04-16

### Chore

- PyPI metadata only: redundant license classifier removed.

---

## [1.0.2](https://github.com/Trenza1ore/GitCode-API/compare/v1.0.1...v1.0.2) — 2026-04-16

### Fix

- **Read the Docs:** Hosted documentation builds install and import `gitcode-api` correctly so API pages render as intended.

---

## [1.0.1](https://github.com/Trenza1ore/GitCode-API/compare/v1.0.0...v1.0.1) — 2026-04-16

### Fix

- **Example:** Commit-listing sample corrected.
- **Compatibility:** Python **3.9** support restored where it had broken.

### Docs

- README updates with the patch release.

---

## [1.0.0](https://github.com/Trenza1ore/GitCode-API/releases/tag/v1.0.0) — 2026-04-15

Initial published release on PyPI.

### Feature

- `**gitcode-api`:** First public Python SDK for the GitCode REST API, built on HTTPX with sync and async clients.

### Docs

- README and publishing metadata for the launch.

