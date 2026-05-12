"""Release, tag, and webhook resource groups."""

from pathlib import Path
from typing import List, Optional, Union

from .._models import ProtectedTag, Release, ReleaseUploadURL, Tag, Webhook
from ._shared import AsyncResource, SyncResource


class ReleasesResource(SyncResource):
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
        """Update a repository release.

        :param tag: Tag name in the release URL path.
        :param name: Release name.
        :param body: Release description.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param release_status: Release status, such as ``pre`` or ``latest``.
        :returns: Updated release payload.
        """
        return self._model(
            "PATCH",
            self._client._repo_path("releases", tag, owner=owner, repo=repo),
            Release,
            json={"name": name, "body": body, "release_status": release_status},
        )

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
        """Upload a release attachment through the pre-signed upload URL.

        :param tag: Tag name in the release URL path.
        :param file_name: Attachment file name to upload.
        :param content: Attachment bytes, or a local file path to read as bytes.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param upload_timeout: Timeout for upload operation. Default to 300 (5 minutes).
        """
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
        """Get a repository release by tag name.

        :param tag: Git tag the release is attached to.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Release metadata for that tag.
        """
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
        """List releases for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param direction: Sort direction, for example ``asc`` or ``desc``.
        :param page: Page number.
        :param per_page: Page size, up to 100.
        :returns: Releases ordered as returned by the API.
        """
        return self._models(
            "GET",
            self._client._repo_path("releases", owner=owner, repo=repo),
            Release,
            params={"direction": direction, "page": page, "per_page": per_page},
        )

    def get_latest(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, type: Optional[str] = None
    ) -> Release:
        """Get the latest repository release.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param type: Selection type, either ``updated`` or ``latest``.
        :returns: Latest release metadata.
        """
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
        """Get a repository release by tag path.

        :param tag: Tag name in the release URL path.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param temp_download_url: Whether to return temporary source package and attachment URLs.
        :returns: Release metadata.
        """
        return self._model(
            "GET",
            self._client._repo_path("releases", tag, owner=owner, repo=repo),
            Release,
            params={"temp_download_url": temp_download_url},
        )

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
        return self._request(
            "GET",
            self._client._repo_path("releases", tag, "attach_files", file_name, "download", owner=owner, repo=repo),
            raw=True,
        )


