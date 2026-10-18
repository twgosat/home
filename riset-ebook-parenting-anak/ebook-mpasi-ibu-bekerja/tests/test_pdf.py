import shutil
from pathlib import Path

import pytest
from pypdf import PdfReader

import build
from ebook.pdf import html_ke_pdf

ROOT = Path(__file__).resolve().parents[1]


def ukuran(pdf: Path, i: int = 0) -> tuple[float, float]:
    box = PdfReader(str(pdf)).pages[i].mediabox
    return round(float(box.width)), round(float(box.height))


def test_html_ke_pdf_satu_halaman(tmp_path):
    p = html_ke_pdf("<html><head></head><body><p>hai</p></body></html>", tmp_path / "a.pdf", "A6")
    assert len(PdfReader(str(p)).pages) == 1
    w, h = ukuran(p)
    assert abs(w - 298) <= 2 and abs(h - 420) <= 2


def test_build_gagal_jika_data_tidak_valid(tmp_path):
    salinan = tmp_path / "proyek"
    shutil.copytree(ROOT, salinan, ignore=shutil.ignore_patterns("dist", "__pycache__", ".pytest_cache"))
    f = salinan / "data" / "masalah.yaml"
    f.write_text(f.read_text(encoding="utf-8").replace("sumber: [S12]", "sumber: [S99]"), encoding="utf-8")
    with pytest.raises(ValueError, match="S99"):
        build.bangun(salinan, tmp_path / "out", hanya="kartu")
    assert not (tmp_path / "out").exists()


@pytest.fixture(scope="module")
def printable(tmp_path_factory):
    out = tmp_path_factory.mktemp("dist")
    return {k: build.bangun(ROOT, out, hanya=k) for k in ("kartu", "kit", "lead-magnet")}


def test_kartu_hp_enam_halaman_a5(printable):
    p = printable["kartu"]["kartu"]
    assert len(PdfReader(str(p)).pages) == 6  # 3 usia × 2 sisi
    assert ukuran(p) == (420, 595)


def test_kit_cetak_a4_lipat(printable):
    p = printable["kit"]["kit"]
    assert ukuran(p, 0) == (842, 595)        # A4 landscape: depan + belakang berdampingan
    r = PdfReader(str(p))
    assert len(r.pages) == 3 + 4             # 3 kartu lipat + label, log, mitos, ASI
    assert ukuran(p, 3) == (595, 842)


def test_lead_magnet(printable):
    p = printable["lead-magnet"]["lead"]
    assert len(PdfReader(str(p)).pages) == 4  # 3 kartu takaran + 1 promosi
