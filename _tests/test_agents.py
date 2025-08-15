import pytest
import respx
from httpx import Response

from ..client import PhantombusterClient
from ..config import PhantombusterConfig
from ..__global_models__ import AgentListResponse, LaunchAgentRequest, SaveAgentRequest, Agent


@pytest.fixture
def config():
    """Provides a mock PhantombusterConfig."""
    return PhantombusterConfig(api_key="test_api_key")


@pytest.fixture
def client(config):
    """Provides a PhantombusterClient instance."""
    return PhantombusterClient.get_instance(config)


@pytest.mark.asyncio
@respx.mock
async def test_fetch_all_agents(client):
    """Tests fetching all agents."""
    mock_response = {
        "data": [
            {"id": 1, "name": "Test Agent 1", "scriptId": 101},
            {"id": 2, "name": "Test Agent 2", "scriptId": 102}
        ]
    }
    route = respx.get(f"{client._base_url_v2}/agents/fetch-all").mock(return_value=Response(200, json=mock_response))

    response = await client.agents.fetch_all()

    assert route.called
    assert isinstance(response, AgentListResponse)
    assert len(response.data) == 2
    assert response.data[0].id == 1


@pytest.mark.asyncio
@respx.mock
async def test_launch_agent(client):
    """Tests launching an agent."""
    agent_id = 123
    mock_response = {"status": "success", "data": {"containerId": "cid-123"}}
    route = respx.post(f"{client._base_url_v2}/agents/launch").mock(return_value=Response(200, json=mock_response))

    request_data = LaunchAgentRequest(id=agent_id)
    response = await client.agents.launch(request_data)

    assert route.called
    assert response["data"]["containerId"] == "cid-123"


@pytest.mark.asyncio
@respx.mock
async def test_save_agent(client):
    """Tests saving an agent."""
    mock_response = {"id": 456, "name": "Updated Agent", "scriptId": 101}
    route = respx.post(f"{client._base_url_v2}/agents/save").mock(return_value=Response(200, json=mock_response))

    request_data = SaveAgentRequest(id=456, name="Updated Agent")
    response = await client.agents.save(request_data)

    assert route.called
    assert isinstance(response, Agent)
    assert response.id == 456
    assert response.name == "Updated Agent"

    await client.close()
