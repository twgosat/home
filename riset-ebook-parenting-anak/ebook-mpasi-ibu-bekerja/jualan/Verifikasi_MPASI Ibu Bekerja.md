# Verifikasi — MPASI Ibu Bekerja

Dibangkitkan otomatis oleh `build.py` pada 2026-10-18. Setiap angka di ebook dan kartu berasal dari `data/fakta.yaml`. Tabel ini adalah buku besar klaimnya.

**Status:** `verified` = dikutip dari sumber; `konservatif` = sumber berbeda, dipakai nilai paling ketat; `computed` = dihitung dari data menu; `estimasi` = perkiraan penulis yang belum diuji.

## 1. Fakta dan aturan

| Kunci | Klaim (seperti tertulis) | Status | Sumber |
|---|---|---|---|
| `tekstur.6-8` | bubur kental atau makanan lumat (dihaluskan) | verified | [3] Kementerian Kesehatan RI; [4] Poltekkes Kemenkes Medan |
| `tekstur.9-11` | makanan dicincang halus dan makanan yang bisa dipegang bayi | verified | [3] Kementerian Kesehatan RI; [4] Poltekkes Kemenkes Medan |
| `tekstur.12-23` | makanan keluarga | verified | [3] Kementerian Kesehatan RI; [4] Poltekkes Kemenkes Medan |
| `frekuensi.6-8` | 2–3 kali makan utama + 1–2 kali selingan per hari | verified | [3] Kementerian Kesehatan RI; [4] Poltekkes Kemenkes Medan |
| `frekuensi.9-11` | 3–4 kali makan utama + 1–2 kali selingan per hari | verified | [3] Kementerian Kesehatan RI; [4] Poltekkes Kemenkes Medan |
| `frekuensi.12-23` | 3–4 kali makan utama + 1–2 kali selingan per hari | verified | [3] Kementerian Kesehatan RI; [4] Poltekkes Kemenkes Medan |
| `porsi.6-8` | 2–3 sdm, bertahap sampai ½ mangkok (125 ml) | verified | [3] Kementerian Kesehatan RI; [4] Poltekkes Kemenkes Medan |
| `porsi.9-11` | ½–¾ mangkok ukuran 250 ml (125–200 ml) | verified | [3] Kementerian Kesehatan RI; [4] Poltekkes Kemenkes Medan |
| `porsi.12-23` | ¾–1 mangkok ukuran 250 ml | verified | [3] Kementerian Kesehatan RI; [4] Poltekkes Kemenkes Medan |
| `energi.6-8` | sekitar 200 kkal per hari dari MPASI | verified | [3] Kementerian Kesehatan RI |
| `energi.9-11` | sekitar 300 kkal per hari dari MPASI | verified | [3] Kementerian Kesehatan RI |
| `energi.12-23` | sekitar 550 kkal per hari dari MPASI | verified | [3] Kementerian Kesehatan RI |
| `mulai.usia` | usia 6 bulan | verified | [1] World Health Organization; [20] Popmama |
| `asi.lanjut` | menyusui dilanjutkan sampai usia 2 tahun atau lebih | verified | [1] World Health Organization; [2] Emergency Nutrition Network (Field Exchange 72) |
| `hewani.harian` | daging, ikan, atau telur setiap hari | verified | [1] World Health Organization; [2] Emergency Nutrition Network (Field Exchange 72) |
| `nabati.harian` | buah dan sayur setiap hari; kacang-kacangan dan biji-bijian sering | verified | [2] Emergency Nutrition Network (Field Exchange 72) |
| `hindari.tinggi_gula_garam` | hindari makanan dan minuman tinggi gula dan garam, termasuk minuman manis; batasi jus buah | verified | [2] Emergency Nutrition Network (Field Exchange 72) |
| `gula_garam.bawah_12` | tanpa tambahan gula dan garam — *Sumber berbeda: media mengutip IDAI 'boleh sesedikit mungkin', sumber lain menganjurkan tanpa tambahan sebelum 1 tahun. Buku ini memakai yang paling ketat.* | konservatif | [27] HaiBunda; [28] KlikDokter; [2] Emergency Nutrition Network (Field Exchange 72) |
| `madu.usia` | madu baru boleh setelah usia 1 tahun (risiko botulisme bayi) | verified | [20] Popmama |
| `stat.tpak_perempuan` | 56,63% (Agustus 2025) | verified | [14] GoodStats |
| `stat.nenek_pengasuh` | naik dari 0,8% (2000) menjadi 5,7% (2014) | verified | [15] Bank Dunia |
| `stat.tinggal_kakek_nenek` | sekitar 14% (data KPAI 2018) | verified | [16] Universitas Diponegoro |
| `stat.pengasuhan_alternatif` | sekitar 75% keluarga | verified | [18] Republika |
| `stat.protein_hewani` | sekitar 1 dari 3 baduta | verified | [21] Kompas |
| `stat.anemia_balita` | 23,8% anak usia 0–4 tahun | verified | [22] Metro TV News |
| `stat.stunting` | 19,8% (SSGI 2024) | verified | [30] Badan Kebijakan Pembangunan Kesehatan, Kemenkes RI |
| `stat.hp_1_4` | 37,02% anak usia 1–4 tahun (2024) | verified | [24] GoodStats |
| `stat.diare_balita` | 4,9% — *Angka diare balita SKI 2023 yang dikutip berbagai sumber berbeda (4,9% dan 7,4%), kemungkinan karena definisi berbeda. Buku ini menulis rentangnya.* | konservatif | [29] Badan Kebijakan Pembangunan Kesehatan, Kemenkes RI |
| `simpan.kulkas_suhu` | di bawah 5°C | verified | [5] detikHealth (mengutip Panduan MPASI UKK IDAI dan American Academy of Pediatrics) |
| `simpan.hewani_kulkas_hari` | 1 hari | verified | [5] detikHealth (mengutip Panduan MPASI UKK IDAI dan American Academy of Pediatrics) |
| `simpan.nabati_kulkas_hari` | 2 hari | verified | [5] detikHealth (mengutip Panduan MPASI UKK IDAI dan American Academy of Pediatrics) |
| `simpan.freezer_hari` | 30 hari — *AAP (dikutip detikHealth) memberi batas 1 bulan di freezer; sumber lain menyebut 3–6 bulan tanpa rujukan jelas. Buku ini memakai 30 hari.* | konservatif | [5] detikHealth (mengutip Panduan MPASI UKK IDAI dan American Academy of Pediatrics) |
| `simpan.freezer_harian` | stok untuk dimakan hari itu tetap aman di freezer; suhu chiller naik bila pintu kulkas sering dibuka | verified | [31] Popmama |
| `cair.aturan` | cairkan di kulkas, jangan di suhu ruang | verified | [6] World Health Organization; [7] Government of Newfoundland and Labrador (Healthy Eating) |
| `panas.aturan` | panaskan satu porsi sampai matang merata, sisa makan dibuang, jangan bekukan ulang | verified | [6] World Health Organization; [7] Government of Newfoundland and Labrador (Healthy Eating) |
| `panas.cek` | aduk dan cek suhunya dulu sebelum disuapkan | verified | [7] Government of Newfoundland and Labrador (Healthy Eating) |
| `higiene.kunci` | jaga kebersihan, pisahkan bahan mentah dan matang, masak sampai matang, simpan pada suhu aman, pakai air dan bahan baku yang aman | verified | [6] World Health Organization |
| `asi.suhu_ruang_jam` | 4 jam (suhu ruang 27–32°C) — *Kemenkes: maksimal 4 jam pada 27–32°C; sumber lain menyebut 6–8 jam pada suhu ruang yang lebih sejuk (≤25°C). Buku ini memakai 4 jam karena suhu ruang di Indonesia umumnya hangat.* | konservatif | [8] detikHealth (mengutip Kementerian Kesehatan RI); [9] Halodoc |
| `asi.cooler_jam` | 24 jam (cooler bag berinsulasi dengan ice pack) | verified | [32] Hello Sehat |
| `asi.kulkas_jam` | 48 jam — *Kemenkes: 48–72 jam; sumber lain 4–5 hari. Buku ini memakai 48 jam (2 hari).* | konservatif | [8] detikHealth (mengutip Kementerian Kesehatan RI); [9] Halodoc |
| `asi.freezer_bulan` | 3 bulan (freezer dua pintu (−18°C sampai −20°C)) — *Kemenkes: 3–6 bulan untuk freezer dua pintu. Buku ini memakai 3 bulan.* | konservatif | [8] detikHealth (mengutip Kementerian Kesehatan RI); [9] Halodoc |
| `asi.cair_jam` | 1 jam (ASI beku yang sudah dicairkan, di suhu ruang; jangan dibekukan ulang) — *Sumber menyebut 1–2 jam; buku ini memakai 1 jam.* | konservatif | [8] detikHealth (mengutip Kementerian Kesehatan RI) |
| `hukum.cuti` | cuti melahirkan paling singkat 3 bulan pertama, ditambah paling lama 3 bulan berikutnya bila ada kondisi khusus dengan surat keterangan dokter | verified | [10] Kontan |
| `hukum.laktasi` | hak mendapat kesempatan dan fasilitas yang layak untuk laktasi selama waktu kerja | verified | [10] Kontan |
| `makan.durasi_menit` | 30 menit | verified | [25] Jurnal Bakti Masyarakat Indonesia, Universitas Tarumanagara; [26] Popmama |
| `makan.jadwal` | jadwal makan teratur | verified | [25] Jurnal Bakti Masyarakat Indonesia, Universitas Tarumanagara |
| `makan.distraksi` | makan tanpa paksaan dan tanpa distraksi seperti TV atau HP | verified | [25] Jurnal Bakti Masyarakat Indonesia, Universitas Tarumanagara |
| `makan.minum` | di luar jam makan, minuman yang diberikan hanya air putih | verified | [25] Jurnal Bakti Masyarakat Indonesia, Universitas Tarumanagara |
| `makan.layar_dampak` | balita yang makan sambil menonton gawai makan lebih sedikit buah dan sayur, dan lebih banyak camilan tinggi gula, garam, dan lemak | verified | [23] Antara |

