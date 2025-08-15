from __future__ import annotations

from typing import TYPE_CHECKING

from ..__global_models__ import (
    Agent,
    AgentListResponse,
    Container,
    LaunchAgentRequest,
    SaveAgentRequest,
)

if TYPE_CHECKING:
    from ..client import PhantombusterClient


class AgentsAPI:
    """
    A class for interacting with the Agents API.
    """

    def __init__(self, client: PhantombusterClient):
        self._client = client

    async def fetch_all(self) -> list[Agent]:
        """Fetches all agents for the current organization.

        Returns:
            A list of Agent objects.
        """
        response = await self._client._request(method="GET", url="/agents/fetch-all")
        return AgentListResponse.model_validate(response.json()).agents

    async def launch(self, agent_id: int) -> Container:
        """Launches an agent.

        Args:
            agent_id: The ID of the agent to launch.

        Returns:
            A Container object representing the new run.
        """
        request_data = LaunchAgentRequest(id=agent_id)
        response = await self._client._request(
            method="POST",
            url="/agents/launch",
            json=request_data.model_dump(),
        )
        return Container.model_validate(response.json())

    async def save(
        self, name: str, script_id: int, agent_id: int | None = None
    ) -> Agent:
        """Saves (creates or updates) an agent.

        Args:
            name: The name of the agent.
            script_id: The ID of the script to use.
            agent_id: The ID of the agent to update. If None, a new agent is created.

        Returns:
            The saved Agent object.
        """
        request_data = SaveAgentRequest(id=agent_id, name=name, script_id=script_id)
        response = await self._client._request(
            method="POST",
            url="/agents/save",
            json=request_data.model_dump(exclude_none=True),
        )
        return Agent.model_validate(response.json())

