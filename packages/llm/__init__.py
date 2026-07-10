"""Atlas LLM abstraction package - FREE options prioritized."""

from .provider import LLMProvider
from .cache import LLMCache

# Optional providers - only imported if API keys present
try:
    from .groq_adapter import GroqProvider
except ImportError:
    GroqProvider = None

__all__ = [
    "LLMProvider",
    "LLMCache",
    "GroqProvider",
]
