# GitCode-API

[![PyPI - Version](https://img.shields.io/pypi/v/gitcode-api?link=https%3A%2F%2Fpypi.org%2Fproject%2Fgitcode-api%2F)](https://pypi.org/project/gitcode-api) [![GitHub Badge](https://img.shields.io/badge/github-repo-blue?logo=github&link=https%3A%2F%2Fgithub.com%2FTrenza1ore%2FGitCode-API)](https://github.com/Trenza1ore/GitCode-API) [![GitCode Badge](https://img.shields.io/badge/gitcode-repo-brown?logo=gitcode&link=https%3A%2F%2Fgitcode.com%2FSushiNinja%2FGitCode-API)](https://gitcode.com/SushiNinja/GitCode-API) [![PyPI Downloads](https://static.pepy.tech/personalized-badge/gitcode-api?period=total&units=INTERNATIONAL_SYSTEM&left_color=GRAY&right_color=RED&left_text=downloads)](https://pepy.tech/projects/gitcode-api)

[![Docs](https://img.shields.io/badge/%E6%96%87%E6%A1%A3-Docs-cyan?style=for-the-badge&logo=readthedocs&link=https%3A%2F%2Fgitcode-api.readthedocs.io%2Fen%2Flatest%2Findex.html)](https://gitcode-api.readthedocs.io) [![English README](https://img.shields.io/badge/English-README-blue?style=for-the-badge&logo=googledocs&link=README.md)](README.md)

`gitcode-api` 是由社区维护的 GitCode REST API Python SDK：提供同步与异步客户端、按资源组组织的调用方式，以及轻量响应模型，让你在 Python 里调用 GitCode 时不必手写底层 HTTP。

## 项目定位

- 面向需要在 Python 中接入 GitCode 的开发者。
- 同步（`GitCode`）与异步（`AsyncGitCode`）两套接口形状一致，便于迁移或混用。
- 通过 `client.repos`、`client.pulls`、`client.users` 等资源组挂载具体 API。
- 可在构造客户端时设置 `owner=`、`repo=`，作为仓库相关接口的默认上下文。
- 本仓库含 Sphinx 文档与 GitCode REST API 参考镜像。

## 安装

推荐从 PyPI 安装：

```bash
pip install -U gitcode-api
```

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

子命令与**同步客户端** `GitCode` 上各资源组的方法一一对应，形如 `gitcode-api <resource> <method> ...`。若某方法还支持 `**params` 或 `**payload` 等额外参数，可多次使用 `--set key=value`，或使用 `--set-json '{"key": "value"}'` 传入 JSON。

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

`GitCode` 与 `AsyncGitCode`（以及更底层的 `SyncAPIClient` / `AsyncAPIClient`）均可作为 `with` / `async with` 的上下文使用：离开代码块时会自动调用 `close()` 或 `await close()`，释放底层 httpx 客户端；若你传入了自定义 `http_client=`，也会随 SDK 客户端一并关闭。

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

## 已支持的资源组

`GitCode` 与 `AsyncGitCode` 均暴露下列资源组：

- `repos` 与 `contents`
- `branches` 与 `commits`
- `issues` 与 `pulls`
- `labels`、`milestones` 与 `members`
- `releases`、`tags` 与 `webhooks`
- `users`、`orgs`、`search` 与 `oauth`

每个资源组（例如 `client.pulls`、`client.repos`）在共享基类上带有缓存属性 `methods`：值为该组**对外可调用的方法名**组成的 `tuple`。顺序由 SDK 根据方法名中下划线分段生成排序键决定，**并非**对完整方法名做字典序排列。不包含以下划线开头的名称，也不包含内省辅助方法 `methods` 与 `method_signature`。适合在交互环境或工具链中快速查看某组暴露了哪些接口。若需要单个方法的参数与返回类型，可调用 `client.pulls.method_signature("list_issues")`（基于 `inspect.signature` 的缓存字符串，注解中的 `gitcode_api._models.` 前缀会被去掉）。

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

本地用 Sphinx 构建 HTML：

```bash
uv run --group docs sphinx-build -b html docs docs/_build/html
```

## 项目状态

本项目由社区维护，仍在持续演进。当前已覆盖大量 GitCode API；随着版本迭代，个别端点或行为仍可能被补充或调整。

## 贡献

欢迎提交 issue、改进文档、补充测试、扩展 API 封装或直接发起 pull request。若你在实际使用中发现缺失接口或不顺手的设计，也欢迎反馈与贡献。
