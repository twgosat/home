"""Memuat dan memvalidasi data sumber, masalah, dan fakta."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class Data:
    sumber: dict[str, dict] = field(default_factory=dict)
    masalah: dict[str, dict] = field(default_factory=dict)
    fakta: dict[str, dict] = field(default_factory=dict)

    def nomor_sumber(self, sid: str) -> int:
        """Nomor rujukan [n] = urutan sumber di sumber.yaml."""
        return list(self.sumber).index(sid) + 1


def _baca(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def muat_data(folder: Path) -> Data:
    folder = Path(folder)
    return Data(
        sumber=_baca(folder / "sumber.yaml"),
        masalah=_baca(folder / "masalah.yaml"),
        fakta=_baca(folder / "fakta.yaml"),
    )


def _angka(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def validasi_data(data: Data) -> list[str]:
    err: list[str] = []
    for sid, s in data.sumber.items():
        for kolom in ("judul", "url", "jenis", "kekuatan"):
            if not s.get(kolom):
                err.append(f"{sid}: kolom {kolom} kosong")
    for pid, m in data.masalah.items():
        if not m.get("sumber"):
            err.append(f"{pid} tidak punya sumber")
        for sid in m.get("sumber", []):
            if sid not in data.sumber:
                err.append(f"{pid}: sumber {sid} tidak ada di sumber.yaml")
    for kunci, f in data.fakta.items():
        if "nilai" not in f:
            err.append(f"{kunci}: tidak punya nilai")
        if not f.get("sumber"):
            err.append(f"{kunci}: tidak punya sumber")
        for sid in f.get("sumber", []):
            if sid not in data.sumber:
                err.append(f"{kunci}: sumber {sid} tidak ada di sumber.yaml")
        alt = f.get("alternatif")
        if alt:
            if not f.get("catatan_konflik"):
                err.append(f"{kunci}: punya alternatif tetapi tidak punya catatan_konflik")
            if _angka(f.get("nilai")) and all(_angka(a) for a in alt) and f["nilai"] > min(alt):
                err.append(f"{kunci}: {f['nilai']} bukan nilai paling konservatif (ada {min(alt)})")
    return err


def nilai_fakta(data: Data, kunci: str) -> str:
    """Teks nilai fakta siap tampil (angka + satuan bila ada)."""
    if kunci not in data.fakta:
        raise KeyError(f"fakta tidak dikenal: {kunci}")
    f = data.fakta[kunci]
    teks = str(f["nilai"])
    if f.get("satuan"):
        teks = f"{teks} {f['satuan']}"
    return teks
