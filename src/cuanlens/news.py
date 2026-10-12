"""News cleaning: dedupe, de-HTML, trim, and a crude lexicon sentiment hint.

The lexicon is intentionally tiny. It exists so the offline path works and so the LLM gets a
cheap prior; the real sentiment judgement is the LLM's job.
"""

from __future__ import annotations

import html
import re
from datetime import datetime, timedelta, timezone

from .models import NewsItem

_POS = frozenset(
    "naik melonjak meroket laba untung rekor dividen ekspansi tumbuh positif akuisisi buyback "
    "surge surges soar soars jump jumps beat beats record profit growth upgrade upgrades "
    "gain gains rally bullish dividend expands approval".split()
)
_NEG = frozenset(
    "turun anjlok jatuh rugi merugi denda korupsi gugatan sanksi suspensi gagal pailit "
    "plunge plunges drop drops fall falls miss misses loss losses downgrade downgrades "
    "probe lawsuit fraud default bankruptcy bearish selloff slump cuts".split()
)
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")
_WORD_RE = re.compile(r"[a-zA-Z]+")


def _text(s: str | None) -> str:
    return _WS_RE.sub(" ", html.unescape(_TAG_RE.sub(" ", s or ""))).strip()


def sentiment_hint(text: str) -> str:
    """'positif' / 'negatif' / 'netral' from word counts. A hint, not a verdict."""
    words = [w.lower() for w in _WORD_RE.findall(text)]
    score = sum(w in _POS for w in words) - sum(w in _NEG for w in words)
    return "positif" if score > 0 else "negatif" if score < 0 else "netral"


def clean_news(
    items: list[NewsItem],
    *,
    max_items: int = 8,
    max_age_days: int | None = 30,
    summary_chars: int = 300,
    now: datetime | None = None,
) -> list[NewsItem]:
    """Return at most ``max_items`` de-duplicated, newest-first, sanitised items.

    Undated items are kept (some feeds omit dates) but sort after dated ones.
    """
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=max_age_days) if max_age_days else None

    seen: set[str] = set()
    kept: list[NewsItem] = []
    for it in items:
        title = _text(it.title)
        if not title:
            continue
        key = re.sub(r"\W+", "", title.lower())
        if key in seen:
            continue
        published = it.published
        if published is not None and published.tzinfo is None:
            published = published.replace(tzinfo=timezone.utc)
        if cutoff and published and published < cutoff:
            continue
        seen.add(key)
        summary = _text(it.summary)
        if len(summary) > summary_chars:
            summary = summary[: summary_chars - 1].rstrip() + "…"
        kept.append(
            NewsItem(
                title=title,
                publisher=_text(it.publisher),
                published=published,
                url=it.url,
                summary=summary,
                hint=sentiment_hint(f"{title} {summary}"),
            )
        )

    floor = datetime.min.replace(tzinfo=timezone.utc)
    kept.sort(key=lambda n: n.published or floor, reverse=True)
    return kept[:max_items]
