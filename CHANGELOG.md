# Changelog

All notable changes to this project are documented here. Release ranges link to the GitHub compare view. Tag names follow the repository (`v1.0.x` through `v1.0.3`, then `1.1.0` onward).

## [1.2.1](https://github.com/Trenza1ore/GitCode-API/compare/1.2.0...main) — Unreleased

### Feature

- Improved the bundled GitCode API skill: tighter workflow patterns, SKILL updates, and enhancements to the skill’s `gitcode_api_cli` helper script.

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
