from pathlib import Path

import pytest

from ebook.data import muat_data
from ebook.render import render_bab

ROOT = Path(__file__).resolve().parents[1]
DATA = muat_data(ROOT / "data")

FM = "---\njudul: Uji\nbagian: Fondasi\nnomor: 1\nmasalah: [P1, P5]\n---\n"


def test_placeholder_diganti():
    bab = render_bab(FM + "Porsi: {{fakta.porsi.6-8}}", DATA)
    assert "2–3 sdm" in bab.html
    assert f"[{DATA.nomor_sumber('S03')}" in bab.html  # sitasi otomatis ikut


def test_nilai_tanpa_sitasi():
    bab = render_bab("Porsi: {{nilai.porsi.6-8}}", DATA)
    assert "2–3 sdm" in bab.html and "class=\"ref\"" not in bab.html


def test_placeholder_tak_dikenal_gagal():
    with pytest.raises(KeyError, match="tidak.ada"):
        render_bab(FM + "{{fakta.tidak.ada}}", DATA)


def test_sitasi_jadi_nomor_referensi():
    bab = render_bab(FM + "Kalimat [@S05].", DATA)
    assert '<sup class="ref">[5]</sup>' in bab.html
    assert "S05" in bab.sitasi


def test_front_matter_masalah():
    bab = render_bab(FM + "isi", DATA)
    assert bab.masalah == ["P1", "P5"] and bab.judul == "Uji" and bab.nomor == 1


def test_kotak_masalah_tampil():
    bab = render_bab(FM + "isi", DATA)
    assert "Masalah nyata yang dijawab bab ini" in bab.html
    assert DATA.masalah["P1"]["judul"] in bab.html and DATA.masalah["P5"]["judul"] in bab.html


def test_catatan_konflik_tampil():
    bab = render_bab(FM + "{{konflik.asi.kulkas_jam}}", DATA)
    assert "Buku ini memakai 48 jam" in bab.html


def test_blok_dari_luar():
    bab = render_bab(FM + "{{blok.menu}}", DATA, blok={"menu": "<table id='m'></table>"})
    assert "<table id='m'></table>" in bab.html
    with pytest.raises(KeyError, match="lain"):
        render_bab(FM + "{{blok.lain}}", DATA, blok={})
