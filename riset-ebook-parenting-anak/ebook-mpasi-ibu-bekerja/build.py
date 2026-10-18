#!/usr/bin/env python3
"""Bangun paket ebook MPASI Ibu Bekerja.

    python build.py                    # semua: ebook, kartu HP, kit cetak, lead magnet, verifikasi
    python build.py --hanya kartu      # kartu | kit | lead-magnet | ebook

Build berhenti (ValueError) bila data, menu, atau naskah tidak lolos validasi.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html as _h
from pathlib import Path

import yaml

from ebook.data import Data, muat_data, validasi_data
from ebook.kartu import (render_kartu, render_kartu_asi, render_label, render_log, render_mitos, teks_wa)
from ebook.menu import cek_menu, daftar_belanja, total_menit
from ebook.naskah import cek_naskah
from ebook.pdf import gabung_pdf, html_ke_pdf, rakit_ebook
from ebook.promo import render_banners
from ebook.render import fakta_html, ref, render_bab
from ebook.sampul import buat_png, html_sampul
from ebook.tema import PALET as P, font_css
from ebook.uji_masak import Klaim, klaim_waktu
from ebook.verifikasi import tulis_verifikasi

ROOT = Path(__file__).resolve().parent
JUDUL = "MPASI Ibu Bekerja"
SUB_SOP = "+ Kartu SOP untuk Nenek & Pengasuh"
BRAND_URL = "https://gosatset.xyz/"
TAHUN = 2026
USIA = ["6-8", "9-11", "12-23"]


def siapkan(root: Path) -> tuple[Data, dict, Klaim]:
    data = muat_data(root / "data")
    menu = yaml.safe_load((root / "data" / "menu.yaml").read_text(encoding="utf-8"))
    err = validasi_data(data) + cek_menu(menu, data)
    if err:
        raise ValueError("Validasi gagal:\n" + "\n".join(err))
    return data, menu, klaim_waktu(root / "data" / "uji-masak.csv")


def subjudul(klaim: Klaim) -> str:
    return f"{klaim.teks_judul} {SUB_SOP}"


# ---------------------------------------------------------------- blok yang dibangkitkan dari data
def tabel_patokan(data: Data) -> str:
    baris = "".join(
        f"<tr><td><b>{u.replace('-', '–')} bulan</b></td><td>{fakta_html(data, f'tekstur.{u}')}</td>"
        f"<td>{fakta_html(data, f'frekuensi.{u}')}</td><td>{fakta_html(data, f'porsi.{u}')}</td>"
        f"<td>{fakta_html(data, f'energi.{u}')}</td></tr>" for u in USIA)
    return ("<table><thead><tr><th>Usia</th><th>Tekstur</th><th>Berapa kali</th><th>Porsi sekali makan</th>"
            f"<th>Kebutuhan energi dari MPASI</th></tr></thead><tbody>{baris}</tbody></table>")


def rincian_waktu(menu: dict) -> str:
    w = menu["minggu"][0]
    baris = [f"<tr><td>Persiapan: cuci, kupas, potong semua bahan</td><td>{w['menit_persiapan']}</td></tr>"]
    baris += [f"<tr><td>{_h.escape(k['nama'])}</td><td>{k['menit_aktif']}</td></tr>" for k in w["komponen"] if k["menit_aktif"]]
    baris.append(f"<tr><td>Penutup: haluskan/cincang per usia, bagi porsi, beri label, bekukan, cuci alat</td>"
                 f"<td>{w['menit_penutup']}</td></tr>")
    baris.append(f"<tr class='waktu-total'><td>Total waktu kerja aktif (estimasi)</td><td>{total_menit(w)}</td></tr>")
    return ("<table><thead><tr><th>Langkah (minggu 1)</th><th>Menit aktif</th></tr></thead><tbody>"
            + "".join(baris) + "</tbody></table>")


def tabel_menu(menu: dict) -> str:
    out = []
    for w in menu["minggu"]:
        komp = {k["id"]: k for k in w["komponen"]}
        hari = "".join(
            f"<tr><td><b>{h['hari']}</b></td><td>{', '.join(_h.escape(komp[k]['nama']) for k in h['makan'])}</td></tr>"
            for h in w["hari"])
        cara = "".join(
            f"<tr><td>{_h.escape(k['nama'])}</td><td>{_h.escape(k['cara'])}</td>"
            f"<td>{'segar' if k['simpan'] == 'segar' else k['simpan']}</td></tr>" for k in w["komponen"])
        belanja = "".join(f"<li>{_h.escape(b)}: {_h.escape(j)}</li>" for b, j in daftar_belanja(menu, w["nomor"]))
        out.append(
            f"<div class='minggu'><h3>Minggu {w['nomor']}: {_h.escape(w['tema'])}</h3>"
            f"<table><thead><tr><th>Hari</th><th>Isi menu (dipakai untuk semua jam makan hari itu)</th></tr></thead>"
            f"<tbody>{hari}</tbody></table>"
            f"<table class='komponen'><thead><tr><th>Komponen</th><th>Cara masak hari Minggu</th><th>Simpan</th></tr></thead>"
            f"<tbody>{cara}</tbody></table>"
            f"<p><b>Daftar belanja (perkiraan untuk 1 anak, 5 hari):</b></p><ul class='belanja'>{belanja}</ul>"
            f"<p class='kecil'>Estimasi waktu kerja aktif minggu ini: {total_menit(w)} menit.</p></div>")
    return "".join(out)


def blok(data: Data, menu: dict, klaim: Klaim) -> dict[str, str]:
    maks = max(total_menit(w) for w in menu["minggu"])
    if klaim.boleh_klaim_2_jam:
        status = (f"Sudah diuji {klaim.jumlah_uji} kali di dapur nyata dengan median "
                  f"{klaim.median_menit_aktif} menit kerja aktif.")
    else:
        status = ("Angka ini adalah estimasi dari rencana menu dan belum diuji di dapur nyata. Catat waktumu sendiri "
                  "selama 3 minggu pertama; banyak dapur lebih lambat di minggu pertama.")
    b = {
        "judul_sistem": _h.escape(klaim.teks_judul),
        "estimasi_menit": f"{maks} menit",
        "status_uji": status,
        "tabel_patokan": tabel_patokan(data),
        "rincian_waktu": rincian_waktu(menu),
        "menu_4_minggu": tabel_menu(menu),
        "mitos": f"<div class='lampiran-kartu'>{render_mitos(data)}</div>",
        "asi": f"<div class='lampiran-kartu'>{render_kartu_asi(data)}</div>",
        "wa_contoh": f"<div class='wa'>{_h.escape(teks_wa(data, '9-11'))}</div>",
        "label_contoh": f"<div class='lampiran-kartu'>{render_label(data, jumlah=2)}</div>",
        "log_contoh": f"<div class='lampiran-kartu'>{render_log()}</div>",
    }
    for u in USIA:
        b[f"kartu_{u.replace('-', '_')}"] = f"<div class='lampiran-kartu'>{render_kartu(data, u)}</div>"
    return b


# ---------------------------------------------------------------- ebook
def _kepala_bab(no: int | str, bagian: str, judul: str) -> str:
    return (f"<div class='bab-kepala'><div class='bab-no'>{no}</div><div><div class='bab-bagian'>{_h.escape(bagian)}</div>"
            f"<h1 class='bab-judul'>{_h.escape(judul)}</h1></div></div>")


def html_ebook(root: Path, data: Data, menu: dict, klaim: Klaim) -> tuple[str, list[tuple[str, str]], list]:
    blk = blok(data, menu, klaim)
    babs = [render_bab(f.read_text(encoding="utf-8"), data, blk) for f in sorted((root / "naskah").glob("*.md"))]
    bagian_bab, isi, toc, bagian_lalu = [], [], [], None
    for i, bab in enumerate(babs, start=1):
        sid = f"b{i}"
        label = f"Bab {bab.nomor} — {bab.judul}"
        bagian_bab.append((f"#{sid}", label))
        if bab.bagian != bagian_lalu:
            toc.append(f"<div class='bagian'>{_h.escape(bab.bagian)}</div>")
            bagian_lalu = bab.bagian
        toc.append(f"<a href='#{sid}'><span>{bab.nomor}. {_h.escape(bab.judul)}</span><span class='pg'></span></a>")
        isi.append(f"<section class='chapter' id='{sid}'>{_kepala_bab(bab.nomor, bab.bagian, bab.judul)}{bab.html}</section>")
    # Lampiran: kit printable dalam bentuk kotak
    lamp_id = f"b{len(babs) + 1}"
    kartu = "".join(blk[f"kartu_{u.replace('-', '_')}"] for u in USIA)
    isi.append(f"<section class='chapter' id='{lamp_id}'>{_kepala_bab('L', 'Lampiran', 'Kit printable (pratinjau)')}"
               "<p>Versi siap pakai ada di bagian <b>BONUS</b> setelah halaman penutup: <b>Kartu Pengasuh (HP)</b> untuk "
               "dibaca di ponsel dan <b>Kit Cetak A4</b> untuk dicetak, dilipat dua, dan ditempel di kulkas.</p>"
               f"{kartu}{blk['label_contoh']}{blk['log_contoh']}</section>")
    bagian_bab.append((f"#{lamp_id}", "Lampiran — Kit printable"))
    toc.append("<div class='bagian'>Penutup</div>")
    toc.append(f"<a href='#{lamp_id}'><span>Lampiran: kit printable</span><span class='pg'></span></a>")
    # Referensi
    ref_id = f"b{len(babs) + 2}"
    daftar = "".join(
        f"<li>{_h.escape(s.get('penerbit', ''))}. <i>{_h.escape(s['judul'])}</i> ({s.get('tahun', 'n.d.')}). "
        f"<span class='kecil'>[{s['jenis']}, bukti {s['kekuatan']}]</span><br><a href='{s['url']}'>{_h.escape(s['url'])}</a></li>"
        for s in data.sumber.values())
    isi.append(f"<section class='chapter' id='{ref_id}'>{_kepala_bab('R', 'Penutup', 'Referensi')}"
               "<p>Nomor di bawah sama dengan nomor kecil <sup class='ref'>[n]</sup> di dalam buku. "
               "Label <i>bukti</i> menunjukkan kekuatan sumber: <b>kuat</b> = lembaga resmi; <b>sedang</b> = jurnal atau "
               "media yang mengutip lembaga resmi; <b>lemah</b> = sumber pendukung yang hanya dipakai bersama sumber lain "
               "atau ditandai sebagai pilihan konservatif.</p>"
               f"<ol class='referensi'>{daftar}</ol></section>")
    bagian_bab.append((f"#{ref_id}", "Referensi"))
    toc.append(f"<a href='#{ref_id}'><span>Referensi</span><span class='pg'></span></a>")
    toc.append("<a><span><b>BONUS</b>: Kartu Pengasuh, Kit Cetak A4, Kartu Porsi MPASI</span>"
               "<span class='pg'>setelah penutup</span></a>")

    depan = f"""<section class="front">
