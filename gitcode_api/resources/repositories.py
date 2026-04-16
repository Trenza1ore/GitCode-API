"""Repository, contents, branch, and commit resource groups."""

from typing import Any, Dict, List, Optional, Union

from .._models import (
    APIObject,
    Blob,
    Branch,
    Commit,
    CommitComment,
    CommitComparison,
    CommitResult,
    ContentObject,
    Contributor,
    ProtectedBranch,
    Repository,
    Tree,
    UserSummary,
    as_model,
)
from ._shared import AsyncResource, SyncResource


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

    def update(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **changes: Any) -> Repository:
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
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **settings: Any
    ) -> APIObject:
        """Update repository module settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param settings: Module settings accepted by the GitCode API.
        :returns: API response payload.
        """
        return self._model(
            "PUT",
            self._client._repo_path("module", "setting", owner=owner, repo=repo),
            APIObject,
            json=settings,
        )

    def update_reviewer_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **settings: Any
    ) -> APIObject:
        """Update repository reviewer settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param settings: Reviewer settings accepted by the GitCode API.
        :returns: API response payload.
        """
        return self._model(
            "PUT",
            self._client._repo_path("reviewer", owner=owner, repo=repo),
            APIObject,
            json=settings,
        )

    def set_org_repo_status(self, *, org: str, repo: str, **payload: Any) -> APIObject:
        """Update organization repository status metadata.

        :param org: Organization path.
        :param repo: Repository path.
        :param payload: Status fields accepted by the API.
        :returns: API response payload.
        """
        return self._model("PUT", self._client._path("org", org, "repo", repo, "status"), APIObject, json=payload)

    def transfer_to_org(self, *, org: str, repo: str, **payload: Any) -> APIObject:
        """Transfer a repository to an organization.

        :param org: Destination organization path.
        :param repo: Repository path.
        :param payload: Transfer options accepted by the API.
        :returns: API response payload.
        """
        return self._model(
            "POST", self._client._path("org", org, "projects", repo, "transfer"), APIObject, json=payload
        )

    def get_transition(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> APIObject:
        """Get repository transition settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Transition configuration.
        """
        return self._model("GET", self._client._repo_path("transition", owner=owner, repo=repo), APIObject)

    def update_transition(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload: Any
    ) -> APIObject:
        """Update repository transition settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Transition settings accepted by the API.
        :returns: API response payload.
        """
        return self._model(
            "PUT", self._client._repo_path("transition", owner=owner, repo=repo), APIObject, json=payload
        )

    def update_push_config(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload: Any
    ) -> APIObject:
        """Update repository push configuration.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Push configuration values accepted by the API.
        :returns: API response payload.
        """
        return self._model(
            "PUT", self._client._repo_path("push_config", owner=owner, repo=repo), APIObject, json=payload
        )

    def get_push_config(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> APIObject:
        """Get repository push configuration.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Push configuration payload.
        """
        return self._model("GET", self._client._repo_path("push_config", owner=owner, repo=repo), APIObject)

    def upload_image(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload: Any) -> APIObject:
        """Upload an image asset for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Upload fields accepted by the API.
        :returns: Uploaded image metadata.
        """
        return self._model(
            "POST", self._client._repo_path("img", "upload", owner=owner, repo=repo), APIObject, json=payload
        )

    def upload_file(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload: Any) -> APIObject:
        """Upload a file asset for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Upload fields accepted by the API.
        :returns: Uploaded file metadata.
        """
        return self._model(
            "POST", self._client._repo_path("file", "upload", owner=owner, repo=repo), APIObject, json=payload
        )

    def update_repo_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload: Any
    ) -> APIObject:
        """Update repository settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Settings fields accepted by the API.
        :returns: API response payload.
        """
        return self._model(
            "PUT", self._client._repo_path("repo_settings", owner=owner, repo=repo), APIObject, json=payload
        )

    def get_repo_settings(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> APIObject:
        """Get repository settings.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Repository settings payload.
        """
        return self._model("GET", self._client._repo_path("repo_settings", owner=owner, repo=repo), APIObject)

    def get_pull_request_settings(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> APIObject:
        """Get pull request settings for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Pull request settings payload.
        """
        return self._model("GET", self._client._repo_path("pull_request_settings", owner=owner, repo=repo), APIObject)

    def update_pull_request_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload: Any
    ) -> APIObject:
        """Update pull request settings for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Pull request settings accepted by the API.
        :returns: API response payload.
        """
        return self._model(
            "PUT",
            self._client._repo_path("pull_request_settings", owner=owner, repo=repo),
            APIObject,
            json=payload,
        )

    def set_member_role(
        self,
        *,
        username: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        permission: Optional[str] = None,
    ) -> APIObject:
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
            APIObject,
            json={"permission": permission},
        )

    def transfer(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload: Any) -> APIObject:
        """Transfer a repository to another owner or namespace.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param payload: Transfer options accepted by the API.
        :returns: API response payload.
        """
        return self._model("POST", self._client._repo_path("transfer", owner=owner, repo=repo), APIObject, json=payload)

    def list_customized_roles(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> List[APIObject]:
        """List customized roles for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Customized role definitions.
        """
        data = self._request("GET", self._client._repo_path("customized_roles", owner=owner, repo=repo))
        return [as_model(item, APIObject) for item in data]

    def get_download_statistics(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params: Any
    ) -> APIObject:
        """Get download statistics for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param params: Query parameters accepted by the statistics endpoint.
        :returns: Download statistics payload.
        """
        return self._model(
            "GET",
            self._client._repo_path("download_statistics", owner=owner, repo=repo),
            APIObject,
            params=params,
        )

    def get_contributor_statistics(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> APIObject:
        """Get code contribution statistics for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Contributor statistics payload.
        """
        return self._model(
            "GET",
            self._client._repo_path("contributors", "statistic", owner=owner, repo=repo),
            APIObject,
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


class RepoContentsResource(SyncResource):
    """Synchronous repository contents endpoints."""

    def get(
        self,
        *,
        path: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        ref: Optional[str] = None,
    ) -> ContentObject:
        """Get a file or directory entry from a repository.

        :param path: Repository-relative file path.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param ref: Optional branch, tag, or commit SHA.
        :returns: Content metadata and payload details.
        """
        return self._model(
            "GET",
            self._client._repo_file_path("contents", path, owner=owner, repo=repo),
            ContentObject,
            params={"ref": ref},
        )

    def create(
        self,
        *,
        path: str,
        content: str,
        message: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        branch: Optional[str] = None,
        author_name: Optional[str] = None,
        author_email: Optional[str] = None,
    ) -> CommitResult:
        """Create a file in a repository.

        :param path: Repository-relative file path.
        :param content: File content, typically base64-encoded for this API.
        :param message: Commit message.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param branch: Optional target branch.
        :param author_name: Optional commit author name.
        :param author_email: Optional commit author email.
        :returns: Commit result payload.
        """
        return self._model(
            "POST",
            self._client._repo_file_path("contents", path, owner=owner, repo=repo),
            CommitResult,
            json={
                "content": content,
                "message": message,
                "branch": branch,
                "author": {"name": author_name, "email": author_email},
            },
        )

    def update(
        self,
        *,
        path: str,
        content: str,
        message: str,
        sha: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        branch: Optional[str] = None,
        author_name: Optional[str] = None,
        author_email: Optional[str] = None,
    ) -> CommitResult:
        """Update a file in a repository.

        :param path: Repository-relative file path.
        :param content: Updated file content, typically base64-encoded.
        :param message: Commit message.
        :param sha: Current blob SHA required by the API.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param branch: Optional target branch.
        :param author_name: Optional commit author name.
        :param author_email: Optional commit author email.
        :returns: Commit result payload.
        """
        return self._model(
            "PUT",
            self._client._repo_file_path("contents", path, owner=owner, repo=repo),
            CommitResult,
            json={
                "content": content,
                "message": message,
                "sha": sha,
                "branch": branch,
                "author": {"name": author_name, "email": author_email},
            },
        )

    def delete(
        self,
        *,
        path: str,
        message: str,
        sha: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        branch: Optional[str] = None,
        author_name: Optional[str] = None,
        author_email: Optional[str] = None,
    ) -> CommitResult:
        """Delete a file from a repository.

        :param path: Repository-relative file path.
        :param message: Commit message.
        :param sha: Current blob SHA required by the API.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param branch: Optional target branch.
        :param author_name: Optional commit author name.
        :param author_email: Optional commit author email.
        :returns: Commit result payload.
        """
        return self._model(
            "DELETE",
            self._client._repo_file_path("contents", path, owner=owner, repo=repo),
            CommitResult,
            json={
                "message": message,
                "sha": sha,
                "branch": branch,
                "author": {"name": author_name, "email": author_email},
            },
        )

    def list_paths(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        ref_name: Optional[str] = None,
        file_name: Optional[str] = None,
    ) -> List[str]:
        """List repository paths known to GitCode.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param ref_name: Optional ref name to inspect.
        :param file_name: Optional filename filter.
        :returns: Matching repository paths.
        """
        return self._request(
            "GET",
            self._client._repo_path("file_list", owner=owner, repo=repo),
            params={"ref_name": ref_name, "file_name": file_name},
        )

    def get_tree(
        self,
        *,
        sha: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        recursive: Optional[int] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> Tree:
        """Get a Git tree object.

        :param sha: Tree SHA.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param recursive: Whether to traverse recursively.
        :param page: Page number for large trees.
        :param per_page: Page size for large trees.
        :returns: Tree metadata and entries.
        """
        return self._model(
            "GET",
            self._client._repo_path("git", "trees", sha, owner=owner, repo=repo),
            Tree,
            params={"recursive": recursive, "page": page, "per_page": per_page},
        )

    def get_blob(self, *, sha: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Blob:
        """Get a Git blob object by SHA.

        :param sha: Blob SHA.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Blob metadata and content.
        """
        return self._model("GET", self._client._repo_path("git", "blobs", sha, owner=owner, repo=repo), Blob)

    def get_raw(
        self,
        *,
        path: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        ref: Optional[str] = None,
    ) -> bytes:
        """Download raw file bytes from a repository.

        :param path: Repository-relative file path.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param ref: Optional branch, tag, or commit SHA.
        :returns: Raw file bytes.
        """
        return self._request(
            "GET",
            self._client._repo_file_path("raw", path, owner=owner, repo=repo),
            params={"ref": ref},
            raw=True,
        )


class BranchesResource(SyncResource):
    """Synchronous branch endpoints."""

    def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        sort: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Branch]:
        """List branches in a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param sort: Optional sort field such as ``name`` or ``updated``.
        :param direction: Sort direction, usually ``asc`` or ``desc``.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Repository branches.
        """
        return self._models(
            "GET",
            self._client._repo_path("branches", owner=owner, repo=repo),
            Branch,
            params={"sort": sort, "direction": direction, "page": page, "per_page": per_page},
        )

    def get(self, *, branch: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Branch:
        """Get a single branch.

        :param branch: Branch name.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Branch details.
        """
        return self._model("GET", self._client._repo_path("branches", branch, owner=owner, repo=repo), Branch)

    def create(self, *, branch: str, ref: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Branch:
        """Create a branch from an existing ref.

        :param branch: New branch name.
        :param ref: Starting ref such as a branch, tag, or commit SHA.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Created branch details.
        """
        return self._model(
            "POST",
            self._client._repo_path("branches", owner=owner, repo=repo),
            Branch,
            json={"branch_name": branch, "refs": ref},
        )

    def list_protected(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> List[ProtectedBranch]:
        """List protected branch rules for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Protected branch rules.
        """
        return self._models(
            "GET",
            self._client._repo_path("protect_branches", owner=owner, repo=repo),
            ProtectedBranch,
        )


class CommitsResource(SyncResource):
    """Synchronous commit endpoints."""

    def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        sha: Optional[str] = None,
        path: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Commit]:
        """List commits in a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param sha: Optional starting SHA or ref.
        :param path: Optional file path filter.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Matching commits.
        """
        return self._models(
            "GET",
            self._client._repo_path("commits", owner=owner, repo=repo),
            Commit,
            params={"sha": sha, "path": path, "page": page, "per_page": per_page},
        )

    def get(self, *, sha: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Commit:
        """Get a single commit.

        :param sha: Commit SHA or branch name accepted by the API.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Commit details.
        """
        return self._model("GET", self._client._repo_path("commits", sha, owner=owner, repo=repo), Commit)

    def compare(
        self, *, base: str, head: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> CommitComparison:
        """Compare two refs in a repository.

        :param base: Base commit SHA, branch, or tag.
        :param head: Head commit SHA, branch, or tag.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Commit comparison payload.
        """
        return self._model(
            "GET",
            self._client._repo_path("compare", f"{base}...{head}", owner=owner, repo=repo),
            CommitComparison,
        )

    def list_comments(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[CommitComment]:
        """List commit comments for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Commit comments.
        """
        return self._models(
            "GET",
            self._client._repo_path("comments", owner=owner, repo=repo),
            CommitComment,
            params={"page": page, "per_page": per_page},
        )

    def get_comment(
        self,
        *,
        comment_id: Union[int, str],
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> CommitComment:
        """Get a single commit comment.

        :param comment_id: Commit comment identifier.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Commit comment details.
        """
        return self._model(
            "GET", self._client._repo_path("comments", comment_id, owner=owner, repo=repo), CommitComment
        )

    def create_comment(
        self,
        *,
        sha: str,
        body: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        path: Optional[str] = None,
        position: Optional[int] = None,
    ) -> CommitComment:
        """Create a comment on a commit.

        :param sha: Commit SHA.
        :param body: Comment body.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param path: Optional file path associated with the comment.
        :param position: Optional diff position.
        :returns: Created commit comment.
        """
        return self._model(
            "POST",
            self._client._repo_path("commits", sha, "comments", owner=owner, repo=repo),
            CommitComment,
            json={"body": body, "path": path, "position": position},
        )

    def update_comment(
        self,
        *,
        comment_id: Union[int, str],
        body: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> CommitComment:
        """Update a commit comment.

        :param comment_id: Commit comment identifier.
        :param body: Updated comment body.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Updated commit comment.
        """
        return self._model(
            "PATCH",
            self._client._repo_path("comments", comment_id, owner=owner, repo=repo),
            CommitComment,
            json={"body": body},
        )

    def delete_comment(
        self, *, comment_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Delete a commit comment.

        :param comment_id: Commit comment identifier.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        """
        self._request("DELETE", self._client._repo_path("comments", comment_id, owner=owner, repo=repo))


class AsyncReposResource(AsyncResource):
    """Asynchronous repository endpoints."""

    async def get(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> Repository:
        return await self._model("GET", self._client._repo_path(owner=owner, repo=repo), Repository)

    async def list_user(self, **params: Any) -> List[Repository]:
        return await self._models("GET", self._client._path("user", "repos"), Repository, params=params)

    async def list_for_owner(self, *, owner: str, **params: Any) -> List[Repository]:
        return await self._models("GET", self._client._path("users", owner, "repos"), Repository, params=params)

    async def create_personal(self, *, name: str, **payload: Any) -> Repository:
        payload["name"] = name
        return await self._model("POST", self._client._path("user", "repos"), Repository, json=payload)

    async def create_for_org(self, *, org: str, name: str, **payload: Any) -> Repository:
        payload["name"] = name
        return await self._model("POST", self._client._path("orgs", org, "repos"), Repository, json=payload)

    async def update(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **changes: Any) -> Repository:
        return await self._model("PATCH", self._client._repo_path(owner=owner, repo=repo), Repository, json=changes)

    async def delete(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        await self._request("DELETE", self._client._repo_path(owner=owner, repo=repo))

    async def fork(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload: Any) -> Repository:
        return await self._model(
            "POST", self._client._repo_path("forks", owner=owner, repo=repo), Repository, json=payload
        )

    async def list_forks(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params: Any
    ) -> List[Repository]:
        return await self._models(
            "GET", self._client._repo_path("forks", owner=owner, repo=repo), Repository, params=params
        )

    async def list_contributors(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params: Any
    ) -> List[Contributor]:
        return await self._models(
            "GET",
            self._client._repo_path("contributors", owner=owner, repo=repo),
            Contributor,
            params=params,
        )

    async def list_languages(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> Dict[str, int]:
        return await self._request("GET", self._client._repo_path("languages", owner=owner, repo=repo))

    async def list_stargazers(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params: Any
    ) -> List[UserSummary]:
        return await self._models(
            "GET", self._client._repo_path("stargazers", owner=owner, repo=repo), UserSummary, params=params
        )

    async def list_subscribers(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params: Any
    ) -> List[UserSummary]:
        return await self._models(
            "GET",
            self._client._repo_path("subscribers", owner=owner, repo=repo),
            UserSummary,
            params=params,
        )

    async def update_module_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **settings: Any
    ) -> APIObject:
        return await self._model(
            "PUT", self._client._repo_path("module", "setting", owner=owner, repo=repo), APIObject, json=settings
        )

    async def update_reviewer_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **settings: Any
    ) -> APIObject:
        return await self._model(
            "PUT", self._client._repo_path("reviewer", owner=owner, repo=repo), APIObject, json=settings
        )

    async def set_org_repo_status(self, *, org: str, repo: str, **payload: Any) -> APIObject:
        return await self._model("PUT", self._client._path("org", org, "repo", repo, "status"), APIObject, json=payload)

    async def transfer_to_org(self, *, org: str, repo: str, **payload: Any) -> APIObject:
        return await self._model(
            "POST", self._client._path("org", org, "projects", repo, "transfer"), APIObject, json=payload
        )

    async def get_transition(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> APIObject:
        return await self._model("GET", self._client._repo_path("transition", owner=owner, repo=repo), APIObject)

    async def update_transition(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload: Any
    ) -> APIObject:
        return await self._model(
            "PUT", self._client._repo_path("transition", owner=owner, repo=repo), APIObject, json=payload
        )

    async def update_push_config(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload: Any
    ) -> APIObject:
        return await self._model(
            "PUT", self._client._repo_path("push_config", owner=owner, repo=repo), APIObject, json=payload
        )

    async def get_push_config(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> APIObject:
        return await self._model("GET", self._client._repo_path("push_config", owner=owner, repo=repo), APIObject)

    async def upload_image(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload: Any
    ) -> APIObject:
        return await self._model(
            "POST", self._client._repo_path("img", "upload", owner=owner, repo=repo), APIObject, json=payload
        )

    async def upload_file(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload: Any
    ) -> APIObject:
        return await self._model(
            "POST", self._client._repo_path("file", "upload", owner=owner, repo=repo), APIObject, json=payload
        )

    async def update_repo_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload: Any
    ) -> APIObject:
        return await self._model(
            "PUT", self._client._repo_path("repo_settings", owner=owner, repo=repo), APIObject, json=payload
        )

    async def get_repo_settings(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> APIObject:
        return await self._model("GET", self._client._repo_path("repo_settings", owner=owner, repo=repo), APIObject)

    async def get_pull_request_settings(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> APIObject:
        return await self._model(
            "GET", self._client._repo_path("pull_request_settings", owner=owner, repo=repo), APIObject
        )

    async def update_pull_request_settings(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload: Any
    ) -> APIObject:
        return await self._model(
            "PUT", self._client._repo_path("pull_request_settings", owner=owner, repo=repo), APIObject, json=payload
        )

    async def set_member_role(
        self,
        *,
        username: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        permission: Optional[str] = None,
    ) -> APIObject:
        return await self._model(
            "PUT",
            self._client._repo_path("members", username, owner=owner, repo=repo),
            APIObject,
            json={"permission": permission},
        )

    async def transfer(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **payload: Any) -> APIObject:
        return await self._model(
            "POST", self._client._repo_path("transfer", owner=owner, repo=repo), APIObject, json=payload
        )

    async def list_customized_roles(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[APIObject]:
        data = await self._request("GET", self._client._repo_path("customized_roles", owner=owner, repo=repo))
        return [as_model(item, APIObject) for item in data]

    async def get_download_statistics(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params: Any
    ) -> APIObject:
        return await self._model(
            "GET", self._client._repo_path("download_statistics", owner=owner, repo=repo), APIObject, params=params
        )

    async def get_contributor_statistics(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> APIObject:
        return await self._model(
            "GET", self._client._repo_path("contributors", "statistic", owner=owner, repo=repo), APIObject
        )

    async def list_events(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params: Any
    ) -> List[APIObject]:
        data = await self._request("GET", self._client._repo_path("events", owner=owner, repo=repo), params=params)
        return [as_model(item, APIObject) for item in data]


class AsyncRepoContentsResource(AsyncResource):
    """Asynchronous repository contents endpoints."""

    async def get(
        self, *, path: str, owner: Optional[str] = None, repo: Optional[str] = None, ref: Optional[str] = None
    ) -> ContentObject:
        return await self._model(
            "GET",
            self._client._repo_file_path("contents", path, owner=owner, repo=repo),
            ContentObject,
            params={"ref": ref},
        )

    async def create(
        self,
        *,
        path: str,
        content: str,
        message: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        branch: Optional[str] = None,
        author_name: Optional[str] = None,
        author_email: Optional[str] = None,
    ) -> CommitResult:
        return await self._model(
            "POST",
            self._client._repo_file_path("contents", path, owner=owner, repo=repo),
            CommitResult,
            json={
                "content": content,
                "message": message,
                "branch": branch,
                "author": {"name": author_name, "email": author_email},
            },
        )

    async def update(
        self,
        *,
        path: str,
        content: str,
        message: str,
        sha: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        branch: Optional[str] = None,
        author_name: Optional[str] = None,
        author_email: Optional[str] = None,
    ) -> CommitResult:
        return await self._model(
            "PUT",
            self._client._repo_file_path("contents", path, owner=owner, repo=repo),
            CommitResult,
            json={
                "content": content,
                "message": message,
                "sha": sha,
                "branch": branch,
                "author": {"name": author_name, "email": author_email},
            },
        )

    async def delete(
        self,
        *,
        path: str,
        message: str,
        sha: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        branch: Optional[str] = None,
        author_name: Optional[str] = None,
        author_email: Optional[str] = None,
    ) -> CommitResult:
        return await self._model(
            "DELETE",
            self._client._repo_file_path("contents", path, owner=owner, repo=repo),
            CommitResult,
            json={
                "message": message,
                "sha": sha,
                "branch": branch,
                "author": {"name": author_name, "email": author_email},
            },
        )

    async def list_paths(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        ref_name: Optional[str] = None,
        file_name: Optional[str] = None,
    ) -> List[str]:
        return await self._request(
            "GET",
            self._client._repo_path("file_list", owner=owner, repo=repo),
            params={"ref_name": ref_name, "file_name": file_name},
        )

    async def get_tree(
        self,
        *,
        sha: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        recursive: Optional[int] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> Tree:
        return await self._model(
            "GET",
            self._client._repo_path("git", "trees", sha, owner=owner, repo=repo),
            Tree,
            params={"recursive": recursive, "page": page, "per_page": per_page},
        )

    async def get_blob(self, *, sha: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Blob:
        return await self._model("GET", self._client._repo_path("git", "blobs", sha, owner=owner, repo=repo), Blob)

    async def get_raw(
        self, *, path: str, owner: Optional[str] = None, repo: Optional[str] = None, ref: Optional[str] = None
    ) -> bytes:
        return await self._request(
            "GET", self._client._repo_file_path("raw", path, owner=owner, repo=repo), params={"ref": ref}, raw=True
        )


class AsyncBranchesResource(AsyncResource):
    """Asynchronous branch endpoints."""

    async def list(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params: Any) -> List[Branch]:
        return await self._models(
            "GET", self._client._repo_path("branches", owner=owner, repo=repo), Branch, params=params
        )

    async def get(self, *, branch: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Branch:
        return await self._model("GET", self._client._repo_path("branches", branch, owner=owner, repo=repo), Branch)

    async def create(self, *, branch: str, ref: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Branch:
        return await self._model(
            "POST",
            self._client._repo_path("branches", owner=owner, repo=repo),
            Branch,
            json={"branch_name": branch, "refs": ref},
        )

    async def list_protected(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> List[ProtectedBranch]:
        return await self._models(
            "GET", self._client._repo_path("protect_branches", owner=owner, repo=repo), ProtectedBranch
        )


class AsyncCommitsResource(AsyncResource):
    """Asynchronous commit endpoints."""

    async def list(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params: Any) -> List[Commit]:
        return await self._models(
            "GET", self._client._repo_path("commits", owner=owner, repo=repo), Commit, params=params
        )

    async def get(self, *, sha: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Commit:
        return await self._model("GET", self._client._repo_path("commits", sha, owner=owner, repo=repo), Commit)

    async def compare(
        self, *, base: str, head: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> CommitComparison:
        return await self._model(
            "GET", self._client._repo_path("compare", f"{base}...{head}", owner=owner, repo=repo), CommitComparison
        )

    async def list_comments(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params: Any
    ) -> List[CommitComment]:
        return await self._models(
            "GET", self._client._repo_path("comments", owner=owner, repo=repo), CommitComment, params=params
        )

    async def get_comment(
        self, *, comment_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> CommitComment:
        return await self._model(
            "GET", self._client._repo_path("comments", comment_id, owner=owner, repo=repo), CommitComment
        )

    async def create_comment(
        self,
        *,
        sha: str,
        body: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        path: Optional[str] = None,
        position: Optional[int] = None,
    ) -> CommitComment:
        return await self._model(
            "POST",
            self._client._repo_path("commits", sha, "comments", owner=owner, repo=repo),
            CommitComment,
            json={"body": body, "path": path, "position": position},
        )

    async def update_comment(
        self, *, comment_id: Union[int, str], body: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> CommitComment:
        return await self._model(
            "PATCH",
            self._client._repo_path("comments", comment_id, owner=owner, repo=repo),
            CommitComment,
            json={"body": body},
        )

    async def delete_comment(
        self, *, comment_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        await self._request("DELETE", self._client._repo_path("comments", comment_id, owner=owner, repo=repo))
