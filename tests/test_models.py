from gitcode_api._models import APIObject


def test_apiobject_wraps_nested_dicts_and_lists() -> None:
    payload = APIObject(
        {
            "name": "GitCode-API",
            "owner": {"login": "SushiNinja"},
            "branches": [{"name": "main"}, {"name": "dev"}],
        }
    )

    assert payload.name == "GitCode-API"
    assert payload.owner.login == "SushiNinja"
    assert payload.branches[0].name == "main"
    assert payload.to_dict()["name"] == "GitCode-API"
