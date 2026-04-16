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
    """Compact user payload embedded in other responses.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar login: Account login name.
    :vartype login: Optional[str]
    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar username: Account username.
    :vartype username: Optional[str]
    :ivar type: Type of the object.
    :vartype type: Optional[str]
    :ivar html_url: Web URL for this object.
    :vartype html_url: Optional[str]
    :ivar avatar_url: Avatar image URL.
    :vartype avatar_url: Optional[str]
    :ivar email: Email address.
    :vartype email: Optional[str]
    :ivar state: Current state value.
    :vartype state: Optional[str]
    :ivar member_role: Role of the user within the current repository or organization context.
    :vartype member_role: Optional[str]
    :ivar remark: Remark or note recorded for the user.
    :vartype remark: Optional[str]
    :ivar url: API URL for this object.
    :vartype url: Optional[str]
    :ivar web_url: Web URL for this object.
    :vartype web_url: Optional[str]
    :ivar name_cn: Chinese display name for the user.
    :vartype name_cn: Optional[str]
    :ivar avatar_path: Path to the user avatar resource.
    :vartype avatar_path: Optional[str]
    :ivar tenant_name: Tenant name associated with the user.
    :vartype tenant_name: Optional[str]
    :ivar is_member: Whether the user is a member in the current context.
    :vartype is_member: Optional[bool]
    :ivar assignee: Whether the user can be selected as an assignee.
    :vartype assignee: Optional[bool]
    :ivar code_owner: Whether the user is configured as a code owner.
    :vartype code_owner: Optional[bool]
    :ivar accept: Whether the user has accepted the invitation or request.
    :vartype accept: Optional[bool]
    """

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
    """User profile payload returned by user-related endpoints.

    :ivar followers_url: Followers URL.
    :vartype followers_url: Optional[str]
    :ivar following_url: Following URL.
    :vartype following_url: Optional[str]
    :ivar gists_url: Gists URL.
    :vartype gists_url: Optional[str]
    :ivar organizations_url: Organizations URL.
    :vartype organizations_url: Optional[str]
    :ivar received_events_url: Received events URL.
    :vartype received_events_url: Optional[str]
    :ivar repos_url: Repos URL.
    :vartype repos_url: Optional[str]
    :ivar starred_url: Starred URL.
    :vartype starred_url: Optional[str]
    :ivar subscriptions_url: Subscriptions URL.
    :vartype subscriptions_url: Optional[str]
    :ivar bio: Bio.
    :vartype bio: Optional[str]
    :ivar blog: Blog.
    :vartype blog: Optional[str]
    :ivar company: Company.
    :vartype company: Optional[str]
    :ivar followers: Followers.
    :vartype followers: Optional[int]
    :ivar following: Following.
    :vartype following: Optional[int]
    :ivar top_languages: Top languages.
    :vartype top_languages: Optional[List[str]]
    """

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
    """Compact user payload returned by stargazer/subscriber endpoints.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar login: Account login name.
    :vartype login: Optional[str]
    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar avatar_url: Avatar image URL.
    :vartype avatar_url: Optional[str]
    :ivar html_url: Web URL for this object.
    :vartype html_url: Optional[str]
    :ivar type: Type of the object.
    :vartype type: Optional[str]
    """

    id: Optional[Union[int, str]] = None
    login: Optional[str] = None
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    html_url: Optional[str] = None
    type: Optional[str] = None


@dataclass(init=False)
class NamespaceDetails(APIObject):
    """Namespace object embedded in repository payloads.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar type: Type of the object.
    :vartype type: Optional[str]
    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar path: Repository-relative or namespace path.
    :vartype path: Optional[str]
    :ivar html_url: Web URL for this object.
    :vartype html_url: Optional[str]
    :ivar develop_mode: Development mode configured for the namespace.
    :vartype develop_mode: Optional[str]
    :ivar region: Region.
    :vartype region: Optional[str]
    :ivar cell: Cell identifier of the namespace.
    :vartype cell: Optional[str]
    :ivar kind: Kind of namespace.
    :vartype kind: Optional[str]
    :ivar full_path: Full path for the object.
    :vartype full_path: Optional[str]
    :ivar full_name: Full display name for the object.
    :vartype full_name: Optional[str]
    :ivar parent_id: ID of the parent namespace.
    :vartype parent_id: Optional[Union[int, str]]
    :ivar visibility_level: Visibility level configured for the namespace.
    :vartype visibility_level: Optional[int]
    :ivar enable_file_control: Whether file control is enabled for the namespace.
    :vartype enable_file_control: Optional[bool]
    :ivar owner_id: ID of the namespace owner.
    :vartype owner_id: Optional[Union[int, str]]
    """

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
    """Namespace payload returned by the namespace lookup endpoint.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar path: Repository-relative or namespace path.
    :vartype path: Optional[str]
    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar html_url: Web URL for this object.
    :vartype html_url: Optional[str]
    :ivar type: Type of the object.
    :vartype type: Optional[str]
    """

    id: Optional[Union[int, str]] = None
    path: Optional[str] = None
    name: Optional[str] = None
    html_url: Optional[str] = None
    type: Optional[str] = None


@dataclass(init=False)
class RepositoryPermission(APIObject):
    """Repository permission summary.

    :ivar pull: Pull.
    :vartype pull: Optional[bool]
    :ivar push: Push.
    :vartype push: Optional[bool]
    :ivar admin: Admin.
    :vartype admin: Optional[bool]
    """

    pull: Optional[bool] = None
    push: Optional[bool] = None
    admin: Optional[bool] = None


@dataclass(init=False)
class EnterpriseRef(APIObject):
    """Enterprise summary embedded in repository search results.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar path: Repository-relative or namespace path.
    :vartype path: Optional[str]
    :ivar html_url: Web URL for this object.
    :vartype html_url: Optional[str]
    :ivar type: Type of the object.
    :vartype type: Optional[str]
    """

    id: Optional[Union[int, str]] = None
    path: Optional[str] = None
    html_url: Optional[str] = None
    type: Optional[str] = None


@dataclass(init=False)
class Repository(APIObject):
    """Repository payload returned by repository endpoints.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar full_name: Full display name for the object.
    :vartype full_name: Optional[str]
    :ivar human_name: Human-readable display name.
    :vartype human_name: Optional[str]
    :ivar path: Repository-relative or namespace path.
    :vartype path: Optional[str]
    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar description: Description text.
    :vartype description: Optional[str]
    :ivar namespace: Namespace that contains the repository.
    :vartype namespace: Optional[NamespaceDetails]
    :ivar owner: Owner of the object.
    :vartype owner: Optional[UserRef]
    :ivar private: Whether the repository is private.
    :vartype private: Optional[bool]
    :ivar public: Whether the repository is public.
    :vartype public: Optional[Union[bool, int]]
    :ivar internal: Whether the repository is internal.
    :vartype internal: Optional[bool]
    :ivar fork: Whether the repository is a fork.
    :vartype fork: Optional[bool]
    :ivar html_url: Web URL for this object.
    :vartype html_url: Optional[str]
    :ivar web_url: Web URL for this object.
    :vartype web_url: Optional[str]
    :ivar url: API URL for this object.
    :vartype url: Optional[str]
    :ivar ssh_url_to_repo: Ssh url to repo.
    :vartype ssh_url_to_repo: Optional[str]
    :ivar http_url_to_repo: Http url to repo.
    :vartype http_url_to_repo: Optional[str]
    :ivar forks_count: Number of forks.
    :vartype forks_count: Optional[int]
    :ivar stargazers_count: Number of stargazers.
    :vartype stargazers_count: Optional[int]
    :ivar watchers_count: Number of watchers.
    :vartype watchers_count: Optional[int]
    :ivar default_branch: Default branch name.
    :vartype default_branch: Optional[str]
    :ivar open_issues_count: Number of open issues.
    :vartype open_issues_count: Optional[int]
    :ivar license: License.
    :vartype license: Optional[APIObject]
    :ivar project_creator: Login or identifier of the repository creator.
    :vartype project_creator: Optional[str]
    :ivar pushed_at: Timestamp of the most recent push.
    :vartype pushed_at: Optional[str]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar updated_at: Timestamp when this object was last updated.
    :vartype updated_at: Optional[str]
    :ivar homepage: Homepage URL configured for the repository.
    :vartype homepage: Optional[str]
    :ivar status: Status string returned by the API.
    :vartype status: Optional[str]
    :ivar relation: Relationship between the current user and the repository.
    :vartype relation: Optional[str]
    :ivar members: Members returned in the repository payload.
    :vartype members: Optional[List[str]]
    :ivar permission: Permission summary for this object.
    :vartype permission: Optional[RepositoryPermission]
    :ivar enterprise: Enterprise associated with the repository.
    :vartype enterprise: Optional[Union[EnterpriseRef, str]]
    :ivar issue_template_source: Source of the issue template project.
    :vartype issue_template_source: Optional[str]
    :ivar has_issue: Whether issue tracking is enabled for the repository.
    :vartype has_issue: Optional[bool]
    :ivar assigner: User who assigned reviewers or assignees.
    :vartype assigner: Optional[UserRef]
    :ivar assignee: Assigned user.
    :vartype assignee: Optional[UserRef]
    :ivar assignees_number: Number of configured assignees.
    :vartype assignees_number: Optional[int]
    :ivar testers_number: Number of configured testers.
    :vartype testers_number: Optional[int]
    :ivar testers: Users configured as testers.
    :vartype testers: Optional[List[UserRef]]
    :ivar paas: PaaS metadata attached to the repository.
    :vartype paas: Optional[APIObject]
    """

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
    """Repository search result payload.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar full_name: Full display name for the object.
    :vartype full_name: Optional[str]
    :ivar human_name: Human-readable display name.
    :vartype human_name: Optional[str]
    :ivar url: API URL for this object.
    :vartype url: Optional[str]
    :ivar namespace: Namespace.
    :vartype namespace: Optional[Namespace]
    :ivar path: Repository-relative or namespace path.
    :vartype path: Optional[str]
    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar description: Description text.
    :vartype description: Optional[str]
    :ivar status: Status string returned by the API.
    :vartype status: Optional[str]
    :ivar ssh_url_to_repo: Ssh url to repo.
    :vartype ssh_url_to_repo: Optional[str]
    :ivar http_url_to_repo: Http url to repo.
    :vartype http_url_to_repo: Optional[str]
    :ivar web_url: Web URL for this object.
    :vartype web_url: Optional[str]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar updated_at: Timestamp when this object was last updated.
    :vartype updated_at: Optional[str]
    :ivar homepage: Homepage URL configured for the repository.
    :vartype homepage: Optional[str]
    :ivar members: Members.
    :vartype members: Optional[List[str]]
    :ivar forks_count: Number of forks.
    :vartype forks_count: Optional[int]
    :ivar stargazers_count: Number of stargazers.
    :vartype stargazers_count: Optional[int]
    :ivar relation: Relationship between the current user and the repository.
    :vartype relation: Optional[str]
    :ivar permission: Permission summary for this object.
    :vartype permission: Optional[RepositoryPermission]
    :ivar internal: Whether the repository is internal.
    :vartype internal: Optional[bool]
    :ivar open_issues_count: Number of open issues.
    :vartype open_issues_count: Optional[int]
    :ivar has_issue: Whether the object has issue.
    :vartype has_issue: Optional[bool]
    :ivar watchers_count: Number of watchers.
    :vartype watchers_count: Optional[int]
    :ivar enterprise: Enterprise.
    :vartype enterprise: Optional[EnterpriseRef]
    :ivar default_branch: Default branch name.
    :vartype default_branch: Optional[str]
    :ivar fork: Whether the repository is a fork.
    :vartype fork: Optional[bool]
    :ivar pushed_at: Timestamp of the most recent push.
    :vartype pushed_at: Optional[str]
    :ivar owner: Owner of the object.
    :vartype owner: Optional[UserSummary]
    :ivar issue_template_source: Source of the issue template project.
    :vartype issue_template_source: Optional[str]
    :ivar private: Whether the repository is private.
    :vartype private: Optional[bool]
    :ivar public: Whether the repository is public.
    :vartype public: Optional[bool]
    """

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
    """Contributor payload returned by repository statistics endpoints.

    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar contributions: Contributions.
    :vartype contributions: Optional[int]
    :ivar email: Email address.
    :vartype email: Optional[str]
    """

    name: Optional[str] = None
    contributions: Optional[int] = None
    email: Optional[str] = None


