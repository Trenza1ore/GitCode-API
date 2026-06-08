"""ReposResource and AsyncReposResource resource group."""

from typing import Dict, List, Optional

from ..._models import (
    APIObject,
    ApiStatusResponse,
    Contributor,
    ContributorStatistics,
    PullRequestSettings,
    RepoMember,
    Repository,
    RepositoryCustomizedRole,
    RepositoryDownloadStatistics,
    RepositoryPermissionMode,
    RepositoryPushConfig,
    RepositoryReviewerSettingsUpdate,
    RepositorySettings,
    RepositoryTransferResult,
    RepositoryUploadResult,
    UserSummary,
    as_model,
)
from .._shared import AsyncResource, SyncResource


class ReposResource(SyncResource):
    """Synchronous repository endpoints."""

    def get(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> Repository:
        """Get a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Repository metadata.
        """
        return self._model("GET", self._client._repo_path(owner=owner, repo=repo), Repository)

    def list_user(
        self,
        *,
        visibility: Optional[str] = None,
        affiliation: Optional[str] = None,
        type: Optional[str] = None,
        sort: Optional[str] = None,
        direction: Optional[str] = None,
        q: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Repository]:
        """List repositories visible to the authenticated user.

        :param visibility: Visibility filter such as ``public``, ``private``, or ``all``.
        :param affiliation: Ownership filter accepted by the REST API.
        :param type: Repository type filter.
        :param sort: Sort field such as ``created`` or ``full_name``.
        :param direction: Sort direction.
        :param q: Optional keyword filter.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Matching repositories.
        """
        return self._models(
            "GET",
            self._client._path("user", "repos"),
            Repository,
            params={
                "visibility": visibility,
                "affiliation": affiliation,
                "type": type,
                "sort": sort,
                "direction": direction,
                "q": q,
                "page": page,
                "per_page": per_page,
            },
        )

    def list_for_owner(
        self,
        *,
        owner: str,
        type: Optional[str] = None,
        sort: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Repository]:
        """List public repositories for a user or owner path.

        :param owner: Repository owner path or username.
        :param type: Repository type filter.
        :param sort: Sort field.
        :param direction: Sort direction.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Matching repositories.
        """
        return self._models(
            "GET",
            self._client._path("users", owner, "repos"),
            Repository,
            params={
                "type": type,
                "sort": sort,
                "direction": direction,
                "page": page,
                "per_page": per_page,
            },
        )

    def create_personal(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        path: Optional[str] = None,
        private: Optional[bool] = None,
        auto_init: Optional[bool] = None,
        has_issues: Optional[bool] = None,
        has_wiki: Optional[bool] = None,
        default_branch: Optional[str] = None,
        gitignore_template: Optional[str] = None,
        license_template: Optional[str] = None,
    ) -> Repository:
        """Create a repository for the authenticated user.

        :param name: Repository name.
        :param description: Repository description.
        :param path: Optional repository path.
        :param private: Whether the repository should be private.
        :param auto_init: Whether to initialize the repository with a README.
        :param has_issues: Whether issues are enabled.
        :param has_wiki: Whether wiki support is enabled.
        :param default_branch: Default branch name when initializing.
        :param gitignore_template: Optional gitignore template.
        :param license_template: Optional license template.
        :returns: Created repository metadata.
        """
        return self._model(
            "POST",
            self._client._path("user", "repos"),
            Repository,
            json={
                "name": name,
                "description": description,
                "path": path,
                "private": private,
                "auto_init": auto_init,
                "has_issues": has_issues,
                "has_wiki": has_wiki,
                "default_branch": default_branch,
                "gitignore_template": gitignore_template,
                "license_template": license_template,
            },
        )

    def create_for_org(
        self,
        *,
        org: str,
        name: str,
        description: Optional[str] = None,
        homepage: Optional[str] = None,
        path: Optional[str] = None,
        private: Optional[bool] = None,
        public: Optional[int] = None,
        auto_init: Optional[bool] = None,
        has_issues: Optional[bool] = None,
        has_wiki: Optional[bool] = None,
        can_comment: Optional[bool] = None,
        default_branch: Optional[str] = None,
        gitignore_template: Optional[str] = None,
        license_template: Optional[str] = None,
    ) -> Repository:
        """Create a repository under an organization.

        :param org: Organization path or login.
        :param name: Repository name.
        :param description: Repository description.
        :param homepage: Repository homepage URL.
        :param path: Optional repository path.
        :param private: Whether the repository should be private.
        :param public: Visibility mode used by the GitCode API.
        :param auto_init: Whether to initialize the repository with a README.
        :param has_issues: Whether issues are enabled.
        :param has_wiki: Whether wiki support is enabled.
        :param can_comment: Whether comments are enabled.
        :param default_branch: Default branch name when initializing.
        :param gitignore_template: Optional gitignore template.
        :param license_template: Optional license template.
        :returns: Created repository metadata.
        """
        return self._model(
            "POST",
            self._client._path("orgs", org, "repos"),
            Repository,
            json={
                "name": name,
                "description": description,
                "homepage": homepage,
                "path": path,
                "private": private,
                "public": public,
                "auto_init": auto_init,
                "has_issues": has_issues,
                "has_wiki": has_wiki,
                "can_comment": can_comment,
                "default_branch": default_branch,
                "gitignore_template": gitignore_template,
                "license_template": license_template,
            },
        )

    def update(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **changes) -> Repository:
        """Update repository metadata.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param changes: Repository fields accepted by the update endpoint.
        :returns: Updated repository metadata.
        """
        return self._model("PATCH", self._client._repo_path(owner=owner, repo=repo), Repository, json=changes)

    def delete(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Delete a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        """
        self._request("DELETE", self._client._repo_path(owner=owner, repo=repo))

    def fork(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        namespace: Optional[str] = None,
        path: Optional[str] = None,
        name: Optional[str] = None,
    ) -> Repository:
        """Fork a repository.

        :param owner: Source repository owner path.
        :param repo: Source repository name.
        :param namespace: Optional destination namespace.
        :param path: Optional destination repository path.
        :param name: Optional destination repository name.
        :returns: Forked repository metadata.
        """
        return self._model(
            "POST",
            self._client._repo_path("forks", owner=owner, repo=repo),
            Repository,
            json={"namespace": namespace, "path": path, "name": name},
        )

    def list_forks(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        sort: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Repository]:
        """List forks of a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param sort: Optional sort field.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Fork repositories.
        """
        return self._models(
            "GET",
            self._client._repo_path("forks", owner=owner, repo=repo),
            Repository,
            params={"sort": sort, "page": page, "per_page": per_page},
        )

    def list_contributors(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Contributor]:
        """List repository contributors.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Contributors for the repository.
        """
        return self._models(
            "GET",
            self._client._repo_path("contributors", owner=owner, repo=repo),
            Contributor,
            params={"page": page, "per_page": per_page},
        )

    def list_languages(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> Dict[str, int]:
        """List language statistics for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Mapping of language names to byte counts.
        """
        return self._request("GET", self._client._repo_path("languages", owner=owner, repo=repo))

    def list_stargazers(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[UserSummary]:
        """List users who starred a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Users who starred the repository.
        """
        return self._models(
            "GET",
            self._client._repo_path("stargazers", owner=owner, repo=repo),
            UserSummary,
            params={"page": page, "per_page": per_page},
        )

    def list_subscribers(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[UserSummary]:
        """List users watching a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Subscribers for the repository.
        """
        return self._models(
            "GET",
            self._client._repo_path("subscribers", owner=owner, repo=repo),
            UserSummary,
            params={"page": page, "per_page": per_page},
        )

    def update_module_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **settings
    ) -> ApiStatusResponse:
        """Update repository module settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param settings: Module settings accepted by the GitCode API.
        :returns: API response payload.
        """
        return self._model(
            "PUT",
            self._client._repo_path("module", "setting", owner=owner, repo=repo),
            ApiStatusResponse,
            json=settings,
        )

    def update_reviewer_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **settings
    ) -> RepositoryReviewerSettingsUpdate:
        """Update repository reviewer settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param settings: Reviewer settings accepted by the GitCode API.
        :returns: API response payload.
        """
        return self._model(
            "PUT",
            self._client._repo_path("reviewer", owner=owner, repo=repo),
            RepositoryReviewerSettingsUpdate,
            json=settings,
        )

    def set_org_repo_status(self, *, org: str, repo: str, **payload) -> ApiStatusResponse:
        """Update organization repository status metadata.

        :param org: Organization path.
        :param repo: Repository path.
        :param payload: Status fields accepted by the API.
        :returns: API response payload.
        """
        return self._model(
            "PUT", self._client._path("org", org, "repo", repo, "status"), ApiStatusResponse, json=payload
        )

    def transfer_to_org(self, *, org: str, repo: str, **payload) -> ApiStatusResponse:
        """Transfer a repository to an organization.

        :param org: Destination organization path.
        :param repo: Repository path.
        :param payload: Transfer options accepted by the API.
        :returns: API response payload.
        """
        return self._model(
            "POST", self._client._path("org", org, "projects", repo, "transfer"), ApiStatusResponse, json=payload
        )

    def get_transition(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> RepositoryPermissionMode:
        """Get repository transition settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Transition configuration.
        """
        return self._model(
            "GET", self._client._repo_path("transition", owner=owner, repo=repo), RepositoryPermissionMode
        )

    def update_transition(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload
    ) -> ApiStatusResponse:
        """Update repository transition settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Transition settings accepted by the API.
        :returns: API response payload.
        """
        return self._model(
            "PUT", self._client._repo_path("transition", owner=owner, repo=repo), ApiStatusResponse, json=payload
        )

    def update_push_config(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload
    ) -> RepositoryPushConfig:
        """Update repository push configuration.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Push configuration values accepted by the API.
        :returns: API response payload.
        """
        return self._model(
            "PUT", self._client._repo_path("push_config", owner=owner, repo=repo), RepositoryPushConfig, json=payload
        )

    def get_push_config(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> RepositoryPushConfig:
        """Get repository push configuration.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Push configuration payload.
        """
        return self._model("GET", self._client._repo_path("push_config", owner=owner, repo=repo), RepositoryPushConfig)

    def upload_image(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload
    ) -> RepositoryUploadResult:
        """Upload an image asset for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Upload fields accepted by the API.
        :returns: Uploaded image metadata.
        """
        return self._model(
            "POST",
            self._client._repo_path("img", "upload", owner=owner, repo=repo),
            RepositoryUploadResult,
            json=payload,
        )

    def upload_file(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload
    ) -> RepositoryUploadResult:
        """Upload a file asset for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Upload fields accepted by the API.
        :returns: Uploaded file metadata.
        """
        return self._model(
            "POST",
            self._client._repo_path("file", "upload", owner=owner, repo=repo),
            RepositoryUploadResult,
            json=payload,
        )

    def update_repo_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload
    ) -> RepositorySettings:
        """Update repository settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Settings fields accepted by the API.
        :returns: API response payload.
        """
        return self._model(
            "PUT", self._client._repo_path("repo_settings", owner=owner, repo=repo), RepositorySettings, json=payload
        )

    def get_repo_settings(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> RepositorySettings:
        """Get repository settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Repository settings payload.
        """
        return self._model("GET", self._client._repo_path("repo_settings", owner=owner, repo=repo), RepositorySettings)

    def get_pull_request_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> PullRequestSettings:
        """Get pull request settings for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Pull request settings payload.
        """
        return self._model(
            "GET", self._client._repo_path("pull_request_settings", owner=owner, repo=repo), PullRequestSettings
        )

    def update_pull_request_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload
    ) -> PullRequestSettings:
        """Update pull request settings for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Pull request settings accepted by the API.
        :returns: API response payload.
        """
        return self._model(
            "PUT",
            self._client._repo_path("pull_request_settings", owner=owner, repo=repo),
            PullRequestSettings,
            json=payload,
        )

    def set_member_role(
        self,
        *,
        username: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        permission: Optional[str] = None,
    ) -> RepoMember:
        """Set a repository member role.

        :param username: Member username or login.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param permission: Permission or role name accepted by the API.
        :returns: API response payload.
        """
        return self._model(
            "PUT",
            self._client._repo_path("members", username, owner=owner, repo=repo),
            RepoMember,
            json={"permission": permission},
        )

    def transfer(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload
    ) -> RepositoryTransferResult:
        """Transfer a repository to another owner or namespace.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Transfer options accepted by the API.
        :returns: API response payload.
        """
        return self._model(
            "POST", self._client._repo_path("transfer", owner=owner, repo=repo), RepositoryTransferResult, json=payload
        )

    def list_customized_roles(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[RepositoryCustomizedRole]:
        """List customized roles for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Customized role definitions.
        """
        data = self._request("GET", self._client._repo_path("customized_roles", owner=owner, repo=repo))
        return [as_model(item, RepositoryCustomizedRole) for item in data]

    def get_download_statistics(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params
    ) -> RepositoryDownloadStatistics:
        """Get download statistics for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param params: Query parameters accepted by the statistics endpoint.
        :returns: Download statistics payload.
        """
        return self._model(
            "GET",
            self._client._repo_path("download_statistics", owner=owner, repo=repo),
            RepositoryDownloadStatistics,
            params=params,
        )

    def get_contributor_statistics(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[ContributorStatistics]:
        """Get code contribution statistics for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Contributor statistics payload.
        """
        return self._models(
            "GET",
            self._client._repo_path("contributors", "statistic", owner=owner, repo=repo),
            ContributorStatistics,
        )

    def list_events(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[APIObject]:
        """List repository events.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Repository event payloads.
        """
        data = self._request(
            "GET",
            self._client._repo_path("events", owner=owner, repo=repo),
            params={"page": page, "per_page": per_page},
        )
        return [as_model(item, APIObject) for item in data]


class AsyncReposResource(AsyncResource):
    """Asynchronous repository endpoints.

    Mirrors :class:`ReposResource`; see that class for parameters and JSON fields
    (Repository API in ``docs/rest_api/repos``).
    """

    async def get(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> Repository:
        """Get a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Repository metadata.
        """
        return await self._model("GET", self._client._repo_path(owner=owner, repo=repo), Repository)

    async def list_user(
        self,
        *,
        visibility: Optional[str] = None,
        affiliation: Optional[str] = None,
        type: Optional[str] = None,
        sort: Optional[str] = None,
        direction: Optional[str] = None,
        q: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Repository]:
        """List repositories visible to the authenticated user.

        :param visibility: Visibility filter such as ``public``, ``private``, or ``all``.
        :param affiliation: Ownership filter accepted by the REST API.
        :param type: Repository type filter.
        :param sort: Sort field such as ``created`` or ``full_name``.
        :param direction: Sort direction.
        :param q: Optional keyword filter.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Matching repositories.
        """
        return await self._models(
            "GET",
            self._client._path("user", "repos"),
            Repository,
            params={
                "visibility": visibility,
                "affiliation": affiliation,
                "type": type,
                "sort": sort,
                "direction": direction,
                "q": q,
                "page": page,
                "per_page": per_page,
            },
        )

    async def list_for_owner(
        self,
        *,
        owner: str,
        type: Optional[str] = None,
        sort: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Repository]:
        """List public repositories for a user or owner path.

        :param owner: Repository owner path or username.
        :param type: Repository type filter.
        :param sort: Sort field.
        :param direction: Sort direction.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Matching repositories.
        """
        return await self._models(
            "GET",
            self._client._path("users", owner, "repos"),
            Repository,
            params={
                "type": type,
                "sort": sort,
                "direction": direction,
                "page": page,
                "per_page": per_page,
            },
        )

    async def create_personal(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        path: Optional[str] = None,
        private: Optional[bool] = None,
        auto_init: Optional[bool] = None,
        has_issues: Optional[bool] = None,
        has_wiki: Optional[bool] = None,
        default_branch: Optional[str] = None,
        gitignore_template: Optional[str] = None,
        license_template: Optional[str] = None,
    ) -> Repository:
        """Create a repository for the authenticated user.

        :param name: Repository name.
        :param description: Repository description.
        :param path: Optional repository path.
        :param private: Whether the repository should be private.
        :param auto_init: Whether to initialize the repository with a README.
        :param has_issues: Whether issues are enabled.
        :param has_wiki: Whether wiki support is enabled.
        :param default_branch: Default branch name when initializing.
        :param gitignore_template: Optional gitignore template.
        :param license_template: Optional license template.
        :returns: Created repository metadata.
        """
        return await self._model(
            "POST",
            self._client._path("user", "repos"),
            Repository,
            json={
                "name": name,
                "description": description,
                "path": path,
                "private": private,
                "auto_init": auto_init,
                "has_issues": has_issues,
                "has_wiki": has_wiki,
                "default_branch": default_branch,
                "gitignore_template": gitignore_template,
                "license_template": license_template,
            },
        )

    async def create_for_org(
        self,
        *,
        org: str,
        name: str,
        description: Optional[str] = None,
        homepage: Optional[str] = None,
        path: Optional[str] = None,
        private: Optional[bool] = None,
        public: Optional[int] = None,
        auto_init: Optional[bool] = None,
        has_issues: Optional[bool] = None,
        has_wiki: Optional[bool] = None,
        can_comment: Optional[bool] = None,
        default_branch: Optional[str] = None,
        gitignore_template: Optional[str] = None,
        license_template: Optional[str] = None,
    ) -> Repository:
        """Create a repository under an organization.

        :param org: Organization path or login.
        :param name: Repository name.
        :param description: Repository description.
        :param homepage: Repository homepage URL.
        :param path: Optional repository path.
        :param private: Whether the repository should be private.
        :param public: Visibility mode used by the GitCode API.
        :param auto_init: Whether to initialize the repository with a README.
        :param has_issues: Whether issues are enabled.
        :param has_wiki: Whether wiki support is enabled.
        :param can_comment: Whether comments are enabled.
        :param default_branch: Default branch name when initializing.
        :param gitignore_template: Optional gitignore template.
        :param license_template: Optional license template.
        :returns: Created repository metadata.
        """
        return await self._model(
            "POST",
            self._client._path("orgs", org, "repos"),
            Repository,
            json={
                "name": name,
                "description": description,
                "homepage": homepage,
                "path": path,
                "private": private,
                "public": public,
                "auto_init": auto_init,
                "has_issues": has_issues,
                "has_wiki": has_wiki,
                "can_comment": can_comment,
                "default_branch": default_branch,
                "gitignore_template": gitignore_template,
                "license_template": license_template,
            },
        )

    async def update(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **changes) -> Repository:
        """Update repository metadata.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param changes: Repository fields accepted by the update endpoint.
        :returns: Updated repository metadata.
        """
        return await self._model("PATCH", self._client._repo_path(owner=owner, repo=repo), Repository, json=changes)

    async def delete(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Delete a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        """
        await self._request("DELETE", self._client._repo_path(owner=owner, repo=repo))

    async def fork(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        namespace: Optional[str] = None,
        path: Optional[str] = None,
        name: Optional[str] = None,
    ) -> Repository:
        """Fork a repository.

        :param owner: Source repository owner path.
        :param repo: Source repository name.
        :param namespace: Optional destination namespace.
        :param path: Optional destination repository path.
        :param name: Optional destination repository name.
        :returns: Forked repository metadata.
        """
        return await self._model(
            "POST",
            self._client._repo_path("forks", owner=owner, repo=repo),
            Repository,
            json={"namespace": namespace, "path": path, "name": name},
        )

    async def list_forks(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        sort: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Repository]:
        """List forks of a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param sort: Optional sort field.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Fork repositories.
        """
        return await self._models(
            "GET",
            self._client._repo_path("forks", owner=owner, repo=repo),
            Repository,
            params={"sort": sort, "page": page, "per_page": per_page},
        )

    async def list_contributors(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Contributor]:
        """List repository contributors.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Contributors for the repository.
        """
        return await self._models(
            "GET",
            self._client._repo_path("contributors", owner=owner, repo=repo),
            Contributor,
            params={"page": page, "per_page": per_page},
        )

    async def list_languages(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> Dict[str, int]:
        """List language statistics for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Mapping of language names to byte counts.
        """
        return await self._request("GET", self._client._repo_path("languages", owner=owner, repo=repo))

    async def list_stargazers(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[UserSummary]:
        """List users who starred a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Users who starred the repository.
        """
        return await self._models(
            "GET",
            self._client._repo_path("stargazers", owner=owner, repo=repo),
            UserSummary,
            params={"page": page, "per_page": per_page},
        )

    async def list_subscribers(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[UserSummary]:
        """List users watching a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Subscribers for the repository.
        """
        return await self._models(
            "GET",
            self._client._repo_path("subscribers", owner=owner, repo=repo),
            UserSummary,
            params={"page": page, "per_page": per_page},
        )

    async def update_module_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **settings
    ) -> ApiStatusResponse:
        """Update repository module settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param settings: Module settings accepted by the GitCode API.
        :returns: API response payload.
        """
        return await self._model(
            "PUT",
            self._client._repo_path("module", "setting", owner=owner, repo=repo),
            ApiStatusResponse,
            json=settings,
        )

    async def update_reviewer_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **settings
    ) -> RepositoryReviewerSettingsUpdate:
        """Update repository reviewer settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param settings: Reviewer settings accepted by the GitCode API.
        :returns: API response payload.
        """
        return await self._model(
            "PUT",
            self._client._repo_path("reviewer", owner=owner, repo=repo),
            RepositoryReviewerSettingsUpdate,
            json=settings,
        )

    async def set_org_repo_status(self, *, org: str, repo: str, **payload) -> ApiStatusResponse:
        """Update organization repository status metadata.

        :param org: Organization path.
        :param repo: Repository path.
        :param payload: Status fields accepted by the API.
        :returns: API response payload.
        """
        return await self._model(
            "PUT", self._client._path("org", org, "repo", repo, "status"), ApiStatusResponse, json=payload
        )

    async def transfer_to_org(self, *, org: str, repo: str, **payload) -> ApiStatusResponse:
        """Transfer a repository to an organization.

        :param org: Destination organization path.
        :param repo: Repository path.
        :param payload: Transfer options accepted by the API.
        :returns: API response payload.
        """
        return await self._model(
            "POST", self._client._path("org", org, "projects", repo, "transfer"), ApiStatusResponse, json=payload
        )

    async def get_transition(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> RepositoryPermissionMode:
        """Get repository transition settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Transition configuration.
        """
        return await self._model(
            "GET", self._client._repo_path("transition", owner=owner, repo=repo), RepositoryPermissionMode
        )

    async def update_transition(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload
    ) -> ApiStatusResponse:
        """Update repository transition settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Transition settings accepted by the API.
        :returns: API response payload.
        """
        return await self._model(
            "PUT", self._client._repo_path("transition", owner=owner, repo=repo), ApiStatusResponse, json=payload
        )

    async def update_push_config(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload
    ) -> RepositoryPushConfig:
        """Update repository push configuration.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Push configuration values accepted by the API.
        :returns: API response payload.
        """
        return await self._model(
            "PUT",
            self._client._repo_path("push_config", owner=owner, repo=repo),
            RepositoryPushConfig,
            json=payload,
        )

    async def get_push_config(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> RepositoryPushConfig:
        """Get repository push configuration.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Push configuration payload.
        """
        return await self._model(
            "GET", self._client._repo_path("push_config", owner=owner, repo=repo), RepositoryPushConfig
        )

    async def upload_image(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload
    ) -> RepositoryUploadResult:
        """Upload an image asset for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Upload fields accepted by the API.
        :returns: Uploaded image metadata.
        """
        return await self._model(
            "POST",
            self._client._repo_path("img", "upload", owner=owner, repo=repo),
            RepositoryUploadResult,
            json=payload,
        )

    async def upload_file(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload
    ) -> RepositoryUploadResult:
        """Upload a file asset for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Upload fields accepted by the API.
        :returns: Uploaded file metadata.
        """
        return await self._model(
            "POST",
            self._client._repo_path("file", "upload", owner=owner, repo=repo),
            RepositoryUploadResult,
            json=payload,
        )

    async def update_repo_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload
    ) -> RepositorySettings:
        """Update repository settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Settings fields accepted by the API.
        :returns: API response payload.
        """
        return await self._model(
            "PUT", self._client._repo_path("repo_settings", owner=owner, repo=repo), RepositorySettings, json=payload
        )

    async def get_repo_settings(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> RepositorySettings:
        """Get repository settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Repository settings payload.
        """
        return await self._model(
            "GET", self._client._repo_path("repo_settings", owner=owner, repo=repo), RepositorySettings
        )

    async def get_pull_request_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> PullRequestSettings:
        """Get pull request settings for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Pull request settings payload.
        """
        return await self._model(
            "GET", self._client._repo_path("pull_request_settings", owner=owner, repo=repo), PullRequestSettings
        )

    async def update_pull_request_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload
    ) -> PullRequestSettings:
        """Update pull request settings for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Pull request settings accepted by the API.
        :returns: API response payload.
        """
        return await self._model(
            "PUT",
            self._client._repo_path("pull_request_settings", owner=owner, repo=repo),
            PullRequestSettings,
            json=payload,
        )

    async def set_member_role(
        self,
        *,
        username: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        permission: Optional[str] = None,
    ) -> RepoMember:
        """Set a repository member role.

        :param username: Member username or login.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param permission: Permission or role name accepted by the API.
        :returns: API response payload.
        """
        return await self._model(
            "PUT",
            self._client._repo_path("members", username, owner=owner, repo=repo),
            RepoMember,
            json={"permission": permission},
        )

    async def transfer(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload
    ) -> RepositoryTransferResult:
        """Transfer a repository to another owner or namespace.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Transfer options accepted by the API.
        :returns: API response payload.
        """
        return await self._model(
            "POST", self._client._repo_path("transfer", owner=owner, repo=repo), RepositoryTransferResult, json=payload
        )

    async def list_customized_roles(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[RepositoryCustomizedRole]:
        """List customized roles for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Customized role definitions.
        """
        data = await self._request("GET", self._client._repo_path("customized_roles", owner=owner, repo=repo))
        return [as_model(item, RepositoryCustomizedRole) for item in data]

    async def get_download_statistics(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params
    ) -> RepositoryDownloadStatistics:
        """Get download statistics for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param params: Query parameters accepted by the statistics endpoint.
        :returns: Download statistics payload.
        """
        return await self._model(
            "GET",
            self._client._repo_path("download_statistics", owner=owner, repo=repo),
            RepositoryDownloadStatistics,
            params=params,
        )

    async def get_contributor_statistics(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[ContributorStatistics]:
        """Get code contribution statistics for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Contributor statistics payload.
        """
        return await self._models(
            "GET",
            self._client._repo_path("contributors", "statistic", owner=owner, repo=repo),
            ContributorStatistics,
        )

    async def list_events(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[APIObject]:
        """List repository events.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Repository event payloads.
        """
        data = await self._request(
            "GET",
            self._client._repo_path("events", owner=owner, repo=repo),
            params={"page": page, "per_page": per_page},
        )
        return [as_model(item, APIObject) for item in data]
