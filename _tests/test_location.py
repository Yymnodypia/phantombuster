import pytest
import respx
from httpx import Response

from ..client import PhantombusterClient
from ..config import PhantombusterConfig
from ..__global_models__ import LocationInfo


@pytest.fixture
def config():
    return PhantombusterConfig(api_key="test_api_key")


@pytest.fixture
def client(config):
    return PhantombusterClient.get_instance(config)


@pytest.mark.asyncio
@respx.mock
async def test_get_ip_location(client):
    """Tests getting IP location information."""
    mock_response = {"ip": "8.8.8.8", "country": "US"}
    route = respx.get(f"{client._base_url_v2}/location/ip").mock(return_value=Response(200, json=mock_response))

    response = await client.location.get_ip()

    assert route.called
    assert isinstance(response, LocationInfo)
    assert response.ip == "8.8.8.8"

    await client.close()
