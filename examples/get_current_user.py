from _shared import load_config

from gitcode_api import GitCode


def main() -> None:
    config = load_config()
    with GitCode(api_key=config.api_key, owner=config.owner, repo=config.repo) as client:
        user = client.users.me()
        print(f"login: {user.login}")
        print(f"name: {user.name}")
        print(f"html_url: {user.html_url}")
        print(f"followers: {user.followers}")
        print(f"following: {user.following}")


if __name__ == "__main__":
    main()
