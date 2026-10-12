from __future__ import annotations

from typing import Protocol, runtime_checkable

from ..models import RawData
from ..tickers import Instrument


@runtime_checkable
class DataProvider(Protocol):
    """Anything that can fetch :class:`RawData` for an instrument.

    Implement this to plug in a licensed data feed (IDX, a broker API, Binance, CSV files...)
    without touching the rest of the library.
    """

    def fetch(self, instrument: Instrument, period: str = "1y") -> RawData: ...
