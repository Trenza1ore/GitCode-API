"""AbstractCommitsResource, CommitsResource, and AsyncCommitsResource resource group."""

from abc import ABC, abstractmethod
from typing import List, Optional, Union

from ..._models import (
    Commit,
    CommitComment,
    CommitComparison,
    CommitSummary,
)
from .._shared import AsyncResource, SyncResource

# mypy: disable-error-code=override
# pylint: disable=invalid-overridden-method,protected-access,redefined-builtin


class AbstractCommitsResource(ABC):
    """Interface for Commits resource endpoints."""

    @abstractmethod
    def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        sha: Optional[str] = None,
        path: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[CommitSummary]:
        """List commits in a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :param sha: Optional starting SHA or ref.
        :param path: Optional file path filter.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Matching commits.
        """

    @abstractmethod
    def get(self, *, sha: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Commit:
        """Get a single commit.

        :param sha: Commit SHA or branch name accepted by the API.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Commit details.
        """

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
    def delete_comment(
        self, *, comment_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Delete a commit comment.

        :param comment_id: Commit comment identifier.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        """


class CommitsResource(SyncResource, AbstractCommitsResource):
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
    ) -> List[CommitSummary]:
        return self._models(
            "GET",
            self._client._repo_path("commits", owner=owner, repo=repo),
            CommitSummary,
            params={"sha": sha, "path": path, "page": page, "per_page": per_page},
        )

    def get(self, *, sha: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Commit:
        return self._model("GET", self._client._repo_path("commits", sha, owner=owner, repo=repo), Commit)

    def compare(
        self, *, base: str, head: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> CommitComparison:
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
        return self._model(
            "PATCH",
            self._client._repo_path("comments", comment_id, owner=owner, repo=repo),
            CommitComment,
            json={"body": body},
        )

    def delete_comment(
        self, *, comment_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        self._request("DELETE", self._client._repo_path("comments", comment_id, owner=owner, repo=repo))


class AsyncCommitsResource(AsyncResource, AbstractCommitsResource):
    """Asynchronous commit endpoints.

    Mirrors :class:`CommitsResource` (``docs/rest_api/repos/commit``).
    """

    async def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        sha: Optional[str] = None,
        path: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[CommitSummary]:
        return await self._models(
            "GET",
            self._client._repo_path("commits", owner=owner, repo=repo),
            CommitSummary,
            params={"sha": sha, "path": path, "page": page, "per_page": per_page},
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
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[CommitComment]:
        return await self._models(
            "GET",
            self._client._repo_path("comments", owner=owner, repo=repo),
            CommitComment,
            params={"page": page, "per_page": per_page},
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
