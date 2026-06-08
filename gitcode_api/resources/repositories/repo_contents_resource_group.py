"""AbstractRepoContentsResource, RepoContentsResource, and AsyncRepoContentsResource resource group."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..._models import (
    Blob,
    CommitResult,
    ContentObject,
    Tree,
)
from .._shared import AsyncResource, SyncResource

# mypy: disable-error-code=override
# pylint: disable=invalid-overridden-method,protected-access,redefined-builtin


class AbstractRepoContentsResource(ABC):
    """Interface for RepoContents resource endpoints."""

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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
        :param recursive: Pass ``1`` to fetch the tree recursively (query parameter per Repository API).
        :param page: Page number for large trees.
        :param per_page: Page size for large trees.
        :returns: Tree metadata and entries.
        """

    @abstractmethod
    def get_blob(self, *, sha: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Blob:
        """Get a Git blob object by SHA.

        :param sha: Blob SHA.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Blob metadata and content.
        """

    @abstractmethod
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


class RepoContentsResource(SyncResource, AbstractRepoContentsResource):
    """Synchronous repository contents endpoints."""

    def get(
        self,
        *,
        path: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        ref: Optional[str] = None,
    ) -> ContentObject:
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
        return self._model(
            "GET",
            self._client._repo_path("git", "trees", sha, owner=owner, repo=repo),
            Tree,
            params={"recursive": recursive, "page": page, "per_page": per_page},
        )

    def get_blob(self, *, sha: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Blob:
        return self._model("GET", self._client._repo_path("git", "blobs", sha, owner=owner, repo=repo), Blob)

    def get_raw(
        self,
        *,
        path: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        ref: Optional[str] = None,
    ) -> bytes:
        return self._request(
            "GET",
            self._client._repo_file_path("raw", path, owner=owner, repo=repo),
            params={"ref": ref},
            raw=True,
        )


class AsyncRepoContentsResource(AsyncResource, AbstractRepoContentsResource):
    """Asynchronous repository contents endpoints.

    Mirrors :class:`RepoContentsResource` (contents, trees, blobs, raw files; see ``docs/rest_api/repos``).
    """

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
