"""MembersResource and AsyncMembersResource resource group."""

from typing import List, Optional

from ..._models import (
    RepoCollaborator,
    RepoMember,
    RepoMemberPermission,
    RepositoryCollaboratorCheck,
)
from .._shared import AsyncResource, SyncResource


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
