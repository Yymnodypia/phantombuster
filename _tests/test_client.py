import pytest
import respx
from httpx import Response

from ..client import PhantombusterClient
from ..config import PhantombusterConfig


@pytest.fixture
def config():
    """Provides a mock PhantombusterConfig."""
    return PhantombusterConfig(api_key="test_api_key")


def test_singleton_pattern(config):
    """Tests that the PhantombusterClient follows the singleton pattern."""
    client1 = PhantombusterClient.get_instance(config)
    client2 = PhantombusterClient.get_instance()
    assert client1 is client2


def test_initialization_with_config(config):
    """Tests that the client initializes correctly with a config."""
    client = PhantombusterClient.get_instance(config)
    assert client.config.api_key == "test_api_key"
    assert client._base_url_v1 == "https://api.phantombuster.com/api/v1"
    assert client._base_url_v2 == "https://api.phantombuster.com/api/v2"


@pytest.mark.asyncio
@respx.mock
async def test_request_v1_and_v2(config):
    """Tests that the _request method calls the correct API version URL."""
    v1_url = "https://api.phantombuster.com/api/v1/test-v1"
    v2_url = "https://api.phantombuster.com/api/v2/test-v2"

    v1_route = respx.get(v1_url).mock(return_value=Response(200, json={"status": "ok"}))
    v2_route = respx.get(v2_url).mock(return_value=Response(200, json={"status": "ok"}))

    client = PhantombusterClient.get_instance(config)

    # Test v1 call
    await client._request("GET", "/test-v1", api_version="v1")
    assert v1_route.called

    # Test v2 call
    await client._request("GET", "/test-v2", api_version="v2")
    assert v2_route.called

    await client.close()
