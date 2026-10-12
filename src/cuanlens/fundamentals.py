"""Yahoo-style ``info`` dict -> clean :class:`FundamentalSnapshot` + fundamental signals.

Yahoo's ``info`` is inconsistent between tickers and library versions, so every field is
optional and nothing here assumes a key exists.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

from .formatting import num, pct
from .signals import Signal

MIN_METRICS_FOR_SCORE = 3


@dataclass(frozen=True)
class Thresholds:
    """Rule-of-thumb cut-offs. Override per sector/market; defaults are generic, not gospel."""

    pe_cheap: float = 10.0
    pe_expensive: float = 25.0
    pbv_cheap: float = 1.0
    pbv_expensive: float = 5.0
    roe_good: float = 15.0  # percent
    roe_weak: float = 8.0
    der_low: float = 0.5  # ratio
    der_high: float = 2.0
    net_margin_good: float = 15.0  # percent
    net_margin_weak: float = 3.0
    growth_good: float = 10.0  # percent
    dividend_good: float = 3.0  # percent


@dataclass
class FundamentalSnapshot:
    name: str | None = None
    sector: str | None = None
    industry: str | None = None
    market_cap: float | None = None
    pe: float | None = None
    forward_pe: float | None = None
    pbv: float | None = None
    roe_pct: float | None = None
    roa_pct: float | None = None
    debt_to_equity: float | None = None  # ratio, e.g. 0.45 (NOT percent)
    current_ratio: float | None = None
    net_margin_pct: float | None = None
    operating_margin_pct: float | None = None
    revenue_growth_pct: float | None = None
    earnings_growth_pct: float | None = None
    dividend_yield_pct: float | None = None
    beta: float | None = None
    eps: float | None = None
    is_financial: bool = False

    _METRICS = (
        "pe", "pbv", "roe_pct", "debt_to_equity", "net_margin_pct",
        "revenue_growth_pct", "earnings_growth_pct", "dividend_yield_pct",
    )  # fmt: skip

    def available_metrics(self) -> int:
        return sum(getattr(self, m) is not None for m in self._METRICS)

    @property
    def has_enough_data(self) -> bool:
        return self.available_metrics() >= MIN_METRICS_FOR_SCORE

    def to_dict(self) -> dict:
        return asdict(self)


def _f(info: dict[str, Any], key: str) -> float | None:
    v = info.get(key)
    if v is None or isinstance(v, bool):
        return None
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def _scale(x: float | None, factor: float) -> float | None:
    return None if x is None else x * factor


def parse_fundamentals(info: dict[str, Any] | None, price: float | None = None) -> FundamentalSnapshot:
    """Normalise a Yahoo ``info`` dict. ``price`` (last close) is used to derive dividend yield."""
    info = info or {}
    sector = info.get("sector")

    # Dividend yield: Yahoo changed `dividendYield` from fraction to percent across versions,
    # so derive it from rate/price when possible and fall back to the trailing *fraction* field.
    dy: float | None = None
    rate = _f(info, "dividendRate")
    if rate is not None and price:
        dy = rate / price * 100
    else:
        t = _f(info, "trailingAnnualDividendYield")
        dy = _scale(t, 100)

    pe = _f(info, "trailingPE")
    eps = _f(info, "trailingEps")
    if pe is not None and pe <= 0:  # negative/zero P/E is not a usable multiple
        pe = None

    der_pct = _f(info, "debtToEquity")  # Yahoo reports this in percent (45.3 == 0.453x)

    return FundamentalSnapshot(
        name=info.get("longName") or info.get("shortName"),
        sector=sector,
        industry=info.get("industry"),
        market_cap=_f(info, "marketCap"),
        pe=pe,
        forward_pe=_f(info, "forwardPE"),
        pbv=_f(info, "priceToBook"),
        roe_pct=_scale(_f(info, "returnOnEquity"), 100),
        roa_pct=_scale(_f(info, "returnOnAssets"), 100),
        debt_to_equity=_scale(der_pct, 0.01),
        current_ratio=_f(info, "currentRatio"),
        net_margin_pct=_scale(_f(info, "profitMargins"), 100),
        operating_margin_pct=_scale(_f(info, "operatingMargins"), 100),
        revenue_growth_pct=_scale(_f(info, "revenueGrowth"), 100),
        earnings_growth_pct=_scale(_f(info, "earningsGrowth"), 100),
        dividend_yield_pct=dy,
        beta=_f(info, "beta"),
        eps=eps,
        is_financial=isinstance(sector, str) and "financial" in sector.lower(),
    )


def fundamental_signals(f: FundamentalSnapshot, th: Thresholds | None = None) -> list[Signal]:
    th = th or Thresholds()
    out: list[Signal] = []

    # Valuation
    if f.pe is not None:
        if f.pe <= th.pe_cheap:
            out.append(Signal("PER", "bullish", f"PER {num(f.pe, 1)}x tergolong murah (cek apakah laba berkelanjutan).", 6))
        elif f.pe >= th.pe_expensive:
            out.append(Signal("PER", "bearish", f"PER {num(f.pe, 1)}x tergolong mahal; ekspektasi pertumbuhan sudah tinggi.", -6))
        else:
            out.append(Signal("PER", "neutral", f"PER {num(f.pe, 1)}x di kisaran wajar.", 0))
    elif f.eps is not None and f.eps < 0:
        out.append(Signal("Laba", "bearish", "Perusahaan masih merugi (EPS negatif), PER tidak bermakna.", -10))

    if f.pbv is not None:
        if f.pbv <= th.pbv_cheap:
            out.append(Signal("PBV", "bullish", f"PBV {num(f.pbv, 2)}x: diperdagangkan di sekitar/di bawah nilai buku.", 4))
        elif f.pbv >= th.pbv_expensive:
            out.append(Signal("PBV", "bearish", f"PBV {num(f.pbv, 2)}x: premi tinggi atas nilai buku.", -4))

    # Profitability
    if f.roe_pct is not None:
        if f.roe_pct < 0:
            out.append(Signal("ROE", "bearish", f"ROE negatif ({pct(f.roe_pct)}).", -10))
        elif f.roe_pct >= th.roe_good:
            out.append(Signal("ROE", "bullish", f"ROE {pct(f.roe_pct)}: efisien menghasilkan laba dari modal.", 8))
        elif f.roe_pct < th.roe_weak:
            out.append(Signal("ROE", "bearish", f"ROE {pct(f.roe_pct)}: imbal hasil modal rendah.", -6))
        else:
            out.append(Signal("ROE", "neutral", f"ROE {pct(f.roe_pct)}: moderat.", 0))

    if f.net_margin_pct is not None:
        if f.net_margin_pct < 0:
            out.append(Signal("Margin bersih", "bearish", f"Margin laba bersih negatif ({pct(f.net_margin_pct)}).", -8))
        elif f.net_margin_pct >= th.net_margin_good:
            out.append(Signal("Margin bersih", "bullish", f"Margin laba bersih {pct(f.net_margin_pct)} tebal.", 4))
        elif f.net_margin_pct < th.net_margin_weak:
            out.append(Signal("Margin bersih", "bearish", f"Margin laba bersih {pct(f.net_margin_pct)} tipis.", -4))

    # Leverage: meaningless for banks/insurers, whose business is debt.
    if not f.is_financial:
        if f.debt_to_equity is not None:
            if f.debt_to_equity >= th.der_high:
                out.append(Signal("DER", "bearish", f"DER {num(f.debt_to_equity, 2)}x: utang besar terhadap ekuitas.", -6))
            elif f.debt_to_equity <= th.der_low:
                out.append(Signal("DER", "bullish", f"DER {num(f.debt_to_equity, 2)}x: struktur modal konservatif.", 4))
        if f.current_ratio is not None and f.current_ratio < 1:
            out.append(Signal("Likuiditas", "bearish", f"Current ratio {num(f.current_ratio, 2)} (<1): aset lancar lebih kecil dari kewajiban lancar.", -3))

    # Growth
    if f.revenue_growth_pct is not None:
        if f.revenue_growth_pct >= th.growth_good:
            out.append(Signal("Pertumbuhan pendapatan", "bullish", f"Pendapatan tumbuh {pct(f.revenue_growth_pct)} YoY.", 4))
        elif f.revenue_growth_pct < 0:
            out.append(Signal("Pertumbuhan pendapatan", "bearish", f"Pendapatan menyusut {pct(abs(f.revenue_growth_pct))} YoY.", -4))
    if f.earnings_growth_pct is not None:
        if f.earnings_growth_pct >= th.growth_good:
            out.append(Signal("Pertumbuhan laba", "bullish", f"Laba tumbuh {pct(f.earnings_growth_pct)} YoY.", 4))
        elif f.earnings_growth_pct < 0:
            out.append(Signal("Pertumbuhan laba", "bearish", f"Laba turun {pct(abs(f.earnings_growth_pct))} YoY.", -4))

    # Income
    if f.dividend_yield_pct is not None and f.dividend_yield_pct >= th.dividend_good:
        out.append(Signal("Dividen", "bullish", f"Dividend yield {pct(f.dividend_yield_pct)}.", 3))

    return out