## 2. Masalah nyata (alasan setiap bab ada)

| ID | Masalah | Bukti | Sumber |
|---|---|---|---|
| P1 | Ibu bekerja kekurangan waktu menyiapkan MPASI | Ibu mengaku kurang waktu membuat MP-ASI sendiri; kurangnya contoh resep praktis membuat ibu enggan memasak; lebih dari separuh perempuan usia kerja ada di angkatan kerja. | [11] Amerta Nutrition, Universitas Airlangga; [13] Jurnal SEPAKAT, Institut Teknologi Kalimantan; [14] GoodStats |
| P2 | Porsi, frekuensi, dan tekstur paling sering salah saat anak diasuh orang lain | Aspek porsi, frekuensi, dan tekstur memiliki tingkat kesesuaian paling rendah; peneliti menyarankan ibu bekerja tetap memantau MPASI yang diberikan pengasuh pengganti. | [12] Poltekkes Kemenkes Yogyakarta |
| P3 | Tekanan keluarga memberi MPASI terlalu dini dan mitos turun-temurun | Ibu mendapat tekanan keluarga untuk memberi MP-ASI lebih dini; bubur nasi dan bubur pisang diberikan saat acara syukuran; IDAI menolak makanan padat sebelum 6 bulan dan madu sebelum 1 tahun. | [11] Amerta Nutrition, Universitas Airlangga; [19] Jurnal Kesehatan Masyarakat, Universitas Malahayati; [20] Popmama |
| P4 | Nenek dan pengasuh makin sering jadi pengasuh utama, pola asuh bisa bertabrakan | Nenek sebagai pengasuh utama naik dari 0,8% (2000) ke 5,7% (2014); sekitar 14% anak tinggal bersama kakek-nenek; sekitar 75% keluarga memakai pengasuhan alternatif; pola asuh ibu otoriter dan nenek permisif berkontribusi pada perilaku bermasalah anak. | [15] Bank Dunia; [16] Universitas Diponegoro; [17] Universitas Katolik Widya Mandala Surabaya; [18] Republika |
| P5 | Risiko keamanan pangan MPASI yang disimpan dan dihangatkan | Diare masih dialami balita (SKI 2023); IDAI meminta makanan disimpan di bawah 5°C; AAP memberi batas simpan kulkas dan freezer; WHO melarang mencairkan makanan beku di suhu ruang. | [29] Badan Kebijakan Pembangunan Kesehatan, Kemenkes RI; [5] detikHealth (mengutip Panduan MPASI UKK IDAI dan American Academy of Pediatrics); [6] World Health Organization; [7] Government of Newfoundland and Labrador (Healthy Eating) |
| P6 | Asupan protein hewani dan zat besi masih kurang | WHO 2023 menganjurkan daging, ikan, atau telur setiap hari; sekitar sepertiga baduta belum cukup protein hewani; anemia balita 0–4 tahun 23,8%. | [1] World Health Organization; [2] Emergency Nutrition Network (Field Exchange 72); [21] Kompas; [22] Metro TV News |
| P7 | Ibu bekerja harus mengelola ASI perah | WHO menganjurkan menyusui dilanjutkan sampai 2 tahun atau lebih; Kemenkes memberi batas simpan ASI perah; UU KIA 2024 mengatur cuti dan hak laktasi saat jam kerja. | [2] Emergency Nutrition Network (Field Exchange 72); [8] detikHealth (mengutip Kementerian Kesehatan RI); [10] Kontan |
| P8 | Anak makan sambil melihat layar atau tanpa jadwal | Balita yang makan sambil menonton gawai makan lebih sedikit buah dan sayur; 37,02% anak usia 1–4 tahun sudah memakai HP; aturan makan menganjurkan jadwal, durasi maksimal 30 menit, dan tanpa distraksi. | [23] Antara; [24] GoodStats; [25] Jurnal Bakti Masyarakat Indonesia, Universitas Tarumanagara |
| P9 | Kebingungan soal gula dan garam untuk bayi | Media mengutip IDAI: boleh sesedikit mungkin; sumber lain: tanpa tambahan di bawah 1 tahun; WHO 2023: hindari makanan dan minuman tinggi gula dan garam. | [27] HaiBunda; [28] KlikDokter; [2] Emergency Nutrition Network (Field Exchange 72) |
| P10 | Orang tua dan pengasuh tidak tahu takaran resmi | Kemenkes 2023 menetapkan tekstur, frekuensi, dan porsi per kelompok usia 6–8, 9–11, dan 12–23 bulan. | [3] Kementerian Kesehatan RI; [4] Poltekkes Kemenkes Medan |

