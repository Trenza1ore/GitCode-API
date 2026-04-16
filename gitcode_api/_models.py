"""Typed response models for the GitCode SDK."""

from dataclasses import MISSING, dataclass, field, fields
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Mapping,
    MutableMapping,
    Optional,
    TypedDict,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

JsonValue = Any


def _wrap_value(value: Any) -> Any:
    """Recursively wrap untyped nested dicts and lists."""
    if isinstance(value, dict):
        return APIObject(dict(value))
    if isinstance(value, list):
        return [_wrap_value(item) for item in value]
    return value


def _coerce_value(value: Any, annotation: Any) -> Any:
    """Best-effort conversion from raw JSON into typed model fields."""
    if value is None:
        return None

    if annotation in (Any, object):
        return _wrap_value(value)

    origin = get_origin(annotation)
    if origin in (list, List):
        item_type = get_args(annotation)[0] if get_args(annotation) else Any
        if not isinstance(value, list):
            return value
        return [_coerce_value(item, item_type) for item in value]

    if origin in (dict, Dict, Mapping, MutableMapping):
        if isinstance(value, dict):
            return dict(value)
        return value

    if origin is Union:
        for candidate in get_args(annotation):
            if candidate is type(None):
                continue
            coerced = _coerce_value(value, candidate)
            if coerced is not value:
                return coerced
            if isinstance(candidate, type) and isinstance(value, candidate):
                return value
        return _wrap_value(value)

    if isinstance(annotation, type) and issubclass(annotation, APIObject) and isinstance(value, dict):
        return annotation(dict(value))

    return value


@dataclass(init=False)
class APIObject(Mapping[str, Any]):
    """Dictionary-backed wrapper around GitCode JSON objects."""

    data: MutableMapping[str, Any] = field(init=False, repr=False)

    def __init__(self, data: Mapping[str, Any]):
        payload = dict(data)
        object.__setattr__(self, "data", payload)
        type_hints = get_type_hints(self.__class__)

        for model_field in fields(self):
            if model_field.name == "data":
                continue

            field_type = type_hints.get(model_field.name, model_field.type)
            if model_field.name in payload:
                raw_value = payload[model_field.name]
                value = _coerce_value(raw_value, field_type)
            elif model_field.default is not MISSING:
                value = model_field.default
            elif model_field.default_factory is not MISSING:  # type: ignore[misc]
                value = model_field.default_factory()  # type: ignore[misc]
            else:
                value = None

            object.__setattr__(self, model_field.name, value)

    def __getitem__(self, key: str) -> Any:
        return _wrap_value(self.data[key])

    def __iter__(self) -> Iterator[str]:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __getattr__(self, name: str) -> Any:
        try:
            return _wrap_value(self.data[name])
        except KeyError as exc:
            raise AttributeError(name) from exc

    def get(self, key: str, default: Any = None) -> Any:
        return _wrap_value(self.data.get(key, default))

    def to_dict(self) -> Dict[str, Any]:
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


@dataclass(init=False)
class UserRef(APIObject):
    """Compact user payload embedded in other responses."""

    id: Optional[Union[int, str]] = None
    login: Optional[str] = None
    name: Optional[str] = None
    username: Optional[str] = None
    type: Optional[str] = None
    html_url: Optional[str] = None
    avatar_url: Optional[str] = None
    email: Optional[str] = None
    state: Optional[str] = None
    member_role: Optional[str] = None
    remark: Optional[str] = None
    url: Optional[str] = None
    web_url: Optional[str] = None
    name_cn: Optional[str] = None
    avatar_path: Optional[str] = None
    tenant_name: Optional[str] = None
    is_member: Optional[bool] = None
    assignee: Optional[bool] = None
    code_owner: Optional[bool] = None
    accept: Optional[bool] = None


@dataclass(init=False)
class User(UserRef):
    """User profile payload returned by user-related endpoints."""

    followers_url: Optional[str] = None
    following_url: Optional[str] = None
    gists_url: Optional[str] = None
    organizations_url: Optional[str] = None
    received_events_url: Optional[str] = None
    repos_url: Optional[str] = None
    starred_url: Optional[str] = None
    subscriptions_url: Optional[str] = None
    bio: Optional[str] = None
    blog: Optional[str] = None
    company: Optional[str] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    top_languages: Optional[List[str]] = None