<div class="brand">GOSATSET.XYZ · EBOOK PARENTING</div>
<h1>{JUDUL}</h1><div class="subjudul">{_h.escape(subjudul(klaim))}</div>
<p class="lead">Untuk ibu dan ayah yang bekerja, dengan anak usia 6–23 bulan yang diasuh nenek, pengasuh, atau daycare.
Masak sekali di hari Minggu, pengasuh tinggal mengikuti kartu. Setiap angka di buku ini punya sumber resmi.</p>
<div class="grid2"><div class="card"><b>Apa yang kamu dapat</b><ul><li>Menu 4 minggu + daftar belanja</li>
<li>Kartu SOP pengasuh per usia (versi HP & cetak)</li><li>Label wadah, log harian, template WhatsApp</li>
<li>Kartu mitos vs pedoman untuk nenek</li><li>Kartu batas aman ASI perah</li><li><b>Bonus</b> siap cetak di akhir buku</li></ul></div>
<div class="card"><b>Cara memakai</b><ul><li>Baca Bab 1–4 sekali</li><li>Pilih menu minggu ini di Bab 5</li>
<li>Cetak kartu & label dari Bonus Kit Cetak A4</li><li>Serahkan kartu ke pengasuh (Bab 6–7)</li>
<li>Cek nomor [n] di Referensi bila ragu</li></ul></div></div>
<div class="toc">{''.join(toc)}</div>
<div class="disclaimer"><b>Penting:</b> Ebook ini adalah panduan edukasi yang disusun dari pedoman WHO, Kementerian Kesehatan,
dan IDAI. Ebook ini <b>tidak ditinjau oleh ahli gizi atau dokter anak</b> dan bukan pengganti konsultasi tenaga kesehatan.
Bila anak sakit, berat badannya tidak naik, atau ada dugaan alergi, periksakan ke dokter, bidan, atau puskesmas.</div>
</section>"""
    penutup = f"""<section class="penutup"><h2>Terima kasih</h2>
