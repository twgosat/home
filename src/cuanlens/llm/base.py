from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class LLM(Protocol):
    """Minimal text-in/text-out interface. Implement it to use any other model."""

    name: str

    def generate(self, system: str, prompt: str) -> str: ...
