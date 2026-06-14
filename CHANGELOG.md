# Changelog

All notable changes to this project are documented here. Release ranges link to the GitHub compare view. Tag names follow the repository (`v1.0.x` through `v1.0.3`, then `1.1.0` onward).

## [1.3.2](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.3.2) — 2026-06-14

Changes since `1.3.1`…`1.3.2`.

### Feature

- **Explicit query parameters on listing methods:** 11 "list" methods that previously accepted only `**params` now expose some documented query parameters as named keyword arguments — `pulls.list`, `pulls.list_operation_logs`, `pulls.list_enterprise`, `pulls.list_org`, `issues.list_enterprise`, `issues.list_user`, `issues.list_org`, `issues.list_enterprise_comments`, `milestones.list`, `users.list_repos`, and `repos.get_download_statistics`. A trailing `**kwargs` preserves backward compatibility for any extra or undocumented parameters.

---

## [1.3.1](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.3.1) — 2026-06-12

Changes since `1.3.0`…`1.3.1`.

### Feature

- **Issue creation `template_path`:** `client.issues.create` now accepts an optional `template_path` parameter, potentially letting you use a repository issue template. *However, GitCode doesn't seem to set it up correctly...*

### Docs

- **Copy button on code blocks:** documentation code blocks now include a one-click copy button (Sphinx `copybutton` extension).

---

## [1.3.0](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.3.0) — 2026-06-08

Changes since `1.2.21`…`1.3.0`.

### Feature

- **Public `models` and `exceptions` modules:** response models and exception classes are now importable from `gitcode_api.models` and `gitcode_api.exceptions` respectively, giving users a stable, documented import path instead of reaching into private `_models` / `_exceptions` internals.

### Refactor

- **Resource sub-packages:** the `resources/account.py`, `resources/collaboration.py`, `resources/misc.py`, and `resources/repositories.py` files have been split (e.g. `resources/collaboration/pulls_resource_group.py`). The public client API (`client.pulls`, `client.issues`, etc.) is unchanged.
- **Docstrings on ABCs:** resource method documentation now lives on abstract base classes, avoiding de-synchronization.

---

## [1.2.21](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.21) — 2026-06-04

Changes since `1.2.20`…`1.2.21`.

### Feature

- **Authentication errors:** 401 responses now raise `GitCodeUnauthorizedError` (a subclass of `GitCodeHTTPStatusError`), and token-related 401s raise the more specific `GitCodeTokenError`, making it easier to catch and handle expired or invalid tokens without inspecting status codes manually.

### Fix

- **CI workflow:** corrected a duplicate step name in the `check-code` workflow and renamed the workflow from "Code format" to "CI".

### Docs

- **README badges:** added a CI status badge to both `README.md` and `README.zh.md`.

---

## [1.2.20](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.20) — 2026-05-27

Changes since `1.2.19`…`1.2.20`.

### Feature

- **Issue and pull request templates:** `get_template` methods for fetching issue and pull request templates now accept `encoding` (default to `"utf-8"`) and optional `decoding_kwargs` forwarded to `bytes.decode`, so non-UTF-8 template files can be read with the codec and error handling of your choice!

### Fix

- **Async client method signatures:** several async methods that previously took a catch-all `**params` or `**payload` as input now use the same keyword arguments as their sync counterparts.

### GitHub Action

- **check-code:** new workflow that runs on push & PR, checking code style (via `ruff`) and ensuring all unit tests pass.

---

## [1.2.19](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.19) — 2026-05-18

Changes since `1.2.18`…`1.2.19`.

### Feature

- **Issue and pull request templates (for GitHub mirror repos):** `list_templates` method now also walk each candidate repository's `.github/` directory as well, so we can support GitHub-mirrored projects that keep `ISSUE_TEMPLATE`* and `PULL_REQUEST_TEMPLATE*` files under `.github/` instead of `.gitcode/`.

### Refactor

- **gitcode_api.constants:** move `GITCODE_ISSUE_TEMPLATE_PATH_RE` and `GITCODE_PULL_REQUEST_TEMPLATE_PATH_RE` to `gitcode_api.constants`, and add `GITCODE_TEMPLATE_REPO`; path patterns match both `.gitcode/` and `.github/` template locations.