@dataclass(init=False)
class ContentLinks(APIObject):
    """Repository content link bundle.

    :ivar self: Self.
    :vartype self: Optional[str]
    :ivar html: Html.
    :vartype html: Optional[str]
    :ivar git: Git.
    :vartype git: Optional[str]
    :ivar download: Download.
    :vartype download: Optional[str]
    """

    self: Optional[str] = None
    html: Optional[str] = None
    git: Optional[str] = None
    download: Optional[str] = None


@dataclass(init=False)
class ContentObject(APIObject):
    """Repository content payload for files and directories.

    :ivar type: Type of the object.
    :vartype type: Optional[str]
    :ivar encoding: Encoding used for the content body.
    :vartype encoding: Optional[str]
    :ivar size: Size.
    :vartype size: Optional[int]
    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar path: Repository-relative or namespace path.
    :vartype path: Optional[str]
    :ivar content: Content returned for this object.
    :vartype content: Optional[str]
    :ivar sha: Git SHA value.
    :vartype sha: Optional[str]
    :ivar url: API URL for this object.
    :vartype url: Optional[str]
    :ivar html_url: Web URL for this object.
    :vartype html_url: Optional[str]
    :ivar download_url: Direct download URL for the content.
    :vartype download_url: Optional[str]
    :ivar _links: Related content links returned by the API.
    :vartype _links: Optional[ContentLinks]
    """

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
    """Commit author/committer identity.

    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar email: Email address.
    :vartype email: Optional[str]
    :ivar date: Date.
    :vartype date: Optional[str]
    """

    name: Optional[str] = None
    email: Optional[str] = None
    date: Optional[str] = None


@dataclass(init=False)
class CommitParent(APIObject):
    """Commit parent reference.

    :ivar sha: Git SHA value.
    :vartype sha: Optional[str]
    :ivar url: API URL for this object.
    :vartype url: Optional[str]
    """

    sha: Optional[str] = None
    url: Optional[str] = None


@dataclass(init=False)
class CommitTreeRef(APIObject):
    """Tree reference embedded in commit summaries.

    :ivar sha: Git SHA value.
    :vartype sha: Optional[str]
    :ivar url: API URL for this object.
    :vartype url: Optional[str]
    """

    sha: Optional[str] = None
    url: Optional[str] = None


@dataclass(init=False)
class CommitPayload(APIObject):
    """Nested commit metadata.

    :ivar author: Author associated with this object.
    :vartype author: Optional[CommitIdentity]
    :ivar committer: Committer associated with this object.
    :vartype committer: Optional[CommitIdentity]
    :ivar tree: Tree.
    :vartype tree: Optional[CommitTreeRef]
    :ivar message: Message text returned by the API.
    :vartype message: Optional[str]
    """

    author: Optional[CommitIdentity] = None
    committer: Optional[CommitIdentity] = None
    tree: Optional[CommitTreeRef] = None
    message: Optional[str] = None


@dataclass(init=False)
class ContentWriteCommit(APIObject):
    """Commit object returned by content write endpoints.

    :ivar sha: Git SHA value.
    :vartype sha: Optional[str]
    :ivar author: Author associated with this object.
    :vartype author: Optional[CommitIdentity]
    :ivar committer: Committer associated with this object.
    :vartype committer: Optional[CommitIdentity]
    :ivar message: Message text returned by the API.
    :vartype message: Optional[str]
    :ivar parents: Parents.
    :vartype parents: Optional[List[CommitParent]]
    """

    sha: Optional[str] = None
    author: Optional[CommitIdentity] = None
    committer: Optional[CommitIdentity] = None
    message: Optional[str] = None
    parents: Optional[List[CommitParent]] = None


@dataclass(init=False)
class CommitResult(APIObject):
    """Commit result payload returned by content write operations.

    :ivar content: Content returned for this object.
    :vartype content: Optional[ContentObject]
    :ivar commit: Commit.
    :vartype commit: Optional[ContentWriteCommit]
    """

    content: Optional[ContentObject] = None
    commit: Optional[ContentWriteCommit] = None


@dataclass(init=False)
class TreeEntry(APIObject):
    """Git tree entry.

    :ivar sha: Git SHA value.
    :vartype sha: Optional[str]
    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar type: Type of the object.
    :vartype type: Optional[str]
    :ivar path: Repository-relative or namespace path.
    :vartype path: Optional[str]
    :ivar mode: Mode.
    :vartype mode: Optional[str]
    :ivar md5: Md5.
    :vartype md5: Optional[str]
    """

    sha: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    path: Optional[str] = None
    mode: Optional[str] = None
    md5: Optional[str] = None


@dataclass(init=False)
class Tree(APIObject):
    """Git tree payload.

    :ivar tree: Tree.
    :vartype tree: Optional[List[TreeEntry]]
    """

    tree: Optional[List[TreeEntry]] = None


@dataclass(init=False)
class Blob(APIObject):
    """Git blob payload.

    :ivar sha: Git SHA value.
    :vartype sha: Optional[str]
    :ivar size: Size.
    :vartype size: Optional[int]
    :ivar encoding: Encoding.
    :vartype encoding: Optional[str]
    :ivar content: Content returned for this object.
    :vartype content: Optional[str]
    """

    sha: Optional[str] = None
    size: Optional[int] = None
    encoding: Optional[str] = None
    content: Optional[str] = None


@dataclass(init=False)
class BranchListCommit(APIObject):
    """Nested branch summary commit payload.

    :ivar commit: Commit.
    :vartype commit: Optional[CommitPayload]
    :ivar sha: Git SHA value.
    :vartype sha: Optional[str]
    :ivar url: API URL for this object.
    :vartype url: Optional[str]
    """

    commit: Optional[CommitPayload] = None
    sha: Optional[str] = None
    url: Optional[str] = None


@dataclass(init=False)
class Branch(APIObject):
    """Repository branch payload returned by list/create endpoints.

    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar commit: Commit.
    :vartype commit: Optional[BranchListCommit]
    :ivar protected: Whether the branch is protected.
    :vartype protected: Optional[bool]
    """

    name: Optional[str] = None
    commit: Optional[BranchListCommit] = None
    protected: Optional[bool] = None


