"""Palet dan font bertema anak & parenting: coral hangat, kuning cerah, biru langit, lavender.
Satu sumber warna untuk sampul, banner, ebook, dan kartu. Warna teks diuji kontrasnya di tests/test_tema.py."""
from __future__ import annotations

from pathlib import Path

FONT_DIR = Path(__file__).resolve().parents[1] / "templates" / "fonts"

PALET = {
    # teks (di atas putih, kontras >= 4.5)
    "judul": "#2e2557",       # ungu tua kebiruan, lembut untuk judul
    "teks": "#3a2e2c",        # cokelat tua hangat
    "redup": "#6e5f5c",
    "aksen": "#b84a35",       # coral tua: header tabel, nomor bab
    "aksen2": "#2a64a8",      # biru langit tua: subjudul, tautan
    "peringatan": "#a3540a",  # amber
    "bahaya": "#b42318",
    # latar dan dekorasi
    "krem": "#fff8f1",
    "peach": "#ffe9dd",
    "garis": "#f1dcd2",
    "langit_muda": "#eaf4ff",
    "kuning_muda": "#fff4d6",
    "lavender_muda": "#f1ecff",
    "coral": "#ff7a59",       # dekorasi sampul/banner
    "kuning": "#ffc94d",
    "langit": "#7cc4ff",
    "lavender": "#a98bfa",
}


def _lum(h: str) -> float:
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def kontras(a: str, b: str) -> float:
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def font_css() -> str:
    """@font-face Nunito dari file lokal (OFL, templates/fonts)."""
    return "".join(
        f"@font-face{{font-family:'Nunito';font-weight:{w};font-style:normal;"
        f"src:url('{(FONT_DIR / f'nunito-latin-{w}-normal.woff2').as_uri()}') format('woff2')}}\n"
        for w in (400, 600, 700, 800, 900))
