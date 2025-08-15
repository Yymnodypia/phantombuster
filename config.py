"""
Configuration for the PhantomBuster SDK.
"""

from pydantic import BaseModel, Field

class PhantombusterConfig(BaseModel):
    """Configuration for the PhantomBuster API client."""

    api_key: str = Field(..., description="Your PhantomBuster API key.")
    base_url_v1: str = Field(
        default="https://api.phantombuster.com/api/v1",
        description="The base URL for the PhantomBuster API v1.",
    )
    base_url_v2: str = Field(
        default="https://api.phantombuster.com/api/v2",
        description="The base URL for the PhantomBuster API v2.",
    )