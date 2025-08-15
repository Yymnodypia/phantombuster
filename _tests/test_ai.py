import pytest
import respx
from httpx import Response

from ..client import PhantombusterClient
from ..config import PhantombusterConfig
from ..__global_models__ import AICompletionsResponse


@pytest.fixture
def config():
    return PhantombusterConfig(api_key="test_api_key")


@pytest.fixture
def client(config):
    return PhantombusterClient.get_instance(config)


@pytest.mark.asyncio
@respx.mock
async def test_ai_completions(client):
    """Tests the AI completions endpoint."""
    mock_response = {
        "completion": "This is a test completion.",
        "stop_reason": "stop_sequence",
        "stop": None
    }
    route = respx.post(f"{client._base_url_v2}/ai/completions").mock(return_value=Response(200, json=mock_response))

    response = await client.ai.completions(
        prompt="Test prompt",
        max_tokens_to_sample=50
    )

    assert route.called
    assert isinstance(response, AICompletionsResponse)
    assert response.completion == "This is a test completion."

    await client.close()