### Docs

- **SDK client API:** Template resolution notes describe `.github/` support for GitHub-mirrored repositories.

---

## [1.2.18](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.18) — 2026-05-18

Changes since `1.2.17`…`1.2.18`.

### Feature

- **Decrypt at request headers construction:** Provided GitCode API token is now decrypted at request headers contruction instead of at client constructor due to security concerns, constructor will merely validate it produces a `str` as output.
- **Version metadata (source checkout):** Improved logic for resolving `__version_`_ and `__build_hash__` in local development environment.

### Fix

- **Typing:** `py.typed` is now an empty PEP 561 marker as one would expect.

### Examples

- **examples/sync_github_release_to_gitcode.py:** Filters release assets by filename pattern, adds tqdm descriptions and clearer status output for create/skip/upload paths.

---

## [1.2.17](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.17) — 2026-05-15

Changes since `1.2.16`…`1.2.17`.

### Feature

- **Version metadata:** `__version_`_ is taken from the installed distribution (`importlib.metadata`), and a new `__build_hash__` value is exposed for telling builds apart. `gitcode-api --version` and the no-argument welcome banner include the build id; the banner also prints **Home Page** and **Docs** links (homepage URL comes from package **Project-URL** metadata when present).
- **gitcode_api.constants:** New documented module with the default API base URL, HTTP timeout, and the `GITCODE_ACCESS_TOKEN` / `GITCODE_CA_BUNDLE` environment names used by the client.

### Fix

- **Packaging:** Wheel/sdist installs now ship `py.typed` via setuptools `package-data`, so type checkers can honor inline typing for the package.

### Docs

- **SDK reference HTML:** After each docs build, `scripts/docs_rename_resource_methods.py` rewrites generated **autosummary** method labels on the client API page so grouped resource methods read with clearer names; Read the Docs runs this step in its build.

### Examples

- **examples/sync_github_release_to_gitcode.py:** Reworked for clearer flow and alignment with current release upload behavior.

---

## [1.2.16](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.16) — 2026-05-13

Changes since `1.2.15`…`1.2.16`.

### Feature

- **Default CA Bundle:** When the internal `GitCode` client builds its own `httpx` client (you do not pass `http_client`), verification uses the path from `GITCODE_CA_BUNDLE` if set, otherwise `REQUESTS_CA_BUNDLE` if set (same convention as many Python HTTP stacks), otherwise the default CA bundle is used. Applies to both `GitCode` and `AsyncGitCode`.

---

## [1.2.15](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.15) — 2026-05-13

Changes since `1.2.14`…`1.2.15`.

### Typing

- **openJiuwen adapter (`gitcode_api.llm.jiuwen`):** Silence mypy `import-untyped` on the `TYPE_CHECKING` import of `LocalFunction` from optional `openjiuwen` (no runtime or public API change). Now we fully pass `mypy` checks!

---

## [1.2.14](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.14) — 2026-05-13

Changes since `1.2.13`…`1.2.14`.

### Feature

- **Issue and pull request templates:** `client.issues` / `client.pulls` (and async counterparts) now expose `list_templates` and `get_template` for GitCode’s `.gitcode/` issue and PR template files on the default branch, including metadata (`RepositoryGitCodeTemplate` with path, SHA, and resolved `template_owner` / `template_repo`). GitCode does not expose this as a dedicated REST “list/get templates” API, so the SDK composes the behavior from repository content calls with **custom resolution logic** (active template paths, default branch, and upstream template sources). The CLI picks these up automatically as `issues list-templates`, `issues get-template`, `pulls list-templates`, and `pulls get-template`.
- **as_dict:** Top-level helper to turn one `APIObject` (or a list of them) into plain `dict` values via `to_dict`, with an optional `deep_copy` flag for isolated mappings.
- **Repository model:** Responses can include a `parent` field describing the upstream source repository when the API returns it.

### Refactor

- **Models:** Dropped unused legacy `TypedDict` definitions from `gitcode_api._models` (no public API change).

