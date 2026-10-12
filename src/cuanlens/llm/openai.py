from __future__ import annotations

import os

from ..errors import LLMError

DEFAULT_MODEL = "gpt-4o-mini"  # override with model= or CUANLENS_OPENAI_MODEL


class OpenAILLM:
    """OpenAI chat models (``pip install cuanlens[openai]``). Also works with any
    OpenAI-compatible endpoint via ``base_url`` (OpenRouter, Ollama, vLLM, ...)."""

    def __init__(
        self,
        model: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        temperature: float = 0.3,
    ) -> None:
        try:
            from openai import OpenAI
        except ImportError as e:
            raise LLMError("OpenAI support needs: pip install 'cuanlens[openai]'") from e
        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise LLMError("Set OPENAI_API_KEY (or pass api_key=...).")
        self.name = model or os.getenv("CUANLENS_OPENAI_MODEL") or DEFAULT_MODEL
        self.temperature = temperature
        self._client = OpenAI(api_key=key, base_url=base_url)

    def generate(self, system: str, prompt: str) -> str:
        try:
            resp = self._client.chat.completions.create(
                model=self.name,
                temperature=self.temperature,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
            )
        except Exception as e:
            raise LLMError(f"OpenAI request failed: {e}") from e
        text = (resp.choices[0].message.content or "").strip()
        if not text:
            raise LLMError("OpenAI returned an empty response.")
        return text
