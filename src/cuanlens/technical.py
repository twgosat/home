"""OHLCV -> :class:`TechnicalSnapshot` + technical :class:`Signal` list."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass

import pandas as pd

from . import indicators as ind
from .errors import DataError
from .formatting import num, pct
from .signals import Signal

MIN_BARS = 30  # below this we refuse to compute anything meaningful

# bars back for "change over X" figures
_LOOKBACKS = {"1d": 1, "5d": 5, "1m": 21, "3m": 63, "6m": 126, "1y": 252}


@dataclass
class TechnicalSnapshot:
    n_bars: int
    close: float
    change_pct: dict[str, float | None]  # keys: 1d 5d 1m 3m 6m 1y
    sma20: float | None
    sma50: float | None
    sma200: float | None
    rsi14: float | None
    macd: float | None
    macd_signal: float | None
    macd_hist: float | None
    bb_pct_b: float | None
    atr_pct: float | None
    volume_ratio: float | None
    high_52w: float
    low_52w: float
    pct_from_high: float
    pct_from_low: float
    max_drawdown_pct: float | None
    volatility_pct: float | None
    trend: str  # uptrend / downtrend / sideways
    ma_cross: str | None  # golden / death / None (recent SMA50 vs SMA200 or SMA20 vs SMA50)
    macd_cross: str | None  # up / down / None

    def to_dict(self) -> dict:
        return asdict(self)


def _last(s: pd.Series) -> float | None:
    if s is None or s.empty:
        return None
    v = s.iloc[-1]
    return None if pd.isna(v) else float(v)


def _clean(x: float | None) -> float | None:
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else x


def _recent_cross(a: pd.Series, b: pd.Series, lookback: int) -> str | None:
    """'up' if ``a`` is above ``b`` now but was at/below within ``lookback`` bars; 'down' mirror."""
    d = (a - b).dropna().tail(lookback + 1)
    if len(d) < 2:
        return None
    if d.iloc[-1] > 0 and (d <= 0).any():
        return "up"
    if d.iloc[-1] < 0 and (d >= 0).any():
        return "down"
    return None


def compute_technical(ohlcv: pd.DataFrame, periods_per_year: int = 252) -> TechnicalSnapshot:
    """Compute the snapshot from a *normalised* OHLCV frame (see ``models.normalize_ohlcv``)."""
    if len(ohlcv) < MIN_BARS:
        raise DataError(f"Need at least {MIN_BARS} price bars, got {len(ohlcv)}.")

    close, high, low, vol = ohlcv["Close"], ohlcv["High"], ohlcv["Low"], ohlcv["Volume"]
    last = float(close.iloc[-1])

    changes: dict[str, float | None] = {}
    for key, n in _LOOKBACKS.items():
        changes[key] = (
            float((last / close.iloc[-1 - n] - 1) * 100)
            if len(close) > n and close.iloc[-1 - n] != 0
            else None
        )

    s20, s50, s200 = ind.sma(close, 20), ind.sma(close, 50), ind.sma(close, 200)
    m = ind.macd(close)
    bb = ind.bollinger(close)
    atr = _last(ind.atr(high, low, close))

    window = close.tail(252)
    hi, lo = float(window.max()), float(window.min())

    # Trend: prefer the long-term stack; fall back to short-term when <200 bars exist.
    v20, v50, v200 = _last(s20), _last(s50), _last(s200)
    if v200 is not None and v50 is not None:
        up, down = last > v50 > v200, last < v50 < v200
        cross_pair = (s50, s200)
    else:
        up = v50 is not None and last > v50 and v20 is not None and v20 > v50
        down = v50 is not None and last < v50 and v20 is not None and v20 < v50
        cross_pair = (s20, s50)
    trend = "uptrend" if up else "downtrend" if down else "sideways"
    cross = _recent_cross(*cross_pair, lookback=20)

    return TechnicalSnapshot(
        n_bars=len(ohlcv),
        close=last,
        change_pct=changes,
        sma20=v20,
        sma50=v50,
        sma200=v200,
        rsi14=_last(ind.rsi(close)),
        macd=_last(m["macd"]),
        macd_signal=_last(m["signal"]),
        macd_hist=_last(m["hist"]),
        bb_pct_b=_last(bb["pct_b"]),
        atr_pct=(atr / last * 100) if atr is not None and last else None,
        volume_ratio=_clean(_last(ind.volume_ratio(vol))),
        high_52w=hi,
        low_52w=lo,
        pct_from_high=(last / hi - 1) * 100 if hi else 0.0,
        pct_from_low=(last / lo - 1) * 100 if lo else 0.0,
        max_drawdown_pct=_clean(ind.max_drawdown(window) * 100),
        volatility_pct=_clean(ind.annualized_volatility(close.tail(252), periods_per_year) * 100),
        trend=trend,
        ma_cross={"up": "golden", "down": "death"}.get(cross) if cross else None,
        macd_cross=_recent_cross(m["macd"], m["signal"], lookback=3),
    )


def technical_signals(t: TechnicalSnapshot) -> list[Signal]:
    """Explainable rules over a snapshot. Each rule adds/subtracts a few points."""
    out: list[Signal] = []

    if t.trend == "uptrend":
        out.append(Signal("Tren", "bullish", "Harga di atas rata-rata jangka menengah dan panjang (tren naik).", 15))
    elif t.trend == "downtrend":
        out.append(Signal("Tren", "bearish", "Harga di bawah rata-rata jangka menengah dan panjang (tren turun).", -15))
    else:
        out.append(Signal("Tren", "neutral", "Harga bergerak campuran terhadap rata-rata bergerak (sideways).", 0))

    if t.ma_cross == "golden":
        out.append(Signal("Persilangan MA", "bullish", "Rata-rata jangka pendek baru memotong ke atas jangka panjang (golden cross).", 8))
    elif t.ma_cross == "death":
        out.append(Signal("Persilangan MA", "bearish", "Rata-rata jangka pendek baru memotong ke bawah jangka panjang (death cross).", -8))

    if t.rsi14 is not None:
        if t.rsi14 >= 70:
            out.append(Signal("RSI", "bearish", f"RSI {num(t.rsi14, 1)} (jenuh beli): rawan koreksi jangka pendek.", -5))
        elif t.rsi14 <= 30:
            out.append(Signal("RSI", "bullish", f"RSI {num(t.rsi14, 1)} (jenuh jual): berpotensi memantul, tapi bisa terus turun.", 5))
        else:
            out.append(Signal("RSI", "neutral", f"RSI {num(t.rsi14, 1)} (zona wajar).", 0))

    if t.macd_hist is not None:
        if t.macd_hist > 0:
            out.append(Signal("MACD", "bullish", "Momentum MACD di atas garis sinyal.", 5))
        else:
            out.append(Signal("MACD", "bearish", "Momentum MACD di bawah garis sinyal.", -5))
    if t.macd_cross == "up":
        out.append(Signal("MACD cross", "bullish", "MACD baru memotong ke atas garis sinyal.", 5))
    elif t.macd_cross == "down":
        out.append(Signal("MACD cross", "bearish", "MACD baru memotong ke bawah garis sinyal.", -5))

    if t.bb_pct_b is not None:
        if t.bb_pct_b > 1:
            out.append(Signal("Bollinger", "bearish", "Harga menembus band atas: bergerak ekstrem, rawan balik arah.", -3))
        elif t.bb_pct_b < 0:
            out.append(Signal("Bollinger", "bullish", "Harga menembus band bawah: tekanan jual ekstrem, rawan memantul.", 3))

    if t.volume_ratio is not None and t.volume_ratio >= 2:
        up_day = (t.change_pct.get("1d") or 0) >= 0
        out.append(
            Signal(
                "Volume",
                "bullish" if up_day else "bearish",
                f"Volume {num(t.volume_ratio, 1)}x rata-rata 20 hari, disertai harga "
                + ("naik." if up_day else "turun."),
                4 if up_day else -4,
            )
        )

    if t.pct_from_high >= -5:
        out.append(Signal("Posisi 52 minggu", "bullish", f"Harga dekat puncak 52 minggu ({pct(t.pct_from_high, 1, True)}).", 4))
    elif t.pct_from_low <= 10:
        out.append(Signal("Posisi 52 minggu", "bearish", f"Harga dekat dasar 52 minggu ({pct(t.pct_from_low, 1, True)} dari low).", -4))

    return out
