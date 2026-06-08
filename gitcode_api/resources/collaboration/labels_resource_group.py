"""LabelsResource and AsyncLabelsResource resource group."""

from typing import List, Optional, Union

from ..._models import Label
from .._shared import AsyncResource, SyncResource


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
