from gitcode_api._models import APIObject, Branch, BranchDetail, CommitResult, PullRequestCount, SearchIssue


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


def test_typed_models_coerce_nested_payloads() -> None:
    branch = Branch({"name": "main", "commit": {"sha": "abc123"}})
    detail = BranchDetail({"name": "main", "commit": {"id": "c1", "title": "Initial commit"}})
    result = CommitResult({"content": {"name": "README.md"}, "commit": {"sha": "deadbeef"}})
    counts = PullRequestCount({"all": 3, "opened": 2, "closed": 1, "merged": 0, "locked": 0})
    issue = SearchIssue({"number": "1", "repository": {"full_name": "SushiNinja/GitCode-API"}})

    assert branch.commit.sha == "abc123"
    assert detail.commit.id == "c1"
    assert result.content.name == "README.md"
    assert result.commit.sha == "deadbeef"
    assert counts.opened == 2
    assert issue.repository.full_name == "SushiNinja/GitCode-API"
