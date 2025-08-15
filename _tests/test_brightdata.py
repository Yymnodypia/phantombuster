import pytest
import respx
from httpx import Response

from ..client import PhantombusterClient
from ..config import PhantombusterConfig
from ..__global_models__ import BrightDataSerpRequest


@pytest.fixture
def config():
    return PhantombusterConfig(api_key="test_api_key")


@pytest.fixture
def client(config):
    return PhantombusterClient.get_instance(config)


@pytest.mark.asyncio
@respx.mock
async def test_brightdata_serp(client):
    """Tests the BrightData SERP endpoint."""
    mock_response = {"status": "success", "data": {"result": "some serp data"}}
    route = respx.get(f"{client._base_url_v2}/brightdata-serp").mock(return_value=Response(200, json=mock_response))

    request_data = BrightDataSerpRequest(query="test query")
    response = await client.brightdata.serp(request_data)

    assert route.called
    assert response["data"]["result"] == "some serp data"

    await client.close()
