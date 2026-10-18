"""Printable untuk pengasuh: kartu SOP (A5 dua sisi), label wadah, log harian, mitos, ASI perah.
Semua angka diambil dari fakta.yaml lewat nilai_fakta; tidak ada angka yang ditulis langsung."""
from __future__ import annotations

import html as _h
import re

from .data import Data, nilai_fakta

RENTANG_USIA: list[tuple[int, int]] = [(6, 8), (9, 11), (12, 23)]
DISCLAIMER = "Panduan umum dari pedoman resmi, bukan pengganti konsultasi tenaga kesehatan."

TRANSISI = {
    "6-8": "Menjelang 9 bulan: naikkan tekstur bertahap ke makanan dicincang halus.",
    "9-11": "Menjelang 12 bulan: kenalkan makanan keluarga sedikit demi sedikit.",
    "12-23": "",
}


def _awal(t: str) -> str:
    """Huruf pertama kapital tanpa mengubah huruf lain (beda dengan str.capitalize)."""
    return t[:1].upper() + t[1:]


def _v(data: Data, kunci: str) -> str:
    return _h.escape(nilai_fakta(data, kunci))


def _sumber_kaki(data: Data, kunci: list[str]) -> str:
    sids = sorted({s for k in kunci for s in data.fakta[k]["sumber"]}, key=data.nomor_sumber)
    nomor = ", ".join(str(data.nomor_sumber(s)) for s in sids)
    return f'<div class="kaki">Sumber: daftar Referensi ebook no. {nomor}. {DISCLAIMER}</div>'


def render_kartu(data: Data, usia: str) -> str:
    """Dua sisi kartu A5 untuk satu kelompok usia: depan (takaran), belakang (langkah aman)."""
    a, z = usia.split("-")
    judul = f"Usia {a}–{z} bulan"
    gula = "gula_garam.bawah_12" if usia != "12-23" else "hindari.tinggi_gula_garam"
    transisi = TRANSISI[usia]
    if usia == "12-23":
        transisi = _awal(_v(data, 'asi.lanjut')) + "."
    depan_kunci = [f"tekstur.{usia}", f"frekuensi.{usia}", f"porsi.{usia}", "hewani.harian"]
    depan = f"""<section class="kartu depan">
  <div class="tag">KARTU PENGASUH · sisi depan</div>
  <h2>{judul}</h2>
  <dl>
    <dt>Tekstur</dt><dd>{_v(data, f'tekstur.{usia}')}</dd>
    <dt>Berapa kali</dt><dd>{_v(data, f'frekuensi.{usia}')}</dd>
    <dt>Porsi sekali makan</dt><dd>{_v(data, f'porsi.{usia}')}</dd>
    <dt>Wajib setiap hari</dt><dd>{_v(data, 'hewani.harian')}</dd>
  </dl>
  <div class="transisi">{transisi}</div>
  {_sumber_kaki(data, depan_kunci + (['asi.lanjut'] if usia == '12-23' else []))}
</section>"""
    belakang_kunci = ["cair.aturan", "panas.aturan", "panas.cek", "makan.durasi_menit", "makan.distraksi",
                      gula, "makan.minum", "madu.usia"]
    larangan = f"{_awal(_v(data, gula))}."
    if usia != "12-23":
        larangan += f" {_awal(_v(data, 'madu.usia'))}."
    belakang = f"""<section class="kartu belakang">
  <div class="tag">KARTU PENGASUH · sisi belakang · {judul}</div>
  <h2>Langkah setiap makan</h2>
  <ol>
    <li>Cuci tangan pakai sabun sebelum menyiapkan makanan.</li>
    <li>Malam sebelumnya: pindahkan porsi besok dari freezer ke kulkas ({_v(data, 'cair.aturan')}).</li>
    <li>{_awal(_v(data, 'panas.aturan'))}.</li>
    <li>{_awal(_v(data, 'panas.cek'))}.</li>
    <li>Makan maks. {data.fakta['makan.durasi_menit']['nilai']} menit, duduk, tanpa HP/TV, tanpa memaksa.</li>
    <li>{larangan}</li>
    <li>{_awal(_v(data, 'makan.minum'))}.</li>
    <li>Catat di log atau kirim laporan WhatsApp ke orang tua.</li>
  </ol>
  <div class="hubungi">Segera hubungi orang tua bila anak muntah, diare, demam, atau menolak makan dan minum.</div>
  {_sumber_kaki(data, belakang_kunci)}
</section>"""
    return depan + belakang


