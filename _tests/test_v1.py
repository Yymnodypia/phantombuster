import pytest
import respx
from httpx import Response

from ..client import PhantombusterClient
from ..config import PhantombusterConfig
from ..__global_models__ import Agent, Script, User


@pytest.fixture
def config():
    return PhantombusterConfig(api_key="test_api_key")


@pytest.fixture
def client(config):
    return PhantombusterClient.get_instance(config)


@pytest.mark.asyncio
@respx.mock
async def test_get_agent_record(client):
    """Tests getting an agent record from v1."""
    agent_id = 123
    mock_response = {"id": agent_id, "name": "V1 Agent", "scriptId": 101}
    route = respx.get(f"{client._base_url_v1}/agent/{agent_id}").mock(return_value=Response(200, json=mock_response))

    response = await client.v1.get_agent_record(agent_id)

    assert route.called
    assert isinstance(response, Agent)
    assert response.id == agent_id


@pytest.mark.asyncio
@respx.mock
async def test_get_script_by_name(client):
    """Tests getting a script by name from v1."""
    mode, name = "public", "TestScript"
    mock_response = {"id": "s1", "name": name}
    route = respx.get(f"{client._base_url_v1}/script/by-name/{mode}/{name}").mock(return_value=Response(200, json=mock_response))

    response = await client.v1.get_script_by_name(mode, name)

    assert route.called
    assert isinstance(response, Script)
    assert response.name == name


@pytest.mark.asyncio
@respx.mock
async def test_get_user(client):
    """Tests getting user info from v1."""
    mock_response = {"id": 1, "name": "Test User", "email": "test@example.com", "agents": []}
    route = respx.get(f"{client._base_url_v1}/user").mock(return_value=Response(200, json=mock_response))

    response = await client.v1.get_user()

    assert route.called
    assert isinstance(response, User)
    assert response.name == "Test User"

    await client.close()
