"""SearchResource and AsyncSearchResource resource group."""

from typing import List, Optional

from ..._models import SearchIssue, SearchRepository, SearchUser
from .._shared import AsyncResource, SyncResource


class SearchResource(SyncResource):
    """Synchronous search endpoints."""

    def users(
        self,
        *,
        q: str,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
    ) -> List[SearchUser]:
        """Search users.

        :param q: Search keywords.
        :param page: Page number.
        :param per_page: Page size.
        :param sort: Optional sort field such as ``joined_at``.
        :param order: Sort order, usually ``asc`` or ``desc``.
        :returns: Matching user search results.
        """
        return self._models(
            "GET",
            self._client._path("search", "users"),
            SearchUser,
            params={"q": q, "page": page, "per_page": per_page, "sort": sort, "order": order},
        )

    def issues(
        self,
        *,
        q: str,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
        repo: Optional[str] = None,
        state: Optional[str] = None,
    ) -> List[SearchIssue]:
        """Search issues.

        :param q: Search keywords.
        :param page: Page number.
        :param per_page: Page size.
        :param sort: Optional sort field.
        :param order: Sort order, usually ``asc`` or ``desc``.
        :param repo: Optional repository path filter.
        :param state: Optional issue state filter.
        :returns: Matching issue search results.
        """
        return self._models(
            "GET",
            self._client._path("search", "issues"),
            SearchIssue,
            params={
                "q": q,
                "page": page,
                "per_page": per_page,
                "sort": sort,
                "order": order,
                "repo": repo,
                "state": state,
            },
        )

    def repositories(
        self,
        *,
        q: str,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
        owner: Optional[str] = None,
        fork: Optional[str] = None,
        language: Optional[str] = None,
    ) -> List[SearchRepository]:
        """Search repositories.

        :param q: Search keywords.
        :param page: Page number.
        :param per_page: Page size.
        :param sort: Optional sort field such as ``stars_count``.
        :param order: Sort order, usually ``asc`` or ``desc``.
        :param owner: Optional owner path filter.
        :param fork: Optional fork visibility filter.
        :param language: Optional programming language filter.
        :returns: Matching repository search results.
        """
        return self._models(
            "GET",
            self._client._path("search", "repositories"),
            SearchRepository,
            params={
                "q": q,
                "page": page,
                "per_page": per_page,
                "sort": sort,
                "order": order,
                "owner": owner,
                "fork": fork,
                "language": language,
            },
        )


class AsyncSearchResource(AsyncResource):
    """Asynchronous search endpoints.

    Query parameters match :class:`SearchResource` (``page``, ``per_page``, ``sort``, ``order``, etc.);
    see ``docs/rest_api/search`` and the synchronous methods for field meanings.
    """

    async def users(
        self,
        *,
        q: str,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
    ) -> List[SearchUser]:
        """Search users.

        :param q: Search keywords.
        :param page: Page number.
        :param per_page: Page size.
        :param sort: Optional sort field such as ``joined_at``.
        :param order: Sort order, usually ``asc`` or ``desc``.
        :returns: Matching user search results.
        """
        return await self._models(
            "GET",
            self._client._path("search", "users"),
            SearchUser,
            params={"q": q, "page": page, "per_page": per_page, "sort": sort, "order": order},
        )

    async def issues(
        self,
        *,
        q: str,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
        repo: Optional[str] = None,
        state: Optional[str] = None,
    ) -> List[SearchIssue]:
        """Search issues.

        :param q: Search keywords.
        :param page: Page number.
        :param per_page: Page size.
        :param sort: Optional sort field.
        :param order: Sort order, usually ``asc`` or ``desc``.
        :param repo: Optional repository path filter.
        :param state: Optional issue state filter.
        :returns: Matching issue search results.
        """
        return await self._models(
            "GET",
            self._client._path("search", "issues"),
            SearchIssue,
            params={
                "q": q,
                "page": page,
                "per_page": per_page,
                "sort": sort,
                "order": order,
                "repo": repo,
                "state": state,
            },
        )

    async def repositories(
        self,
        *,
        q: str,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
        owner: Optional[str] = None,
        fork: Optional[str] = None,
        language: Optional[str] = None,
    ) -> List[SearchRepository]:
        """Search repositories.

        :param q: Search keywords.
        :param page: Page number.
        :param per_page: Page size.
        :param sort: Optional sort field such as ``stars_count``.
        :param order: Sort order, usually ``asc`` or ``desc``.
        :param owner: Optional owner path filter.
        :param fork: Optional fork visibility filter.
        :param language: Optional programming language filter.
        :returns: Matching repository search results.
        """
        return await self._models(
            "GET",
            self._client._path("search", "repositories"),
            SearchRepository,
            params={
                "q": q,
                "page": page,
                "per_page": per_page,
                "sort": sort,
                "order": order,
                "owner": owner,
                "fork": fork,
                "language": language,
            },
        )
