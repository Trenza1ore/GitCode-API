from _shared import load_config

from gitcode_api import GitCode


def main() -> None:
    config = load_config()
    with GitCode(api_key=config.api_key, owner=config.owner, repo=config.repo) as client:
        pulls = client.pulls.list(state=config.pull_state, per_page=config.per_page)
        print(f"pull request state: {config.pull_state}")
        print(f"repository: {config.owner}/{config.repo}")
        print("")

        for pull in pulls:
            print(
                f"- #{pull.number} [{pull.state}] "
                f"{pull.title} "
                f"(source={pull.source_branch}, target={pull.target_branch})"
            )


if __name__ == "__main__":
    main()
