"""
Main client for the PhantomBuster SDK.
"""

import httpx
from threading import Lock
from typing import Any, Dict, Optional

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from aiolimiter import AsyncLimiter

from .config import PhantombusterConfig
from .api.branches import BranchesAPI
from .api.scripts import ScriptsAPI
from .api.orgs import OrgsAPI
from .api.containers import ContainersAPI
from .api.agents import AgentsAPI
from .api.org_storage import OrgStorageAPI
from .api.identities import IdentitiesAPI
from .api.brightdata import BrightDataAPI
from .api.location import LocationAPI
from .api.captcha import CaptchaAPI
from .api.ai import AIAPI
from .api.v1 import V1API
from .__global_exceptions__ import (
    PhantomBusterAPIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServerError,
)

class PhantombusterClient:
    """Asynchronous client for interacting with the PhantomBuster API."""

    _instance = None
    _lock = Lock()

    def __new__(cls, config: PhantombusterConfig | None = None):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: PhantombusterConfig | None = None):
        if not hasattr(self, '_initialized'):
            if config is None:
                raise ValueError("Configuration must be provided for the first client initialization.")
            self.config = config
            self._base_url_v1 = self.config.base_url_v1
            self._base_url_v2 = self.config.base_url_v2
            self._client = httpx.AsyncClient(
                headers={
                    "X-Phantombuster-Key-1": self.config.api_key,
                    "Content-Type": "application/json",
                },
                timeout=30.0,
            )
            self._limiter = AsyncLimiter(10, 1)  # 10 requests per second
            self._branches_api = BranchesAPI(self)
            self._scripts_api = ScriptsAPI(self)
            self._orgs_api = OrgsAPI(self)
            self._containers_api = ContainersAPI(self)
            self._agents_api = AgentsAPI(self)
            self._org_storage_api = OrgStorageAPI(self)
            self._identities_api = IdentitiesAPI(self)
            self._brightdata_api = BrightDataAPI(self)
            self._location_api = LocationAPI(self)
            self._captcha_api = CaptchaAPI(self)
            self._ai_api = AIAPI(self)
            self._v1_api = V1API(self)
            self._initialized = True

    @classmethod
    def get_instance(cls, config: PhantombusterConfig | None = None) -> 'PhantombusterClient':
        """Get the singleton instance of the client."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(config)
        return cls._instance

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError, ServerError)),
    )
    async def _request(
        self, method: str, url: str, api_version: str = "v2", **kwargs: Any
    ) -> httpx.Response:
        """Make an async request with error handling and retry logic."""
        base_url = self._base_url_v1 if api_version == "v1" else self._base_url_v2
        async with self._limiter:
            try:
                full_url = f"{base_url}{url}"
                response = await self._client.request(method, full_url, **kwargs)
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                message = f"HTTP error {status_code}: {e.response.text}"
                if status_code == 401:
                    raise AuthenticationError(message, status_code)
                if status_code == 404:
                    raise NotFoundError(message, status_code)
                if status_code == 429:
                    raise RateLimitError(message, status_code)
                if 500 <= status_code < 600:
                    raise ServerError(message, status_code)
                raise PhantomBusterAPIError(message, status_code)
            except httpx.RequestError as e:
                raise PhantomBusterAPIError(f"Request error: {e}")

    async def close(self):
        """Close the underlying HTTP client."""
        await self._client.aclose()

    @property
    def branches(self) -> BranchesAPI:
        return self._branches_api

    @property
    def scripts(self) -> ScriptsAPI:
        return self._scripts_api

    @property
    def orgs(self) -> OrgsAPI:
        return self._orgs_api

    @property
    def containers(self) -> ContainersAPI:
        return self._containers_api

    @property
    def agents(self) -> AgentsAPI:
        return self._agents_api

    @property
    def org_storage(self) -> OrgStorageAPI:
        return self._org_storage_api

    @property
    def identities(self) -> IdentitiesAPI:
        return self._identities_api

    @property
    def brightdata(self) -> BrightDataAPI:
        return self._brightdata_api

    @property
    def location(self) -> LocationAPI:
        return self._location_api

    @property
    def captcha(self) -> CaptchaAPI:
        return self._captcha_api

    @property
    def ai(self) -> AIAPI:
        return self._ai_api

    @property
    def v1(self) -> V1API:
        return self._v1_api