@dataclass(init=False)
class BranchDetailCommit(APIObject):
    """Commit object returned inside branch detail responses.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[str]
    :ivar message: Message text returned by the API.
    :vartype message: Optional[str]
    :ivar parent_ids: Parent commit IDs.
    :vartype parent_ids: Optional[List[str]]
    :ivar authored_date: Timestamp when the commit was authored.
    :vartype authored_date: Optional[str]
    :ivar author_name: Author name.
    :vartype author_name: Optional[str]
    :ivar author_iam_id: IAM identifier of the commit author.
    :vartype author_iam_id: Optional[str]
    :ivar author_email: Author email.
    :vartype author_email: Optional[str]
    :ivar author_user_name: Username of the commit author.
    :vartype author_user_name: Optional[str]
    :ivar committed_date: Timestamp when the commit was committed.
    :vartype committed_date: Optional[str]
    :ivar committer_name: Committer name.
    :vartype committer_name: Optional[str]
    :ivar committer_email: Committer email.
    :vartype committer_email: Optional[str]
    :ivar committer_user_name: Username of the committer.
    :vartype committer_user_name: Optional[str]
    :ivar open_gpg_verified: Whether OpenGPG verification is enabled for the commit.
    :vartype open_gpg_verified: Optional[bool]
    :ivar verification_status: Signature verification status for the commit.
    :vartype verification_status: Optional[str]
    :ivar gpg_primary_key_id: Primary GPG key ID used for verification.
    :vartype gpg_primary_key_id: Optional[str]
    :ivar short_id: Short commit identifier.
    :vartype short_id: Optional[str]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar title: Title of the object.
    :vartype title: Optional[str]
    :ivar author_avatar_url: Avatar URL of the commit author.
    :vartype author_avatar_url: Optional[str]
    :ivar committer_avatar_url: Avatar URL of the committer.
    :vartype committer_avatar_url: Optional[str]
    :ivar relate_url: Related web URL for the commit.
    :vartype relate_url: Optional[str]
    """

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
    """Repository branch payload returned by the detail endpoint.

    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar commit: Commit.
    :vartype commit: Optional[BranchDetailCommit]
    :ivar merged: Merged.
    :vartype merged: Optional[bool]
    :ivar protected: Whether the branch is protected.
    :vartype protected: Optional[bool]
    :ivar developers_can_push: Developers can push.
    :vartype developers_can_push: Optional[bool]
    :ivar developers_can_merge: Developers can merge.
    :vartype developers_can_merge: Optional[bool]
    :ivar can_push: Whether the current user can push.
    :vartype can_push: Optional[bool]
    :ivar default: Whether this is the default branch.
    :vartype default: Optional[bool]
    """

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
    """Protected branch configuration payload.

    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar updated_at: Timestamp when this object was last updated.
    :vartype updated_at: Optional[str]
    :ivar push_users: Users allowed to push to the protected branch.
    :vartype push_users: Optional[Union[List[UserRef], List[Any]]]
    :ivar merge_users: Users allowed to merge into the protected branch.
    :vartype merge_users: Optional[Union[List[UserRef], List[Any]]]
    :ivar merged: Merged.
    :vartype merged: Optional[bool]
    :ivar developers_can_push: Whether developers can push to the protected branch.
    :vartype developers_can_push: Optional[bool]
    :ivar developers_can_merge: Whether developers can merge into the protected branch.
    :vartype developers_can_merge: Optional[bool]
    :ivar committer_can_push: Whether committers can push to the protected branch.
    :vartype committer_can_push: Optional[bool]
    :ivar committer_can_merge: Whether committers can merge into the protected branch.
    :vartype committer_can_merge: Optional[bool]
    :ivar master_can_push: Whether masters can push to the protected branch.
    :vartype master_can_push: Optional[bool]
    :ivar master_can_merge: Whether masters can merge into the protected branch.
    :vartype master_can_merge: Optional[bool]
    :ivar maintainer_can_push: Whether maintainers can push to the protected branch.
    :vartype maintainer_can_push: Optional[bool]
    :ivar maintainer_can_merge: Whether maintainers can merge into the protected branch.
    :vartype maintainer_can_merge: Optional[bool]
    :ivar owner_can_push: Whether owners can push to the protected branch.
    :vartype owner_can_push: Optional[bool]
    :ivar owner_can_merge: Whether owners can merge into the protected branch.
    :vartype owner_can_merge: Optional[bool]
    :ivar no_one_can_push: Whether pushing is disabled for everyone.
    :vartype no_one_can_push: Optional[bool]
    :ivar no_one_can_merge: Whether merging is disabled for everyone.
    :vartype no_one_can_merge: Optional[bool]
    """

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
    """Author summary on commit/search payloads.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar login: Account login name.
    :vartype login: Optional[str]
    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar type: Type of the object.
    :vartype type: Optional[str]
    :ivar email: Email address.
    :vartype email: Optional[str]
    :ivar date: Date.
    :vartype date: Optional[str]
    """

    id: Optional[Union[int, str]] = None
    login: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    email: Optional[str] = None
    date: Optional[str] = None


@dataclass(init=False)
class CommitStats(APIObject):
    """Commit diff stats.

    :ivar additions: Additions.
    :vartype additions: Optional[int]
    :ivar deletions: Deletions.
    :vartype deletions: Optional[int]
    :ivar total: Total.
    :vartype total: Optional[int]
    """

    additions: Optional[int] = None
    deletions: Optional[int] = None
    total: Optional[int] = None


@dataclass(init=False)
class CommitFile(APIObject):
    """Commit file entry.

    :ivar filename: Filename.
    :vartype filename: Optional[str]
    :ivar raw_url: Raw URL.
    :vartype raw_url: Optional[str]
    :ivar content_url: Content URL.
    :vartype content_url: Optional[str]
    """

    filename: Optional[str] = None
    raw_url: Optional[str] = None
    content_url: Optional[str] = None


@dataclass(init=False)
class CommitSummary(APIObject):
    """Commit payload returned by list endpoints.

    :ivar url: API URL for this object.
    :vartype url: Optional[str]
    :ivar sha: Git SHA value.
    :vartype sha: Optional[str]
    :ivar html_url: Web URL for this object.
    :vartype html_url: Optional[str]
    :ivar comments_url: Comments URL.
    :vartype comments_url: Optional[str]
    :ivar commit: Commit.
    :vartype commit: Optional[CommitPayload]
    :ivar author: Author associated with this object.
    :vartype author: Optional[CommitAuthorSummary]
    :ivar committer: Committer associated with this object.
    :vartype committer: Optional[CommitAuthorSummary]
    :ivar parents: Parents.
    :vartype parents: Optional[List[CommitParent]]
    """

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
    """Commit payload returned by detail endpoints.

    :ivar stats: Stats.
    :vartype stats: Optional[CommitStats]
    :ivar files: Files.
    :vartype files: Optional[List[CommitFile]]
    :ivar id: Unique identifier for this object.
    :vartype id: Optional[str]
    :ivar message: Message text returned by the API.
    :vartype message: Optional[str]
    :ivar parent_ids: Parent ids.
    :vartype parent_ids: Optional[List[str]]
    :ivar authored_date: Authored date.
    :vartype authored_date: Optional[str]
    :ivar author_name: Author name.
    :vartype author_name: Optional[str]
    :ivar author_iam_id: ID of the related author iam.
    :vartype author_iam_id: Optional[str]
    :ivar author_email: Author email.
    :vartype author_email: Optional[str]
    :ivar author_user_name: Author user name.
    :vartype author_user_name: Optional[str]
    :ivar committed_date: Committed date.
    :vartype committed_date: Optional[str]
    :ivar committer_name: Committer name.
    :vartype committer_name: Optional[str]
    :ivar committer_email: Committer email.
    :vartype committer_email: Optional[str]
    :ivar committer_user_name: Committer user name.
    :vartype committer_user_name: Optional[str]
    :ivar open_gpg_verified: Open gpg verified.
    :vartype open_gpg_verified: Optional[bool]
    :ivar verification_status: Verification status.
    :vartype verification_status: Optional[str]
    :ivar gpg_primary_key_id: ID of the related gpg primary key.
    :vartype gpg_primary_key_id: Optional[str]
    :ivar short_id: ID of the related short.
    :vartype short_id: Optional[str]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar title: Title of the object.
    :vartype title: Optional[str]
    :ivar author_avatar_url: Author avatar URL.
    :vartype author_avatar_url: Optional[str]
    :ivar committer_avatar_url: Committer avatar URL.
    :vartype committer_avatar_url: Optional[str]
    :ivar relate_url: Relate URL.
    :vartype relate_url: Optional[str]
    """

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
    """Commit comparison payload.

    :ivar base_commit: Base commit.
    :vartype base_commit: Optional[CommitSummary]
    :ivar merge_base_commit: Merge base commit.
    :vartype merge_base_commit: Optional[CommitSummary]
    :ivar commits: Commits.
    :vartype commits: Optional[List[CommitSummary]]
    :ivar files: Files.
    :vartype files: Optional[List[CommitFile]]
    :ivar status: Status string returned by the API.
    :vartype status: Optional[str]
    :ivar ahead_by: Ahead by.
    :vartype ahead_by: Optional[int]
    :ivar behind_by: Behind by.
    :vartype behind_by: Optional[int]
    :ivar total_commits: Total commits.
    :vartype total_commits: Optional[int]
    :ivar commits_count: Number of commits.
    :vartype commits_count: Optional[int]
    """

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
    """Commit comment payload.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar body: Body text of the object.
    :vartype body: Optional[str]
    :ivar user: User associated with this object.
    :vartype user: Optional[UserRef]
    :ivar commit_id: ID of the related commit.
    :vartype commit_id: Optional[str]
    :ivar path: Repository-relative or namespace path.
    :vartype path: Optional[str]
    :ivar position: Position.
    :vartype position: Optional[int]
    :ivar line: Line.
    :vartype line: Optional[int]
    :ivar noteable_id: ID of the related noteable.
    :vartype noteable_id: Optional[int]
    :ivar noteable_type: Noteable type.
    :vartype noteable_type: Optional[str]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar updated_at: Timestamp when this object was last updated.
    :vartype updated_at: Optional[str]
    :ivar html_url: Web URL for this object.
    :vartype html_url: Optional[str]
    :ivar target: Target.
    :vartype target: Optional[APIObject]
    """

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
    """Label payload.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar title: Title of the object.
    :vartype title: Optional[str]
    :ivar color: Color.
    :vartype color: Optional[str]
    :ivar repository_id: Numeric ID of the related repository.
    :vartype repository_id: Optional[int]
    :ivar type: Type of the object.
    :vartype type: Optional[str]
    :ivar text_color: Text color.
    :vartype text_color: Optional[str]
    """

    id: Optional[Union[int, str]] = None
    name: Optional[str] = None
    title: Optional[str] = None
    color: Optional[str] = None
    repository_id: Optional[int] = None
    type: Optional[str] = None
    text_color: Optional[str] = None


