"""Lint naskah: setiap bab menjawab masalah nyata, bersumber, tanpa klaim medis, tanpa angka liar."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

from .data import Data

TERLARANG = ("menyembuhkan", "menjamin", "dijamin", "pasti tidak stunting", "dosis", "obat", "100% aman")
# Satuan takaran/durasi wajib berasal dari fakta.yaml. "bulan" tidak diperiksa karena dipakai untuk usia anak.
POLA_ANGKA = re.compile(r"\d+(?:[.,]\d+)?\s?(?:sdm|sdt|ml|jam|menit|hari|kkal|%|°C)(?![\w])", re.I)
POLA_PLACEHOLDER = re.compile(r"\{\{[^}]+\}\}")
POLA_SITASI = re.compile(r"\[@S\d+|\{\{(?:fakta|konflik)\.")


def _front_matter(teks: str) -> tuple[dict, str]:
    if teks.startswith("---"):
        _, fm, isi = teks.split("---", 2)
        return yaml.safe_load(fm) or {}, isi
    return {}, teks


def cek_naskah(folder: Path, data: Data) -> list[str]:
    err: list[str] = []
    terjawab: set[str] = set()
    for f in sorted(Path(folder).glob("*.md")):
        fm, isi = _front_matter(f.read_text(encoding="utf-8"))
        masalah = fm.get("masalah") or []
        if not masalah:
            err.append(f"{f.name}: tidak menjawab masalah apa pun")
        for p in masalah:
            if p not in data.masalah:
                err.append(f"{f.name}: masalah {p} tidak dikenal")
        terjawab.update(masalah)
        if not POLA_SITASI.search(isi):
            err.append(f"{f.name}: tidak punya sitasi sumber")
        bawah = isi.lower()
        for kata in TERLARANG:
            if re.search(rf"(?<![\w]){re.escape(kata)}(?![\w])", bawah):
                err.append(f"{f.name}: kata terlarang '{kata}'")
        for no, baris in enumerate(isi.splitlines(), start=1):
            if baris.lstrip().startswith("> Sumber:"):
                continue
            for m in POLA_ANGKA.finditer(POLA_PLACEHOLDER.sub("", baris)):
                err.append(f"{f.name}:{no}: '{m.group(0)}' — angka harus dari fakta.yaml")
    for p in data.masalah:
        if p not in terjawab:
            err.append(f"masalah {p} belum dijawab bab mana pun")
    return err
