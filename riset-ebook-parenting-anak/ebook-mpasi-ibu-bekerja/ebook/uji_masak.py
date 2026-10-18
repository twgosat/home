"""Klaim waktu di judul hanya dari uji masak nyata (data/uji-masak.csv)."""
from __future__ import annotations

import csv
import statistics
from dataclasses import dataclass
from pathlib import Path

BATAS = 120
MIN_UJI = 3
JUDUL_TANPA_KLAIM = "Sistem Masak Seminggu Sekali"


@dataclass
class Klaim:
    jumlah_uji: int
    median_menit_aktif: int | None
    boleh_klaim_2_jam: bool
    teks_judul: str


def _durasi(menit: int) -> str:
    j, m = divmod(menit, 60)
    return f"{j} Jam" + (f" {m} Menit" if m else "")


def klaim_waktu(path: Path) -> Klaim:
    with open(path, encoding="utf-8", newline="") as f:
        menit = [int(r["menit_aktif"]) for r in csv.DictReader(f) if r.get("menit_aktif")]
    if len(menit) < MIN_UJI:
        return Klaim(len(menit), None, False, JUDUL_TANPA_KLAIM)
    med = int(statistics.median(menit))
    boleh = med <= BATAS
    teks = "Sistem Masak 2 Jam Seminggu" if boleh else f"Sistem Masak {_durasi(med)} Seminggu"
    return Klaim(len(menit), med, boleh, teks)