<p>Semoga dapur hari Minggu jadi lebih tenang, dan pengasuh di rumah lebih percaya diri.</p>
<p class="url">www.GoSatSet.xyz</p><p class="kecil">© {TAHUN} www.GoSatSet.xyz · Seluruh angka bersumber; lihat Referensi.</p></section>"""
    css = (root / "templates" / "ebook.css").read_text(encoding="utf-8")
    html = (f"<!doctype html><html lang='id'><head><meta charset='utf-8'><title>{JUDUL}</title><style>{font_css()}{css}</style>"
            f"</head><body>{depan}{''.join(isi)}{penutup}</body></html>")
    return html, bagian_bab, babs


# ---------------------------------------------------------------- printable
def _dok(root: Path, isi: str, ekstra_css: str = "") -> str:
    css = (root / "templates" / "kartu.css").read_text(encoding="utf-8")
    ebook_css = (root / "templates" / "ebook.css").read_text(encoding="utf-8")
    return (f"<!doctype html><html lang='id'><head><meta charset='utf-8'><style>{font_css()}{ebook_css}\n{css}\n{ekstra_css}"
            f"</style></head><body>{isi}</body></html>")


def bangun_kartu_hp(root: Path, data: Data, keluar: Path) -> Path:
    isi = "".join(render_kartu(data, u) for u in USIA)
    return html_ke_pdf(_dok(root, isi, "@page{margin:0} .kartu:last-child{break-after:auto}"), keluar, "A5")


def bangun_kit(root: Path, data: Data, keluar: Path) -> Path:
    tmp = keluar.parent / "_kit"
    lipat = "".join(f"<div class='lipat'>{render_kartu(data, u)}</div>" for u in USIA)
    a = html_ke_pdf(_dok(root, lipat, "@page{margin:0} .lipat:last-child{break-after:auto}"), tmp / "lipat.pdf", "A4L")
    lembar = (render_label(data) + "<div style='break-before:page'></div>" + render_log()
              + "<div style='break-before:page'></div>" + render_mitos(data)
              + "<div style='break-before:page'></div>" + render_kartu_asi(data))
    b = html_ke_pdf(_dok(root, lembar, "@page{margin:14mm} body{font-size:13pt}"), tmp / "lembar.pdf", "A4")
    return gabung_pdf([a, b], keluar)


def bangun_lead(root: Path, data: Data, klaim: Klaim, keluar: Path) -> Path:
    depan = "".join(render_kartu(data, u).split('<section class="kartu belakang">')[0] for u in USIA)
    promo = (f"<section class='kartu'><div class='tag'>GRATIS DARI GOSATSET.XYZ</div><h2>Mau sistem lengkapnya?</h2>"
             f"<p>Ebook <b>{JUDUL}: {_h.escape(subjudul(klaim))}</b> berisi menu 4 minggu, daftar belanja, kartu langkah "
             "aman untuk pengasuh, label wadah, log harian, kartu mitos untuk nenek, dan kartu ASI perah.</p>"
             "<p><b>gosatset.xyz</b></p><div class='kaki'>Panduan umum dari pedoman resmi, bukan pengganti konsultasi "
             "tenaga kesehatan.</div></section>")
    return html_ke_pdf(_dok(root, depan + promo, "@page{margin:0} .kartu:last-child{break-after:auto}"), keluar, "A5")


# ---------------------------------------------------------------- gabungan: ebook + pembatas + bonus
def html_pembatas(root: Path, bonus: list[tuple[str, str, str, int, int]]) -> str:
    """bonus: (nama, ukuran, kegunaan, hal_awal, hal_akhir) — nomor halaman = penomoran viewer setelah Sampul."""
    warna = [P["coral"], P["langit"], P["kuning"]]
    kartu = "".join(
        f"<div class='bonus'><div class='no' style='background:{warna[i % 3]}'>{i + 1}</div><div>"
        f"<div class='nm'>{_h.escape(nama)}</div><div class='ket'>{_h.escape(ukuran)} · {_h.escape(guna)}</div></div>"
        f"<div class='hal'>hal {a}–{z}</div></div>"
        for i, (nama, ukuran, guna, a, z) in enumerate(bonus))
    hadiah = (f"<svg width='190' height='170' viewBox='0 0 190 170'><rect x='20' y='62' width='150' height='100' rx='14' "
              f"fill='{P['coral']}'/><rect x='10' y='42' width='170' height='34' rx='10' fill='#e2553a'/>"
              f"<rect x='84' y='42' width='22' height='120' fill='{P['kuning']}'/>"
              f"<path d='M95 42 C70 5 35 20 60 42 Z M95 42 C120 5 155 20 130 42 Z' fill='{P['kuning']}' stroke='#e0a800' stroke-width='3'/>"
              f"<circle cx='30' cy='20' r='6' fill='{P['langit']}'/><circle cx='165' cy='14' r='5' fill='{P['lavender']}'/>"
              f"<circle cx='178' cy='70' r='4' fill='{P['langit']}'/></svg>")
    css = (root / "templates" / "ebook.css").read_text(encoding="utf-8")
    return f"""<!doctype html><html lang='id'><head><meta charset='utf-8'><style>{font_css()}{css}
