"""Top-level synchronous and asynchronous GitCode API clients.

These client classes expose grouped resource helpers that mirror the
published GitCode REST API documentation.
"""

from typing import Optional

import httpx

from ._base_client import DEFAULT_BASE_URL, AsyncAPIClient, SyncAPIClient
from .resources import (
    AsyncBranchesResource,
    AsyncCommitsResource,
    AsyncIssuesResource,
    AsyncLabelsResource,
    AsyncMembersResource,
    AsyncMilestonesResource,
    AsyncOAuthResource,
    AsyncOrgsResource,
    AsyncPullsResource,
    AsyncReleasesResource,
    AsyncRepoContentsResource,
    AsyncReposResource,
    AsyncSearchResource,
    AsyncTagsResource,
    AsyncUsersResource,
    AsyncWebhooksResource,
    BranchesResource,
    CommitsResource,
    IssuesResource,
    LabelsResource,
    MembersResource,
    MilestonesResource,
    OAuthResource,
    OrgsResource,
    PullsResource,
    ReleasesResource,
    RepoContentsResource,
    ReposResource,
    SearchResource,
    TagsResource,
    UsersResource,
    WebhooksResource,
)


class GitCode(SyncAPIClient):
    """Synchronous GitCode API client.

    :param api_key: Personal access token used for GitCode API requests.
    :param owner: Default repository owner used by repository-scoped helpers.
    :param repo: Default repository name used by repository-scoped helpers.
    :param base_url: Base URL for the GitCode REST API.
    :param timeout: Request timeout in seconds.
    :param http_client: Optional pre-configured ``httpx.Client`` instance.
    """

    repos: ReposResource
    """Repository endpoints exposed as ``client.repos``."""

    contents: RepoContentsResource
    """Repository content endpoints exposed as ``client.contents``."""

    branches: BranchesResource
    """Repository branch endpoints exposed as ``client.branches``."""

    commits: CommitsResource
    """Repository commit endpoints exposed as ``client.commits``."""

    issues: IssuesResource
    """Issue endpoints exposed as ``client.issues``."""

    pulls: PullsResource
    """Pull request endpoints exposed as ``client.pulls``."""

    labels: LabelsResource
    """Label endpoints exposed as ``client.labels``."""

    milestones: MilestonesResource
    """Milestone endpoints exposed as ``client.milestones``."""

    members: MembersResource
    """Repository member endpoints exposed as ``client.members``."""

    releases: ReleasesResource
    """Release endpoints exposed as ``client.releases``."""

    tags: TagsResource
    """Tag endpoints exposed as ``client.tags``."""

    webhooks: WebhooksResource
    """Webhook endpoints exposed as ``client.webhooks``."""

    users: UsersResource
    """User endpoints exposed as ``client.users``."""

    orgs: OrgsResource
    """Organization endpoints exposed as ``client.orgs``."""

    search: SearchResource
    """Search endpoints exposed as ``client.search``."""

    oauth: OAuthResource
    """OAuth helper endpoints exposed as ``client.oauth``."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: Optional[float] = None,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        """Create a synchronous client and attach resource groups."""
        super().__init__(
            api_key=api_key,
            owner=owner,
            repo=repo,
            base_url=base_url,
            timeout=timeout,
            http_client=http_client,
        )
        self.repos = ReposResource(self)
        self.contents = RepoContentsResource(self)
        self.branches = BranchesResource(self)
        self.commits = CommitsResource(self)
        self.issues = IssuesResource(self)
        self.pulls = PullsResource(self)
        self.labels = LabelsResource(self)
        self.milestones = MilestonesResource(self)
        self.members = MembersResource(self)
        self.releases = ReleasesResource(self)
        self.tags = TagsResource(self)
        self.webhooks = WebhooksResource(self)
        self.users = UsersResource(self)
        self.orgs = OrgsResource(self)
        self.search = SearchResource(self)
        self.oauth = OAuthResource(self)

    def __enter__(self) -> "GitCode":
        return self


class AsyncGitCode(AsyncAPIClient):
    """Asynchronous GitCode API client.

    :param api_key: Personal access token used for GitCode API requests.
    :param owner: Default repository owner used by repository-scoped helpers.
    :param repo: Default repository name used by repository-scoped helpers.
    :param base_url: Base URL for the GitCode REST API.
    :param timeout: Request timeout in seconds.
    :param http_client: Optional pre-configured ``httpx.AsyncClient`` instance.
    """

    repos: AsyncReposResource
    """Repository endpoints exposed as ``client.repos``."""

    contents: AsyncRepoContentsResource
    """Repository content endpoints exposed as ``client.contents``."""

    branches: AsyncBranchesResource
    """Repository branch endpoints exposed as ``client.branches``."""

    commits: AsyncCommitsResource
    """Repository commit endpoints exposed as ``client.commits``."""

    issues: AsyncIssuesResource
    """Issue endpoints exposed as ``client.issues``."""

    pulls: AsyncPullsResource
    """Pull request endpoints exposed as ``client.pulls``."""

    labels: AsyncLabelsResource
    """Label endpoints exposed as ``client.labels``."""

    milestones: AsyncMilestonesResource
    """Milestone endpoints exposed as ``client.milestones``."""

    members: AsyncMembersResource
    """Repository member endpoints exposed as ``client.members``."""

    releases: AsyncReleasesResource
    """Release endpoints exposed as ``client.releases``."""

    tags: AsyncTagsResource
    """Tag endpoints exposed as ``client.tags``."""

    webhooks: AsyncWebhooksResource
    """Webhook endpoints exposed as ``client.webhooks``."""

    users: AsyncUsersResource
    """User endpoints exposed as ``client.users``."""

    orgs: AsyncOrgsResource
    """Organization endpoints exposed as ``client.orgs``."""

    search: AsyncSearchResource
    """Search endpoints exposed as ``client.search``."""

    oauth: AsyncOAuthResource
    """OAuth helper endpoints exposed as ``client.oauth``."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: Optional[float] = None,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        """Create an asynchronous client and attach resource groups."""
        super().__init__(
            api_key=api_key,
            owner=owner,
            repo=repo,
            base_url=base_url,
            timeout=timeout,
            http_client=http_client,
        )
        self.repos = AsyncReposResource(self)
        self.contents = AsyncRepoContentsResource(self)
        self.branches = AsyncBranchesResource(self)
        self.commits = AsyncCommitsResource(self)
        self.issues = AsyncIssuesResource(self)
        self.pulls = AsyncPullsResource(self)
        self.labels = AsyncLabelsResource(self)
        self.milestones = AsyncMilestonesResource(self)
        self.members = AsyncMembersResource(self)
        self.releases = AsyncReleasesResource(self)
        self.tags = AsyncTagsResource(self)
        self.webhooks = AsyncWebhooksResource(self)
        self.users = AsyncUsersResource(self)
        self.orgs = AsyncOrgsResource(self)
        self.search = AsyncSearchResource(self)
        self.oauth = AsyncOAuthResource(self)

    async def __aenter__(self) -> "AsyncGitCode":
        return self
