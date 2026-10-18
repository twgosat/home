"""Render naskah Markdown dan printable menjadi HTML. Semua angka diambil dari Data."""
from __future__ import annotations

import html as _html
import re
from dataclasses import dataclass, field

import markdown as _md
import yaml

from .data import Data, nilai_fakta

POLA_FAKTA = re.compile(r"\{\{(fakta|nilai|konflik|blok)\.([\w.\-]+)\}\}")
POLA_SITASI = re.compile(r"\[@(S\d+(?:\s*,\s*S\d+)*)\]")


@dataclass
class BabHTML:
    judul: str
    nomor: int
    bagian: str
    masalah: list[str]
    html: str
    sitasi: list[str] = field(default_factory=list)


def ref(data: Data, sids: list[str]) -> str:
    nomor = sorted({data.nomor_sumber(s) for s in sids})
    return f'<sup class="ref">[{", ".join(map(str, nomor))}]</sup>'


def fakta_html(data: Data, kunci: str, sitasi: bool = True) -> str:
    teks = _html.escape(nilai_fakta(data, kunci))
    return teks + (ref(data, data.fakta[kunci]["sumber"]) if sitasi else "")


def konflik_html(data: Data, kunci: str) -> str:
    if kunci not in data.fakta:
        raise KeyError(f"fakta tidak dikenal: {kunci}")
    catatan = data.fakta[kunci].get("catatan_konflik")
    if not catatan:
        raise KeyError(f"fakta tanpa catatan_konflik: {kunci}")
    return (f'<div class="box info"><b>Sumber berbeda.</b> {_html.escape(catatan)}'
            f'{ref(data, data.fakta[kunci]["sumber"])}</div>')


def _pisah_front_matter(md: str) -> tuple[dict, str]:
    if md.startswith("---"):
        _, fm, isi = md.split("---", 2)
        return yaml.safe_load(fm) or {}, isi
    return {}, md


def isi_placeholder(teks: str, data: Data, blok: dict[str, str] | None = None,
                    sitasi_terpakai: list[str] | None = None) -> str:
    blok = blok or {}
    terpakai = sitasi_terpakai if sitasi_terpakai is not None else []

    def ganti(m: re.Match) -> str:
        jenis, kunci = m.group(1), m.group(2)
        if jenis == "blok":
            if kunci not in blok:
                raise KeyError(f"blok tidak dikenal: {kunci}")
            return blok[kunci]
        if jenis == "konflik":
            terpakai.extend(data.fakta.get(kunci, {}).get("sumber", []))
            return konflik_html(data, kunci)
        if jenis == "fakta":
            html_f = fakta_html(data, kunci)
            terpakai.extend(data.fakta[kunci]["sumber"])
            return html_f
        return fakta_html(data, kunci, sitasi=False)

    teks = POLA_FAKTA.sub(ganti, teks)

    def ganti_sitasi(m: re.Match) -> str:
        sids = [s.strip() for s in m.group(1).split(",")]
        for s in sids:
            if s not in data.sumber:
                raise KeyError(f"sumber tidak dikenal: {s}")
        terpakai.extend(sids)
        return ref(data, sids)

    return POLA_SITASI.sub(ganti_sitasi, teks)


def kotak_masalah(data: Data, ids: list[str]) -> str:
    butir = "".join(
        f"<li><b>{_html.escape(data.masalah[p]['judul'])}.</b> {_html.escape(data.masalah[p]['bukti'])}"
        f"{ref(data, data.masalah[p]['sumber'])}</li>"
        for p in ids
    )
    return f'<div class="masalah"><div class="masalah-judul">Masalah nyata yang dijawab bab ini</div><ul>{butir}</ul></div>'


def render_bab(md: str, data: Data, blok: dict[str, str] | None = None) -> BabHTML:
    fm, isi = _pisah_front_matter(md)
    masalah = list(fm.get("masalah") or [])
    for p in masalah:
        if p not in data.masalah:
            raise KeyError(f"masalah tidak dikenal: {p}")
    sitasi: list[str] = []
    isi = isi_placeholder(isi, data, blok, sitasi)
    for p in masalah:
        sitasi.extend(data.masalah[p]["sumber"])
    badan = _md.markdown(isi, extensions=["tables", "attr_list", "md_in_html"])
    pembuka = kotak_masalah(data, masalah) if masalah else ""
    return BabHTML(
        judul=str(fm.get("judul", "")),
        nomor=int(fm.get("nomor", 0)),
        bagian=str(fm.get("bagian", "")),
        masalah=masalah,
        html=pembuka + badan,
        sitasi=sorted(set(sitasi)),
    )
