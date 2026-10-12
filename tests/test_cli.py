import json

from cuanlens.cli import main


def test_analyze_demo(capsys):
    assert main(["analyze", "BBCA", "--demo"]) == 0
    assert "## Ringkasan" in capsys.readouterr().out


def test_analyze_json(capsys):
    assert main(["analyze", "BTC", "--demo", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["market"] == "crypto"


def test_prompt_mode_does_not_need_api_key(capsys, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    assert main(["analyze", "BBCA", "--demo", "--llm", "gemini", "--prompt"]) == 0
    assert "INSTRUMEN: BBCA" in capsys.readouterr().out


def test_screen_demo(capsys):
    assert main(["screen", "BBCA", "BBRI", "--demo"]) == 0
    out = capsys.readouterr().out
    assert "BBCA" in out and "overall_score" in out


def test_screen_requires_symbols(capsys):
    assert main(["screen", "--demo"]) == 2


def test_bad_ticker_gives_clean_error(capsys):
    assert main(["analyze", "??", "--demo"]) == 1
    assert "Error" in capsys.readouterr().err


def test_missing_api_key_gives_clean_error(capsys, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    # either SDK missing or key missing -> both are LLMError -> exit code 1, no traceback
    assert main(["analyze", "BBCA", "--demo", "--llm", "openai"]) == 1
    assert "Error" in capsys.readouterr().err
