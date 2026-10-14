# Verifikasi Konten: Misi Anak Hebat

Daftar setiap klaim faktual/angka di dalam PDF, sumbernya, dan statusnya. Angka hasil hitungan berasal dari `source/calc.py`.

## Claim ledger

| id | Halaman | Klaim (seperti tertulis) | Jenis | Sumber | Tanggal sumber | Tier | Status |
|---|---|---|---|---|---|---|---|
| 1 | 3, 13 | Kemendikdasmen meluncurkan Gerakan 7 Kebiasaan Anak Indonesia Hebat pada 27 Desember 2024 | aturan/program | Guru Inovatif; NU Online; GNFI | 30 Des 2024; Des 2024; 15 Jul 2025 | 2 | verified |
| 2 | 3, 6 | Tujuh kebiasaan: bangun pagi, beribadah, berolahraga, makan sehat dan bergizi, gemar belajar, bermasyarakat, tidur cepat | program | sama dengan #1 | 2024–2025 | 2 | verified |
| 3 | 3, 28 | Gerakan dijalankan oleh sekolah, keluarga, masyarakat, dan media (Catur Pusat Pendidikan) | program | GNFI 14 Agu 2025; NU Online | 2025 | 2 | verified |
| 4 | 4, 10, 31 | Anak 6–12 tahun: 9–12 jam tidur per 24 jam secara teratur | statistik/pedoman | Paruthi dkk., AASM, J Clin Sleep Med 2016;12(6):785–786 (didukung AAP) | 2016, masih pedoman berlaku | 1 | verified |
| 5 | 4 | Anak 3–5 tahun: 10–13 jam (termasuk tidur siang) | pedoman | AASM 2016 | 2016 | 1 | verified |
| 6 | 4, 31 | Tidur cukup berkaitan dengan perhatian, perilaku, belajar, memori, dan pengelolaan emosi yang lebih baik | pedoman | AASM 2016 (ditulis sebagai "berkaitan", bukan sebab-akibat) | 2016 | 1 | verified |
| 7 | 4, 16 | Usia 5–17 tahun: rata-rata 60 menit/hari aktivitas fisik sedang–berat; aktivitas berat & penguatan otot-tulang ≥3 hari/minggu; batasi duduk lama/layar hiburan | pedoman | WHO Guidelines on Physical Activity and Sedentary Behaviour 2020 (NCBI NBK566046) | 2020, versi terbaru | 1 | verified |
| 8 | 4, 19, 20 | Isi Piringku: ½ piring sayur & buah (sayur lebih banyak), ½ piring makanan pokok & lauk (pokok lebih banyak); cuci tangan pakai sabun sebelum & sesudah makan | pedoman | Kemenkes (kemkes.go.id); Kompas 23 Sep 2024 | 2024 | 1 | verified |
| 9 | 20 | Sayur ⅓ piring, buah ⅙, makanan pokok ⅓, lauk ⅙ | rumus | dihitung dari #8 (2/3 × 1/2, 1/3 × 1/2) | — | — | computed |
| 10 | 4, 19 | Kebutuhan air anak 7–9 tahun ±1.650 mL/hari | statistik | Permenkes No. 28/2019 (AKG), dikutip Poltekkes Yogyakarta & Hellosehat; status berlaku per pasal.id | 2019, berlaku | 1 (via kutipan sekunder) | verified |
| 11 | 4, 19 | Setara ±8 gelas kecil 200 mL | rumus | 1.650 / 200 = 8,25 | — | — | computed |
| 12 | 4 | Tabel hitung mundur: bangun 05.00 → 20.00 / 19.00; 05.30 → 20.30 / 19.30; 06.00 → 21.00 / 20.00 | rumus | `calc.py` | — | — | computed |
| 13 | 10 | Bangun 05.30 dengan tidur 9 jam → tidur pukul 20.30 | rumus | `calc.py` | — | — | computed |
| 14 | 25 | Membaca 15 menit × 30 hari = 450 menit = 7,5 jam | rumus | `calc.py` | — | — | computed |
| 15 | 16 | 60 menit boleh dicicil 20 + 20 + 20 menit | contoh | WHO menyebut rata-rata harian; pembagian ini contoh praktis | — | — | softened (contoh) |
| 16 | 3 | "Untuk TK–SD (±5–12 tahun)" | definisi produk | keputusan desain | — | — | n/a |

`calc.py` output:

