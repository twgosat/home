import pytest

from cuanlens.errors import TickerError
from cuanlens.tickers import resolve


@pytest.mark.parametrize(
    "raw,symbol,market,yahoo",
    [
        ("bbca", "BBCA", "idx", "BBCA.JK"),
        (" BBRI.JK ", "BBRI", "idx", "BBRI.JK"),
        ("BTC", "BTC", "crypto", "BTC-USD"),
        ("eth-usd", "ETH", "crypto", "ETH-USD"),
        ("SOL-IDR", "SOL", "crypto", "SOL-IDR"),
    ],
)
def test_resolve(raw, symbol, market, yahoo):
    i = resolve(raw)
    assert (i.symbol, i.market, i.yahoo_symbol) == (symbol, market, yahoo)


def test_explicit_market_overrides_detection():
    assert resolve("PEPE", market="crypto").yahoo_symbol == "PEPE-USD"


def test_currency_and_annualisation():
    assert resolve("BBCA").currency == "IDR" and resolve("BBCA").periods_per_year == 252
    assert resolve("BTC").currency == "USD" and resolve("BTC").periods_per_year == 365
    assert resolve("BTC-IDR").currency == "IDR"


@pytest.mark.parametrize("bad", ["", "  ", "AB", "TOOLONGSYM", "BCA1", "BTC.JK"])
def test_bad_symbols(bad):
    with pytest.raises(TickerError):
        resolve(bad)


def test_conflicting_market_rejected():
    with pytest.raises(TickerError):
        resolve("BTC-USD", market="idx")
    with pytest.raises(TickerError):
        resolve("BBCA.JK", market="crypto")
