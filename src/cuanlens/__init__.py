"""CuanLens: turn messy IDX / crypto market data into narratives retail investors understand."""

from .brief import StockBrief, build_brief
from .errors import CuanLensError, DataError, LLMError, TickerError
from .fundamentals import Thresholds
from .narrator import Analysis, analyze, narrate, offline_narrative
from .screener import screen
from .tickers import Instrument, resolve

__version__ = "0.1.0"

__all__ = [
    "Analysis",
    "CuanLensError",
    "DataError",
    "Instrument",
    "LLMError",
    "StockBrief",
    "Thresholds",
    "TickerError",
    "__version__",
    "analyze",
    "build_brief",
    "narrate",
    "offline_narrative",
    "resolve",
    "screen",
]
