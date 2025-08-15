from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..__global_models__ import (
    DeleteLeadsRequest,
    DeleteListRequest,
    Lead,
    LeadListResponse,
    SaveLeadRequest,
    SuccessResponse,
)

if TYPE_CHECKING:
    from ..client import PhantombusterClient


class OrgStorageAPI:
    """
    A class for interacting with the Organization Storage API.
    """

    def __init__(self, client: PhantombusterClient):
        self._client = client

    async def fetch_leads_by_list(self, list_id: int) -> list[Lead]:
        """Fetches leads by their list ID.

        Args:
            list_id: The ID of the list to fetch leads from.

        Returns:
            A list of Lead objects.
        """
        response = await self._client._request(
            method="POST", url=f"/org-storage/leads/by-list/{list_id}"
        )
        return LeadListResponse.model_validate(response.json()).leads

    async def save_lead(
        self, list_id: int, data: dict[str, Any], lead_id: int | None = None
    ) -> Lead:
        """Saves a lead.

        Args:
            list_id: The ID of the list to save the lead to.
            data: The lead's data.
            lead_id: The ID of the lead to update. If None, a new lead is created.

        Returns:
            The saved Lead object.
        """
        request_data = SaveLeadRequest(list_id=list_id, data=data, id=lead_id)
        response = await self._client._request(
            method="POST",
            url="/org-storage/leads/save",
            json=request_data.model_dump(exclude_none=True),
        )
        return Lead.model_validate(response.json())

    async def delete_many_leads(self, lead_ids: list[int]) -> SuccessResponse:
        """Deletes many leads.

        Args:
            lead_ids: A list of lead IDs to delete.

        Returns:
            A success response.
        """
        request_data = DeleteLeadsRequest(lead_ids=lead_ids)
        response = await self._client._request(
            method="POST",
            url="/org-storage/leads/delete-many",
            json=request_data.model_dump(),
        )
        return SuccessResponse.model_validate(response.json())

    async def delete_list(self, list_id: int) -> SuccessResponse:
        """Deletes a list.

        Args:
            list_id: The ID of the list to delete.

        Returns:
            A success response.
        """
        request_data = DeleteListRequest(list_id=list_id)
        response = await self._client._request(
            method="POST",
            url="/org-storage/lists/delete",
            json=request_data.model_dump(),
        )
        return SuccessResponse.model_validate(response.json())
