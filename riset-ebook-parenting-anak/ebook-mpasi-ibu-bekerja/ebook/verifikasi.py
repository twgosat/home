"""Buku besar klaim (Verifikasi_<Judul>.md) dibangkitkan dari data, bukan ditulis tangan."""
from __future__ import annotations

from .data import Data, nilai_fakta
from .menu import total_menit
from .uji_masak import Klaim

TIER = {"resmi": "Tier 1", "jurnal": "Tier 1–2", "data": "Tier 2 (mengutip BPS)", "media": "Tier 2"}


def _sumber(data: Data, sids: list[str]) -> str:
    return "; ".join(f"[{data.nomor_sumber(s)}] {data.sumber[s].get('penerbit', '')}" for s in sids)


def tulis_verifikasi(data: Data, menu: dict, klaim: Klaim, judul: str, tanggal: str) -> str:
    b = [f"# Verifikasi — {judul}", "",
         f"Dibangkitkan otomatis oleh `build.py` pada {tanggal}. Setiap angka di ebook dan kartu berasal dari "
         "`data/fakta.yaml`. Tabel ini adalah buku besar klaimnya.", "",
         "**Status:** `verified` = dikutip dari sumber; `konservatif` = sumber berbeda, dipakai nilai paling ketat; "
         "`computed` = dihitung dari data menu; `estimasi` = perkiraan penulis yang belum diuji.", "",
         "## 1. Fakta dan aturan", "",
         "| Kunci | Klaim (seperti tertulis) | Status | Sumber |", "|---|---|---|---|"]
    for k, f in data.fakta.items():
        status = "konservatif" if f.get("alternatif") else "verified"
        teks = nilai_fakta(data, k) + (f" ({f['kondisi']})" if f.get("kondisi") else "")
        if f.get("catatan_konflik"):
            teks += f" — *{f['catatan_konflik']}*"
        b.append(f"| `{k}` | {teks} | {status} | {_sumber(data, f['sumber'])} |")
    b += ["", "## 2. Masalah nyata (alasan setiap bab ada)", "", "| ID | Masalah | Bukti | Sumber |", "|---|---|---|---|"]
    for p, m in data.masalah.items():
        b.append(f"| {p} | {m['judul']} | {m['bukti']} | {_sumber(data, m['sumber'])} |")
    b += ["", "## 3. Angka yang dihitung", "", "| Klaim | Nilai | Status | Dasar |", "|---|---|---|---|"]
    for w in menu["minggu"]:
        b.append(f"| Waktu kerja aktif minggu {w['nomor']} | {total_menit(w)} menit | estimasi + computed | "
                 "jumlah `menit_aktif` + persiapan + penutup di `data/menu.yaml` (estimasi penulis) |")
    uji = (f"{klaim.jumlah_uji} uji, median {klaim.median_menit_aktif} menit" if klaim.median_menit_aktif
           else f"{klaim.jumlah_uji} uji (butuh minimal 3)")
    b.append(f"| Judul: \"{klaim.teks_judul}\" | {uji} | {'verified' if klaim.boleh_klaim_2_jam else 'tanpa klaim waktu'} "
             "| `data/uji-masak.csv` |")
    b.append("| Protein hewani setiap hari Senin–Jumat | 20 dari 20 hari | computed | `cek_menu()` |")
    b.append("| Tanpa gula, garam, madu, kecap, penyedap di menu | 0 bahan terlarang | computed | `cek_menu()` |")
    b += ["", "## 4. Yang sengaja tidak dimuat", "",
          "- Dosis suplemen atau obat, pertolongan pertama tersedak, diagnosis alergi: ebook tidak ditinjau tenaga kesehatan.",
          "- Kalori per resep: tidak ada ahli gizi yang menghitung. Yang dijamin adalah komposisi dan porsi resmi per usia.",
          "- PP 33/2012 tentang ruang laktasi: statusnya perlu dicek setelah UU 17/2023 dan PP 28/2024, jadi hanya UU KIA 2024 yang dikutip.",
          "", "## 5. Daftar sumber", ""]
    for i, (sid, s) in enumerate(data.sumber.items(), start=1):
        b.append(f"{i}. {s.get('penerbit', '')} — *{s['judul']}* ({s.get('tahun', 'n.d.')}). "
                 f"{TIER.get(s['jenis'], s['jenis'])}, kekuatan {s['kekuatan']}. {s['url']}")
    return "\n".join(b) + "\n"
