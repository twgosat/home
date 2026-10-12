"""Brief -> narrative text: via an LLM, or deterministically offline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from . import formatting as fm
from .brief import StockBrief, build_brief
from .errors import CuanLensError, LLMError
from .fundamentals import Thresholds
from .llm import LLM
from .models import RawData
from .prompts import disclaimer, system_prompt, user_prompt
from .providers import DataProvider, YahooProvider
from .signals import score_label
from .tickers import Market, resolve

Source = Literal["llm", "offline"]


@dataclass
class Analysis:
    brief: StockBrief
    narrative: str  # always ends with the disclaimer
    source: Source
    model: str | None = None  # LLM name when source == "llm"
    warning: str | None = None  # e.g. why we fell back to offline

    def to_markdown(self) -> str:
        b = self.brief
        head = f"# {b.instrument.symbol} - {b.name}\n_Data per {b.as_of} · skor gabungan {b.overall_score}/100 ({score_label(b.overall_score)})_\n\n"
        return head + self.narrative

    def to_dict(self) -> dict:
        return {
            "narrative": self.narrative,
            "source": self.source,
            "model": self.model,
            "warning": self.warning,
            "brief": self.brief.to_dict(),
        }


def offline_narrative(brief: StockBrief, language: str = "id") -> str:
    """Rule-based explanation built straight from the signals. No API key, no network.

    Less fluent than an LLM but fully deterministic, which also makes it a good test oracle
    and a free-tier fallback.
    """
    if language != "id":
        raise ValueError("Offline narrative currently supports language='id' only.")
    t, f, cur = brief.technical, brief.fundamentals, brief.instrument.currency
    trend_txt = {
        "uptrend": "tren naik",
        "downtrend": "tren turun",
        "sideways": "tren mendatar/campuran",
    }[t.trend]
    out: list[str] = []

    out.append("## Ringkasan")
    out.append(
        f"{brief.instrument.symbol} ditutup di {fm.price(t.close, cur)}; kondisi saat ini: {trend_txt}. "
        f"Dalam 1 bulan harga berubah {fm.pct(t.change_pct.get('1m'), 1, True)} dan "
        f"{fm.pct(t.change_pct.get('3m'), 1, True)} dalam 3 bulan. Skor heuristik gabungan "
        f"{brief.overall_score}/100 ({score_label(brief.overall_score)}) - alat penyaring, bukan sinyal beli/jual."
    )

    out.append("\n## Teknikal")
    for s in brief.technical_signals:
        out.append(f"- **{s.name}**: {s.detail}")
    out.append(
        f"- Harga berada {fm.pct(t.pct_from_high, 1, True)} dari puncak 52 minggu "
        f"({fm.price(t.high_52w, cur)}); volatilitas tahunan {fm.pct(t.volatility_pct, 1)}."
    )

    out.append("\n## Fundamental")
    if f is None or not brief.fundamental_signals:
        out.append("Data fundamental tidak tersedia atau tidak memadai.")
    else:
        for s in brief.fundamental_signals:
            out.append(f"- **{s.name}**: {s.detail}")

    out.append("\n## Sentimen Berita")
    if not brief.news:
        out.append("Tidak ada berita terbaru yang tersedia.")
    else:
        pos = sum(n.hint == "positif" for n in brief.news)
        neg = sum(n.hint == "negatif" for n in brief.news)
        tone = "campuran" if pos and neg else "cenderung positif" if pos else "cenderung negatif" if neg else "netral"
        out.append(
            f"Dari {len(brief.news)} berita terbaru, nada terbaca {tone} "
            f"({pos} positif, {neg} negatif; pembacaan berbasis kata kunci sederhana)."
        )
        for n in brief.news[:3]:
            out.append(f"- {n.title}" + (f" ({n.publisher})" if n.publisher else ""))

    out.append("\n## Risiko & Hal yang Perlu Dipantau")
    bearish = [s for s in brief.signals if s.stance == "bearish"]
    if bearish:
        out += [f"- {s.detail}" for s in bearish[:4]]
    else:
        out.append("- Tidak ada sinyal negatif menonjol dari indikator yang dipakai; tetap pantau perubahan tren dan berita.")
    for note in brief.notes:
        out.append(f"- Catatan data: {note}")

    return "\n".join(out)


def narrate(
    brief: StockBrief,
    llm: LLM | None = None,
    *,
    language: str = "id",
    fallback_to_offline: bool = False,
) -> Analysis:
    """Produce an :class:`Analysis` from a brief.

    With ``llm=None`` the offline narrator is used. If the LLM raises :class:`LLMError` the
    error propagates unless ``fallback_to_offline=True``.
    """
    foot = "\n\n" + disclaimer(language)
    if llm is None:
        return Analysis(brief, offline_narrative(brief, language) + foot, "offline")

    try:
        text = llm.generate(system_prompt(language), user_prompt(brief.to_prompt_context(), language))
    except LLMError as e:
        if not fallback_to_offline:
            raise
        return Analysis(
            brief,
            offline_narrative(brief, language) + foot,
            "offline",
            warning=f"LLM gagal ({e}); memakai narasi offline.",
        )
    return Analysis(brief, text.strip() + foot, "llm", model=getattr(llm, "name", None))


def analyze(
    symbol: str,
    *,
    llm: LLM | None = None,
    provider: DataProvider | None = None,
    market: Market | None = None,
    period: str = "1y",
    language: str = "id",
    thresholds: Thresholds | None = None,
    fallback_to_offline: bool = False,
) -> Analysis:
    """One call from ticker to narrative: fetch -> preprocess -> (LLM|offline) narrate."""
    instrument = resolve(symbol, market)
    provider = provider or YahooProvider()
    raw: RawData = provider.fetch(instrument, period)
    brief = build_brief(raw, thresholds=thresholds)
    return narrate(brief, llm, language=language, fallback_to_offline=fallback_to_offline)


__all__ = ["Analysis", "CuanLensError", "analyze", "narrate", "offline_narrative"]
