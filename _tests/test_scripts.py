import pytest
import respx
from httpx import Response

from ..client import PhantombusterClient
from ..config import PhantombusterConfig
from ..__global_models__ import ScriptListResponse, Script, SaveScriptRequest


@pytest.fixture
def config():
    return PhantombusterConfig(api_key="test_api_key")


@pytest.fixture
def client(config):
    return PhantombusterClient.get_instance(config)


@pytest.mark.asyncio
@respx.mock
async def test_fetch_all_scripts(client):
    """Tests fetching all scripts."""
    mock_response = {"data": [{"id": "s1", "name": "Script 1"}, {"id": "s2", "name": "Script 2"}]}
    route = respx.get(f"{client._base_url_v2}/scripts/fetch-all").mock(return_value=Response(200, json=mock_response))

    response = await client.scripts.fetch_all()

    assert route.called
    assert isinstance(response, ScriptListResponse)
    assert len(response.data) == 2


@pytest.mark.asyncio
@respx.mock
async def test_fetch_script(client):
    """Tests fetching a single script."""
    script_id = "s1"
    mock_response = {"id": script_id, "name": "Script 1"}
    route = respx.get(f"{client._base_url_v2}/scripts/fetch?id={script_id}").mock(return_value=Response(200, json=mock_response))

    response = await client.scripts.fetch(script_id)

    assert route.called
    assert isinstance(response, Script)
    assert response.id == script_id


@pytest.mark.asyncio
@respx.mock
async def test_save_script(client):
    """Tests saving a script."""
    script_id = "s3"
    mock_response = {"id": script_id, "name": "New Script", "code": "console.log('hello')"}
    route = respx.post(f"{client._base_url_v2}/scripts/save").mock(return_value=Response(200, json=mock_response))

    request_data = SaveScriptRequest(id=script_id, name="New Script", code="console.log('hello')")
    response = await client.scripts.save(request_data)

    assert route.called
    assert isinstance(response, Script)
    assert response.name == "New Script"

    await client.close()