@dataclass(init=False)
class UserSummary(APIObject):
    """Compact user payload returned by stargazer/subscriber endpoints."""

    id: Optional[Union[int, str]] = None
    login: Optional[str] = None
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    html_url: Optional[str] = None
    type: Optional[str] = None


@dataclass(init=False)
class NamespaceDetails(APIObject):
    """Namespace object embedded in repository payloads."""

    id: Optional[Union[int, str]] = None
    type: Optional[str] = None
    name: Optional[str] = None
    path: Optional[str] = None
    html_url: Optional[str] = None
    develop_mode: Optional[str] = None
    region: Optional[str] = None
    cell: Optional[str] = None
    kind: Optional[str] = None
    full_path: Optional[str] = None
    full_name: Optional[str] = None
    parent_id: Optional[Union[int, str]] = None
    visibility_level: Optional[int] = None
    enable_file_control: Optional[bool] = None
    owner_id: Optional[Union[int, str]] = None


@dataclass(init=False)
class Namespace(APIObject):
    """Namespace payload returned by the namespace lookup endpoint."""

    id: Optional[Union[int, str]] = None
    path: Optional[str] = None
    name: Optional[str] = None
    html_url: Optional[str] = None
    type: Optional[str] = None


@dataclass(init=False)
class RepositoryPermission(APIObject):
    """Repository permission summary."""

    pull: Optional[bool] = None
    push: Optional[bool] = None
    admin: Optional[bool] = None


@dataclass(init=False)
class EnterpriseRef(APIObject):
    """Enterprise summary embedded in repository search results."""

    id: Optional[Union[int, str]] = None
    path: Optional[str] = None
    html_url: Optional[str] = None
    type: Optional[str] = None


@dataclass(init=False)
class Repository(APIObject):
    """Repository payload returned by repository endpoints."""

    id: Optional[Union[int, str]] = None
    full_name: Optional[str] = None
    human_name: Optional[str] = None
    path: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    namespace: Optional[NamespaceDetails] = None
    owner: Optional[UserRef] = None
    private: Optional[bool] = None
    public: Optional[Union[bool, int]] = None
    internal: Optional[bool] = None
    fork: Optional[bool] = None
    html_url: Optional[str] = None
    web_url: Optional[str] = None
    url: Optional[str] = None
    ssh_url_to_repo: Optional[str] = None
    http_url_to_repo: Optional[str] = None
    forks_count: Optional[int] = None
    stargazers_count: Optional[int] = None
    watchers_count: Optional[int] = None
    default_branch: Optional[str] = None
    open_issues_count: Optional[int] = None
    license: Optional[APIObject] = None
    project_creator: Optional[str] = None
    pushed_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    homepage: Optional[str] = None
    status: Optional[str] = None
    relation: Optional[str] = None
    members: Optional[List[str]] = None
    permission: Optional[RepositoryPermission] = None
    enterprise: Optional[Union[EnterpriseRef, str]] = None
    issue_template_source: Optional[str] = None
    has_issue: Optional[bool] = None
    assigner: Optional[UserRef] = None
    assignee: Optional[UserRef] = None
    assignees_number: Optional[int] = None
    testers_number: Optional[int] = None
    testers: Optional[List[UserRef]] = None
    paas: Optional[APIObject] = None


@dataclass(init=False)
class SearchRepository(APIObject):
    """Repository search result payload."""

    id: Optional[Union[int, str]] = None
    full_name: Optional[str] = None
    human_name: Optional[str] = None
    url: Optional[str] = None
    namespace: Optional[Namespace] = None
    path: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    ssh_url_to_repo: Optional[str] = None
    http_url_to_repo: Optional[str] = None
    web_url: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    homepage: Optional[str] = None
    members: Optional[List[str]] = None
    forks_count: Optional[int] = None
    stargazers_count: Optional[int] = None
    relation: Optional[str] = None
    permission: Optional[RepositoryPermission] = None
    internal: Optional[bool] = None
    open_issues_count: Optional[int] = None
    has_issue: Optional[bool] = None
    watchers_count: Optional[int] = None
    enterprise: Optional[EnterpriseRef] = None
    default_branch: Optional[str] = None
    fork: Optional[bool] = None
    pushed_at: Optional[str] = None
    owner: Optional[UserSummary] = None
    issue_template_source: Optional[str] = None
    private: Optional[bool] = None
    public: Optional[bool] = None


