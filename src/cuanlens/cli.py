"""Command line: ``cuanlens analyze BBCA``, ``cuanlens screen --universe idx-starter``."""

from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .doctor import exit_code, format_report, run_doctor
from .errors import CuanLensError
from .llm import get_llm
from .narrator import analyze
from .providers import CachedProvider, DataProvider, DemoProvider, YahooProvider
from .screener import screen
from .universes import UNIVERSES


def _provider(demo: bool) -> DataProvider:
    return DemoProvider() if demo else CachedProvider(YahooProvider())


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="cuanlens", description="Saham IDX & kripto -> narasi yang mudah dipahami.")
    p.add_argument("--version", action="version", version=f"cuanlens {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("analyze", help="Analisis satu instrumen")
    a.add_argument("symbol", help="BBCA, BBCA.JK, BTC, BTC-USD ...")
    a.add_argument("--market", choices=["idx", "crypto"])
    a.add_argument("--llm", choices=["none", "gemini", "openai"], default="none", help="Backend narasi (default: none = offline)")
    a.add_argument("--model", help="Nama model untuk backend LLM")
    a.add_argument("--period", default="1y", help="Rentang histori Yahoo (default 1y)")
    a.add_argument("--lang", choices=["id", "en"], default="id")
    a.add_argument("--json", action="store_true", help="Cetak brief terstruktur (JSON), tanpa narasi")
    a.add_argument("--prompt", action="store_true", help="Cetak konteks yang akan dikirim ke LLM, lalu keluar")
    a.add_argument("--fallback", action="store_true", help="Jika LLM gagal, pakai narasi offline")
    a.add_argument("--demo", action="store_true", help="Pakai data SINTETIS offline (tanpa jaringan)")

    s = sub.add_parser("screen", help="Saring dan urutkan banyak instrumen berdasarkan skor")
    s.add_argument("symbols", nargs="*", help="Daftar simbol")
    s.add_argument("--universe", choices=sorted(UNIVERSES), help="Pakai daftar bawaan")
    s.add_argument("--market", choices=["idx", "crypto"])
    s.add_argument("--min-score", type=int)
    s.add_argument("--max-pe", type=float)
    s.add_argument("--min-roe", type=float, help="ROE minimum dalam persen")
    s.add_argument("--trend", choices=["uptrend", "downtrend", "sideways"])
    s.add_argument("--sort", default="overall_score", dest="sort_by")
    s.add_argument("--workers", type=int, default=4)
    s.add_argument("--demo", action="store_true", help="Pakai data SINTETIS offline")

    d = sub.add_parser("doctor", help="Periksa apakah jalur data live (Yahoo) dan LLM siap dipakai")
    d.add_argument("symbols", nargs="*", default=["BBCA", "BTC"], help="Simbol uji (default: BBCA BTC)")
    return p


def _cmd_doctor(args: argparse.Namespace) -> int:
    checks = run_doctor(symbols=tuple(args.symbols))
    print(format_report(checks))
    return exit_code(checks)


def _cmd_analyze(args: argparse.Namespace) -> int:
    llm = None
    if args.llm != "none" and not args.prompt and not args.json:
        kwargs = {"model": args.model} if args.model else {}
        llm = get_llm(args.llm, **kwargs)

    result = analyze(
        args.symbol,
        llm=llm,
        provider=_provider(args.demo),
        market=args.market,
        period=args.period,
        language=args.lang,
        fallback_to_offline=args.fallback,
    )
    if args.json:
        print(result.brief.to_json())
    elif args.prompt:
        print(result.brief.to_prompt_context())
    else:
        if result.warning:
            print(f"[peringatan] {result.warning}", file=sys.stderr)
        print(result.to_markdown())
    return 0


def _cmd_screen(args: argparse.Namespace) -> int:
    symbols = list(args.symbols)
    if args.universe:
        symbols += UNIVERSES[args.universe]
    if not symbols:
        print("Beri daftar simbol atau --universe.", file=sys.stderr)
        return 2
    df = screen(
        symbols,
        provider=_provider(args.demo),
        market=args.market,
        min_score=args.min_score,
        max_pe=args.max_pe,
        min_roe=args.min_roe,
        trend=args.trend,
        sort_by=args.sort_by,
        workers=args.workers,
    )
    cols = ["symbol", "price", "chg_1m_pct", "trend", "rsi14", "pe", "pbv", "roe_pct", "technical_score", "fundamental_score", "overall_score", "label"]
    if df.empty:
        print("Tidak ada hasil.")
    else:
        print(df[[c for c in cols if c in df.columns]].round(2).to_string(index=False))
    errors = df.attrs.get("errors", {})
    if errors:
        print("\nGagal:", json.dumps(errors, ensure_ascii=False, indent=2), file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        handler = {"analyze": _cmd_analyze, "screen": _cmd_screen, "doctor": _cmd_doctor}[args.cmd]
        return handler(args)
    except CuanLensError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
