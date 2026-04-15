"""Issue, pull request, label, milestone, and member resource groups."""

from typing import Any, List, Optional, Union

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
    PullRequestComment,
    PullRequestFile,
    PullRequestReview,
    PullRequestTest,
    RepoMember,
    RepoMemberPermission,
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
        :param state: Optional issue state filter.
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
        :param security_hole: Optional private issue flag accepted by the API.
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
        :param security_hole: Optional private issue flag accepted by the API.
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
        """List comments for an issue."""
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
        """Create a comment on an issue."""
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
        """Get a single issue comment by identifier."""
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
        """Update an issue comment."""
        return self._model(
            "PATCH",
            self._client._repo_path("issues", "comments", comment_id, owner=owner, repo=repo),
            IssueComment,
            json={"body": body},
        )

    def delete_comment(self, *, comment_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Delete an issue comment."""
        self._request("DELETE", self._client._repo_path("issues", "comments", comment_id, owner=owner, repo=repo))

    def list_pull_requests(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[PullRequest]:
        """List pull requests associated with an issue."""
        return self._models(
            "GET",
            self._client._repo_path("issues", number, "pull_requests", owner=owner, repo=repo),
            PullRequest,
        )

    def add_labels(
        self, *, number: Union[int, str], labels: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Label]:
        """Add labels to an issue."""
        return self._models(
            "POST",
            self._client._repo_path("issues", number, "labels", owner=owner, repo=repo),
            Label,
            json=labels,
        )

    def remove_label(
        self, *, number: Union[int, str], name: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Remove one or more labels from an issue."""
        self._request("DELETE", self._client._repo_path("issues", number, "labels", name, owner=owner, repo=repo))

    def list_enterprise(self, *, enterprise: str, **params: Any) -> List[Issue]:
        """List enterprise issues visible to the caller."""
        return self._models("GET", self._client._path("enterprises", enterprise, "issues"), Issue, params=params)

    def list_user(self, **params: Any) -> List[Issue]:
        """List issues for the authenticated user."""
        return self._models("GET", self._client._path("user", "issues"), Issue, params=params)

    def list_org(self, *, org: str, **params: Any) -> List[Issue]:
        """List organization issues visible to the current user."""
        return self._models("GET", self._client._path("orgs", org, "issues"), Issue, params=params)

    def get_enterprise_issue(self, *, enterprise: str, number: Union[int, str]) -> Issue:
        """Get a specific enterprise issue by global issue identifier."""
        return self._model("GET", self._client._path("enterprises", enterprise, "issues", number), Issue)

    def list_enterprise_comments(self, *, enterprise: str, number: Union[int, str], **params: Any) -> List[IssueComment]:
        """List comments for an enterprise issue."""
        return self._models(
            "GET",
            self._client._path("enterprises", enterprise, "issues", number, "comments"),
            IssueComment,
            params=params,
        )

    def list_enterprise_labels(self, *, enterprise: str, issue_id: Union[int, str]) -> List[Label]:
        """List labels attached to an enterprise issue."""
        return self._models("GET", self._client._path("enterprises", enterprise, "issues", issue_id, "labels"), Label)

    def list_operation_logs(
        self, *, owner: str, number: Union[int, str], page: Optional[int] = None, per_page: Optional[int] = None
    ) -> List[IssueOperationLog]:
        """List operation logs for an issue."""
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
        **params: Any,
    ) -> Union[List[PullRequest], APIObject]:
        """List pull requests for a repository."""
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
            return as_model(response, APIObject)
        return [as_model(item, PullRequest) for item in response]

    def get(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> PullRequest:
        """Get a single pull request."""
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
        """Create a pull request."""
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
        """Update a pull request."""
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
        """Merge a pull request."""
        return self._model(
            "PUT",
            self._client._repo_path("pulls", number, "merge", owner=owner, repo=repo),
            MergeResult,
            json={"merge_commit_message": merge_commit_message, "squash": squash},
        )

    def get_merge_status(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> MergeStatus:
        """Get mergeability status for a pull request."""
        return self._model(
            "GET",
            self._client._repo_path("pulls", number, "merge", owner=owner, repo=repo),
            MergeStatus,
        )

    def list_commits(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[APIObject]:
        """List commits included in a pull request."""
        data = self._request("GET", self._client._repo_path("pulls", number, "commits", owner=owner, repo=repo))
        return [as_model(item, APIObject) for item in data]

    def list_files(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[PullRequestFile]:
        """List files changed by a pull request."""
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
        """List comments on a pull request."""
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
        """Create a pull request comment."""
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
        """Get a single pull request comment."""
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
        """Update a pull request comment."""
        return self._model(
            "PATCH",
            self._client._repo_path("pulls", "comments", comment_id, owner=owner, repo=repo),
            PullRequestComment,
            json={"body": body},
        )

    def delete_comment(self, *, comment_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Delete a pull request comment."""
        self._request("DELETE", self._client._repo_path("pulls", "comments", comment_id, owner=owner, repo=repo))

    def list_labels(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> List[Label]:
        """List labels attached to a pull request."""
        return self._models(
            "GET",
            self._client._repo_path("pulls", number, "labels", owner=owner, repo=repo),
            Label,
        )

    def add_labels(
        self, *, number: Union[int, str], labels: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Label]:
        """Add labels to a pull request."""
        return self._models(
            "POST",
            self._client._repo_path("pulls", number, "labels", owner=owner, repo=repo),
            Label,
            json=labels,
        )

    def replace_labels(
        self, *, number: Union[int, str], labels: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Label]:
        """Replace all labels on a pull request."""
        return self._models(
            "PUT",
            self._client._repo_path("pulls", number, "labels", owner=owner, repo=repo),
            Label,
            json=labels,
        )

    def remove_label(
        self, *, number: Union[int, str], label: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Remove a label from a pull request."""
        self._request("DELETE", self._client._repo_path("pulls", number, "labels", label, owner=owner, repo=repo))

    def request_review(
        self,
        *,
        number: Union[int, str],
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        event: str,
        body: Optional[str] = None,
    ) -> PullRequestReview:
        """Submit a pull request review event."""
        return self._model(
            "POST",
            self._client._repo_path("pulls", number, "review", owner=owner, repo=repo),
            PullRequestReview,
            json={"event": event, "body": body},
        )

    def list_operation_logs(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None, **params: Any
    ) -> List[APIObject]:
        """List operation logs for a pull request."""
        data = self._request(
            "GET",
            self._client._repo_path("pulls", number, "operate_logs", owner=owner, repo=repo),
            params=params,
        )
        return [as_model(item, APIObject) for item in data]

    def request_test(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None, **payload: Any
    ) -> PullRequestTest:
        """Request testing for a pull request."""
        return self._model(
            "POST",
            self._client._repo_path("pulls", number, "test", owner=owner, repo=repo),
            PullRequestTest,
            json=payload,
        )

    def update_testers(
        self, *, number: Union[int, str], testers: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> APIObject:
        """Replace pull request testers."""
        return self._model(
            "PATCH",
            self._client._repo_path("pulls", number, "testers", owner=owner, repo=repo),
            APIObject,
            json={"testers": _comma_join(testers)},
        )

    def add_testers(
        self, *, number: Union[int, str], testers: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> APIObject:
        """Add testers to a pull request."""
        return self._model(
            "POST",
            self._client._repo_path("pulls", number, "testers", owner=owner, repo=repo),
            APIObject,
            json={"testers": _comma_join(testers)},
        )

    def update_assignees(
        self, *, number: Union[int, str], assignees: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> APIObject:
        """Replace pull request assignees."""
        return self._model(
            "PATCH",
            self._client._repo_path("pulls", number, "assignees", owner=owner, repo=repo),
            APIObject,
            json={"assignees": _comma_join(assignees)},
        )

    def add_assignees(
        self, *, number: Union[int, str], assignees: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> APIObject:
        """Add assignees to a pull request."""
        return self._model(
            "POST",
            self._client._repo_path("pulls", number, "assignees", owner=owner, repo=repo),
            APIObject,
            json={"assignees": _comma_join(assignees)},
        )

    def remove_assignees(
        self, *, number: Union[int, str], assignees: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Remove assignees from a pull request."""
        self._request(
            "DELETE",
            self._client._repo_path("pulls", number, "assignees", owner=owner, repo=repo),
            json={"assignees": _comma_join(assignees)},
        )

    def list_issues(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> List[Issue]:
        """List issues linked to a pull request."""
        return self._models("GET", self._client._repo_path("pulls", number, "issues", owner=owner, repo=repo), Issue)

    def list_enterprise(self, *, enterprise: str, **params: Any) -> List[PullRequest]:
        """List enterprise pull requests."""
        return self._models(
            "GET", self._client._path("enterprises", enterprise, "pull_requests"), PullRequest, params=params
        )

    def list_org(self, *, org: str, **params: Any) -> List[PullRequest]:
        """List pull requests for an organization scope."""
        return self._models("GET", self._client._path("org", org, "pull_requests"), PullRequest, params=params)

    def list_issue_pull_requests(self, *, enterprise: str, number: Union[int, str]) -> List[PullRequest]:
        """List pull requests associated with an enterprise issue."""
        return self._models(
            "GET",
            self._client._path("enterprises", enterprise, "issues", number, "pull_requests"),
            PullRequest,
        )


class LabelsResource(SyncResource):
    """Synchronous label endpoints."""

    def list(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> List[Label]:
        """List repository labels."""
        return self._models("GET", self._client._repo_path("labels", owner=owner, repo=repo), Label)

    def create(self, *, name: str, color: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Label:
        """Create a repository label."""
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
        """Update a repository label."""
        return self._model(
            "PATCH",
            self._client._repo_path("labels", original_name, owner=owner, repo=repo),
            Label,
            json={"name": name, "color": color},
        )

    def delete(self, *, name: str, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Delete a repository label."""
        self._request("DELETE", self._client._repo_path("labels", name, owner=owner, repo=repo))

    def clear_issue_labels(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Remove all labels from an issue."""
        self._request("DELETE", self._client._repo_path("issues", number, "labels", owner=owner, repo=repo))

    def replace_issue_labels(
        self, *, number: Union[int, str], labels: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Label]:
        """Replace all labels on an issue."""
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
        """List labels for an enterprise, optionally using a different API version."""
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

    def list(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params: Any) -> List[Milestone]:
        """List milestones for a repository."""
        return self._models(
            "GET", self._client._repo_path("milestones", owner=owner, repo=repo), Milestone, params=params
        )

    def get(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> Milestone:
        """Get a single milestone."""
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
        """Create a milestone."""
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
        """Update a milestone."""
        return self._model(
            "PATCH",
            self._client._repo_path("milestones", number, owner=owner, repo=repo),
            Milestone,
            json={"title": title, "due_on": due_on, "description": description, "state": state},
        )

    def delete(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Delete a milestone."""
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
        """Add or update repository member permissions."""
        return self._model(
            "PUT",
            self._client._repo_path("collaborators", username, owner=owner, repo=repo),
            RepoMember,
            json={"permission": permission},
        )

    def remove(self, *, username: str, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Remove a repository member."""
        self._request("DELETE", self._client._repo_path("collaborators", username, owner=owner, repo=repo))

    def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[RepoMember]:
        """List repository members."""
        return self._models(
            "GET",
            self._client._repo_path("collaborators", owner=owner, repo=repo),
            RepoMember,
            params={"page": page, "per_page": per_page},
        )

    def get(self, *, username: str, owner: Optional[str] = None, repo: Optional[str] = None) -> APIObject:
        """Check whether a user is a repository member."""
        return self._model("GET", self._client._repo_path("collaborators", username, owner=owner, repo=repo), APIObject)

    def get_permission(
        self, *, username: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> RepoMemberPermission:
        """Get repository member permissions."""
        return self._model(
            "GET",
            self._client._repo_path("collaborators", username, "permission", owner=owner, repo=repo),
            RepoMemberPermission,
        )


class AsyncIssuesResource(AsyncResource):
    """Asynchronous issue endpoints."""

    async def list(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params: Any) -> List[Issue]:
        return await self._models(
            "GET", self._client._repo_path("issues", owner=owner, repo=repo), Issue, params=params
        )

    async def get(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> Issue:
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
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None, **params: Any
    ) -> List[IssueComment]:
        return await self._models(
            "GET",
            self._client._repo_path("issues", number, "comments", owner=owner, repo=repo),
            IssueComment,
            params=params,
        )

    async def create_comment(
        self, *, number: Union[int, str], body: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> IssueComment:
        return await self._model(
            "POST",
            self._client._repo_path("issues", number, "comments", owner=owner, repo=repo),
            IssueComment,
            json={"body": body},
        )

    async def get_comment(
        self, *, comment_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> IssueComment:
        return await self._model(
            "GET", self._client._repo_path("issues", "comments", comment_id, owner=owner, repo=repo), IssueComment
        )

    async def update_comment(
        self, *, comment_id: Union[int, str], body: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> IssueComment:
        return await self._model(
            "PATCH",
            self._client._repo_path("issues", "comments", comment_id, owner=owner, repo=repo),
            IssueComment,
            json={"body": body},
        )

    async def delete_comment(
        self, *, comment_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        await self._request("DELETE", self._client._repo_path("issues", "comments", comment_id, owner=owner, repo=repo))

    async def list_pull_requests(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[PullRequest]:
        return await self._models(
            "GET", self._client._repo_path("issues", number, "pull_requests", owner=owner, repo=repo), PullRequest
        )

    async def add_labels(
        self, *, number: Union[int, str], labels: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Label]:
        return await self._models(
            "POST", self._client._repo_path("issues", number, "labels", owner=owner, repo=repo), Label, json=labels
        )

    async def remove_label(
        self, *, number: Union[int, str], name: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        await self._request("DELETE", self._client._repo_path("issues", number, "labels", name, owner=owner, repo=repo))

    async def list_enterprise(self, *, enterprise: str, **params: Any) -> List[Issue]:
        return await self._models("GET", self._client._path("enterprises", enterprise, "issues"), Issue, params=params)

    async def list_user(self, **params: Any) -> List[Issue]:
        return await self._models("GET", self._client._path("user", "issues"), Issue, params=params)

    async def list_org(self, *, org: str, **params: Any) -> List[Issue]:
        return await self._models("GET", self._client._path("orgs", org, "issues"), Issue, params=params)

    async def get_enterprise_issue(self, *, enterprise: str, number: Union[int, str]) -> Issue:
        return await self._model("GET", self._client._path("enterprises", enterprise, "issues", number), Issue)

    async def list_enterprise_comments(
        self, *, enterprise: str, number: Union[int, str], **params: Any
    ) -> List[IssueComment]:
        return await self._models(
            "GET",
            self._client._path("enterprises", enterprise, "issues", number, "comments"),
            IssueComment,
            params=params,
        )

    async def list_enterprise_labels(self, *, enterprise: str, issue_id: Union[int, str]) -> List[Label]:
        return await self._models(
            "GET", self._client._path("enterprises", enterprise, "issues", issue_id, "labels"), Label
        )

    async def list_operation_logs(self, *, owner: str, number: Union[int, str], **params: Any) -> List[IssueOperationLog]:
        return await self._models(
            "GET",
            self._client._path("repos", owner, "issues", number, "operate_logs"),
            IssueOperationLog,
            params=params,
        )


class AsyncPullsResource(AsyncResource):
    """Asynchronous pull request endpoints."""

    async def list(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params: Any
    ) -> Union[List[PullRequest], APIObject]:
        response = await self._request("GET", self._client._repo_path("pulls", owner=owner, repo=repo), params=params)
        if isinstance(response, dict):
            return as_model(response, APIObject)
        return [as_model(item, PullRequest) for item in response]

    async def get(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> PullRequest:
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
        return await self._model(
            "PUT",
            self._client._repo_path("pulls", number, "merge", owner=owner, repo=repo),
            MergeResult,
            json={"merge_commit_message": merge_commit_message, "squash": squash},
        )

    async def get_merge_status(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> MergeStatus:
        return await self._model(
            "GET", self._client._repo_path("pulls", number, "merge", owner=owner, repo=repo), MergeStatus
        )

    async def list_commits(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[APIObject]:
        data = await self._request("GET", self._client._repo_path("pulls", number, "commits", owner=owner, repo=repo))
        return [as_model(item, APIObject) for item in data]

    async def list_files(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[PullRequestFile]:
        return await self._models(
            "GET", self._client._repo_path("pulls", number, "files", owner=owner, repo=repo), PullRequestFile
        )

    async def list_comments(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None, **params: Any
    ) -> List[PullRequestComment]:
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
        return await self._model(
            "POST",
            self._client._repo_path("pulls", number, "comments", owner=owner, repo=repo),
            PullRequestComment,
            json={"body": body, "commit_id": commit_id, "path": path, "position": position},
        )

    async def get_comment(
        self, *, comment_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> PullRequestComment:
        return await self._model(
            "GET", self._client._repo_path("pulls", "comments", comment_id, owner=owner, repo=repo), PullRequestComment
        )

    async def update_comment(
        self, *, comment_id: Union[int, str], body: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> PullRequestComment:
        return await self._model(
            "PATCH",
            self._client._repo_path("pulls", "comments", comment_id, owner=owner, repo=repo),
            PullRequestComment,
            json={"body": body},
        )

    async def delete_comment(
        self, *, comment_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        await self._request("DELETE", self._client._repo_path("pulls", "comments", comment_id, owner=owner, repo=repo))

    async def list_labels(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Label]:
        return await self._models(
            "GET", self._client._repo_path("pulls", number, "labels", owner=owner, repo=repo), Label
        )

    async def add_labels(
        self, *, number: Union[int, str], labels: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Label]:
        return await self._models(
            "POST", self._client._repo_path("pulls", number, "labels", owner=owner, repo=repo), Label, json=labels
        )

    async def replace_labels(
        self, *, number: Union[int, str], labels: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Label]:
        return await self._models(
            "PUT", self._client._repo_path("pulls", number, "labels", owner=owner, repo=repo), Label, json=labels
        )

    async def remove_label(
        self, *, number: Union[int, str], label: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        await self._request("DELETE", self._client._repo_path("pulls", number, "labels", label, owner=owner, repo=repo))

    async def request_review(
        self,
        *,
        number: Union[int, str],
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        event: str,
        body: Optional[str] = None,
    ) -> PullRequestReview:
        return await self._model(
            "POST",
            self._client._repo_path("pulls", number, "review", owner=owner, repo=repo),
            PullRequestReview,
            json={"event": event, "body": body},
        )

    async def list_operation_logs(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None, **params: Any
    ) -> List[APIObject]:
        data = await self._request(
            "GET", self._client._repo_path("pulls", number, "operate_logs", owner=owner, repo=repo), params=params
        )
        return [as_model(item, APIObject) for item in data]

    async def request_test(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None, **payload: Any
    ) -> PullRequestTest:
        return await self._model(
            "POST",
            self._client._repo_path("pulls", number, "test", owner=owner, repo=repo),
            PullRequestTest,
            json=payload,
        )

    async def update_testers(
        self, *, number: Union[int, str], testers: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> APIObject:
        return await self._model(
            "PATCH",
            self._client._repo_path("pulls", number, "testers", owner=owner, repo=repo),
            APIObject,
            json={"testers": _comma_join(testers)},
        )

    async def add_testers(
        self, *, number: Union[int, str], testers: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> APIObject:
        return await self._model(
            "POST",
            self._client._repo_path("pulls", number, "testers", owner=owner, repo=repo),
            APIObject,
            json={"testers": _comma_join(testers)},
        )

    async def update_assignees(
        self, *, number: Union[int, str], assignees: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> APIObject:
        return await self._model(
            "PATCH",
            self._client._repo_path("pulls", number, "assignees", owner=owner, repo=repo),
            APIObject,
            json={"assignees": _comma_join(assignees)},
        )

    async def add_assignees(
        self, *, number: Union[int, str], assignees: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> APIObject:
        return await self._model(
            "POST",
            self._client._repo_path("pulls", number, "assignees", owner=owner, repo=repo),
            APIObject,
            json={"assignees": _comma_join(assignees)},
        )

    async def remove_assignees(
        self, *, number: Union[int, str], assignees: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        await self._request(
            "DELETE",
            self._client._repo_path("pulls", number, "assignees", owner=owner, repo=repo),
            json={"assignees": _comma_join(assignees)},
        )

    async def list_issues(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Issue]:
        return await self._models(
            "GET", self._client._repo_path("pulls", number, "issues", owner=owner, repo=repo), Issue
        )

    async def list_enterprise(self, *, enterprise: str, **params: Any) -> List[PullRequest]:
        return await self._models(
            "GET", self._client._path("enterprises", enterprise, "pull_requests"), PullRequest, params=params
        )

    async def list_org(self, *, org: str, **params: Any) -> List[PullRequest]:
        return await self._models("GET", self._client._path("org", org, "pull_requests"), PullRequest, params=params)

    async def list_issue_pull_requests(self, *, enterprise: str, number: Union[int, str]) -> List[PullRequest]:
        return await self._models(
            "GET", self._client._path("enterprises", enterprise, "issues", number, "pull_requests"), PullRequest
        )


class AsyncLabelsResource(AsyncResource):
    """Asynchronous label endpoints."""

    async def list(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> List[Label]:
        return await self._models("GET", self._client._repo_path("labels", owner=owner, repo=repo), Label)

    async def create(self, *, name: str, color: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Label:
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
        return await self._model(
            "PATCH",
            self._client._repo_path("labels", original_name, owner=owner, repo=repo),
            Label,
            json={"name": name, "color": color},
        )

    async def delete(self, *, name: str, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        await self._request("DELETE", self._client._repo_path("labels", name, owner=owner, repo=repo))

    async def clear_issue_labels(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        await self._request("DELETE", self._client._repo_path("issues", number, "labels", owner=owner, repo=repo))

    async def replace_issue_labels(
        self, *, number: Union[int, str], labels: List[str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> List[Label]:
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
        if api_version == "v5":
            path = self._client._path("enterprises", enterprise, "labels")
        else:
            host = self._client.base_url.split("/api/", maxsplit=1)[0]
            path = f"{host}/api/{api_version}/enterprises/{self._client._encode_segment(enterprise)}/labels"
        return await self._models(
            "GET", path, Label, params={"search": search, "direction": direction, "page": page, "per_page": per_page}
        )


class AsyncMilestonesResource(AsyncResource):
    """Asynchronous milestone endpoints."""

    async def list(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params: Any) -> List[Milestone]:
        return await self._models(
            "GET", self._client._repo_path("milestones", owner=owner, repo=repo), Milestone, params=params
        )

    async def get(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> Milestone:
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
        return await self._model(
            "PATCH",
            self._client._repo_path("milestones", number, owner=owner, repo=repo),
            Milestone,
            json={"title": title, "due_on": due_on, "description": description, "state": state},
        )

    async def delete(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        await self._request("DELETE", self._client._repo_path("milestones", number, owner=owner, repo=repo))


class AsyncMembersResource(AsyncResource):
    """Asynchronous repository member endpoints."""

    async def add_or_update(
        self,
        *,
        username: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        permission: Optional[str] = None,
    ) -> RepoMember:
        return await self._model(
            "PUT",
            self._client._repo_path("collaborators", username, owner=owner, repo=repo),
            RepoMember,
            json={"permission": permission},
        )

    async def remove(self, *, username: str, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        await self._request("DELETE", self._client._repo_path("collaborators", username, owner=owner, repo=repo))

    async def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[RepoMember]:
        return await self._models(
            "GET",
            self._client._repo_path("collaborators", owner=owner, repo=repo),
            RepoMember,
            params={"page": page, "per_page": per_page},
        )

    async def get(self, *, username: str, owner: Optional[str] = None, repo: Optional[str] = None) -> APIObject:
        return await self._model(
            "GET", self._client._repo_path("collaborators", username, owner=owner, repo=repo), APIObject
        )

    async def get_permission(
        self, *, username: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> RepoMemberPermission:
        return await self._model(
            "GET",
            self._client._repo_path("collaborators", username, "permission", owner=owner, repo=repo),
            RepoMemberPermission,
        )