```
SLEEP_TABLE [('05.00', '20.00', '19.00'), ('05.30', '20.30', '19.30'), ('06.00', '21.00', '20.00')]
bangun 05.30 tidur 9 jam -> 20.30
READ 450 menit = 7.5 jam
WATER_GLASS 8.25
PLATE {'sayur': 0.333, 'buah': 0.167, 'pokok': 0.333, 'lauk': 0.167} sum 1.0
```

## Perubahan dibanding produk referensi (12 halaman)

- Semua gambar referensi diganti ilustrasi SVG orisinal (maskot jam, tangan berdoa, bola, apel, buku, hati, bulan, anak-anak, matahari, pelangi).
- Semua teks ditulis ulang; tidak ada kalimat yang disalin.
- Tracker referensi hanya sampai tanggal 30; kini 31 hari agar cocok untuk semua bulan.
- Referensi tidak punya panduan orang tua, sumber, atau aktivitas selain tracker. Kini ada panduan, angka rujukan bersumber, kontrak, peta awal/akhir, target & hadiah, jadwal harian, grafik, bingo, Isi Piringku, Pelangi Sayur & Buah, log buku, tracker gabungan, refleksi mingguan, koleksi bintang, lembar paraf guru, dan sertifikat.
- Halaman ibadah dibuat inklusif (Salat 5 Waktu + Pohon Syukur & Doa untuk semua agama).
- Latar halaman isi putih (hemat tinta); referensi memakai latar penuh warna di setiap halaman.
- Trace scan: PDF referensi tidak memuat nama penulis, penerbit, kontak, atau kredit gambar (metadata hanya `Producer: iLovePDF`); PDF baru tidak memuat teks atau metadata dari referensi.

## Referensi lengkap

1. Guru Inovatif, "Kemendikdasmen Luncurkan Program Gerakan 7 Kebiasaan Anak Indonesia Hebat", 30 Des 2024. https://guruinovatif.id/artikel/kemendikdasmen-luncurkan-program-gerakan-7-kebiasaan-anak-indonesia-hebat-sebagai-langkah-penguatan-karakter-utama-bangsa
   NU Online, "Alasan Gerakan 7 Kebiasaan Anak Indonesia Hebat Diluncurkan Kemendikdasmen". https://www.nu.or.id/nasional/alasan-gerakan-7-kebiasaan-anak-indonesia-hebat-diluncurkan-kemendikdasmen-vQKI1
2. Good News From Indonesia, "7 Kebiasaan Anak Indonesia Hebat (KAIH) Wujudkan Pendidikan Karakter untuk Indonesia Emas 2045", 14 Agu 2025. https://www.goodnewsfromindonesia.id/2025/08/14/7-kebiasaan-anak-indonesia-hebat-kaih-wujudkan-pendidikan-karakter-untuk-indonesia-emas-2045
3. Paruthi S. dkk., "Recommended Amount of Sleep for Pediatric Populations: A Consensus Statement of the American Academy of Sleep Medicine", J Clin Sleep Med 2016;12(6):785–786. https://pmc.ncbi.nlm.nih.gov/articles/PMC4877308/
4. WHO, "Guidelines on Physical Activity and Sedentary Behaviour", 2020. https://www.ncbi.nlm.nih.gov/books/NBK566046/ ; https://www.who.int/initiatives/behealthy/physical-activity
5. Kementerian Kesehatan RI, Pedoman Gizi Seimbang "Isi Piringku". https://kemkes.go.id/id/kemenkes-pecahkan-rekor-dunia-isi-piringku ; Kompas, 23 Sep 2024. https://www.kompas.com/tren/read/2024/09/23/153000865/konsep-4-sehat-5-sempurna-diganti-pedoman-gizi-seimbang-isi-piringku-ini
6. Permenkes No. 28 Tahun 2019 tentang Angka Kecukupan Gizi. https://pasal.id/peraturan/permen/permenkes-no-28-tahun-2019 ; tabel AKG dikutip di https://eprints.poltekkesjogja.ac.id/19733/4/Chapter%202.pdf.pdf

Catatan: halaman sumber diverifikasi lewat hasil pencarian per Oktober 2026 (beberapa situs tidak dapat dibuka langsung dari lingkungan kerja). Angka AKG berasal dari kutipan sekunder yang konsisten satu sama lain; untuk keperluan formal, cek lampiran resmi Permenkes 28/2019.
