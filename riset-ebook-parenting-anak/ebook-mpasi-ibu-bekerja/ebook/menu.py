"""Validasi menu mingguan terhadap aturan keamanan dan gizi di fakta.yaml."""
from __future__ import annotations

from collections import OrderedDict

from .data import Data

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
BATAS_MENIT = 120
# Tidak ada tambahan gula/garam sebelum 12 bulan (fakta gula_garam.bawah_12) dan madu sebelum 1 tahun (madu.usia).
# Menu dipakai juga untuk 6–11 bulan, jadi bahan ini dilarang di semua komponen.
TERLARANG = ("madu", "garam", "gula", "kecap", "penyedap")


def total_menit(minggu: dict) -> int:
    return (minggu.get("menit_persiapan", 0) + minggu.get("menit_penutup", 0)
            + sum(k.get("menit_aktif", 0) for k in minggu["komponen"]))


def _batas_kulkas(jenis: str, data: Data) -> int:
    # Batas AAP: 2 hari untuk sayur/buah saring, 1 hari untuk hewani. Karbohidrat matang tidak disebut
    # sumber, jadi diperlakukan seketat hewani (pilihan konservatif).
    if jenis in ("sayur", "buah"):
        return data.fakta["simpan.nabati_kulkas_hari"]["nilai"]
    return data.fakta["simpan.hewani_kulkas_hari"]["nilai"]


def cek_menu(menu: dict, data: Data) -> list[str]:
    err: list[str] = []
    batas_freezer = data.fakta["simpan.freezer_hari"]["nilai"]
    for w in menu["minggu"]:
        n = w["nomor"]
        komp = {k["id"]: k for k in w["komponen"]}
        for k in w["komponen"]:
            for bahan in k.get("bahan", {}):
                if any(t in bahan.lower() for t in TERLARANG):
                    err.append(f"minggu {n} komponen {k['id']}: bahan terlarang di bawah 12 bulan ({bahan})")
        hari_pakai: dict[str, int] = {}
        for i, h in enumerate(w["hari"], start=1):
            ada_hewani = False
            for kid in h["makan"]:
                if kid not in komp:
                    err.append(f"minggu {n} hari {h['hari']}: komponen {kid} tidak dikenal")
                    continue
                hari_pakai[kid] = max(hari_pakai.get(kid, 0), i)
                ada_hewani |= komp[kid]["jenis"] == "hewani"
            if not ada_hewani:
                err.append(f"minggu {n} hari {h['hari']}: tanpa protein hewani")
        for kid, terakhir in hari_pakai.items():
            k = komp[kid]
            if k["simpan"] == "kulkas" and terakhir > _batas_kulkas(k["jenis"], data):
                err.append(f"minggu {n} komponen {kid}: disimpan di kulkas tetapi dimakan hari ke-{terakhir} "
                           f"(batas {_batas_kulkas(k['jenis'], data)} hari)")
            if k["simpan"] == "freezer" and terakhir > batas_freezer:
                err.append(f"minggu {n} komponen {kid}: melewati batas freezer {batas_freezer} hari")
        t = total_menit(w)
        if t > BATAS_MENIT:
            err.append(f"minggu {n}: {t} menit > {BATAS_MENIT}")
    return err


def _angka(x: float) -> str:
    return str(int(x)) if float(x).is_integer() else str(x)


def daftar_belanja(menu: dict, minggu: int) -> list[tuple[str, str]]:
    w = next(m for m in menu["minggu"] if m["nomor"] == minggu)
    total: OrderedDict[tuple[str, str], float] = OrderedDict()
    for k in w["komponen"]:
        for bahan, (jumlah, satuan) in k.get("bahan", {}).items():
            total[(bahan, satuan)] = total.get((bahan, satuan), 0) + jumlah
    return [(b, f"{_angka(j)} {s}") for (b, s), j in total.items()]
