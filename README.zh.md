# GitCode-API

[![PyPI - Version](https://img.shields.io/pypi/v/gitcode-api?link=https%3A%2F%2Fpypi.org%2Fproject%2Fgitcode-api%2F)](https://pypi.org/project/gitcode-api) [![GitHub Badge](https://img.shields.io/badge/github-repo-blue?logo=github&link=https%3A%2F%2Fgithub.com%2FTrenza1ore%2FGitCode-API)](https://github.com/Trenza1ore/GitCode-API) [![GitCode Badge](https://img.shields.io/badge/gitcode-repo-brown?logo=gitcode&link=https%3A%2F%2Fgitcode.com%2FSushiNinja%2FGitCode-API)](https://gitcode.com/SushiNinja/GitCode-API) [![PyPI Downloads](https://static.pepy.tech/personalized-badge/gitcode-api?period=total&units=INTERNATIONAL_SYSTEM&left_color=GRAY&right_color=RED&left_text=downloads)](https://pepy.tech/projects/gitcode-api)

[![Docs](https://img.shields.io/badge/%E6%96%87%E6%A1%A3-Docs-cyan?style=for-the-badge&logo=readthedocs&link=https%3A%2F%2Fgitcode-api.readthedocs.io%2Fen%2Flatest%2Findex.html)](https://gitcode-api.readthedocs.io) [![中文README](https://img.shields.io/badge/%E4%B8%AD%E6%96%87-README-brown?style=for-the-badge&logo=googledocs&link=README.zh.md)](README.zh.md) [![English README](https://img.shields.io/badge/English-README-blue?style=for-the-badge&logo=googledocs&link=README.md)](README.md)

`gitcode-api` 是一个由社区维护的 GitCode REST API Python SDK。它提供易用的同步和异步客户端、按资源分组的调用入口，以及轻量级响应模型，帮助你在 Python 中更方便地使用 GitCode，而不必手写原始 HTTP 请求。

## 项目定位

- 面向社区的 GitCode Python 库项目。
- 同时提供同步和异步客户端，调用方式保持一致。
- 提供 `client.repos`、`client.pulls`、`client.users` 等资源命名空间。
- 支持在客户端上设置 `owner=` 和 `repo=` 作为仓库级默认上下文。
- 仓库内包含 Sphinx 文档，以及 GitCode REST API 文档镜像。

## 安装

推荐直接通过 PyPI 安装：

```bash
pip install gitcode-api
```

## 认证

你可以直接传入 `api_key=`，也可以通过环境变量设置访问令牌：

```bash
export GITCODE_ACCESS_TOKEN="your-token"
```

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

`GitCode` 与 `AsyncGitCode`（以及底层的 `SyncAPIClient` / `AsyncAPIClient`）支持 `with` / `async with`。当由 SDK 自行创建底层 httpx 客户端时，离开代码块会自动对其调用 `close()` / `await close()`。

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

若你传入自定义的 `http_client=`，SDK 不会关闭该实例，仍由你负责其生命周期（例如先 `async with httpx.AsyncClient(...) as http:`，再传入 `AsyncGitCode(http_client=http)`）。

## 常见用法

创建 Pull Request：

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

获取当前认证用户：

```python
from gitcode_api import GitCode

client = GitCode()

try:
    user = client.users.me()
    print(user.login)
finally:
    client.close()
```

搜索仓库：

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

## 已支持的资源分组

`GitCode` 和 `AsyncGitCode` 都提供以下资源入口：

- `repos` 与 `contents`
- `branches` 与 `commits`
- `issues` 与 `pulls`
- `labels`、`milestones` 与 `members`
- `releases`、`tags` 与 `webhooks`
- `users`、`orgs`、`search` 与 `oauth`

## 示例

可运行示例位于 `examples/`：

- `get_current_user.py`
- `get_repository_overview.py`
- `list_pull_requests.py`
- `async_list_branches.py`

这些示例会通过 `python-dotenv` 从 `examples/.env` 读取共享配置。

```bash
uv run python examples/get_current_user.py
uv run python examples/get_repository_overview.py
uv run python examples/list_pull_requests.py
uv run python examples/async_list_branches.py
```

所需环境变量可以参考 `examples/.env.example`。

## 文档

- 项目文档入口：`docs/index.rst`
- SDK 文档：`docs/sdk/index.rst`
- REST API 文档镜像：`docs/rest_api/index.rst`

使用 Sphinx 本地构建文档：

```bash
uv run --group docs sphinx-build -b html docs docs/_build/html
```

## 项目状态

这是一个社区项目，目前仍在持续完善中。当前已经覆盖较多 GitCode API 能力，但随着 SDK 继续演进，部分端点和行为仍可能进一步补充和优化。

## 贡献

欢迎提交 issue、修复文档、补充测试、完善 API 覆盖率或直接发起 pull request。如果你在实际使用 GitCode 时发现缺失的端点或不够顺手的 SDK 设计，也非常欢迎反馈和贡献。