@dataclass(init=False)
class Contributor(APIObject):
    """Contributor payload returned by repository statistics endpoints."""

    name: Optional[str] = None
    contributions: Optional[int] = None
    email: Optional[str] = None


@dataclass(init=False)
class ContentLinks(APIObject):
    """Repository content link bundle."""

    self: Optional[str] = None
    html: Optional[str] = None
    git: Optional[str] = None
    download: Optional[str] = None


@dataclass(init=False)
class ContentObject(APIObject):
    """Repository content payload for files and directories."""

    type: Optional[str] = None
    encoding: Optional[str] = None
    size: Optional[int] = None
    name: Optional[str] = None
    path: Optional[str] = None
    content: Optional[str] = None
    sha: Optional[str] = None
    url: Optional[str] = None
    html_url: Optional[str] = None
    download_url: Optional[str] = None
    _links: Optional[ContentLinks] = None


@dataclass(init=False)
class CommitIdentity(APIObject):
    """Commit author/committer identity."""

    name: Optional[str] = None
    email: Optional[str] = None
    date: Optional[str] = None


@dataclass(init=False)
class CommitParent(APIObject):
    """Commit parent reference."""

    sha: Optional[str] = None
    url: Optional[str] = None


@dataclass(init=False)
class CommitTreeRef(APIObject):
    """Tree reference embedded in commit summaries."""

    sha: Optional[str] = None
    url: Optional[str] = None


@dataclass(init=False)
class CommitPayload(APIObject):
    """Nested commit metadata."""

    author: Optional[CommitIdentity] = None
    committer: Optional[CommitIdentity] = None
    tree: Optional[CommitTreeRef] = None
    message: Optional[str] = None


@dataclass(init=False)
class ContentWriteCommit(APIObject):
    """Commit object returned by content write endpoints."""

    sha: Optional[str] = None
    author: Optional[CommitIdentity] = None
    committer: Optional[CommitIdentity] = None
    message: Optional[str] = None
    parents: Optional[List[CommitParent]] = None


@dataclass(init=False)
class CommitResult(APIObject):
    """Commit result payload returned by content write operations."""

    content: Optional[ContentObject] = None
    commit: Optional[ContentWriteCommit] = None


@dataclass(init=False)
class TreeEntry(APIObject):
    """Git tree entry."""

    sha: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    path: Optional[str] = None
    mode: Optional[str] = None
    md5: Optional[str] = None


@dataclass(init=False)
class Tree(APIObject):
    """Git tree payload."""

    tree: Optional[List[TreeEntry]] = None


@dataclass(init=False)
class Blob(APIObject):
    """Git blob payload."""

    sha: Optional[str] = None
    size: Optional[int] = None
    encoding: Optional[str] = None
    content: Optional[str] = None


@dataclass(init=False)
class BranchListCommit(APIObject):
    """Nested branch summary commit payload."""

    commit: Optional[CommitPayload] = None
    sha: Optional[str] = None
    url: Optional[str] = None


@dataclass(init=False)
class Branch(APIObject):
    """Repository branch payload returned by list/create endpoints."""

    name: Optional[str] = None
    commit: Optional[BranchListCommit] = None
    protected: Optional[bool] = None


@dataclass(init=False)
class BranchDetailCommit(APIObject):
    """Commit object returned inside branch detail responses."""

    id: Optional[str] = None
    message: Optional[str] = None
    parent_ids: Optional[List[str]] = None
    authored_date: Optional[str] = None
    author_name: Optional[str] = None
    author_iam_id: Optional[str] = None
    author_email: Optional[str] = None
    author_user_name: Optional[str] = None
    committed_date: Optional[str] = None
    committer_name: Optional[str] = None
    committer_email: Optional[str] = None
    committer_user_name: Optional[str] = None
    open_gpg_verified: Optional[bool] = None
    verification_status: Optional[str] = None
    gpg_primary_key_id: Optional[str] = None
    short_id: Optional[str] = None
    created_at: Optional[str] = None
    title: Optional[str] = None
    author_avatar_url: Optional[str] = None
    committer_avatar_url: Optional[str] = None
    relate_url: Optional[str] = None


