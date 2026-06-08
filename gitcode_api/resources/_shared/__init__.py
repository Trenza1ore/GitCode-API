"""Shared resource base classes and template helpers."""

from .base import AsyncResource, SyncResource
from .fetch_template import (
    get_gitcode_template_body_async,
    get_gitcode_template_body_sync,
    list_gitcode_template_rows_async,
    list_gitcode_template_rows_sync,
)

__all__ = [
    "AsyncResource",
    "SyncResource",
    "get_gitcode_template_body_sync",
    "get_gitcode_template_body_async",
    "list_gitcode_template_rows_sync",
    "list_gitcode_template_rows_async",
]
