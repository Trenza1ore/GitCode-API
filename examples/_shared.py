import os
import sys
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gitcode_api import AsyncGitCode, GitCode

ENV_PATH = Path(__file__).with_name(".env")


@dataclass
class ExampleConfig:
    api_key: str
    owner: str
    repo: str
    username: str
    pull_state: str
    per_page: int


def load_config() -> ExampleConfig:
    if not ENV_PATH.exists():
        raise RuntimeError(f"Missing config file: {ENV_PATH}")

    load_dotenv(ENV_PATH, override=True)

    required_keys = [
        "GITCODE_ACCESS_TOKEN",
        "GITCODE_OWNER",
        "GITCODE_REPO",
        "GITCODE_USERNAME",
    ]
    missing = [key for key in required_keys if not os.getenv(key)]
    if missing:
        raise RuntimeError("Please fill in these keys in examples/.env before running examples: " + ", ".join(missing))

    return ExampleConfig(
        api_key=os.environ["GITCODE_ACCESS_TOKEN"],
        owner=os.environ["GITCODE_OWNER"],
        repo=os.environ["GITCODE_REPO"],
        username=os.environ["GITCODE_USERNAME"],
        pull_state=os.getenv("GITCODE_PULL_STATE", "open") or "open",
        per_page=int(os.getenv("GITCODE_PER_PAGE", "5") or "5"),
    )


def create_client() -> GitCode:
    config = load_config()
    return GitCode(api_key=config.api_key, owner=config.owner, repo=config.repo)


def create_async_client() -> AsyncGitCode:
    config = load_config()
    return AsyncGitCode(api_key=config.api_key, owner=config.owner, repo=config.repo)
