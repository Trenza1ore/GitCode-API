from _shared import create_client


def main() -> None:
    client = create_client()
    try:
        user = client.users.me()
        print(f"login: {user.login}")
        print(f"name: {user.get('name')}")
        print(f"html_url: {user.get('html_url')}")
        print(f"followers: {user.get('followers')}")
        print(f"following: {user.get('following')}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
