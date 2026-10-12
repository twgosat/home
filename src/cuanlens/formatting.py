"""Small number-formatting helpers (Indonesian style: ``1.234,5``)."""

from __future__ import annotations

import math


def _ok(x: float | None) -> bool:
    return x is not None and not (isinstance(x, float) and math.isnan(x)) and math.isfinite(x)


def num(x: float | None, decimals: int = 2) -> str:
    """Indonesian-style number: thousands ``.``, decimal ``,``. ``n/a`` for missing."""
    if not _ok(x):
        return "n/a"
    s = f"{x:,.{decimals}f}"
    return s.replace(",", "\0").replace(".", ",").replace("\0", ".")


def pct(x: float | None, decimals: int = 1, signed: bool = False) -> str:
    """Format a value that is *already* in percent units (3.2 -> ``3,2%``)."""
    if not _ok(x):
        return "n/a"
    body = num(x, decimals)
    if signed and x > 0:
        body = "+" + body
    return f"{body}%"


def money(x: float | None, currency: str = "IDR") -> str:
    """Shorten large amounts: IDR uses ribu/juta/miliar/triliun, others K/M/B/T."""
    if not _ok(x):
        return "n/a"
    sign = "-" if x < 0 else ""
    v = abs(x)
    if currency == "IDR":
        units = [(1e12, "triliun"), (1e9, "miliar"), (1e6, "juta")]
        prefix = "Rp "
    else:
        units = [(1e12, "T"), (1e9, "B"), (1e6, "M")]
        prefix = "$"
    for size, label in units:
        if v >= size:
            sep = " " if currency == "IDR" else ""
            return f"{sign}{prefix}{num(v / size, 2)}{sep}{label}"
    return f"{sign}{prefix}{num(v, 2 if currency != 'IDR' else 0)}"


def price(x: float | None, currency: str = "IDR") -> str:
    if not _ok(x):
        return "n/a"
    if currency == "IDR":
        return f"Rp {num(x, 0)}"
    return f"${num(x, 2 if x >= 1 else 6)}"
