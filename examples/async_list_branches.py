import asyncio

from _shared import create_async_client, load_config


async def main() -> None:
    config = load_config()
    client = create_async_client()
    try:
        branches = await client.branches.list(per_page=config.per_page)
        print(f"repository: {config.owner}/{config.repo}")
        print("branches:")
        for branch in branches[: config.per_page]:
            print(f"- {branch.name} (protected={branch.get('protected')})")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
