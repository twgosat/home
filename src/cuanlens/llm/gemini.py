from __future__ import annotations

import os

from ..errors import LLMError

DEFAULT_MODEL = "gemini-2.5-flash"  # override with model= or CUANLENS_GEMINI_MODEL


class GeminiLLM:
    """Google Gemini via the ``google-genai`` SDK (``pip install cuanlens[gemini]``)."""

    def __init__(
        self,
        model: str | None = None,
        api_key: str | None = None,
        temperature: float = 0.3,
    ) -> None:
        try:
            from google import genai
        except ImportError as e:
            raise LLMError("Gemini support needs: pip install 'cuanlens[gemini]'") from e
        key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not key:
            raise LLMError("Set GEMINI_API_KEY (or pass api_key=...).")
        self.name = model or os.getenv("CUANLENS_GEMINI_MODEL") or DEFAULT_MODEL
        self.temperature = temperature
        self._client = genai.Client(api_key=key)

    def generate(self, system: str, prompt: str) -> str:
        from google.genai import types

        try:
            resp = self._client.models.generate_content(
                model=self.name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system, temperature=self.temperature
                ),
            )
        except Exception as e:
            raise LLMError(f"Gemini request failed: {str(e)[:240]}") from e
        text = (resp.text or "").strip()
        if not text:
            raise LLMError("Gemini returned an empty response (possibly blocked by safety filters).")
        return text