@dataclass(init=False)
class RepositorySummary(APIObject):
    """Minimal repository payload embedded in issue/search responses.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar full_name: Full display name for the object.
    :vartype full_name: Optional[str]
    :ivar human_name: Human-readable display name.
    :vartype human_name: Optional[str]
    :ivar path: Repository-relative or namespace path.
    :vartype path: Optional[str]
    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar url: API URL for this object.
    :vartype url: Optional[str]
    :ivar description: Description text.
    :vartype description: Optional[str]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar updated_at: Timestamp when this object was last updated.
    :vartype updated_at: Optional[str]
    :ivar owner: Owner of the object.
    :vartype owner: Optional[Union[UserSummary, UserRef]]
    """

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
    """Issue payload.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar html_url: Web URL for this object.
    :vartype html_url: Optional[str]
    :ivar number: Sequence number for the object within its repository.
    :vartype number: Optional[Union[int, str]]
    :ivar state: Current state value.
    :vartype state: Optional[str]
    :ivar title: Title of the object.
    :vartype title: Optional[str]
    :ivar body: Body text of the object.
    :vartype body: Optional[str]
    :ivar user: User associated with this object.
    :vartype user: Optional[Union[User, UserRef]]
    :ivar assignee: Assigned user.
    :vartype assignee: Optional[Union[User, UserRef]]
    :ivar repository: Repository.
    :vartype repository: Optional[RepositorySummary]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar updated_at: Timestamp when this object was last updated.
    :vartype updated_at: Optional[str]
    :ivar finished_at: Timestamp when this issue was completed.
    :vartype finished_at: Optional[str]
    :ivar labels: Labels attached to this object.
    :vartype labels: Optional[List[Label]]
    :ivar priority: Priority value of the issue.
    :vartype priority: Optional[Union[int, str]]
    :ivar issue_type: Issue type returned by the API.
    :vartype issue_type: Optional[str]
    :ivar issue_state: Workflow state of the issue.
    :vartype issue_state: Optional[str]
    :ivar issue_state_detail: Detailed workflow state information for the issue.
    :vartype issue_state_detail: Optional[str]
    :ivar stage: Current workflow stage of the issue.
    :vartype stage: Optional[str]
    :ivar severity: Severity level of the issue.
    :vartype severity: Optional[str]
    :ivar comments: Number of comments.
    :vartype comments: Optional[int]
    :ivar parent_id: ID of the parent issue.
    :vartype parent_id: Optional[int]
    """

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
    """Issue search result payload.

    :ivar repository: Repository.
    :vartype repository: Optional[RepositorySummary]
    """

    repository: Optional[RepositorySummary] = None


@dataclass(init=False)
class IssueComment(APIObject):
    """Issue comment payload.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar body: Body text of the object.
    :vartype body: Optional[str]
    :ivar user: User associated with this object.
    :vartype user: Optional[UserRef]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar updated_at: Timestamp when this object was last updated.
    :vartype updated_at: Optional[str]
    :ivar target: Target.
    :vartype target: Optional[APIObject]
    """

    id: Optional[Union[int, str]] = None
    body: Optional[str] = None
    user: Optional[UserRef] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    target: Optional[APIObject] = None


@dataclass(init=False)
class IssueOperationLog(APIObject):
    """Issue operation log payload.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar action_type: Action type.
    :vartype action_type: Optional[str]
    :ivar content: Content returned for this object.
    :vartype content: Optional[str]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar user: User associated with this object.
    :vartype user: Optional[UserRef]
    """

    id: Optional[Union[int, str]] = None
    action_type: Optional[str] = None
    content: Optional[str] = None
    created_at: Optional[str] = None
    user: Optional[UserRef] = None


@dataclass(init=False)
class PullRequestBranch(APIObject):
    """Head/base branch payload in pull request responses.

    :ivar label: Display label for the ref.
    :vartype label: Optional[str]
    :ivar ref: Git ref name.
    :vartype ref: Optional[str]
    :ivar sha: Git SHA value.
    :vartype sha: Optional[str]
    :ivar user: User associated with this object.
    :vartype user: Optional[UserRef]
    :ivar repo: Repo.
    :vartype repo: Optional[Repository]
    """

    label: Optional[str] = None
    ref: Optional[str] = None
    sha: Optional[str] = None
    user: Optional[UserRef] = None
    repo: Optional[Repository] = None


@dataclass(init=False)
class PullRequestApprover(APIObject):
    """Approver/tester embedded in pull request responses.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar username: Account username.
    :vartype username: Optional[str]
    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar nick_name: Nickname of the approver or tester.
    :vartype nick_name: Optional[str]
    :ivar name_cn: Chinese display name of the approver or tester.
    :vartype name_cn: Optional[str]
    :ivar email: Email address.
    :vartype email: Optional[str]
    :ivar state: Current state value.
    :vartype state: Optional[str]
    :ivar is_codeowner: Whether the approver is a code owner.
    :vartype is_codeowner: Optional[bool]
    :ivar updated_at: Timestamp when this object was last updated.
    :vartype updated_at: Optional[str]
    :ivar avatar_url: Avatar image URL.
    :vartype avatar_url: Optional[str]
    """

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
    """Time tracking fields embedded in pull requests.

    :ivar time_estimate: Estimated time in seconds.
    :vartype time_estimate: Optional[int]
    :ivar total_time_spent: Total time spent in seconds.
    :vartype total_time_spent: Optional[int]
    :ivar human_time_estimate: Human-readable estimated time.
    :vartype human_time_estimate: Optional[str]
    :ivar human_total_time_spent: Human-readable total time spent.
    :vartype human_total_time_spent: Optional[str]
    """

    time_estimate: Optional[int] = None
    total_time_spent: Optional[int] = None
    human_time_estimate: Optional[str] = None
    human_total_time_spent: Optional[str] = None


@dataclass(init=False)
class PullRequestDiffRefs(APIObject):
    """Diff refs embedded in pull requests.

    :ivar base_sha: Base sha.
    :vartype base_sha: Optional[str]
    :ivar head_sha: Head sha.
    :vartype head_sha: Optional[str]
    :ivar start_sha: Start sha.
    :vartype start_sha: Optional[str]
    """

    base_sha: Optional[str] = None
    head_sha: Optional[str] = None
    start_sha: Optional[str] = None