@dataclass(init=False)
class BranchDetail(APIObject):
    """Repository branch payload returned by the detail endpoint."""

    name: Optional[str] = None
    commit: Optional[BranchDetailCommit] = None
    merged: Optional[bool] = None
    protected: Optional[bool] = None
    developers_can_push: Optional[bool] = None
    developers_can_merge: Optional[bool] = None
    can_push: Optional[bool] = None
    default: Optional[bool] = None


@dataclass(init=False)
class ProtectedBranch(APIObject):
    """Protected branch configuration payload."""

    name: Optional[str] = None
    updated_at: Optional[str] = None
    push_users: Optional[Union[List[UserRef], List[Any]]] = None
    merge_users: Optional[Union[List[UserRef], List[Any]]] = None
    merged: Optional[bool] = None
    developers_can_push: Optional[bool] = None
    developers_can_merge: Optional[bool] = None
    committer_can_push: Optional[bool] = None
    committer_can_merge: Optional[bool] = None
    master_can_push: Optional[bool] = None
    master_can_merge: Optional[bool] = None
    maintainer_can_push: Optional[bool] = None
    maintainer_can_merge: Optional[bool] = None
    owner_can_push: Optional[bool] = None
    owner_can_merge: Optional[bool] = None
    no_one_can_push: Optional[bool] = None
    no_one_can_merge: Optional[bool] = None


@dataclass(init=False)
class CommitAuthorSummary(APIObject):
    """Author summary on commit/search payloads."""

    id: Optional[Union[int, str]] = None
    login: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    email: Optional[str] = None
    date: Optional[str] = None


@dataclass(init=False)
class CommitStats(APIObject):
    """Commit diff stats."""

    additions: Optional[int] = None
    deletions: Optional[int] = None
    total: Optional[int] = None


@dataclass(init=False)
class CommitFile(APIObject):
    """Commit file entry."""

    filename: Optional[str] = None
    raw_url: Optional[str] = None
    content_url: Optional[str] = None


@dataclass(init=False)
class CommitSummary(APIObject):
    """Commit payload returned by list endpoints."""

    url: Optional[str] = None
    sha: Optional[str] = None
    html_url: Optional[str] = None
    comments_url: Optional[str] = None
    commit: Optional[CommitPayload] = None
    author: Optional[CommitAuthorSummary] = None
    committer: Optional[CommitAuthorSummary] = None
    parents: Optional[List[CommitParent]] = None


@dataclass(init=False)
class Commit(CommitSummary):
    """Commit payload returned by detail endpoints."""

    stats: Optional[CommitStats] = None
    files: Optional[List[CommitFile]] = None
    id: Optional[str] = None
    message: Optional[str] = None
    parent_ids: Optional[List[str]] = None
    authored_date: Optional[str] = None
    author_name: Optional[str] = None
    author_iam_id: Optional[str] = None
    author_email: Optional[str] = None
    author_user_name: Optional[str] = None
    committed_date: Optional[str] = None
    committer_name: Optional[str] = None
    committer_email: Optional[str] = None
    committer_user_name: Optional[str] = None
    open_gpg_verified: Optional[bool] = None
    verification_status: Optional[str] = None
    gpg_primary_key_id: Optional[str] = None
    short_id: Optional[str] = None
    created_at: Optional[str] = None
    title: Optional[str] = None
    author_avatar_url: Optional[str] = None
    committer_avatar_url: Optional[str] = None
    relate_url: Optional[str] = None


@dataclass(init=False)
class CommitComparison(APIObject):
    """Commit comparison payload."""

    base_commit: Optional[CommitSummary] = None
    merge_base_commit: Optional[CommitSummary] = None
    commits: Optional[List[CommitSummary]] = None
    files: Optional[List[CommitFile]] = None
    status: Optional[str] = None
    ahead_by: Optional[int] = None
    behind_by: Optional[int] = None
    total_commits: Optional[int] = None
    commits_count: Optional[int] = None


@dataclass(init=False)
class CommitComment(APIObject):
    """Commit comment payload."""

    id: Optional[Union[int, str]] = None
    body: Optional[str] = None
    user: Optional[UserRef] = None
    commit_id: Optional[str] = None
    path: Optional[str] = None
    position: Optional[int] = None
    line: Optional[int] = None
    noteable_id: Optional[int] = None
    noteable_type: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    html_url: Optional[str] = None
    target: Optional[APIObject] = None


