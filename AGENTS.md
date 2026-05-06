# AGENTS.md

Guidance for AI agents working in this repository.

## Project Overview

`gitcode-api` is a community-maintained Python SDK for the GitCode REST API. It exposes synchronous and asynchronous `httpx` clients, resource-oriented helpers such as `client.repos` and `client.pulls`, lightweight response models, a small CLI, examples, and Sphinx documentation. Optional **LLM / agent** helpers live under `gitcode_api.llm` (OpenAI Chat Completions tool shape, MCP via FastMCP) with lazy imports so the core install stays light.

Primary source paths:

- `gitcode_api/`: package source.
- `gitcode_api/_client.py`: top-level `GitCode` and `AsyncGitCode` clients.
- `gitcode_api/_base_client.py`: shared transport, auth, URL building, payload cleanup, response parsing, and context-manager behavior.
- `gitcode_api/_base_resource.py`: shared resource introspection (`methods`, `method_signature`).
- `gitcode_api/resources/`: sync and async REST resource groups.
- `gitcode_api/_models.py`: dictionary-backed response models and typed parameter payloads.
- `gitcode_api/llm/`: optional adapters — `GitCodeOpenAITool`, `GitCodeMCP`, `create_mcp_*` / `register_mcp_*` / `create_mcp_server`; shared logic in `gitcode_api/llm/_tool.py` (`GitCodeLLMTool`). Public names load lazily through `gitcode_api.llm.__getattr__`.
- `gitcode_api/cli.py`: installed CLI entry point, exposed as `gitcode-api`.
- `tests/`: unit tests and docs-backed endpoint/response checks.
- `docs/`: Sphinx documentation.
- `examples/`: runnable examples that read configuration from `examples/.env`.

Ignore generated or build output as source of truth, especially `build/`, `dist/`, `docs/_build/`, `docs/_downloads/`, and `docs/sdk/generated/`.

## Tooling And Commands

Use `uv` from the repository root.

- Install/sync development dependencies: `uv sync --all-groups`.
- Run tests: `uv run pytest` or `make test`.
- Run a focused test: `uv run pytest tests/test_client.py -k context_manager`.
- Format and fix imports: `make format`.
- Type-check the package: `make lint` (`mypy -p gitcode_api`).
- Check docstrings: `make docstring`.
- Build docs: `make docs`.
- Clean docs build artifacts: `make docs-clean`.
- Build a standalone CLI binary (PyInstaller one-file): `make binary` (uses dependency group `binary`; output under `dist/`).

The `Makefile` currently defines:

- `docs`: removes old docs build/generated SDK files, then runs Sphinx (`html`, `epub`, and `singlehtml` into `docs/_build/{html,epub,singlehtml}/`).
- `format`: runs Ruff fixes, import sorting, and formatting. The commands are allowed to continue on failure because they use `|| true`; inspect output if formatting matters.
- `lint`: runs mypy against `gitcode_api` (`uv run mypy -p gitcode_api`).
- `test`: installs the package into the active uv environment, then runs pytest.
- `docstring`: runs `pydocstyle` against `gitcode_api/` to check PEP 257/reST-style docstrings.
- `release`: bumps `gitcode_api/version.txt`, `pyproject.toml`, locks, commits, tags, and pushes. Do not run it unless the user explicitly asks for a release.
- `binary`: runs PyInstaller from `gitcode-api.spec`; produces `dist/gitcode-api` (Unix) or `dist/gitcode-api.exe` (Windows). Build on each target OS; the binary embeds the Python used to build it. On GitHub Release publish, `release-binaries.yml` builds those platforms and uploads a zip per runner (binary, `.claude/`, `README.md`, `README.zh.md`) via `scripts/package_release_zip.py`.

Project metadata and tool configuration live in `pyproject.toml`:

- Python support is `>=3.9,<4`.
- Runtime dependency is intentionally small: `httpx`.
- Optional extra `[mcp]` installs FastMCP on **Python 3.10+** only (`python_version >= '3.10'` marker in metadata). The uv `mcp` dependency group mirrors that; `docs` and `binary` groups include `mcp` so docs builds and PyInstaller bundles resolve MCP-related imports.
- Test/docs/format/binary (frozen CLI) dependencies are uv dependency groups.
- Ruff line length is 120 and target version is Python 3.9.
- Pydocstyle convention is `pep257`.
- `uv.lock` is intentionally tracked.

## Coding Conventions

Follow the existing style before introducing new abstractions.

- Keep Python compatible with 3.9.
- Prefer explicit `typing` imports such as `Optional`, `Union`, `List`, and `Dict` where the surrounding code uses them.
- Keep line length at or below 120.
- Use keyword-only resource method parameters for public SDK methods.
- Drop `None` from query params and form data by passing dictionaries through the existing client/resource helpers rather than ad hoc filtering.
- Keep sync and async resource surfaces aligned when adding endpoints.
- Return typed `APIObject` subclasses or lists of them via `_model(...)` / `_models(...)` where possible.
- Use `raw=True` only for endpoints that intentionally return bytes.
- Prefer context managers in examples: `with GitCode(...) as client:` and `async with AsyncGitCode(...) as client:`.
- Keep authentication behavior centered on `api_key=`, `GITCODE_ACCESS_TOKEN`, and optional `decrypt=`.
- Do not add network calls to unit tests; use `httpx.MockTransport`.
- Keep `gitcode_api` passing `make lint` when changing public types or resource surfaces.
- For `gitcode_api.llm`, preserve lazy loading via `llm/__getattr__` rather than importing FastMCP or heavy helpers at package import time.