## 3. Angka yang dihitung

| Klaim | Nilai | Status | Dasar |
|---|---|---|---|
| Waktu kerja aktif minggu 1 | 115 menit | estimasi + computed | jumlah `menit_aktif` + persiapan + penutup di `data/menu.yaml` (estimasi penulis) |
| Waktu kerja aktif minggu 2 | 120 menit | estimasi + computed | jumlah `menit_aktif` + persiapan + penutup di `data/menu.yaml` (estimasi penulis) |
| Waktu kerja aktif minggu 3 | 115 menit | estimasi + computed | jumlah `menit_aktif` + persiapan + penutup di `data/menu.yaml` (estimasi penulis) |
| Waktu kerja aktif minggu 4 | 120 menit | estimasi + computed | jumlah `menit_aktif` + persiapan + penutup di `data/menu.yaml` (estimasi penulis) |
| Judul: "Sistem Masak Seminggu Sekali" | 0 uji (butuh minimal 3) | tanpa klaim waktu | `data/uji-masak.csv` |
| Protein hewani setiap hari Senin–Jumat | 20 dari 20 hari | computed | `cek_menu()` |
| Tanpa gula, garam, madu, kecap, penyedap di menu | 0 bahan terlarang | computed | `cek_menu()` |

## 4. Yang sengaja tidak dimuat