@dataclass(init=False)
class Label(APIObject):
    """Label payload."""

    id: Optional[Union[int, str]] = None
    name: Optional[str] = None
    title: Optional[str] = None
    color: Optional[str] = None
    repository_id: Optional[int] = None
    type: Optional[str] = None
    text_color: Optional[str] = None


@dataclass(init=False)
class RepositorySummary(APIObject):
    """Minimal repository payload embedded in issue/search responses."""

    id: Optional[Union[int, str]] = None
    full_name: Optional[str] = None
    human_name: Optional[str] = None
    path: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    owner: Optional[Union[UserSummary, UserRef]] = None


@dataclass(init=False)
class Issue(APIObject):
    """Issue payload."""

    id: Optional[Union[int, str]] = None
    html_url: Optional[str] = None
    number: Optional[Union[int, str]] = None
    state: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None
    user: Optional[Union[User, UserRef]] = None
    assignee: Optional[Union[User, UserRef]] = None
    repository: Optional[RepositorySummary] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    finished_at: Optional[str] = None
    labels: Optional[List[Label]] = None
    priority: Optional[Union[int, str]] = None
    issue_type: Optional[str] = None
    issue_state: Optional[str] = None
    issue_state_detail: Optional[str] = None
    stage: Optional[str] = None
    severity: Optional[str] = None
    comments: Optional[int] = None
    parent_id: Optional[int] = None


@dataclass(init=False)
class SearchIssue(Issue):
    """Issue search result payload."""

    repository: Optional[RepositorySummary] = None


@dataclass(init=False)
class IssueComment(APIObject):
    """Issue comment payload."""

    id: Optional[Union[int, str]] = None
    body: Optional[str] = None
    user: Optional[UserRef] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    target: Optional[APIObject] = None


@dataclass(init=False)
class IssueOperationLog(APIObject):
    """Issue operation log payload."""

    id: Optional[Union[int, str]] = None
    action_type: Optional[str] = None
    content: Optional[str] = None
    created_at: Optional[str] = None
    user: Optional[UserRef] = None


@dataclass(init=False)
class PullRequestBranch(APIObject):
    """Head/base branch payload in pull request responses."""

    label: Optional[str] = None
    ref: Optional[str] = None
    sha: Optional[str] = None
    user: Optional[UserRef] = None
    repo: Optional[Repository] = None


@dataclass(init=False)
class PullRequestApprover(APIObject):
    """Approver/tester embedded in pull request responses."""

    id: Optional[Union[int, str]] = None
    username: Optional[str] = None
    name: Optional[str] = None
    nick_name: Optional[str] = None
    name_cn: Optional[str] = None
    email: Optional[str] = None
    state: Optional[str] = None
    is_codeowner: Optional[bool] = None
    updated_at: Optional[str] = None
    avatar_url: Optional[str] = None


@dataclass(init=False)
class PullRequestTimeStats(APIObject):
    """Time tracking fields embedded in pull requests."""

    time_estimate: Optional[int] = None
    total_time_spent: Optional[int] = None
    human_time_estimate: Optional[str] = None
    human_total_time_spent: Optional[str] = None


@dataclass(init=False)
class PullRequestDiffRefs(APIObject):
    """Diff refs embedded in pull requests."""

    base_sha: Optional[str] = None
    head_sha: Optional[str] = None
    start_sha: Optional[str] = None


