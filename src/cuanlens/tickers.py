"""Symbol normalisation: ``BBCA`` -> ``BBCA.JK``, ``BTC`` -> ``BTC-USD``."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from .errors import TickerError

Market = Literal["idx", "crypto"]

# Common crypto base symbols. Anything else can still be used as ``XXX-USD`` or with
# ``market="crypto"``; this set only powers auto-detection for bare symbols.
KNOWN_CRYPTO = frozenset(
    {"BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "DOGE", "AVAX", "DOT", "LINK", "TRX", "LTC", "MATIC"}
)

_IDX_RE = re.compile(r"^[A-Z]{4}$")
_CRYPTO_PAIR_RE = re.compile(r"^([A-Z0-9]{2,10})-(USD|USDT|IDR)$")


@dataclass(frozen=True)
class Instrument:
    """A resolved instrument.

    ``symbol`` is what humans type (``BBCA``), ``yahoo_symbol`` is what Yahoo Finance
    expects (``BBCA.JK``).
    """

    symbol: str
    market: Market
    yahoo_symbol: str

    @property
    def currency(self) -> str:
        return "IDR" if self.market == "idx" or self.yahoo_symbol.endswith("-IDR") else "USD"

    @property
    def periods_per_year(self) -> int:
        """Trading periods per year, used to annualise volatility."""
        return 252 if self.market == "idx" else 365


def resolve(symbol: str, market: Market | None = None) -> Instrument:
    """Turn user input into an :class:`Instrument`.

    Rules, in order:

    * ``market`` given explicitly wins (``"idx"`` or ``"crypto"``).
    * ``XXXX.JK`` -> IDX.
    * ``XXX-USD`` / ``XXX-USDT`` / ``XXX-IDR`` -> crypto.
    * A bare symbol in :data:`KNOWN_CRYPTO` -> crypto (``BTC`` -> ``BTC-USD``).
    * A bare 4-letter symbol -> IDX (all IDX tickers are four letters).

    Raises :class:`TickerError` when none of those match.
    """
    if not isinstance(symbol, str) or not symbol.strip():
        raise TickerError("Symbol must be a non-empty string.")
    raw = symbol.strip().upper()

    if market not in (None, "idx", "crypto"):
        raise TickerError(f"Unknown market {market!r}; use 'idx' or 'crypto'.")

    if raw.endswith(".JK"):
        base = raw[:-3]
        if market == "crypto" or not _IDX_RE.match(base):
            raise TickerError(f"{symbol!r} is not a valid IDX ticker.")
        return Instrument(base, "idx", raw)

    pair = _CRYPTO_PAIR_RE.match(raw)
    if pair:
        if market == "idx":
            raise TickerError(f"{symbol!r} looks like a crypto pair, not an IDX ticker.")
        return Instrument(pair.group(1), "crypto", raw)

    if market == "crypto" or (market is None and raw in KNOWN_CRYPTO):
        if not re.match(r"^[A-Z0-9]{2,10}$", raw):
            raise TickerError(f"{symbol!r} is not a valid crypto symbol.")
        return Instrument(raw, "crypto", f"{raw}-USD")

    if _IDX_RE.match(raw):
        return Instrument(raw, "idx", f"{raw}.JK")

    raise TickerError(
        f"Cannot infer market for {symbol!r}. IDX tickers are 4 letters (e.g. BBCA); "
        "for crypto use BTC, BTC-USD or pass market='crypto'."
    )
