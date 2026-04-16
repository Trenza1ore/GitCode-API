import asyncio

from _shared import load_config

from gitcode_api import AsyncGitCode


async def main() -> None:
    config = load_config()
    async with AsyncGitCode(api_key=config.api_key, owner=config.owner, repo=config.repo) as client:
        branches = await client.branches.list(per_page=config.per_page)
        print(f"repository: {config.owner}/{config.repo}")
        print("branches:")
        for branch in branches[: config.per_page]:
            print(f"- {branch.name} (protected={branch.get('protected')})")


if __name__ == "__main__":
    asyncio.run(main())
