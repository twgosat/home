"""Adapter tests run against the REAL SDK objects with the network call stubbed out."""

from types import SimpleNamespace

import pytest

from cuanlens.errors import LLMError
from cuanlens.llm import get_llm


def test_unknown_backend():
    with pytest.raises(LLMError):
        get_llm("claude-but-not-implemented")


def test_gemini_requires_key(monkeypatch):
    pytest.importorskip("google.genai")
    for k in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    with pytest.raises(LLMError, match="GEMINI_API_KEY"):
        get_llm("gemini")


def test_gemini_request_shape_and_errors(monkeypatch):
    pytest.importorskip("google.genai")
    monkeypatch.setenv("GEMINI_API_KEY", "fake")
    llm = get_llm("gemini", model="m-1")
    seen = {}

    def ok(model, contents, config):
        seen.update(model=model, contents=contents, system=config.system_instruction, temp=config.temperature)
        return SimpleNamespace(text="  halo  ")

    llm._client = SimpleNamespace(models=SimpleNamespace(generate_content=ok))
    assert llm.generate("SYS", "PROMPT") == "halo"
    assert seen == {"model": "m-1", "contents": "PROMPT", "system": "SYS", "temp": 0.3}

    def boom(**_):
        raise RuntimeError("429")

    llm._client = SimpleNamespace(models=SimpleNamespace(generate_content=boom))
    with pytest.raises(LLMError, match="429"):
        llm.generate("a", "b")

    llm._client = SimpleNamespace(models=SimpleNamespace(generate_content=lambda **_: SimpleNamespace(text=None)))
    with pytest.raises(LLMError, match="empty"):
        llm.generate("a", "b")


def test_openai_requires_key(monkeypatch):
    pytest.importorskip("openai")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(LLMError, match="OPENAI_API_KEY"):
        get_llm("openai")


def test_openai_request_shape_and_errors(monkeypatch):
    pytest.importorskip("openai")
    monkeypatch.setenv("OPENAI_API_KEY", "fake")
    monkeypatch.setenv("CUANLENS_OPENAI_MODEL", "from-env")
    llm = get_llm("openai")
    assert llm.name == "from-env"
    captured = {}

    def create(**kw):
        captured.update(kw)
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=" halo "))])

    llm._client.chat.completions.create = create
    assert llm.generate("SYS", "PROMPT") == "halo"
    assert [m["role"] for m in captured["messages"]] == ["system", "user"]

    def boom(**_):
        raise RuntimeError("rate limited")

    llm._client.chat.completions.create = boom
    with pytest.raises(LLMError, match="rate limited"):
        llm.generate("a", "b")
