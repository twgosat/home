"""Turn raw numbers into labelled, human-readable signals.

A :class:`Signal` is deliberately explainable: a name, a stance, a one-line reason in
Indonesian and the points it adds to a heuristic 0-100 score. The score is a *screening
aid*, not a prediction and not a buy/sell recommendation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Stance = Literal["bullish", "bearish", "neutral"]


@dataclass(frozen=True)
class Signal:
    name: str
    stance: Stance
    detail: str
    points: int = 0

    def to_dict(self) -> dict:
        return {"name": self.name, "stance": self.stance, "detail": self.detail, "points": self.points}


def score_from(signals: list[Signal], base: int = 50) -> int:
    """Clamp ``base + sum(points)`` into 0..100."""
    return max(0, min(100, base + sum(s.points for s in signals)))


def score_label(score: float | None) -> str:
    if score is None:
        return "n/a"
    if score >= 65:
        return "kuat"
    if score >= 45:
        return "netral"
    return "lemah"
