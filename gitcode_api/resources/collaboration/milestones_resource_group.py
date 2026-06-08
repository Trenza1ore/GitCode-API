"""AbstractMilestonesResource, MilestonesResource, and AsyncMilestonesResource resource group."""

from abc import ABC, abstractmethod
from typing import List, Optional, Union

from ..._models import Milestone
from .._shared import AsyncResource, SyncResource

# mypy: disable-error-code=override
# pylint: disable=invalid-overridden-method,protected-access,redefined-builtin


class AbstractMilestonesResource(ABC):
    """Interface for Milestones resource endpoints."""

    @abstractmethod
    def list(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params) -> List[Milestone]:
        """List milestones for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param params: Query parameters accepted by the milestones listing (state, sort, pagination, etc.).
        :returns: Milestones.
        """

    @abstractmethod
    def get(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> Milestone:
        """Get a single milestone.

        :param number: Milestone number in the repository.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Milestone details.
        """

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
    def delete(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Delete a milestone.

        :param number: Milestone number.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """


class MilestonesResource(SyncResource, AbstractMilestonesResource):
    """Synchronous milestone endpoints."""

    def list(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params) -> List[Milestone]:
        return self._models(
            "GET", self._client._repo_path("milestones", owner=owner, repo=repo), Milestone, params=params
        )

    def get(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> Milestone:
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
        return self._model(
            "PATCH",
            self._client._repo_path("milestones", number, owner=owner, repo=repo),
            Milestone,
            json={"title": title, "due_on": due_on, "description": description, "state": state},
        )

    def delete(self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        self._request("DELETE", self._client._repo_path("milestones", number, owner=owner, repo=repo))


class AsyncMilestonesResource(AsyncResource, AbstractMilestonesResource):
    """Asynchronous milestone endpoints.

    Mirrors :class:`MilestonesResource`; see that class for parameter documentation.
    """

    async def list(self, *, owner: Optional[str] = None, repo: Optional[str] = None, **params) -> List[Milestone]:
        return await self._models(
            "GET", self._client._repo_path("milestones", owner=owner, repo=repo), Milestone, params=params
        )

    async def get(
        self, *, number: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> Milestone:
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
