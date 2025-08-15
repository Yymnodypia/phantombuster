import pytest
import respx
from httpx import Response

from ..client import PhantombusterClient
from ..config import PhantombusterConfig
from ..__global_models__ import BranchListResponse, BranchDiffResponse, Branch


@pytest.fixture
def config():
    return PhantombusterConfig(api_key="test_api_key")


@pytest.fixture
def client(config):
    return PhantombusterClient.get_instance(config)


@pytest.mark.asyncio
@respx.mock
async def test_fetch_all_branches(client):
    """Tests fetching all branches for a script."""
    script_id = "sid123"
    mock_response = {"data": [{"name": "main", "scriptId": script_id}, {"name": "develop", "scriptId": script_id}]}
    route = respx.get(f"{client._base_url_v2}/scripts/branches?scriptId={script_id}").mock(return_value=Response(200, json=mock_response))

    response = await client.branches.fetch_all(script_id)

    assert route.called
    assert isinstance(response, BranchListResponse)
    assert len(response.data) == 2


@pytest.mark.asyncio
@respx.mock
async def test_diff_branch(client):
    """Tests getting the diff for a branch."""
    script_id = "sid123"
    branch_name = "develop"
    mock_response = {"data": {"diff": "+ new line"}}
    route = respx.get(f"{client._base_url_v2}/scripts/branch/diff?scriptId={script_id}&branch={branch_name}").mock(return_value=Response(200, json=mock_response))

    response = await client.branches.diff(script_id, branch_name)

    assert route.called
    assert isinstance(response, BranchDiffResponse)
    assert response.data.diff == "+ new line"


@pytest.mark.asyncio
@respx.mock
async def test_create_branch(client):
    """Tests creating a new branch."""
    script_id = "sid123"
    branch_name = "feature-branch"
    mock_response = {"name": branch_name, "scriptId": script_id}
    route = respx.post(f"{client._base_url_v2}/scripts/branch/create").mock(return_value=Response(200, json=mock_response))

    response = await client.branches.create(script_id, branch_name)

    assert route.called
    assert isinstance(response, Branch)
    assert response.name == branch_name

    await client.close()
