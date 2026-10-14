#!/usr/bin/env python3
"""Render book.html -> PDF (A4), add bookmarks, page labels, metadata."""
import sys, pathlib, logging
logging.disable(logging.WARNING)
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter
import build_book as BB

HERE = pathlib.Path(__file__).resolve().parent
out = pathlib.Path(sys.argv[1])
html, marks, n = BB.build()
src = HERE / "book.html"; src.write_text(html, encoding="utf-8")
(HERE / "cover.html").write_text(BB.cover_page_html(), encoding="utf-8")
tmp = HERE / "raw.pdf"
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    pg = b.new_page()
    pg.goto(src.as_uri(), wait_until="networkidle")
    pg.evaluate("document.fonts.ready")
    over = pg.evaluate("""() => [...document.querySelectorAll('.page .inner')].map((el,i)=>[i, el.scrollHeight - el.clientHeight]).filter(x=>x[1]>1)""")
    print("overflowing pages (index, px):", over)
    pg.pdf(path=str(tmp), format="A4", print_background=True, prefer_css_page_size=True)
    b.close()
r = PdfReader(str(tmp))
assert len(r.pages) == n, (len(r.pages), n)
w = PdfWriter(); w.append(r)
w.set_page_label(0, 0, prefix="Cover")
w.set_page_label(1, n - 1, style="/D", start=1)
w.add_outline_item("Cover", 0)
for lab, i in marks:
    w.add_outline_item(lab, i)
w.add_metadata({"/Title": f"{BB.TITLE}: {BB.SUBTITLE}", "/Author": "GoSatSet", "/Subject": "Jurnal & tracker 30 hari 7 Kebiasaan Anak Indonesia Hebat, siap cetak A4", "/Creator": "GoSatSet.xyz"})
out.parent.mkdir(parents=True, exist_ok=True)
with open(out, "wb") as f: w.write(f)
print("done", out, n, "pages")