@dataclass(init=False)
class PullRequest(APIObject):
    """Pull request payload."""

    number: Optional[Union[int, str]] = None
    id: Optional[Union[int, str]] = None
    iid: Optional[int] = None
    project_id: Optional[int] = None
    html_url: Optional[str] = None
    url: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None
    state: Optional[str] = None
    draft: Optional[bool] = None
    close_related_issue: Optional[bool] = None
    prune_branch: Optional[bool] = None
    labels: Optional[List[Label]] = None
    user: Optional[UserRef] = None
    assignees: Optional[List[UserRef]] = None
    head: Optional[PullRequestBranch] = None
    base: Optional[PullRequestBranch] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    merged_at: Optional[str] = None
    closed_by: Optional[UserRef] = None
    closed_at: Optional[str] = None
    target_branch: Optional[str] = None
    source_branch: Optional[str] = None
    squash_commit_message: Optional[str] = None
    user_notes_count: Optional[int] = None
    upvotes: Optional[int] = None
    downvotes: Optional[int] = None
    source_project_id: Optional[int] = None
    target_project_id: Optional[int] = None
    work_in_progress: Optional[bool] = None
    milestone: Optional[APIObject] = None
    merge_when_pipeline_succeeds: Optional[bool] = None
    merge_status: Optional[str] = None
    sha: Optional[str] = None
    merge_commit_sha: Optional[str] = None
    should_remove_source_branch: Optional[bool] = None
    force_remove_source_branch: Optional[bool] = None
    web_url: Optional[str] = None
    time_stats: Optional[PullRequestTimeStats] = None
    squash: Optional[bool] = None
    merge_request_type: Optional[str] = None
    has_pre_merge_ref: Optional[bool] = None
    review_mode: Optional[str] = None
    is_source_branch_exist: Optional[bool] = None
    approval_merge_request_approvers: Optional[List[PullRequestApprover]] = None
    approval_merge_request_testers: Optional[List[PullRequestApprover]] = None
    added_lines: Optional[int] = None
    removed_lines: Optional[int] = None
    subscribed: Optional[bool] = None
    changes_count: Optional[Union[int, str]] = None
    diff_refs: Optional[PullRequestDiffRefs] = None
    notes: Optional[int] = None
    unresolved_discussions_count: Optional[int] = None
    gate_check: Optional[bool] = None


@dataclass(init=False)
class PullRequestCount(APIObject):
    """Pull request count payload returned when ``only_count`` is enabled."""

    all: Optional[int] = None
    opened: Optional[int] = None
    closed: Optional[int] = None
    merged: Optional[int] = None
    locked: Optional[int] = None


@dataclass(init=False)
class PullRequestFile(APIObject):
    """Pull request file diff payload."""

    filename: Optional[str] = None
    status: Optional[str] = None
    additions: Optional[int] = None
    deletions: Optional[int] = None
    changes: Optional[int] = None
    blob_url: Optional[str] = None
    raw_url: Optional[str] = None
    contents_url: Optional[str] = None
    patch: Optional[str] = None


@dataclass(init=False)
class PullRequestComment(APIObject):
    """Pull request comment payload."""

    id: Optional[Union[int, str]] = None
    body: Optional[str] = None
    user: Optional[UserRef] = None
    path: Optional[str] = None
    position: Optional[int] = None
    commit_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    comment_type: Optional[str] = None
    target: Optional[APIObject] = None


@dataclass(init=False)
class PullRequestReview(APIObject):
    """Pull request review payload."""

    id: Optional[Union[int, str]] = None
    state: Optional[str] = None
    body: Optional[str] = None


@dataclass(init=False)
class PullRequestTest(APIObject):
    """Pull request test request payload."""

    id: Optional[Union[int, str]] = None
    state: Optional[str] = None
    body: Optional[str] = None


@dataclass(init=False)
class MergeResult(APIObject):
    """Merge operation result payload."""

    sha: Optional[str] = None
    merged: Optional[bool] = None
    message: Optional[str] = None


@dataclass(init=False)
class MergeStatus(APIObject):
    """Merge status payload."""

    message: Optional[str] = None
    error: Optional[str] = None


@dataclass(init=False)
class Milestone(APIObject):
    """Milestone payload."""

    id: Optional[Union[int, str]] = None
    number: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    state: Optional[str] = None
    due_on: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass(init=False)
class RepoMemberPermissions(APIObject):
    """Collaborator permissions payload."""

    pull: Optional[bool] = None
    push: Optional[bool] = None
    admin: Optional[bool] = None


@dataclass(init=False)
class RepoMember(APIObject):
    """Repository member payload returned by add/update operations."""

    id: Optional[Union[int, str]] = None
    login: Optional[str] = None
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    html_url: Optional[str] = None
    remark: Optional[str] = None
    type: Optional[str] = None
    permissions: Optional[RepoMemberPermissions] = None


