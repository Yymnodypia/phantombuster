import pytest
import respx
from httpx import Response

from ..client import PhantombusterClient
from ..config import PhantombusterConfig
from ..__global_models__ import OrgResources, AgentGroupListResponse


@pytest.fixture
def config():
    return PhantombusterConfig(api_key="test_api_key")


@pytest.fixture
def client(config):
    return PhantombusterClient.get_instance(config)


@pytest.mark.asyncio
@respx.mock
async def test_fetch_org_resources(client):
    """Tests fetching organization resources."""
    org_id = "1"
    mock_response = {"credits": 100, "storage": 5000}
    route = respx.get(f"{client._base_url_v2}/orgs/fetch-resources?id={org_id}").mock(return_value=Response(200, json=mock_response))

    response = await client.orgs.fetch_resources(org_id)

    assert route.called
    assert isinstance(response, OrgResources)
    assert response.credits == 100


@pytest.mark.asyncio
@respx.mock
async def test_fetch_agent_groups(client):
    """Tests fetching agent groups for an organization."""
    org_id = "1"
    mock_response = {"data": [{"id": 1, "name": "Group 1"}]}
    route = respx.get(f"{client._base_url_v2}/orgs/fetch-agent-groups?id={org_id}").mock(return_value=Response(200, json=mock_response))

    response = await client.orgs.fetch_agent_groups(org_id)

    assert route.called
    assert isinstance(response, AgentGroupListResponse)
    assert len(response.data) == 1

    await client.close()
