"""IssuesResource and AsyncIssuesResource resource group."""

from typing import List, Optional, Union

from ..._models import (
    Issue,
    IssueComment,
    IssueOperationLog,
    Label,
    PullRequest,
    RepositoryGitCodeTemplate,
    as_model,
)
from ...constants import GITCODE_ISSUE_TEMPLATE_PATH_RE
from .._shared import (
    AsyncResource,
    SyncResource,
    get_gitcode_template_body_async,
    get_gitcode_template_body_sync,
    list_gitcode_template_rows_async,
    list_gitcode_template_rows_sync,
)
from ._helpers import _comma_join


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

    def list_templates(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> List[RepositoryGitCodeTemplate]:
        """List active issue templates under ``.gitcode/`` for this repository.

        Matches Markdown (``.md``, ``.markdown``) and YAML (``.yml`` / ``.yaml``) paths whose
        names start with ``ISSUE_TEMPLATE`` under ``.gitcode/`` (case-insensitive), including
        files inside localized directories such as ``.gitcode/ISSUE_TEMPLATE.en/``.

        Resolution tries the repository, then the owner's ``.gitcode`` repository, then any
        parent main and ``parent/.gitcode`` pairs discovered from forks (each candidate is
        inspected with ``GET /repos/{owner}/{repo}``; when ``fork`` is true, its parent's repos
        are appended, deduplicated, and visited in order). The first source with matching
        templates wins.

        Version 1.2.19: Now also supporting GitHub-mirrored repos with a ``.github/`` folder.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Template metadata entries (paths and SHAs); empty when none match.
        """
        resolved_owner, resolved_repo = self._client._resolve_repo_context(owner, repo)
        rows = list_gitcode_template_rows_sync(
            self._client, resolved_owner, resolved_repo, GITCODE_ISSUE_TEMPLATE_PATH_RE
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
        """Load a single issue template file body from the default branch.

        Uses the same resolution order as :meth:`list_templates`. The path must match the
        active issue template naming convention (see GitCode ``.gitcode`` documentation).

        :param path: Repository-relative path such as ``.gitcode/ISSUE_TEMPLATE_bug.md`` or
            ``.gitcode/ISSUE_TEMPLATE/config.yml``.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param encoding: Codec to use when decoding raw file bytes. Default ``utf-8``.
        :param decoding_kwargs: Keyword arguments forwarded to :meth:`bytes.decode`, such as
            ``errors`` (``"strict"``, ``"ignore"``, or ``"replace"``).
        :returns: Decoded template file contents.
        """
        resolved_owner, resolved_repo = self._client._resolve_repo_context(owner, repo)
        return get_gitcode_template_body_sync(
            self._client,
            path,
            GITCODE_ISSUE_TEMPLATE_PATH_RE,
            resolved_owner,
            resolved_repo,
            encoding=encoding,
            **decoding_kwargs,
        )


class AsyncIssuesResource(AsyncResource):
    """Asynchronous issue endpoints.

    Methods correspond one-to-one with :class:`IssuesResource`; signatures, JSON/query
    payloads, and return types are the same. Refer to the synchronous class for full
    parameter descriptions aligned with ``docs/rest_api`` (Issues API).
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
        return await self._models(
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
        return await self._models(
            "GET",
            self._client._repo_path("issues", number, "comments", owner=owner, repo=repo),
            IssueComment,
            params={"page": page, "per_page": per_page},
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

    async def list_operation_logs(
        self, *, owner: str, number: Union[int, str], page: Optional[int] = None, per_page: Optional[int] = None
    ) -> List[IssueOperationLog]:
        """List operation (audit) logs for an issue.

        :param owner: Repository owner path (path segment ``repos/{owner}/...`` for this endpoint).
        :param number: Repository-local issue number.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Operation log entries.
        """
        return await self._models(
            "GET",
            self._client._path("repos", owner, "issues", number, "operate_logs"),
            IssueOperationLog,
            params={"page": page, "per_page": per_page},
        )

    async def list_templates(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> List[RepositoryGitCodeTemplate]:
        """List active issue templates under ``.gitcode/`` for this repository.

        Matches Markdown (``.md``, ``.markdown``) and YAML (``.yml`` / ``.yaml``) paths whose
        names start with ``ISSUE_TEMPLATE`` under ``.gitcode/`` (case-insensitive), including
        files inside localized directories such as ``.gitcode/ISSUE_TEMPLATE.en/``.

        Resolution tries the repository, then the owner's ``.gitcode`` repository, then any
        parent main and ``parent/.gitcode`` pairs discovered from forks (each candidate is
        inspected with ``GET /repos/{owner}/{repo}``; when ``fork`` is true, its parent's repos
        are appended, deduplicated, and visited in order). The first source with matching
        templates wins.

        Version 1.2.19: Now also supporting GitHub-mirrored repos with a ``.github/`` folder.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Template metadata entries (paths and SHAs); empty when none match.
        """
        resolved_owner, resolved_repo = self._client._resolve_repo_context(owner, repo)
        rows = await list_gitcode_template_rows_async(
            self._client, resolved_owner, resolved_repo, GITCODE_ISSUE_TEMPLATE_PATH_RE
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
        """Load a single issue template file body from the default branch.

        Uses the same resolution order as :meth:`list_templates`. The path must match the
        active issue template naming convention (see GitCode ``.gitcode`` documentation).

        :param path: Repository-relative path such as ``.gitcode/ISSUE_TEMPLATE_bug.md`` or
            ``.gitcode/ISSUE_TEMPLATE/config.yml``.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param encoding: Codec to use when decoding raw file bytes. Default ``utf-8``.
        :param decoding_kwargs: Keyword arguments forwarded to :meth:`bytes.decode`, such as
            ``errors`` (``"strict"``, ``"ignore"``, or ``"replace"``).
        :returns: Decoded template file contents.
        """
        resolved_owner, resolved_repo = self._client._resolve_repo_context(owner, repo)
        return await get_gitcode_template_body_async(
            self._client,
            path,
            GITCODE_ISSUE_TEMPLATE_PATH_RE,
            resolved_owner,
            resolved_repo,
            encoding=encoding,
            **decoding_kwargs,
        )
