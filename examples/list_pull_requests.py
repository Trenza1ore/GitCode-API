from _shared import create_client, load_config


def main() -> None:
    config = load_config()
    client = create_client()
    try:
        pulls = client.pulls.list(state=config.pull_state, per_page=config.per_page)
        print(f"pull request state: {config.pull_state}")
        print(f"repository: {config.owner}/{config.repo}")
        print("")

        for pull in pulls:
            print(
                f"- #{pull.number} [{pull.state}] "
                f"{pull.title} "
                f"(source={pull.get('source_branch')}, target={pull.get('target_branch')})"
            )
    finally:
        client.close()


if __name__ == "__main__":
    main()
