"""Shared constant values for the GitCode SDK."""

import re

DEFAULT_BASE_URL = "https://api.gitcode.com/api/v5"
DEFAULT_TIMEOUT = 30.0
DEFAULT_TOKEN_ENV = "GITCODE_ACCESS_TOKEN"
DEFAULT_CA_ENV = "GITCODE_CA_BUNDLE"
GITCODE_ISSUE_TEMPLATE_PATH_RE: re.Pattern[str] = re.compile(
    r"\.git(code|hub)/ISSUE_TEMPLATE.*\.(md|markdown|ya?ml)$", re.IGNORECASE
)
GITCODE_PULL_REQUEST_TEMPLATE_PATH_RE: re.Pattern[str] = re.compile(
    r"\.git(code|hub)/PULL_REQUEST_TEMPLATE.*\.(md|markdown|ya?ml)$", re.IGNORECASE
)
GITCODE_TEMPLATE_REPO = ".gitcode"

__all__ = [
    "DEFAULT_BASE_URL",
    "DEFAULT_TIMEOUT",
    "DEFAULT_TOKEN_ENV",
    "DEFAULT_CA_ENV",
    "GITCODE_ISSUE_TEMPLATE_PATH_RE",
    "GITCODE_PULL_REQUEST_TEMPLATE_PATH_RE",
    "GITCODE_TEMPLATE_REPO",
]
