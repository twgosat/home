from __future__ import annotations

import pandas as pd
import pytest

from cuanlens.models import RawData
from cuanlens.providers.demo import synthetic_ohlcv
from cuanlens.tickers import resolve

HEALTHY_INFO = {
    "longName": "PT Contoh Tbk",
    "sector": "Industrials",
    "trailingPE": 8.0,
    "priceToBook": 0.9,
    "returnOnEquity": 0.18,
    "debtToEquity": 40.0,  # percent -> 0.40x
    "profitMargins": 0.17,
    "revenueGrowth": 0.12,
    "earningsGrowth": 0.15,
    "currentRatio": 1.8,
}


def trending(n: int = 260, daily: float = 0.004) -> pd.DataFrame:
    """Deterministic steadily rising series (low noise)."""
    return synthetic_ohlcv(n, drift=daily, vol=0.002, seed=1)


@pytest.fixture
def idx():
    return resolve("BBCA")


@pytest.fixture
def raw_healthy(idx) -> RawData:
    return RawData(instrument=idx, history=trending(), info=dict(HEALTHY_INFO))
