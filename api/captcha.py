from __future__ import annotations

from typing import TYPE_CHECKING

from ..__global_models__ import (
    HCaptchaRequest,
    RecaptchaRequest,
    CaptchaResponse,
)

if TYPE_CHECKING:
    from ..client import PhantombusterClient


class CaptchaAPI:
    """
    A class for interacting with the Captcha API.
    """

    def __init__(self, client: PhantombusterClient):
        self._client = client

    async def solve_hcaptcha(self, sitekey: str, pageurl: str) -> CaptchaResponse:
        """Solves an hCaptcha challenge.

        Args:
            sitekey: The hCaptcha site key.
            pageurl: The URL of the page with the hCaptcha.

        Returns:
            The captcha solution.
        """
        request_data = HCaptchaRequest(sitekey=sitekey, pageurl=pageurl)
        response = await self._client._request(
            method="POST",
            url="/hcaptcha",
            json=request_data.model_dump(),
        )
        return CaptchaResponse.model_validate(response.json())

    async def solve_recaptcha(self, sitekey: str, pageurl: str) -> CaptchaResponse:
        """Solves a reCAPTCHA challenge.

        Args:
            sitekey: The reCAPTCHA site key.
            pageurl: The URL of the page with the reCAPTCHA.

        Returns:
            The captcha solution.
        """
        request_data = RecaptchaRequest(sitekey=sitekey, pageurl=pageurl)
        response = await self._client._request(
            method="POST",
            url="/recaptcha",
            json=request_data.model_dump(),
        )
        return CaptchaResponse.model_validate(response.json())
