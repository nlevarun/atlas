"""Groq provider adapter - FREE tier LLM (15 requests/min)."""

from typing import Any
from .provider import LLMProvider
import os
import httpx


class GroqProvider(LLMProvider):
    """
    Groq LLM provider implementation.

    FREE TIER: 15 requests/minute, 6000 requests/day
    Models: llama-3.1-70b-versatile, mixtral-8x7b, etc.
    Extremely fast inference.
    """

    def __init__(self, api_key: str, model: str = "llama-3.1-70b-versatile", cache: Any = None):
        """
        Initialize Groq provider.

        Args:
            api_key: Groq API key (free from https://console.groq.com)
            model: Model to use (default: llama-3.1-70b-versatile)
            cache: Optional LLMCache instance
        """
        self.api_key = api_key
        self.model = model
        self.cache = cache
        self.base_url = "https://api.groq.com/openai/v1"

    async def complete(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """Generate completion using Groq API (OpenAI-compatible)."""
        # Check cache
        if self.cache:
            cache_key = self.cache.make_key(
                prompt=str(messages),
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

        # Call Groq API
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    result = data["choices"][0]["message"]["content"]

                    # Cache result
                    if self.cache:
                        await self.cache.set(cache_key, result)

                    return result
                else:
                    # Fallback on error
                    return "Groq API error - using fallback synthesis"

            except Exception as e:
                # Fallback on exception
                return f"Groq error: {str(e)}"

    async def embed(self, text: str) -> list[float]:
        """Groq doesn't provide embeddings - use Hugging Face or local."""
        # Placeholder - would need separate embedding service
        return [0.0] * 768  # Standard BERT dimension

    def count_tokens(self, text: str) -> int:
        """Estimate token count."""
        # Rough estimate: 1 token ≈ 4 characters
        return len(text) // 4
