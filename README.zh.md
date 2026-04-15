# GitCode-API

[English README](README.md)

`gitcode-api` 是一个由社区维护的 GitCode REST API Python SDK。它提供易用的同步和异步客户端、按资源分组的调用入口，以及轻量级响应模型，帮助你在 Python 中更方便地使用 GitCode，而不必手写原始 HTTP 请求。

## 项目定位

- 面向社区的 GitCode Python 库项目。
- 同时提供同步和异步客户端，调用方式保持一致。
- 提供 `client.repos`、`client.pulls`、`client.users` 等资源命名空间。
- 支持在客户端上设置 `owner=` 和 `repo=` 作为仓库级默认上下文。
- 仓库内包含 Sphinx 文档，以及 GitCode REST API 文档镜像。

## 安装

当前仓库主要面向源码使用和本地开发：

```bash
uv sync
```

如果需要构建文档：

```bash
uv sync --group docs
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

try:
    repo = client.repos.get()
    branches = client.branches.list(per_page=5)

    print(repo.full_name)
    for branch in branches:
        print(branch.name)
finally:
    client.close()
```

### 异步客户端

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