@dataclass(init=False)
class PullRequest(APIObject):
    """Pull request payload.

    :ivar number: Sequence number for the object within its repository.
    :vartype number: Optional[Union[int, str]]
    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar iid: Internal identifier scoped to the repository.
    :vartype iid: Optional[int]
    :ivar project_id: Numeric ID of the related project.
    :vartype project_id: Optional[int]
    :ivar html_url: Web URL for this object.
    :vartype html_url: Optional[str]
    :ivar url: API URL for this object.
    :vartype url: Optional[str]
    :ivar title: Title of the object.
    :vartype title: Optional[str]
    :ivar body: Body text of the object.
    :vartype body: Optional[str]
    :ivar state: Current state value.
    :vartype state: Optional[str]
    :ivar draft: Whether the pull request is a draft.
    :vartype draft: Optional[bool]
    :ivar close_related_issue: Whether related issues are closed when the pull request is merged.
    :vartype close_related_issue: Optional[bool]
    :ivar prune_branch: Whether the source branch should be pruned after merge.
    :vartype prune_branch: Optional[bool]
    :ivar labels: Labels attached to this object.
    :vartype labels: Optional[List[Label]]
    :ivar user: User associated with this object.
    :vartype user: Optional[UserRef]
    :ivar assignees: Users assigned to this object.
    :vartype assignees: Optional[List[UserRef]]
    :ivar head: Head.
    :vartype head: Optional[PullRequestBranch]
    :ivar base: Base.
    :vartype base: Optional[PullRequestBranch]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar updated_at: Timestamp when this object was last updated.
    :vartype updated_at: Optional[str]
    :ivar merged_at: Timestamp when this pull request was merged.
    :vartype merged_at: Optional[str]
    :ivar closed_by: Closed by.
    :vartype closed_by: Optional[UserRef]
    :ivar closed_at: Timestamp when this object was closed.
    :vartype closed_at: Optional[str]
    :ivar target_branch: Target branch name.
    :vartype target_branch: Optional[str]
    :ivar source_branch: Source branch name.
    :vartype source_branch: Optional[str]
    :ivar squash_commit_message: Commit message to use for a squash merge.
    :vartype squash_commit_message: Optional[str]
    :ivar user_notes_count: Number of user notes on the pull request.
    :vartype user_notes_count: Optional[int]
    :ivar upvotes: Number of upvotes.
    :vartype upvotes: Optional[int]
    :ivar downvotes: Number of downvotes.
    :vartype downvotes: Optional[int]
    :ivar source_project_id: ID of the source project.
    :vartype source_project_id: Optional[int]
    :ivar target_project_id: ID of the target project.
    :vartype target_project_id: Optional[int]
    :ivar work_in_progress: Whether the pull request is marked as work in progress.
    :vartype work_in_progress: Optional[bool]
    :ivar milestone: Milestone associated with the pull request.
    :vartype milestone: Optional[APIObject]
    :ivar merge_when_pipeline_succeeds: Whether the pull request should merge automatically after the pipeline succeeds.
    :vartype merge_when_pipeline_succeeds: Optional[bool]
    :ivar merge_status: Merge status reported by the API.
    :vartype merge_status: Optional[str]
    :ivar sha: Git SHA value.
    :vartype sha: Optional[str]
    :ivar merge_commit_sha: SHA of the merge commit.
    :vartype merge_commit_sha: Optional[str]
    :ivar should_remove_source_branch: Whether the source branch should be removed after merge.
    :vartype should_remove_source_branch: Optional[bool]
    :ivar force_remove_source_branch: Whether the source branch should be force removed after merge.
    :vartype force_remove_source_branch: Optional[bool]
    :ivar web_url: Web URL for this object.
    :vartype web_url: Optional[str]
    :ivar time_stats: Time tracking information for the pull request.
    :vartype time_stats: Optional[PullRequestTimeStats]
    :ivar squash: Whether the pull request will be squashed on merge.
    :vartype squash: Optional[bool]
    :ivar merge_request_type: Pull request type returned by the API.
    :vartype merge_request_type: Optional[str]
    :ivar has_pre_merge_ref: Whether a pre-merge ref exists for the pull request.
    :vartype has_pre_merge_ref: Optional[bool]
    :ivar review_mode: Review mode configured for the pull request.
    :vartype review_mode: Optional[str]
    :ivar is_source_branch_exist: Whether the source branch still exists.
    :vartype is_source_branch_exist: Optional[bool]
    :ivar approval_merge_request_approvers: Approvers configured for the pull request.
    :vartype approval_merge_request_approvers: Optional[List[PullRequestApprover]]
    :ivar approval_merge_request_testers: Testers configured for the pull request.
    :vartype approval_merge_request_testers: Optional[List[PullRequestApprover]]
    :ivar added_lines: Number of added lines in the pull request.
    :vartype added_lines: Optional[int]
    :ivar removed_lines: Number of removed lines in the pull request.
    :vartype removed_lines: Optional[int]
    :ivar subscribed: Whether the current user is subscribed.
    :vartype subscribed: Optional[bool]
    :ivar changes_count: Number of changed files or changes reported by the API.
    :vartype changes_count: Optional[Union[int, str]]
    :ivar diff_refs: Diff references used to compute the pull request changes.
    :vartype diff_refs: Optional[PullRequestDiffRefs]
    :ivar notes: Number of notes.
    :vartype notes: Optional[int]
    :ivar unresolved_discussions_count: Number of unresolved discussions.
    :vartype unresolved_discussions_count: Optional[int]
    :ivar gate_check: Whether gate checks passed for the pull request.
    :vartype gate_check: Optional[bool]
    """

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
    """Pull request count payload returned when ``only_count`` is enabled.

    :ivar all: All.
    :vartype all: Optional[int]
    :ivar opened: Opened.
    :vartype opened: Optional[int]
    :ivar closed: Closed.
    :vartype closed: Optional[int]
    :ivar merged: Merged.
    :vartype merged: Optional[int]
    :ivar locked: Locked.
    :vartype locked: Optional[int]
    """

    all: Optional[int] = None
    opened: Optional[int] = None
    closed: Optional[int] = None
    merged: Optional[int] = None
    locked: Optional[int] = None


@dataclass(init=False)
class PullRequestFile(APIObject):
    """Pull request file diff payload.

    :ivar filename: Filename.
    :vartype filename: Optional[str]
    :ivar status: Status string returned by the API.
    :vartype status: Optional[str]
    :ivar additions: Additions.
    :vartype additions: Optional[int]
    :ivar deletions: Deletions.
    :vartype deletions: Optional[int]
    :ivar changes: Changes.
    :vartype changes: Optional[int]
    :ivar blob_url: Blob URL.
    :vartype blob_url: Optional[str]
    :ivar raw_url: Raw URL.
    :vartype raw_url: Optional[str]
    :ivar contents_url: Contents URL.
    :vartype contents_url: Optional[str]
    :ivar patch: Patch.
    :vartype patch: Optional[str]
    """

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
    """Pull request comment payload.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar body: Body text of the object.
    :vartype body: Optional[str]
    :ivar user: User associated with this object.
    :vartype user: Optional[UserRef]
    :ivar path: Repository-relative or namespace path.
    :vartype path: Optional[str]
    :ivar position: Position.
    :vartype position: Optional[int]
    :ivar commit_id: ID of the related commit.
    :vartype commit_id: Optional[str]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar updated_at: Timestamp when this object was last updated.
    :vartype updated_at: Optional[str]
    :ivar comment_type: Comment type.
    :vartype comment_type: Optional[str]
    :ivar target: Target.
    :vartype target: Optional[APIObject]
    """

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
    """Pull request review payload.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar state: Current state value.
    :vartype state: Optional[str]
    :ivar body: Body text of the object.
    :vartype body: Optional[str]
    """

    id: Optional[Union[int, str]] = None
    state: Optional[str] = None
    body: Optional[str] = None


@dataclass(init=False)
class PullRequestTest(APIObject):
    """Pull request test request payload.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar state: Current state value.
    :vartype state: Optional[str]
    :ivar body: Body text of the object.
    :vartype body: Optional[str]
    """

    id: Optional[Union[int, str]] = None
    state: Optional[str] = None
    body: Optional[str] = None


@dataclass(init=False)
class MergeResult(APIObject):
    """Merge operation result payload.

    :ivar sha: Git SHA value.
    :vartype sha: Optional[str]
    :ivar merged: Merged.
    :vartype merged: Optional[bool]
    :ivar message: Message text returned by the API.
    :vartype message: Optional[str]
    """

    sha: Optional[str] = None
    merged: Optional[bool] = None
    message: Optional[str] = None


@dataclass(init=False)
class MergeStatus(APIObject):
    """Merge status payload.

    :ivar message: Message text returned by the API.
    :vartype message: Optional[str]
    :ivar error: Error.
    :vartype error: Optional[str]
    """

    message: Optional[str] = None
    error: Optional[str] = None


@dataclass(init=False)
class Milestone(APIObject):
    """Milestone payload.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar number: Sequence number for the object within its repository.
    :vartype number: Optional[int]
    :ivar title: Title of the object.
    :vartype title: Optional[str]
    :ivar description: Description text.
    :vartype description: Optional[str]
    :ivar state: Current state value.
    :vartype state: Optional[str]
    :ivar due_on: Due date for the milestone.
    :vartype due_on: Optional[str]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar updated_at: Timestamp when this object was last updated.
    :vartype updated_at: Optional[str]
    """

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
    """Collaborator permissions payload.

    :ivar pull: Pull.
    :vartype pull: Optional[bool]
    :ivar push: Push.
    :vartype push: Optional[bool]
    :ivar admin: Admin.
    :vartype admin: Optional[bool]
    """

    pull: Optional[bool] = None
    push: Optional[bool] = None
    admin: Optional[bool] = None


@dataclass(init=False)
class RepoMember(APIObject):
    """Repository member payload returned by add/update operations.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar login: Account login name.
    :vartype login: Optional[str]
    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar avatar_url: Avatar image URL.
    :vartype avatar_url: Optional[str]
    :ivar html_url: Web URL for this object.
    :vartype html_url: Optional[str]
    :ivar remark: Remark.
    :vartype remark: Optional[str]
    :ivar type: Type of the object.
    :vartype type: Optional[str]
    :ivar permissions: Permissions granted for this user.
    :vartype permissions: Optional[RepoMemberPermissions]
    """

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
    """Repository collaborator payload returned by list operations.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar username: Account username.
    :vartype username: Optional[str]
    :ivar nick_name: Nick name.
    :vartype nick_name: Optional[str]
    :ivar state: Current state value.
    :vartype state: Optional[str]
    :ivar avatar: Avatar path or URL returned for the collaborator.
    :vartype avatar: Optional[str]
    :ivar avatar_url: Avatar image URL.
    :vartype avatar_url: Optional[str]
    :ivar email: Email address.
    :vartype email: Optional[str]
    :ivar name_cn: Name cn.
    :vartype name_cn: Optional[str]
    :ivar web_url: Web URL for this object.
    :vartype web_url: Optional[str]
    :ivar access_level: Access level granted to the collaborator.
    :vartype access_level: Optional[int]
    :ivar expires_at: Timestamp when the collaborator access expires.
    :vartype expires_at: Optional[str]
    :ivar limited: Whether the collaborator has limited access.
    :vartype limited: Optional[bool]
    :ivar type: Type of the object.
    :vartype type: Optional[str]
    :ivar last_owner: Previous owner recorded for the collaborator source.
    :vartype last_owner: Optional[str]
    :ivar is_current_source_member: Whether the collaborator is still a member of the source entity.
    :vartype is_current_source_member: Optional[bool]
    :ivar last_source_owner: Previous source owner recorded for the collaborator.
    :vartype last_source_owner: Optional[str]
    :ivar join_way: How the collaborator joined the repository.
    :vartype join_way: Optional[str]
    :ivar source_name: Name of the source entity that granted access.
    :vartype source_name: Optional[str]
    :ivar member_roles: Custom member roles attached to the collaborator.
    :vartype member_roles: Optional[List[APIObject]]
    :ivar iam_id: IAM identifier of the collaborator.
    :vartype iam_id: Optional[str]
    :ivar committer_system_from: System from which committer identity is sourced.
    :vartype committer_system_from: Optional[str]
    :ivar permissions: Permissions granted for this user.
    :vartype permissions: Optional[RepoMemberPermissions]
    """

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
    """Repository member permission payload.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar login: Account login name.
    :vartype login: Optional[str]
    :ivar permission: Permission summary for this object.
    :vartype permission: Optional[str]
    """

    id: Optional[Union[int, str]] = None
    login: Optional[str] = None
    permission: Optional[str] = None


