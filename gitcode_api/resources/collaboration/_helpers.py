"""Shared helpers for collaboration resource groups."""

from typing import List, Optional


def _comma_join(values: Optional[List[str]]) -> Optional[str]:
    """Join a list of strings into the comma-separated format used by the API."""
    if not values:
        return None
    return ",".join(values)
