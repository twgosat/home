"""Run:  python examples/quickstart.py            (offline demo, synthetic data)
       python examples/quickstart.py --live      (Yahoo Finance; add GEMINI_API_KEY for an LLM narrative)
"""

import os
import sys

from cuanlens import analyze, screen
from cuanlens.llm import get_llm
from cuanlens.providers import DemoProvider

live = "--live" in sys.argv
provider = None if live else DemoProvider()  # None -> Yahoo Finance

# 1) One call: ticker -> narrative. Offline narrator unless an LLM is supplied.
llm = get_llm("gemini") if live and os.getenv("GEMINI_API_KEY") else None
result = analyze("BBCA", llm=llm, provider=provider)
print(result.to_markdown())

# 2) The structured brief is what the LLM actually sees, so you can reuse it anywhere.
print("\n--- skor ---", result.brief.to_dict()["scores"])

# 3) Screen a basket and rank by heuristic score.
table = screen(["BBCA", "BBRI", "BMRI", "TLKM", "ASII"], provider=provider)
print("\n", table[["symbol", "trend", "pe", "roe_pct", "overall_score", "label"]].round(1).to_string(index=False))
