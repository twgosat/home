"""Technical indicators implemented on plain pandas, no TA-Lib needed.

All functions take/return ``pd.Series`` (or ``DataFrame``) aligned to the input index and
leave warm-up periods as NaN.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _rma(s: pd.Series, window: int) -> pd.Series:
    """Wilder's smoothing (RMA): seeded with the simple mean of the first ``window`` values,
    then ``(prev * (window - 1) + x) / window``. Matches TradingView / textbook RSI and ATR.

    Leading NaNs are skipped; a NaN later in the series carries the previous value forward.
    """
    vals = s.to_numpy(dtype=float)
    out = np.full(len(vals), np.nan)
    valid = np.flatnonzero(~np.isnan(vals))
    if len(valid) == 0 or len(vals) - valid[0] < window:
        return pd.Series(out, index=s.index)
    start = valid[0]
    seed_end = start + window
    out[seed_end - 1] = vals[start:seed_end].mean()
    for i in range(seed_end, len(vals)):
        x = vals[i]
        out[i] = out[i - 1] if np.isnan(x) else (out[i - 1] * (window - 1) + x) / window
    return pd.Series(out, index=s.index)


def sma(s: pd.Series, window: int) -> pd.Series:
    return s.rolling(window, min_periods=window).mean()


def ema(s: pd.Series, span: int) -> pd.Series:
    return s.ewm(span=span, adjust=False, min_periods=span).mean()


def rsi(close: pd.Series, window: int = 14) -> pd.Series:
    """Wilder's RSI (same seeding as TradingView). A flat series yields 50; a series with only gains yields 100."""
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    # delta[0] is NaN; keep NaN there so the Wilder seed starts at the first real change.
    gain, loss = gain.where(delta.notna()), loss.where(delta.notna())
    avg_gain, avg_loss = _rma(gain, window), _rma(loss, window)
    with np.errstate(divide="ignore", invalid="ignore"):
        rs = avg_gain / avg_loss
        out = 100 - 100 / (1 + rs)
    flat = (avg_gain == 0) & (avg_loss == 0)
    return out.mask(flat, 50.0)


def macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    line = ema(close, fast) - ema(close, slow)
    sig = line.ewm(span=signal, adjust=False, min_periods=signal).mean()
    return pd.DataFrame({"macd": line, "signal": sig, "hist": line - sig})


def bollinger(close: pd.Series, window: int = 20, k: float = 2.0) -> pd.DataFrame:
    mid = sma(close, window)
    std = close.rolling(window, min_periods=window).std(ddof=0)
    upper = mid + k * std
    lower = mid - k * std
    width = (upper - lower).replace(0, np.nan)
    return pd.DataFrame(
        {"mid": mid, "upper": upper, "lower": lower, "pct_b": (close - lower) / width}
    )


def atr(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> pd.Series:
    prev_close = close.shift(1)
    tr = pd.concat(
        [high - low, (high - prev_close).abs(), (low - prev_close).abs()], axis=1
    ).max(axis=1)
    return _rma(tr, window)


def volume_ratio(volume: pd.Series, window: int = 20) -> pd.Series:
    """Today's volume divided by the average of the *previous* ``window`` days."""
    base = volume.shift(1).rolling(window, min_periods=window).mean()
    return volume / base.replace(0, np.nan)


def max_drawdown(close: pd.Series) -> float:
    """Worst peak-to-trough decline as a negative fraction (-0.35 = -35%)."""
    if close.empty:
        return float("nan")
    return float((close / close.cummax() - 1).min())


def annualized_volatility(close: pd.Series, periods_per_year: int = 252) -> float:
    rets = close.pct_change().dropna()
    if len(rets) < 2:
        return float("nan")
    return float(rets.std(ddof=1) * np.sqrt(periods_per_year))
