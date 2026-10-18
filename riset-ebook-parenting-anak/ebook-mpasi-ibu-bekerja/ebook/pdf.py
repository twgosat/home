"""HTML -> PDF lewat Chromium headless (Playwright). Diadaptasi dari builder ebook-pro:
render dua kali untuk mengisi nomor halaman daftar isi, sampul full-bleed, footer bertaut,
label halaman, bookmark per bab, dan metadata."""
from __future__ import annotations

import json
import logging
import re
import tempfile
from pathlib import Path

logging.disable(logging.WARNING)

# Chromium tidak mengenal kata kunci A6 di @page, jadi semua ukuran ditulis dalam mm/in.
UKURAN = {"A4": "210mm 297mm", "A4L": "297mm 210mm", "A5": "148mm 210mm", "A6": "105mm 148mm",
          "Letter": "8.5in 11in"}


def html_ke_pdf(html: str, keluar: Path, ukuran: str, footer_html: str | None = None) -> Path:
    """Render satu dokumen HTML. `ukuran` ∈ A4 | A4L (landscape) | A5 | A6 | Letter.
    Ukuran halaman sebenarnya diatur lewat @page yang disisipkan di sini."""
    from playwright.sync_api import sync_playwright

    if ukuran not in UKURAN:
        raise ValueError(f"ukuran tidak dikenal: {ukuran}")
    page_css = UKURAN[ukuran]
    sisip = f"<style>@page {{ size: {page_css}; }} html,body{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}</style>"
    html = html.replace("</head>", sisip + "</head>", 1) if "</head>" in html else sisip + html
    keluar = Path(keluar)
    keluar.parent.mkdir(parents=True, exist_ok=True)
    kerja = Path(tempfile.mkdtemp(prefix="ebook_"))
    f = kerja / "doc.html"
    f.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 816, "height": 1056})
        pg.goto(f.as_uri(), wait_until="networkidle")
        pg.emulate_media(media="print")
        pg.evaluate("document.fonts.ready")
        opsi = dict(path=str(keluar), print_background=True, prefer_css_page_size=True)
        if footer_html:
            opsi.update(display_header_footer=True, header_template="<span></span>", footer_template=footer_html)
        pg.pdf(**opsi)
        b.close()
    return keluar


def _penanda_js() -> str:
    return """(sel) => { sel.forEach((s, i) => { const el = document.querySelector(s); if (!el) return;
      const m = document.createElement('span'); m.textContent = 'QQMARK' + i + 'QQ';
      m.style.cssText = 'position:absolute;top:0;left:0;font-size:2px;line-height:2px;color:rgba(128,128,128,0.02);white-space:nowrap';
      if (getComputedStyle(el).position === 'static') el.style.position = 'relative'; el.prepend(m); }); }"""


def _awal_bab(pdf_path: Path) -> tuple[dict[int, int], int]:
    import pdfplumber
    awal: dict[int, int] = {}
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages):
            for m in re.finditer(r"QQMARK(\d+)QQ", page.extract_text() or ""):
                awal.setdefault(int(m.group(1)), i + 1)
        return awal, len(pdf.pages)


def _render_badan(html: str, keluar: Path, bab: list[tuple[str, str]], footer: str) -> None:
    from playwright.sync_api import sync_playwright
    kerja = keluar.parent
    f = kerja / "badan.html"
    f.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 816, "height": 1056})
        pg.goto(f.as_uri(), wait_until="networkidle")
        pg.emulate_media(media="print")
        pg.evaluate("document.fonts.ready")
        pg.evaluate(_penanda_js(), [s for s, _ in bab])
        pg.pdf(path=str(keluar), format="Letter", print_background=True, prefer_css_page_size=True,
               display_header_footer=True, header_template="<span></span>", footer_template=footer)
        b.close()


