from _shared import load_config

from gitcode_api import GitCode


def main() -> None:
    config = load_config()
    with GitCode(api_key=config.api_key, owner=config.owner, repo=config.repo) as client:
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


if __name__ == "__main__":
    main()
