# Misi Anak Hebat: Jurnal Juara 30 Hari

Template printable 47 halaman (A4) untuk membangun 7 Kebiasaan Anak Indonesia Hebat. Hasil redesign (ATM) dari produk referensi "Jurnal 7 Kebiasaan Anak Hebat" (12 halaman).

| File | Isi |
|---|---|
| `Misi_Anak_Hebat_Jurnal_Juara_30_Hari.pdf` | Produk utama, 47 halaman (1 cover + 46 isi), termasuk halaman ibadah 6 agama, dengan bookmark |
| `promo/00-cover-HD-2480x3508.png` | Cover HD (A4 @300 dpi) |
| `promo/01`–`05` | Banner feed, story, landscape, header web, dan carousel isi |
| `Paket_Produk_Misi_Anak_Hebat.md` | Deskripsi, hashtag, keyword, kategori, rekomendasi harga + sumber |
| `Verifikasi_Misi_Anak_Hebat.md` | Daftar klaim, sumber, dan hasil hitungan |
| `source/` | Generator (Python + Playwright) untuk membangun ulang PDF dan banner |

## Membangun ulang

```bash
cd produk/misi-anak-hebat/source
npm i @fontsource/fredoka @fontsource/nunito
pip install playwright pypdf pillow
python3 render_pdf.py ../Misi_Anak_Hebat_Jurnal_Juara_30_Hari.pdf
python3 banners.py ../promo 47
```

`render_pdf.py` dan `banners.py` memakai Chromium di `/opt/pw-browsers/chromium`; ubah `executable_path` bila Chromium ada di lokasi lain.

© 2026 www.GoSatSet.xyz
