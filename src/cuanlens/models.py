"""Plain data containers passed between pipeline stages."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

import pandas as pd

from .errors import DataError
from .tickers import Instrument

OHLCV_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


@dataclass
class NewsItem:
    title: str
    publisher: str = ""
    published: datetime | None = None
    url: str = ""
    summary: str = ""
    hint: str = "netral"  # filled by news.clean_news: positif / negatif / netral


@dataclass
class RawData:
    """What a provider returns for one instrument. No interpretation yet."""

    instrument: Instrument
    history: pd.DataFrame
    info: dict[str, Any] = field(default_factory=dict)
    news: list[NewsItem] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)  # provider-supplied data-quality caveats
    fetched_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


def normalize_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean a price history frame.

    Keeps only OHLCV columns, makes the index tz-naive, sorted and unique, and drops rows
    without a close. Raises :class:`DataError` if required columns are missing or nothing
    is left.
    """
    if df is None or len(df) == 0:
        raise DataError("Price history is empty.")
    missing = [c for c in OHLCV_COLUMNS if c not in df.columns]
    if missing:
        raise DataError(f"Price history is missing columns: {missing}")

    out = df[OHLCV_COLUMNS].copy()
    idx = pd.DatetimeIndex(out.index)
    if idx.tz is not None:
        idx = idx.tz_localize(None)
    out.index = idx.normalize()
    out = out[~out.index.duplicated(keep="last")].sort_index()
    out = out.apply(pd.to_numeric, errors="coerce")
    out = out.dropna(subset=["Close"])
    out["Volume"] = out["Volume"].fillna(0)
    if out.empty:
        raise DataError("Price history has no valid closing prices.")
    return out