def render_label(data: Data, jumlah: int = 12) -> str:
    batas = nilai_fakta(data, "simpan.freezer_hari")
    satu = (f'<div class="label"><b>Isi:</b> ______________ <b>Usia:</b> ______<br>'
            f'<b>Tanggal masak:</b> ____/____<br><b>Pakai sebelum (maks. {batas}):</b> ____/____</div>')
    return (f'<section class="lembar"><h2>Label wadah freezer</h2><p class="kecil">Gunting dan tempel di wadah. '
            f'Batas {_h.escape(batas)} di freezer mengikuti pedoman (lihat Bab 4).</p>'
            f'<div class="grid-label">{satu * jumlah}</div></section>')


def render_log() -> str:
    hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
    baris = "".join(f"<tr><td>{h}</td>" + "<td></td>" * 5 + "</tr>" for h in hari)
    return ("<section class=\"lembar\"><h2>Log harian pengasuh</h2>"
            "<table class=\"log\"><thead><tr><th>Hari</th><th>Jam makan</th><th>Menu</th>"
            "<th>Habis berapa (¼ ½ ¾ habis)</th><th>BAB/BAK</th><th>Catatan</th></tr></thead>"
            f"<tbody>{baris}</tbody></table></section>")


def teks_wa(data: Data, usia: str) -> str:
    a, z = usia.split("-")
    return (f"Laporan makan (usia {a}–{z} bulan) – tanggal: ...\n"
            f"Target porsi sekali makan: {nilai_fakta(data, f'porsi.{usia}')}\n"
            "Jam makan: ... / ... / ...\n"
            "Menu: ...\n"
            "Habis berapa: ¼ / ½ / ¾ / habis\n"
            "Minum air putih: ... kali\n"
            "BAB/BAK: ...\n"
            "Tidur siang: ...\n"
            "Catatan (rewel, tidak mau makan, dll.): ...")


MITOS = [
    ("Bayi 3–4 bulan sudah boleh diberi pisang atau bubur supaya kenyang.",
     "MPASI dimulai pada {mulai.usia}. Sebelum itu, bayi cukup ASI."),
    ("Oles atau campur madu supaya bayi sehat.", "{madu.usia}."),
    ("Kasih sedikit garam atau gula supaya mau makan.",
     "Di bawah 12 bulan: {gula_garam.bawah_12}. Setelah itu: {hindari.tinggi_gula_garam}."),
    ("Biar makannya banyak, suapi sambil menonton HP atau TV.",
     "Faktanya, {makan.layar_dampak}. Aturan makan: {makan.distraksi}."),
    ("Sayur dan nasi dulu, daging dan ikan nanti saja kalau sudah besar.", "Pedoman WHO: {hewani.harian}."),
    ("Makanan beku pasti basi atau tidak layak.",
     "MPASI matang boleh dibekukan dan dipakai dalam {simpan.freezer_hari}, asal {cair.aturan}."),
]


def render_mitos(data: Data) -> str:
    def isi(t: str) -> str:
        return re.sub(r"\{([\w.\-]+)\}", lambda m: _h.escape(nilai_fakta(data, m.group(1))), t)
    kunci = sorted({k for _, f in MITOS for k in re.findall(r"\{([\w.\-]+)\}", f)})
    baris = "".join(f'<div class="mitos"><div class="m"><b>Katanya:</b> {_h.escape(m)}</div>'
                    f'<div class="f"><b>Pedoman resmi:</b> {_awal(isi(f))}</div></div>'
                    for m, f in MITOS)
    return f'<section class="lembar"><h2>Mitos vs pedoman resmi</h2>{baris}{_sumber_kaki(data, kunci)}</section>'


def render_kartu_asi(data: Data) -> str:
    f = data.fakta
    def baris(kunci: str, tempat: str) -> str:
        return f"<tr><td>{tempat}</td><td>{_h.escape(f[kunci].get('kondisi', ''))}</td><td><b>{_v(data, kunci)}</b></td></tr>"
    tabel = "".join([
        baris("asi.suhu_ruang_jam", "Suhu ruang"),
        baris("asi.cooler_jam", "Cooler bag"),
        baris("asi.kulkas_jam", "Kulkas (bukan pintu)"),
        baris("asi.freezer_bulan", "Freezer"),
        baris("asi.cair_jam", "Setelah dicairkan"),
    ])
    kunci = ["asi.suhu_ruang_jam", "asi.cooler_jam", "asi.kulkas_jam", "asi.freezer_bulan", "asi.cair_jam"]
    return (f'<section class="lembar"><h2>ASI perah: batas aman</h2>'
            f'<table class="log"><thead><tr><th>Tempat</th><th>Kondisi</th><th>Batas maksimal</th></tr></thead>'
            f'<tbody>{tabel}</tbody></table>'
            f'<p class="kecil">Batas di tabel adalah yang paling ketat bila sumber berbeda (lihat Bab 8).</p>'
            f'{_sumber_kaki(data, kunci)}</section>')
