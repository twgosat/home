import pytest

from cuanlens.fundamentals import Thresholds, fundamental_signals, parse_fundamentals
from cuanlens.signals import score_from


def test_debt_to_equity_converted_from_percent():
    f = parse_fundamentals({"debtToEquity": 45.3})
    assert f.debt_to_equity == pytest.approx(0.453)


def test_dividend_yield_derived_from_rate_and_price():
    f = parse_fundamentals({"dividendRate": 200.0, "dividendYield": 9999}, price=5000.0)
    assert f.dividend_yield_pct == pytest.approx(4.0)  # ignores the ambiguous dividendYield field


def test_dividend_yield_fallback_to_trailing_fraction():
    f = parse_fundamentals({"trailingAnnualDividendYield": 0.035})
    assert f.dividend_yield_pct == pytest.approx(3.5)


def test_negative_pe_dropped_and_loss_flagged():
    f = parse_fundamentals({"trailingPE": -12.0, "trailingEps": -50.0})
    assert f.pe is None
    sigs = fundamental_signals(f)
    assert any(s.name == "Laba" and s.stance == "bearish" for s in sigs)


def test_garbage_values_are_ignored():
    f = parse_fundamentals({"trailingPE": "n/a", "priceToBook": float("nan"), "marketCap": True})
    assert f.pe is None and f.pbv is None and f.market_cap is None


def test_none_info_is_safe():
    f = parse_fundamentals(None)
    assert not f.has_enough_data


def test_bank_leverage_not_penalised():
    base = {"sector": "Financial Services", "debtToEquity": 900.0, "returnOnEquity": 0.2, "trailingPE": 15, "priceToBook": 3}
    sigs = fundamental_signals(parse_fundamentals(base))
    assert not any(s.name in {"DER", "Likuiditas"} for s in sigs)
    corp = dict(base, sector="Industrials")
    assert any(s.name == "DER" and s.stance == "bearish" for s in fundamental_signals(parse_fundamentals(corp)))


def test_healthy_company_scores_above_neutral_and_weak_below():
    healthy = parse_fundamentals(
        {"trailingPE": 8, "priceToBook": 0.9, "returnOnEquity": 0.2, "debtToEquity": 30,
         "profitMargins": 0.2, "revenueGrowth": 0.15, "earningsGrowth": 0.2}
    )
    weak = parse_fundamentals(
        {"trailingPE": 40, "priceToBook": 8, "returnOnEquity": 0.03, "debtToEquity": 300,
         "profitMargins": 0.01, "revenueGrowth": -0.1, "earningsGrowth": -0.2}
    )
    assert score_from(fundamental_signals(healthy)) > 70
    assert score_from(fundamental_signals(weak)) < 30


def test_decline_wording_has_no_double_negative():
    f = parse_fundamentals({"earningsGrowth": -0.08, "revenueGrowth": -0.05})
    details = " ".join(s.detail for s in fundamental_signals(f))
    assert "turun -" not in details and "menyusut -" not in details


def test_custom_thresholds_change_outcome():
    f = parse_fundamentals({"trailingPE": 18})
    default = fundamental_signals(f)[0]
    strict = fundamental_signals(f, Thresholds(pe_expensive=15))[0]
    assert default.stance == "neutral" and strict.stance == "bearish"
