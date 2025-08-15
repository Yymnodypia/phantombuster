import pytest
import respx
from httpx import Response

from ..client import PhantombusterClient
from ..config import PhantombusterConfig
from ..__global_models__ import ContainerListResponse, Container


@pytest.fixture
def config():
    return PhantombusterConfig(api_key="test_api_key")


@pytest.fixture
def client(config):
    return PhantombusterClient.get_instance(config)


@pytest.mark.asyncio
@respx.mock
async def test_fetch_all_containers(client):
    """Tests fetching all containers for an agent."""
    agent_id = "123"
    mock_response = {"data": [{"id": "cid1", "agentId": agent_id}, {"id": "cid2", "agentId": agent_id}]}
    route = respx.get(f"{client._base_url_v2}/containers/fetch-all?agentId={agent_id}").mock(return_value=Response(200, json=mock_response))

    response = await client.containers.fetch_all(agent_id)

    assert route.called
    assert isinstance(response, ContainerListResponse)
    assert len(response.data) == 2


@pytest.mark.asyncio
@respx.mock
async def test_fetch_container(client):
    """Tests fetching a single container."""
    container_id = "cid123"
    mock_response = {"id": container_id, "agentId": "123"}
    route = respx.get(f"{client._base_url_v2}/containers/fetch?id={container_id}").mock(return_value=Response(200, json=mock_response))

    response = await client.containers.fetch(container_id)

    assert route.called
    assert isinstance(response, Container)
    assert response.id == container_id


@pytest.mark.asyncio
@respx.mock
async def test_fetch_result_object(client):
    """Tests fetching the result object for a container."""
    container_id = "cid123"
    mock_response = {"result": "some data"}
    route = respx.get(f"{client._base_url_v2}/containers/fetch-result-object?id={container_id}").mock(return_value=Response(200, json=mock_response))

    response = await client.containers.fetch_result_object(container_id)

    assert route.called
    assert response["result"] == "some data"

    await client.close()
