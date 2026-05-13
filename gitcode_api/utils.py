"""Utility helper functions."""

from copy import deepcopy
from typing import Any, Dict, List, Union, overload

from ._models import APIObject


@overload
def as_dict(data: APIObject, deep_copy: bool = False) -> Dict[str, Any]: ...


@overload
def as_dict(data: List[APIObject], deep_copy: bool = False) -> List[Dict[str, Any]]: ...


def as_dict(data: Union[APIObject, List[APIObject]], deep_copy: bool = False) -> Union[Dict, List[Dict]]:
    """Convert one :class:`~gitcode_api._models.APIObject` to a plain ``dict``, or several to a list of dicts.

    Similar to :func:`dataclasses.asdict`. Input is converted with :meth:`~gitcode_api._models.APIObject.to_dict`.
    When ``deep_copy`` is true, each mapping is copied with :func:`copy.deepcopy`.

    :param data: A single response model or a list of them.
    :param deep_copy: When true, return deep-copied dicts.
    :returns: A dict for a single input, or a list of dicts for a list input.
    """
    if isinstance(data, list):
        items = data
    else:
        items = [data]
    if not all(hasattr(item, "to_dict") for item in items):
        raise TypeError("Input is not APIObject or list[APIObject]")
    if deep_copy:
        out = [deepcopy(item.to_dict()) for item in items]
    else:
        out = [item.to_dict() for item in items]
    return out[0] if len(out) == 1 else out
