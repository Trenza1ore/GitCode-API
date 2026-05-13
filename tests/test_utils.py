import pytest

from gitcode_api import as_dict
from gitcode_api._models import APIObject


def test_as_dict_single() -> None:
    obj = APIObject({"name": "x"})
    assert as_dict(obj) == {"name": "x"}


def test_as_dict_list() -> None:
    objs = [APIObject({"a": 1}), APIObject({"b": 2})]
    assert as_dict(objs) == [{"a": 1}, {"b": 2}]


def test_as_dict_rejects_non_models() -> None:
    with pytest.raises(TypeError, match="APIObject"):
        as_dict([APIObject({"a": 1}), object()])  # type: ignore[list-item]


def test_as_dict_deep_copy_is_detached() -> None:
    obj = APIObject({"nested": {"k": 1}})
    plain = as_dict(obj, deep_copy=True)
    plain["nested"]["k"] = 2
    assert obj.nested.k == 1
