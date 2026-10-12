from datetime import date

import pandas as pd
import pytest

from cuanlens.cli import main
from cuanlens.doctor import FAIL, PASS, WARN, check_symbol, exit_code, format_report, llm_checks, run_doctor
from cuanlens.errors import DataError
from cuanlens.models import RawData
from cuanlens.providers import DemoProvider, YahooProvider
from cuanlens.providers.demo import synthetic_ohlcv
from cuanlens.tickers import resolve

TODAY = date(2026, 10, 12)


def statuses(checks):
    return {c.name: c.status for c in checks}


# ---- doctor -------------------------------------------------------------------------------

def test_doctor_all_green_with_demo_data():
    checks = run_doctor(DemoProvider(), ("BBCA", "BTC"), env={"GEMINI_API_KEY": "x"}, today=TODAY)
    st = statuses(checks)
    assert st["Harga BBCA"] == PASS and st["Fundamental BBCA"] == PASS and st["Harga BTC"] == PASS
    assert "Fundamental BTC" not in st  # crypto has none, and that is not a failure
    assert exit_code(checks) == 0
    assert "Berjalan" in format_report(checks) or "Semua beres" in format_report(checks)


def test_doctor_reports_fetch_failure_with_actionable_hint():
    class Down:
        def fetch(self, instrument, period="1y"):
            raise DataError("CONNECT tunnel failed, response 403")

    checks = check_symbol(Down(), "BBCA", today=TODAY)
    assert checks[0].status == FAIL and "yahoo.com" in checks[0].hint
    assert exit_code(checks) == 1
    assert "--demo" in format_report(checks)


def test_doctor_flags_stale_data_and_thin_fundamentals():
    class Stale:
        def fetch(self, instrument, period="1y"):
            return RawData(instrument=instrument, history=synthetic_ohlcv(120, end="2026-08-01"), info={"longName": "X"})

    st = statuses(check_symbol(Stale(), "BBCA", today=TODAY))
    assert st["Harga BBCA"] == WARN and st["Fundamental BBCA"] == WARN and st["Berita BBCA"] == WARN


def test_doctor_bad_symbol_is_a_failure_not_a_crash():
    checks = check_symbol(DemoProvider(), "??", today=TODAY)
    assert checks[0].status == FAIL


def test_llm_checks_never_leak_keys():
    checks = llm_checks({"OPENAI_API_KEY": "sk-secret-123"})
    assert "sk-secret-123" not in format_report(checks)
    assert any(c.name == "LLM OpenAI" for c in checks)


def test_doctor_cli_exit_codes(monkeypatch, capsys):
    import cuanlens.cli as cli

    monkeypatch.setattr(cli, "run_doctor", lambda symbols: run_doctor(DemoProvider(), symbols, env={}, today=TODAY))
    assert main(["doctor", "BBCA"]) == 0
    assert "[ OK ]" in capsys.readouterr().out


# ---- YahooProvider against a stand-in that mimics real yfinance output ---------------------

def _yahoo_like_history():
    df = synthetic_ohlcv(260)
    df.index = df.index.tz_localize("Asia/Jakarta")
    df["Dividends"] = 0.0
    df["Stock Splits"] = 0.0
    return df


class FakeTicker:
    def __init__(self, symbol):
        self.symbol = symbol

    def history(self, period, auto_adjust):
        assert auto_adjust is False  # we want raw closes, matching broker apps
        return _yahoo_like_history()

    @property
    def info(self):
        return {"longName": "PT Bank Central Asia Tbk", "sector": "Financial Services", "trailingPE": 22.0,
                "priceToBook": 4.1, "returnOnEquity": 0.21, "profitMargins": 0.4, "dividendRate": 280.0}

    @property
    def news(self):
        return [{"id": "1", "content": {"title": "BBCA cetak laba rekor", "provider": {"displayName": "CNBC"},
                                        "pubDate": "2026-10-10T03:00:00Z", "canonicalUrl": {"url": "https://x/1"}}}]


def test_yahoo_provider_end_to_end_with_realistic_shapes(monkeypatch):
    import yfinance

    monkeypatch.setattr(yfinance, "Ticker", FakeTicker)
    raw = YahooProvider().fetch(resolve("BBCA"))
    assert list(raw.history.columns) == ["Open", "High", "Low", "Close", "Volume"]
    assert raw.history.index.tz is None
    assert raw.info["longName"].startswith("PT Bank") and raw.news[0].publisher == "CNBC"


def test_yahoo_provider_survives_broken_info_and_news(monkeypatch):
    import yfinance

    class Flaky(FakeTicker):
        @property
        def info(self):
            raise RuntimeError("429 Too Many Requests")

        @property
        def news(self):
            raise RuntimeError("down")

    monkeypatch.setattr(yfinance, "Ticker", Flaky)
    raw = YahooProvider().fetch(resolve("BBCA"))
    assert raw.info == {} and raw.news == [] and len(raw.history) > 200


def test_yahoo_provider_empty_history_gives_helpful_error(monkeypatch):
    import yfinance

    class Empty(FakeTicker):
        def history(self, period, auto_adjust):
            return pd.DataFrame()

    monkeypatch.setattr(yfinance, "Ticker", Empty)
    with pytest.raises(DataError, match="BBCA.JK"):
        YahooProvider().fetch(resolve("BBCA"))


def test_yahoo_provider_wraps_network_errors(monkeypatch):
    import yfinance

    class Offline(FakeTicker):
        def history(self, period, auto_adjust):
            raise ConnectionError("CONNECT tunnel failed")

    monkeypatch.setattr(yfinance, "Ticker", Offline)
    with pytest.raises(DataError, match="tunnel"):
        YahooProvider().fetch(resolve("BBCA"))


def test_full_pipeline_through_yahoo_provider(monkeypatch):
    import yfinance

    from cuanlens import analyze

    monkeypatch.setattr(yfinance, "Ticker", FakeTicker)
    res = analyze("BBCA", provider=YahooProvider())
    b = res.brief
    assert b.fundamentals.is_financial and b.fundamentals.name.startswith("PT Bank")
    assert b.fundamentals.dividend_yield_pct == pytest.approx(280.0 / b.technical.close * 100)
    assert any("keuangan" in n for n in b.notes)
    assert "BBCA cetak laba rekor" in res.narrative
