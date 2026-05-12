# GitCode-API

[![PyPI - Version](https://img.shields.io/pypi/v/gitcode-api?link=https%3A%2F%2Fpypi.org%2Fproject%2Fgitcode-api%2F&uuid=3d29a8a729b04a77b482ce499707c734)](https://pypi.org/project/gitcode-api) [![PyPI Downloads](https://static.pepy.tech/personalized-badge/gitcode-api?period=total&units=INTERNATIONAL_SYSTEM&left_color=GRAY&right_color=RED&left_text=downloads&uuid=4cb2c38f5f5c4a868ff1b53658b30ea0)](https://pepy.tech/projects/gitcode-api) [![CodeFactor](https://www.codefactor.io/repository/github/trenza1ore/gitcode-api/badge)](https://www.codefactor.io/repository/github/trenza1ore/gitcode-api)
[![Install in Cursor](https://img.shields.io/badge/Install_in-Cursor-000000?logoColor=white)](https://cursor.com/en/install-mcp?name=GitCode%20API&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJnaXRjb2RlLWFwaVttY3BdIiwiZ2l0Y29kZS1hcGkiLCJzZXJ2ZSJdLCJlbnYiOnsiR0lUQ09ERV9BQ0NFU1NfVE9LRU4iOiIke2lucHV0OmdpdGNvZGVfYWNjZXNzX3Rva2VufSJ9LCJpbnB1dHMiOlt7ImlkIjoiZ2l0Y29kZV9hY2Nlc3NfdG9rZW4iLCJ0eXBlIjoicHJvbXB0U3RyaW5nIiwiZGVzY3JpcHRpb24iOiJFbnRlciBHSVRDT0RFX0FDQ0VTU19UT0tFTiIsInBhc3N3b3JkIjp0cnVlfV19) [![Install in VS Code](https://img.shields.io/badge/Install_in-VS_Code-0098FF?logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=GitCode%20API&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--from%22%2C%22gitcode-api%5Bmcp%5D%22%2C%22gitcode-api%22%2C%22serve%22%5D%2C%22env%22%3A%7B%22GITCODE_ACCESS_TOKEN%22%3A%22%24%7Binput%3Agitcode_access_token%7D%22%7D%2C%22inputs%22%3A%5B%7B%22id%22%3A%22gitcode_access_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Enter%20GITCODE_ACCESS_TOKEN%22%2C%22password%22%3Atrue%7D%5D%7D)
[![GitHub Badge](https://img.shields.io/badge/github-repo-blue?logo=github&link=https%3A%2F%2Fgithub.com%2FTrenza1ore%2FGitCode-API)](https://github.com/Trenza1ore/GitCode-API) [![GitCode Badge](https://img.shields.io/badge/gitcode-repo-brown?logo=gitcode&link=https%3A%2F%2Fgitcode.com%2FSushiNinja%2FGitCode-API)](https://gitcode.com/SushiNinja/GitCode-API)

[![Docs](https://img.shields.io/badge/%E6%96%87%E6%A1%A3-Docs-cyan?style=for-the-badge&logo=readthedocs&link=https%3A%2F%2Fgitcode-api.readthedocs.io%2Fen%2Flatest%2Findex.html)](https://gitcode-api.readthedocs.io) [![English README](https://img.shields.io/badge/English-README-blue?style=for-the-badge&logo=googledocs&link=README.md)](README.md)

`gitcode-api` 是由社区维护的 GitCode REST API Python SDK：提供同步与异步客户端、按资源组组织的调用方式，以及轻量响应模型，让你在 Python 里调用 GitCode 时不必手写底层 HTTP。`gitcode_api.llm` 还提供 OpenAI 格式的工具、MCP 服务，以及 [openJiuwen](https://openjiuwen.com) 格式的工具集成，便于智能体复用同一套资源型 API。

## 项目定位

- 面向需要在 Python 中接入 GitCode 的开发者。
- 同步（`GitCode`）与异步（`AsyncGitCode`）两套接口形状一致，便于迁移或混用。
- 通过 `client.repos`、`client.pulls`、`client.users` 等资源组挂载具体 API。
- 可在构造客户端时设置 `owner=`、`repo=`，作为仓库相关接口的默认上下文。
- 本仓库含 Sphinx 文档与 GitCode REST API 参考镜像。
- 提供面向 LLM 智能体的 MCP 服务、OpenAI 工具，以及 [openJiuwen](https://openjiuwen.com) 工具。
- 提供可一键安装到常用 AI IDE（如 Cursor、VS Code）的 MCP 服务。
- 提供可直接安装至 Claude 桌面应用使用的 [mcpb包](https://www.anthropic.com/engineering/desktop-extensions)，在 [Release 页面](https://github.com/Trenza1ore/GitCode-API/releases/latest)下载。

## 安装

推荐从 PyPI 安装：

```bash
pip install -U gitcode-api
```

将 MCP 服务器安装到你常用的 AI IDE：
[![Install in Cursor](https://img.shields.io/badge/Install_in-Cursor-000000?style=flat-square&logoColor=white)](https://cursor.com/en/install-mcp?name=GitCode%20API&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJnaXRjb2RlLWFwaVttY3BdIiwiZ2l0Y29kZS1hcGkiLCJzZXJ2ZSJdLCJlbnYiOnsiR0lUQ09ERV9BQ0NFU1NfVE9LRU4iOiIke2lucHV0OmdpdGNvZGVfYWNjZXNzX3Rva2VufSJ9LCJpbnB1dHMiOlt7ImlkIjoiZ2l0Y29kZV9hY2Nlc3NfdG9rZW4iLCJ0eXBlIjoicHJvbXB0U3RyaW5nIiwiZGVzY3JpcHRpb24iOiJFbnRlciBHSVRDT0RFX0FDQ0VTU19UT0tFTiIsInBhc3N3b3JkIjp0cnVlfV19)
[![Install in VS Code](https://img.shields.io/badge/Install_in-VS_Code-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=GitCode%20API&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--from%22%2C%22gitcode-api%5Bmcp%5D%22%2C%22gitcode-api%22%2C%22serve%22%5D%2C%22env%22%3A%7B%22GITCODE_ACCESS_TOKEN%22%3A%22%24%7Binput%3Agitcode_access_token%7D%22%7D%2C%22inputs%22%3A%5B%7B%22id%22%3A%22gitcode_access_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Enter%20GITCODE_ACCESS_TOKEN%22%2C%22password%22%3Atrue%7D%5D%7D)
[![Install in VS Code Insiders](https://img.shields.io/badge/Install_in-VS_Code_Insiders-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=GitCode%20API&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--from%22%2C%22gitcode-api%5Bmcp%5D%22%2C%22gitcode-api%22%2C%22serve%22%5D%2C%22env%22%3A%7B%22GITCODE_ACCESS_TOKEN%22%3A%22%24%7Binput%3Agitcode_access_token%7D%22%7D%2C%22inputs%22%3A%5B%7B%22id%22%3A%22gitcode_access_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Enter%20GITCODE_ACCESS_TOKEN%22%2C%22password%22%3Atrue%7D%5D%7D&quality=insiders)
[![Install in Visual Studio](https://img.shields.io/badge/Install_in-Visual_Studio-C16FDE?style=flat-square&logo=visualstudio&logoColor=white)](https://vs-open.link/mcp-install?%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--from%22%2C%22gitcode-api%5Bmcp%5D%22%2C%22gitcode-api%22%2C%22serve%22%5D%2C%22env%22%3A%7B%22GITCODE_ACCESS_TOKEN%22%3A%22%24%7Binput%3Agitcode_access_token%7D%22%7D%2C%22inputs%22%3A%5B%7B%22id%22%3A%22gitcode_access_token%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Enter%20GITCODE_ACCESS_TOKEN%22%2C%22password%22%3Atrue%7D%5D%7D)
[![Add MCP Server GitCode API to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-light.svg)](https://lmstudio.ai/install-mcp?name=GitCode%20API&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJnaXRjb2RlLWFwaVttY3BdIiwiZ2l0Y29kZS1hcGkiLCJzZXJ2ZSJdLCJlbnYiOnsiR0lUQ09ERV9BQ0NFU1NfVE9LRU4iOiIke2lucHV0OmdpdGNvZGVfYWNjZXNzX3Rva2VufSJ9LCJpbnB1dHMiOlt7ImlkIjoiZ2l0Y29kZV9hY2Nlc3NfdG9rZW4iLCJ0eXBlIjoicHJvbXB0U3RyaW5nIiwiZGVzY3JpcHRpb24iOiJFbnRlciBHSVRDT0RFX0FDQ0VTU19UT0tFTiIsInBhc3N3b3JkIjp0cnVlfV19)

详细安装说明（包括安装到 Claude Code / Codex 等服务）见 [install_mcp_server.md](install_mcp_server.md)。

## 认证

可直接传入 `api_key=`，或将访问令牌写入环境变量：

```bash
export GITCODE_ACCESS_TOKEN="your-token"
```

若令牌以密文形式保存，可在构造客户端时传入 `decrypt=`，在发起请求前解密 `api_key=` 或环境变量 `GITCODE_ACCESS_TOKEN`：

```python
from gitcode_api import GitCode
from trusted_library import decrypt_token

client = GitCode(
    api_key="encrypted-token",
    decrypt=decrypt_token,
)
```

## CLI

安装后可通过命令行调用 SDK，例如：

```bash
gitcode-api repos get --api-key "$GITCODE_ACCESS_TOKEN" --owner SushiNinja --repo GitCode-API
python -m gitcode_api pulls list --api-key "$GITCODE_ACCESS_TOKEN" --owner SushiNinja --repo GitCode-API --state open
```

已安装 `gitcode-api[mcp]`（Python 3.10+）时，可通过 stdio 启动内置的 FastMCP 服务：

```bash
gitcode-api serve --api-key "$GITCODE_ACCESS_TOKEN"
```

`gitcode-api serve -h` 可查看 `--owner`、`--repo`、`--transport`（`stdio`、`http`、`sse`）等选项。

子命令与**同步客户端** `GitCode` 上各资源组的方法一一对应，形如 `gitcode-api <resource> <method> ...`。若某方法还支持 `**params` 或 `**payload` 等额外参数，可多次使用 `--set key=value`，或使用 `--set-json '{"key": "value"}'` 传入 JSON。

当传入的参数包含转义字符时（比如换行符 `\n`），可使用 `-e` / `--escape` 指定要反转义的字符，例如 `-e '\n\t'`。

## 快速开始

### 同步客户端

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

### 异步客户端

```python
import asyncio
from gitcode_api import AsyncGitCode

async def main() -> None:
    client = AsyncGitCode(owner="SushiNinja", repo="GitCode-API")
    pulls = await client.pulls.list(state="open", per_page=20)
    print(len(pulls))

asyncio.run(main())
```

### 上下文管理器

`GitCode` 与 `AsyncGitCode`（以及更底层的 `SyncAPIClient` / `AsyncAPIClient`）均可作为 `with` / `async with` 的上下文使用：离开代码块时会自动调用 `close()` 或 `await close()`，释放底层 httpx 客户端；若你传入了自定义 `http_client=`，也会随 SDK 客户端一并关闭。`close()` 还会清空各资源组上 `method_signature(...)` 的 LRU 缓存见 **资源组**，避免 LRU 缓存在关闭后仍持有引用、影响垃圾回收。

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

## 常见场景示例

创建 Pull Request：

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

获取当前登录用户：

```python
from gitcode_api import GitCode

client = GitCode()

user = client.users.me()
print(user.login)
```

搜索仓库：

```python
from gitcode_api import GitCode

client = GitCode()

repos = client.search.repositories(q="sdk language:python", per_page=10)
for repo in repos:
    print(repo.full_name)
```

## 资源组

`GitCode` 与 `AsyncGitCode` 均暴露下列资源组：

- `repos` 与 `contents`
- `branches` 与 `commits`
- `issues` 与 `pulls`
- `labels`、`milestones` 与 `members`
- `releases`、`tags` 与 `webhooks`
- `users`、`orgs`、`search` 与 `oauth`

每个资源组（例如 `client.pulls`、`client.repos`）在共享基类上带有缓存属性 `methods`：值为该组**对外可调用的方法名**组成的 `tuple`。顺序由 SDK 根据方法名中下划线分段生成排序键决定，**并非**对完整方法名做字典序排列。不包含以下划线开头的名称，也不包含内省辅助方法 `methods` 与 `method_signature`。适合在交互环境或工具链中快速查看某组暴露了哪些接口。若需要单个方法的参数与返回类型，可调用 `client.pulls.method_signature("list_issues")`（基于 `inspect.signature` 的缓存字符串，注解中的 `gitcode_api._models.` 前缀会被去掉）。

## LLM 工具、MCP 与 openJiuwen

`gitcode_api.llm` 模块对外提供一个统一的工具 **`gitcode_api_tool`**，自动将调用路由到对应的同步或异步 SDK 资源组。面向模型的参数与 OpenAI 风格函数工具的 JSON Schema 一致：

| 参数 | 作用 |
| --- | --- |
| `op_type` | 必填。客户端上的资源组名（与 `GitCode` 属性一致，如 `repos`、`pulls`、`issues` 等）。 |
| `action` | 该资源上的方法名（如 `get`、`list`）。在配合 `help` 时若为空，可返回方法发现说明文本。 |
| `params` | 传给该方法的**关键字参数**组成的 JSON 对象；省略或 `null` 视为 `{}`。 |
| `help` | 为 `true` 时，在适用场景下返回格式化的帮助信息（可用方法或目标方法签名），而非执行常规 API 请求。 |

工具负载为经 JSON 序列化后的字符串：成功时其内容类似普通对象（如 `APIObject.to_dict()`、对 `bytes` 做 base64 包装等）；失败时使用 `"error": true`、`"message"` 字段，HTTP 或配置错误在可用时附带额外字段。

### OpenAI 工具（`GitCodeOpenAITool`）

除核心包外无需额外依赖。通过 `.tool` 或 `to_dict()` 生成 Chat Completions 风格的工具定义，再用上文参数以同步方式调用同一实例；需要 `await` 时启用异步模式。每次调用都会对负载执行 `json.dumps`，因此返回值**始终为 `str`**。默认关键字参数 `indent=2` 会美化 JSON；传入 `indent=None` 可得到紧凑的单行字符串。

```python
from gitcode_api.llm import GitCodeOpenAITool

tool = GitCodeOpenAITool(owner="SushiNinja", repo="GitCode-API")
tools_payload = [tool.tool]  # 或单条使用 tool.to_dict()

# 默认：同步调用
result = tool("repos", "get", params={})

# 异步客户端 / 可 await 的封装
async_tool = GitCodeOpenAITool(owner="SushiNinja", repo="GitCode-API", async_mode=True)
# await async_tool("pulls", "list", params={"state": "open", "per_page": 5})
```

也可以直接把生成的工具定义传给 `chat.completions.create(...)`，并像
`test.py` 那样手动处理工具调用：

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

### MCP 服务与 MCP 工具（FastMCP）

[MCP](https://modelcontextprotocol.io) 集成基于 [FastMCP](https://github.com/jlowin/fastmcp)。请安装可选依赖组（因 `fastmcp` 约束，需 **Python 3.10+**）：

```bash
pip install 'gitcode-api[mcp]'
```

- **`create_mcp_server`** — 创建已注册 `gitcode_api_tool` 的 `FastMCP` 实例；可选 `name=`、`tool=` 以及其余关键字参数会原样传给 `FastMCP(...)`。
- **`GitCodeMCP`** — 薄封装：构造上述服务并注册工具；未定义的属性会委托给底层 `FastMCP` 对象（例如各版本 FastMCP 暴露的传输相关接口）。
- **`create_mcp_gitcode_api_tool`** — 返回独立的异步可调用对象，作为工具实现，供自定义挂载。
- **`register_mcp_gitcode_api_tool`** — 将上述可调用对象注册到已有的 FastMCP 兼容对象上（`mcp.tool(...)` 或 `mcp.add_tool(...)`）。

```python
from gitcode_api.llm import create_mcp_server

mcp = create_mcp_server(name="GitCode API", owner="SushiNinja", repo="GitCode-API")
# 按你所用的 FastMCP 版本文档启动或导出服务（stdio、HTTP 等）。
```

等价地也可通过命令行 `gitcode-api serve` 启动同一套内置服务（见上文 [CLI](#cli) 小节）。

若要在多个工具间共享认证或客户端，可只构造一次 `GitCodeLLMTool`（`from gitcode_api.llm._tool import GitCodeLLMTool`），再以 `tool=` 传入 `GitCodeMCP`、`create_mcp_server`、`register_mcp_gitcode_api_tool` 或 `create_mcp_gitcode_api_tool`。

### openJiuwen（`LocalFunction`）

[openJiuwen](https://openjiuwen.com) 是开放的智能体平台。另行安装 `openjiuwen` 包（**Python 3.11+**）后，可使用 `create_openjiuwen_gitcode_api_tool` 获得与 OpenAI 适配器使用相同 `op_type` / `action` / `params` / `help` 参数的 `LocalFunction`。调用方式为 **仅异步**（`await jiuwen_tool.invoke({...})`）。

```bash
pip install openjiuwen
```

```python
from gitcode_api.llm import create_openjiuwen_gitcode_api_tool

jiuwen_tool = create_openjiuwen_gitcode_api_tool(owner="SushiNinja", repo="GitCode-API")
# jiuwen_tool.card — 名称、描述、input_params
# await jiuwen_tool.invoke({"op_type": "repos", "action": "get", "params": {}})
```

可用 `name=`、`description=` 覆盖默认工具卡。其余构造参数与 `GitCode` / `AsyncGitCode` 一致（`client=`、`async_client=`、`api_key=`、`owner=`、`repo=`、`base_url=`、`timeout=`、`decrypt=`）。

**Claude Desktop（MCPB）：** 每个已发布的 GitHub Release 会附带 `gitcode-<version>.mcpb`，可在 Claude Desktop 中作为扩展一键安装；说明见 Anthropic 文档 [使用 MCPB 构建桌面扩展](https://claude.com/docs/connectors/building/mcpb)。在仓库根目录执行 `make mcpb` 可在本地打包（需已安装 [`@anthropic-ai/mcpb`](https://www.npmjs.com/package/@anthropic-ai/mcpb) 并可在 `PATH` 中调用 `mcpb`）。

## 示例

可运行脚本位于 `examples/`：

- `get_current_user.py`
- `get_repository_overview.py`
- `list_pull_requests.py`
- `async_list_branches.py`

示例使用 `python-dotenv` 从 `examples/.env` 读取配置。

```bash
uv run python examples/get_current_user.py
uv run python examples/get_repository_overview.py
uv run python examples/list_pull_requests.py
uv run python examples/async_list_branches.py
```

环境变量说明见 `examples/.env.example`。

## 文档

- 文档总入口：`docs/index.rst`
- SDK 文档：`docs/sdk/index.rst`
- REST API 参考镜像：`docs/rest_api/index.rst`

在仓库根目录构建文档。`make docs` 会先清理旧的 `docs/_build` 与 `docs/sdk/generated`，再通过 `uv` 依次运行 Sphinx 的 `html`、`epub`、`singlehtml` 构建器；产物分别位于 `docs/_build/html/`、`docs/_build/epub/`（含 `GitCodeAPI.epub`）、`docs/_build/singlehtml/`：

```bash
make docs
```

在仓库根目录常用的其他 Makefile 目标（建议先执行 `uv sync --all-groups`，以便安装文档、测试、格式化等可选依赖组）：

- `make docs-clean` — 仅删除 `docs/_build` 与 `docs/sdk/generated`，不重新构建。
- `make format` — Ruff 修复、import 排序与代码格式化。
- `make test` — 将包安装到当前环境并运行 pytest。
- `make docstring` — 对 `gitcode_api/` 运行 pydocstyle 检查。
- `make binary` — 使用 PyInstaller 打包单文件 CLI 到 `dist/`（需 `binary` 依赖组）。

## 常见问题

### SSL 或企业网络报错（如「自签名证书」）

若在企业代理或私有 PKI 环境下访问 GitCode HTTPS 失败，可为 `httpx` 指定 `verify` 指向 CA 证书包路径（思路类似 `requests` 使用的 `REQUESTS_CA_BUNDLE`）：

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

异步场景请对 `AsyncGitCode` 使用 `httpx.AsyncClient(verify=...)`。

OpenAI 工具（`GitCodeOpenAITool`）、MCP 相关接口与 `create_openjiuwen_gitcode_api_tool` 同样支持传入已配置好的 `client=` / `async_client=`（OpenAI 与 MCP 还可通过 `tool=` 传入已设置上述客户端的 `GitCodeLLMTool`）。先用自定义 `http_client` 构造 `GitCode` / `AsyncGitCode`，再传入这些适配器，LLM 工具调用会沿用同一套 TLS 与证书配置，不必另做一套处理。

## 项目状态

本项目由社区维护，仍在持续演进。当前已覆盖大量 GitCode API；随着版本迭代，个别端点或行为仍可能被补充或调整。

## 贡献

欢迎提交 issue、改进文档、补充测试、扩展 API 封装或直接发起 pull request。若你在实际使用中发现缺失接口或不顺手的设计，也欢迎反馈与贡献。
