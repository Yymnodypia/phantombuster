from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from ..__global_models__ import Container, ContainerListResponse

if TYPE_CHECKING:
    from ..client import PhantombusterClient


class ContainersAPI:
    """
    A class for interacting with the Containers API.
    """

    def __init__(self, client: PhantombusterClient):
        self._client = client

    async def fetch(self, container_id: str) -> Container:
        """Fetches a container by its ID.

        Args:
            container_id: The ID of the container to fetch.

        Returns:
            A Container object.
        """
        response = await self._client._request(
            method="GET", url=f"/containers/fetch?id={container_id}"
        )
        return Container.model_validate(response.json())

    async def fetch_all(self, agent_id: str) -> list[Container]:
        """Fetches all containers for a given agent.

        Args:
            agent_id: The ID of the agent.

        Returns:
            A list of Container objects.
        """
        response = await self._client._request(
            method="GET", url=f"/containers/fetch-all?agentId={agent_id}"
        )
        return ContainerListResponse.model_validate(response.json()).containers

    async def fetch_result_object(self, container_id: str) -> Dict[str, Any]:
        """Fetches the result object for a given container.

        Args:
            container_id: The ID of the container.

        Returns:
            A dictionary representing the result object.
        """
        response = await self._client._request(
            method="GET", url=f"/containers/fetch-result-object?id={container_id}"
        )
        return response.json()

