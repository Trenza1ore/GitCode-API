"""PullsResource and AsyncPullsResource resource group."""

from typing import List, Optional, Union

from ..._models import (
    APIObject,
    Issue,
    Label,
    MergeResult,
    MergeStatus,
    PullRequest,
    PullRequestAssigneeCount,
    PullRequestComment,
    PullRequestCount,
    PullRequestFile,
    PullRequestOperationLog,
    RepositoryGitCodeTemplate,
    UserSummary,
    as_model,
)
from ...constants import GITCODE_PULL_REQUEST_TEMPLATE_PATH_RE
from .._shared import (
    AsyncResource,
    SyncResource,
    get_gitcode_template_body_async,
    get_gitcode_template_body_sync,
    list_gitcode_template_rows_async,
    list_gitcode_template_rows_sync,
)
from ._helpers import _comma_join


class PullsResource(SyncResource):
    """Synchronous pull request endpoints."""

    def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        state: Optional[str] = None,
        sort: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        **params,
    ) -> Union[List[PullRequest], PullRequestCount]:
        """List pull requests for a repository.

        When ``only_count`` is true in ``params`` (or passed via ``**params``), the API returns a
        JSON object with counts per state instead of an array (see Pull Request API).

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path (name). Uses the client default when omitted.
        :param state: PR state filter: ``all``, ``open``, ``closed``, ``locked``, ``merged`` (default ``all`` in API).
        :param sort: Sort field, typically ``created`` or ``updated``.
        :param direction: ``asc`` or ``desc`` (API default is usually ``desc``).
        :param page: Current page number.
        :param per_page: Page size (max 100 per API documentation).
        :param params: Extra query parameters from the Pull Request API, for example ``base``,
            ``since``, ``author``, ``assignee``, ``reviewer``, ``milestone_number``, ``labels`` (comma-separated),
            ``merged_after``, ``merged_before``, ``created_after``, ``created_before``, ``updated_after``,
            ``updated_before``, ``only_count`` (boolean), and ISO 8601 timestamps (URL-encoded when sent).
        :returns: A list of pull requests, or an :class:`~gitcode_api._models.APIObject` for count-only responses.
        """
        path = self._client._repo_path("pulls", owner=owner, repo=repo)
        response = self._request(
            "GET",
            path,
            params={
                "state": state,
                "sort": sort,
                "direction": direction,
                "page": page,
                "per_page": per_page,
                **params,
            },
        )
        if isinstance(response, dict):
            return as_model(response, PullRequestCount)
        return [as_model(item, PullRequest) for item in response]

    def get(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> PullRequest:
        """Get a single pull request.

        :param number: Pull request number in the repository.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Pull request details.
        """
        return self._model("GET", self._client._repo_path("pulls", number, owner=owner, repo=repo), PullRequest)

    def create(
        self,
        *,
        title: str,
        head: str,
        base: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        body: Optional[str] = None,
        draft: Optional[bool] = None,
        assignees: Optional[List[str]] = None,
        testers: Optional[List[str]] = None,
        labels: Optional[List[str]] = None,
        milestone_number: Optional[int] = None,
        issue: Optional[str] = None,
        prune_source_branch: Optional[bool] = None,
        squash: Optional[bool] = None,
        squash_commit_message: Optional[str] = None,
        fork_path: Optional[str] = None,
    ) -> PullRequest:
        """Create a pull request.

        :param title: Pull request title.
        :param head: Source branch ref (head branch, in forks use ``owner:branch`` like "SushiNinja:develop").
        :param base: Target branch ref (base branch).
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param body: Description body.
        :param draft: Whether to create as draft.
        :param assignees: Assignee logins; sent as a comma-separated string per API.
        :param testers: Tester logins; comma-separated in the JSON body.
        :param labels: Label names; comma-separated in the JSON body.
        :param milestone_number: Target milestone number.
        :param issue: Related issue reference when supported by the API.
        :param prune_source_branch: Whether to delete the source branch after merge when applicable.
        :param squash: Squash-merge preference where supported.
        :param squash_commit_message: Custom squash commit message.
        :param fork_path: Fork ``owner/repo`` when opening a PR from a fork, like "SushiNinja/agent-core-contrib".
        :returns: Created pull request.
        """
        return self._model(
            "POST",
            self._client._repo_path("pulls", owner=owner, repo=repo),
            PullRequest,
            json={
                "title": title,
                "head": head,
                "base": base,
                "body": body,
                "draft": draft,
                "assignees": _comma_join(assignees),
                "testers": _comma_join(testers),
                "labels": _comma_join(labels),
                "milestone_number": milestone_number,
                "issue": issue,
                "prune_source_branch": prune_source_branch,
                "squash": squash,
                "squash_commit_message": squash_commit_message,
                "fork_path": fork_path,
            },
        )

    def update(
        self,
        *,
        number: Union[int, str],
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        base: Optional[str] = None,
        labels: Optional[List[str]] = None,
        draft: Optional[bool] = None,
    ) -> PullRequest:
        """Update a pull request.

        :param number: Pull request number in the repository.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param title: New title.
        :param body: New description.
        :param state: New state as accepted by the API (for example close or reopen semantics).
        :param base: New base branch name.
        :param labels: Replacement labels; comma-separated in the JSON body.
        :param draft: Draft flag.
        :returns: Updated pull request.
        """
        return self._model(
            "PATCH",
            self._client._repo_path("pulls", number, owner=owner, repo=repo),
            PullRequest,
            json={
                "title": title,
                "body": body,
                "state": state,
                "base": base,
                "labels": _comma_join(labels),
                "draft": draft,
            },
        )

    def merge(
        self,
        *,
        number: Union[int, str],
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        merge_commit_message: Optional[str] = None,
        squash: Optional[bool] = None,
    ) -> MergeResult:
        """Merge a pull request.

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param merge_commit_message: Optional merge commit message.
        :param squash: Whether to squash merge when supported.
        :returns: Merge result payload.
        """
        return self._model(
            "PUT",
            self._client._repo_path("pulls", number, "merge", owner=owner, repo=repo),
            MergeResult,
            json={"merge_commit_message": merge_commit_message, "squash": squash},
        )

    def get_merge_status(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> MergeStatus:
        """Get mergeability status for a pull request (GET on the merge resource).

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Merge status / mergeability information.
        """
        return self._model(
            "GET",
            self._client._repo_path("pulls", number, "merge", owner=owner, repo=repo),
            MergeStatus,
        )

    def list_commits(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[APIObject]:
        """List commits included in a pull request.

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Commit objects (wrapped as :class:`~gitcode_api._models.APIObject`).
        """
        data = self._request("GET", self._client._repo_path("pulls", number, "commits", owner=owner, repo=repo))
        return [as_model(item, APIObject) for item in data]

    def list_files(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[PullRequestFile]:
        """List files changed by a pull request.

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: File change entries.
        """
        return self._models(
            "GET",
            self._client._repo_path("pulls", number, "files", owner=owner, repo=repo),
            PullRequestFile,
        )

    def list_comments(
        self,
        *,
        number: Union[int, str],
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[PullRequestComment]:
        """List comments on a pull request.

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Pull request review comments.
        """
        return self._models(
            "GET",
            self._client._repo_path("pulls", number, "comments", owner=owner, repo=repo),
            PullRequestComment,
            params={"page": page, "per_page": per_page},
        )

    def create_comment(
        self,
        *,
        number: Union[int, str],
        body: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        commit_id: Optional[str] = None,
        path: Optional[str] = None,
        position: Optional[int] = None,
    ) -> PullRequestComment:
        """Create a pull request (review) comment.

        :param number: Pull request number.
        :param body: Comment body.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param commit_id: Commit SHA the comment applies to.
        :param path: File path in the diff.
        :param position: Line or diff position as defined by the API.
        :returns: Created comment.
        """
        return self._model(
            "POST",
            self._client._repo_path("pulls", number, "comments", owner=owner, repo=repo),
            PullRequestComment,
            json={"body": body, "commit_id": commit_id, "path": path, "position": position},
        )

    def get_comment(
        self,
        *,
        comment_id: Union[int, str],
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> PullRequestComment:
        """Get a single pull request comment by id (global comment endpoint).

        :param comment_id: Comment id.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Pull request comment.
        """
        return self._model(
            "GET",
            self._client._repo_path("pulls", "comments", comment_id, owner=owner, repo=repo),
            PullRequestComment,
        )

    def update_comment(
        self,
        *,
        comment_id: Union[int, str],
        body: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> PullRequestComment:
        """Update a pull request comment.

        :param comment_id: Comment id.
        :param body: Updated body.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Updated comment.
        """
        return self._model(
            "PATCH",
            self._client._repo_path("pulls", "comments", comment_id, owner=owner, repo=repo),
            PullRequestComment,
            json={"body": body},
        )

    def delete_comment(
        self, *, comment_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Delete a pull request comment.

        :param comment_id: Comment id.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        self._request("DELETE", self._client._repo_path("pulls", "comments", comment_id, owner=owner, repo=repo))

    def list_labels(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Label]:
        """List labels attached to a pull request.

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Labels on the pull request.
        """
        return self._models(
            "GET",
            self._client._repo_path("pulls", number, "labels", owner=owner, repo=repo),
            Label,
        )

    def add_labels(
        self, *, number: Union[int, str], labels: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Label]:
        """Add labels to a pull request.

        :param number: Pull request number.
        :param labels: Label names (JSON array body per API).
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Labels after the operation.
        """
        return self._models(
            "POST",
            self._client._repo_path("pulls", number, "labels", owner=owner, repo=repo),
            Label,
            json=labels,
        )

    def replace_labels(
        self, *, number: Union[int, str], labels: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Label]:
        """Replace all labels on a pull request.

        :param number: Pull request number.
        :param labels: Complete new label set (JSON array body).
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Labels after replacement.
        """
        return self._models(
            "PUT",
            self._client._repo_path("pulls", number, "labels", owner=owner, repo=repo),
            Label,
            json=labels,
        )

    def remove_label(
        self, *, number: Union[int, str], label: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Remove a label from a pull request.

        :param number: Pull request number.
        :param label: Label name to remove.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        self._request("DELETE", self._client._repo_path("pulls", number, "labels", label, owner=owner, repo=repo))

    def request_review(
        self,
        *,
        number: Union[int, str],
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        event: str,
        body: Optional[str] = None,
    ) -> None:
        """Submit a pull request review event (approve, request changes, etc., per API).

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param event: Review event name as required by GitCode (for example ``APPROVE``; see API docs).
        :param body: Optional comment body accompanying the event.
        :returns: Review result object.
        """
        self._request(
            "POST",
            self._client._repo_path("pulls", number, "review", owner=owner, repo=repo),
            json={"event": event, "body": body},
        )

    def list_operation_logs(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None, **params
    ) -> List[PullRequestOperationLog]:
        """List operation logs for a pull request.

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param params: Additional query parameters accepted by the operate_logs endpoint.
        :returns: Log entries as generic API objects.
        """
        data = self._request(
            "GET",
            self._client._repo_path("pulls", number, "operate_logs", owner=owner, repo=repo),
            params=params,
        )
        return [as_model(item, PullRequestOperationLog) for item in data]

    def request_test(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None, **payload
    ) -> None:
        """Request testing for a pull request.

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param payload: JSON fields required by the test request endpoint.
        :returns: Test request result.
        """
        self._request(
            "POST",
            self._client._repo_path("pulls", number, "test", owner=owner, repo=repo),
            json=payload,
        )

    def update_testers(
        self, *, number: Union[int, str], testers: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Replace pull request testers.

        :param number: Pull request number.
        :param testers: New tester list; serialized as a comma-separated ``testers`` field in JSON.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: API response payload.
        """
        self._request(
            "PATCH",
            self._client._repo_path("pulls", number, "testers", owner=owner, repo=repo),
            json={"testers": _comma_join(testers)},
        )

    def add_testers(
        self, *, number: Union[int, str], testers: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[UserSummary]:
        """Add testers to a pull request.

        :param number: Pull request number.
        :param testers: Usernames to add; comma-separated in the JSON body.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: API response payload.
        """
        data = self._request(
            "POST",
            self._client._repo_path("pulls", number, "testers", owner=owner, repo=repo),
            json={"testers": _comma_join(testers)},
        )
        return [as_model(item, UserSummary) for item in data]

    def update_assignees(
        self, *, number: Union[int, str], assignees: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Replace pull request assignees.

        :param number: Pull request number.
        :param assignees: New assignee list; comma-separated in the JSON body.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: API response payload.
        """
        self._request(
            "PATCH",
            self._client._repo_path("pulls", number, "assignees", owner=owner, repo=repo),
            json={"assignees": _comma_join(assignees)},
        )

    def add_assignees(
        self, *, number: Union[int, str], assignees: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> PullRequestAssigneeCount:
        """Add assignees to a pull request.

        :param number: Pull request number.
        :param assignees: Usernames to add; comma-separated in the JSON body.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: API response payload.
        """
        return self._model(
            "POST",
            self._client._repo_path("pulls", number, "assignees", owner=owner, repo=repo),
            PullRequestAssigneeCount,
            json={"assignees": _comma_join(assignees)},
        )

    def remove_assignees(
        self, *, number: Union[int, str], assignees: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Remove assignees from a pull request.

        :param number: Pull request number.
        :param assignees: Usernames to remove; comma-separated in the JSON body.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        self._request(
            "DELETE",
            self._client._repo_path("pulls", number, "assignees", owner=owner, repo=repo),
            json={"assignees": _comma_join(assignees)},
        )

    def list_issues(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Issue]:
        """List issues linked to a pull request.

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Linked issues.
        """
        return self._models("GET", self._client._repo_path("pulls", number, "issues", owner=owner, repo=repo), Issue)

    def list_enterprise(self, *, enterprise: str, **params) -> List[PullRequest]:
        """List enterprise pull requests.

        :param enterprise: Enterprise path or login.
        :param params: Query parameters for the enterprise pull_requests listing.
        :returns: Pull requests in the enterprise scope.
        """
        return self._models(
            "GET", self._client._path("enterprises", enterprise, "pull_requests"), PullRequest, params=params
        )

    def list_org(self, *, org: str, **params) -> List[PullRequest]:
        """List pull requests for an organization scope.

        :param org: Organization path (``GET .../org/{org}/pull_requests``).
        :param params: Query parameters accepted by that listing.
        :returns: Organization-scoped pull requests.
        """
        return self._models("GET", self._client._path("org", org, "pull_requests"), PullRequest, params=params)

    def list_issue_pull_requests(self, *, enterprise: str, number: Union[int, str]) -> List[PullRequest]:
        """List pull requests associated with an enterprise issue.

        :param enterprise: Enterprise path or login.
        :param number: Enterprise issue number or id in the path.
        :returns: Related pull requests.
        """
        return self._models(
            "GET",
            self._client._path("enterprises", enterprise, "issues", number, "pull_requests"),
            PullRequest,
        )

    def list_templates(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> List[RepositoryGitCodeTemplate]:
        """List active pull request templates under ``.gitcode/`` for this repository.

        Resolution tries the repository, then the owner's ``.gitcode`` repository, then any
        parent main and ``parent/.gitcode`` pairs discovered from forks (each candidate is
        inspected with ``GET /repos/{owner}/{repo}``; when ``fork`` is true, its parent's repos
        are appended, deduplicated, and visited in order). The first source with matching
        templates wins.

        Version 1.2.19: Now also supporting GitHub-mirrored repos with a ``.github/`` folder.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Template metadata entries (paths and SHAs); empty when none match.
        """
        resolved_owner, resolved_repo = self._client._resolve_repo_context(owner, repo)
        rows = list_gitcode_template_rows_sync(
            self._client, resolved_owner, resolved_repo, GITCODE_PULL_REQUEST_TEMPLATE_PATH_RE
        )
        return [
            as_model(
                {
                    "path": path,
                    "sha": sha,
                    "template_owner": template_owner,
                    "template_repo": template_repo,
                },
                RepositoryGitCodeTemplate,
            )
            for template_owner, template_repo, path, sha in rows
        ]

    def get_template(
        self,
        *,
        path: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        encoding: str = "utf-8",
        **decoding_kwargs,
    ) -> str:
        """Load a single pull request template file body from the default branch.

        Uses the same resolution order as :meth:`list_templates`. The path must match the
        active pull request template naming convention (see GitCode ``.gitcode`` documentation).

        :param path: Repository-relative path such as ``.gitcode/PULL_REQUEST_TEMPLATE.md``.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param encoding: Codec to use when decoding raw file bytes. Default ``utf-8``.
        :param decoding_kwargs: Keyword arguments forwarded to :meth:`bytes.decode`, such as
            ``errors`` (``"strict"``, ``"ignore"``, or ``"replace"``).
        :returns: Decoded template file contents.
        """
        resolved_owner, resolved_repo = self._client._resolve_repo_context(owner, repo)
        return get_gitcode_template_body_sync(
            self._client,
            path,
            GITCODE_PULL_REQUEST_TEMPLATE_PATH_RE,
            resolved_owner,
            resolved_repo,
            encoding=encoding,
            **decoding_kwargs,
        )


class AsyncPullsResource(AsyncResource):
    """Asynchronous pull request endpoints.

    Methods correspond to :class:`PullsResource` with identical arguments and semantics,
    including ``only_count`` responses documented in the Pull Request API under ``docs/rest_api``.
    """

    async def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        state: Optional[str] = None,
        sort: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        **params,
    ) -> Union[List[PullRequest], PullRequestCount]:
        """List pull requests for a repository.

        When ``only_count`` is true in ``params`` (or passed via ``**params``), the API returns a
        JSON object with counts per state instead of an array (see Pull Request API).

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path (name). Uses the client default when omitted.
        :param state: PR state filter: ``all``, ``open``, ``closed``, ``locked``, ``merged`` (default ``all`` in API).
        :param sort: Sort field, typically ``created`` or ``updated``.
        :param direction: ``asc`` or ``desc`` (API default is usually ``desc``).
        :param page: Current page number.
        :param per_page: Page size (max 100 per API documentation).
        :param params: Extra query parameters from the Pull Request API, for example ``base``,
            ``since``, ``author``, ``assignee``, ``reviewer``, ``milestone_number``, ``labels`` (comma-separated),
            ``merged_after``, ``merged_before``, ``created_after``, ``created_before``, ``updated_after``,
            ``updated_before``, ``only_count`` (boolean), and ISO 8601 timestamps (URL-encoded when sent).
        :returns: A list of pull requests, or an :class:`~gitcode_api._models.APIObject` for count-only responses.
        """
        response = await self._request(
            "GET",
            self._client._repo_path("pulls", owner=owner, repo=repo),
            params={
                "state": state,
                "sort": sort,
                "direction": direction,
                "page": page,
                "per_page": per_page,
                **params,
            },
        )
        if isinstance(response, dict):
            return as_model(response, PullRequestCount)
        return [as_model(item, PullRequest) for item in response]

    async def get(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> PullRequest:
        """Get a single pull request.

        :param number: Pull request number in the repository.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Pull request details.
        """
        return await self._model("GET", self._client._repo_path("pulls", number, owner=owner, repo=repo), PullRequest)

    async def create(
        self,
        *,
        title: str,
        head: str,
        base: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        body: Optional[str] = None,
        draft: Optional[bool] = None,
        assignees: Optional[List[str]] = None,
        testers: Optional[List[str]] = None,
        labels: Optional[List[str]] = None,
        milestone_number: Optional[int] = None,
        issue: Optional[str] = None,
        prune_source_branch: Optional[bool] = None,
        squash: Optional[bool] = None,
        squash_commit_message: Optional[str] = None,
        fork_path: Optional[str] = None,
    ) -> PullRequest:
        """Create a pull request.

        :param title: Pull request title.
        :param head: Source branch ref (head branch, in forks use ``owner:branch`` like "SushiNinja:develop").
        :param base: Target branch ref (base branch).
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param body: Description body.
        :param draft: Whether to create as draft.
        :param assignees: Assignee logins; sent as a comma-separated string per API.
        :param testers: Tester logins; comma-separated in the JSON body.
        :param labels: Label names; comma-separated in the JSON body.
        :param milestone_number: Target milestone number.
        :param issue: Related issue reference when supported by the API.
        :param prune_source_branch: Whether to delete the source branch after merge when applicable.
        :param squash: Squash-merge preference where supported.
        :param squash_commit_message: Custom squash commit message.
        :param fork_path: Fork ``owner/repo`` when opening a PR from a fork, like "SushiNinja/agent-core-contrib".
        :returns: Created pull request.
        """
        return await self._model(
            "POST",
            self._client._repo_path("pulls", owner=owner, repo=repo),
            PullRequest,
            json={
                "title": title,
                "head": head,
                "base": base,
                "body": body,
                "draft": draft,
                "assignees": _comma_join(assignees),
                "testers": _comma_join(testers),
                "labels": _comma_join(labels),
                "milestone_number": milestone_number,
                "issue": issue,
                "prune_source_branch": prune_source_branch,
                "squash": squash,
                "squash_commit_message": squash_commit_message,
                "fork_path": fork_path,
            },
        )

    async def update(
        self,
        *,
        number: Union[int, str],
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        base: Optional[str] = None,
        labels: Optional[List[str]] = None,
        draft: Optional[bool] = None,
    ) -> PullRequest:
        """Update a pull request.

        :param number: Pull request number in the repository.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param title: New title.
        :param body: New description.
        :param state: New state as accepted by the API.
        :param base: New base branch name.
        :param labels: Replacement labels; comma-separated in the JSON body.
        :param draft: Draft flag.
        :returns: Updated pull request.
        """
        return await self._model(
            "PATCH",
            self._client._repo_path("pulls", number, owner=owner, repo=repo),
            PullRequest,
            json={
                "title": title,
                "body": body,
                "state": state,
                "base": base,
                "labels": _comma_join(labels),
                "draft": draft,
            },
        )

    async def merge(
        self,
        *,
        number: Union[int, str],
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        merge_commit_message: Optional[str] = None,
        squash: Optional[bool] = None,
    ) -> MergeResult:
        """Merge a pull request.

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param merge_commit_message: Optional merge commit message.
        :param squash: Whether to squash merge when supported.
        :returns: Merge result payload.
        """
        return await self._model(
            "PUT",
            self._client._repo_path("pulls", number, "merge", owner=owner, repo=repo),
            MergeResult,
            json={"merge_commit_message": merge_commit_message, "squash": squash},
        )

    async def get_merge_status(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> MergeStatus:
        """Get mergeability status for a pull request (GET on the merge resource).

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Merge status / mergeability information.
        """
        return await self._model(
            "GET", self._client._repo_path("pulls", number, "merge", owner=owner, repo=repo), MergeStatus
        )

    async def list_commits(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[APIObject]:
        """List commits included in a pull request.

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Commit objects (wrapped as :class:`~gitcode_api._models.APIObject`).
        """
        data = await self._request("GET", self._client._repo_path("pulls", number, "commits", owner=owner, repo=repo))
        return [as_model(item, APIObject) for item in data]

    async def list_files(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[PullRequestFile]:
        """List files changed by a pull request.

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: File change entries.
        """
        return await self._models(
            "GET", self._client._repo_path("pulls", number, "files", owner=owner, repo=repo), PullRequestFile
        )

    async def list_comments(
        self,
        *,
        number: Union[int, str],
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[PullRequestComment]:
        """List comments on a pull request.

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Pull request review comments.
        """
        return await self._models(
            "GET",
            self._client._repo_path("pulls", number, "comments", owner=owner, repo=repo),
            PullRequestComment,
            params={"page": page, "per_page": per_page},
        )

    async def create_comment(
        self,
        *,
        number: Union[int, str],
        body: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        commit_id: Optional[str] = None,
        path: Optional[str] = None,
        position: Optional[int] = None,
    ) -> PullRequestComment:
        """Create a pull request (review) comment.

        :param number: Pull request number.
        :param body: Comment body.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param commit_id: Commit SHA the comment applies to.
        :param path: File path in the diff.
        :param position: Line or diff position as defined by the API.
        :returns: Created comment.
        """
        return await self._model(
            "POST",
            self._client._repo_path("pulls", number, "comments", owner=owner, repo=repo),
            PullRequestComment,
            json={"body": body, "commit_id": commit_id, "path": path, "position": position},
        )

    async def get_comment(
        self, *, comment_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> PullRequestComment:
        """Get a single pull request comment by id (global comment endpoint).

        :param comment_id: Comment id.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Pull request comment.
        """
        return await self._model(
            "GET", self._client._repo_path("pulls", "comments", comment_id, owner=owner, repo=repo), PullRequestComment
        )

    async def update_comment(
        self, *, comment_id: Union[int, str], body: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> PullRequestComment:
        """Update a pull request comment.

        :param comment_id: Comment id.
        :param body: Updated body.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Updated comment.
        """
        return await self._model(
            "PATCH",
            self._client._repo_path("pulls", "comments", comment_id, owner=owner, repo=repo),
            PullRequestComment,
            json={"body": body},
        )

    async def delete_comment(
        self, *, comment_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Delete a pull request comment.

        :param comment_id: Comment id.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        await self._request("DELETE", self._client._repo_path("pulls", "comments", comment_id, owner=owner, repo=repo))

    async def list_labels(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Label]:
        """List labels attached to a pull request.

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Labels on the pull request.
        """
        return await self._models(
            "GET", self._client._repo_path("pulls", number, "labels", owner=owner, repo=repo), Label
        )

    async def add_labels(
        self, *, number: Union[int, str], labels: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Label]:
        """Add labels to a pull request.

        :param number: Pull request number.
        :param labels: Label names (JSON array body per API).
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Labels after the operation.
        """
        return await self._models(
            "POST", self._client._repo_path("pulls", number, "labels", owner=owner, repo=repo), Label, json=labels
        )

    async def replace_labels(
        self, *, number: Union[int, str], labels: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Label]:
        """Replace all labels on a pull request.

        :param number: Pull request number.
        :param labels: Complete new label set (JSON array body).
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Labels after replacement.
        """
        return await self._models(
            "PUT", self._client._repo_path("pulls", number, "labels", owner=owner, repo=repo), Label, json=labels
        )

    async def remove_label(
        self, *, number: Union[int, str], label: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Remove a label from a pull request.

        :param number: Pull request number.
        :param label: Label name to remove.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        await self._request("DELETE", self._client._repo_path("pulls", number, "labels", label, owner=owner, repo=repo))

    async def request_review(
        self,
        *,
        number: Union[int, str],
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        event: str,
        body: Optional[str] = None,
    ) -> None:
        """Submit a pull request review event (approve, request changes, etc., per API).

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param event: Review event name as required by GitCode (see API docs).
        :param body: Optional comment body accompanying the event.
        :returns: Review result object.
        """
        await self._request(
            "POST",
            self._client._repo_path("pulls", number, "review", owner=owner, repo=repo),
            json={"event": event, "body": body},
        )

    async def list_operation_logs(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None, **params
    ) -> List[PullRequestOperationLog]:
        """List operation logs for a pull request.

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param params: Additional query parameters accepted by the operate_logs endpoint.
        :returns: Log entries as generic API objects.
        """
        data = await self._request(
            "GET", self._client._repo_path("pulls", number, "operate_logs", owner=owner, repo=repo), params=params
        )
        return [as_model(item, PullRequestOperationLog) for item in data]

    async def request_test(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None, **payload
    ) -> None:
        """Request testing for a pull request.

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param payload: JSON fields required by the test request endpoint.
        :returns: Test request result.
        """
        await self._request(
            "POST",
            self._client._repo_path("pulls", number, "test", owner=owner, repo=repo),
            json=payload,
        )

    async def update_testers(
        self, *, number: Union[int, str], testers: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Replace pull request testers.

        :param number: Pull request number.
        :param testers: New tester list; serialized as a comma-separated ``testers`` field in JSON.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: API response payload.
        """
        await self._request(
            "PATCH",
            self._client._repo_path("pulls", number, "testers", owner=owner, repo=repo),
            json={"testers": _comma_join(testers)},
        )

    async def add_testers(
        self, *, number: Union[int, str], testers: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[UserSummary]:
        """Add testers to a pull request.

        :param number: Pull request number.
        :param testers: Usernames to add; comma-separated in the JSON body.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: API response payload.
        """
        data = await self._request(
            "POST",
            self._client._repo_path("pulls", number, "testers", owner=owner, repo=repo),
            json={"testers": _comma_join(testers)},
        )
        return [as_model(item, UserSummary) for item in data]

    async def update_assignees(
        self, *, number: Union[int, str], assignees: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Replace pull request assignees.

        :param number: Pull request number.
        :param assignees: New assignee list; comma-separated in the JSON body.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: API response payload.
        """
        await self._request(
            "PATCH",
            self._client._repo_path("pulls", number, "assignees", owner=owner, repo=repo),
            json={"assignees": _comma_join(assignees)},
        )

    async def add_assignees(
        self, *, number: Union[int, str], assignees: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> PullRequestAssigneeCount:
        """Add assignees to a pull request.

        :param number: Pull request number.
        :param assignees: Usernames to add; comma-separated in the JSON body.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: API response payload.
        """
        return await self._model(
            "POST",
            self._client._repo_path("pulls", number, "assignees", owner=owner, repo=repo),
            PullRequestAssigneeCount,
            json={"assignees": _comma_join(assignees)},
        )

    async def remove_assignees(
        self, *, number: Union[int, str], assignees: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Remove assignees from a pull request.

        :param number: Pull request number.
        :param assignees: Usernames to remove; comma-separated in the JSON body.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        await self._request(
            "DELETE",
            self._client._repo_path("pulls", number, "assignees", owner=owner, repo=repo),
            json={"assignees": _comma_join(assignees)},
        )

    async def list_issues(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Issue]:
        """List issues linked to a pull request.

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Linked issues.
        """
        return await self._models(
            "GET", self._client._repo_path("pulls", number, "issues", owner=owner, repo=repo), Issue
        )

    async def list_enterprise(self, *, enterprise: str, **params) -> List[PullRequest]:
        """List enterprise pull requests.

        :param enterprise: Enterprise path or login.
        :param params: Query parameters for the enterprise pull_requests listing.
        :returns: Pull requests in the enterprise scope.
        """
        return await self._models(
            "GET", self._client._path("enterprises", enterprise, "pull_requests"), PullRequest, params=params
        )

    async def list_org(self, *, org: str, **params) -> List[PullRequest]:
        """List pull requests for an organization scope.

        :param org: Organization path (``GET .../org/{org}/pull_requests``).
        :param params: Query parameters accepted by that listing.
        :returns: Organization-scoped pull requests.
        """
        return await self._models("GET", self._client._path("org", org, "pull_requests"), PullRequest, params=params)

    async def list_issue_pull_requests(self, *, enterprise: str, number: Union[int, str]) -> List[PullRequest]:
        """List pull requests associated with an enterprise issue.

        :param enterprise: Enterprise path or login.
        :param number: Enterprise issue number or id in the path.
        :returns: Related pull requests.
        """
        return await self._models(
            "GET", self._client._path("enterprises", enterprise, "issues", number, "pull_requests"), PullRequest
        )

    async def list_templates(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> List[RepositoryGitCodeTemplate]:
        """List active pull request templates under ``.gitcode/`` for this repository.

        Resolution tries the repository, then the owner's ``.gitcode`` repository, then any
        parent main and ``parent/.gitcode`` pairs discovered from forks (each candidate is
        inspected with ``GET /repos/{owner}/{repo}``; when ``fork`` is true, its parent's repos
        are appended, deduplicated, and visited in order). The first source with matching
        templates wins.

        Version 1.2.19: Now also supporting GitHub-mirrored repos with a ``.github/`` folder.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Template metadata entries (paths and SHAs); empty when none match.
        """
        resolved_owner, resolved_repo = self._client._resolve_repo_context(owner, repo)
        rows = await list_gitcode_template_rows_async(
            self._client, resolved_owner, resolved_repo, GITCODE_PULL_REQUEST_TEMPLATE_PATH_RE
        )
        return [
            as_model(
                {
                    "path": path,
                    "sha": sha,
                    "template_owner": template_owner,
                    "template_repo": template_repo,
                },
                RepositoryGitCodeTemplate,
            )
            for template_owner, template_repo, path, sha in rows
        ]

    async def get_template(
        self,
        *,
        path: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        encoding: str = "utf-8",
        **decoding_kwargs,
    ) -> str:
        """Load a single pull request template file body from the default branch.

        Uses the same resolution order as :meth:`list_templates`. The path must match the
        active pull request template naming convention (see GitCode ``.gitcode`` documentation).

        :param path: Repository-relative path such as ``.gitcode/PULL_REQUEST_TEMPLATE.md``.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param encoding: Codec to use when decoding raw file bytes. Default ``utf-8``.
        :param decoding_kwargs: Keyword arguments forwarded to :meth:`bytes.decode`, such as
            ``errors`` (``"strict"``, ``"ignore"``, or ``"replace"``).
        :returns: Decoded template file contents.
        """
        resolved_owner, resolved_repo = self._client._resolve_repo_context(owner, repo)
        return await get_gitcode_template_body_async(
            self._client,
            path,
            GITCODE_PULL_REQUEST_TEMPLATE_PATH_RE,
            resolved_owner,
            resolved_repo,
            encoding=encoding,
            **decoding_kwargs,
        )
