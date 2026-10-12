"""Yahoo Finance provider (via ``yfinance``).

Note: Yahoo's data is for personal/informational use under its terms. If you build a paid
product on CuanLens, swap this for a licensed feed by implementing ``DataProvider``.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ..errors import DataError
from ..models import NewsItem, RawData, normalize_ohlcv
from ..tickers import Instrument


def _parse_dt(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc)
    if isinstance(value, str):
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    return None


def parse_news(items: list[dict[str, Any]] | None) -> list[NewsItem]:
    """Handle both yfinance news layouts (legacy flat dicts and the newer ``content`` wrapper)."""
    out: list[NewsItem] = []
    for it in items or []:
        if not isinstance(it, dict):
            continue
        c = it.get("content") if isinstance(it.get("content"), dict) else it
        title = c.get("title") or ""
        if not title:
            continue
        provider = c.get("provider")
        publisher = (
            provider.get("displayName", "") if isinstance(provider, dict) else c.get("publisher", "")
        )
        url_obj = c.get("canonicalUrl") or c.get("clickThroughUrl")
        url = url_obj.get("url", "") if isinstance(url_obj, dict) else (c.get("link") or "")
        out.append(
            NewsItem(
                title=title,
                publisher=publisher or "",
                published=_parse_dt(c.get("pubDate") or c.get("providerPublishTime")),
                url=url or "",
                summary=c.get("summary") or c.get("description") or "",
            )
        )
    return out


class YahooProvider:
    """Fetch history, fundamentals (``info``) and news for one instrument."""

    def __init__(self, *, include_news: bool = True, include_info: bool = True) -> None:
        self.include_news = include_news
        self.include_info = include_info

    def fetch(self, instrument: Instrument, period: str = "1y") -> RawData:
        try:
            import yfinance as yf
        except ImportError as e:  # pragma: no cover - yfinance is a core dependency
            raise DataError("yfinance is not installed: pip install yfinance") from e

        ticker = yf.Ticker(instrument.yahoo_symbol)
        try:
            history = ticker.history(period=period, auto_adjust=False)
        except Exception as e:
            raise DataError(f"Failed to fetch prices for {instrument.yahoo_symbol}: {e}") from e
        history = normalize_ohlcv(history)  # raises DataError if empty (bad ticker / delisted)

        info: dict[str, Any] = {}
        if self.include_info and instrument.market == "idx":
            try:
                info = dict(ticker.info or {})
            except Exception:  # Yahoo frequently rate-limits `info`; degrade gracefully.
                info = {}

        news: list[NewsItem] = []
        if self.include_news:
            try:
                news = parse_news(ticker.news)
            except Exception:
                news = []

        return RawData(instrument=instrument, history=history, info=info, news=news)
