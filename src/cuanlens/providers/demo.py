"""Offline demo provider with SYNTHETIC data.

Lets people try the pipeline (and the test-suite run) without network access or API keys.
The numbers are random-walk fiction: never use them for decisions.
"""

from __future__ import annotations

import zlib
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from ..models import NewsItem, RawData
from ..tickers import Instrument

DEMO_NOTICE = "DATA SINTETIS UNTUK DEMO - bukan data pasar sungguhan."


def synthetic_ohlcv(
    n: int = 260,
    *,
    start_price: float = 1000.0,
    drift: float = 0.0004,
    vol: float = 0.015,
    seed: int = 0,
    end: str | pd.Timestamp = "2026-10-09",
) -> pd.DataFrame:
    """Geometric random walk with plausible OHLC/volume, ending on business day ``end``."""
    rng = np.random.default_rng(seed)
    rets = rng.normal(drift, vol, n)
    close = start_price * np.exp(np.cumsum(rets))
    open_ = np.concatenate([[start_price], close[:-1]]) * (1 + rng.normal(0, vol / 4, n))
    spread = np.abs(rng.normal(0, vol / 2, n))
    high = np.maximum(open_, close) * (1 + spread)
    low = np.minimum(open_, close) * (1 - spread)
    volume = rng.lognormal(mean=15, sigma=0.35, size=n).round()
    idx = pd.bdate_range(end=pd.Timestamp(end), periods=n)
    return pd.DataFrame(
        {"Open": open_, "High": high, "Low": low, "Close": close, "Volume": volume}, index=idx
    )


class DemoProvider:
    """Deterministic fake market: the same symbol always yields the same data."""

    def fetch(self, instrument: Instrument, period: str = "1y") -> RawData:
        seed = zlib.crc32(instrument.symbol.encode())
        is_idx = instrument.market == "idx"
        history = synthetic_ohlcv(
            start_price=5000.0 if is_idx else 30000.0,
            drift=0.0006 if seed % 2 else -0.0001,
            vol=0.016 if is_idx else 0.03,
            seed=seed,
        )
        info = (
            {
                "longName": f"{instrument.symbol} (demo)",
                "sector": "Industrials",
                "industry": "Demo",
                "marketCap": 5e13,
                "trailingPE": 6.0 + seed % 25,
                "priceToBook": 0.8 + (seed % 40) / 10,
                "returnOnEquity": 0.05 + (seed % 20) / 100,
                "debtToEquity": 30 + seed % 200,
                "profitMargins": 0.02 + (seed % 20) / 100,
                "revenueGrowth": (seed % 30 - 8) / 100,
                "earningsGrowth": (seed % 40 - 12) / 100,
                "dividendRate": 120.0,
                "currentRatio": 0.9 + (seed % 15) / 10,
                "beta": 1.0,
            }
            if is_idx
            else {}
        )
        now = datetime.now(timezone.utc)
        news = [
            NewsItem(title=f"{DEMO_NOTICE} Laba {instrument.symbol} tumbuh pada kuartal terbaru", publisher="Demo", published=now),
            NewsItem(title=f"{DEMO_NOTICE} Analis menurunkan target harga {instrument.symbol}", publisher="Demo", published=now),
        ]
        return RawData(instrument=instrument, history=history, info=info, news=news, notes=[DEMO_NOTICE])
