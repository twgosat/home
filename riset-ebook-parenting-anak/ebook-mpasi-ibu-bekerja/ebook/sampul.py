"""Sampul 850×1100 (rasio Letter) dirender jadi PNG. Skala 2 untuk PDF, 3 untuk HD 2550×3300."""
from __future__ import annotations

import html as _h
from pathlib import Path


def html_sampul(subjudul: str, pil: list[str], tahun: int) -> str:
    pills = "".join(f'<span class="pill">{_h.escape(p)}</span>' for p in pil)
    # Ilustrasi: rak freezer berisi wadah berlabel + kalender Senin–Jumat dicentang (di bawah semua teks).
    wadah = "".join(
        f'<g transform="translate({60 + (i % 5) * 140},{40 + (i // 5) * 96})">'
        f'<rect width="118" height="74" rx="12" fill="#0f2a20" stroke="#4fd1c5" stroke-width="3"/>'
        f'<rect x="14" y="14" width="90" height="20" rx="4" fill="#b8f35c"/>'
        f'<rect x="14" y="44" width="60" height="8" rx="4" fill="#4fd1c5" opacity=".7"/></g>'
        for i in range(10))
    hari = "".join(
        f'<g transform="translate({60 + i * 140},250)"><rect width="118" height="64" rx="10" fill="#0b1f18" '
        f'stroke="#2d4a3e" stroke-width="2"/><text x="59" y="26" text-anchor="middle" font-size="18" '
        f'fill="#a7bfb2" font-family="Inter">{d}</text><path d="M40 42 l12 12 l26 -26" stroke="#b8f35c" '
        f'stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'
        for i, d in enumerate(["Sen", "Sel", "Rab", "Kam", "Jum"]))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:850px;height:1100px;overflow:hidden;font-family:Inter,'DejaVu Sans',sans-serif;color:#eaf5ee;
background:radial-gradient(circle at 75% 18%,rgba(184,243,92,.18),transparent 45%),
radial-gradient(circle at 10% 90%,rgba(79,209,197,.16),transparent 50%),#07130f;position:relative}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),
linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);background-size:50px 50px}}
.isi{{position:absolute;left:70px;right:70px;top:80px}}
.tag{{font-size:20px;font-weight:700;letter-spacing:.18em;color:#4fd1c5}}
h1{{font-size:150px;line-height:.95;font-weight:900;color:#b8f35c;margin-top:26px;letter-spacing:-.02em}}
h2{{font-size:84px;line-height:1;font-weight:900;color:#ffffff;letter-spacing:-.01em}}
.sub{{font-size:31px;line-height:1.3;font-weight:600;margin-top:30px;color:#eaf5ee;max-width:690px}}
.pills{{margin-top:34px;display:flex;flex-wrap:wrap;gap:14px}}
.pill{{font-size:21px;font-weight:700;padding:11px 20px;border-radius:999px;border:2px solid #4fd1c5;color:#dffaf6;
background:rgba(79,209,197,.08)}}
svg{{position:absolute;left:0;bottom:120px}}
.kaki{{position:absolute;left:70px;right:70px;bottom:46px;display:flex;justify-content:space-between;font-size:22px;
font-weight:700;color:#a7bfb2}}
.kaki b{{color:#b8f35c}}
</style></head><body><div class="grid"></div>
<div class="isi"><div class="tag">EBOOK + KIT PRINTABLE · USIA 6–23 BULAN</div>
<h1>MPASI</h1><h2>IBU BEKERJA</h2>
<div class="sub">{_h.escape(subjudul)}</div><div class="pills">{pills}</div></div>
<svg width="850" height="330" viewBox="0 0 850 330">{wadah}{hari}</svg>
<div class="kaki"><span>Edisi {tahun}</span><b>GoSatSet.xyz</b></div></body></html>"""


def buat_png(html: str, keluar: Path, skala: int) -> Path:
    from playwright.sync_api import sync_playwright
    keluar = Path(keluar)
    keluar.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 850, "height": 1100}, device_scale_factor=skala)
        pg.set_content(html, wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.screenshot(path=str(keluar), full_page=False)
        b.close()
    return keluar
