from __future__ import annotations

from typing import TYPE_CHECKING

from ..__global_models__ import LocationInfo

if TYPE_CHECKING:
    from ..client import PhantombusterClient


class LocationAPI:
    """
    A class for interacting with the Location API.
    """

    def __init__(self, client: PhantombusterClient):
        self._client = client

    async def get_ip(self) -> LocationInfo:
        """Retrieves the country of the IP address.

        Returns:
            The location information for the IP address.
        """
        response = await self._client._request(method="GET", url="/location/ip")
        return LocationInfo.model_validate(response.json())
