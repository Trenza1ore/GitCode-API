# GitCode-API

![PyPI - Version](https://img.shields.io/pypi/v/gitcode-api) ![GitHub Badge](https://img.shields.io/badge/github-repo-blue?logo=github&link=https%3A%2F%2Fgithub.com%2FTrenza1ore%2FGitCode-API) ![GitCode Badge](https://img.shields.io/badge/gitcode-repo-brown?logo=gitcode&link=https%3A%2F%2Fgitcode.com%2FSushiNinja%2FGitCode-API) ![PyPI - License](https://img.shields.io/pypi/l/gitcode-api)

![Docs](https://img.shields.io/badge/%E6%96%87%E6%A1%A3-Docs-cyan?style=for-the-badge&logo=readthedocs&link=https%3A%2F%2Fgitcode-api.readthedocs.io%2Fen%2Flatest%2Findex.html) ![中文README](https://img.shields.io/badge/%E4%B8%AD%E6%96%87-README-brown?style=for-the-badge&logo=googledocs&link=README.zh.md) ![English README](https://img.shields.io/badge/English-README-blue?style=for-the-badge&logo=googledocs&link=README.md)

`gitcode-api` is a community-maintained Python SDK for the GitCode REST API. It provides easy-to-use synchronous and asynchronous clients, repository-scoped helpers, and lightweight response models so you can work with GitCode from Python without hand-writing raw HTTP requests.

## Why This Project

- Community project for developers who want a practical GitCode Python library.
- Sync and async clients with a consistent API surface.
- Resource namespaces such as `client.repos`, `client.pulls`, and `client.users`.
- Repository defaults via `owner=` and `repo=` on the client.
- Sphinx docs plus a mirrored GitCode REST API reference in `docs/`.

## Installation

Install from PyPI:

```bash
pip install gitcode-api
```

For local development from source:

```bash
uv sync
```

Install documentation dependencies:

```bash
uv sync --group docs
```

## Authentication

Pass `api_key=` directly, or set `GITCODE_ACCESS_TOKEN` in your environment:

```bash
export GITCODE_ACCESS_TOKEN="your-token"
```

## Quick Start

### Sync client

```python
from gitcode_api import GitCode

client = GitCode(
    owner="SushiNinja",
    repo="GitCode-API",
)

try:
    repo = client.repos.get()
    branches = client.branches.list(per_page=5)

    print(repo.full_name)
    for branch in branches:
        print(branch.name)
finally:
    client.close()
```

### Async client

```python
import asyncio

from gitcode_api import AsyncGitCode


async def main() -> None:
    client = AsyncGitCode(owner="SushiNinja", repo="GitCode-API")
    try:
        pulls = await client.pulls.list(state="open", per_page=20)
        print(len(pulls))
    finally:
        await client.close()


asyncio.run(main())
```

## Common Workflows

Create a pull request:

```python
from gitcode_api import GitCode

client = GitCode(owner="SushiNinja", repo="GitCode-API")

try:
    pull = client.pulls.create(
        title="Add feature",
        head="feature-branch",
        base="main",
        body="Implements the new flow.",
    )
    print(pull.number)
finally:
    client.close()
```

Get the authenticated user:

```python
from gitcode_api import GitCode

client = GitCode()

try:
    user = client.users.me()
    print(user.login)
finally:
    client.close()
```

Search repositories:

```python
from gitcode_api import GitCode

client = GitCode()

try:
    repos = client.search.repositories(q="sdk language:python", per_page=10)
    for repo in repos:
        print(repo.full_name)
finally:
    client.close()
```

## Available Resources

Both `GitCode` and `AsyncGitCode` expose:

- `repos` and `contents`
- `branches` and `commits`
- `issues` and `pulls`
- `labels`, `milestones`, and `members`
- `releases`, `tags`, and `webhooks`
- `users`, `orgs`, `search`, and `oauth`

## Examples

Runnable examples live in `examples/`:

- `get_current_user.py`
- `get_repository_overview.py`
- `list_pull_requests.py`
- `async_list_branches.py`

Example scripts load shared configuration from `examples/.env` using `python-dotenv`.

```bash
uv run python examples/get_current_user.py
uv run python examples/get_repository_overview.py
uv run python examples/list_pull_requests.py
uv run python examples/async_list_branches.py
```

See `examples/.env.example` for the expected variables.

## Documentation

- Project docs entry: `docs/index.rst`
- SDK docs: `docs/sdk/index.rst`
- REST API mirror: `docs/rest_api/index.rst`

Build the docs locally with Sphinx:

```bash
uv run --group docs sphinx-build -b html docs docs/_build/html
```

## Project Status

This is a community project and is still evolving. API coverage is already broad, but some endpoints and behaviors may continue to be refined as the SDK grows.

## Contributing

Issues, bug reports, API coverage improvements, docs fixes, and pull requests are welcome. If you are using GitCode heavily and notice missing endpoints or awkward ergonomics, contributions are especially appreciated.
