"""Banner promosi (standar ebook-pro). Teks banner hanya memakai fakta yang benar tentang buku."""
from __future__ import annotations

import html as _h
from pathlib import Path

from .tema import PALET as P, font_css

DISCLAIMER = "Edukasi dari pedoman WHO, Kemenkes & IDAI · bukan pengganti konsultasi tenaga kesehatan"

BASE_CSS = f"""*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Inter,'DejaVu Sans','Noto Color Emoji',sans-serif;color:{P['teks']};overflow:hidden;position:relative;
background:{P['krem']}}}
.titik{{position:absolute;inset:0;background-image:radial-gradient({P['garis']} 2px,transparent 2.5px);background-size:34px 34px;opacity:.7}}
.blob{{position:absolute;border-radius:50%}}
.book{{position:absolute;perspective:1800px}}
.book .b{{width:100%;height:100%;transform:rotateY(-22deg) rotateX(3deg);position:relative;border-radius:6px 14px 14px 6px;
box-shadow:-24px 34px 60px rgba(46,37,87,.28),0 0 0 1px rgba(46,37,87,.06)}}
.book img{{width:100%;height:100%;display:block;border-radius:6px 14px 14px 6px}}
.book .b:before{{content:'';position:absolute;left:0;top:0;bottom:0;width:5%;
background:linear-gradient(90deg,rgba(46,37,87,.35),rgba(255,255,255,.4),transparent);z-index:2}}
.tag{{display:inline-block;font-family:Nunito,Inter,sans-serif;font-weight:900;letter-spacing:.12em;color:#fff;
background:{P['aksen2']};border-radius:999px}}
h1{{font-family:Nunito,Inter,sans-serif;font-weight:900;line-height:1.05;color:{P['judul']}}}
h1 em{{font-style:normal;color:#e2553a}}
.pill{{display:inline-block;font-family:Nunito,Inter,sans-serif;font-weight:800;border:2px solid;border-radius:999px}}
.cta{{display:inline-block;background:#e2553a;color:#fff;font-family:Nunito,Inter,sans-serif;font-weight:900;border-radius:999px;
box-shadow:0 6px 0 {P['kuning']}}}
.disc{{position:absolute;color:{P['redup']};background:{P['krem']};padding:4px 12px;margin-left:-12px;border-radius:10px;z-index:3}}
.wave{{position:absolute;left:0;bottom:0;width:100%}}
"""

KARTU_WARNA = [P["coral"], P["langit"], P["kuning"], P["lavender"]]
PIL_WARNA = [(P["peach"], P["aksen"]), (P["langit_muda"], P["aksen2"]), (P["kuning_muda"], P["peringatan"]),
             (P["lavender_muda"], P["judul"])]


def _pill(teks: str, i: int, gaya: str) -> str:
    bg, fg = PIL_WARNA[i % len(PIL_WARNA)]
    return f'<span class="pill" style="background:{bg};color:{fg};border-color:{fg}40;{gaya}">{_h.escape(teks)}</span>'


def _wave(w: int, h: int) -> str:
    return (f'<svg class="wave" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><path d="M0 {h * .85} '
            f'C {w * .25} {h * .7}, {w * .45} {h * .9}, {w * .65} {h * .55} S {w * .9} {h * .35}, {w} {h * .2}" '
            f'stroke="{P['kuning']}" stroke-width="6" fill="none" stroke-dasharray="2 14" stroke-linecap="round"/></svg>')


def _blobs(w: int, h: int) -> str:
    return (f'<div class="blob" style="width:{int(w*.45)}px;height:{int(w*.45)}px;right:-{int(w*.12)}px;top:-{int(w*.12)}px;background:{P['peach']}"></div>'
            f'<div class="blob" style="width:{int(w*.22)}px;height:{int(w*.22)}px;left:-{int(w*.08)}px;bottom:{int(h*.18)}px;background:{P['langit_muda']}"></div>'
            f'<div class="blob" style="width:{int(w*.1)}px;height:{int(w*.1)}px;right:{int(w*.4)}px;bottom:{int(h*.08)}px;background:{P['kuning_muda']}"></div>')


