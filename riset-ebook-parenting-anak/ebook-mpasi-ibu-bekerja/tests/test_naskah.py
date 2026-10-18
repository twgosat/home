from pathlib import Path

from ebook.data import muat_data
from ebook.naskah import cek_naskah

ROOT = Path(__file__).resolve().parents[1]
DATA = muat_data(ROOT / "data")
FM = "---\njudul: Uji\nnomor: 1\nbagian: A\nmasalah: [{m}]\n---\n"


def folder(tmp_path, isi: dict[str, str]):
    for nama, teks in isi.items():
        (tmp_path / nama).write_text(teks, encoding="utf-8")
    return tmp_path


def semua_masalah():
    return FM.format(m=", ".join(DATA.masalah)) + "Kalimat [@S01].\n"


def test_setiap_bab_punya_masalah(tmp_path):
    f = folder(tmp_path, {"01-a.md": "---\njudul: x\n---\nIsi [@S01].", "02-b.md": semua_masalah()})
    assert "01-a.md: tidak menjawab masalah apa pun" in cek_naskah(f, DATA)


def test_setiap_bab_punya_sitasi(tmp_path):
    f = folder(tmp_path, {"01-a.md": FM.format(m="P1") + "Tanpa sumber.", "02-b.md": semua_masalah()})
    assert any("01-a.md" in e and "sitasi" in e for e in cek_naskah(f, DATA))


def test_klaim_terlarang(tmp_path):
    for kata in ("menyembuhkan", "menjamin", "dosis", "100% aman"):
        f = folder(tmp_path, {"01-a.md": semua_masalah() + f"Menu ini {kata} anak."})
        assert any(kata in e for e in cek_naskah(f, DATA)), kata


def test_angka_ditulis_langsung(tmp_path):
    f = folder(tmp_path, {"01-a.md": semua_masalah() + "Simpan 3 hari di kulkas."})
    assert any("angka harus dari fakta.yaml" in e for e in cek_naskah(f, DATA))
    ok = folder(tmp_path, {"01-a.md": semua_masalah() + "Simpan {{fakta.simpan.nabati_kulkas_hari}} saja.\n"
                                                       "Usia 6–8 bulan.\n> Sumber: 2 jam menurut uji.\n"})
    assert cek_naskah(ok, DATA) == []


def test_semua_masalah_terjawab(tmp_path):
    f = folder(tmp_path, {"01-a.md": FM.format(m="P1") + "x [@S01]"})
    assert any("P10" in e for e in cek_naskah(f, DATA))


def test_naskah_asli_lolos():
    assert cek_naskah(ROOT / "naskah", DATA) == []
