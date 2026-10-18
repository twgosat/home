from ebook.uji_masak import klaim_waktu

KEPALA = "tanggal,penguji,minggu_menu,menit_aktif,menit_total,catatan\n"


def tulis(tmp_path, menit):
    p = tmp_path / "uji.csv"
    p.write_text(KEPALA + "".join(f"2026-10-{i+1:02d},A,{i+1},{m},{m+40},-\n" for i, m in enumerate(menit)))
    return p


def test_kurang_dari_3_uji(tmp_path):
    k = klaim_waktu(tulis(tmp_path, [100, 110]))
    assert k.jumlah_uji == 2 and not k.boleh_klaim_2_jam
    assert k.teks_judul == "Sistem Masak Seminggu Sekali"


def test_median_dalam_batas(tmp_path):
    k = klaim_waktu(tulis(tmp_path, [100, 115, 130]))
    assert k.median_menit_aktif == 115 and k.boleh_klaim_2_jam
    assert k.teks_judul == "Sistem Masak 2 Jam Seminggu"


def test_median_melebihi(tmp_path):
    k = klaim_waktu(tulis(tmp_path, [130, 140, 150]))
    assert k.median_menit_aktif == 140 and not k.boleh_klaim_2_jam
    assert k.teks_judul == "Sistem Masak 2 Jam 20 Menit Seminggu"


def test_file_kosong(tmp_path):
    k = klaim_waktu(tulis(tmp_path, []))
    assert k.jumlah_uji == 0 and k.teks_judul == "Sistem Masak Seminggu Sekali"
