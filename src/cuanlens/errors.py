"""Exception hierarchy. Catch ``CuanLensError`` to handle everything the library raises."""

from __future__ import annotations


class CuanLensError(Exception):
    """Base class for all CuanLens errors."""


class TickerError(CuanLensError):
    """The symbol could not be understood or mapped to a market."""


class DataError(CuanLensError):
    """Market data is missing, empty, or malformed."""


class LLMError(CuanLensError):
    """The LLM backend is misconfigured or the call failed."""
