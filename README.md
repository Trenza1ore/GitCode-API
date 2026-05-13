# GitCode-API

[![PyPI - Version](https://img.shields.io/pypi/v/gitcode-api?link=https%3A%2F%2Fpypi.org%2Fproject%2Fgitcode-api%2F&uuid=1d56ca66edb448b88c30fbfd677b8542)](https://pypi.org/project/gitcode-api) [![PyPI Downloads](https://static.pepy.tech/personalized-badge/gitcode-api?period=total&units=INTERNATIONAL_SYSTEM&left_color=GRAY&right_color=RED&left_text=downloads&uuid=03b2f61f19894ce49501bb9e856b434a)](https://pepy.tech/projects/gitcode-api) [![CodeFactor](https://www.codefactor.io/repository/github/trenza1ore/gitcode-api/badge)](https://www.codefactor.io/repository/github/trenza1ore/gitcode-api)
[![Install in Cursor](https://img.shields.io/badge/Install_in-Cursor-000000?logoColor=white)](https://cursor.com/en/install-mcp?name=GitCode%20API&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJnaXRjb2RlLWFwaVttY3BdIiwiZ2l0Y29kZS1hcGkiLCJzZXJ2ZSJdLCJlbnYiOnsiR0lUQ09ERV9BQ0NFU1NfVE9LRU4iOiIke2lucHV0OmdpdGNvZGVfYWNjZXNzX3Rva2VufSJ9LCJpbnB1dHMiOlt7ImlkIjoiZ2l0Y29kZV9hY2Nlc3NfdG9rZW4iLCJ0eXBlIjoicHJvbXB0U3RyaW5nIiwiZGVzY3JpcHRpb24iOiJFbnRlciBHSVRDT0RFX0FDQ0VTU19UT0tFTiIsInBhc3N3b3JkIjp0cnVlfV19) [![Install in VS Code](https://img.shields.io/badge/Install_in-VS_Code-0098FF?logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=GitCode%20API&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--from%22%2C%22gitcode-api%5Bmcp%5D%22%2C%22gitcode-api%22%2C%22serve%22%5D%2C%22env%22%3A%7B%22GITCODE_ACCESS_TOKEN%22%3A%22%24%7Binput%3Agitcode_access_token%7D%22%7D%2C%22inputs%22%3A%5B%7B%22id%22%3A%22gitcode_access_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Enter%20GITCODE_ACCESS_TOKEN%22%2C%22password%22%3Atrue%7D%5D%7D)
[![GitHub Badge](https://img.shields.io/badge/github-repo-blue?logo=github&link=https%3A%2F%2Fgithub.com%2FTrenza1ore%2FGitCode-API)](https://github.com/Trenza1ore/GitCode-API) [![GitCode Badge](https://img.shields.io/badge/gitcode-repo-brown?logo=gitcode&link=https%3A%2F%2Fgitcode.com%2FSushiNinja%2FGitCode-API)](https://gitcode.com/SushiNinja/GitCode-API)

[![Docs](https://img.shields.io/badge/%E6%96%87%E6%A1%A3-Docs-cyan?style=for-the-badge&logo=readthedocs&link=https%3A%2F%2Fgitcode-api.readthedocs.io%2Fen%2Flatest%2Findex.html)](https://gitcode-api.readthedocs.io) [![中文README](https://img.shields.io/badge/%E4%B8%AD%E6%96%87-README-brown?style=for-the-badge&logo=googledocs&link=README.zh.md)](README.zh.md)

`gitcode-api` is a community-maintained Python SDK for the GitCode REST API. It provides easy-to-use synchronous and asynchronous clients, repository-scoped helpers, and lightweight response models so you can work with GitCode from Python without hand-writing raw HTTP requests. The `gitcode_api.llm` module adds an OpenAI-style function tool, an MCP service, and an [openJiuwen](https://openjiuwen.com) tool integration so agents can reuse the same resource-oriented API.

## Why This Project

- Community project for developers who want a practical GitCode Python library.
- Sync and async clients with a consistent API surface.
- Convenient methods not offered by REST API directly: such as fetching Issue and PR templates.
- Resource groups such as `client.repos`, `client.pulls`, and `client.users`.
- Repository defaults via `owner=` and `repo=` on the client.
- Sphinx docs plus a mirrored GitCode REST API reference in `docs/`.
- Provides MCP server, OpenAI tool, and [openJiuwen](https://openjiuwen.com) tool for LLM agent usage.
- Provide MCP service that directly installs to your IDE of choice, such as Cursor and VS Code!
- Provides an [mcpb bundle](https://www.anthropic.com/engineering/desktop-extensions) you can install directly in the Claude desktop app; download it from [Release](https://github.com/Trenza1ore/GitCode-API/releases/latest).

## Installation

Install from PyPI:

```bash
pip install -U gitcode-api
```

Install the MCP server to your AI-powered IDE of choice:

[![Install in Cursor](https://img.shields.io/badge/Install_in-Cursor-000000?style=flat-square&logoColor=white)](https://cursor.com/en/install-mcp?name=GitCode%20API&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJnaXRjb2RlLWFwaVttY3BdIiwiZ2l0Y29kZS1hcGkiLCJzZXJ2ZSJdLCJlbnYiOnsiR0lUQ09ERV9BQ0NFU1NfVE9LRU4iOiIke2lucHV0OmdpdGNvZGVfYWNjZXNzX3Rva2VufSJ9LCJpbnB1dHMiOlt7ImlkIjoiZ2l0Y29kZV9hY2Nlc3NfdG9rZW4iLCJ0eXBlIjoicHJvbXB0U3RyaW5nIiwiZGVzY3JpcHRpb24iOiJFbnRlciBHSVRDT0RFX0FDQ0VTU19UT0tFTiIsInBhc3N3b3JkIjp0cnVlfV19)
[![Install in VS Code](https://img.shields.io/badge/Install_in-VS_Code-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=GitCode%20API&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--from%22%2C%22gitcode-api%5Bmcp%5D%22%2C%22gitcode-api%22%2C%22serve%22%5D%2C%22env%22%3A%7B%22GITCODE_ACCESS_TOKEN%22%3A%22%24%7Binput%3Agitcode_access_token%7D%22%7D%2C%22inputs%22%3A%5B%7B%22id%22%3A%22gitcode_access_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Enter%20GITCODE_ACCESS_TOKEN%22%2C%22password%22%3Atrue%7D%5D%7D)
[![Install in VS Code Insiders](https://img.shields.io/badge/Install_in-VS_Code_Insiders-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=GitCode%20API&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--from%22%2C%22gitcode-api%5Bmcp%5D%22%2C%22gitcode-api%22%2C%22serve%22%5D%2C%22env%22%3A%7B%22GITCODE_ACCESS_TOKEN%22%3A%22%24%7Binput%3Agitcode_access_token%7D%22%7D%2C%22inputs%22%3A%5B%7B%22id%22%3A%22gitcode_access_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Enter%20GITCODE_ACCESS_TOKEN%22%2C%22password%22%3Atrue%7D%5D%7D&quality=insiders)
[![Install in Visual Studio](https://img.shields.io/badge/Install_in-Visual_Studio-C16FDE?style=flat-square&logo=visualstudio&logoColor=white)](https://vs-open.link/mcp-install?%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--from%22%2C%22gitcode-api%5Bmcp%5D%22%2C%22gitcode-api%22%2C%22serve%22%5D%2C%22env%22%3A%7B%22GITCODE_ACCESS_TOKEN%22%3A%22%24%7Binput%3Agitcode_access_token%7D%22%7D%2C%22inputs%22%3A%5B%7B%22id%22%3A%22gitcode_access_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Enter%20GITCODE_ACCESS_TOKEN%22%2C%22password%22%3Atrue%7D%5D%7D)
[![Add MCP Server GitCode API to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-light.svg)](https://lmstudio.ai/install-mcp?name=GitCode%20API&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJnaXRjb2RlLWFwaVttY3BdIiwiZ2l0Y29kZS1hcGkiLCJzZXJ2ZSJdLCJlbnYiOnsiR0lUQ09ERV9BQ0NFU1NfVE9LRU4iOiIke2lucHV0OmdpdGNvZGVfYWNjZXNzX3Rva2VufSJ9LCJpbnB1dHMiOlt7ImlkIjoiZ2l0Y29kZV9hY2Nlc3NfdG9rZW4iLCJ0eXBlIjoicHJvbXB0U3RyaW5nIiwiZGVzY3JpcHRpb24iOiJFbnRlciBHSVRDT0RFX0FDQ0VTU19UT0tFTiIsInBhc3N3b3JkIjp0cnVlfV19)

For detailed setup (including installing to services like Claude Code / Codex): see [install_mcp_server.md](install_mcp_server.md).

## Authentication

Pass `api_key=` directly, or set `GITCODE_ACCESS_TOKEN` in your environment:

```bash
export GITCODE_ACCESS_TOKEN="your-token"
```

If your token is stored in encrypted form, pass `decrypt=` to decode either an
encrypted `api_key=` value or an encrypted `GITCODE_ACCESS_TOKEN` value before
the client uses it.

```python
from gitcode_api import GitCode
from trusted_library import decrypt_token

client = GitCode(
    api_key="encrypted-token",
    decrypt=decrypt_token,
)
```

## CLI

After installation, you can invoke the SDK directly from the command line:

```bash
gitcode-api repos get --api-key "$GITCODE_ACCESS_TOKEN" --owner SushiNinja --repo GitCode-API
python -m gitcode_api pulls list --api-key "$GITCODE_ACCESS_TOKEN" --owner SushiNinja --repo GitCode-API --state open
```

With `gitcode-api[mcp]` installed (Python 3.10+), you can start the bundled FastMCP server over stdio:

```bash
gitcode-api serve --api-key "$GITCODE_ACCESS_TOKEN"
```

Use `gitcode-api serve -h` for defaults such as `--owner`, `--repo`, `--transport` (`stdio`, `http`, or `sse`), and other options.

Commands mirror the synchronous resource methods on `GitCode`, using the pattern
`gitcode-api <resource> <method> ...`. For methods that accept extra `**params`
or `**payload`, pass repeated `--set key=value` flags or `--set-json '{"key": "value"}'`.

When using string arguments with escape sequence (such as line break `\n`), pass `-e` / `--escape` with the sequences to un-escape, such as `-e '\n\t'`.

## Quick Start

### Sync client

```python
from gitcode_api import GitCode

client = GitCode(
    owner="SushiNinja",
    repo="GitCode-API",
)

repo = client.repos.get()
branches = client.branches.list(per_page=5)

print(repo.full_name)
for branch in branches:
    print(branch.name)
```

### Async client

```python
import asyncio
from gitcode_api import AsyncGitCode

async def main() -> None:
    client = AsyncGitCode(owner="SushiNinja", repo="GitCode-API")
    pulls = await client.pulls.list(state="open", per_page=20)
    print(len(pulls))

asyncio.run(main())
```

### Convert typed return objects to dicts with `as_dict`

Response values are typed `APIObject` subclasses. For serialization or code that expects built-in `dict`, import `as_dict` from the package root: pass a single model to get a `dict`, or pass a list (for example from `client.pulls.list(...)`) to get `list[dict]`. This mirrors the idea of `dataclasses.asdict` but uses each model’s `to_dict()` method. Use `deep_copy=True` when you need detached deep copies.

```python
from gitcode_api import GitCode, as_dict

client = GitCode(owner="SushiNinja")
pulls = client.pulls.list_templates(repo="GitCode-API")
payload = as_dict(pulls)  # list[dict]

repo = client.repos.get(repo="GitCode-API")
meta = as_dict(repo)  # dict
```

### Context managers

`GitCode` and `AsyncGitCode` (and the lower-level `SyncAPIClient` / `AsyncAPIClient`) support `with` / `async with`. Leaving the block calls `close()` / `await close()` on the underlying client automatically, including a custom `http_client=` you passed in. `close()` also clears the LRU cache used by each resource group's `method_signature(...)` helper (see the [Available Resources](#available-resources) section).

```python
from gitcode_api import GitCode

with GitCode(owner="SushiNinja", repo="GitCode-API") as client:
    repo = client.repos.get()
    print(repo.full_name)
```

```python
import asyncio
from gitcode_api import AsyncGitCode

async def main() -> None:
    async with AsyncGitCode(owner="SushiNinja", repo="GitCode-API") as client:
        pulls = await client.pulls.list(state="open", per_page=20)
        print(len(pulls))

asyncio.run(main())
```

## Common Workflows

Create a pull request:

```python
from gitcode_api import GitCode

client = GitCode(owner="SushiNinja", repo="GitCode-API")

pull = client.pulls.create(
    title="Add feature",
    head="feature-branch",
    base="main",
    body="Implements the new flow.",
)
print(pull.number)
```

Get the authenticated user:

```python
from gitcode_api import GitCode

client = GitCode()

user = client.users.me()
print(user.login)
```

Search repositories:

```python
from gitcode_api import GitCode

client = GitCode()

repos = client.search.repositories(q="sdk language:python", per_page=10)
for repo in repos:
    print(repo.full_name)
```

## Available Resources

Both `GitCode` and `AsyncGitCode` expose:

- `repos` and `contents`
- `branches` and `commits`
- `issues` and `pulls`
- `labels`, `milestones`, and `members`
- `releases`, `tags`, and `webhooks`
- `users`, `orgs`, `search`, and `oauth`

Every resource group inherits a cached `methods` property from the shared resource base: a `tuple` of public callable names in stable SDK order (underscore-segment sort key, not plain A–Z on the full identifier). Private names and the introspection helpers `methods` and `method_signature` are omitted. For example, `client.pulls.methods` helps with discovery or tooling without reading the full manual list. For one method’s parameters and return type, call `client.pulls.method_signature("list_issues")` (a cached string from `inspect.signature`, with `gitcode_api._models.` stripped from annotations).

## LLM tools, MCP, and openJiuwen

The `gitcode_api.llm` module exposes a single unified tool, **`gitcode_api_tool`**, that routes calls to respective sync or async SDK resource groups. Model-facing parameters match the JSON schema used by OpenAI-style function tools:

| Parameter | Role |
| --- | --- |
| `op_type` | Required. Resource group on the client (same names as `GitCode` attributes: `repos`, `pulls`, `issues`, and so on). |
| `action` | Method on that resource (for example `get`, `list`). Empty with `help` returns method discovery text. |
| `params` | Keyword arguments for the method as a JSON object; omitted or `null` is treated as `{}`. |
| `help` | When `true`, returns formatted help (available methods or a target signature) instead of performing a normal API call where applicable. |

Tool payloads are JSON-serialized strings: successes look like plain objects (`APIObject.to_dict()`, base64-wrapped `bytes`, and similar); failures use `"error": true`, a `"message"` string, and optional extra fields on HTTP/configuration errors.

### OpenAI tool (`GitCodeOpenAITool`)

No extra dependencies beyond the core package. Build a Chat Completions–style tool definition with `.tool` or `.to_dict()`, then invoke the same instance with the arguments above (sync) or configure async mode for `await`. Each invocation applies `json.dumps` to payload so the return type is **always `str`**. The default keyword argument `indent=2` pretty-prints JSON; pass `indent=None` for a compact single-line string.

```python
from gitcode_api.llm import GitCodeOpenAITool

tool = GitCodeOpenAITool(owner="SushiNinja", repo="GitCode-API")
tools_payload = [tool.tool]  # or tool.to_dict() for a single entry

# Sync invocation (default)
result = tool("repos", "get", params={})

# Async client / awaitable wrapper
async_tool = GitCodeOpenAITool(owner="SushiNinja", repo="GitCode-API", async_mode=True)
# await async_tool("pulls", "list", params={"state": "open", "per_page": 5})
```

You can pass the emitted tool definition into `chat.completions.create(...)`
and handle tool calls directly:

```python
import json
import os
from typing import Dict, List

from openai import OpenAI

from gitcode_api.llm import GitCodeOpenAITool

MESSAGE_SEP = "\n" + "=" * 60 + "\n"
USER_QUERY = "List the repos owned by SushiNinja."
CONVERSATION: List[Dict[str, str]] = [dict(role="user", content=USER_QUERY)]

tools = {"gitcode_api_tool": GitCodeOpenAITool()}
client = OpenAI()

print("U:\n" + USER_QUERY + MESSAGE_SEP)
while True:
    response = (
        client.chat.completions.create(
            model="gpt-5.4-nano",
            messages=CONVERSATION,
            tools=[tools["gitcode_api_tool"].tool],
        )
        .choices[0]
        .message
    )
    CONVERSATION.append(response.to_dict())
    print("A:\n" + (response.content or ""))
    for tool_call in response.tool_calls or []:
        selected_tool = tools[tool_call.function.name]
        result = selected_tool(**json.loads(tool_call.function.arguments))
        CONVERSATION.append(dict(role="tool", tool_call_id=tool_call.id, content=result))
        print(f"<Calling tool {tool_call.function.name}({tool_call.function.arguments})>")
    print(MESSAGE_SEP)
    if not response.tool_calls:
        break
```

### MCP server and MCP tool (FastMCP)

[MCP](https://modelcontextprotocol.io) integration uses [FastMCP](https://github.com/jlowin/fastmcp). Install the optional extra (requires **Python 3.10+** because of the `fastmcp` dependency):

```bash
pip install 'gitcode-api[mcp]'
```

- **`create_mcp_server`** — builds a `FastMCP` instance with `gitcode_api_tool` already registered; optional `name=`, `tool=`, and extra keyword arguments are forwarded to `FastMCP(...)`.
- **`GitCodeMCP`** — thin wrapper that constructs that server and registers the tool; unknown attributes are delegated to the underlying `FastMCP` object (for example transport helpers exposed by your FastMCP version).
- **`create_mcp_gitcode_api_tool`** — returns the standalone async callable used as the tool body (for custom wiring).
- **`register_mcp_gitcode_api_tool`** — attaches that callable to an existing FastMCP-compatible object (`mcp.tool(...)` or `mcp.add_tool(...)`).

```python
from gitcode_api.llm import create_mcp_server

mcp = create_mcp_server(name="GitCode API", owner="SushiNinja", repo="GitCode-API")
# Run or export the server using FastMCP’s API for your version (stdio, HTTP, etc.).
```

The same server is available from the CLI as `gitcode-api serve` (see the [CLI](#cli) section).

To share auth or clients across tools, build `GitCodeLLMTool` once (`from gitcode_api.llm._tool import GitCodeLLMTool`) and pass it as `tool=` into `GitCodeMCP`, `create_mcp_server`, `register_mcp_gitcode_api_tool`, or `create_mcp_gitcode_api_tool`.

### openJiuwen (`LocalFunction`)

[openJiuwen](https://openjiuwen.com) is an open agent platform. With the separate `openjiuwen` package installed (**Python 3.11+**), `create_openjiuwen_gitcode_api_tool` returns an openJiuwen `LocalFunction` that uses the same `op_type` / `action` / `params` / `help` arguments as the OpenAI adapter. Invocation is async-only (`await jiuwen_tool.invoke({...})`).

```bash
pip install openjiuwen
```

```python
from gitcode_api.llm import create_openjiuwen_gitcode_api_tool

jiuwen_tool = create_openjiuwen_gitcode_api_tool(owner="SushiNinja", repo="GitCode-API")
# jiuwen_tool.card — name, description, input_params
# await jiuwen_tool.invoke({"op_type": "repos", "action": "get", "params": {}})
```

Optional `name=` and `description=` override the default tool card. Constructor options otherwise mirror `GitCode` / `AsyncGitCode` (`client=`, `async_client=`, `api_key=`, `owner=`, `repo=`, `base_url=`, `timeout=`, `decrypt=`).

**Claude Desktop (MCPB):** published GitHub Releases include a `gitcode-<version>.mcpb` bundle for one-click installation as a Claude Desktop extension; see Anthropic’s guide, [Build a desktop extension with MCPB](https://claude.com/docs/connectors/building/mcpb). From a checkout you can run `make mcpb` (requires the [`@anthropic-ai/mcpb`](https://www.npmjs.com/package/@anthropic-ai/mcpb) CLI on your `PATH`).

## Examples

Runnable examples live in `examples/`:

- `get_current_user.py`
- `get_repository_overview.py`
- `get_issue_templates.py`
- `get_pull_request_templates.py`
- `list_pull_requests.py`
- `async_list_branches.py`

Example scripts load shared configuration from `examples/.env` using `python-dotenv`.

```bash
uv run python examples/get_current_user.py
uv run python examples/get_repository_overview.py
uv run python examples/get_issue_templates.py
uv run python examples/get_pull_request_templates.py
uv run python examples/list_pull_requests.py
uv run python examples/async_list_branches.py
```

See `examples/.env.example` for the expected variables.

## Documentation

- Project docs entry: `docs/index.rst`
- SDK docs: `docs/sdk/index.rst`
- REST API mirror: `docs/rest_api/index.rst`

Build the docs locally from the repository root. The `docs` Makefile target removes stale `docs/_build` and `docs/sdk/generated` output, then runs Sphinx (via `uv`) with the `html`, `epub`, and `singlehtml` builders. Outputs land under `docs/_build/html/`, `docs/_build/epub/` (including `GitCodeAPI.epub`), and `docs/_build/singlehtml/`:

```bash
make docs
```

Other common targets from the repository root (after `uv sync --all-groups` so optional dependency groups are available):

- `make docs-clean` — remove `docs/_build` and `docs/sdk/generated` without rebuilding.
- `make format` — Ruff lint fixes, import sorting, and formatting.
- `make test` — install the package into the active environment and run pytest.
- `make docstring` — pydocstyle checks for `gitcode_api/`.
- `make binary` — PyInstaller one-file CLI under `dist/` (requires the `binary` group).

## FAQ

### SSL or corporate network errors ("self-signed certificate")

If GitCode HTTPS fails behind a corporate proxy or private PKI, point `httpx` at a CA bundle with `verify` (similar in spirit to `REQUESTS_CA_BUNDLE` for `requests`):

```python
from gitcode_api import GitCode
from httpx import Client

with GitCode(
    owner="SushiNinja",
    repo="GitCode-API",
    http_client=Client(verify="path/to/my/certificate.crt"),
) as client:
    repo = client.repos.get()
    pulls = client.pulls.list(state="open", per_page=5)
```

> Default CA bundle / `verify` behavior for the built-in `httpx` client is documented under **TLS and certificate verification** in [`docs/sdk/quickstart.rst`](docs/sdk/quickstart.rst) and summarized at the top of [`docs/sdk/client_api.rst`](docs/sdk/client_api.rst).

Use `httpx.AsyncClient(verify=...)` with `AsyncGitCode` for async code.

The OpenAI tool (`GitCodeOpenAITool`), MCP helpers, and `create_openjiuwen_gitcode_api_tool` accept the same `client=` / `async_client=` arguments (OpenAI and MCP also accept a shared `GitCodeLLMTool` via `tool=`). Build `GitCode` / `AsyncGitCode` with your custom `http_client` once and pass it through so LLM tool calls reuse the same TLS settings.

## Project Status

This is a community project and is still evolving. API coverage is already broad, but some endpoints and behaviors may continue to be refined as the SDK grows.

## Contributing

Issues, bug reports, API coverage improvements, docs fixes, and pull requests are welcome. If you are using GitCode heavily and notice missing endpoints or awkward ergonomics, contributions are especially appreciated.
