from __future__ import annotations

import threading
import time

from ..models import RawData
from ..tickers import Instrument
from .base import DataProvider


class CachedProvider:
    """In-memory TTL cache around any provider.

    Cuts Yahoo rate-limit pain and repeat-request cost (e.g. several users opening the same
    ticker). For multi-process deployments, put Redis behind your own ``DataProvider`` instead.
    """

    def __init__(self, inner: DataProvider, ttl_seconds: float = 900.0) -> None:
        self.inner = inner
        self.ttl = ttl_seconds
        self._store: dict[tuple[str, str], tuple[float, RawData]] = {}
        self._lock = threading.Lock()

    def fetch(self, instrument: Instrument, period: str = "1y") -> RawData:
        key = (instrument.yahoo_symbol, period)
        now = time.monotonic()
        with self._lock:
            hit = self._store.get(key)
            if hit and now - hit[0] < self.ttl:
                return hit[1]
        data = self.inner.fetch(instrument, period)
        with self._lock:
            self._store[key] = (time.monotonic(), data)
        return data

    def clear(self) -> None:
        with self._lock:
            self._store.clear()
