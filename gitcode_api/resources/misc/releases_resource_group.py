"""AbstractReleasesResource, ReleasesResource, and AsyncReleasesResource resource group."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Union

from ..._models import Release, ReleaseUploadURL
from .._shared import AsyncResource, SyncResource

# mypy: disable-error-code=override
# pylint: disable=invalid-overridden-method,protected-access,redefined-builtin


class AbstractReleasesResource(ABC):
    """Interface for Releases resource endpoints."""

    @abstractmethod
    def create(
        self,
        *,
        tag: str,
        name: str,
        body: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        target_commitish: Optional[str] = None,
        release_status: Optional[str] = None,
    ) -> Release:
        """Create a repository release.

        :param tag: Tag name for the release.
        :param name: Release title.
        :param body: Release description.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param target_commitish: Branch name or commit SHA for creating a missing tag.
        :param release_status: Release status, such as ``pre`` or ``latest``.
        :returns: Created release payload.
        """

    @abstractmethod
    def update(
        self,
        *,
        tag: str,
        name: str,
        body: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        release_status: Optional[str] = None,
    ) -> Release:
        """Update a repository release.

        :param tag: Tag name in the release URL path.
        :param name: Release name.
        :param body: Release description.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param release_status: Release status, such as ``pre`` or ``latest``.
        :returns: Updated release payload.
        """

    @abstractmethod
    def get_upload_url(
        self, *, tag: str, file_name: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> ReleaseUploadURL:
        """Get a pre-signed URL for uploading a release attachment.

        :param tag: Tag name in the release URL path.
        :param file_name: Attachment file name to upload.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Upload URL and required headers.
        """

    @abstractmethod
    def upload(
        self,
        *,
        tag: str,
        file_name: str,
        content: Union[bytes, str],
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        upload_timeout: Optional[float] = 300.0,
    ) -> None:
        """Upload a release attachment through the pre-signed upload URL.

        :param tag: Tag name in the release URL path.
        :param file_name: Attachment file name to upload.
        :param content: Attachment bytes, or a local file path to read as bytes.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param upload_timeout: Timeout for upload operation. Default to 300 (5 minutes).
        """

    @abstractmethod
    def get_by_tag(self, *, tag: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Release:
        """Get a repository release by tag name.

        :param tag: Git tag the release is attached to.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Release metadata for that tag.
        """

    @abstractmethod
    def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Release]:
        """List releases for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param direction: Sort direction, for example ``asc`` or ``desc``.
        :param page: Page number.
        :param per_page: Page size, up to 100.
        :returns: Releases ordered as returned by the API.
        """

    @abstractmethod
    def get_latest(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, type: Optional[str] = None
    ) -> Release:
        """Get the latest repository release.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param type: Selection type, either ``updated`` or ``latest``.
        :returns: Latest release metadata.
        """

    @abstractmethod
    def get(
        self,
        *,
        tag: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        temp_download_url: Optional[Union[bool, str]] = None,
    ) -> Release:
        """Get a repository release by tag path.

        :param tag: Tag name in the release URL path.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param temp_download_url: Whether to return temporary source package and attachment URLs.
        :returns: Release metadata.
        """

    @abstractmethod
    def download_attachment(
        self, *, tag: str, file_name: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> bytes:
        """Download a release attachment as bytes.

        :param tag: Tag name in the release URL path.
        :param file_name: Attachment file name.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Attachment bytes.
        """


class ReleasesResource(SyncResource, AbstractReleasesResource):
    """Synchronous release endpoints."""

    def create(
        self,
        *,
        tag: str,
        name: str,
        body: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        target_commitish: Optional[str] = None,
        release_status: Optional[str] = None,
    ) -> Release:
        return self._model(
            "POST",
            self._client._repo_path("releases", owner=owner, repo=repo),
            Release,
            json={
                "tag_name": tag,
                "name": name,
                "body": body,
                "target_commitish": target_commitish,
                "release_status": release_status,
            },
        )

    def update(
        self,
        *,
        tag: str,
        name: str,
        body: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        release_status: Optional[str] = None,
    ) -> Release:
        return self._model(
            "PATCH",
            self._client._repo_path("releases", tag, owner=owner, repo=repo),
            Release,
            json={"name": name, "body": body, "release_status": release_status},
        )

    def get_upload_url(
        self, *, tag: str, file_name: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> ReleaseUploadURL:
        return self._model(
            "GET",
            self._client._repo_path("releases", tag, "upload_url", owner=owner, repo=repo),
            ReleaseUploadURL,
            params={"file_name": file_name},
        )

    def upload(
        self,
        *,
        tag: str,
        file_name: str,
        content: Union[bytes, str],
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        upload_timeout: Optional[float] = 300.0,
    ) -> None:
        upload_content = Path(content).read_bytes() if isinstance(content, str) else content
        if not isinstance(upload_content, bytes):
            raise TypeError("content must be bytes or a file path string.")

        upload_url = self.get_upload_url(tag=tag, file_name=file_name, owner=owner, repo=repo)
        if not upload_url.url:
            raise ValueError("Release upload URL response did not include a URL.")

        self._client._client.request(
            "PUT",
            upload_url.url,
            content=upload_content,
            headers=upload_url.headers or {},
            timeout=upload_timeout,
        )

    def get_by_tag(self, *, tag: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Release:
        return self._model(
            "GET",
            self._client._repo_path("releases", "tags", tag, owner=owner, repo=repo),
            Release,
        )

    def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Release]:
        return self._models(
            "GET",
            self._client._repo_path("releases", owner=owner, repo=repo),
            Release,
            params={"direction": direction, "page": page, "per_page": per_page},
        )

    def get_latest(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, type: Optional[str] = None
    ) -> Release:
        return self._model(
            "GET",
            self._client._repo_path("releases", "latest", owner=owner, repo=repo),
            Release,
            params={"type": type},
        )

    def get(
        self,
        *,
        tag: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        temp_download_url: Optional[Union[bool, str]] = None,
    ) -> Release:
        return self._model(
            "GET",
            self._client._repo_path("releases", tag, owner=owner, repo=repo),
            Release,
            params={"temp_download_url": temp_download_url},
        )

    def download_attachment(
        self, *, tag: str, file_name: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> bytes:
        return self._request(
            "GET",
            self._client._repo_path("releases", tag, "attach_files", file_name, "download", owner=owner, repo=repo),
            raw=True,
        )


class AsyncReleasesResource(AsyncResource, AbstractReleasesResource):
    """Asynchronous release endpoints.

    Mirrors :class:`ReleasesResource`; see that class for parameters (Release API in ``docs/rest_api``).
    """

    async def create(
        self,
        *,
        tag: str,
        name: str,
        body: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        target_commitish: Optional[str] = None,
        release_status: Optional[str] = None,
    ) -> Release:
        return await self._model(
            "POST",
            self._client._repo_path("releases", owner=owner, repo=repo),
            Release,
            json={
                "tag_name": tag,
                "name": name,
                "body": body,
                "target_commitish": target_commitish,
                "release_status": release_status,
            },
        )

    async def update(
        self,
        *,
        tag: str,
        name: str,
        body: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        release_status: Optional[str] = None,
    ) -> Release:
        return await self._model(
            "PATCH",
            self._client._repo_path("releases", tag, owner=owner, repo=repo),
            Release,
            json={"name": name, "body": body, "release_status": release_status},
        )

    async def get_upload_url(
        self, *, tag: str, file_name: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> ReleaseUploadURL:
        return await self._model(
            "GET",
            self._client._repo_path("releases", tag, "upload_url", owner=owner, repo=repo),
            ReleaseUploadURL,
            params={"file_name": file_name},
        )

    async def upload(
        self,
        *,
        tag: str,
        file_name: str,
        content: Union[bytes, str],
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        upload_timeout: Optional[float] = 300.0,
    ) -> None:
        upload_content = Path(content).read_bytes() if isinstance(content, str) else content
        if not isinstance(upload_content, bytes):
            raise TypeError("content must be bytes or a file path string.")

        upload_url = await self.get_upload_url(tag=tag, file_name=file_name, owner=owner, repo=repo)
        if not upload_url.url:
            raise ValueError("Release upload URL response did not include a URL.")

        await self._client._client.request(
            "PUT",
            upload_url.url,
            content=upload_content,
            headers=upload_url.headers or {},
            timeout=upload_timeout,
        )

    async def get_by_tag(self, *, tag: str, owner: Optional[str] = None, repo: Optional[str] = None) -> Release:
        return await self._model(
            "GET", self._client._repo_path("releases", "tags", tag, owner=owner, repo=repo), Release
        )

    async def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        direction: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Release]:
        return await self._models(
            "GET",
            self._client._repo_path("releases", owner=owner, repo=repo),
            Release,
            params={"direction": direction, "page": page, "per_page": per_page},
        )

    async def get_latest(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, type: Optional[str] = None
    ) -> Release:
        return await self._model(
            "GET",
            self._client._repo_path("releases", "latest", owner=owner, repo=repo),
            Release,
            params={"type": type},
        )

    async def get(
        self,
        *,
        tag: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        temp_download_url: Optional[Union[bool, str]] = None,
    ) -> Release:
        return await self._model(
            "GET",
            self._client._repo_path("releases", tag, owner=owner, repo=repo),
            Release,
            params={"temp_download_url": temp_download_url},
        )

    async def download_attachment(
        self, *, tag: str, file_name: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> bytes:
        return await self._request(
            "GET",
            self._client._repo_path("releases", tag, "attach_files", file_name, "download", owner=owner, repo=repo),
            raw=True,
        )
