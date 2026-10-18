from pathlib import Path

import pdfplumber
import pytest
from pypdf import PdfReader

import build

ROOT = Path(__file__).resolve().parents[1]


def _n(p: Path) -> int:
    return len(PdfReader(str(p)).pages)


def _ukuran(p: Path, i: int) -> tuple[int, int]:
    b = PdfReader(str(p)).pages[i].mediabox
    return round(float(b.width)), round(float(b.height))


@pytest.fixture(scope="module")
def hasil(tmp_path_factory):
    out = tmp_path_factory.mktemp("gab")
    return build.bangun(ROOT, out, hanya="gabungan"), out


def test_urutan_dan_jumlah_halaman(hasil):
    h, _ = hasil
    ebook, kartu, kit, lead, gab = h["ebook"], h["kartu"], h["kit"], h["lead"], h["gabungan"]
    # ebook + 1 pembatas + kartu + kit + kartu porsi tanpa halaman promosi
    assert _n(gab) == _n(ebook) + 1 + _n(kartu) + _n(kit) + (_n(lead) - 1)
    i = _n(ebook)
    assert _ukuran(gab, i) == (612, 792)          # pembatas Letter, sama dengan ebook
    assert _ukuran(gab, i + 1) == (420, 595)      # Kartu Pengasuh A5
    assert _ukuran(gab, i + 1 + _n(kartu)) == (842, 595)  # Kit Cetak: lipat A4 landscape


def test_pembatas_menyatakan_bonus(hasil):
    h, _ = hasil
    i = _n(h["ebook"])
    with pdfplumber.open(str(h["gabungan"])) as pdf:
        teks = pdf.pages[i].extract_text()
    assert "BONUS" in teks and "pembelian ebook" in teks
    for nama in ("Kartu Pengasuh", "Kit Cetak A4", "Kartu Porsi MPASI"):
        assert nama in teks


def test_halaman_promosi_tidak_ikut(hasil):
    h, _ = hasil
    with pdfplumber.open(str(h["gabungan"])) as pdf:
        teks = "".join(p.extract_text() or "" for p in pdf.pages[_n(h["ebook"]) + 1:])
    assert "Mau sistem lengkapnya?" not in teks


def test_bookmark_bonus(hasil):
    h, _ = hasil
    judul = [o.title for o in PdfReader(str(h["gabungan"])).outline if not isinstance(o, list)]
    assert "Bab 1 — Kenapa MPASI sering gagal saat ibu bekerja" in judul
    assert "BONUS untuk pembeli ebook" in judul
