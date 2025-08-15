from __future__ import annotations

from typing import TYPE_CHECKING

from ..__global_models__ import (
    OrgResources,
    Container,
    ContainerListResponse,
    AgentGroup,
    AgentGroupListResponse,
)

if TYPE_CHECKING:
    from ..client import PhantombusterClient


class OrgsAPI:
    """
    A class for interacting with the Orgs API.
    """

    def __init__(self, client: PhantombusterClient):
        self._client = client

    async def fetch_resources(self) -> OrgResources:
        """Fetches the current organization's resources and usage.

        Returns:
            An OrgResources object.
        """
        response = await self._client._request(
            method="GET", url="/orgs/fetch-resources"
        )
        return OrgResources.model_validate(response.json())

    async def export_agent_usage(self) -> str:
        """Exports agent usage as a CSV string.

        Returns:
            A string containing the CSV data.
        """
        response = await self._client._request(
            method="GET", url="/orgs/export-agent-usage"
        )
        return response.text

    async def fetch_running_containers(self) -> list[Container]:
        """Fetches the current organization's running containers.

        Returns:
            A list of Container objects.
        """
        response = await self._client._request(
            method="GET", url="/orgs/fetch-running-containers"
        )
        return ContainerListResponse.model_validate(response.json()).containers

    async def fetch_agent_groups(self) -> list[AgentGroup]:
        """Fetches the agent groups for the current organization.

        Returns:
            A list of AgentGroup objects.
        """
        response = await self._client._request(
            method="GET", url="/orgs/fetch-agent-groups"
        )
        return AgentGroupListResponse.model_validate(response.json()).agent_groups

    async def export_container_usage(self) -> str:
        """Exports container usage as a CSV string.

        Returns:
            A string containing the CSV data.
        """
        response = await self._client._request(
            method="GET", url="/orgs/export-container-usage"
        )
        return response.text
