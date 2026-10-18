# Ebook: MPASI Ibu Bekerja

Ebook PDF dan kit printable untuk orang tua bekerja dengan anak 6–23 bulan yang diasuh nenek, pengasuh, atau daycare. Rencananya ada di [`../rencana/2026-10-18-ebook-mpasi-ibu-bekerja.md`](../rencana/2026-10-18-ebook-mpasi-ibu-bekerja.md).

**Prinsipnya: setiap angka berasal dari `data/fakta.yaml` dan punya sumber.** Naskah dan kartu hanya memanggil `{{fakta.<kunci>}}`. Build akan gagal jika ada bab tanpa masalah nyata, sitasi tanpa sumber, angka yang ditulis langsung, kata klaim medis, menu tanpa protein hewani, bahan terlarang untuk bayi di bawah 12 bulan, atau batas simpan yang dilanggar.

## Menjalankan

```bash
pip install -r requirements.txt     # butuh Chromium Playwright (sudah ada di /opt/pw-browsers pada sesi cloud)
python -m pytest -q                 # 58 tes
python build.py                     # semua output ke dist/
python build.py --hanya lead-magnet # kartu | kit | lead-magnet | ebook | gabungan
```

## Output (`dist/`)

| File | Isi |
|---|---|
| `MPASI Ibu Bekerja.pdf` | **File jual utama (61 halaman):** ebook → pembatas BONUS → Kartu Pengasuh (HP) → Kit Cetak A4 → Kartu Porsi MPASI (tanpa halaman promosi). Bookmark per bab dan per bonus |
| `MPASI Ibu Bekerja (ebook saja).pdf` | Ebook Letter 44 halaman, tema putih, footer bertaut ke GoSatSet.xyz (bahan gabungan) |
| `Kartu Pengasuh (HP).pdf` | 3 kartu × 2 sisi, A5, huruf ≥ 14 pt |
| `Kit Cetak A4.pdf` | 3 kartu lipat (A4 landscape) + label, log, mitos, ASI perah |
| `Gratis - Kartu Porsi MPASI.pdf` | Lead magnet |
| `Verifikasi_MPASI Ibu Bekerja.md` | Buku besar klaim (juga disalin ke `jualan/`) |
| `promo/` | Sampul HD 2550×3300 + 5 banner |

Salinan rilis v1 disimpan di `rilis/v1/`.

## Struktur

| Path | Isi |
|---|---|
| `data/` | `sumber.yaml`, `masalah.yaml` (P1–P10), `fakta.yaml`, `menu.yaml`, `uji-masak.csv` |
| `naskah/` | 10 bab Markdown dengan front matter `masalah:` |
| `ebook/` | `data`, `render`, `kartu`, `menu`, `naskah` (lint), `pdf`, `sampul`, `promo`, `uji_masak`, `verifikasi` |
| `templates/` | `ebook.css` (Letter), `kartu.css` (A5, ≥ 14 pt), `fonts/` (Nunito, lisensi OFL) |
| `jualan/` | Paket produk, teks Lynk.id, lead magnet, lembar hasil validasi |

## Tema warna

Nuansa anak dan parenting: coral hangat, kuning cerah, biru langit, lavender di atas latar krem (sampul dan banner) atau putih (halaman isi). Judul memakai Nunito yang bulat. Semua warna ada di `ebook/tema.py`. `tests/test_tema.py` memastikan tidak ada warna hijau dan teks di atas putih memenuhi kontras WCAG AA (≥ 4,5).

## Klaim waktu "2 jam"

Selama `data/uji-masak.csv` belum berisi 3 uji dengan median ≤ 120 menit kerja aktif, subjudul memakai "Sistem Masak Seminggu Sekali". Setelah syarat itu terpenuhi, jalankan ulang `python build.py`; sampul, banner, dan subjudul akan berganti otomatis.
