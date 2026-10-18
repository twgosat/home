import copy
from pathlib import Path

import yaml

from ebook.data import muat_data
from ebook.menu import cek_menu, daftar_belanja, total_menit

ROOT = Path(__file__).resolve().parents[1]
DATA = muat_data(ROOT / "data")
MENU = yaml.safe_load((ROOT / "data" / "menu.yaml").read_text(encoding="utf-8"))


def menu_mini():
    return {"minggu": [{
        "nomor": 1, "menit_persiapan": 20, "menit_penutup": 30,
        "komponen": [
            {"id": "nasi", "nama": "Nasi tim", "jenis": "karbo", "bahan": {"beras": [300, "g"]},
             "menit_aktif": 10, "simpan": "freezer"},
            {"id": "ayam", "nama": "Ayam", "jenis": "hewani", "bahan": {"telur": [2, "butir"]},
             "menit_aktif": 15, "simpan": "freezer"},
            {"id": "telur", "nama": "Telur", "jenis": "hewani", "bahan": {"telur": [2, "butir"]},
             "menit_aktif": 10, "simpan": "freezer"},
        ],
        "hari": [{"hari": "Senin", "makan": ["nasi", "ayam"]},
                 {"hari": "Selasa", "makan": ["nasi", "telur"]}],
    }]}


def test_menu_mini_valid():
    assert cek_menu(menu_mini(), DATA) == []


def test_protein_hewani_tiap_hari():
    m = menu_mini()
    m["minggu"][0]["hari"][0]["makan"] = ["nasi"]
    assert "minggu 1 hari Senin: tanpa protein hewani" in cek_menu(m, DATA)


def test_bahan_terlarang_bawah_12_bulan():
    m = menu_mini()
    m["minggu"][0]["komponen"][1]["bahan"]["garam"] = [1, "sdt"]
    m["minggu"][0]["komponen"][2]["bahan"]["madu"] = [1, "sdm"]
    err = cek_menu(m, DATA)
    assert any("garam" in e for e in err) and any("madu" in e for e in err)


def test_hewani_di_kulkas_maks_1_hari():
    m = menu_mini()
    m["minggu"][0]["komponen"][2]["simpan"] = "kulkas"  # telur dimakan Selasa = hari ke-2
    assert any("telur" in e and "kulkas" in e for e in cek_menu(m, DATA))
    m2 = menu_mini()
    m2["minggu"][0]["komponen"][1]["simpan"] = "kulkas"  # ayam dimakan Senin = hari ke-1
    assert cek_menu(m2, DATA) == []


def test_menit_aktif_mingguan_maks_120():
    m = menu_mini()
    m["minggu"][0]["menit_persiapan"] = 90  # 90 + 30 + 35 = 155
    assert "minggu 1: 155 menit > 120" in cek_menu(m, DATA)


def test_komponen_tak_dikenal():
    m = menu_mini()
    m["minggu"][0]["hari"][0]["makan"].append("tahu")
    assert any("tahu" in e for e in cek_menu(m, DATA))


def test_menu_asli_valid():
    assert cek_menu(MENU, DATA) == []
    assert len(MENU["minggu"]) == 4
    assert all(total_menit(w) <= 120 for w in MENU["minggu"])


def test_daftar_belanja_gabung_bahan():
    assert ("telur", "4 butir") in daftar_belanja(menu_mini(), 1)