- Dosis suplemen atau obat, pertolongan pertama tersedak, diagnosis alergi: ebook tidak ditinjau tenaga kesehatan.
- Kalori per resep: tidak ada ahli gizi yang menghitung. Yang dijamin adalah komposisi dan porsi resmi per usia.
- PP 33/2012 tentang ruang laktasi: statusnya perlu dicek setelah UU 17/2023 dan PP 28/2024, jadi hanya UU KIA 2024 yang dikutip.

## 5. Daftar sumber

1. World Health Organization — *WHO Guideline for complementary feeding of infants and young children 6–23 months of age* (2023). Tier 1, kekuatan kuat. https://www.who.int/publications/i/item/9789240081864
2. Emergency Nutrition Network (Field Exchange 72) — *WHO guideline for complementary feeding of infants and young children 6–23 months of age (ringkasan)* (2024). Tier 1–2, kekuatan sedang. https://ennonline.net/fex/72/who-guideline-for-complementary-feeding-of-infants-and-young-children
3. Kementerian Kesehatan RI — *Buku Resep Makanan Lokal Balita dan Ibu Hamil (tabel anjuran MPASI)* (2023). Tier 1, kekuatan kuat. https://pkmpati2.patikab.go.id/data_bansos/file/Buku_Resep_Makanan_Lokal_Balita_dan_Ibu_Hamil.pdf
4. Poltekkes Kemenkes Medan — *Tinjauan pustaka MPASI (mengutip tabel Kemenkes 2023)* (2024). Tier 1–2, kekuatan lemah. https://repository.poltekkes-medan.ac.id/6324/3/BAB%20II.pdf
5. detikHealth (mengutip Panduan MPASI UKK IDAI dan American Academy of Pediatrics) — *Berapa Lama Waktu Penyimpanan MPASI di Kulkas Menurut Ikatan Dokter Anak?* (2025). Tier 2, kekuatan sedang. https://health.detik.com/berita-detikhealth/d-8009834/berapa-lama-waktu-penyimpanan-mpasi-di-kulkas-menurut-ikatan-dokter-anak
6. World Health Organization — *Five Keys to Safer Food* (2006). Tier 1, kekuatan kuat. https://www.afro.who.int/sites/default/files/2017-06/fan_5keys_en%20%282%29.pdf
7. Government of Newfoundland and Labrador (Healthy Eating) — *Keep Family Food Safe for Your Baby* (2024). Tier 1, kekuatan kuat. https://www.gov.nl.ca/healthyeating/baby/offering-healthy-foods/keep-family-food-safe-for-your-baby/
8. detikHealth (mengutip Kementerian Kesehatan RI) — *ASI Bertahan Berapa Jam? Ini Cara Menyimpan dan Mencairkan* (2025). Tier 2, kekuatan sedang. https://health.detik.com/berita-detikhealth/d-7890338/asi-bertahan-berapa-jam-ini-cara-menyimpan-dan-mencairkan
9. Halodoc — *Penyimpanan ASI Perah: Anti Ribet, Awet, dan Aman* (2025). Tier 2, kekuatan lemah. https://www.halodoc.com/artikel/penyimpanan-asi-perah-aman-awet-nutrisi-terjaga
10. Kontan — *DPR Sahkan RUU KIA, Ibu Bekerja Berhak Cuti Melahirkan Sampai 6 Bulan* (2024). Tier 2, kekuatan sedang. https://nasional.kontan.co.id/news/dpr-sahkan-ruu-kia-ibu-bekerja-berhak-cuti-melahirkan-sampai-6-bulan
11. Amerta Nutrition, Universitas Airlangga — *Kendala praktik pemberian MP-ASI pada ibu (studi kualitatif)* (2025). Tier 1–2, kekuatan sedang. https://e-journal.unair.ac.id/AMNT/article/download/63581/33994/437297
12. Poltekkes Kemenkes Yogyakarta — *Praktik pemberian MP-ASI pada ibu bekerja (kesimpulan penelitian)* (2025). Tier 1–2, kekuatan lemah. https://eprints.poltekkesjogja.ac.id/22990/7/Conclusion.pdf
13. Jurnal SEPAKAT, Institut Teknologi Kalimantan — *Pelatihan pembuatan MP-ASI berbasis pangan lokal bagi ibu bekerja* (2024). Tier 1–2, kekuatan lemah. https://journal.itk.ac.id/index.php/sepakat/article/view/574/267
14. GoodStats — *Tingkat Partisipasi Pekerja Perempuan Naik Tipis pada 2025 (data BPS Sakernas Agustus 2025)* (2025). Tier 2 (mengutip BPS), kekuatan sedang. https://data.goodstats.id/statistic/tingkat-partisipasi-pekerja-perempuan-naik-tipis-pada-2025-pKHVM
15. Bank Dunia — *Indonesia Childcare Demand Brief (analisis SAKERTI 1993–2014)* (2017). Tier 1, kekuatan kuat. https://documents1.worldbank.org/curated/en/145471496053832463/pdf/113927-BAHASA-INDONESIAN-PUBLIC-7-IndonesiaChildcareDemandBriefvBHS.pdf
16. Universitas Diponegoro — *Pengasuhan anak oleh kakek-nenek (mengutip data KPAI 2018)* (2019). Tier 1–2, kekuatan lemah. https://eprints2.undip.ac.id/id/eprint/28828/2/BAB%201.pdf
17. Universitas Katolik Widya Mandala Surabaya — *Pengasuhan ibu dan nenek terhadap perilaku anak usia 2–6 tahun (188 pasangan, Surabaya)* (2020). Tier 1–2, kekuatan sedang. https://repositori.ukwms.ac.id/id/eprint/29730/1/Pengasuhan%20kakek%20nenek_Final.pdf
18. Republika — *Benarkah Banyak Daycare Tak Berizin? (data KemenPPPA)* (2026). Tier 2, kekuatan sedang. https://news.republika.co.id/berita/te5lh4393/benarkah-banyak-daycare-tak-berizin
19. Jurnal Kesehatan Masyarakat, Universitas Malahayati — *Faktor budaya dan pemberian MP-ASI dini* (2025). Tier 1–2, kekuatan sedang. https://ejurnalmalahayati.ac.id/index.php/manuju/article/download/20161/Download%20Artikel
20. Popmama — *Mitos dan Fakta Pisang Kerok untuk Bayi (mengutip IDAI)* (2024). Tier 2, kekuatan sedang. https://www.popmama.com/baby/0-6-months/mitos-dan-fakta-pisang-kerok-untuk-bayi-00-gdrd1-gg9vlx/amp
21. Kompas — *1 dari 3 Bayi di Indonesia Kurang Makan Daging, Telur, dan Ikan (SEAMEO RECFON)* (2024). Tier 2, kekuatan sedang. https://lestari.kompas.com/read/2024/01/30/100000386/1-dari-3-bayi-di-indonesia-kurang-makan-daging-telur-dan-ikan
22. Metro TV News — *Kemenkes: Hampir Seperempat Balita Kita Mengalami Anemia* (2025). Tier 2, kekuatan sedang. https://www.metrotvnews.com/read/NP6C3PAA-kemenkes-hampir-seperempat-balita-kita-mengalami-anemia
23. Antara — *Makan Bergizi Gratis dan Pembelajaran Mindful Eating Sejak Dini (mengutip Kemenkes, Pearson dkk. 2018)* (2025). Tier 2, kekuatan sedang. https://gorontalo.antaranews.com/berita/296202/makan-bergizi-gratis-dan-pembelajaran-mindful-eating-sejak-dini
24. GoodStats — *6% Anak di Bawah Usia 1 Tahun Sudah Gunakan HP (data BPS 2024)* (2025). Tier 2 (mengutip BPS), kekuatan sedang. https://data.goodstats.id/statistic/6-anak-di-bawah-usia-1-tahun-sudah-gunakan-hp-Jan9u
25. Jurnal Bakti Masyarakat Indonesia, Universitas Tarumanagara — *Edukasi feeding rules bagi orang tua balita* (2023). Tier 1–2, kekuatan sedang. https://journal.untar.ac.id/index.php/baktimas/article/view/25049/16600
26. Popmama — *Menerapkan 3 Feeding Rules untuk Mencegah Anak Stunting dan Obesitas (dr. Novitria Dwinanda, Sp.A)* (2024). Tier 2, kekuatan lemah. https://www.popmama.com/kid/1-3-years-old/menerapkan-3-feeding-rules-untuk-mencegah-anak-stunting-dan-obesitas-00-vdgkd-2ldggq/amp
27. HaiBunda — *Umur Berapa Bayi Boleh Makan Garam? Begini Panduannya (mengutip IDAI)* (2026). Tier 2, kekuatan sedang. https://haibunda.com/parenting/20260826083130-59-396532/umur-berapa-bayi-boleh-makan-garam-begini-panduannya
28. KlikDokter — *Bolehkah Menambahkan Garam dan Gula dalam MPASI?* (2024). Tier 2, kekuatan lemah. https://www.klikdokter.com/ibu-anak/kesehatan-bayi/bolehkah-menambahkan-garam-dan-gula-dalam-mpasi
29. Badan Kebijakan Pembangunan Kesehatan, Kemenkes RI — *Survei Kesehatan Indonesia (SKI) 2023 Dalam Angka* (2024). Tier 1, kekuatan kuat. https://www.badankebijakan.kemkes.go.id/SKI-2023-Dalam-Angka/
30. Badan Kebijakan Pembangunan Kesehatan, Kemenkes RI — *SSGI 2024: Prevalensi Stunting Nasional Turun Menjadi 19,8%* (2025). Tier 1, kekuatan kuat. https://www.badankebijakan.kemkes.go.id/ssgi-2024
31. Popmama — *Menyimpan MPASI Sebaiknya di Chiller atau Freezer? Ini Kata Dokter* (2024). Tier 2, kekuatan lemah. https://www.popmama.com/baby/7-12-months/menyimpan-mpasi-sebaiknya-di-chiller-atau-freezer-ini-kata-dokter-00-rz7fm-ghnxlx
32. Hello Sehat — *Cooler Bag ASI (mengutip IDAI)* (2024). Tier 2, kekuatan lemah. https://hellosehat.com/parenting/bayi/menyusui/cooler-bag-asi/
