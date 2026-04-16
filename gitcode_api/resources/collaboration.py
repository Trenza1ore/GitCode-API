"""Issue, pull request, label, milestone, and member resource groups."""

from typing import List, Optional, Union

from .._models import (
    APIObject,
    Issue,
    IssueComment,
    IssueOperationLog,
    Label,
    MergeResult,
    MergeStatus,
    Milestone,
    PullRequest,
    PullRequestAssigneeCount,
    PullRequestComment,
    PullRequestCount,
    PullRequestFile,
    PullRequestOperationLog,
    RepoCollaborator,
    RepoMember,
    RepoMemberPermission,
    RepositoryCollaboratorCheck,
    UserSummary,
    as_model,
)
from ._shared import AsyncResource, SyncResource


def _comma_join(values: Optional[List[str]]) -> Optional[str]:
    """Join a list of strings into the comma-separated format used by the API."""
    if not values:
        return None
    return ",".join(values)


class IssuesResource(SyncResource):
    """Synchronous issue endpoints."""

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
    ) -> List[Issue]:
        """List issues for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param state: Issue state filter such as ``open`` or ``closed`` (see Issues API).
        :param sort: Optional sort field.
        :param direction: Optional sort direction.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Matching issues.
        """
        return self._models(
            "GET",
            self._client._repo_path("issues", owner=owner, repo=repo),
            Issue,
            params={
                "state": state,
                "sort": sort,
                "direction": direction,
                "page": page,
                "per_page": per_page,
            },
        )

    def get(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> Issue:
        """Get a single issue by number.

        :param number: Repository-local issue number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Issue details.
        """
        return self._model("GET", self._client._repo_path("issues", number, owner=owner, repo=repo), Issue)

    def create(
        self,
        *,
        owner: str,
        repo: Optional[str] = None,
        title: str,
        body: Optional[str] = None,
        assignee: Optional[str] = None,
        labels: Optional[List[str]] = None,
        milestone: Union[int, str, None] = None,
        security_hole: Optional[str] = None,
    ) -> Issue:
        """Create an issue for a repository.

        :param owner: Repository owner path.
        :param repo: Repository name. Uses the client default when omitted.
        :param title: Issue title.
        :param body: Optional issue description.
        :param assignee: Optional assignee username.
        :param labels: Optional label names.
        :param milestone: Optional milestone identifier.
        :param security_hole: Whether the issue is private; form field described in the Issues API (default public).
        :returns: Created issue details.
        """
        resolved_repo = repo or self._client.repo
        return self._model(
            "POST",
            self._client._path("repos", owner, "issues"),
            Issue,
            json={
                "repo": resolved_repo,
                "title": title,
                "body": body,
                "assignee": assignee,
                "labels": _comma_join(labels),
                "milestone": milestone,
                "security_hole": security_hole,
            },
        )

    def update(
        self,
        *,
        number: Union[int, str],
        owner: str,
        repo: Optional[str] = None,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        assignee: Optional[str] = None,
        labels: Optional[List[str]] = None,
        milestone: Union[int, str, None] = None,
        security_hole: Optional[str] = None,
    ) -> Issue:
        """Update an existing issue.

        :param number: Repository-local issue number.
        :param owner: Repository owner path.
        :param repo: Repository name. Uses the client default when omitted.
        :param title: Updated issue title.
        :param body: Updated issue description.
        :param state: Updated state such as ``reopen`` or ``close``.
        :param assignee: Updated assignee username.
        :param labels: Replacement label names.
        :param milestone: Updated milestone identifier.
        :param security_hole: Whether the issue is private; form field described in the Issues API.
        :returns: Updated issue details.
        """
        resolved_repo = repo or self._client.repo
        return self._model(
            "PATCH",
            self._client._path("repos", owner, "issues", number),
            Issue,
            json={
                "repo": resolved_repo,
                "title": title,
                "body": body,
                "state": state,
                "assignee": assignee,
                "labels": _comma_join(labels),
                "milestone": milestone,
                "security_hole": security_hole,
            },
        )

    def list_comments(
        self,
        *,
        number: Union[int, str],
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[IssueComment]:
        """List comments for an issue.

        :param number: Repository-local issue number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path (name). Uses the client default when omitted.
        :param page: Current page number (query).
        :param per_page: Page size; maximum per REST API is typically 100.
        :returns: Issue comments.
        """
        return self._models(
            "GET",
            self._client._repo_path("issues", number, "comments", owner=owner, repo=repo),
            IssueComment,
            params={"page": page, "per_page": per_page},
        )

    def create_comment(
        self,
        *,
        number: Union[int, str],
        body: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> IssueComment:
        """Create a comment on an issue.

        :param number: Repository-local issue number.
        :param body: Comment body text.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Created comment.
        """
        return self._model(
            "POST",
            self._client._repo_path("issues", number, "comments", owner=owner, repo=repo),
            IssueComment,
            json={"body": body},
        )

    def get_comment(
        self,
        *,
        comment_id: Union[int, str],
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> IssueComment:
        """Get a single issue comment by identifier.

        :param comment_id: Comment id from the API.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Issue comment.
        """
        return self._model(
            "GET",
            self._client._repo_path("issues", "comments", comment_id, owner=owner, repo=repo),
            IssueComment,
        )

    def update_comment(
        self,
        *,
        comment_id: Union[int, str],
        body: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> IssueComment:
        """Update an issue comment.

        :param comment_id: Comment id from the API.
        :param body: Updated comment body.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Updated comment.
        """
        return self._model(
            "PATCH",
            self._client._repo_path("issues", "comments", comment_id, owner=owner, repo=repo),
            IssueComment,
            json={"body": body},
        )

    def delete_comment(
        self, *, comment_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Delete an issue comment.

        :param comment_id: Comment id from the API.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        self._request("DELETE", self._client._repo_path("issues", "comments", comment_id, owner=owner, repo=repo))

    def list_pull_requests(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[PullRequest]:
        """List pull requests associated with an issue.

        :param number: Repository-local issue number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Pull requests linked to the issue.
        """
        return self._models(
            "GET",
            self._client._repo_path("issues", number, "pull_requests", owner=owner, repo=repo),
            PullRequest,
        )

    def add_labels(
        self, *, number: Union[int, str], labels: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Label]:
        """Add labels to an issue.

        :param number: Repository-local issue number.
        :param labels: Label names to add (request body is a JSON array per REST API).
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Labels on the issue after the operation.
        """
        return self._models(
            "POST",
            self._client._repo_path("issues", number, "labels", owner=owner, repo=repo),
            Label,
            json=labels,
        )

    def remove_label(
        self, *, number: Union[int, str], name: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Remove one label from an issue (REST path includes the label name).

        :param number: Repository-local issue number.
        :param name: Label name to remove.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        self._request("DELETE", self._client._repo_path("issues", number, "labels", name, owner=owner, repo=repo))

    def list_enterprise(self, *, enterprise: str, **params) -> List[Issue]:
        """List enterprise issues visible to the caller.

        :param enterprise: Enterprise path or login.
        :param params: Additional query parameters accepted by ``GET .../enterprises/{enterprise}/issues``.
        :returns: Enterprise-scoped issues.
        """
        return self._models("GET", self._client._path("enterprises", enterprise, "issues"), Issue, params=params)

    def list_user(self, **params) -> List[Issue]:
        """List issues for the authenticated user.

        :param params: Query parameters for ``GET /user/issues`` (filters, pagination, etc.).
        :returns: Issues assigned to or authored by the user, per API rules.
        """
        return self._models("GET", self._client._path("user", "issues"), Issue, params=params)

    def list_org(self, *, org: str, **params) -> List[Issue]:
        """List organization issues visible to the current user.

        :param org: Organization path or login.
        :param params: Query parameters for ``GET .../orgs/{org}/issues``.
        :returns: Organization-scoped issues.
        """
        return self._models("GET", self._client._path("orgs", org, "issues"), Issue, params=params)

    def get_enterprise_issue(self, *, enterprise: str, number: Union[int, str]) -> Issue:
        """Get a specific enterprise issue.

        :param enterprise: Enterprise path or login.
        :param number: Enterprise issue id or number as accepted by the API path.
        :returns: Issue payload.
        """
        return self._model("GET", self._client._path("enterprises", enterprise, "issues", number), Issue)

    def list_enterprise_comments(self, *, enterprise: str, number: Union[int, str], **params) -> List[IssueComment]:
        """List comments for an enterprise issue.

        :param enterprise: Enterprise path or login.
        :param number: Enterprise issue identifier in the path.
        :param params: Optional pagination or filter query parameters.
        :returns: Comments on the enterprise issue.
        """
        return self._models(
            "GET",
            self._client._path("enterprises", enterprise, "issues", number, "comments"),
            IssueComment,
            params=params,
        )

    def list_enterprise_labels(self, *, enterprise: str, issue_id: Union[int, str]) -> List[Label]:
        """List labels attached to an enterprise issue.

        :param enterprise: Enterprise path or login.
        :param issue_id: Enterprise issue id in the path segment ``.../issues/{issue_id}/labels``.
        :returns: Labels on the issue.
        """
        return self._models("GET", self._client._path("enterprises", enterprise, "issues", issue_id, "labels"), Label)

    def list_operation_logs(
        self, *, owner: str, number: Union[int, str], page: Optional[int] = None, per_page: Optional[int] = None
    ) -> List[IssueOperationLog]:
        """List operation (audit) logs for an issue.

        :param owner: Repository owner path (path segment ``repos/{owner}/...`` for this endpoint).
        :param number: Repository-local issue number.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Operation log entries.
        """
        return self._models(
            "GET",
            self._client._path("repos", owner, "issues", number, "operate_logs"),
            IssueOperationLog,
            params={"page": page, "per_page": per_page},
        )


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
        :returns: A list of pull requests, or an :class:`~gitcode_api._models.APIObject` when the response is a count object.
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
        :param head: Source branch ref (head branch).
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
        :param fork_path: Fork namespace/path when opening a PR from a fork.
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


class LabelsResource(SyncResource):
    """Synchronous label endpoints."""

    def list(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> List[Label]:
        """List repository labels.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: All labels defined on the repository.
        """
        return self._models("GET", self._client._repo_path("labels", owner=owner, repo=repo), Label)

    def create(self, *, name: str, color: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Label:
        """Create a repository label.

        :param name: Label name.
        :param color: Label color (typically a ``#RRGGBB`` hex string per API examples).
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Created label.
        """
        return self._model(
            "POST",
            self._client._repo_path("labels", owner=owner, repo=repo),
            Label,
            json={"name": name, "color": color},
        )

    def update(
        self,
        *,
        original_name: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        name: Optional[str] = None,
        color: Optional[str] = None,
    ) -> Label:
        """Update a repository label.

        :param original_name: Current label name in the URL path.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param name: New label name, if renaming.
        :param color: New color value.
        :returns: Updated label.
        """
        return self._model(
            "PATCH",
            self._client._repo_path("labels", original_name, owner=owner, repo=repo),
            Label,
            json={"name": name, "color": color},
        )

    def delete(self, *, name: str, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Delete a repository label.

        :param name: Label name in the path.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        self._request("DELETE", self._client._repo_path("labels", name, owner=owner, repo=repo))

    def clear_issue_labels(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Remove all labels from an issue.

        :param number: Repository-local issue number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        self._request("DELETE", self._client._repo_path("issues", number, "labels", owner=owner, repo=repo))

    def replace_issue_labels(
        self, *, number: Union[int, str], labels: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Label]:
        """Replace all labels on an issue.

        :param number: Repository-local issue number.
        :param labels: Complete new label set (JSON array body).
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Labels after replacement.
        """
        return self._models(
            "PUT",
            self._client._repo_path("issues", number, "labels", owner=owner, repo=repo),
            Label,
            json=labels,
        )

    def list_enterprise(
        self,
        *,
        enterprise: str,
        search: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        api_version: str = "v5",
    ) -> List[Label]:
        """List labels for an enterprise, optionally using a different API version.

        :param enterprise: Enterprise path or login.
        :param search: Optional name search string.
        :param direction: Sort direction for results.
        :param page: Page number.
        :param per_page: Page size.
        :param api_version: ``v5`` uses ``/api/v5/...``; other values build ``/api/{version}/...`` on the same host.
        :returns: Enterprise label definitions.
        """
        if api_version == "v5":
            path = self._client._path("enterprises", enterprise, "labels")
        else:
            host = self._client.base_url.split("/api/", maxsplit=1)[0]
            path = f"{host}/api/{api_version}/enterprises/{self._client._encode_segment(enterprise)}/labels"
        return self._models(
            "GET",
            path,
            Label,
            params={"search": search, "direction": direction, "page": page, "per_page": per_page},
        )


class MilestonesResource(SyncResource):
    """Synchronous milestone endpoints."""

    def list(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params) -> List[Milestone]:
        """List milestones for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param params: Query parameters accepted by the milestones listing (state, sort, pagination, etc.).
        :returns: Milestones.
        """
        return self._models(
            "GET", self._client._repo_path("milestones", owner=owner, repo=repo), Milestone, params=params
        )

    def get(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> Milestone:
        """Get a single milestone.

        :param number: Milestone number in the repository.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Milestone details.
        """
        return self._model("GET", self._client._repo_path("milestones", number, owner=owner, repo=repo), Milestone)

    def create(
        self,
        *,
        title: str,
        due_on: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Milestone:
        """Create a milestone.

        :param title: Milestone title.
        :param due_on: Due date string in the format expected by the API (often ISO 8601).
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param description: Optional description.
        :returns: Created milestone.
        """
        return self._model(
            "POST",
            self._client._repo_path("milestones", owner=owner, repo=repo),
            Milestone,
            json={"title": title, "due_on": due_on, "description": description},
        )

    def update(
        self,
        *,
        number: Union[int, str],
        title: str,
        due_on: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        description: Optional[str] = None,
        state: Optional[str] = None,
    ) -> Milestone:
        """Update a milestone.

        :param number: Milestone number.
        :param title: Updated title.
        :param due_on: Updated due date.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param description: Updated description.
        :param state: Milestone state such as ``open`` or ``closed`` per API.
        :returns: Updated milestone.
        """
        return self._model(
            "PATCH",
            self._client._repo_path("milestones", number, owner=owner, repo=repo),
            Milestone,
            json={"title": title, "due_on": due_on, "description": description, "state": state},
        )

    def delete(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Delete a milestone.

        :param number: Milestone number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        self._request("DELETE", self._client._repo_path("milestones", number, owner=owner, repo=repo))


class MembersResource(SyncResource):
    """Synchronous repository member endpoints."""

    def add_or_update(
        self,
        *,
        username: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        permission: Optional[str] = None,
    ) -> RepoMember:
        """Add or update repository member permissions.

        :param username: Collaborator login.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param permission: Permission string (for example ``pull``, ``push``, ``admin`` per GitCode API).
        :returns: Collaborator record.
        """
        return self._model(
            "PUT",
            self._client._repo_path("collaborators", username, owner=owner, repo=repo),
            RepoMember,
            json={"permission": permission},
        )

    def remove(self, *, username: str, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Remove a repository member.

        :param username: Collaborator login to remove.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        self._request("DELETE", self._client._repo_path("collaborators", username, owner=owner, repo=repo))

    def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[RepoCollaborator]:
        """List repository members (collaborators).

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Collaborators with permission metadata.
        """
        return self._models(
            "GET",
            self._client._repo_path("collaborators", owner=owner, repo=repo),
            RepoCollaborator,
            params={"page": page, "per_page": per_page},
        )

    def get(
        self, *, username: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> RepositoryCollaboratorCheck:
        """Check whether a user is a repository member."""
        return self._model(
            "GET",
            self._client._repo_path("collaborators", username, owner=owner, repo=repo),
            RepositoryCollaboratorCheck,
        )

    def get_permission(
        self, *, username: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> RepoMemberPermission:
        """Get repository member permissions.

        :param username: Collaborator login.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Effective permission for the user on the repository.
        """
        return self._model(
            "GET",
            self._client._repo_path("collaborators", username, "permission", owner=owner, repo=repo),
            RepoMemberPermission,
        )


class AsyncIssuesResource(AsyncResource):
    """Asynchronous issue endpoints.

    Methods correspond one-to-one with :class:`IssuesResource`; signatures, JSON/query
    payloads, and return types are the same. Refer to the synchronous class for full
    parameter descriptions aligned with ``docs/rest_api`` (Issues API).
    """

    async def list(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params) -> List[Issue]:
        """List issues for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param params: Query parameters such as ``state``, ``sort``, ``direction``, ``page``, ``per_page``.
        :returns: Matching issues.
        """
        return await self._models(
            "GET", self._client._repo_path("issues", owner=owner, repo=repo), Issue, params=params
        )

    async def get(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> Issue:
        """Get a single issue by number.

        :param number: Repository-local issue number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Issue details.
        """
        return await self._model("GET", self._client._repo_path("issues", number, owner=owner, repo=repo), Issue)

    async def create(
        self,
        *,
        owner: str,
        repo: Optional[str] = None,
        title: str,
        body: Optional[str] = None,
        assignee: Optional[str] = None,
        labels: Optional[List[str]] = None,
        milestone: Union[int, str, None] = None,
        security_hole: Optional[str] = None,
    ) -> Issue:
        """Create an issue for a repository.

        :param owner: Repository owner path.
        :param repo: Repository name. Uses the client default when omitted.
        :param title: Issue title.
        :param body: Optional issue description.
        :param assignee: Optional assignee username.
        :param labels: Optional label names (comma-separated in the JSON body).
        :param milestone: Optional milestone identifier.
        :param security_hole: Whether the issue is private; form field described in the Issues API.
        :returns: Created issue details.
        """
        resolved_repo = repo or self._client.repo
        return await self._model(
            "POST",
            self._client._path("repos", owner, "issues"),
            Issue,
            json={
                "repo": resolved_repo,
                "title": title,
                "body": body,
                "assignee": assignee,
                "labels": _comma_join(labels),
                "milestone": milestone,
                "security_hole": security_hole,
            },
        )

    async def update(
        self,
        *,
        number: Union[int, str],
        owner: str,
        repo: Optional[str] = None,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        assignee: Optional[str] = None,
        labels: Optional[List[str]] = None,
        milestone: Union[int, str, None] = None,
        security_hole: Optional[str] = None,
    ) -> Issue:
        """Update an existing issue.

        :param number: Repository-local issue number.
        :param owner: Repository owner path.
        :param repo: Repository name. Uses the client default when omitted.
        :param title: Updated issue title.
        :param body: Updated issue description.
        :param state: Updated state such as ``reopen`` or ``close``.
        :param assignee: Updated assignee username.
        :param labels: Replacement label names (comma-separated in the JSON body).
        :param milestone: Updated milestone identifier.
        :param security_hole: Whether the issue is private; form field described in the Issues API.
        :returns: Updated issue details.
        """
        resolved_repo = repo or self._client.repo
        return await self._model(
            "PATCH",
            self._client._path("repos", owner, "issues", number),
            Issue,
            json={
                "repo": resolved_repo,
                "title": title,
                "body": body,
                "state": state,
                "assignee": assignee,
                "labels": _comma_join(labels),
                "milestone": milestone,
                "security_hole": security_hole,
            },
        )

    async def list_comments(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None, **params
    ) -> List[IssueComment]:
        """List comments for an issue.

        :param number: Repository-local issue number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path (name). Uses the client default when omitted.
        :param params: Optional query parameters (for example ``page``, ``per_page``).
        :returns: Issue comments.
        """
        return await self._models(
            "GET",
            self._client._repo_path("issues", number, "comments", owner=owner, repo=repo),
            IssueComment,
            params=params,
        )

    async def create_comment(
        self, *, number: Union[int, str], body: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> IssueComment:
        """Create a comment on an issue.

        :param number: Repository-local issue number.
        :param body: Comment body text.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Created comment.
        """
        return await self._model(
            "POST",
            self._client._repo_path("issues", number, "comments", owner=owner, repo=repo),
            IssueComment,
            json={"body": body},
        )

    async def get_comment(
        self, *, comment_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> IssueComment:
        """Get a single issue comment by identifier.

        :param comment_id: Comment id from the API.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Issue comment.
        """
        return await self._model(
            "GET", self._client._repo_path("issues", "comments", comment_id, owner=owner, repo=repo), IssueComment
        )

    async def update_comment(
        self, *, comment_id: Union[int, str], body: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> IssueComment:
        """Update an issue comment.

        :param comment_id: Comment id from the API.
        :param body: Updated comment body.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Updated comment.
        """
        return await self._model(
            "PATCH",
            self._client._repo_path("issues", "comments", comment_id, owner=owner, repo=repo),
            IssueComment,
            json={"body": body},
        )

    async def delete_comment(
        self, *, comment_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Delete an issue comment.

        :param comment_id: Comment id from the API.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        await self._request("DELETE", self._client._repo_path("issues", "comments", comment_id, owner=owner, repo=repo))

    async def list_pull_requests(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[PullRequest]:
        """List pull requests associated with an issue.

        :param number: Repository-local issue number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Pull requests linked to the issue.
        """
        return await self._models(
            "GET", self._client._repo_path("issues", number, "pull_requests", owner=owner, repo=repo), PullRequest
        )

    async def add_labels(
        self, *, number: Union[int, str], labels: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Label]:
        """Add labels to an issue.

        :param number: Repository-local issue number.
        :param labels: Label names to add (request body is a JSON array per REST API).
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Labels on the issue after the operation.
        """
        return await self._models(
            "POST", self._client._repo_path("issues", number, "labels", owner=owner, repo=repo), Label, json=labels
        )

    async def remove_label(
        self, *, number: Union[int, str], name: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Remove one label from an issue (REST path includes the label name).

        :param number: Repository-local issue number.
        :param name: Label name to remove.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        await self._request("DELETE", self._client._repo_path("issues", number, "labels", name, owner=owner, repo=repo))

    async def list_enterprise(self, *, enterprise: str, **params) -> List[Issue]:
        """List enterprise issues visible to the caller.

        :param enterprise: Enterprise path or login.
        :param params: Additional query parameters accepted by ``GET .../enterprises/{enterprise}/issues``.
        :returns: Enterprise-scoped issues.
        """
        return await self._models("GET", self._client._path("enterprises", enterprise, "issues"), Issue, params=params)

    async def list_user(self, **params) -> List[Issue]:
        """List issues for the authenticated user.

        :param params: Query parameters for ``GET /user/issues`` (filters, pagination, etc.).
        :returns: Issues assigned to or authored by the user, per API rules.
        """
        return await self._models("GET", self._client._path("user", "issues"), Issue, params=params)

    async def list_org(self, *, org: str, **params) -> List[Issue]:
        """List organization issues visible to the current user.

        :param org: Organization path or login.
        :param params: Query parameters for ``GET .../orgs/{org}/issues``.
        :returns: Organization-scoped issues.
        """
        return await self._models("GET", self._client._path("orgs", org, "issues"), Issue, params=params)

    async def get_enterprise_issue(self, *, enterprise: str, number: Union[int, str]) -> Issue:
        """Get a specific enterprise issue.

        :param enterprise: Enterprise path or login.
        :param number: Enterprise issue id or number as accepted by the API path.
        :returns: Issue payload.
        """
        return await self._model("GET", self._client._path("enterprises", enterprise, "issues", number), Issue)

    async def list_enterprise_comments(
        self, *, enterprise: str, number: Union[int, str], **params
    ) -> List[IssueComment]:
        """List comments for an enterprise issue.

        :param enterprise: Enterprise path or login.
        :param number: Enterprise issue identifier in the path.
        :param params: Optional pagination or filter query parameters.
        :returns: Comments on the enterprise issue.
        """
        return await self._models(
            "GET",
            self._client._path("enterprises", enterprise, "issues", number, "comments"),
            IssueComment,
            params=params,
        )

    async def list_enterprise_labels(self, *, enterprise: str, issue_id: Union[int, str]) -> List[Label]:
        """List labels attached to an enterprise issue.

        :param enterprise: Enterprise path or login.
        :param issue_id: Enterprise issue id in the path segment ``.../issues/{issue_id}/labels``.
        :returns: Labels on the issue.
        """
        return await self._models(
            "GET", self._client._path("enterprises", enterprise, "issues", issue_id, "labels"), Label
        )

    async def list_operation_logs(self, *, owner: str, number: Union[int, str], **params) -> List[IssueOperationLog]:
        """List operation (audit) logs for an issue.

        :param owner: Repository owner path (path segment ``repos/{owner}/...`` for this endpoint).
        :param number: Repository-local issue number.
        :param params: Optional query parameters (for example ``page``, ``per_page``).
        :returns: Operation log entries.
        """
        return await self._models(
            "GET",
            self._client._path("repos", owner, "issues", number, "operate_logs"),
            IssueOperationLog,
            params=params,
        )


class AsyncPullsResource(AsyncResource):
    """Asynchronous pull request endpoints.

    Methods correspond to :class:`PullsResource` with identical arguments and semantics,
    including ``only_count`` responses documented in the Pull Request API under ``docs/rest_api``.
    """

    async def list(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params
    ) -> Union[List[PullRequest], PullRequestCount]:
        """List pull requests for a repository.

        When ``only_count`` is true in ``params``, the API returns a JSON object with counts per state
        instead of an array (see Pull Request API).

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path (name). Uses the client default when omitted.
        :param params: Query parameters: ``state``, ``sort``, ``direction``, ``page``, ``per_page``, ``base``,
            ``since``, ``author``, ``assignee``, ``reviewer``, ``milestone_number``, ``labels``, time filters,
            ``only_count``, and other fields documented under ``docs/rest_api``.
        :returns: A list of pull requests, or an :class:`~gitcode_api._models.APIObject` for count-only responses.
        """
        response = await self._request("GET", self._client._repo_path("pulls", owner=owner, repo=repo), params=params)
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
        :param head: Source branch ref (head branch).
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
        :param fork_path: Fork namespace/path when opening a PR from a fork.
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
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None, **params
    ) -> List[PullRequestComment]:
        """List comments on a pull request.

        :param number: Pull request number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param params: Optional query parameters (for example ``page``, ``per_page``).
        :returns: Pull request review comments.
        """
        return await self._models(
            "GET",
            self._client._repo_path("pulls", number, "comments", owner=owner, repo=repo),
            PullRequestComment,
            params=params,
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


class AsyncLabelsResource(AsyncResource):
    """Asynchronous label endpoints.

    Mirrors :class:`LabelsResource`; see that class for parameter documentation.
    """

    async def list(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> List[Label]:
        """List repository labels.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: All labels defined on the repository.
        """
        return await self._models("GET", self._client._repo_path("labels", owner=owner, repo=repo), Label)

    async def create(self, *, name: str, color: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Label:
        """Create a repository label.

        :param name: Label name.
        :param color: Label color (typically a ``#RRGGBB`` hex string per API examples).
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Created label.
        """
        return await self._model(
            "POST",
            self._client._repo_path("labels", owner=owner, repo=repo),
            Label,
            json={"name": name, "color": color},
        )

    async def update(
        self,
        *,
        original_name: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        name: Optional[str] = None,
        color: Optional[str] = None,
    ) -> Label:
        """Update a repository label.

        :param original_name: Current label name in the URL path.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param name: New label name, if renaming.
        :param color: New color value.
        :returns: Updated label.
        """
        return await self._model(
            "PATCH",
            self._client._repo_path("labels", original_name, owner=owner, repo=repo),
            Label,
            json={"name": name, "color": color},
        )

    async def delete(self, *, name: str, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Delete a repository label.

        :param name: Label name in the path.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        await self._request("DELETE", self._client._repo_path("labels", name, owner=owner, repo=repo))

    async def clear_issue_labels(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Remove all labels from an issue.

        :param number: Repository-local issue number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        await self._request("DELETE", self._client._repo_path("issues", number, "labels", owner=owner, repo=repo))

    async def replace_issue_labels(
        self, *, number: Union[int, str], labels: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Label]:
        """Replace all labels on an issue.

        :param number: Repository-local issue number.
        :param labels: Complete new label set (JSON array body).
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Labels after replacement.
        """
        return await self._models(
            "PUT", self._client._repo_path("issues", number, "labels", owner=owner, repo=repo), Label, json=labels
        )

    async def list_enterprise(
        self,
        *,
        enterprise: str,
        search: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        api_version: str = "v5",
    ) -> List[Label]:
        """List labels for an enterprise, optionally using a different API version.

        :param enterprise: Enterprise path or login.
        :param search: Optional name search string.
        :param direction: Sort direction for results.
        :param page: Page number.
        :param per_page: Page size.
        :param api_version: ``v5`` uses ``/api/v5/...``; other values build ``/api/{version}/...`` on the same host.
        :returns: Enterprise label definitions.
        """
        if api_version == "v5":
            path = self._client._path("enterprises", enterprise, "labels")
        else:
            host = self._client.base_url.split("/api/", maxsplit=1)[0]
            path = f"{host}/api/{api_version}/enterprises/{self._client._encode_segment(enterprise)}/labels"
        return await self._models(
            "GET", path, Label, params={"search": search, "direction": direction, "page": page, "per_page": per_page}
        )


class AsyncMilestonesResource(AsyncResource):
    """Asynchronous milestone endpoints.

    Mirrors :class:`MilestonesResource`; see that class for parameter documentation.
    """

    async def list(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params) -> List[Milestone]:
        """List milestones for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param params: Query parameters accepted by the milestones listing (state, sort, pagination, etc.).
        :returns: Milestones.
        """
        return await self._models(
            "GET", self._client._repo_path("milestones", owner=owner, repo=repo), Milestone, params=params
        )

    async def get(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> Milestone:
        """Get a single milestone.

        :param number: Milestone number in the repository.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Milestone details.
        """
        return await self._model(
            "GET", self._client._repo_path("milestones", number, owner=owner, repo=repo), Milestone
        )

    async def create(
        self,
        *,
        title: str,
        due_on: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Milestone:
        """Create a milestone.

        :param title: Milestone title.
        :param due_on: Due date string in the format expected by the API (often ISO 8601).
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param description: Optional description.
        :returns: Created milestone.
        """
        return await self._model(
            "POST",
            self._client._repo_path("milestones", owner=owner, repo=repo),
            Milestone,
            json={"title": title, "due_on": due_on, "description": description},
        )

    async def update(
        self,
        *,
        number: Union[int, str],
        title: str,
        due_on: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        description: Optional[str] = None,
        state: Optional[str] = None,
    ) -> Milestone:
        """Update a milestone.

        :param number: Milestone number.
        :param title: Updated title.
        :param due_on: Updated due date.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param description: Updated description.
        :param state: Milestone state such as ``open`` or ``closed`` per API.
        :returns: Updated milestone.
        """
        return await self._model(
            "PATCH",
            self._client._repo_path("milestones", number, owner=owner, repo=repo),
            Milestone,
            json={"title": title, "due_on": due_on, "description": description, "state": state},
        )

    async def delete(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Delete a milestone.

        :param number: Milestone number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        await self._request("DELETE", self._client._repo_path("milestones", number, owner=owner, repo=repo))


class AsyncMembersResource(AsyncResource):
    """Asynchronous repository member endpoints.

    Mirrors :class:`MembersResource` (collaborators API); see that class for parameters.
    """

    async def add_or_update(
        self,
        *,
        username: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        permission: Optional[str] = None,
    ) -> RepoMember:
        """Add or update repository member permissions.

        :param username: Collaborator login.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param permission: Permission string (for example ``pull``, ``push``, ``admin`` per GitCode API).
        :returns: Collaborator record.
        """
        return await self._model(
            "PUT",
            self._client._repo_path("collaborators", username, owner=owner, repo=repo),
            RepoMember,
            json={"permission": permission},
        )

    async def remove(self, *, username: str, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Remove a repository member.

        :param username: Collaborator login to remove.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        await self._request("DELETE", self._client._repo_path("collaborators", username, owner=owner, repo=repo))

    async def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[RepoCollaborator]:
        """List repository members (collaborators).

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Collaborators with permission metadata.
        """
        return await self._models(
            "GET",
            self._client._repo_path("collaborators", owner=owner, repo=repo),
            RepoCollaborator,
            params={"page": page, "per_page": per_page},
        )

    async def get(
        self, *, username: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> RepositoryCollaboratorCheck:
        """Check whether a user is a repository member.

        :param username: User login to look up.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Membership payload (typically includes whether the user is a collaborator).
        """
        return await self._model(
            "GET",
            self._client._repo_path("collaborators", username, owner=owner, repo=repo),
            RepositoryCollaboratorCheck,
        )

    async def get_permission(
        self, *, username: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> RepoMemberPermission:
        """Get repository member permissions.

        :param username: Collaborator login.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Effective permission for the user on the repository.
        """
        return await self._model(
            "GET",
            self._client._repo_path("collaborators", username, "permission", owner=owner, repo=repo),
            RepoMemberPermission,
        )