## Docstrings

Use concise PEP 257 docstrings with reStructuredText fields, matching the current codebase:

```python
def get(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> Repository:
    """Get a repository.

    :param owner: Repository owner path. Uses the client default when omitted.
    :param repo: Repository name. Uses the client default when omitted.
    :returns: Repository metadata.
    """
```

Module docstrings should briefly explain the module purpose. Class docstrings should describe the public role and list constructor parameters with `:param`. Public resource methods should document parameters and returns. Avoid noisy docstrings on trivial internal helpers unless they clarify behavior.

Run `make docstring` after changing package docstrings to verify they conform to the project's PEP 257/reStructuredText style.

## Tests

Tests use pytest, pytest-asyncio, and `httpx.MockTransport`.

- Shared test client factories are in `tests/conftest.py`.
- Async tests use `@pytest.mark.asyncio`.
- Keep tests deterministic and offline.
- When adding a resource method, cover request method/path, query params or payload cleanup, response model coercion, and async parity when applicable.
- LLM adapter behavior is covered in `tests/test_llm_tools.py` (OpenAI tool schema, sync/async invocation, MCP registration); CLI MCP wiring is partially covered in `tests/test_cli.py`.
- Docs-backed REST checks live under `tests/restful_docs_examples/`; update them when SDK methods are meant to mirror documented REST examples.

## Documentation

The documentation is a Sphinx project under `docs/`.

- `docs/conf.py` enables `sphinx.ext.autodoc`, `autosummary`, `intersphinx`, and `myst_parser`.
- `docs/index.rst` is the main entry point.
- SDK docs are under `docs/sdk/`, including `docs/sdk/llm_tools.rst` for OpenAI tools, MCP / FastMCP, `GitCodeLLMTool`, and TLS notes.
- REST API mirror docs are under `docs/rest_api/`.
- `docs/changelog.md` includes the root `CHANGELOG.md` through MyST.
- Read the Docs builds from `.readthedocs.yaml` using Python 3.11 and `docs/requirements.txt`.

Use reStructuredText for existing `.rst` pages. Use MyST Markdown only where the file is already Markdown. Build locally with `make docs` after nontrivial docs changes.

The REST API reference is mirrored from GitCode Help documentation. Broad refreshes should go through `scripts/build_gitcode_sphinx_docs.py`, which requires `pandoc` and downloads upstream pages. Generated REST pages include a footer that says not to edit by hand; avoid hand-editing those pages except for small, user-requested fixes.

## Examples And CLI

Examples live in `examples/` and load local configuration from `examples/.env` using variables shown in `examples/.env.example`. Never commit real tokens or generated `.env` files.

The package CLI is available as:

- `gitcode-api ...`
- `python -m gitcode_api ...`

Commands mirror synchronous `GitCode` resource methods with the pattern `gitcode-api <resource> <method> ...`, where `<resource>` is the same name as on the client (kebab-cased in the CLI). The top-level `gitcode-api serve` command starts the bundled FastMCP server (requires the `mcp` extra / FastMCP on Python 3.10+). Extra `**params` or `**payload` values can be passed with repeated `--set key=value` flags or `--set-json '{"key": "value"}'`.

The `.claude/skills/gitcode-api/` directory is a packaged agent skill for using this SDK from external agents. Its `scripts/gitcode_api_cli.py` is a legacy helper and explicitly deprecated in favor of the package CLI.

## Release And Publishing Notes

Version information is stored in both `pyproject.toml` and `gitcode_api/version.txt`. Releases are published to PyPI by `.github/workflows/python-publish.yml` when a GitHub Release is published, using trusted publishing.

For pre-release changelog sections, use the title format `## [next-version](https://github.com/Trenza1ore/GitCode-API/compare/previous-version...main) — Unreleased`, for example `## [1.2.1](https://github.com/Trenza1ore/GitCode-API/compare/1.2.0...main) — Unreleased`. Released sections use the same compare-link style but end with the release date, such as `— 2026-05-01`.

Do not create tags, push, publish, or run `make release` unless the user explicitly requests it. If changing release notes or changelogs, keep `CHANGELOG.md`, `docs/changelog.md`, and any release note files consistent with the requested version.

## Git commit messages

Use this convention only when the user **explicitly** asks for a commit (for example, they say to commit, stage, or write a commit message). Do not invent commits otherwise. And never add tags or push unless **explicitly asked and confirmed**.

Template (scope can be omitted):

`<type>(<scope>): <subject>`

Types:

- `feat`: (new feature for the user, not a new feature for build script)
- `fix`: (bug fix for the user, not a fix to a build script)
- `docs`: (changes to the documentation)
- `style`: (formatting, missing semi colons, etc; no production code change)
- `refactor`: (refactoring production code, eg. renaming a variable)
- `test`: (adding missing tests, refactoring tests; no production code change)
- `chore`: (updating grunt tasks etc; no production code change)

## Safety Notes

- The working tree may contain user changes. Do not revert unrelated edits.
- Do not commit secrets such as `GITCODE_ACCESS_TOKEN`, `.env`, `.pypirc`, or credentials.
- Prefer focused changes with matching tests and docs updates when public SDK behavior changes.
- Do not treat `build/lib/` as editable source.
