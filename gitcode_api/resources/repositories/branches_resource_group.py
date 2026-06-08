"""BranchesResource and AsyncBranchesResource resource group."""

from typing import List, Optional

from ..._models import (
    Branch,
    BranchDetail,
    ProtectedBranch,
)
from .._shared import AsyncResource, SyncResource


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

    def get(self, *, branch: str, owner: Optional[str] = None, repo: Optional[str] = None) -> BranchDetail:
        """Get a single branch.

        :param branch: Branch name.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Branch details.
        """
        return self._model("GET", self._client._repo_path("branches", branch, owner=owner, repo=repo), BranchDetail)

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


class AsyncBranchesResource(AsyncResource):
    """Asynchronous branch endpoints.

    Mirrors :class:`BranchesResource` (``docs/rest_api/repos/branch``).
    """

    async def list(
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
        return await self._models(
            "GET",
            self._client._repo_path("branches", owner=owner, repo=repo),
            Branch,
            params={"sort": sort, "direction": direction, "page": page, "per_page": per_page},
        )

    async def get(self, *, branch: str, owner: Optional[str] = None, repo: Optional[str] = None) -> BranchDetail:
        """Get a single branch.

        :param branch: Branch name.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Branch details.
        """
        return await self._model(
            "GET", self._client._repo_path("branches", branch, owner=owner, repo=repo), BranchDetail
        )

    async def create(self, *, branch: str, ref: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Branch:
        """Create a branch from an existing ref.

        :param branch: New branch name.
        :param ref: Starting ref such as a branch, tag, or commit SHA.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Created branch details.
        """
        return await self._model(
            "POST",
            self._client._repo_path("branches", owner=owner, repo=repo),
            Branch,
            json={"branch_name": branch, "refs": ref},
        )

    async def list_protected(self, *, owner: Optional[str] = None, repo: Optional[str] = None) -> List[ProtectedBranch]:
        """List protected branch rules for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository name. Uses the client default when omitted.
        :returns: Protected branch rules.
        """
        return await self._models(
            "GET", self._client._repo_path("protect_branches", owner=owner, repo=repo), ProtectedBranch
        )