@page{{size:Letter;margin:0}} body{{margin:0}} .pembatas svg{{display:block;margin:0 auto}}
.pembatas{{width:8.5in;height:11in;padding:1.1in 0.9in;position:relative;overflow:hidden;text-align:center}}
.pita{{position:absolute;left:0;right:0;top:0;height:.35in;background:linear-gradient(90deg,{P['coral']} 0 33%,{P['kuning']} 33% 66%,{P['langit']} 66%)}}
.label{{display:inline-block;margin-top:18px;font:900 15px Nunito,Inter,sans-serif;letter-spacing:.16em;color:#fff;background:{P['aksen2']};padding:7px 16px;border-radius:999px}}
.besar{{font:900 96px/1 Nunito,Inter,sans-serif;color:#e2553a;margin:14px 0 4px}}
.sub{{font:800 24px Nunito,Inter,sans-serif;color:{P['judul']}}}
.lead2{{max-width:5.8in;margin:16px auto 26px;color:{P['redup']};font-size:14px;line-height:1.6}}
.bonus{{display:flex;align-items:center;gap:16px;text-align:left;background:#fff;border:2px solid {P['garis']};border-radius:18px;
padding:14px 18px;margin:12px auto;max-width:6.2in}}
.bonus .no{{flex:none;width:46px;height:46px;border-radius:50%;color:#fff;font:900 24px/46px Nunito,Inter,sans-serif;text-align:center}}
.bonus .nm{{font:900 19px Nunito,Inter,sans-serif;color:{P['judul']}}}
.bonus .ket{{font-size:13px;color:{P['redup']};margin-top:2px}}
.bonus .hal{{margin-left:auto;font:800 15px Nunito,Inter,sans-serif;color:{P['aksen']};white-space:nowrap}}
.catatan{{max-width:6.2in;margin:22px auto 0;font-size:12px;color:{P['redup']};text-align:left;background:{P['kuning_muda']};
border-radius:12px;padding:10px 14px;line-height:1.55}}
</style></head><body><section class='pembatas'><div class='pita'></div>{hadiah}
<div class='label'>BATAS AKHIR EBOOK UTAMA</div><div class='besar'>BONUS</div>
<div class='sub'>untuk pembeli ebook {JUDUL}</div>
<p class='lead2'>Halaman-halaman setelah ini adalah <b>produk bonus dari pembelian ebook utama</b>: alat siap pakai untuk
pengasuh, nenek, atau daycare. Isinya mengikuti patokan resmi yang sama dengan Bab 2, 4, dan 8.</p>
{kartu}
<div class='catatan'><b>Cara mencetak:</b> pilih nomor halaman bonus di menu cetak. Halaman bonus berukuran berbeda dari
ebook (A5 dan A4) supaya pas dibaca di ponsel atau dicetak; pilih opsi "Sesuaikan dengan kertas / Fit to page" bila
printer memintanya. Kartu lipat Kit Cetak dicetak A4 mendatar lalu dilipat dua.</div>
</section></body></html>"""


def gabung_bonus(root: Path, ebook: Path, kartu: Path, kit: Path, lead: Path, keluar: Path, metadata: dict) -> Path:
    """Satu file: ebook utama → pembatas BONUS → Kartu Pengasuh (HP) → Kit Cetak A4 → Kartu Porsi MPASI
    (tanpa halaman promosi lead magnet, karena pembaca sudah membeli ebook)."""
    from pypdf import PdfReader, PdfWriter
    n = {k: len(PdfReader(str(p)).pages) for k, p in (("e", ebook), ("k", kartu), ("t", kit), ("l", lead))}
    n_lead = n["l"] - 1
    hal_bonus = n["e"]                     # label viewer: Sampul, 1..n_e-1, lalu pembatas = n_e
    a_k = hal_bonus + 1
    a_t = a_k + n["k"]
    a_l = a_t + n["t"]
    daftar = [("Kartu Pengasuh (versi HP)", f"{n['k']} halaman A5", "3 kelompok usia × sisi depan dan belakang", a_k, a_t - 1),
              ("Kit Cetak A4", f"{n['t']} halaman A4", "kartu lipat untuk kulkas, label wadah, log harian, mitos, ASI perah",
               a_t, a_l - 1),
              ("Kartu Porsi MPASI (ringkas)", f"{n_lead} halaman A5", "takaran per usia untuk ditempel atau dibagikan",
               a_l, a_l + n_lead - 1)]
    pemb = html_ke_pdf(html_pembatas(root, daftar), keluar.parent / "_pembatas.pdf", "Letter")
    w = PdfWriter()
    w.append(str(ebook))                   # ikut membawa bookmark dan tautan footer ebook
    idx = len(w.pages)
    w.append(str(pemb), import_outline=False)
    w.append(str(kartu), import_outline=False)
    w.append(str(kit), import_outline=False)
    w.append(str(lead), pages=(0, n_lead), import_outline=False)
    induk = w.add_outline_item("BONUS untuk pembeli ebook", idx)
    w.add_outline_item("Bonus 1 — Kartu Pengasuh (HP)", idx + 1, parent=induk)
    w.add_outline_item("Bonus 2 — Kit Cetak A4", idx + 1 + n["k"], parent=induk)
    w.add_outline_item("Bonus 3 — Kartu Porsi MPASI", idx + 1 + n["k"] + n["t"], parent=induk)
    w.set_page_label(0, 0, prefix="Sampul")
    w.set_page_label(1, len(w.pages) - 1, style="/D", start=1)
    w.add_metadata(metadata)
    with open(keluar, "wb") as fh:
        w.write(fh)
    pemb.unlink()
    return keluar


# ---------------------------------------------------------------- orkestrasi
def bangun(root: Path = ROOT, keluar: Path | None = None, hanya: str | None = None) -> dict[str, Path]:
    """hanya: None (semua) | kartu | kit | lead-magnet | ebook | gabungan (ebook + bonus, tanpa banner)."""
    root = Path(root)
    keluar = Path(keluar or root / "dist")
    data, menu, klaim = siapkan(root)
    hasil: dict[str, Path] = {}
    ingin = (lambda *k: hanya is None or hanya in k)
    if ingin("ebook", "gabungan"):
        err = cek_naskah(root / "naskah", data)
        if err:
            raise ValueError("Naskah tidak lolos:\n" + "\n".join(err))
    if ingin("kartu", "gabungan"):
        hasil["kartu"] = bangun_kartu_hp(root, data, keluar / "Kartu Pengasuh (HP).pdf")
    if ingin("kit", "gabungan"):
        hasil["kit"] = bangun_kit(root, data, keluar / "Kit Cetak A4.pdf")
    if ingin("lead-magnet", "gabungan"):
        hasil["lead"] = bangun_lead(root, data, klaim, keluar / "Gratis - Kartu Porsi MPASI.pdf")
    if ingin("ebook", "gabungan"):
        sampul_html = html_sampul(subjudul(klaim), ["Menu 4 minggu", "Kartu SOP pengasuh", "Semua angka bersumber"], TAHUN)
        sampul = buat_png(sampul_html, keluar / "promo" / "00-cover-HD-2550x3300.png", 3)
        (keluar / "promo" / "sampul.html").write_text(sampul_html, encoding="utf-8")
        html, bab, _ = html_ebook(root, data, menu, klaim)
        (keluar / "ebook.html").write_text(html, encoding="utf-8")
        meta = {"/Title": JUDUL, "/Author": "GoSatSet", "/Subject": subjudul(klaim)}
        info = rakit_ebook(html, keluar / f"{JUDUL} (ebook saja).pdf", JUDUL, sampul, bab, f"{JUDUL} | GoSatSet.xyz",
                           BRAND_URL, {k: v for k, v in meta.items() if k != "/Title"})
        hasil["ebook"] = keluar / f"{JUDUL} (ebook saja).pdf"
        hasil["info"] = info  # type: ignore[assignment]
        if "kartu" in hasil and "kit" in hasil and "lead" in hasil:
            hasil["gabungan"] = gabung_bonus(root, hasil["ebook"], hasil["kartu"], hasil["kit"], hasil["lead"],
                                             keluar / f"{JUDUL}.pdf", meta)
        ver = tulis_verifikasi(data, menu, klaim, JUDUL, dt.date.today().isoformat())
        for tujuan in (keluar / f"Verifikasi_{JUDUL}.md", root / "jualan" / f"Verifikasi_{JUDUL}.md"):
            tujuan.write_text(ver, encoding="utf-8")
        hasil["verifikasi"] = keluar / f"Verifikasi_{JUDUL}.md"
    if ingin("ebook"):
        sampul_mockup = buat_png(sampul_html, keluar / "promo" / "_sampul-2x.png", 2)
        hasil["banner"] = render_banners(sampul_mockup, {"halaman": info["halaman"], "bab": len(bab) - 2,
                                                         "sumber": len(data.sumber)}, keluar / "promo")  # type: ignore[assignment]
        sampul_mockup.unlink()
    return hasil


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--hanya", choices=["kartu", "kit", "lead-magnet", "ebook", "gabungan"])
    a = ap.parse_args()
    for k, v in bangun(hanya=a.hanya).items():
        print(f"{k}: {v}")