def _book(cover: Path, left: int, top: int, w: int) -> str:
    return (f'<div class="book" style="left:{left}px;top:{top}px;width:{w}px;height:{int(w * 1100 / 850)}px">'
            f'<div class="b"><img src="{cover.as_uri()}"></div></div>')


def _doc(w: int, h: int, isi: str) -> str:
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{font_css()}{BASE_CSS}body{{width:{w}px;height:{h}px}}"
            f"</style></head><body><div class='titik'></div>{_blobs(w, h)}{_wave(w, int(h * .35))}{isi}</body></html>")


def banners(cover: Path, fakta: dict) -> dict[str, tuple[int, int, str]]:
    """fakta: halaman, bab, minggu_menu, sumber (angka nyata dari build)."""
    hal, bab, sumber = fakta["halaman"], fakta["bab"], fakta["sumber"]
    pills4 = ["Menu 4 minggu + belanja", "Kartu SOP pengasuh", "Label, log & template WA", f"{sumber} sumber resmi"]
    out: dict[str, tuple[int, int, str]] = {}

    p = "".join(_pill(x, i, "font-size:24px;padding:10px 20px;margin:0 10px 12px 0") for i, x in enumerate(pills4))
    out["01-feed-square-1080x1080"] = (1080, 1080, _doc(1080, 1080,
        f'<div style="position:absolute;left:64px;top:70px;width:560px">'
        f'<div class="tag" style="font-size:22px;padding:8px 18px">IBU BEKERJA · ANAK 6–23 BULAN</div>'
        f'<h1 style="font-size:70px;margin-top:22px">Masak <em>sekali</em><br>seminggu.<br>Pengasuh tinggal<br>ikut <em>kartu</em>.</h1>'
        f'<div style="margin-top:30px">{p}</div>'
        f'<div class="cta" style="font-size:30px;padding:18px 30px;margin-top:20px">Ambil ebooknya →</div></div>'
        f'{_book(cover, 640, 190, 380)}'
        f'<div class="disc" style="left:64px;right:64px;bottom:34px;font-size:18px">{DISCLAIMER}</div>'))

    ben = ["Menu 4 minggu, protein hewani setiap hari", "Kartu SOP untuk nenek & pengasuh",
           "Aturan simpan & panaskan yang aman", "Kartu mitos vs pedoman untuk nenek"]
    li = "".join(f'<div style="font-size:38px;font-weight:700;margin:18px 0"><span style="color:#e2553a">✔</span> {_h.escape(x)}</div>' for x in ben)
    out["02-story-1080x1920"] = (1080, 1920, _doc(1080, 1920,
        f'{_book(cover, 300, 250, 470)}'
        f'<div style="position:absolute;left:80px;right:80px;top:930px">'
        f'<div class="tag" style="font-size:26px;padding:10px 22px">EBOOK + KIT PRINTABLE</div>'
        f'<h1 style="font-size:84px;margin:18px 0 24px">MPASI <em>Ibu Bekerja</em></h1>{li}'
        f'<div class="cta" style="font-size:40px;padding:22px 40px;margin-top:26px">Ketuk link di bio →</div></div>'
        f'<div class="disc" style="left:80px;right:80px;bottom:240px;font-size:22px">{DISCLAIMER}</div>'))

    out["03-landscape-1200x630"] = (1200, 630, _doc(1200, 630,
        f'<div style="position:absolute;left:60px;top:60px;width:700px">'
        f'<div class="tag" style="font-size:18px;padding:7px 16px">EBOOK PARENTING · GOSATSET.XYZ</div>'
        f'<h1 style="font-size:64px;margin-top:16px">MPASI <em>Ibu Bekerja</em></h1>'
        f'<div style="font-size:26px;font-weight:600;margin-top:16px;line-height:1.35">Sistem masak seminggu sekali + Kartu SOP '
        f'untuk nenek & pengasuh</div>'
        f'<div style="font-size:20px;color:{P["redup"]};margin-top:16px">{hal} halaman · {bab} bab · menu 4 minggu · kit printable</div>'
        f'<div class="cta" style="font-size:24px;padding:14px 26px;margin-top:24px">Lihat isinya →</div></div>'
        f'{_book(cover, 850, 70, 290)}'
        f'<div class="disc" style="left:60px;bottom:22px;font-size:15px">{DISCLAIMER}</div>'))

    out["04-header-web-1920x600"] = (1920, 600, _doc(1920, 600,
        f'<div style="position:absolute;left:110px;top:90px;width:1150px">'
        f'<div class="tag" style="font-size:20px;padding:8px 18px">UNTUK ORANG TUA BEKERJA DENGAN ANAK 6–23 BULAN</div>'
        f'<h1 style="font-size:84px;margin-top:16px">MPASI <em>Ibu Bekerja</em></h1>'
        f'<div style="font-size:32px;font-weight:600;margin-top:14px">Masak sekali di hari Minggu. Pengasuh tinggal ikut kartu.</div>'
        f'<div style="margin-top:26px">{_pill("Menu 4 minggu", 0, "font-size:22px;padding:10px 20px;margin-right:12px")}'
        f'{_pill("Kartu SOP pengasuh", 1, "font-size:22px;padding:10px 20px;margin-right:22px")}'
        f'<span class="cta" style="font-size:26px;padding:14px 28px">Dapatkan sekarang →</span></div></div>'
        f'{_book(cover, 1500, 70, 300)}'
        f'<div class="disc" style="left:110px;bottom:24px;font-size:17px">{DISCLAIMER}</div>'))

    cards = [("1", "Patokan resmi", "Tekstur, frekuensi & porsi per usia dari Kemenkes"),
             ("2", "Sistem Minggu", "Masak komponen sekali, bekukan per porsi"),
             ("3", "Aman disimpan", "Batas kulkas & freezer, cara cairkan & panaskan"),
             ("4", "Serah terima", "Kartu pengasuh, log harian, laporan WhatsApp"),
             ("5", "Damai dengan nenek", "Kartu mitos vs pedoman + contoh kalimat"),
             ("6", "ASI perah", "Batas aman & hak ibu bekerja (UU KIA 2024)")]
    kotak = "".join(
        f'<div style="background:#fff;border:3px solid {KARTU_WARNA[i % 4]};border-radius:26px;padding:26px;'
        f'box-shadow:0 8px 0 {KARTU_WARNA[i % 4]}55">'
        f'<div style="width:62px;height:62px;border-radius:50%;background:{KARTU_WARNA[i % 4]};color:#fff;'
        f'font:900 36px/62px Nunito,Inter,sans-serif;text-align:center">{n}</div>'
        f'<div style="font-family:Nunito,Inter,sans-serif;font-size:32px;font-weight:900;margin-top:12px;color:{P["judul"]}">{_h.escape(t)}</div>'
        f'<div style="font-size:24px;color:{P["redup"]};margin-top:8px;line-height:1.3">{_h.escape(d)}</div></div>'
        for i, (n, t, d) in enumerate(cards))
    out["05-portrait-isi-1080x1350"] = (1080, 1350, _doc(1080, 1350,
        f'<div style="position:absolute;left:64px;right:64px;top:70px">'
        f'<div class="tag" style="font-size:22px;padding:8px 18px">MPASI IBU BEKERJA</div>'
        f'<h1 style="font-size:66px;margin:14px 0 36px">Apa yang kamu <em>pelajari</em>?</h1>'
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:22px">{kotak}</div></div>'
        f'<div class="disc" style="left:64px;right:64px;bottom:40px;font-size:19px">{DISCLAIMER}</div>'))
    return out


def render_banners(cover: Path, fakta: dict, keluar: Path) -> list[Path]:
    from playwright.sync_api import sync_playwright
    keluar.mkdir(parents=True, exist_ok=True)
    hasil = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for nama, (w, h, html) in banners(cover, fakta).items():
            f = keluar / f"{nama}.html"
            f.write_text(html, encoding="utf-8")
            pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
            pg.goto(f.as_uri(), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            out = keluar / f"{nama}.png"
            pg.screenshot(path=str(out))
            pg.close()
            f.unlink()
            hasil.append(out)
        b.close()
    return hasil