@dataclass(init=False)
class RepoCollaborator(APIObject):
    """Repository collaborator payload returned by list operations."""

    id: Optional[Union[int, str]] = None
    name: Optional[str] = None
    username: Optional[str] = None
    nick_name: Optional[str] = None
    state: Optional[str] = None
    avatar: Optional[str] = None
    avatar_url: Optional[str] = None
    email: Optional[str] = None
    name_cn: Optional[str] = None
    web_url: Optional[str] = None
    access_level: Optional[int] = None
    expires_at: Optional[str] = None
    limited: Optional[bool] = None
    type: Optional[str] = None
    last_owner: Optional[str] = None
    is_current_source_member: Optional[bool] = None
    last_source_owner: Optional[str] = None
    join_way: Optional[str] = None
    source_name: Optional[str] = None
    member_roles: Optional[List[APIObject]] = None
    iam_id: Optional[str] = None
    committer_system_from: Optional[str] = None
    permissions: Optional[RepoMemberPermissions] = None


@dataclass(init=False)
class RepoMemberPermission(APIObject):
    """Repository member permission payload."""

    id: Optional[Union[int, str]] = None
    login: Optional[str] = None
    permission: Optional[str] = None


@dataclass(init=False)
class Release(APIObject):
    """Release payload."""

    id: Optional[Union[int, str]] = None
    tag_name: Optional[str] = None
    name: Optional[str] = None
    body: Optional[str] = None
    author: Optional[UserRef] = None
    created_at: Optional[str] = None
    published_at: Optional[str] = None
    html_url: Optional[str] = None


@dataclass(init=False)
class TagCommit(APIObject):
    """Commit object embedded in tag payloads."""

    sha: Optional[str] = None
    url: Optional[str] = None


@dataclass(init=False)
class Tagger(APIObject):
    """Tagger identity."""

    name: Optional[str] = None
    email: Optional[str] = None
    date: Optional[str] = None


@dataclass(init=False)
class Tag(APIObject):
    """Tag payload."""

    name: Optional[str] = None
    message: Optional[str] = None
    commit: Optional[TagCommit] = None
    tagger: Optional[Tagger] = None


@dataclass(init=False)
class ProtectedTag(APIObject):
    """Protected tag configuration payload."""

    name: Optional[str] = None
    create_access_level: Optional[int] = None
    create_access_level_desc: Optional[str] = None


@dataclass(init=False)
class Webhook(APIObject):
    """Webhook payload."""

    id: Optional[Union[int, str]] = None
    url: Optional[str] = None
    password: Optional[str] = None
    result: Optional[str] = None
    project_id: Optional[int] = None
    result_code: Optional[int] = None
    push_events: Optional[bool] = None
    tag_push_events: Optional[bool] = None
    issues_events: Optional[bool] = None
    note_events: Optional[bool] = None
    merge_requests_events: Optional[bool] = None
    created_at: Optional[str] = None


@dataclass(init=False)
class OrganizationSummary(APIObject):
    """Organization summary payload returned by list endpoints."""

    id: Optional[Union[int, str]] = None
    login: Optional[str] = None
    path: Optional[str] = None
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    repos_url: Optional[str] = None
    events_url: Optional[str] = None
    members_url: Optional[str] = None
    description: Optional[str] = None
    follow_count: Optional[int] = None


@dataclass(init=False)
class Organization(OrganizationSummary):
    """Organization payload."""

    enterprise: Optional[str] = None
    gitee: Optional[APIObject] = None


@dataclass(init=False)
class OrganizationMembership(APIObject):
    """Organization membership payload."""

    id: Optional[Union[int, str]] = None
    path: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    avatar_url: Optional[str] = None
    user: Optional[UserRef] = None
    role: Optional[str] = None
    organization: Optional[OrganizationSummary] = None


@dataclass(init=False)
class EnterpriseMember(APIObject):
    """Enterprise member payload."""

    id: Optional[Union[int, str]] = None
    role: Optional[str] = None
    url: Optional[str] = None
    user: Optional[UserRef] = None
    login: Optional[str] = None
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    html_url: Optional[str] = None


@dataclass(init=False)
class Email(APIObject):
    """Email payload for the authenticated user."""

    email: Optional[str] = None
    state: Optional[str] = None


@dataclass(init=False)
class OAuthToken(APIObject):
    """OAuth token payload."""

    access_token: Optional[str] = None
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    created_at: Optional[str] = None


@dataclass(init=False)
class SearchUser(APIObject):
    """User search result payload."""

    avatar_url: Optional[str] = None
    created_at: Optional[str] = None
    html_url: Optional[str] = None
    id: Optional[Union[int, str]] = None
    login: Optional[str] = None
    name: Optional[str] = None


@dataclass(init=False)
class SearchResult(APIObject):
    """Backward-compatible generic search result payload."""
