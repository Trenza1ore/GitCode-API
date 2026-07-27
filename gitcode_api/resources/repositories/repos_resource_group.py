"""AbstractReposResource, ReposResource, and AsyncReposResource resource group."""

from abc import ABC, abstractmethod
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
    RepositorySyncResult,
    RepositoryTransferResult,
    RepositoryUploadResult,
    UserSummary,
    as_model,
)
from .._shared import AsyncResource, SyncResource

# mypy: disable-error-code=override
# pylint: disable=invalid-overridden-method,protected-access,redefined-builtin


class AbstractReposResource(ABC):
    """Interface for Repos resource endpoints."""

    @abstractmethod
    def get(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> Repository:
        """Get a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Repository metadata.
        """

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
    def update(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **changes) -> Repository:
        """Update repository metadata.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param changes: Repository fields accepted by the update endpoint.
        :returns: Updated repository metadata.
        """

    @abstractmethod
    def delete(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Delete a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        """

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
    def check_sync_repo(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        branch: Optional[str] = None,
    ) -> RepositorySyncResult:
        """Check fork synchronization task progress.

        Reports sync-task progress or last sync outcome. This does not indicate
        whether the fork is commit-behind its upstream source.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param branch: Optional branch name.
        :returns: Fork synchronization task progress payload.
        """

    @abstractmethod
    def sync_repo(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        branch: Optional[str] = None,
    ) -> RepositorySyncResult:
        """Sync a fork repository with its source repository.

        Starts a fork sync task. A response with ``repo_sync_result`` false and
        ``repo_sync_message`` ``committed`` commonly means the sync was accepted.
        Repeated calls within about 10 minutes may return HTTP 400.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param branch: Optional branch to pull; omit to update all branches.
        :returns: Fork synchronization task result payload.
        """

    @abstractmethod
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

    @abstractmethod
    def list_languages(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> Dict[str, int]:
        """List language statistics for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Mapping of language names to byte counts.
        """

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
    def update_module_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **settings
    ) -> ApiStatusResponse:
        """Update repository module settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param settings: Module settings accepted by the GitCode API.
        :returns: API response payload.
        """

    @abstractmethod
    def update_reviewer_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **settings
    ) -> RepositoryReviewerSettingsUpdate:
        """Update repository reviewer settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param settings: Reviewer settings accepted by the GitCode API.
        :returns: API response payload.
        """

    @abstractmethod
    def set_org_repo_status(self, *, org: str, repo: str, status: int, password: str, **kwargs) -> ApiStatusResponse:
        """Update organization repository status metadata.

        :param org: Organization path.
        :param repo: Repository path.
        :param status: State, 0: open, 2: archived.
        :param password: User password for verification.
        :param kwargs: Additional arguments forwarded directly in request.
        :returns: API response payload.
        """

    @abstractmethod
    def transfer_to_org(self, *, org: str, repo: str, transfer_to: str, password: str, **kwargs) -> ApiStatusResponse:
        """Transfer a repository to an organization.

        :param org: Source organization path.
        :param repo: Repository path.
        :param transfer_to: Target namespace.
        :param password: User password for verification.
        :param kwargs: Additional arguments forwarded directly in request.
        :returns: API response payload.
        """

    @abstractmethod
    def get_transition(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> RepositoryPermissionMode:
        """Get repository transition settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Transition configuration.
        """

    @abstractmethod
    def update_transition(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, mode: Optional[int] = None, **kwargs
    ) -> ApiStatusResponse:
        """Update repository transition settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param mode: Permission management mode: 1 (inheritance) or 2 (independent).
        :param kwargs: Additional arguments forwarded directly in request.
        :returns: API response payload.
        """

    @abstractmethod
    def update_push_config(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        reject_not_signed_by_gpg: Optional[bool] = None,
        commit_message_regex: Optional[str] = None,
        max_file_size: Optional[int] = None,
        skip_rule_for_owner: Optional[bool] = None,
        deny_force_push: Optional[bool] = None,
        **kwargs,
    ) -> RepositoryPushConfig:
        """Update repository push configuration.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param reject_not_signed_by_gpg: Only allow commits with verified GPG signatures.
        :param commit_message_regex: Commit message validation regex.
        :param max_file_size: Commit file size limit in MB.
        :param skip_rule_for_owner: Whether project administrators skip push rules.
        :param deny_force_push: Prohibit force push (including for administrators).
        :param kwargs: Additional arguments forwarded directly in request.
        :returns: Updated push configuration.
        """

    @abstractmethod
    def get_push_config(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> RepositoryPushConfig:
        """Get repository push configuration.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Push configuration payload.
        """

    @abstractmethod
    def upload_image(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        body: Optional[str] = None,
        file_name: Optional[str] = None,
        **kwargs,
    ) -> RepositoryUploadResult:
        """Upload an image asset for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param body: File content in base64 format (limit: 20 MB).
        :param file_name: File name.
        :param kwargs: Additional arguments forwarded directly in request.
        :returns: Uploaded image metadata.
        """

    @abstractmethod
    def upload_file(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        file: Optional[str] = None,
        **kwargs,
    ) -> RepositoryUploadResult:
        """Upload a file asset for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param file: File content in base64 format (limit: 20 MB).
        :param kwargs: Additional arguments forwarded directly in request.
        :returns: Uploaded file metadata.
        """

    @abstractmethod
    def update_repo_settings(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        disable_fork: Optional[bool] = None,
        forbidden_developer_create_branch: Optional[bool] = None,
        forbidden_developer_create_tag: Optional[bool] = None,
        forbidden_committer_create_branch: Optional[bool] = None,
        forbidden_developer_create_branch_user_ids: Optional[str] = None,
        branch_name_regex: Optional[str] = None,
        tag_name_regex: Optional[str] = None,
        generate_pre_merge_ref: Optional[bool] = None,
        rebase_disable_trigger_webhook: Optional[bool] = None,
        open_gpg_verified: Optional[bool] = None,
        include_lfs_objects: Optional[bool] = None,
        **kwargs,
    ) -> RepositorySettings:
        """Update repository settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param disable_fork: Disable forking.
        :param forbidden_developer_create_branch: Forbid developers from creating branches.
        :param forbidden_developer_create_tag: Forbid developers from creating tags.
        :param forbidden_committer_create_branch: Forbid committers from creating branches.
        :param forbidden_developer_create_branch_user_ids: User IDs forbidden from creating branches.
        :param branch_name_regex: Branch name validation regex.
        :param tag_name_regex: Tag name validation regex.
        :param generate_pre_merge_ref: Generate pre-merge ref.
        :param rebase_disable_trigger_webhook: Disable webhook trigger on rebase.
        :param open_gpg_verified: Enable GPG verification.
        :param include_lfs_objects: Include LFS objects in ZIP download.
        :param kwargs: Additional arguments forwarded directly in request.
        :returns: Updated repository settings.
        """

    @abstractmethod
    def get_repo_settings(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> RepositorySettings:
        """Get repository settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Repository settings payload.
        """

    @abstractmethod
    def get_pull_request_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> PullRequestSettings:
        """Get pull request settings for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Pull request settings payload.
        """

    @abstractmethod
    def update_pull_request_settings(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        approval_required_reviewers_enable: Optional[bool] = None,
        approval_required_reviewers: Optional[int] = None,
        only_allow_merge_if_all_discussions_are_resolved: Optional[bool] = None,
        only_allow_merge_if_pipeline_succeeds: Optional[bool] = None,
        disable_merge_by_self: Optional[bool] = None,
        can_force_merge: Optional[bool] = None,
        add_notes_after_merged: Optional[bool] = None,
        mark_auto_merged_mr_as_closed: Optional[bool] = None,
        can_reopen: Optional[bool] = None,
        delete_source_branch_when_merged: Optional[bool] = None,
        disable_squash_merge: Optional[bool] = None,
        auto_squash_merge: Optional[bool] = None,
        merge_method: Optional[str] = None,
        squash_merge_with_no_merge_commit: Optional[bool] = None,
        merged_commit_author: Optional[str] = None,
        approval_required_approvers: Optional[int] = None,
        approval_approver_ids: Optional[str] = None,
        approval_tester_ids: Optional[str] = None,
        approval_required_testers: Optional[int] = None,
        is_check_cla: Optional[bool] = None,
        is_allow_lite_merge_request: Optional[bool] = None,
        lite_merge_request_prefix_title: Optional[str] = None,
        close_issue_when_mr_merged: Optional[bool] = None,
        **kwargs,
    ) -> PullRequestSettings:
        """Update pull request settings for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param approval_required_reviewers_enable: Enable required reviewers approval.
        :param approval_required_reviewers: Minimum number of required reviewers (1-5, or 0 to disable).
        :param only_allow_merge_if_all_discussions_are_resolved: Require all discussions resolved before merge.
        :param only_allow_merge_if_pipeline_succeeds: Only allow merge when pipeline succeeds.
        :param disable_merge_by_self: Forbid merging self-created pull requests.
        :param can_force_merge: Allow administrators to force merge.
        :param add_notes_after_merged: Allow code review comments after merge.
        :param mark_auto_merged_mr_as_closed: Mark auto-merged MRs as closed.
        :param can_reopen: Allow reopening closed pull requests.
        :param delete_source_branch_when_merged: Delete source branch when merged.
        :param disable_squash_merge: Disable squash merge.
        :param auto_squash_merge: Default enable squash merge for new pull requests.
        :param merge_method: Merge method (``merge``, ``rebase_merge``, or ``ff``).
        :param squash_merge_with_no_merge_commit: Squash merge without producing a merge commit.
        :param merged_commit_author: Merge commit author (``merged_by`` or ``created_by``).
        :param approval_required_approvers: Number of required approvers.
        :param approval_approver_ids: Project reviewer user IDs, comma-separated.
        :param approval_tester_ids: Project tester user IDs, comma-separated.
        :param approval_required_testers: Minimum number of testers that must pass.
        :param is_check_cla: Whether to verify CLA.
        :param is_allow_lite_merge_request: Enable lightweight pull requests.
        :param lite_merge_request_prefix_title: Title prefix for lightweight pull requests.
        :param close_issue_when_mr_merged: Default check "close linked issues on merge".
        :param kwargs: Additional arguments forwarded directly in request.
        :returns: Updated pull request settings.
        """

    @abstractmethod
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

    @abstractmethod
    def transfer(self, *, owner: str, repo: str, new_owner: str, **kwargs) -> RepositoryTransferResult:
        """Transfer a repository to another owner or namespace.

        :param owner: Repository owner path.
        :param repo: Repository name.
        :param new_owner: Target namespace to transfer the repository to.
        :param kwargs: Additional arguments forwarded directly in request.
        :returns: Transfer result.
        """

    @abstractmethod
    def list_customized_roles(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[RepositoryCustomizedRole]:
        """List customized roles for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Customized role definitions.
        """

    @abstractmethod
    def get_download_statistics(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        direction: Optional[str] = None,
        **kwargs,
    ) -> RepositoryDownloadStatistics:
        """Get download statistics for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param start_date: Start date filter (e.g. ``2024-01-06``).
        :param end_date: End date filter (e.g. ``2024-12-06``).
        :param direction: Sort direction: ``asc`` or ``desc``. Default: ``desc``.
        :param kwargs: Additional arguments forwarded directly in request.
        :returns: Download statistics payload.
        """

    @abstractmethod
    def get_contributor_statistics(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[ContributorStatistics]:
        """Get code contribution statistics for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Contributor statistics payload.
        """

    @abstractmethod
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


class ReposResource(SyncResource, AbstractReposResource):
    """Synchronous repository endpoints."""

    def get(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> Repository:
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
        return self._model("PATCH", self._client._repo_path(owner=owner, repo=repo), Repository, json=changes)

    def delete(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
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
        return self._models(
            "GET",
            self._client._repo_path("forks", owner=owner, repo=repo),
            Repository,
            params={"sort": sort, "page": page, "per_page": per_page},
        )

    def check_sync_repo(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        branch: Optional[str] = None,
    ) -> RepositorySyncResult:
        return self._model(
            "GET",
            self._client._repo_path("sync_repo", owner=owner, repo=repo),
            RepositorySyncResult,
            params={"branch": branch},
        )

    def sync_repo(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        branch: Optional[str] = None,
    ) -> RepositorySyncResult:
        return self._model(
            "PUT",
            self._client._repo_path("sync_repo", owner=owner, repo=repo),
            RepositorySyncResult,
            json={"branch": branch},
        )

    def list_contributors(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Contributor]:
        return self._models(
            "GET",
            self._client._repo_path("contributors", owner=owner, repo=repo),
            Contributor,
            params={"page": page, "per_page": per_page},
        )

    def list_languages(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> Dict[str, int]:
        return self._request("GET", self._client._repo_path("languages", owner=owner, repo=repo))

    def list_stargazers(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[UserSummary]:
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
        return self._models(
            "GET",
            self._client._repo_path("subscribers", owner=owner, repo=repo),
            UserSummary,
            params={"page": page, "per_page": per_page},
        )

    def update_module_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **settings
    ) -> ApiStatusResponse:
        return self._model(
            "PUT",
            self._client._repo_path("module", "setting", owner=owner, repo=repo),
            ApiStatusResponse,
            json=settings,
        )

    def update_reviewer_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **settings
    ) -> RepositoryReviewerSettingsUpdate:
        return self._model(
            "PUT",
            self._client._repo_path("reviewer", owner=owner, repo=repo),
            RepositoryReviewerSettingsUpdate,
            json=settings,
        )

    def set_org_repo_status(self, *, org: str, repo: str, status: int, password: str, **kwargs) -> ApiStatusResponse:
        return self._model(
            "PUT",
            self._client._path("org", org, "repo", repo, "status"),
            ApiStatusResponse,
            json={"status": status, "password": password, **kwargs},
        )

    def transfer_to_org(self, *, org: str, repo: str, transfer_to: str, password: str, **kwargs) -> ApiStatusResponse:
        return self._model(
            "POST",
            self._client._path("org", org, "projects", repo, "transfer"),
            ApiStatusResponse,
            json={"transfer_to": transfer_to, "password": password, **kwargs},
        )

    def get_transition(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> RepositoryPermissionMode:
        return self._model(
            "GET", self._client._repo_path("transition", owner=owner, repo=repo), RepositoryPermissionMode
        )

    def update_transition(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, mode: Optional[int] = None, **kwargs
    ) -> ApiStatusResponse:
        return self._model(
            "PUT",
            self._client._repo_path("transition", owner=owner, repo=repo),
            ApiStatusResponse,
            json={"mode": mode, **kwargs},
        )

    def update_push_config(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        reject_not_signed_by_gpg: Optional[bool] = None,
        commit_message_regex: Optional[str] = None,
        max_file_size: Optional[int] = None,
        skip_rule_for_owner: Optional[bool] = None,
        deny_force_push: Optional[bool] = None,
        **kwargs,
    ) -> RepositoryPushConfig:
        return self._model(
            "PUT",
            self._client._repo_path("push_config", owner=owner, repo=repo),
            RepositoryPushConfig,
            json={
                "reject_not_signed_by_gpg": reject_not_signed_by_gpg,
                "commit_message_regex": commit_message_regex,
                "max_file_size": max_file_size,
                "skip_rule_for_owner": skip_rule_for_owner,
                "deny_force_push": deny_force_push,
                **kwargs,
            },
        )

    def get_push_config(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> RepositoryPushConfig:
        return self._model("GET", self._client._repo_path("push_config", owner=owner, repo=repo), RepositoryPushConfig)

    def upload_image(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        body: Optional[str] = None,
        file_name: Optional[str] = None,
        **kwargs,
    ) -> RepositoryUploadResult:
        return self._model(
            "POST",
            self._client._repo_path("img", "upload", owner=owner, repo=repo),
            RepositoryUploadResult,
            json={"body": body, "file_name": file_name, **kwargs},
        )

    def upload_file(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        file: Optional[str] = None,
        **kwargs,
    ) -> RepositoryUploadResult:
        return self._model(
            "POST",
            self._client._repo_path("file", "upload", owner=owner, repo=repo),
            RepositoryUploadResult,
            json={"file": file, **kwargs},
        )

    def update_repo_settings(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        disable_fork: Optional[bool] = None,
        forbidden_developer_create_branch: Optional[bool] = None,
        forbidden_developer_create_tag: Optional[bool] = None,
        forbidden_committer_create_branch: Optional[bool] = None,
        forbidden_developer_create_branch_user_ids: Optional[str] = None,
        branch_name_regex: Optional[str] = None,
        tag_name_regex: Optional[str] = None,
        generate_pre_merge_ref: Optional[bool] = None,
        rebase_disable_trigger_webhook: Optional[bool] = None,
        open_gpg_verified: Optional[bool] = None,
        include_lfs_objects: Optional[bool] = None,
        **kwargs,
    ) -> RepositorySettings:
        return self._model(
            "PUT",
            self._client._repo_path("repo_settings", owner=owner, repo=repo),
            RepositorySettings,
            json={
                "disable_fork": disable_fork,
                "forbidden_developer_create_branch": forbidden_developer_create_branch,
                "forbidden_developer_create_tag": forbidden_developer_create_tag,
                "forbidden_committer_create_branch": forbidden_committer_create_branch,
                "forbidden_developer_create_branch_user_ids": forbidden_developer_create_branch_user_ids,
                "branch_name_regex": branch_name_regex,
                "tag_name_regex": tag_name_regex,
                "generate_pre_merge_ref": generate_pre_merge_ref,
                "rebase_disable_trigger_webhook": rebase_disable_trigger_webhook,
                "open_gpg_verified": open_gpg_verified,
                "include_lfs_objects": include_lfs_objects,
                **kwargs,
            },
        )

    def get_repo_settings(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> RepositorySettings:
        return self._model("GET", self._client._repo_path("repo_settings", owner=owner, repo=repo), RepositorySettings)

    def get_pull_request_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> PullRequestSettings:
        return self._model(
            "GET", self._client._repo_path("pull_request_settings", owner=owner, repo=repo), PullRequestSettings
        )

    def update_pull_request_settings(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        approval_required_reviewers_enable: Optional[bool] = None,
        approval_required_reviewers: Optional[int] = None,
        only_allow_merge_if_all_discussions_are_resolved: Optional[bool] = None,
        only_allow_merge_if_pipeline_succeeds: Optional[bool] = None,
        disable_merge_by_self: Optional[bool] = None,
        can_force_merge: Optional[bool] = None,
        add_notes_after_merged: Optional[bool] = None,
        mark_auto_merged_mr_as_closed: Optional[bool] = None,
        can_reopen: Optional[bool] = None,
        delete_source_branch_when_merged: Optional[bool] = None,
        disable_squash_merge: Optional[bool] = None,
        auto_squash_merge: Optional[bool] = None,
        merge_method: Optional[str] = None,
        squash_merge_with_no_merge_commit: Optional[bool] = None,
        merged_commit_author: Optional[str] = None,
        approval_required_approvers: Optional[int] = None,
        approval_approver_ids: Optional[str] = None,
        approval_tester_ids: Optional[str] = None,
        approval_required_testers: Optional[int] = None,
        is_check_cla: Optional[bool] = None,
        is_allow_lite_merge_request: Optional[bool] = None,
        lite_merge_request_prefix_title: Optional[str] = None,
        close_issue_when_mr_merged: Optional[bool] = None,
        **kwargs,
    ) -> PullRequestSettings:
        return self._model(
            "PUT",
            self._client._repo_path("pull_request_settings", owner=owner, repo=repo),
            PullRequestSettings,
            json={
                "approval_required_reviewers_enable": approval_required_reviewers_enable,
                "approval_required_reviewers": approval_required_reviewers,
                "only_allow_merge_if_all_discussions_are_resolved": only_allow_merge_if_all_discussions_are_resolved,
                "only_allow_merge_if_pipeline_succeeds": only_allow_merge_if_pipeline_succeeds,
                "disable_merge_by_self": disable_merge_by_self,
                "can_force_merge": can_force_merge,
                "add_notes_after_merged": add_notes_after_merged,
                "mark_auto_merged_mr_as_closed": mark_auto_merged_mr_as_closed,
                "can_reopen": can_reopen,
                "delete_source_branch_when_merged": delete_source_branch_when_merged,
                "disable_squash_merge": disable_squash_merge,
                "auto_squash_merge": auto_squash_merge,
                "merge_method": merge_method,
                "squash_merge_with_no_merge_commit": squash_merge_with_no_merge_commit,
                "merged_commit_author": merged_commit_author,
                "approval_required_approvers": approval_required_approvers,
                "approval_approver_ids": approval_approver_ids,
                "approval_tester_ids": approval_tester_ids,
                "approval_required_testers": approval_required_testers,
                "is_check_cla": is_check_cla,
                "is_allow_lite_merge_request": is_allow_lite_merge_request,
                "lite_merge_request_prefix_title": lite_merge_request_prefix_title,
                "close_issue_when_mr_merged": close_issue_when_mr_merged,
                **kwargs,
            },
        )

    def set_member_role(
        self,
        *,
        username: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        permission: Optional[str] = None,
    ) -> RepoMember:
        return self._model(
            "PUT",
            self._client._repo_path("members", username, owner=owner, repo=repo),
            RepoMember,
            json={"permission": permission},
        )

    def transfer(self, *, owner: str, repo: str, new_owner: str, **kwargs) -> RepositoryTransferResult:
        return self._model(
            "POST",
            self._client._repo_path("transfer", owner=owner, repo=repo),
            RepositoryTransferResult,
            json={"new_owner": new_owner, **kwargs},
        )

    def list_customized_roles(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[RepositoryCustomizedRole]:
        data = self._request("GET", self._client._repo_path("customized_roles", owner=owner, repo=repo))
        return [as_model(item, RepositoryCustomizedRole) for item in data]

    def get_download_statistics(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        direction: Optional[str] = None,
        **kwargs,
    ) -> RepositoryDownloadStatistics:
        return self._model(
            "GET",
            self._client._repo_path("download_statistics", owner=owner, repo=repo),
            RepositoryDownloadStatistics,
            params={"start_date": start_date, "end_date": end_date, "direction": direction, **kwargs},
        )

    def get_contributor_statistics(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[ContributorStatistics]:
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
        data = self._request(
            "GET",
            self._client._repo_path("events", owner=owner, repo=repo),
            params={"page": page, "per_page": per_page},
        )
        return [as_model(item, APIObject) for item in data]


class AsyncReposResource(AsyncResource, AbstractReposResource):
    """Asynchronous repository endpoints.

    Mirrors :class:`ReposResource`; see that class for parameters and JSON fields
    (Repository API in ``docs/rest_api/repos``).
    """

    async def get(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> Repository:
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
        return await self._model("PATCH", self._client._repo_path(owner=owner, repo=repo), Repository, json=changes)

    async def delete(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
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
        return await self._models(
            "GET",
            self._client._repo_path("forks", owner=owner, repo=repo),
            Repository,
            params={"sort": sort, "page": page, "per_page": per_page},
        )

    async def check_sync_repo(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        branch: Optional[str] = None,
    ) -> RepositorySyncResult:
        return await self._model(
            "GET",
            self._client._repo_path("sync_repo", owner=owner, repo=repo),
            RepositorySyncResult,
            params={"branch": branch},
        )

    async def sync_repo(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        branch: Optional[str] = None,
    ) -> RepositorySyncResult:
        return await self._model(
            "PUT",
            self._client._repo_path("sync_repo", owner=owner, repo=repo),
            RepositorySyncResult,
            json={"branch": branch},
        )

    async def list_contributors(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Contributor]:
        return await self._models(
            "GET",
            self._client._repo_path("contributors", owner=owner, repo=repo),
            Contributor,
            params={"page": page, "per_page": per_page},
        )

    async def list_languages(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> Dict[str, int]:
        return await self._request("GET", self._client._repo_path("languages", owner=owner, repo=repo))

    async def list_stargazers(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[UserSummary]:
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
        return await self._models(
            "GET",
            self._client._repo_path("subscribers", owner=owner, repo=repo),
            UserSummary,
            params={"page": page, "per_page": per_page},
        )

    async def update_module_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **settings
    ) -> ApiStatusResponse:
        return await self._model(
            "PUT",
            self._client._repo_path("module", "setting", owner=owner, repo=repo),
            ApiStatusResponse,
            json=settings,
        )

    async def update_reviewer_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **settings
    ) -> RepositoryReviewerSettingsUpdate:
        return await self._model(
            "PUT",
            self._client._repo_path("reviewer", owner=owner, repo=repo),
            RepositoryReviewerSettingsUpdate,
            json=settings,
        )

    async def set_org_repo_status(
        self, *, org: str, repo: str, status: int, password: str, **kwargs
    ) -> ApiStatusResponse:
        return await self._model(
            "PUT",
            self._client._path("org", org, "repo", repo, "status"),
            ApiStatusResponse,
            json={"status": status, "password": password, **kwargs},
        )

    async def transfer_to_org(
        self, *, org: str, repo: str, transfer_to: str, password: str, **kwargs
    ) -> ApiStatusResponse:
        return await self._model(
            "POST",
            self._client._path("org", org, "projects", repo, "transfer"),
            ApiStatusResponse,
            json={"transfer_to": transfer_to, "password": password, **kwargs},
        )

    async def get_transition(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> RepositoryPermissionMode:
        return await self._model(
            "GET", self._client._repo_path("transition", owner=owner, repo=repo), RepositoryPermissionMode
        )

    async def update_transition(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, mode: Optional[int] = None, **kwargs
    ) -> ApiStatusResponse:
        return await self._model(
            "PUT",
            self._client._repo_path("transition", owner=owner, repo=repo),
            ApiStatusResponse,
            json={"mode": mode, **kwargs},
        )

    async def update_push_config(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        reject_not_signed_by_gpg: Optional[bool] = None,
        commit_message_regex: Optional[str] = None,
        max_file_size: Optional[int] = None,
        skip_rule_for_owner: Optional[bool] = None,
        deny_force_push: Optional[bool] = None,
        **kwargs,
    ) -> RepositoryPushConfig:
        return await self._model(
            "PUT",
            self._client._repo_path("push_config", owner=owner, repo=repo),
            RepositoryPushConfig,
            json={
                "reject_not_signed_by_gpg": reject_not_signed_by_gpg,
                "commit_message_regex": commit_message_regex,
                "max_file_size": max_file_size,
                "skip_rule_for_owner": skip_rule_for_owner,
                "deny_force_push": deny_force_push,
                **kwargs,
            },
        )

    async def get_push_config(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> RepositoryPushConfig:
        return await self._model(
            "GET", self._client._repo_path("push_config", owner=owner, repo=repo), RepositoryPushConfig
        )

    async def upload_image(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        body: Optional[str] = None,
        file_name: Optional[str] = None,
        **kwargs,
    ) -> RepositoryUploadResult:
        return await self._model(
            "POST",
            self._client._repo_path("img", "upload", owner=owner, repo=repo),
            RepositoryUploadResult,
            json={"body": body, "file_name": file_name, **kwargs},
        )

    async def upload_file(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        file: Optional[str] = None,
        **kwargs,
    ) -> RepositoryUploadResult:
        return await self._model(
            "POST",
            self._client._repo_path("file", "upload", owner=owner, repo=repo),
            RepositoryUploadResult,
            json={"file": file, **kwargs},
        )

    async def update_repo_settings(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        disable_fork: Optional[bool] = None,
        forbidden_developer_create_branch: Optional[bool] = None,
        forbidden_developer_create_tag: Optional[bool] = None,
        forbidden_committer_create_branch: Optional[bool] = None,
        forbidden_developer_create_branch_user_ids: Optional[str] = None,
        branch_name_regex: Optional[str] = None,
        tag_name_regex: Optional[str] = None,
        generate_pre_merge_ref: Optional[bool] = None,
        rebase_disable_trigger_webhook: Optional[bool] = None,
        open_gpg_verified: Optional[bool] = None,
        include_lfs_objects: Optional[bool] = None,
        **kwargs,
    ) -> RepositorySettings:
        return await self._model(
            "PUT",
            self._client._repo_path("repo_settings", owner=owner, repo=repo),
            RepositorySettings,
            json={
                "disable_fork": disable_fork,
                "forbidden_developer_create_branch": forbidden_developer_create_branch,
                "forbidden_developer_create_tag": forbidden_developer_create_tag,
                "forbidden_committer_create_branch": forbidden_committer_create_branch,
                "forbidden_developer_create_branch_user_ids": forbidden_developer_create_branch_user_ids,
                "branch_name_regex": branch_name_regex,
                "tag_name_regex": tag_name_regex,
                "generate_pre_merge_ref": generate_pre_merge_ref,
                "rebase_disable_trigger_webhook": rebase_disable_trigger_webhook,
                "open_gpg_verified": open_gpg_verified,
                "include_lfs_objects": include_lfs_objects,
                **kwargs,
            },
        )

    async def get_repo_settings(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> RepositorySettings:
        return await self._model(
            "GET", self._client._repo_path("repo_settings", owner=owner, repo=repo), RepositorySettings
        )

    async def get_pull_request_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> PullRequestSettings:
        return await self._model(
            "GET", self._client._repo_path("pull_request_settings", owner=owner, repo=repo), PullRequestSettings
        )

    async def update_pull_request_settings(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        approval_required_reviewers_enable: Optional[bool] = None,
        approval_required_reviewers: Optional[int] = None,
        only_allow_merge_if_all_discussions_are_resolved: Optional[bool] = None,
        only_allow_merge_if_pipeline_succeeds: Optional[bool] = None,
        disable_merge_by_self: Optional[bool] = None,
        can_force_merge: Optional[bool] = None,
        add_notes_after_merged: Optional[bool] = None,
        mark_auto_merged_mr_as_closed: Optional[bool] = None,
        can_reopen: Optional[bool] = None,
        delete_source_branch_when_merged: Optional[bool] = None,
        disable_squash_merge: Optional[bool] = None,
        auto_squash_merge: Optional[bool] = None,
        merge_method: Optional[str] = None,
        squash_merge_with_no_merge_commit: Optional[bool] = None,
        merged_commit_author: Optional[str] = None,
        approval_required_approvers: Optional[int] = None,
        approval_approver_ids: Optional[str] = None,
        approval_tester_ids: Optional[str] = None,
        approval_required_testers: Optional[int] = None,
        is_check_cla: Optional[bool] = None,
        is_allow_lite_merge_request: Optional[bool] = None,
        lite_merge_request_prefix_title: Optional[str] = None,
        close_issue_when_mr_merged: Optional[bool] = None,
        **kwargs,
    ) -> PullRequestSettings:
        return await self._model(
            "PUT",
            self._client._repo_path("pull_request_settings", owner=owner, repo=repo),
            PullRequestSettings,
            json={
                "approval_required_reviewers_enable": approval_required_reviewers_enable,
                "approval_required_reviewers": approval_required_reviewers,
                "only_allow_merge_if_all_discussions_are_resolved": only_allow_merge_if_all_discussions_are_resolved,
                "only_allow_merge_if_pipeline_succeeds": only_allow_merge_if_pipeline_succeeds,
                "disable_merge_by_self": disable_merge_by_self,
                "can_force_merge": can_force_merge,
                "add_notes_after_merged": add_notes_after_merged,
                "mark_auto_merged_mr_as_closed": mark_auto_merged_mr_as_closed,
                "can_reopen": can_reopen,
                "delete_source_branch_when_merged": delete_source_branch_when_merged,
                "disable_squash_merge": disable_squash_merge,
                "auto_squash_merge": auto_squash_merge,
                "merge_method": merge_method,
                "squash_merge_with_no_merge_commit": squash_merge_with_no_merge_commit,
                "merged_commit_author": merged_commit_author,
                "approval_required_approvers": approval_required_approvers,
                "approval_approver_ids": approval_approver_ids,
                "approval_tester_ids": approval_tester_ids,
                "approval_required_testers": approval_required_testers,
                "is_check_cla": is_check_cla,
                "is_allow_lite_merge_request": is_allow_lite_merge_request,
                "lite_merge_request_prefix_title": lite_merge_request_prefix_title,
                "close_issue_when_mr_merged": close_issue_when_mr_merged,
                **kwargs,
            },
        )

    async def set_member_role(
        self,
        *,
        username: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        permission: Optional[str] = None,
    ) -> RepoMember:
        return await self._model(
            "PUT",
            self._client._repo_path("members", username, owner=owner, repo=repo),
            RepoMember,
            json={"permission": permission},
        )

    async def transfer(self, *, owner: str, repo: str, new_owner: str, **kwargs) -> RepositoryTransferResult:
        return await self._model(
            "POST",
            self._client._repo_path("transfer", owner=owner, repo=repo),
            RepositoryTransferResult,
            json={"new_owner": new_owner, **kwargs},
        )

    async def list_customized_roles(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[RepositoryCustomizedRole]:
        data = await self._request("GET", self._client._repo_path("customized_roles", owner=owner, repo=repo))
        return [as_model(item, RepositoryCustomizedRole) for item in data]

    async def get_download_statistics(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        direction: Optional[str] = None,
        **kwargs,
    ) -> RepositoryDownloadStatistics:
        return await self._model(
            "GET",
            self._client._repo_path("download_statistics", owner=owner, repo=repo),
            RepositoryDownloadStatistics,
            params={"start_date": start_date, "end_date": end_date, "direction": direction, **kwargs},
        )

    async def get_contributor_statistics(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[ContributorStatistics]:
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
        data = await self._request(
            "GET",
            self._client._repo_path("events", owner=owner, repo=repo),
            params={"page": page, "per_page": per_page},
        )
        return [as_model(item, APIObject) for item in data]
