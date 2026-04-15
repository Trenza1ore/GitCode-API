from _shared import create_client, load_config


def main() -> None:
    config = load_config()
    client = create_client()
    try:
        repo = client.repos.get()
        branches = client.branches.list(per_page=config.per_page)
        commits = client.commits.list(per_page=config.per_page)

        print(f"full_name: {repo.full_name}")
        print(f"description: {repo.get('description')}")
        print(f"default_branch: {repo.get('default_branch')}")
        print(f"private: {repo.get('private')}")
        print(f"stars: {repo.get('stargazers_count')}")
        print(f"forks: {repo.get('forks_count')}")
        print("")
        print("branches:")
        for branch in branches[: config.per_page]:
            print(f"- {branch.name}")
        print("")
        print("recent commits:")
        for commit in commits[: config.per_page]:
            print(f"- {str(commit.get('sha'))[:10]}... {(commit.get('commit', {}).get('message')).splitlines()[0]}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
