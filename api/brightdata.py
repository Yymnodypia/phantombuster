from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..__global_models__ import BrightDataSerpRequest

if TYPE_CHECKING:
    from ..client import PhantombusterClient


class BrightDataAPI:
    """
    A class for interacting with the Bright Data API.
    """

    def __init__(self, client: PhantombusterClient):
        self._client = client

    async def serp(
        self,
        query: str,
        gl: str | None = None,
        hl: str | None = None,
        tbm: str | None = None,
        start: int | None = None,
        num: int | None = None,
        uule: str | None = None,
        brd_mobile: str | None = None,
        brd_browser: str | None = None,
    ) -> dict[str, Any]:
        """Performs a search using Bright Data.

        Args:
            query: The search query.
            gl: The country to search from.
            hl: The language to search in.
            tbm: The search type.
            start: The result offset.
            num: The number of results to return.
            uule: The encoded location.
            brd_mobile: The mobile device to use.
            brd_browser: The browser to use.

        Returns:
            The search results.
        """
        params = BrightDataSerpRequest(
            q=query,
            gl=gl,
            hl=hl,
            tbm=tbm,
            start=start,
            num=num,
            uule=uule,
            brd_mobile=brd_mobile,
            brd_browser=brd_browser,
        )
        response = await self._client._request(
            method="GET",
            url="/brightdata/serp",
            params=params.model_dump(exclude_none=True),
        )
        return response.json()