@dataclass(init=False)
class Release(APIObject):
    """Release payload.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar tag_name: Tag name.
    :vartype tag_name: Optional[str]
    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar body: Body text of the object.
    :vartype body: Optional[str]
    :ivar author: Author associated with this object.
    :vartype author: Optional[UserRef]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar published_at: Timestamp when this object was published.
    :vartype published_at: Optional[str]
    :ivar html_url: Web URL for this object.
    :vartype html_url: Optional[str]
    """

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
    """Commit object embedded in tag payloads.

    :ivar sha: Git SHA value.
    :vartype sha: Optional[str]
    :ivar url: API URL for this object.
    :vartype url: Optional[str]
    """

    sha: Optional[str] = None
    url: Optional[str] = None


@dataclass(init=False)
class Tagger(APIObject):
    """Tagger identity.

    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar email: Email address.
    :vartype email: Optional[str]
    :ivar date: Date.
    :vartype date: Optional[str]
    """

    name: Optional[str] = None
    email: Optional[str] = None
    date: Optional[str] = None


@dataclass(init=False)
class Tag(APIObject):
    """Tag payload.

    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar message: Message text returned by the API.
    :vartype message: Optional[str]
    :ivar commit: Commit.
    :vartype commit: Optional[TagCommit]
    :ivar tagger: Tagger.
    :vartype tagger: Optional[Tagger]
    """

    name: Optional[str] = None
    message: Optional[str] = None
    commit: Optional[TagCommit] = None
    tagger: Optional[Tagger] = None


@dataclass(init=False)
class ProtectedTag(APIObject):
    """Protected tag configuration payload.

    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar create_access_level: Access level required to create the protected tag.
    :vartype create_access_level: Optional[int]
    :ivar create_access_level_desc: Description of the access levels allowed to create the protected tag.
    :vartype create_access_level_desc: Optional[str]
    """

    name: Optional[str] = None
    create_access_level: Optional[int] = None
    create_access_level_desc: Optional[str] = None


@dataclass(init=False)
class Webhook(APIObject):
    """Webhook payload.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar url: API URL for this object.
    :vartype url: Optional[str]
    :ivar password: Password.
    :vartype password: Optional[str]
    :ivar result: Result text returned by the webhook.
    :vartype result: Optional[str]
    :ivar project_id: Numeric ID of the related project.
    :vartype project_id: Optional[int]
    :ivar result_code: Result code returned by the webhook.
    :vartype result_code: Optional[int]
    :ivar push_events: Push events.
    :vartype push_events: Optional[bool]
    :ivar tag_push_events: Tag push events.
    :vartype tag_push_events: Optional[bool]
    :ivar issues_events: Issues events.
    :vartype issues_events: Optional[bool]
    :ivar note_events: Note events.
    :vartype note_events: Optional[bool]
    :ivar merge_requests_events: Merge requests events.
    :vartype merge_requests_events: Optional[bool]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    """

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
    """Organization summary payload returned by list endpoints.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar login: Account login name.
    :vartype login: Optional[str]
    :ivar path: Repository-relative or namespace path.
    :vartype path: Optional[str]
    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar avatar_url: Avatar image URL.
    :vartype avatar_url: Optional[str]
    :ivar repos_url: Repos URL.
    :vartype repos_url: Optional[str]
    :ivar events_url: Events URL.
    :vartype events_url: Optional[str]
    :ivar members_url: Members URL.
    :vartype members_url: Optional[str]
    :ivar description: Description text.
    :vartype description: Optional[str]
    :ivar follow_count: Number of follow.
    :vartype follow_count: Optional[int]
    """

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
    """Organization payload.

    :ivar enterprise: Enterprise identifier associated with the organization.
    :vartype enterprise: Optional[str]
    :ivar gitee: Additional mirrored-platform metadata.
    :vartype gitee: Optional[APIObject]
    """

    enterprise: Optional[str] = None
    gitee: Optional[APIObject] = None


@dataclass(init=False)
class OrganizationMembership(APIObject):
    """Organization membership payload.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar path: Repository-relative or namespace path.
    :vartype path: Optional[str]
    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar url: API URL for this object.
    :vartype url: Optional[str]
    :ivar avatar_url: Avatar image URL.
    :vartype avatar_url: Optional[str]
    :ivar user: User associated with this object.
    :vartype user: Optional[UserRef]
    :ivar role: Role.
    :vartype role: Optional[str]
    :ivar organization: Organization.
    :vartype organization: Optional[OrganizationSummary]
    """

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
    """Enterprise member payload.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar role: Role.
    :vartype role: Optional[str]
    :ivar url: API URL for this object.
    :vartype url: Optional[str]
    :ivar user: User associated with this object.
    :vartype user: Optional[UserRef]
    :ivar login: Account login name.
    :vartype login: Optional[str]
    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar avatar_url: Avatar image URL.
    :vartype avatar_url: Optional[str]
    :ivar html_url: Web URL for this object.
    :vartype html_url: Optional[str]
    """

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
    """Email payload for the authenticated user.

    :ivar email: Email address.
    :vartype email: Optional[str]
    :ivar state: Current state value.
    :vartype state: Optional[str]
    """

    email: Optional[str] = None
    state: Optional[str] = None


@dataclass(init=False)
class OAuthToken(APIObject):
    """OAuth token payload.

    :ivar access_token: OAuth access token.
    :vartype access_token: Optional[str]
    :ivar expires_in: Lifetime of the token in seconds.
    :vartype expires_in: Optional[int]
    :ivar refresh_token: OAuth refresh token.
    :vartype refresh_token: Optional[str]
    :ivar scope: OAuth scopes granted to the token.
    :vartype scope: Optional[str]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    """

    access_token: Optional[str] = None
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    created_at: Optional[str] = None


@dataclass(init=False)
class EmptyResponse(APIObject):
    """Empty JSON object returned by some mutation endpoints."""


@dataclass(init=False)
class ApiStatusResponse(APIObject):
    """Simple success/error response containing a numeric code and message.

    :ivar code: Numeric status code returned by the API.
    :vartype code: Optional[int]
    :ivar msg: Message returned by the API.
    :vartype msg: Optional[str]
    """

    code: Optional[int] = None
    msg: Optional[str] = None


@dataclass(init=False)
class PublicKey(APIObject):
    """Public SSH key payload.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar title: Title of the object.
    :vartype title: Optional[str]
    :ivar key: Public key material.
    :vartype key: Optional[str]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar url: API URL for this object.
    :vartype url: Optional[str]
    """

    id: Optional[Union[int, str]] = None
    title: Optional[str] = None
    key: Optional[str] = None
    created_at: Optional[str] = None
    url: Optional[str] = None


@dataclass(init=False)
class UserEventProject(APIObject):
    """Project summary embedded in user event responses.

    :ivar main_repository_language: Primary languages reported for the repository.
    :vartype main_repository_language: Optional[List[Any]]
    :ivar star_count: Number of stars on the repository.
    :vartype star_count: Optional[int]
    :ivar forks_count: Number of forks.
    :vartype forks_count: Optional[int]
    :ivar develop_mode: Development mode of the repository.
    :vartype develop_mode: Optional[str]
    :ivar stared: Whether the current user has starred the repository.
    :vartype stared: Optional[bool]
    """

    main_repository_language: Optional[List[Any]] = None
    star_count: Optional[int] = None
    forks_count: Optional[int] = None
    develop_mode: Optional[str] = None
    stared: Optional[bool] = None


@dataclass(init=False)
class UserEventPushData(APIObject):
    """Push event metadata embedded in user events.

    :ivar commit_count: Number of commits included in the push event.
    :vartype commit_count: Optional[int]
    :ivar action: Action.
    :vartype action: Optional[str]
    :ivar ref_type: Type of Git ref involved in the push event.
    :vartype ref_type: Optional[str]
    :ivar commit_from: Starting commit SHA for the push event.
    :vartype commit_from: Optional[str]
    :ivar commit_to: Ending commit SHA for the push event.
    :vartype commit_to: Optional[str]
    :ivar ref: Git ref name.
    :vartype ref: Optional[str]
    :ivar commit_title: Title of the primary commit in the push event.
    :vartype commit_title: Optional[str]
    """

    commit_count: Optional[int] = None
    action: Optional[str] = None
    ref_type: Optional[str] = None
    commit_from: Optional[str] = None
    commit_to: Optional[str] = None
    ref: Optional[str] = None
    commit_title: Optional[str] = None


