# Halaman jualan Lynk.id & checklist rilis (Task 9 rencana)

## Isi halaman

- **Judul produk:** MPASI Ibu Bekerja — Sistem Masak Seminggu Sekali + Kartu SOP untuk Nenek & Pengasuh
  - Bila uji masak (`data/uji-masak.csv`) sudah 3 kali dengan median ≤ 120 menit, `build.py` otomatis mengganti subjudul menjadi "Sistem Masak 2 Jam Seminggu". Pakai judul yang dicetak `build.py`, jangan diketik manual.
- **Harga:** normal Rp79.000; promo atau pre-order Rp59.000 (lihat `Paket_Produk_MPASI Ibu Bekerja.md`).
- **Deskripsi, hashtag, keyword:** salin dari `Paket_Produk_MPASI Ibu Bekerja.md`.
- **Gambar:** `dist/promo/00-cover-HD-2550x3300.png` sebagai gambar utama, `05-portrait-isi-1080x1350.png` sebagai galeri.
- **Bagian "Dari mana angka di buku ini?":** WHO 2023, Kementerian Kesehatan, IDAI, BPS. Setiap angka bernomor sumber. Sertakan pernyataan jujur: *tidak ditinjau ahli gizi atau dokter anak*.

## FAQ untuk halaman jualan

- **Formatnya apa?** Satu file PDF (61 halaman): ebook 44 halaman, lalu halaman pembatas BONUS, Kartu Pengasuh versi HP, Kit Cetak A4, dan Kartu Porsi MPASI.
- **Tidak punya printer?** Kartu Pengasuh versi HP bisa dikirim langsung ke WhatsApp pengasuh, dan template laporan WA ada di Bab 6.
- **Bisa dicetak?** Bisa. Kit Cetak A4 berisi kartu yang dilipat dua, label wadah, log harian, kartu mitos, dan kartu ASI perah.
- **Cara mengunduh ulang?** Lewat email konfirmasi pembelian Lynk.id.
- **Apakah ini nasihat medis?** Bukan. Ini panduan edukasi dari pedoman resmi.

## Checklist rilis

- [ ] `rm -rf dist && python build.py` selesai tanpa error, menghasilkan 6 PDF (termasuk file gabungan `MPASI Ibu Bekerja.pdf`) + `promo/` + `Verifikasi_*.md`
- [ ] Ukuran `dist/MPASI Ibu Bekerja.pdf` < 20 MB
- [ ] Unggah 1 file ke produk berbayar: `MPASI Ibu Bekerja.pdf` (ebook + bonus). File bonus terpisah di `rilis/v1/bonus-terpisah/` opsional, misalnya untuk dikirim ke pengasuh
- [ ] Unggah `Gratis - Kartu Porsi MPASI.pdf` sebagai produk gratis (lead magnet)
- [ ] Cek biaya transaksi Lynk.id di dasbor (artikel lama menyebut 5% untuk paket gratis)
- [ ] Lakukan 1 pembelian uji dan pastikan email berisi file ebook + bonus
- [ ] Kirim versi final ke pembeli pre-order
