"""Sampul 850×1100 (rasio Letter) dirender jadi PNG. Skala 2 untuk PDF, 3 untuk HD 2550×3300.
Tema anak & parenting: latar krem, bentuk bulat coral/kuning/biru langit/lavender, judul Nunito."""
from __future__ import annotations

import html as _h
from pathlib import Path

from .tema import PALET as P, font_css

TUTUP = [P["coral"], P["kuning"], P["langit"], P["lavender"]]


def _ilustrasi() -> str:
    # Rak wadah porsi dengan tutup warna-warni + kalender Senin–Jumat dicentang (selalu di bawah teks).
    wadah = "".join(
        f'<g transform="translate({70 + (i % 5) * 142},{30 + (i // 5) * 100})">'
        f'<rect y="14" width="118" height="70" rx="16" fill="#ffffff" stroke="{TUTUP[(i + i // 5) % 4]}" stroke-width="4"/>'
        f'<rect x="-4" y="2" width="126" height="22" rx="11" fill="{TUTUP[(i + i // 5) % 4]}"/>'
        f'<rect x="20" y="40" width="78" height="14" rx="7" fill="{P["krem"]}" stroke="{P["garis"]}" stroke-width="2"/>'
        f'<circle cx="44" cy="68" r="4" fill="{P["judul"]}"/><circle cx="74" cy="68" r="4" fill="{P["judul"]}"/>'
        f'<path d="M50 74 q9 7 18 0" stroke="{P["judul"]}" stroke-width="3" fill="none" stroke-linecap="round"/></g>'
        for i in range(10))
    hari = "".join(
        f'<g transform="translate({70 + i * 142},248)"><rect width="118" height="66" rx="16" fill="#ffffff" '
        f'stroke="{P["garis"]}" stroke-width="3"/><text x="59" y="24" text-anchor="middle" font-size="17" font-weight="800" '
        f'fill="{P["redup"]}" font-family="Nunito, Inter, sans-serif">{d}</text><path d="M44 44 l10 10 l20 -20" stroke="{P["coral"]}" '
        f'stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'
        for i, d in enumerate(["Sen", "Sel", "Rab", "Kam", "Jum"]))
    return f'<svg width="850" height="330" viewBox="0 0 850 330">{wadah}{hari}</svg>'


def html_sampul(subjudul: str, pil: list[str], tahun: int) -> str:
    warna_pil = [(P["peach"], P["aksen"]), (P["langit_muda"], P["aksen2"]), (P["kuning_muda"], P["peringatan"])]
    pills = "".join(
        f'<span class="pill" style="background:{bg};color:{fg};border-color:{fg}33">{_h.escape(p)}</span>'
        for p, (bg, fg) in zip(pil, warna_pil * 2))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{font_css()}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:850px;height:1100px;overflow:hidden;font-family:Nunito,Inter,sans-serif;color:{P['teks']};
background:{P['krem']};position:relative}}
.blob{{position:absolute;border-radius:50%}}
.titik{{position:absolute;inset:0;background-image:radial-gradient({P['garis']} 2px,transparent 2.5px);background-size:34px 34px;opacity:.7}}
.isi{{position:absolute;left:70px;right:70px;top:78px}}
.tag{{display:inline-block;font-size:19px;font-weight:900;letter-spacing:.14em;color:#fff;background:{P['aksen2']};
padding:8px 16px;border-radius:999px}}
h1{{font-size:168px;line-height:.95;font-weight:900;color:#e2553a;margin-top:26px;letter-spacing:-.01em}}
h2{{font-size:88px;line-height:1;font-weight:900;color:{P['judul']}}}
.sub{{font-size:31px;line-height:1.3;font-weight:800;margin-top:28px;color:{P['teks']};max-width:700px}}
.pills{{margin-top:30px;display:flex;flex-wrap:wrap;gap:14px}}
.pill{{font-size:22px;font-weight:800;padding:11px 22px;border-radius:999px;border:2px solid}}
svg{{position:absolute;left:0;bottom:118px}}
.kaki{{position:absolute;left:70px;right:70px;bottom:46px;display:flex;justify-content:space-between;font-size:23px;
font-weight:800;color:{P['redup']}}}
.kaki b{{color:{P['aksen']}}}
</style></head><body><div class="titik"></div>
<div class="blob" style="width:420px;height:420px;right:-140px;top:-120px;background:{P['peach']}"></div>
<div class="blob" style="width:170px;height:170px;right:70px;top:220px;background:{P['kuning_muda']}"></div>
<div class="blob" style="width:300px;height:300px;left:-130px;bottom:300px;background:{P['langit_muda']}"></div>
<div class="blob" style="width:120px;height:120px;right:110px;bottom:470px;background:{P['lavender_muda']}"></div>
<div class="isi"><div class="tag">EBOOK + KIT PRINTABLE · USIA 6–23 BULAN</div>
<h1>MPASI</h1><h2>IBU BEKERJA</h2>
<div class="sub">{_h.escape(subjudul)}</div><div class="pills">{pills}</div></div>
{_ilustrasi()}
<div class="kaki"><span>Edisi {tahun}</span><b>GoSatSet.xyz</b></div></body></html>"""


def buat_png(html: str, keluar: Path, skala: int) -> Path:
    from playwright.sync_api import sync_playwright
    keluar = Path(keluar)
    keluar.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 850, "height": 1100}, device_scale_factor=skala)
        # Dari file, bukan set_content: halaman about:blank tidak boleh memuat font file://.
        tmp = keluar.parent / f"_{keluar.stem}.html"
        tmp.write_text(html, encoding="utf-8")
        pg.goto(tmp.as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.screenshot(path=str(keluar), full_page=False)
        b.close()
    tmp.unlink()
    return keluar
