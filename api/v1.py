from __future__ import annotations

from typing import TYPE_CHECKING

from ..__global_models__ import Agent, Script, User

if TYPE_CHECKING:
    from ..client import PhantombusterClient


class V1API:
    """
    A class for interacting with the v1 PhantomBuster API.
    """

    def __init__(self, client: PhantombusterClient):
        self._client = client

    async def get_agent_record(self, agent_id: str | int) -> Agent:
        """Get an agent record.

        Args:
            agent_id: The ID of the agent to get.

        Returns:
            The agent record.
        """
        response = await self._client._request(
            method="GET",
            url=f"/agent/{agent_id}",
            api_version="v1",
        )
        return Agent.model_validate(response.json())

    async def get_script_by_name(self, mode: str, name: str) -> Script:
        """Get a script record by its name.

        Args:
            mode: The mode of the script (e.g., 'public', 'private').
            name: The name of the script.

        Returns:
            The script record.
        """
        response = await self._client._request(
            method="GET",
            url=f"/script/by-name/{mode}/{name}",
            api_version="v1",
        )
        return Script.model_validate(response.json())

    async def get_user(self) -> User:
        """Get information about your Phantombuster account.

        Returns:
            The user account information.
        """
        response = await self._client._request(
            method="GET",
            url="/user",
            api_version="v1",
        )
        return User.model_validate(response.json())
