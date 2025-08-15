from __future__ import annotations

from typing import TYPE_CHECKING

from ..__global_models__ import Identity, SaveIdentityRequest

if TYPE_CHECKING:
    from ..client import PhantombusterClient


class IdentitiesAPI:
    """
    A class for interacting with the Identities API.
    """

    def __init__(self, client: PhantombusterClient):
        self._client = client

    async def save_with_token(self, name: str, token: str) -> Identity:
        """Saves an identity using a token.

        Args:
            name: The name of the identity.
            token: The token to use for saving the identity.

        Returns:
            The created Identity object.
        """
        request_data = SaveIdentityRequest(name=name, token=token)
        response = await self._client._request(
            method="POST",
            url="/identities/save-with-token",
            json=request_data.model_dump(),
        )
        return Identity.model_validate(response.json())
