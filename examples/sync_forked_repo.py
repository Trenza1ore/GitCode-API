from _shared import load_config

from gitcode_api import GitCode


def main() -> None:
    config = load_config()
    owner = "SushiNinja"
    repo = "agent-core-contrib"

    with GitCode(api_key=config.api_key, owner=owner, repo=repo) as client:
        status = client.repos.sync_repo()
        print(f"repository: {owner}/{repo}")
        print(f"repo_sync_result: {status.repo_sync_result}")
        print(f"repo_sync_message: {status.repo_sync_message}")
        print(f"raw_response: {status.to_dict()}")


if __name__ == "__main__":
    main()
