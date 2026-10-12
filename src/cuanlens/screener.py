"""Batch screening: many symbols in, one ranked DataFrame out."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from .brief import StockBrief, build_brief
from .fundamentals import Thresholds
from .providers import DataProvider, YahooProvider
from .tickers import Market, resolve


def screen(
    symbols: list[str],
    *,
    provider: DataProvider | None = None,
    market: Market | None = None,
    period: str = "1y",
    min_score: int | None = None,
    max_pe: float | None = None,
    min_roe: float | None = None,
    trend: str | None = None,
    sort_by: str = "overall_score",
    ascending: bool = False,
    workers: int = 4,
    thresholds: Thresholds | None = None,
) -> pd.DataFrame:
    """Score every symbol and return a filtered, sorted DataFrame.

    Failures (bad ticker, no data) never abort the batch: they are collected in
    ``df.attrs["errors"]`` as ``{symbol: message}``. Keep ``workers`` modest; Yahoo
    rate-limits aggressive parallel callers.

    Filters: ``min_score`` on the overall score, ``max_pe`` (rows without PER are dropped),
    ``min_roe`` in percent, ``trend`` one of uptrend/downtrend/sideways.
    """
    provider = provider or YahooProvider()
    errors: dict[str, str] = {}
    briefs: list[StockBrief] = []

    def work(sym: str) -> StockBrief:
        inst = resolve(sym, market)
        return build_brief(provider.fetch(inst, period), thresholds=thresholds)

    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = {sym: pool.submit(work, sym) for sym in dict.fromkeys(symbols)}
        for sym, fut in futures.items():
            try:
                briefs.append(fut.result())
            except Exception as e:  # one bad ticker must not sink the batch
                errors[sym] = f"{type(e).__name__}: {e}"

    df = pd.DataFrame([b.to_row() for b in briefs])
    if df.empty:
        df.attrs["errors"] = errors
        return df

    if min_score is not None:
        df = df[df["overall_score"] >= min_score]
    if max_pe is not None:
        df = df[df["pe"].notna() & (df["pe"] <= max_pe)]
    if min_roe is not None:
        df = df[df["roe_pct"].notna() & (df["roe_pct"] >= min_roe)]
    if trend is not None:
        df = df[df["trend"] == trend]

    if sort_by not in df.columns:
        raise ValueError(f"Unknown sort_by {sort_by!r}; columns: {list(df.columns)}")
    df = df.sort_values(sort_by, ascending=ascending, na_position="last").reset_index(drop=True)
    df.attrs["errors"] = errors
    return df