### Docs

- Homepage and REST API index: added a short “Why this project” section and clarified that the REST mirror is based on GitCode Help material but **manually corrected and extended** in this repo.
- README and SDK docs updated for template listing/fetching; runnable examples under `examples/` for issue and pull request templates.

---

## [1.2.13](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.13) — 2026-05-12

Changes since `1.2.12`…`1.2.13`.

### Feature

- **Releases (`client.releases` / async parity):** Reworked to match the current GitCode API — `create`, tag-based `update`, `list` with `direction` / `page` / `per_page`, `get` / `get_by_tag` / `get_latest` with documented query options, `get_upload_url` and `upload` (input bytes or local file path) for attachments, and `download_attachment` for raw bytes.
- **Models:** `Release` now exposes `assets` and `release_status`; upload URL responses use `ReleaseUploadURL`.

### Breaking Change

- **GitCode.releases.update:** Targets a release by **tag in the URL path** (`tag=…`) instead of `release_id`; the JSON body is `name`, `body`, and optional `release_status` only (no `tag_name` in the payload). Update any code that still passed `release_id` or relied on the old request shape.

### Docs

- REST API mirror: release create/upload and related pages, missing release topics, and table cleanup; SDK release documentation updated for the new methods and parameters.
- Added example `examples/sync_github_release_to_gitcode.py`.

---

## [1.2.12](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.12) — 2026-05-11

Changes since `1.2.11`…`1.2.12`.

### Feature

