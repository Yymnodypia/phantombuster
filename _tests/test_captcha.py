import pytest
import respx
from httpx import Response

from ..client import PhantombusterClient
from ..config import PhantombusterConfig
from ..__global_models__ import HCaptchaRequest, RecaptchaRequest, CaptchaResponse


@pytest.fixture
def config():
    return PhantombusterConfig(api_key="test_api_key")


@pytest.fixture
def client(config):
    return PhantombusterClient.get_instance(config)


@pytest.mark.asyncio
@respx.mock
async def test_solve_hcaptcha(client):
    """Tests solving an hCaptcha."""
    mock_response = {"token": "hcaptcha-token", "useragent": "test-agent"}
    route = respx.post(f"{client._base_url_v2}/hcaptcha").mock(return_value=Response(200, json=mock_response))

    request_data = HCaptchaRequest(website="example.com", website_key="key123")
    response = await client.captcha.solve_hcaptcha(request_data)

    assert route.called
    assert isinstance(response, CaptchaResponse)
    assert response.token == "hcaptcha-token"


@pytest.mark.asyncio
@respx.mock
async def test_solve_recaptcha(client):
    """Tests solving a reCAPTCHA."""
    mock_response = {"token": "recaptcha-token", "useragent": "test-agent"}
    route = respx.post(f"{client._base_url_v2}/recaptcha").mock(return_value=Response(200, json=mock_response))

    request_data = RecaptchaRequest(website="example.com", website_key="key456")
    response = await client.captcha.solve_recaptcha(request_data)

    assert route.called
    assert isinstance(response, CaptchaResponse)
    assert response.token == "recaptcha-token"

    await client.close()
