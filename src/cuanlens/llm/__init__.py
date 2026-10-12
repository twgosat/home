from __future__ import annotations

from ..errors import LLMError
from .base import LLM


def get_llm(name: str, **kwargs) -> LLM:
    """Factory: ``get_llm("gemini")`` or ``get_llm("openai", model="gpt-4o")``.

    Backends are imported lazily so the optional SDKs are only needed if you use them.
    """
    key = name.lower()
    if key == "gemini":
        from .gemini import GeminiLLM

        return GeminiLLM(**kwargs)
    if key == "openai":
        from .openai import OpenAILLM

        return OpenAILLM(**kwargs)
    raise LLMError(f"Unknown LLM backend {name!r}; choose 'gemini' or 'openai'.")


__all__ = ["LLM", "get_llm"]
