"""
API module for interacting with the PhantomBuster 'branches' endpoints.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import PhantombusterClient
from ..__global_models__ import (
    Branch,
    BranchListResponse,
    BranchDiffResponse,
    CreateBranchRequest,
    DeleteBranchRequest,
    ReleaseBranchRequest,
    SuccessResponse,
)

class BranchesAPI:
    """Provides methods for the /branches endpoints."""

    def __init__(self, client: "PhantombusterClient"):
        self._client = client

    async def fetch_all(self) -> BranchListResponse:
        """Gets the branches associated with the current organization's id."""
        response = await self._client._request("get", "/branches/fetch-all")
        return BranchListResponse.parse_obj(response.json())

    async def diff(self) -> BranchDiffResponse:
        """Gets the length difference between the staging and release branches of all scripts."""
        response = await self._client._request("get", "/branches/diff")
        return BranchDiffResponse.parse_obj(response.json())

    async def create(self, data: CreateBranchRequest) -> Branch:
        """Creates a new branch."""
        response = await self._client._request("post", "/branches/create", json=data.dict())
        # Assuming the API returns the created branch object
        return Branch.parse_obj(response.json())

    async def delete(self, data: DeleteBranchRequest) -> SuccessResponse:
        """Deletes a branch by ID."""
        response = await self._client._request("post", "/branches/delete", json=data.dict())
        return SuccessResponse.parse_obj(response.json())

    async def release(self, data: ReleaseBranchRequest) -> SuccessResponse:
        """Releases a script branch."""
        response = await self._client._request("post", "/branches/release", json=data.dict())
        return SuccessResponse.parse_obj(response.json())
