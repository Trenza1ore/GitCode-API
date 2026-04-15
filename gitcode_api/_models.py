"""Lightweight wrappers and typed payload hints for GitCode API responses."""

from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Mapping, MutableMapping, TypedDict, TypeVar, Union

JsonValue = Any


def _wrap_value(value: Any) -> Any:
    """Recursively wrap nested dicts and lists in SDK helper objects."""
    if isinstance(value, dict):
        return APIObject(dict(value))
    if isinstance(value, list):
        return [_wrap_value(item) for item in value]
    return value


@dataclass
class APIObject(Mapping[str, Any]):
    """Dictionary-backed wrapper around GitCode JSON objects.

    The object behaves like a mapping while also allowing attribute access for
    top-level keys returned by the API.
    """

    data: MutableMapping[str, Any]

    def __getitem__(self, key: str) -> Any:
        """Return a wrapped item by key."""
        return _wrap_value(self.data[key])

    def __iter__(self) -> Iterator[str]:
        """Iterate over keys in the underlying mapping."""
        return iter(self.data)

    def __len__(self) -> int:
        """Return the number of top-level keys."""
        return len(self.data)

    def __getattr__(self, name: str) -> Any:
        """Provide attribute-style access to top-level JSON keys."""
        try:
            return _wrap_value(self.data[name])
        except KeyError as exc:
            raise AttributeError(name) from exc

    def get(self, key: str, default: Any = None) -> Any:
        """Return a wrapped value with an optional default."""
        return _wrap_value(self.data.get(key, default))

    def to_dict(self) -> Dict[str, Any]:
        """Return a shallow ``dict`` copy of the underlying payload."""
        return dict(self.data)


ModelT = TypeVar("ModelT", bound=APIObject)


def as_model(data: Mapping[str, Any], model_type: type[ModelT]) -> ModelT:
    """Wrap a mapping in the requested SDK model type."""
    return model_type(dict(data))


def as_model_list(data: List[Mapping[str, Any]], model_type: type[ModelT]) -> List[ModelT]:
    """Wrap a list of mappings in the requested SDK model type."""
    return [as_model(item, model_type) for item in data]


class RepositoryCreateParams(TypedDict, total=False):
    """Typed fields accepted by repository creation endpoints."""

    name: str
    description: str
    has_issues: bool
    has_wiki: bool
    auto_init: bool
    gitignore_template: str
    license_template: str
    path: str
    private: bool
    public: int
    default_branch: str
    homepage: str
    can_comment: bool


class IssueCreateParams(TypedDict, total=False):
    """Typed fields accepted by issue creation endpoints."""

    title: str
    body: str
    assignee: str
    labels: List[str]
    milestone: Union[int, str]


class PullRequestCreateParams(TypedDict, total=False):
    """Typed fields accepted by pull request creation endpoints."""

    title: str
    body: str
    head: str
    base: str
    assignees: List[str]
    testers: List[str]
    labels: List[str]
    draft: bool


class WebhookCreateParams(TypedDict, total=False):
    """Typed fields accepted by webhook creation endpoints."""

    url: str
    encryption_type: int
    password: str
    push_events: bool
    tag_push_events: bool
    issues_events: bool
    note_events: bool
    merge_requests_events: bool


class User(APIObject):
    """User profile payload returned by user-related endpoints."""


class UserSummary(APIObject):
    """Compact user payload returned by listing endpoints."""


class Repository(APIObject):
    """Repository payload returned by repository endpoints."""


class Contributor(APIObject):
    """Contributor payload returned by repository statistics endpoints."""


class ContentObject(APIObject):
    """Repository content payload for files and directories."""


class CommitResult(APIObject):
    """Commit result payload returned by content write operations."""


class Tree(APIObject):
    """Git tree payload."""


class Blob(APIObject):
    """Git blob payload."""


class Branch(APIObject):
    """Repository branch payload."""


class ProtectedBranch(APIObject):
    """Protected branch configuration payload."""


class Commit(APIObject):
    """Commit payload."""


class CommitComparison(APIObject):
    """Commit comparison payload."""


class CommitComment(APIObject):
    """Commit comment payload."""


class Issue(APIObject):
    """Issue payload."""


class IssueComment(APIObject):
    """Issue comment payload."""


class IssueOperationLog(APIObject):
    """Issue operation log payload."""


class PullRequest(APIObject):
    """Pull request payload."""


class PullRequestFile(APIObject):
    """Pull request file diff payload."""


class PullRequestComment(APIObject):
    """Pull request comment payload."""


class PullRequestReview(APIObject):
    """Pull request review payload."""


class PullRequestTest(APIObject):
    """Pull request test request payload."""


class MergeResult(APIObject):
    """Merge operation result payload."""


class MergeStatus(APIObject):
    """Merge status payload."""


class Label(APIObject):
    """Label payload."""


class Milestone(APIObject):
    """Milestone payload."""


class RepoMember(APIObject):
    """Repository member payload."""


class RepoMemberPermission(APIObject):
    """Repository member permission payload."""


class Release(APIObject):
    """Release payload."""


class Tag(APIObject):
    """Tag payload."""


class ProtectedTag(APIObject):
    """Protected tag configuration payload."""


class Webhook(APIObject):
    """Webhook payload."""


class Organization(APIObject):
    """Organization payload."""


class OrganizationMembership(APIObject):
    """Organization membership payload."""


class EnterpriseMember(APIObject):
    """Enterprise member payload."""


class Namespace(APIObject):
    """Namespace payload."""


class Email(APIObject):
    """Email payload for the authenticated user."""


class OAuthToken(APIObject):
    """OAuth token payload."""


class SearchResult(APIObject):
    """Search result payload."""
