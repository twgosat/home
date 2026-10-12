"""``cuanlens doctor``: verify the live pipeline end-to-end on the user's machine.

Each check returns PASS / WARN / FAIL with a hint, so "it doesn't work" turns into a
specific, fixable statement (network blocked, Yahoo rate-limit, missing API key...).
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from datetime import date

from .brief import build_brief
from .errors import CuanLensError
from .providers import DataProvider, YahooProvider
from .tickers import resolve

PASS, WARN, FAIL = "PASS", "WARN", "FAIL"
STALE_DAYS = 7


@dataclass
class Check:
    name: str
    status: str
    detail: str
    hint: str = ""


def _python() -> Check:
    v = sys.version_info
    ok = v >= (3, 10)
    return Check("Python", PASS if ok else FAIL, f"{v.major}.{v.minor}.{v.micro}", "" if ok else "Butuh Python >= 3.10.")


def check_symbol(provider: DataProvider, symbol: str, *, today: date | None = None) -> list[Check]:
    """Fetch one symbol through ``provider`` and report on prices, fundamentals and news."""
    today = today or date.today()
    try:
        inst = resolve(symbol)
        raw = provider.fetch(inst, "1y")
    except CuanLensError as e:
        return [
            Check(
                f"Harga {symbol}",
                FAIL,
                str(e)[:200],
                "Cek koneksi internet/VPN/proxy kantor (host: query1.finance.yahoo.com, "
                "query2.finance.yahoo.com, fc.yahoo.com). Jika jaringan normal, Yahoo mungkin "
                "sedang membatasi laju: tunggu beberapa menit lalu coba lagi.",
            )
        ]

    out: list[Check] = []
    last = raw.history.index[-1].date()
    age = (today - last).days
    out.append(
        Check(
            f"Harga {symbol}",
            PASS if age <= STALE_DAYS else WARN,
            f"{len(raw.history)} bar, terakhir {last.isoformat()} ({age} hari lalu)",
            "" if age <= STALE_DAYS else "Data tampak basi. Wajar saat libur panjang; jika tidak, laporkan sebagai Issue.",
        )
    )

    try:
        brief = build_brief(raw)
    except CuanLensError as e:
        out.append(Check(f"Preprocessing {symbol}", FAIL, str(e), "Histori terlalu pendek? Coba ticker lain."))
        return out
    out.append(Check(f"Preprocessing {symbol}", PASS, f"tren {brief.technical.trend}, skor {brief.overall_score}/100"))

    if inst.market == "idx":
        f = brief.fundamentals
        n = f.available_metrics() if f else 0
        if n >= 3:
            out.append(Check(f"Fundamental {symbol}", PASS, f"{n} metrik tersedia"))
        else:
            out.append(
                Check(
                    f"Fundamental {symbol}",
                    WARN,
                    f"hanya {n} metrik",
                    "Yahoo sering membatasi/menunda data fundamental. Analisis tetap jalan hanya dengan teknikal.",
                )
            )
    out.append(
        Check(f"Berita {symbol}", PASS if brief.news else WARN, f"{len(brief.news)} berita",
              "" if brief.news else "Tidak ada berita terbaru; narasi tetap dibuat tanpa bagian sentimen.")
    )
    return out


def llm_checks(env: dict[str, str] | None = None) -> list[Check]:
    """Report which LLM backends are usable. Never calls a model (no cost, no key leakage)."""
    env = os.environ if env is None else env
    out: list[Check] = []
    for label, module, keys, extra in (
        ("Gemini", "google.genai", ("GEMINI_API_KEY", "GOOGLE_API_KEY"), "gemini"),
        ("OpenAI", "openai", ("OPENAI_API_KEY",), "openai"),
    ):
        try:
            __import__(module)
            sdk = True
        except ImportError:
            sdk = False
        has_key = any(env.get(k) for k in keys)
        if sdk and has_key:
            out.append(Check(f"LLM {label}", PASS, "SDK terpasang, API key terdeteksi"))
        else:
            missing = []
            if not sdk:
                missing.append(f"pip install 'cuanlens[{extra}]'")
            if not has_key:
                missing.append(f"set {keys[0]}")
            out.append(Check(f"LLM {label}", WARN, "belum siap (opsional)", " dan ".join(missing)))
    return out


def run_doctor(
    provider: DataProvider | None = None,
    symbols: tuple[str, ...] = ("BBCA", "BTC"),
    *,
    env: dict[str, str] | None = None,
    today: date | None = None,
) -> list[Check]:
    provider = provider or YahooProvider()
    checks = [_python()]
    for s in symbols:
        checks += check_symbol(provider, s, today=today)
    checks += llm_checks(env)
    return checks


def format_report(checks: list[Check]) -> str:
    icon = {PASS: "[ OK ]", WARN: "[WARN]", FAIL: "[FAIL]"}
    lines = []
    for c in checks:
        lines.append(f"{icon[c.status]} {c.name}: {c.detail}")
        if c.hint:
            lines.append(f"         -> {c.hint}")
    fails = sum(c.status == FAIL for c in checks)
    warns = sum(c.status == WARN for c in checks)
    lines.append("")
    if fails:
        lines.append(f"{fails} masalah harus diperbaiki sebelum data live bisa dipakai. Mode offline tetap jalan: cuanlens analyze BBCA --demo")
    elif warns:
        lines.append("Berjalan, dengan catatan di atas (bagian bertanda WARN bersifat opsional/sementara).")
    else:
        lines.append("Semua beres. Coba: cuanlens analyze BBCA")
    return "\n".join(lines)


def exit_code(checks: list[Check]) -> int:
    return 1 if any(c.status == FAIL for c in checks) else 0
