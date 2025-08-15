from __future__ import annotations

from typing import TYPE_CHECKING

from ..__global_models__ import (
    Script,
    ScriptListResponse,
    SuccessResponse,
    UpdateScriptVisibilityRequest,
    UpdateScriptAccessListRequest,
    SaveScriptRequest,
    DeleteScriptRequest,
)

if TYPE_CHECKING:
    from ..client import PhantombusterClient


class ScriptsAPI:
    """
    A class for interacting with the Scripts API.
    """

    def __init__(self, client: PhantombusterClient):
        self._client = client

    async def fetch(self, script_id: str) -> Script:
        """Fetches a script by its ID.

        Args:
            script_id: The ID of the script to fetch.

        Returns:
            A Script object.
        """
        response = await self._client._request(
            method="GET", url=f"/scripts/fetch?id={script_id}"
        )
        return Script.model_validate(response.json())

    async def fetch_all(self) -> list[Script]:
        """Fetches all scripts for the current user.

        Returns:
            A list of Script objects.
        """
        response = await self._client._request(method="GET", url="/scripts/fetch-all")
        return ScriptListResponse.model_validate(response.json()).scripts

    async def get_code(self, script_id: str) -> str:
        """Gets the code of a script.

        Args:
            script_id: The ID of the script.

        Returns:
            The script code as a string.
        """
        response = await self._client._request(
            method="GET", url=f"/scripts/code?id={script_id}"
        )
        return response.text

    async def set_visibility(self, script_id: str, visibility: str) -> SuccessResponse:
        """Updates the visibility of a script.

        Args:
            script_id: The ID of the script to update.
            visibility: The new visibility setting (e.g., 'private' or 'public').

        Returns:
            A SuccessResponse object.
        """
        request_data = UpdateScriptVisibilityRequest(id=script_id, visibility=visibility)
        response = await self._client._request(
            method="POST",
            url="/scripts/visibility",
            json=request_data.model_dump(),
        )
        return SuccessResponse.model_validate(response.json())

    async def set_access_list(
        self, script_id: str, access_list: list[str]
    ) -> SuccessResponse:
        """Updates the access list of a script.

        Args:
            script_id: The ID of the script to update.
            access_list: A list of users to grant access to.

        Returns:
            A SuccessResponse object.
        """
        request_data = UpdateScriptAccessListRequest(
            id=script_id, accessList=access_list
        )
        response = await self._client._request(
            method="POST",
            url="/scripts/access-list",
            json=request_data.model_dump(by_alias=True),
        )
        return SuccessResponse.model_validate(response.json())

    async def save(
        self, script: str, script_id: str | None = None, name: str | None = None
    ) -> SuccessResponse:
        """Saves (creates or updates) a script.

        Args:
            script: The script code.
            script_id: The ID of the script to update. If None, a new script is created.
            name: The name for a new script. Required if script_id is None.

        Returns:
            A SuccessResponse object.
        """
        if script_id is None and name is None:
            raise ValueError("Either script_id or name must be provided.")

        request_data = SaveScriptRequest(script=script, id=script_id, name=name)
        response = await self._client._request(
            method="POST",
            url="/scripts/save",
            json=request_data.model_dump(exclude_none=True),
        )
        return SuccessResponse.model_validate(response.json())

    async def delete(self, script_id: str) -> SuccessResponse:
        """Deletes a script by its ID.

        Args:
            script_id: The ID of the script to delete.

        Returns:
            A SuccessResponse object.
        """
        request_data = DeleteScriptRequest(id=script_id)
        response = await self._client._request(
            method="POST",
            url="/scripts/delete",
            json=request_data.model_dump(),
        )
        return SuccessResponse.model_validate(response.json())
