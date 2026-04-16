import sys
from collections.abc import Callable
from pathlib import Path
from typing import Tuple

import httpx
import pytest

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gitcode_api import AsyncGitCode, GitCode

ResponseFactory = Callable[[httpx.Request], httpx.Response]


def make_sync_client(handler: ResponseFactory, **client_kwargs) -> Tuple[GitCode, httpx.Client]:
    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = GitCode(api_key="test-token", http_client=http_client, **client_kwargs)
    return client, http_client


def make_async_client(handler: ResponseFactory, **client_kwargs) -> Tuple[AsyncGitCode, httpx.AsyncClient]:
    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AsyncGitCode(api_key="test-token", http_client=http_client, **client_kwargs)
    return client, http_client


@pytest.fixture
def sync_client_factory() -> Callable[..., Tuple[GitCode, httpx.Client]]:
    return make_sync_client


@pytest.fixture
def async_client_factory() -> Callable[..., Tuple[AsyncGitCode, httpx.AsyncClient]]:
    return make_async_client
