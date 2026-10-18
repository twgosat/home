import re
from pathlib import Path

from ebook.tema import PALET, font_css, kontras

ROOT = Path(__file__).resolve().parents[1]
HIJAU_LAMA = ("#0f7a4d", "#b8f35c", "#4fd1c5", "#0b6e83", "#07130f", "#06150f", "#16241d", "#51675b", "#f3f8f5")
FILE_TEMA = [ROOT / "templates" / "ebook.css", ROOT / "templates" / "kartu.css",
             ROOT / "ebook" / "sampul.py", ROOT / "ebook" / "promo.py"]


def _hue_hijau(hexwarna: str) -> bool:
    r, g, b = (int(hexwarna[i:i + 2], 16) for i in (1, 3, 5))
    return g > r + 25 and g > b + 25  # hijau dominan


def test_tidak_ada_warna_hijau_lama():
    for f in FILE_TEMA:
        teks = f.read_text(encoding="utf-8").lower()
        for h in HIJAU_LAMA:
            assert h not in teks, f"{f.name} masih memakai {h}"


def test_tidak_ada_warna_hijau_dominan():
    for f in FILE_TEMA:
        for h in re.findall(r"#[0-9a-fA-F]{6}\b", f.read_text(encoding="utf-8")):
            assert not _hue_hijau(h), f"{f.name}: {h} dominan hijau"
    for nama, h in PALET.items():
        assert not _hue_hijau(h), nama


def test_kontras_teks_di_atas_putih():
    # WCAG AA teks normal: >= 4.5
    for nama in ("teks", "judul", "aksen", "aksen2", "redup", "peringatan"):
        assert kontras(PALET[nama], "#ffffff") >= 4.5, nama


def test_kontras_teks_putih_di_header_tabel():
    assert kontras("#ffffff", PALET["aksen"]) >= 4.5


def test_font_css_menunjuk_file_yang_ada():
    css = font_css()
    files = re.findall(r"url\('file://([^']+)'\)", css)
    assert files and all(Path(f).exists() for f in files)
    assert "Nunito" in css
