from pathlib import Path

import pytest

from ebook.data import Data, muat_data, nilai_fakta, validasi_data

ROOT = Path(__file__).resolve().parents[1]


def data_mini(**ubah):
    d = Data(
        sumber={"S01": {"judul": "WHO", "url": "https://who.int", "jenis": "resmi", "kekuatan": "kuat"}},
        masalah={"P1": {"judul": "Kurang waktu", "bukti": "x", "sumber": ["S01"]}},
        fakta={"porsi.6-8": {"nilai": "2–3 sdm", "sumber": ["S01"]}},
    )
    for k, v in ubah.items():
        setattr(d, k, v)
    return d


def test_setiap_masalah_punya_sumber_valid():
    d = data_mini(masalah={"P1": {"judul": "x", "bukti": "x", "sumber": []}})
    assert any("P1 tidak punya sumber" in e for e in validasi_data(d))


def test_sitasi_fakta_harus_ada_di_sumber():
    d = data_mini(fakta={"a": {"nilai": "1", "sumber": ["S99"]}})
    assert any("S99" in e for e in validasi_data(d))


def test_konflik_pakai_nilai_konservatif():
    ok = data_mini(fakta={"asi.kulkas_jam": {"nilai": 48, "alternatif": [96, 120], "sumber": ["S01"],
                                             "catatan_konflik": "sumber berbeda"}})
    assert validasi_data(ok) == []
    salah = data_mini(fakta={"asi.kulkas_jam": {"nilai": 96, "alternatif": [48], "sumber": ["S01"],
                                                "catatan_konflik": "sumber berbeda"}})
    assert any("bukan nilai paling konservatif" in e for e in validasi_data(salah))


def test_fakta_konflik_wajib_catatan():
    d = data_mini(fakta={"a": {"nilai": 1, "alternatif": [2], "sumber": ["S01"]}})
    assert any("catatan_konflik" in e for e in validasi_data(d))


def test_data_asli_valid():
    assert validasi_data(muat_data(ROOT / "data")) == []


def test_nilai_fakta():
    d = muat_data(ROOT / "data")
    assert nilai_fakta(d, "porsi.6-8") == "2–3 sdm, bertahap sampai ½ mangkok (125 ml)"
    with pytest.raises(KeyError, match="tidak.ada"):
        nilai_fakta(d, "tidak.ada")