@dataclass(init=False)
class UserEventLinks(APIObject):
    """Link bundle embedded in user event responses.

    :ivar project: Link to the related project.
    :vartype project: Optional[str]
    :ivar action_type: Link to the action type resource.
    :vartype action_type: Optional[str]
    """

    project: Optional[str] = None
    action_type: Optional[str] = None


@dataclass(init=False)
class UserEvent(APIObject):
    """Single activity event returned by the user events endpoint.

    :ivar action: Action code reported for the event.
    :vartype action: Optional[Union[int, str]]
    :ivar action_name: Human-readable action name.
    :vartype action_name: Optional[str]
    :ivar author: Author associated with this object.
    :vartype author: Optional[UserRef]
    :ivar author_id: ID of the event author.
    :vartype author_id: Optional[Union[int, str]]
    :ivar author_username: Username of the event author.
    :vartype author_username: Optional[str]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar project: Project associated with the event.
    :vartype project: Optional[UserEventProject]
    :ivar project_id: ID of the related project.
    :vartype project_id: Optional[Union[int, str]]
    :ivar project_name: Name of the related project.
    :vartype project_name: Optional[str]
    :ivar push_data: Push metadata for push events.
    :vartype push_data: Optional[UserEventPushData]
    :ivar _links: Related links for the event.
    :vartype _links: Optional[UserEventLinks]
    """

    action: Optional[Union[int, str]] = None
    action_name: Optional[str] = None
    author: Optional[UserRef] = None
    author_id: Optional[Union[int, str]] = None
    author_username: Optional[str] = None
    created_at: Optional[str] = None
    project: Optional[UserEventProject] = None
    project_id: Optional[Union[int, str]] = None
    project_name: Optional[str] = None
    push_data: Optional[UserEventPushData] = None
    _links: Optional[UserEventLinks] = None


@dataclass(init=False)
class UserEventsResponse(APIObject):
    """Grouped user events response keyed by date.

    :ivar events: Events grouped by date.
    :vartype events: Optional[Dict[str, List[UserEvent]]]
    :ivar next: URL or token used to fetch the next page.
    :vartype next: Optional[str]
    """

    events: Optional[Dict[str, List[UserEvent]]] = None
    next: Optional[str] = None


