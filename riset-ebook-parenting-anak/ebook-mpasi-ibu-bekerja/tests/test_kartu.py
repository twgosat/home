import re
from pathlib import Path

from ebook.data import muat_data, nilai_fakta
from ebook.kartu import (RENTANG_USIA, render_kartu, render_kartu_asi, render_label, render_log,
                         render_mitos, teks_wa)

ROOT = Path(__file__).resolve().parents[1]
DATA = muat_data(ROOT / "data")
ASING = ("puree", "finger food", "batch", "thawing", "reheat")


def test_kartu_memuat_angka_fakta():
    h = render_kartu(DATA, "9-11")
    for k in ("porsi.9-11", "tekstur.9-11", "frekuensi.9-11"):
        assert nilai_fakta(DATA, k) in h


def test_rentang_usia_tanpa_celah():
    bulan = [b for a, z in RENTANG_USIA for b in range(a, z + 1)]
    assert bulan == list(range(6, 24))


def test_kartu_ada_catatan_transisi():
    assert "menjelang 9 bulan" in render_kartu(DATA, "6-8").lower()
    assert "menjelang 12 bulan" in render_kartu(DATA, "9-11").lower()


def test_font_kartu_minimal_14pt():
    css = (ROOT / "templates" / "kartu.css").read_text(encoding="utf-8")
    ukuran = re.findall(r"font-size:\s*([\d.]+)(\w+)", css)
    assert ukuran, "kartu.css harus menulis font-size"
    for angka, unit in ukuran:
        assert unit == "pt" and float(angka) >= 14, f"font-size {angka}{unit} < 14pt"


def test_tanpa_istilah_asing():
    semua = "".join(render_kartu(DATA, u) for u in ("6-8", "9-11", "12-23")) + render_mitos(DATA)
    for kata in ASING:
        assert kata not in semua.lower()


def test_kartu_ada_disclaimer():
    assert "bukan pengganti konsultasi tenaga kesehatan" in render_kartu(DATA, "12-23")


def test_kartu_aturan_panas():
    h = render_kartu(DATA, "6-8").lower()
    assert nilai_fakta(DATA, "panas.aturan").lower() in h and nilai_fakta(DATA, "cair.aturan") in h


def test_kartu_gula_garam_sesuai_usia():
    assert nilai_fakta(DATA, "gula_garam.bawah_12") in render_kartu(DATA, "9-11").lower()
    assert nilai_fakta(DATA, "hindari.tinggi_gula_garam") in render_kartu(DATA, "12-23").lower()


def test_label_memuat_batas():
    h = render_label(DATA)
    assert "Tanggal masak" in h and "Pakai sebelum (maks. 30 hari)" in h


def test_teks_wa_tanpa_html():
    t = teks_wa(DATA, "12-23")
    assert "<" not in t
    for kata in ("Jam makan", "Habis berapa", "BAB/BAK", nilai_fakta(DATA, "porsi.12-23")):
        assert kata in t


def test_kartu_aturan_makan():
    h = render_kartu(DATA, "12-23")
    assert "maks. 30 menit" in h and "tanpa HP/TV" in h


def test_log_dan_asi_dan_mitos():
    assert "Habis berapa" in render_log()
    asi = render_kartu_asi(DATA)
    assert "4 jam" in asi and "48 jam" in asi and "3 bulan" in asi
    assert nilai_fakta(DATA, "madu.usia") in render_mitos(DATA).lower()
