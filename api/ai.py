from __future__ import annotations

from typing import TYPE_CHECKING

from ..__global_models__ import (
    AICompletionsRequest,
    AICompletionsResponse,
)

if TYPE_CHECKING:
    from ..client import PhantombusterClient


class AIAPI:
    """
    A class for interacting with the AI API.
    """

    def __init__(self, client: PhantombusterClient):
        self._client = client

    async def completions(
        self,
        prompt: str,
        max_tokens_to_sample: int,
        temperature: float | None = None,
        top_p: float | None = None,
        top_k: int | None = None,
        stop_sequences: list[str] | None = None,
    ) -> AICompletionsResponse:
        """Get a completion from the AI.

        Args:
            prompt: The prompt to get a completion for.
            max_tokens_to_sample: The maximum number of tokens to sample.
            temperature: The temperature to use for sampling.
            top_p: The top_p to use for sampling.
            top_k: The top_k to use for sampling.
            stop_sequences: The stop sequences to use for sampling.

        Returns:
            The AI completion.
        """
        request_data = AICompletionsRequest(
            prompt=prompt,
            max_tokens_to_sample=max_tokens_to_sample,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            stop_sequences=stop_sequences,
        )
        response = await self._client._request(
            method="POST",
            url="/ai/completions",
            json=request_data.model_dump(exclude_none=True),
        )
        return AICompletionsResponse.model_validate(response.json())