@dataclass(init=False)
class RepositoryReviewerSettingsUpdate(APIObject):
    """Response returned after updating repository reviewer settings.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar updated_at: Timestamp when this object was last updated.
    :vartype updated_at: Optional[str]
    """

    id: Optional[Union[int, str]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass(init=False)
class RepositoryPermissionMode(APIObject):
    """Repository member management mode.

    :ivar memberMgntMode: Repository member management mode.
    :vartype memberMgntMode: Optional[int]
    """

    memberMgntMode: Optional[int] = None


@dataclass(init=False)
class RepositoryPushConfig(APIObject):
    """Repository push rules configuration.

    :ivar reject_not_signed_by_gpg: Whether unsigned commits are rejected.
    :vartype reject_not_signed_by_gpg: Optional[bool]
    :ivar commit_message_regex: Regular expression required for commit messages.
    :vartype commit_message_regex: Optional[str]
    :ivar max_file_size: Maximum allowed file size for pushes.
    :vartype max_file_size: Optional[int]
    :ivar skip_rule_for_owner: Whether push rules are skipped for owners.
    :vartype skip_rule_for_owner: Optional[bool]
    :ivar deny_force_push: Whether force pushes are denied.
    :vartype deny_force_push: Optional[bool]
    """

    reject_not_signed_by_gpg: Optional[bool] = None
    commit_message_regex: Optional[str] = None
    max_file_size: Optional[int] = None
    skip_rule_for_owner: Optional[bool] = None
    deny_force_push: Optional[bool] = None


@dataclass(init=False)
class RepositoryUploadResult(APIObject):
    """Uploaded repository attachment metadata.

    :ivar success: Success.
    :vartype success: Optional[bool]
    :ivar path: Repository-relative or namespace path.
    :vartype path: Optional[str]
    :ivar full_path: Full path for the object.
    :vartype full_path: Optional[str]
    """

    success: Optional[bool] = None
    path: Optional[str] = None
    full_path: Optional[str] = None


@dataclass(init=False)
class RepositorySettings(APIObject):
    """Repository-level settings payload.

    :ivar disable_fork: Whether repository forking is disabled.
    :vartype disable_fork: Optional[bool]
    :ivar forbidden_developer_create_branch: Whether developers are forbidden from creating branches.
    :vartype forbidden_developer_create_branch: Optional[bool]
    :ivar forbidden_developer_create_tag: Whether developers are forbidden from creating tags.
    :vartype forbidden_developer_create_tag: Optional[bool]
    :ivar forbidden_committer_create_branch: Whether committers are forbidden from creating branches.
    :vartype forbidden_committer_create_branch: Optional[bool]
    :ivar forbidden_developer_create_branch_user_ids: User IDs exempted from the developer branch-creation restriction.
    :vartype forbidden_developer_create_branch_user_ids: Optional[str]
    :ivar branch_name_regex: Regular expression required for branch names.
    :vartype branch_name_regex: Optional[str]
    :ivar tag_name_regex: Regular expression required for tag names.
    :vartype tag_name_regex: Optional[str]
    :ivar generate_pre_merge_ref: Whether pre-merge refs are generated.
    :vartype generate_pre_merge_ref: Optional[bool]
    :ivar rebase_disable_trigger_webhook: Whether rebases avoid triggering webhooks.
    :vartype rebase_disable_trigger_webhook: Optional[bool]
    :ivar open_gpg_verified: Whether OpenGPG verification is enabled.
    :vartype open_gpg_verified: Optional[bool]
    :ivar include_lfs_objects: Whether LFS objects are included.
    :vartype include_lfs_objects: Optional[bool]
    :ivar forbidden_gitlab_access: Whether GitLab access is forbidden.
    :vartype forbidden_gitlab_access: Optional[bool]
    """

    disable_fork: Optional[bool] = None
    forbidden_developer_create_branch: Optional[bool] = None
    forbidden_developer_create_tag: Optional[bool] = None
    forbidden_committer_create_branch: Optional[bool] = None
    forbidden_developer_create_branch_user_ids: Optional[str] = None
    branch_name_regex: Optional[str] = None
    tag_name_regex: Optional[str] = None
    generate_pre_merge_ref: Optional[bool] = None
    rebase_disable_trigger_webhook: Optional[bool] = None
    open_gpg_verified: Optional[bool] = None
    include_lfs_objects: Optional[bool] = None
    forbidden_gitlab_access: Optional[bool] = None


@dataclass(init=False)
class PullRequestSettingDetail(APIObject):
    """Nested merge request setting payload in repository PR settings.

    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar project_id: Numeric ID of the related project.
    :vartype project_id: Optional[Union[int, str]]
    :ivar disable_merge_by_self: Whether users are prevented from merging pull requests they created.
    :vartype disable_merge_by_self: Optional[bool]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar updated_at: Timestamp when this object was last updated.
    :vartype updated_at: Optional[str]
    :ivar can_force_merge: Whether administrators can force merge.
    :vartype can_force_merge: Optional[bool]
    :ivar disable_squash_merge: Whether squash merge is disabled.
    :vartype disable_squash_merge: Optional[bool]
    :ivar approval_required_reviewers: Number of reviewers required before merge.
    :vartype approval_required_reviewers: Optional[int]
    :ivar approval_required_approvers: Number of approvers required before merge.
    :vartype approval_required_approvers: Optional[int]
    :ivar add_notes_after_merged: Whether notes are added after merge.
    :vartype add_notes_after_merged: Optional[bool]
    :ivar merged_commit_author: Author name used for merged commits.
    :vartype merged_commit_author: Optional[str]
    :ivar mark_auto_merged_mr_as_closed: Whether auto-merged pull requests are marked as closed.
    :vartype mark_auto_merged_mr_as_closed: Optional[bool]
    :ivar delete_source_branch_when_merged: Whether source branches are deleted after merge.
    :vartype delete_source_branch_when_merged: Optional[bool]
    :ivar auto_squash_merge: Whether squash merge is enabled by default.
    :vartype auto_squash_merge: Optional[bool]
    :ivar squash_merge_with_no_merge_commit: Whether squash merges omit a merge commit.
    :vartype squash_merge_with_no_merge_commit: Optional[bool]
    :ivar close_issue_when_mr_merged: Whether related issues are closed when a pull request is merged.
    :vartype close_issue_when_mr_merged: Optional[bool]
    :ivar can_reopen: Whether merged or closed pull requests can be reopened.
    :vartype can_reopen: Optional[bool]
    :ivar is_check_cla: Whether CLA checks are enabled.
    :vartype is_check_cla: Optional[bool]
    :ivar approval_approvers: Available approver rules for the repository.
    :vartype approval_approvers: Optional[List[APIObject]]
    :ivar approval_testers: Available tester rules for the repository.
    :vartype approval_testers: Optional[List[APIObject]]
    :ivar approval_required_testers: Number of testers required before merge.
    :vartype approval_required_testers: Optional[int]
    :ivar is_allow_lite_merge_request: Whether lightweight pull requests are allowed.
    :vartype is_allow_lite_merge_request: Optional[bool]
    :ivar lite_merge_request_prefix_title: Title prefix used for lightweight pull requests.
    :vartype lite_merge_request_prefix_title: Optional[str]
    """

    id: Optional[Union[int, str]] = None
    project_id: Optional[Union[int, str]] = None
    disable_merge_by_self: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    can_force_merge: Optional[bool] = None
    disable_squash_merge: Optional[bool] = None
    approval_required_reviewers: Optional[int] = None
    approval_required_approvers: Optional[int] = None
    add_notes_after_merged: Optional[bool] = None
    merged_commit_author: Optional[str] = None
    mark_auto_merged_mr_as_closed: Optional[bool] = None
    delete_source_branch_when_merged: Optional[bool] = None
    auto_squash_merge: Optional[bool] = None
    squash_merge_with_no_merge_commit: Optional[bool] = None
    close_issue_when_mr_merged: Optional[bool] = None
    can_reopen: Optional[bool] = None
    is_check_cla: Optional[bool] = None
    approval_approvers: Optional[List[APIObject]] = None
    approval_testers: Optional[List[APIObject]] = None
    approval_required_testers: Optional[int] = None
    is_allow_lite_merge_request: Optional[bool] = None
    lite_merge_request_prefix_title: Optional[str] = None


@dataclass(init=False)
class PullRequestSettings(APIObject):
    """Repository pull request settings payload.

    :ivar merge_request_setting: Detailed pull request merge settings.
    :vartype merge_request_setting: Optional[PullRequestSettingDetail]
    :ivar only_allow_merge_if_all_discussions_are_resolved: Whether all discussions must be resolved before merge.
    :vartype only_allow_merge_if_all_discussions_are_resolved: Optional[bool]
    :ivar only_allow_merge_if_pipeline_succeeds: Whether merges require a successful pipeline.
    :vartype only_allow_merge_if_pipeline_succeeds: Optional[bool]
    :ivar merge_method: Merge strategy configured for pull requests.
    :vartype merge_method: Optional[str]
    """

    merge_request_setting: Optional[PullRequestSettingDetail] = None
    only_allow_merge_if_all_discussions_are_resolved: Optional[bool] = None
    only_allow_merge_if_pipeline_succeeds: Optional[bool] = None
    merge_method: Optional[str] = None


@dataclass(init=False)
class RepositoryTransferResult(APIObject):
    """Repository transfer result payload.

    :ivar new_owner: New owner.
    :vartype new_owner: Optional[str]
    :ivar new_name: New name.
    :vartype new_name: Optional[str]
    """

    new_owner: Optional[str] = None
    new_name: Optional[str] = None


@dataclass(init=False)
class RepositoryCustomizedRole(APIObject):
    """Customized repository role definition.

    :ivar role_id: Identifier of the custom role.
    :vartype role_id: Optional[str]
    :ivar access_level: Access level granted by the custom role.
    :vartype access_level: Optional[int]
    :ivar role_name: Name of the custom role.
    :vartype role_name: Optional[str]
    :ivar role_chinese_name: Chinese name of the custom role.
    :vartype role_chinese_name: Optional[str]
    :ivar role_description: Description of the custom role.
    :vartype role_description: Optional[str]
    :ivar role_type: Type of the custom role.
    :vartype role_type: Optional[str]
    :ivar member_count: Number of members assigned to the custom role.
    :vartype member_count: Optional[int]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar updated_at: Timestamp when this object was last updated.
    :vartype updated_at: Optional[str]
    """

    role_id: Optional[str] = None
    access_level: Optional[int] = None
    role_name: Optional[str] = None
    role_chinese_name: Optional[str] = None
    role_description: Optional[str] = None
    role_type: Optional[str] = None
    member_count: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass(init=False)
class RepositoryDownloadStatisticsDetail(APIObject):
    """Per-day repository download statistics entry.

    :ivar pdate: Date for this statistics entry.
    :vartype pdate: Optional[str]
    :ivar repo_id: Repository ID.
    :vartype repo_id: Optional[str]
    :ivar total_dl_cnt: Total download count up to this date.
    :vartype total_dl_cnt: Optional[int]
    :ivar today_dl_cnt: Download count for this date.
    :vartype today_dl_cnt: Optional[int]
    """

    pdate: Optional[str] = None
    repo_id: Optional[str] = None
    total_dl_cnt: Optional[int] = None
    today_dl_cnt: Optional[int] = None


@dataclass(init=False)
class RepositoryDownloadStatistics(APIObject):
    """Repository download statistics payload.

    :ivar download_statistics_detail: Per-day download statistics entries.
    :vartype download_statistics_detail: Optional[List[RepositoryDownloadStatisticsDetail]]
    :ivar download_statistics_total: Total downloads within the requested time range.
    :vartype download_statistics_total: Optional[int]
    :ivar download_statistics_history_total: Historical total downloads for the repository.
    :vartype download_statistics_history_total: Optional[int]
    """

    download_statistics_detail: Optional[List[RepositoryDownloadStatisticsDetail]] = None
    download_statistics_total: Optional[int] = None
    download_statistics_history_total: Optional[int] = None


@dataclass(init=False)
class ContributorStatisticsOverview(APIObject):
    """Aggregate contributor statistics summary.

    :ivar additions: Additions.
    :vartype additions: Optional[int]
    :ivar deletions: Deletions.
    :vartype deletions: Optional[int]
    :ivar total_changes: Total lines changed.
    :vartype total_changes: Optional[int]
    :ivar commit_count: Number of commits.
    :vartype commit_count: Optional[int]
    """

    additions: Optional[int] = None
    deletions: Optional[int] = None
    total_changes: Optional[int] = None
    commit_count: Optional[int] = None


@dataclass(init=False)
class ContributorStatisticsEntry(APIObject):
    """Per-day contributor statistics entry.

    :ivar date: Date for this contribution statistics entry.
    :vartype date: Optional[str]
    :ivar additions: Additions.
    :vartype additions: Optional[int]
    :ivar deletions: Deletions.
    :vartype deletions: Optional[int]
    :ivar total_changes: Total lines changed on this date.
    :vartype total_changes: Optional[int]
    :ivar commit_count: Number of commits on this date.
    :vartype commit_count: Optional[int]
    """

    date: Optional[str] = None
    additions: Optional[int] = None
    deletions: Optional[int] = None
    total_changes: Optional[int] = None
    commit_count: Optional[int] = None


@dataclass(init=False)
class ContributorStatistics(APIObject):
    """Contributor statistics payload returned by the repository statistics endpoint.

    :ivar name: Display name.
    :vartype name: Optional[str]
    :ivar email: Email address.
    :vartype email: Optional[str]
    :ivar overview: Aggregate contribution statistics.
    :vartype overview: Optional[ContributorStatisticsOverview]
    :ivar contributions: Per-day contribution statistics.
    :vartype contributions: Optional[List[ContributorStatisticsEntry]]
    """

    name: Optional[str] = None
    email: Optional[str] = None
    overview: Optional[ContributorStatisticsOverview] = None
    contributions: Optional[List[ContributorStatisticsEntry]] = None


@dataclass(init=False)
class PullRequestOperationLog(APIObject):
    """Pull request operation log entry.

    :ivar content: Content returned for this object.
    :vartype content: Optional[str]
    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar action: Action recorded in the operation log.
    :vartype action: Optional[str]
    :ivar merge_request_id: ID of the related pull request.
    :vartype merge_request_id: Optional[Union[int, str]]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar updated_at: Timestamp when this object was last updated.
    :vartype updated_at: Optional[str]
    :ivar discussion_id: ID of the related discussion.
    :vartype discussion_id: Optional[str]
    :ivar project: Project identifier recorded in the log entry.
    :vartype project: Optional[str]
    :ivar assignee: Assignee metadata captured in the log entry.
    :vartype assignee: Optional[APIObject]
    :ivar proposer: Proposer metadata captured in the log entry.
    :vartype proposer: Optional[APIObject]
    :ivar user: User associated with this object.
    :vartype user: Optional[UserRef]
    """

    content: Optional[str] = None
    id: Optional[Union[int, str]] = None
    action: Optional[str] = None
    merge_request_id: Optional[Union[int, str]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    discussion_id: Optional[str] = None
    project: Optional[str] = None
    assignee: Optional[APIObject] = None
    proposer: Optional[APIObject] = None
    user: Optional[UserRef] = None


@dataclass(init=False)
class PullRequestAssigneeCount(APIObject):
    """Response payload when assignees are added to a pull request.

    :ivar assignees_number: Assignees number.
    :vartype assignees_number: Optional[int]
    """

    assignees_number: Optional[int] = None


@dataclass(init=False)
class RepositoryCollaboratorCheck(APIObject):
    """Repository collaborator presence check response.

    :ivar message: Message text returned by the API.
    :vartype message: Optional[str]
    """

    message: Optional[str] = None


@dataclass(init=False)
class SearchUser(APIObject):
    """User search result payload.

    :ivar avatar_url: Avatar image URL.
    :vartype avatar_url: Optional[str]
    :ivar created_at: Timestamp when this object was created.
    :vartype created_at: Optional[str]
    :ivar html_url: Web URL for this object.
    :vartype html_url: Optional[str]
    :ivar id: Unique identifier for this object.
    :vartype id: Optional[Union[int, str]]
    :ivar login: Account login name.
    :vartype login: Optional[str]
    :ivar name: Display name.
    :vartype name: Optional[str]
    """

    avatar_url: Optional[str] = None
    created_at: Optional[str] = None
    html_url: Optional[str] = None
    id: Optional[Union[int, str]] = None
    login: Optional[str] = None
    name: Optional[str] = None


@dataclass(init=False)
class SearchResult(APIObject):
    """Backward-compatible generic search result payload."""
