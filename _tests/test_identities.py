import pytest
import respx
from httpx import Response

from ..client import PhantombusterClient
from ..config import PhantombusterConfig
from ..__global_models__ import SaveIdentityRequest, Identity


@pytest.fixture
def config():
    return PhantombusterConfig(api_key="test_api_key")


@pytest.fixture
def client(config):
    return PhantombusterClient.get_instance(config)


@pytest.mark.asyncio
@respx.mock
async def test_save_identity_with_token(client):
    """Tests saving an identity with a token."""
    mock_response = {"id": 1, "name": "Test Identity", "type": "cookie"}
    route = respx.post(f"{client._base_url_v2}/identities/save-with-token").mock(return_value=Response(200, json=mock_response))

    request_data = SaveIdentityRequest(name="Test Identity", type="cookie", value="token-value")
    response = await client.identities.save_with_token(request_data)

    assert route.called
    assert isinstance(response, Identity)
    assert response.name == "Test Identity"

    await client.close()