def rakit_ebook(html: str, keluar: Path, judul: str, sampul_png: Path | None, bab: list[tuple[str, str]],
                footer_teks: str, footer_url: str, metadata: dict[str, str]) -> dict:
    """Bangun ebook Letter: sampul + badan bernomor. `bab` = [(selector, label bookmark)].
    Isi `<span class="pg">` di dalam `a[href="#id"]` daftar isi dengan 'hal X'."""
    from pypdf import PdfReader, PdfWriter
    from pypdf.annotations import Link
    import pdfplumber

    keluar = Path(keluar)
    kerja = Path(tempfile.mkdtemp(prefix="ebook_"))
    footer = ('<div style="width:100%;font-family:Inter,Helvetica,sans-serif;font-size:8px;color:#64748b;'
              'padding:0 0.55in;display:flex;justify-content:space-between;">'
              f'<span>{footer_teks}</span><span class="pageNumber"></span></div>')
    p1 = kerja / "pass1.pdf"
    _render_badan(html, p1, bab, footer)
    awal, total = _awal_bab(p1)
    isi = {bab[i][0]: f"hal {n}" for i, n in awal.items()}
    js = (f"<script>document.addEventListener('DOMContentLoaded',()=>{{const R={json.dumps(isi)};"
          "for (const [sel,t] of Object.entries(R)) { const el=document.querySelector(sel); if(!el||!el.id) continue;"
          "document.querySelectorAll('a[href=\"#'+el.id+'\"] .pg').forEach(s=>s.textContent=t); } });</script>")
    p2 = kerja / "pass2.pdf"
    _render_badan(html.replace("</body>", js + "</body>", 1), p2, bab, footer)
    awal2, total2 = _awal_bab(p2)

    w = PdfWriter()
    geser = 0
    if sampul_png:
        sp = kerja / "sampul.pdf"
        html_ke_pdf(f"<html><head><style>@page{{margin:0}}html,body{{margin:0}}img{{display:block;width:100vw;height:100vh;"
                    f"object-fit:cover}}</style></head><body><img src='{Path(sampul_png).as_uri()}'></body></html>",
                    sp, "Letter")
        w.append(str(sp))
        geser = 1
    for halaman in PdfReader(str(p2)).pages:
        w.add_page(halaman)
    tautan = 0
    with pdfplumber.open(str(p2)) as pdf:
        hal = pdf.pages[0]
        H = float(hal.height)
        kata = [k for k in hal.extract_words() if k["top"] > H - 0.75 * 72]
        akhir = footer_teks.split()[-1]
        idx = next((i for i, k in enumerate(kata) if akhir in k["text"]), None)
        if idx is not None:
            baris = kata[: idx + 1]
            rect = (min(k["x0"] for k in baris) - 2, H - max(k["bottom"] for k in baris) - 2,
                    max(k["x1"] for k in baris) + 2, H - min(k["top"] for k in baris) + 2)
            for i in range(geser, len(w.pages)):
                w.add_annotation(page_number=i, annotation=Link(rect=rect, url=footer_url))
                tautan += 1
    if geser:
        w.set_page_label(0, 0, prefix="Sampul")
        w.add_outline_item("Sampul", 0)
    w.set_page_label(geser, len(w.pages) - 1, style="/D", start=1)
    for i in sorted(awal2, key=awal2.get):
        w.add_outline_item(bab[i][1], awal2[i] - 1 + geser)
    w.add_metadata({"/Title": judul, **metadata})
    keluar.parent.mkdir(parents=True, exist_ok=True)
    with open(keluar, "wb") as fh:
        w.write(fh)
    return {"halaman": len(w.pages), "halaman_badan": total2, "awal_bab": {bab[i][1]: n for i, n in awal2.items()},
            "geser_antar_pass": awal != awal2, "tautan_footer": tautan}


def gabung_pdf(bagian: list[Path], keluar: Path) -> Path:
    from pypdf import PdfWriter
    w = PdfWriter()
    for b in bagian:
        w.append(str(b))
    keluar.parent.mkdir(parents=True, exist_ok=True)
    with open(keluar, "wb") as fh:
        w.write(fh)
    return keluar