- **CLI:** `-e` / `--escape` takes a string of `\`-style escape sequences (for example `"\n\t"`) to un-escape, which makes multiline payloads easier for human users (e.g. `gitcode-api pulls create ... --body 'Line1\nLine2' -e '\n'`).
- **CLI:** The shared cli argument parser no longer passes `--owner` / `--repo` into the `GitCode` client constructor. Use each method’s own flags so defaults match the SDK method signatures.
- **CLI (`gitcode-api serve`):** `--show-banner` / `-b` accepts `true` or `false` and forwards to FastMCP’s `run(show_banner=…)`; omit it to keep the library default.
- **CLI (`gitcode-api serve`):** `--transport` is validated against `stdio`, `http`, and `sse`.

### Docs

- Added a homepage for this project: [https://hugohuang.com/gitcode-api](https://hugohuang.com/gitcode-api)
- README, SDK CLI page (`docs/sdk/cli.rst`), `install_mcp_server.md`, and PyPI homepage links updated for the new CLI and MCP options.
- Download stat & PyPI version badges now are mutated automatically per-release to suit GitCode's image-caching strategy for `README.md`.

---

## [1.2.11](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.11) — 2026-05-07

Changes since `1.2.10`…`1.2.11`.

### Feature

- **gitcode_api.llm:** `GitCodeLLMTool` is eagerly imported and exposed in namespace, easier for custom adapters, MCP wiring, and static analysis.
- **LLM adapters (OpenAI, openJiuwen):** `GitCodeOpenAITool`, `create_openjiuwen_gitcode_api_tool`, and the openJiuwen binding use explicit keyword parameters for GitCode clients (`client`, `async_client`, `api_key`, `base_url`, `timeout`, `decrypt`, `owner`, `repo`) instead of a `**kwargs` catch-all — clearer signatures, better editor hints, and the same ordering as `GitCodeLLMTool`.

### Docs

- README and SDK LLM guide use consistent “unified tool” wording for `gitcode_api_tool`.
- Changelog section titles point at GitHub release pages; markdown structure cleaned up.

### File Layout Improvement

- PyInstaller spec moved to `scripts/gitcode-api.spec`; `make binary` and the release-binaries workflow call that path (repo root stays simpler).
- `scripts/build_manifest.py` emits a transient `.mcpbignore` for MCP bundle packing; tracked top-level `.mcpbignore` was removed — `make mcpb` still removes generated artifacts afterward.

---

## [1.2.10](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.10) — 2026-05-07

Changes since `1.2.9`…`1.2.10`.

### Feature

- **OpenAI tool (`GitCodeOpenAITool`):** Invocation results are now **JSON strings** (`str`) from `json.dumps` with `ensure_ascii=False`, so payloads fit Chat Completions **tool** message `content` without extra serialization. `indent` controls formatting (default `2`; pass `None` for compact single-line JSON).
- **OpenAI tool constructor:** `async_mode` defaults to `False`. Use `async_mode=True` and `await` the coroutine returned from the instance — the `async` keyword alias for async mode is no longer accepted on `GitCodeOpenAITool`.

### Docs

- README (English and Chinese), SDK LLM guide, and new runnable example `examples/openai_tool_call.py` updated for string tool results and a multi-turn Chat Completions loop.

---

## [1.2.9](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.9) — 2026-05-07

Changes since `1.2.8`…`1.2.9`.

### Feature

- **LLM tools:** Optional [openJiuwen](https://openjiuwen.com) integration — install `openjiuwen` (Python **3.11+**), then use `create_openjiuwen_gitcode_api_tool` from `gitcode_api.llm` with the same GitCode tool contract as the OpenAI and MCP adapters.

### Docs

- README (English and Chinese), SDK LLM guide, and PyPI description updated for openJiuwen.

---

## [1.2.8](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.8) — 2026-05-07

Changes since `1.2.7`…`1.2.8`.

### Feature

- **Claude Desktop:** Install the GitCode MCP server as an [MCPB](https://claude.com/docs/connectors/building/mcpb) bundle; each GitHub Release ships a matching `gitcode-<version>.mcpb` you can add in Claude Desktop.

### Docs

- README, MCP install notes, and the SDK LLM guide link to Anthropic’s MCPB guide for the `.mcpb` flow.
- To build the same bundle yourself, run `make mcpb` with the official `mcpb` CLI on your `PATH`.

### Contributing

- GitHub issue templates for bug reports and feature requests.

---

## [1.2.7](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.7) — 2026-05-06

Changes since `1.2.6`…`1.2.7`.

### Feature

- **MCP server:** Built-in instructions and **help** responses so clients can learn how to use the tool before any GitCode API call.

### Fix

- **MCP / LLM tools:** Help and discovery responses work even when no API key is configured yet.

### Docs

- MCP setup notes for common IDEs and agents (including VS Code and Cursor).

---

## [1.2.6](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.6) — 2026-05-06

### Fix

- **Standalone CLI (`make binary`):** PyInstaller builds again bundle FastMCP correctly on Python **3.10+**, so the frozen `gitcode-api` binary can run MCP-related code paths when you use that workflow.

---

## [1.2.5](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.5) — 2026-05-06

Changes since `1.2.4`…`1.2.5`.

### Feature

- **LLM tools:** Optional OpenAI-style tool (`GitCodeOpenAITool`) and **MCP** server helpers for agents — install with `pip install 'gitcode-api[mcp]'` (FastMCP requires Python **3.10+**). Optional LLM pieces stay off the import path until you use them.

### Docs

- README and FAQ cover MCP and OpenAI tool usage; new SDK page documents both, shared tool behavior, and TLS notes. PyPI description highlights the CLI and LLM/MCP options.
- The docs build also publishes **EPUB** and **single-page HTML** alongside the main HTML site, for offline or single-file reading.
- PyPI project links include this changelog.

---

## [1.2.4](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.4) — 2026-05-01

### Fix

- **GitHub Release zips:** Each platform zip contains the standalone CLI, the bundled `.claude/` skill, and the root English and Chinese READMEs — no longer a stray `examples/README.md` inside the archive.

---

## [1.2.3](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.3) — 2026-05-01

### Feature

- **GitHub Releases:** CLI binaries ship as **versioned zips per platform** (`gitcode-api-<version>-<platform>.zip`) with predictable Linux, Windows, and macOS (Apple Silicon) builds (Python **3.12**), each bundling the CLI, skill tree, and root READMEs.

---

## [1.2.2](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.2) — 2026-05-01

Changes since `1.2.1`…`1.2.2`.

### Feature

- **Standalone CLI:** Build a single-file `gitcode-api` executable with `make binary` (output under `dist/`), using the documented PyInstaller setup.
- **GitHub Releases:** Published releases automatically attach matching CLI builds for Linux (x86_64), Windows (x86_64), and macOS (Apple Silicon).

### Docs

- Documentation explains how to build the standalone CLI and what each GitHub Release download contains.

---

## [1.2.1](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.1) — 2026-05-01

Changes since `1.2.0`…`1.2.1`.

### Feature

- `AGENTS.md`: In-repo guidance for AI-assisted work on this SDK.
- **Bundled skill:** Clearer GitCode API workflows for Cursor and similar tools; improved helper script for skill-driven CLI use.

### Docs

- Expanded CLI chapter in the docs; README quickstarts use simpler `with GitCode(...)` examples without extra `try`/`finally` noise.

---

## [1.2.0](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.2.0) — 2026-05-01

Changes since `1.1.3`…`1.2.0`.

### Feature

- **Discovery:** Resource namespaces expose `methods` (list callable API operations) and `method_signature` (inspect parameters and returns) for runtime introspection.
- **Example:** `examples/inspect_resource_group_methods.py` shows how to use those helpers.

### Fix

- **Client lifecycle:** Closing the SDK client and tearing down resource groups behaves consistently whether you rely on garbage collection or explicit shutdown.

### Docs

- CLI usage documented in the main docs site; REST “quickstart” page removed in favor of SDK-first navigation.
- `pulls.create`: Docstring clarified for fork-based pull requests.
- **Terminology:** Docs and bundled skill use **resource group** consistently.

---

## [1.1.3](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.1.3) — 2026-04-18

### Feature

- `gitcode-api CLI` (experimental): command-line access to SDK operations.

### Docs

- Installation examples use `pip install -U` for upgrades.

---

## [1.1.2](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.1.2) — 2026-04-16

### Feature

- **Bundled skill** for Cursor and other agents to follow GitCode API workflows from the editor.
- **Tokens:** Optional support for **encrypted** GitCode access tokens.

### Fix

- **Clients:** `GitCode` / `AsyncGitCode` always shut down the underlying HTTP client on close, including when you pass a custom `httpx` client.

### Docs

- Token encryption documented alongside the skill; docs site lists more project links.

---

## [1.1.1](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.1.1) — 2026-04-16

### Feature

- **Typing:** Richer annotations on response models and clients for better editor hints and static checking.

### Fix

- **Docs mirror:** Corrected the Organizations page in the mirrored REST reference.

### Style

- Examples favor straightforward attribute access on response objects.

---

## [1.1.0](https://github.com/Trenza1ore/GitCode-API/releases/tag/1.1.0) — 2026-04-16

Changes since `v1.0.3`…`1.1.0`.

### Feature

- **Examples:** Refreshed; `python-dotenv` is no longer a required dependency of the package (load env in your own app or examples as you prefer).

### Style

- Broader docstring coverage; consistent formatting with Ruff.

### Docs

- Documentation refresh; context manager usage for clients called out explicitly.

---

## [1.0.3](https://github.com/Trenza1ore/GitCode-API/releases/tag/v1.0.3) — 2026-04-16

### Chore

- PyPI metadata only: redundant license classifier removed.

---

## [1.0.2](https://github.com/Trenza1ore/GitCode-API/releases/tag/v1.0.2) — 2026-04-16

### Fix

- **Read the Docs:** Hosted documentation builds install and import `gitcode-api` correctly so API pages render as intended.

---

## [1.0.1](https://github.com/Trenza1ore/GitCode-API/releases/tag/v1.0.1) — 2026-04-16

### Fix

- **Example:** Commit-listing sample corrected.
- **Compatibility:** Python **3.9** support restored where it had broken.

### Docs

- README updates with the patch release.

---

## [1.0.0](https://github.com/Trenza1ore/GitCode-API/releases/tag/v1.0.0) — 2026-04-15

Initial published release on PyPI.

### Feature

- `gitcode-api`: First public Python SDK for the GitCode REST API, built on HTTPX with sync and async clients.

### Docs

- README and publishing metadata for the launch.

