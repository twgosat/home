"""Starter symbol lists for quick experiments.

These are hand-picked liquid names, NOT official index constituents (LQ45/IDX30 rebalance
twice a year). Pass your own list for anything serious.
"""

from __future__ import annotations

IDX_STARTER = [
    "BBCA", "BBRI", "BMRI", "BBNI", "TLKM", "ASII", "UNVR", "ICBP", "INDF", "KLBF",
    "ADRO", "PTBA", "ANTM", "AMRT", "CPIN", "SMGR", "MDKA", "INCO", "ITMG", "GOTO",
]  # fmt: skip

CRYPTO_STARTER = ["BTC", "ETH", "SOL", "BNB", "XRP"]

UNIVERSES = {"idx-starter": IDX_STARTER, "crypto-starter": CRYPTO_STARTER}
