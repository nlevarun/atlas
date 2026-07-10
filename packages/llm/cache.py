"""Redis cache wrapper for LLM responses."""

import hashlib
import json
from typing import Any


class LLMCache:
    """Redis-backed cache for LLM completions."""

    def __init__(self, redis_client: Any):
        """
        Initialize cache with Redis client.

        Args:
            redis_client: redis.asyncio.Redis instance
        """
        self.client = redis_client

    async def get(self, key: str) -> str | None:
        """
        Get cached value.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        value = await self.client.get(key)
        return value.decode() if value else None

    async def set(self, key: str, value: str, ttl_seconds: int = 3600):
        """
        Set cached value with TTL.

        Args:
            key: Cache key
            value: Value to cache
            ttl_seconds: Time to live in seconds (default 1 hour)
        """
        await self.client.setex(key, ttl_seconds, value)

    @staticmethod
    def make_key(prompt: str, model: str, **params) -> str:
        """
        Generate cache key from prompt and parameters.

        Args:
            prompt: The prompt text
            model: Model identifier
            **params: Additional parameters to include in key

        Returns:
            Cache key (hash of inputs)
        """
        # Include all parameters in cache key
        key_data = {
            "model": model,
            "prompt": prompt,
            **params
        }
        data_str = json.dumps(key_data, sort_keys=True)
        hash_digest = hashlib.sha256(data_str.encode()).hexdigest()
        return f"llm:{model}:{hash_digest[:16]}"