class TagsResource(SyncResource):
    """Synchronous tag endpoints."""

    def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Tag]:
        """List tags for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Tags.
        """
        return self._models(
            "GET",
            self._client._repo_path("tags", owner=owner, repo=repo),
            Tag,
            params={"page": page, "per_page": per_page},
        )

    def create(
        self,
        *,
        refs: str,
        tag_name: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        tag_message: Optional[str] = None,
    ) -> Tag:
        """Create a tag for a repository.

        :param refs: Object SHA or ref the tag should point to.
        :param tag_name: Name of the new tag.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param tag_message: Optional annotated tag message.
        :returns: Created tag.
        """
        return self._model(
            "POST",
            self._client._repo_path("tags", owner=owner, repo=repo),
            Tag,
            json={"refs": refs, "tag_name": tag_name, "tag_message": tag_message},
        )

    def list_protected(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[ProtectedTag]:
        """List protected tags for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Protected tag rules.
        """
        return self._models(
            "GET",
            self._client._repo_path("protected_tags", owner=owner, repo=repo),
            ProtectedTag,
            params={"page": page, "per_page": per_page},
        )

    def delete_protected(self, *, tag_name: str, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Delete a protected tag rule.

        :param tag_name: Protected tag name in the URL path.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        self._request("DELETE", self._client._repo_path("protected_tags", tag_name, owner=owner, repo=repo))

    def get_protected(self, *, tag_name: str, owner: Optional[str] = None, repo: Optional[str] = None) -> ProtectedTag:
        """Get details for a protected tag rule.

        :param tag_name: Tag name in the path.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Protected tag configuration.
        """
        return self._model(
            "GET",
            self._client._repo_path("protected_tags", tag_name, owner=owner, repo=repo),
            ProtectedTag,
        )

    def create_protected(
        self,
        *,
        name: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        create_access_level: Optional[int] = None,
    ) -> ProtectedTag:
        """Create a protected tag rule.

        :param name: Tag name or pattern to protect.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param create_access_level: Minimum access level required to create matching tags (API-specific integer).
        :returns: Created rule.
        """
        return self._model(
            "POST",
            self._client._repo_path("protected_tags", owner=owner, repo=repo),
            ProtectedTag,
            json={"name": name, "create_access_level": create_access_level},
        )

    def update_protected(
        self, *, name: str, create_access_level: int, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> ProtectedTag:
        """Update a protected tag rule."""
        return self._model(
            "PUT",
            self._client._repo_path("protected_tags", owner=owner, repo=repo),
            ProtectedTag,
            json={"name": name, "create_access_level": create_access_level},
        )


class WebhooksResource(SyncResource):
    """Synchronous webhook endpoints."""

    def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Webhook]:
        """List webhooks for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Hook configurations.
        """
        return self._models(
            "GET",
            self._client._repo_path("hooks", owner=owner, repo=repo),
            Webhook,
            params={"page": page, "per_page": per_page},
        )

    def create(self, *, url: str, owner: Optional[str] = None, repo: Optional[str] = None, **payload) -> Webhook:
        """Create a repository webhook.

        :param url: Payload URL GitCode should POST events to.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param payload: Additional fields from the Webhooks API (events list, secret, content type, etc.).
        :returns: Created webhook.
        """
        payload["url"] = url
        return self._model("POST", self._client._repo_path("hooks", owner=owner, repo=repo), Webhook, json=payload)

    def get(self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> Webhook:
        """Get a repository webhook by identifier.

        :param hook_id: Webhook id from the API.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Webhook configuration.
        """
        return self._model("GET", self._client._repo_path("hooks", hook_id, owner=owner, repo=repo), Webhook)

    def update(
        self,
        *,
        hook_id: Union[int, str],
        url: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        **payload,
    ) -> Webhook:
        """Update a repository webhook.

        :param hook_id: Webhook id.
        :param url: New payload URL (merged into the JSON body).
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param payload: Other mutable webhook fields accepted by the API.
        :returns: Updated webhook.
        """
        payload["url"] = url
        return self._model(
            "PATCH", self._client._repo_path("hooks", hook_id, owner=owner, repo=repo), Webhook, json=payload
        )

    def delete(self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Delete a repository webhook.

        :param hook_id: Webhook id.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        self._request("DELETE", self._client._repo_path("hooks", hook_id, owner=owner, repo=repo))

    def test(self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Send a test delivery for a repository webhook.

        :param hook_id: Webhook id.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        self._request("POST", self._client._repo_path("hooks", hook_id, "tests", owner=owner, repo=repo))


class AsyncReleasesResource(AsyncResource):
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
        """Update a repository release.

        :param tag: Tag name in the release URL path.
        :param name: Release name.
        :param body: Release description.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param release_status: Release status, such as ``pre`` or ``latest``.
        :returns: Updated release payload.
        """
        return await self._model(
            "PATCH",
            self._client._repo_path("releases", tag, owner=owner, repo=repo),
            Release,
            json={"name": name, "body": body, "release_status": release_status},
        )

    async def get_upload_url(
        self, *, tag: str, file_name: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> ReleaseUploadURL:
        """Get a pre-signed URL for uploading a release attachment.

        :param tag: Tag name in the release URL path.
        :param file_name: Attachment file name to upload.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Upload URL and required headers.
        """
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
        """Upload a release attachment through the pre-signed upload URL.

        :param tag: Tag name in the release URL path.
        :param file_name: Attachment file name to upload.
        :param content: Attachment bytes, or a local file path to read as bytes.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param upload_timeout: Timeout for upload operation. Default to 300 (5 minutes).
        """
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
        """Get a repository release by tag name.

        :param tag: Git tag the release is attached to.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Release metadata for that tag.
        """
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
        """List releases for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param direction: Sort direction, for example ``asc`` or ``desc``.
        :param page: Page number.
        :param per_page: Page size, up to 100.
        :returns: Releases ordered as returned by the API.
        """
        return await self._models(
            "GET",
            self._client._repo_path("releases", owner=owner, repo=repo),
            Release,
            params={"direction": direction, "page": page, "per_page": per_page},
        )

    async def get_latest(
        self, *, owner: Optional[str] = None, repo: Optional[str] = None, type: Optional[str] = None
    ) -> Release:
        """Get the latest repository release.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param type: Selection type, either ``updated`` or ``latest``.
        :returns: Latest release metadata.
        """
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
        """Get a repository release by tag path.

        :param tag: Tag name in the release URL path.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param temp_download_url: Whether to return temporary source package and attachment URLs.
        :returns: Release metadata.
        """
        return await self._model(
            "GET",
            self._client._repo_path("releases", tag, owner=owner, repo=repo),
            Release,
            params={"temp_download_url": temp_download_url},
        )

    async def download_attachment(
        self, *, tag: str, file_name: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> bytes:
        """Download a release attachment as bytes.

        :param tag: Tag name in the release URL path.
        :param file_name: Attachment file name.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Attachment bytes.
        """
        return await self._request(
            "GET",
            self._client._repo_path("releases", tag, "attach_files", file_name, "download", owner=owner, repo=repo),
            raw=True,
        )


class AsyncTagsResource(AsyncResource):
    """Asynchronous tag endpoints.

    Mirrors :class:`TagsResource`; see that class and ``docs/rest_api/repos/tag`` for semantics.
    """

    async def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Tag]:
        """List tags for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Tags.
        """
        return await self._models(
            "GET",
            self._client._repo_path("tags", owner=owner, repo=repo),
            Tag,
            params={"page": page, "per_page": per_page},
        )

    async def create(
        self,
        *,
        refs: str,
        tag_name: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        tag_message: Optional[str] = None,
    ) -> Tag:
        """Create a tag for a repository.

        :param refs: Object SHA or ref the tag should point to.
        :param tag_name: Name of the new tag.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param tag_message: Optional annotated tag message.
        :returns: Created tag.
        """
        return await self._model(
            "POST",
            self._client._repo_path("tags", owner=owner, repo=repo),
            Tag,
            json={"refs": refs, "tag_name": tag_name, "tag_message": tag_message},
        )

    async def list_protected(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[ProtectedTag]:
        """List protected tags for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Protected tag rules.
        """
        return await self._models(
            "GET",
            self._client._repo_path("protected_tags", owner=owner, repo=repo),
            ProtectedTag,
            params={"page": page, "per_page": per_page},
        )

    async def delete_protected(self, *, tag_name: str, owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Delete a protected tag rule.

        :param tag_name: Protected tag name in the URL path.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        await self._request("DELETE", self._client._repo_path("protected_tags", tag_name, owner=owner, repo=repo))

    async def get_protected(
        self, *, tag_name: str, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> ProtectedTag:
        """Get details for a protected tag rule.

        :param tag_name: Tag name in the path.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Protected tag configuration.
        """
        return await self._model(
            "GET", self._client._repo_path("protected_tags", tag_name, owner=owner, repo=repo), ProtectedTag
        )

    async def create_protected(
        self,
        *,
        name: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        create_access_level: Optional[int] = None,
    ) -> ProtectedTag:
        """Create a protected tag rule.

        :param name: Tag name or pattern to protect.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param create_access_level: Minimum access level required to create matching tags (API-specific integer).
        :returns: Created rule.
        """
        return await self._model(
            "POST",
            self._client._repo_path("protected_tags", owner=owner, repo=repo),
            ProtectedTag,
            json={"name": name, "create_access_level": create_access_level},
        )

    async def update_protected(
        self, *, name: str, create_access_level: int, owner: Optional[str] = None, repo: Optional[str] = None
    ) -> ProtectedTag:
        """Update a protected tag rule.

        :param name: Tag name or pattern.
        :param create_access_level: New create access level.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Updated rule.
        """
        return await self._model(
            "PUT",
            self._client._repo_path("protected_tags", owner=owner, repo=repo),
            ProtectedTag,
            json={"name": name, "create_access_level": create_access_level},
        )


class AsyncWebhooksResource(AsyncResource):
    """Asynchronous webhook endpoints.

    Mirrors :class:`WebhooksResource`; see that class and ``docs/rest_api/repos/webhooks``.
    """

    async def list(
        self,
        *,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> List[Webhook]:
        """List webhooks for a repository.

        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param page: Page number.
        :param per_page: Page size.
        :returns: Hook configurations.
        """
        return await self._models(
            "GET",
            self._client._repo_path("hooks", owner=owner, repo=repo),
            Webhook,
            params={"page": page, "per_page": per_page},
        )

    async def create(self, *, url: str, owner: Optional[str] = None, repo: Optional[str] = None, **payload) -> Webhook:
        """Create a repository webhook.

        :param url: Payload URL GitCode should POST events to.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param payload: Additional fields from the Webhooks API (events list, secret, content type, etc.).
        :returns: Created webhook.
        """
        payload["url"] = url
        return await self._model(
            "POST", self._client._repo_path("hooks", owner=owner, repo=repo), Webhook, json=payload
        )

    async def get(
        self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> Webhook:
        """Get a repository webhook by identifier.

        :param hook_id: Webhook id from the API.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :returns: Webhook configuration.
        """
        return await self._model("GET", self._client._repo_path("hooks", hook_id, owner=owner, repo=repo), Webhook)

    async def update(
        self,
        *,
        hook_id: Union[int, str],
        url: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        **payload,
    ) -> Webhook:
        """Update a repository webhook.

        :param hook_id: Webhook id.
        :param url: New payload URL (merged into the JSON body).
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        :param payload: Other mutable webhook fields accepted by the API.
        :returns: Updated webhook.
        """
        payload["url"] = url
        return await self._model(
            "PATCH", self._client._repo_path("hooks", hook_id, owner=owner, repo=repo), Webhook, json=payload
        )

    async def delete(
        self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None
    ) -> None:
        """Delete a repository webhook.

        :param hook_id: Webhook id.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        await self._request("DELETE", self._client._repo_path("hooks", hook_id, owner=owner, repo=repo))

    async def test(self, *, hook_id: Union[int, str], owner: Optional[str] = None, repo: Optional[str] = None) -> None:
        """Send a test delivery for a repository webhook.

        :param hook_id: Webhook id.
        :param owner: Repository owner path. Uses the client default when omitted.
        :param repo: Repository path. Uses the client default when omitted.
        """
        await self._request("POST", self._client._repo_path("hooks", hook_id, "tests", owner=owner, repo=repo))
