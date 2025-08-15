import pytest
import respx
from httpx import Response

from ..client import PhantombusterClient
from ..config import PhantombusterConfig
from ..__global_models__ import LeadListResponse, SaveLeadRequest, Lead


@pytest.fixture
def config():
    return PhantombusterConfig(api_key="test_api_key")


@pytest.fixture
def client(config):
    return PhantombusterClient.get_instance(config)


@pytest.mark.asyncio
@respx.mock
async def test_fetch_leads_by_list(client):
    """Tests fetching leads by list ID."""
    list_id = 123
    mock_response = {"data": [{"id": 1, "name": "Lead 1"}]}
    route = respx.post(f"{client._base_url_v2}/org-storage/leads/by-list/{list_id}").mock(return_value=Response(200, json=mock_response))

    response = await client.org_storage.fetch_leads_by_list(list_id)

    assert route.called
    assert isinstance(response, LeadListResponse)
    assert len(response.data) == 1


@pytest.mark.asyncio
@respx.mock
async def test_save_lead(client):
    """Tests saving a lead."""
    mock_response = {"id": 2, "name": "New Lead"}
    route = respx.post(f"{client._base_url_v2}/org-storage/leads/save").mock(return_value=Response(200, json=mock_response))

    request_data = SaveLeadRequest(list_id=123, data={"name": "New Lead"})
    response = await client.org_storage.save_lead(request_data)

    assert route.called
    assert isinstance(response, Lead)
    assert response.name == "New Lead"

    await client.close()
