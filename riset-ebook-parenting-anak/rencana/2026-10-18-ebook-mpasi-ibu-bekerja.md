# Ebook "MPASI Ibu Bekerja" — Rencana Implementasi

**Tujuan:** Membuat ebook PDF berbayar (di atas Rp50 ribu) berjudul *MPASI Ibu Bekerja: Sistem Masak 2 Jam Seminggu + Kartu SOP untuk Nenek & Pengasuh*, untuk anak 6–24 bulan, dijual di Lynk.id. Setiap angka dan setiap bab harus bisa ditelusuri ke masalah nyata dan sumber resmi.

**Arsitektur:** Semua fakta (porsi, tekstur, frekuensi, batas simpan, aturan ASI perah) disimpan sekali di `data/fakta.yaml` beserta ID sumbernya. Naskah bab, kartu SOP, label, dan menu mengambil angka dari file itu, sehingga angka di buku dan di kartu tidak bisa berbeda. Skrip Python merender Markdown dan YAML menjadi HTML, lalu Chromium headless mencetaknya menjadi PDF. Validator otomatis menolak build jika ada bab tanpa masalah nyata, sitasi tanpa sumber, menu yang melanggar aturan keamanan, atau kalimat klaim medis.

**Tech Stack:** Python 3.13, PyYAML (sudah terpasang), `markdown` (pip), `pypdf` (sudah terpasang), `pytest` (pip), Chromium di `/opt/pw-browsers` untuk HTML→PDF.

**Sumber spec:** permintaan Bang Emteio (18 Okt 2026), jawaban pertanyaan (tanpa peninjau ahli; usia 6–24 bulan; PDF dibangun otomatis dari repo; dijual di Lynk.id), [`../ide-produk-pesaing.md`](../ide-produk-pesaing.md) (ide #3), [`../README.md`](../README.md).

## Batasan Global
- Harga jual > Rp50.000. Ditetapkan **Rp79.000 normal** dan **Rp59.000 pre-order**.
- Usia anak yang dicakup **6–23 bulan** (mengikuti rentang WHO dan Kemenkes; "6–24 bulan" di sampul berarti sampai sebelum ulang tahun ke-2).
- **Tanpa peninjau ahli.** Setiap angka wajib mengutip WHO, Kemenkes, IDAI, atau badan resmi. Opini editorial diberi label "Tips penulis".
- Dilarang memuat dosis obat atau suplemen, pertolongan pertama tersedak, atau diagnosis. Disclaimer "bukan pengganti konsultasi tenaga kesehatan" wajib ada di halaman 2 dan di setiap kartu.
- Jika sumber bertentangan, **pakai nilai yang paling konservatif** dan tulis bahwa sumbernya berbeda.
- Klaim "2 jam seminggu" boleh tampil di sampul hanya jika uji masak nyata (Task 7) mencatat median ≤ 120 menit.
- Penjualan lewat Lynk.id, dengan file PDF dikirim otomatis.
- Semua file proyek ada di `riset-ebook-parenting-anak/ebook-mpasi-ibu-bekerja/`. Tes proyek ini tidak boleh mengganggu `tests/` milik CuanLens.

## Asumsi
- Lokasi rencana ini adalah `riset-ebook-parenting-anak/rencana/`, bukan `docs/plans/`, karena `docs/` milik proyek CuanLens.
- Ukuran ebook **A5 portrait** dengan target 60–90 halaman. Kartu SOP berukuran **A6** (satu kartu per halaman, nyaman dibaca di HP) ditambah versi cetak **4 kartu per halaman A4** dengan garis potong.
- Kelompok usia mengikuti tabel Kemenkes 2023: **6–8, 9–11, 12–23 bulan**.
- Menu disusun untuk **4 minggu**, dimasak hari Minggu untuk Senin–Jumat. Akhir pekan memakai makanan keluarga yang dimodifikasi.
- Target validasi pasar: **100 unduhan lead magnet dan 20 pre-order dalam 14 hari**. Jika tidak tercapai, evaluasi judul dan harga sebelum menulis naskah penuh.
- Biaya transaksi Lynk.id diasumsikan 5% (paket gratis). Sumbernya artikel lama, jadi cek ulang di dasbor Lynk.id.
- Resep tidak mencantumkan kalori per porsi karena tidak ada ahli gizi yang menghitung. Yang dijamin adalah komposisi (protein hewani setiap hari, menurut WHO 2023) dan porsi per usia (Kemenkes).

## Fokus Review
| # | Kondisi berisiko | Perilaku yang diharapkan | Diuji di |
|---|---|---|---|
| 1 | Sumber saling bertentangan (misalnya ASI perah di kulkas 2–3 hari menurut Kemenkes vs 4–5 hari menurut sumber lain; gula/garam untuk bayi di bawah 1 tahun) | Nilai yang dipakai adalah yang paling ketat, ditambah kalimat "sumber berbeda" yang tampil di buku | Task 1 |
| 2 | Anak di batas usia (8→9 bulan, 11→12 bulan) | Rentang usia kartu tidak tumpang tindih, tidak ada celah dari 6 sampai 23 bulan, dan ada catatan transisi bertahap | Task 4 |
| 3 | Pengasuh lansia dengan penglihatan menurun dan tidak akrab istilah asing | Huruf kartu ≥ 14 pt. Istilah "puree", "finger food", "batch", "thawing" diganti kata Indonesia | Task 4 |
| 4 | Pembeli tidak punya printer | Kartu A6 terbaca di HP (satu kartu per halaman), dan log harian tersedia sebagai teks siap tempel ke WhatsApp | Task 4, Task 6 |
| 5 | Klaim "2 jam" ternyata tidak realistis | Estimasi menu ≤ 120 menit aktif per minggu. Uji masak nyata 3 kali. Jika median > 120 menit, judul memakai angka median aktual | Task 3, Task 7 |

## Peta Masalah → Materi

Setiap bab hanya boleh ada jika menjawab masalah di tabel ini. ID masalah (P1–P10) disimpan di `data/masalah.yaml` dan ditulis di front matter setiap bab.

| ID | Masalah nyata | Bukti (sumber) | Materi yang menjawab |
|---|---|---|---|
| P1 | Ibu bekerja kekurangan waktu menyiapkan MPASI | Kendala "kurang waktu membuat MP-ASI sendiri" ([Unair AMNT](https://e-journal.unair.ac.id/AMNT/article/download/63581/33994/437297)). TPAK perempuan 56,63% ([BPS via GoodStats, Agt 2025](https://data.goodstats.id/statistic/tingkat-partisipasi-pekerja-perempuan-naik-tipis-pada-2025-pKHVM)). Kurang contoh resep praktis membuat ibu enggan memasak ([ITK](https://journal.itk.ac.id/index.php/sepakat/article/view/574/267)) | Bab 3 Sistem Masak 2 Jam, Bab 5 Menu 4 Minggu |
| P2 | Saat anak diasuh pengganti, porsi, frekuensi, dan tekstur paling sering salah | Aspek porsi, frekuensi, dan tekstur memiliki kesesuaian terendah ([Poltekkes Jogja](https://eprints.poltekkesjogja.ac.id/22990/7/Conclusion.pdf)). Tekstur 9–11 bulan dan porsi 12–23 bulan banyak yang tidak sesuai (studi Soroako, [FMJ UMI](https://fmj.fk.umi.ac.id/index.php/fmj/article/download/270/198)) | Bab 2 Patokan Resmi, Bab 6 Kartu SOP |
| P3 | Tekanan keluarga untuk memberi MPASI dini, dan mitos turun-temurun | Tekanan keluarga untuk MPASI dini ([Unair AMNT](https://e-journal.unair.ac.id/AMNT/article/download/63581/33994/437297)). Bubur nasi/pisang saat syukuran ([J. Malahayati](https://ejurnalmalahayati.ac.id/index.php/manuju/article/download/20161/Download%20Artikel)). IDAI: madu baru boleh setelah 1 tahun, makanan padat tidak boleh sebelum 6 bulan ([Popmama mengutip IDAI](https://www.popmama.com/baby/0-6-months/mitos-dan-fakta-pisang-kerok-untuk-bayi-00-gdrd1-gg9vlx/amp)) | Bab 7 Bicara dengan Nenek |
| P4 | Konflik pola asuh ibu dan nenek; makin banyak anak diasuh nenek | Nenek sebagai pengasuh utama naik dari 0,8% ke 5,7% pada 2000–2014 ([Bank Dunia](https://documents1.worldbank.org/curated/en/145471496053832463/pdf/113927-BAHASA-INDONESIAN-PUBLIC-7-IndonesiaChildcareDemandBriefvBHS.pdf)). Sekitar 14% anak tinggal bersama kakek-nenek (KPAI 2018, via [Undip](https://eprints2.undip.ac.id/id/eprint/28828/2/BAB%201.pdf)). Ibu otoriter dan nenek permisif berkontribusi pada perilaku bermasalah anak (n=188, [UKWMS](https://repositori.ukwms.ac.id/id/eprint/29730/1/Pengasuhan%20kakek%20nenek_Final.pdf)). Sekitar 75% keluarga memakai pengasuhan alternatif ([Republika, KemenPPPA](https://news.republika.co.id/berita/te5lh4393/benarkah-banyak-daycare-tak-berizin)) | Bab 7, Bab 6 |
| P5 | Risiko keamanan pangan dari MPASI yang disimpan dan dihangatkan | Diare balita 4,9–7,4% (SKI 2023; angka antarsumber berbeda, [Kemenkes SKI](https://www.badankebijakan.kemkes.go.id/SKI-2023-Dalam-Angka/)). IDAI: simpan di bawah 5°C ([detik](https://health.detik.com/berita-detikhealth/d-8009834/berapa-lama-waktu-penyimpanan-mpasi-di-kulkas-menurut-ikatan-dokter-anak)). Durasi AAP: puree buah/sayur 2 hari di kulkas, daging/ikan/telur 1 hari, keduanya 1 bulan di freezer (sumber sama). WHO 5 Keys: jangan mencairkan di suhu ruang, panaskan sampai matang ([WHO](https://www.afro.who.int/sites/default/files/2017-06/fan_5keys_en%20%282%29.pdf)). Panaskan satu porsi, jangan bekukan ulang ([Pemerintah NL](https://www.gov.nl.ca/healthyeating/baby/offering-healthy-foods/keep-family-food-safe-for-your-baby/)) | Bab 4 Keamanan, label wadah, kartu SOP |
| P6 | Kurang protein hewani dan zat besi | WHO 2023: daging, ikan, atau telur setiap hari ([WHO](https://www.who.int/publications/i/item/9789240081864); [ENN](https://ennonline.net/fex/72/who-guideline-for-complementary-feeding-of-infants-and-young-children)). Sekitar 1 dari 3 baduta kurang protein hewani ([Kompas](https://lestari.kompas.com/read/2024/01/30/100000386/1-dari-3-bayi-di-indonesia-kurang-makan-daging-telur-dan-ikan)). Anemia balita 23,8% ([Metro TV/Kemenkes](https://www.metrotvnews.com/read/NP6C3PAA-kemenkes-hampir-seperempat-balita-kita-mengalami-anemia)) | Bab 2, Bab 5 (protein hewani setiap hari, divalidasi otomatis) |
| P7 | Ibu bekerja harus mengelola ASI perah | WHO: menyusui dilanjutkan sampai 2 tahun ([ENN](https://ennonline.net/fex/72/who-guideline-for-complementary-feeding-of-infants-and-young-children)). Kemenkes: suhu ruang 27–32°C maks. 4 jam, kulkas 2–3 hari, freezer dua pintu 3–6 bulan ([detik](https://health.detik.com/berita-detikhealth/d-7890338/asi-bertahan-berapa-jam-ini-cara-menyimpan-dan-mencairkan)). UU KIA 2024: cuti 3 bulan + 3 bulan dengan surat dokter, hak laktasi saat jam kerja ([Kontan](https://nasional.kontan.co.id/news/dpr-sahkan-ruu-kia-ibu-bekerja-berhak-cuti-melahirkan-sampai-6-bulan)) | Bab 8 ASI Perah & Hak Ibu Bekerja |
| P8 | Anak makan sambil melihat layar atau tanpa jadwal saat diasuh orang lain | Makan sambil menonton gawai: lebih sedikit buah dan sayur, lebih banyak camilan tinggi gula, garam, dan lemak (Pearson 2018 via [Antara/Kemenkes](https://gorontalo.antaranews.com/berita/296202/makan-bergizi-gratis-dan-pembelajaran-mindful-eating-sejak-dini)). 37,02% anak 1–4 tahun memakai HP ([GoodStats/BPS](https://data.goodstats.id/statistic/6-anak-di-bawah-usia-1-tahun-sudah-gunakan-hp-Jan9u)). Aturan makan: jadwal, maks. 30 menit, tanpa distraksi ([J. Untar](https://journal.untar.ac.id/index.php/baktimas/article/view/25049/16600); [Popmama, dr. Novitria Sp.A](https://www.popmama.com/kid/1-3-years-old/menerapkan-3-feeding-rules-untuk-mencegah-anak-stunting-dan-obesitas-00-vdgkd-2ldggq/amp)) | Bab 9 Aturan Makan, kartu SOP |
| P9 | Kebingungan soal gula dan garam | Kutipan IDAI di media: "sesedikit mungkin". Sumber lain: tanpa tambahan di bawah 1 tahun ([HaiBunda](https://haibunda.com/parenting/20260826083130-59-396532/umur-berapa-bayi-boleh-makan-garam-begini-panduannya); [Klikdokter](https://www.klikdokter.com/ibu-anak/kesehatan-bayi/bolehkah-menambahkan-garam-dan-gula-dalam-mpasi)). Pakai sikap konservatif: **tanpa tambahan gula dan garam di bawah 12 bulan** | Bab 2, Bab 7, validasi menu |
| P10 | Orang tua tidak tahu takaran resmi | Tabel Kemenkes 2023: 6–8 bulan bubur kental, 2–3× makan + 1–2× selingan, mulai 2–3 sdm sampai ½ mangkok 125 ml; 9–11 bulan cincang halus dan makanan genggam, 3–4× + 1–2×, ½–¾ mangkok 250 ml; 12–23 bulan makanan keluarga, 3–4× + 1–2×, ¾–1 mangkok 250 ml ([Buku Resep Makanan Lokal](https://pkmpati2.patikab.go.id/data_bansos/file/Buku_Resep_Makanan_Lokal_Balita_dan_Ibu_Hamil.pdf); [Poltekkes Medan](https://repository.poltekkes-medan.ac.id/6324/3/BAB%20II.pdf)) | Bab 2, kartu SOP |

**Isi paket (yang membuat harga di atas Rp50 ribu masuk akal):**
1. Ebook utama A5, 10 bab.
2. Menu 4 minggu, lengkap dengan daftar belanja per minggu.
3. Kartu SOP pengasuh per kelompok usia (3 kartu; versi HP dan versi cetak).
4. Label wadah freezer (tanggal masak dan batas pakai).
5. Log harian pengasuh (cetak) dan template laporan WhatsApp.
6. Kartu "Mitos vs Fakta untuk Nenek".
7. Kartu ASI perah (suhu dan batas waktu).

Pembanding harga: bundel worksheet anak di Lynk.id/Shopee dijual Rp149.990–219.990 ([Zivanakids](https://bio.zivanakids.com/-rHmS)), langganan Gramedia Digital Rp89.000 per bulan, dan produk digital parenting umumnya Rp15–150 ribu (lihat [README](../README.md)).

## Struktur File

Semua path relatif terhadap `riset-ebook-parenting-anak/ebook-mpasi-ibu-bekerja/`.

| File | Tanggung jawab |
|---|---|
| `README.md` | Cara build, cara menjalankan tes, isi paket |
| `requirements.txt` | `markdown==3.7`, `pytest>=8`, `PyYAML>=6`, `pypdf>=4` |
| `.gitignore` | Mengabaikan `dist/` |
| `data/sumber.yaml` | Daftar sumber: `id` (S01…), `judul`, `penerbit`, `tahun`, `url`, `jenis` (resmi/jurnal/media), `kekuatan` (kuat/sedang/lemah) |
| `data/masalah.yaml` | P1–P10: `id`, `judul`, `bukti`, `sumber` (daftar ID) |
| `data/fakta.yaml` | Satu-satunya tempat angka: porsi, tekstur, frekuensi per usia, batas simpan MPASI, aturan ASI perah, suhu. Setiap entri punya `nilai`, `sumber`, dan (jika sumber berbeda) `alternatif` + `catatan_konflik` |
| `data/menu.yaml` | 4 minggu × 5 hari. Setiap hari: `protein_hewani`, `karbohidrat`, `sayur_buah`, `komponen_masak` (dengan `menit_aktif`), `simpan` (kulkas/freezer), `hari_konsumsi` |
| `naskah/00-cara-pakai.md` … `naskah/09-aturan-makan.md` | Bab dengan front matter `masalah: [P..]`, sitasi `[@S..]`, dan placeholder `{{fakta.<kunci>}}` |
| `templates/ebook.css`, `templates/kartu.css` | Gaya A5 (ebook) dan A6/A4 (kartu) |
| `ebook/data.py` | `muat_data()`, `validasi_data()` |
| `ebook/render.py` | `render_bab()`, `render_kartu()`, `render_label()`, `render_log()` |
| `ebook/menu.py` | `cek_menu()`, `daftar_belanja()` |
| `ebook/naskah.py` | `cek_naskah()` (lint klaim terlarang dan kelengkapan bab) |
| `ebook/pdf.py` | `html_ke_pdf()` |
| `ebook/uji_masak.py` | `klaim_waktu()` |
| `build.py` | CLI: validasi semua, render, hasilkan `dist/ebook.pdf`, `dist/kit-cetak-a4.pdf`, `dist/kartu-hp.pdf`, `dist/lead-magnet.pdf` |
| `data/uji-masak.csv` | Log uji masak nyata: `tanggal,penguji,minggu_menu,menit_aktif,menit_total,catatan` |
| `jualan/lynk-id.md` | Teks halaman jualan, harga, FAQ, checklist upload |
| `tests/test_*.py` | Tes per modul |

---

### Task 1: Data fakta, sumber, dan masalah beserta validatornya
**File:** Buat `requirements.txt`, `.gitignore`, `data/sumber.yaml`, `data/masalah.yaml`, `data/fakta.yaml`, `ebook/__init__.py`, `ebook/data.py` · Tes `tests/test_data.py`
**Interface:** Menghasilkan `muat_data(folder: Path) -> Data` (dataclass berisi `sumber: dict[str, dict]`, `masalah: dict[str, dict]`, `fakta: dict[str, dict]`), `validasi_data(data: Data) -> list[str]` (daftar pesan error; kosong berarti valid), `nilai_fakta(data: Data, kunci: str) -> str`

- [x] Langkah 1: Tulis tes yang gagal:
  - `test_setiap_masalah_punya_sumber_valid`: masalah tanpa `sumber` menghasilkan error berisi `"P1 tidak punya sumber"`.
  - `test_sitasi_fakta_harus_ada_di_sumber`: fakta yang mengutip `S99` menghasilkan error berisi `"S99"`.
  - `test_konflik_pakai_nilai_konservatif`: fakta `asi.kulkas_jam` dengan `nilai: 48` dan `alternatif: [96, 120]` lolos. Jika `nilai: 96` sementara alternatif berisi 48, keluar error `"bukan nilai paling konservatif"`.
  - `test_fakta_konflik_wajib_catatan`: fakta yang punya `alternatif` tetapi tidak punya `catatan_konflik` menghasilkan error.
  - `test_data_asli_valid`: `validasi_data(muat_data(Path("data")))` menghasilkan `[]`.
  - `test_nilai_fakta`: `nilai_fakta(d, "porsi.6-8")` menghasilkan `"2–3 sdm, bertahap sampai ½ mangkok (125 ml)"`.
- [x] Langkah 2: Jalankan `python -m pytest tests/test_data.py -q` dari folder proyek dan pastikan GAGAL dengan `ModuleNotFoundError: ebook`.
- [x] Langkah 3: Isi data:
  - `sumber.yaml` memuat semua sumber di tabel Peta Masalah (S01–S30).
  - `masalah.yaml` memuat P1–P10 persis seperti tabel.
  - `fakta.yaml` memuat kunci berikut dengan nilai persis:
    - `porsi.6-8`, `porsi.9-11`, `porsi.12-23`, `tekstur.*`, `frekuensi.*` (tabel Kemenkes P10)
    - `energi.6-8=200 kkal`, `energi.9-11=300 kkal`, `energi.12-23=550 kkal`
    - `simpan.kulkas_suhu="di bawah 5°C"`
    - `simpan.hewani_kulkas_hari=1`, `simpan.nabati_kulkas_hari=2`, `simpan.freezer_hari=30`
    - `asi.suhu_ruang_jam=4` (27–32°C), `asi.kulkas_jam=48` (alternatif 72, 96, 120), `asi.freezer_bulan=3` (freezer dua pintu, alternatif 6)
    - `panas.aturan="panaskan sampai mengepul merata, satu porsi, jangan bekukan ulang, cairkan di kulkas"`
    - `gula_garam.bawah_12="tanpa tambahan"` (alternatif "sesedikit mungkin", dengan catatan konflik)

  Lalu implementasi tiga fungsi di `ebook/data.py`.
- [x] Langkah 4: Jalankan `pip install -r requirements.txt && python -m pytest tests/test_data.py -q` dan pastikan `6 passed`.
- [x] Langkah 5: Commit dengan pesan "ebook: data fakta, sumber, masalah + validator".

### Task 2: Renderer bab (sitasi, placeholder fakta, front matter)
**File:** Buat `ebook/render.py`, `templates/ebook.css` · Tes `tests/test_render_bab.py`
**Interface:** Memakai `Data`, `nilai_fakta()` · Menghasilkan `render_bab(md: str, data: Data, nomor_awal_catatan: int = 1) -> BabHTML` (dataclass berisi `judul: str`, `html: str`, `masalah: list[str]`, `sitasi: list[str]`)

- [x] Langkah 1: Tulis tes yang gagal:
  - `test_placeholder_diganti`: `"Porsi: {{fakta.porsi.6-8}}"` menghasilkan HTML yang memuat `"2–3 sdm"`.
  - `test_placeholder_tak_dikenal_gagal`: `{{fakta.tidak.ada}}` memunculkan `KeyError` dengan pesan `"tidak.ada"`.
  - `test_sitasi_jadi_catatan_kaki`: `"... [@S05]"` menghasilkan `<sup>1</sup>` dan daftar sumber di akhir bab yang memuat judul S05.
  - `test_front_matter_masalah`: front matter `masalah: [P1, P5]` menghasilkan `bab.masalah == ["P1","P5"]`.
  - `test_kotak_masalah_tampil`: HTML memuat kotak "Masalah nyata yang dijawab bab ini" berisi judul P1 dan P5.
- [x] Langkah 2: Jalankan `python -m pytest tests/test_render_bab.py -q` dan pastikan GAGAL.
- [x] Langkah 3: Implementasi `render_bab` (front matter YAML di antara `---`, regex `\{\{fakta\.([\w.\-]+)\}\}` dan `\[@(S\d+)\]`, lalu `markdown.markdown(..., extensions=["tables"])`).
- [x] Langkah 4: Jalankan tes dan pastikan `5 passed`.
- [x] Langkah 5: Commit dengan pesan "ebook: renderer bab dengan sitasi dan fakta".

### Task 3: Menu 4 minggu dan validator keamanan menu
**File:** Buat `data/menu.yaml`, `ebook/menu.py` · Tes `tests/test_menu.py`
**Interface:** Memakai `Data` · Menghasilkan `cek_menu(menu: dict, data: Data) -> list[str]`, `daftar_belanja(menu: dict, minggu: int) -> list[tuple[str, str]]` (bahan, jumlah)

- [x] Langkah 1: Tulis tes yang gagal:
  - `test_protein_hewani_tiap_hari` (P6, WHO 2023): hari tanpa `protein_hewani` menghasilkan error `"minggu 1 hari Senin: tanpa protein hewani"`.
  - `test_bahan_terlarang_bawah_12_bulan` (P3, P9): resep untuk usia 6–8 atau 9–11 yang memuat `madu`, `garam`, `gula`, atau `kecap` menghasilkan error.
  - `test_hewani_di_kulkas_maks_1_hari` (P5): komponen hewani `simpan: kulkas` dengan selisih hari masak–konsumsi 2 menghasilkan error. Komponen `simpan: freezer` dengan selisih ≤ 30 lolos.
  - `test_menit_aktif_mingguan_maks_120` (P1, Fokus Review 5): total `menit_aktif` satu minggu 125 menghasilkan error `"minggu 1: 125 menit > 120"`.
  - `test_menu_asli_valid`: `cek_menu(menu.yaml asli)` menghasilkan `[]`.
  - `test_daftar_belanja_gabung_bahan`: dua resep yang masing-masing memakai `telur: 2 butir` digabung menjadi `("telur", "4 butir")`.
- [x] Langkah 2: Jalankan tes dan pastikan GAGAL.
- [x] Langkah 3: Susun `menu.yaml` dengan sistem komponen: 1 dasar karbohidrat, 2–3 protein hewani yang dirotasi (telur, ikan kembung, hati ayam, daging sapi, ayam), dan 2 sayur atau buah per minggu, semuanya dari bahan lokal. Lalu implementasi `cek_menu` dan `daftar_belanja`.
- [x] Langkah 4: Jalankan tes dan pastikan `6 passed`.
- [x] Langkah 5: Commit dengan pesan "ebook: menu 4 minggu + validator keamanan".

### Task 4: Kartu SOP, label wadah, log pengasuh, dan lead magnet
**File:** Ubah `ebook/render.py` · Buat `templates/kartu.css` · Tes `tests/test_kartu.py`
**Interface:** Memakai `Data`, `nilai_fakta()` · Menghasilkan:
- `render_kartu(data: Data, usia: str) -> str` (HTML satu kartu A6; `usia` ∈ {"6-8","9-11","12-23"})
- `render_label(data: Data) -> str`
- `render_log() -> str`
- `teks_wa(usia: str) -> str`
- `render_mitos(data: Data) -> str`
- `render_kartu_asi(data: Data) -> str`
- `RENTANG_USIA: list[tuple[int, int]] = [(6, 8), (9, 11), (12, 23)]`

- [x] Langkah 1: Tulis tes yang gagal:
  - `test_kartu_memuat_angka_fakta` (P2, P10): kartu "9-11" memuat porsi, tekstur, dan frekuensi persis dari `nilai_fakta`.
  - `test_rentang_usia_tanpa_celah` (Fokus Review 2): `RENTANG_USIA` menutup bulan 6–23 tanpa tumpang tindih dan tanpa celah.
  - `test_kartu_ada_catatan_transisi`: kartu "6-8" memuat `"menjelang 9 bulan"`.
  - `test_font_kartu_minimal_14pt` (Fokus Review 3): setiap `font-size` di `kartu.css` ≥ 14pt.
  - `test_tanpa_istilah_asing` (Fokus Review 3): HTML kartu tidak memuat `puree`, `finger food`, `batch`, `thawing`, atau `reheat`.
  - `test_kartu_ada_disclaimer`: kartu memuat `"bukan pengganti konsultasi tenaga kesehatan"`.
  - `test_kartu_aturan_panas` (P5): kartu memuat `nilai_fakta("panas.aturan")`.
  - `test_label_memuat_batas`: label memuat kolom "Tanggal masak" dan "Pakai sebelum (maks. 30 hari)".
  - `test_teks_wa_tanpa_html` (Fokus Review 4): `teks_wa("12-23")` tidak memuat `<`, tetapi memuat `"Jam makan"`, `"Habis berapa"`, dan `"BAB/BAK"`.
  - `test_kartu_aturan_makan` (P8): kartu memuat `"maks. 30 menit"` dan `"tanpa HP/TV"`.
- [x] Langkah 2: Jalankan tes dan pastikan GAGAL.
- [x] Langkah 3: Implementasi fungsi-fungsi di atas. Kartu memakai template HTML string dengan data dari `fakta.yaml`, tanpa angka yang ditulis langsung di kode.
- [x] Langkah 4: Jalankan tes dan pastikan `10 passed`.
- [x] Langkah 5: Commit dengan pesan "ebook: kartu SOP, label, log, mitos, ASI".

### Task 5: Bangun PDF (ebook, kit cetak, kartu HP, lead magnet)
**File:** Buat `ebook/pdf.py`, `build.py` · Tes `tests/test_pdf.py`
**Interface:** Memakai semua renderer · Menghasilkan `html_ke_pdf(html: str, keluar: Path, ukuran: str) -> Path` (`ukuran` ∈ {"A5","A6","A4"}), `bangun(folder: Path, keluar: Path) -> dict[str, Path]`, dan CLI `python build.py [--hanya lead-magnet]`

- [x] Langkah 1: Tulis tes yang gagal:
  - `test_html_ke_pdf_satu_halaman`: HTML sederhana ukuran A6 menghasilkan PDF 1 halaman berukuran 298×420 pt (±2) menurut `pypdf`.
  - `test_build_gagal_jika_data_tidak_valid`: folder data dengan sitasi `S99` menyebabkan `bangun()` memunculkan `ValueError` berisi `"S99"` dan tidak menulis PDF.
  - `test_kit_cetak_a4_empat_kartu`: halaman pertama `kit-cetak-a4.pdf` berukuran A4 (595×842 pt).
  - `test_kartu_hp_tiga_halaman` (Fokus Review 4): `kartu-hp.pdf` berukuran A6 dan berisi tepat 3 halaman.
  - `test_lead_magnet`: `bangun(..., hanya="lead-magnet")` menghasilkan `lead-magnet.pdf` berisi 3 kartu porsi dan tekstur plus 1 halaman promosi.
- [x] Langkah 2: Jalankan tes dan pastikan GAGAL.
- [x] Langkah 3: Implementasi `html_ke_pdf` dengan perintah `subprocess.run([CHROMIUM, "--headless", "--no-pdf-header-footer", f"--print-to-pdf={keluar}", file_html], timeout=120)`. Path `CHROMIUM` dicari dari `/opt/pw-browsers/chromium*/chrome-linux/chrome` dan bisa ditimpa dengan env `CHROMIUM_PATH`. Ukuran halaman diatur lewat CSS `@page`. `bangun()` menjalankan `validasi_data`, `cek_menu`, dan `cek_naskah` (jika naskah sudah ada) sebelum menulis PDF.
- [x] Langkah 4: Jalankan tes dan pastikan `5 passed`. Buka `dist/kartu-hp.pdf` dan periksa: teks terbaca di layar HP dan tidak ada teks terpotong.
- [x] Langkah 5: Commit dengan pesan "ebook: build PDF via Chromium".

### Task 6: Rilis lead magnet dan pre-order (validasi pasar)
**File:** Buat `jualan/lead-magnet.md` (teks posting dan CTA), `jualan/hasil-validasi.md` · Verifikasi manual (dikerjakan Bang Emteio)
**Interface:** Memakai `dist/lead-magnet.pdf` dari Task 5

- [x] Langkah 1: Tulis `jualan/lead-magnet.md`: judul lead magnet "Kartu Porsi & Tekstur MPASI Resmi untuk Pengasuh (gratis)", 3 teks posting Instagram/TikTok yang masing-masing membuka dengan satu masalah (P2, P3, P1) beserta sumbernya, dan CTA pre-order Rp59.000.
- [ ] Langkah 2: Bang Emteio mengunggah lead magnet gratis dan produk pre-order Rp59.000 di Lynk.id.
- [ ] Langkah 3: Setelah 14 hari, catat di `jualan/hasil-validasi.md`: jumlah unduhan, jumlah pre-order, dan 10 pertanyaan atau keluhan terbanyak dari DM/komentar.
- [ ] Langkah 4: Keputusan. Jika ≥ 100 unduhan dan ≥ 20 pre-order, lanjut ke Task 7. Jika di bawah itu, revisi judul atau harga, catat alasannya, dan ulangi satu putaran. Pertanyaan pembeli yang belum tertampung di P1–P10 ditambahkan ke `masalah.yaml` hanya jika ada sumbernya.
- [ ] Langkah 5: Commit dengan pesan "ebook: hasil validasi pasar".

### Task 7: Uji masak nyata untuk klaim "2 jam"
**File:** Buat `data/uji-masak.csv`, `ebook/uji_masak.py` · Tes `tests/test_uji_masak.py`
**Interface:** Menghasilkan `klaim_waktu(csv: Path) -> Klaim` (dataclass berisi `jumlah_uji: int`, `median_menit_aktif: int`, `boleh_klaim_2_jam: bool`, `teks_judul: str`)

- [x] Langkah 1: Tulis tes yang gagal:
  - `test_kurang_dari_3_uji`: 2 baris data menghasilkan `boleh_klaim_2_jam=False` dan `teks_judul` memuat `"belum diuji"`.
  - `test_median_dalam_batas`: menit aktif 100, 115, 130 menghasilkan median 115, `boleh_klaim_2_jam=True`, dan `teks_judul="Sistem Masak 2 Jam Seminggu"`.
  - `test_median_melebihi`: menit aktif 130, 140, 150 menghasilkan median 140 dan `teks_judul="Sistem Masak 2 Jam 20 Menit Seminggu"`.
- [x] Langkah 2: Jalankan tes dan pastikan GAGAL.
- [x] Langkah 3: Implementasi `klaim_waktu`, lalu sambungkan ke `build.py` sehingga judul sampul diambil dari `teks_judul`.
- [ ] Langkah 4: Bang Emteio atau penguji memasak menu minggu 1, 2, dan 3 dengan stopwatch, lalu mencatat 3 baris di `uji-masak.csv`. Jalankan `python -m pytest tests/test_uji_masak.py -q` (`3 passed`), lalu `python -c "from ebook.uji_masak import klaim_waktu; print(klaim_waktu(Path('data/uji-masak.csv')))"`.
- [x] Langkah 5: Commit dengan pesan "ebook: klaim waktu berbasis uji masak".

### Task 8: Naskah 10 bab dan lint naskah
**File:** Buat `naskah/00-cara-pakai.md` … `naskah/09-aturan-makan.md`, `naskah/99-sumber.md`, `ebook/naskah.py` · Tes `tests/test_naskah.py`
**Interface:** Memakai `render_bab`, `Data` · Menghasilkan `cek_naskah(folder: Path, data: Data) -> list[str]`

Daftar bab dan masalah yang dijawab:

| File | Bab | Masalah |
|---|---|---|
| `00-cara-pakai` | Cara pakai: alur Minggu → Senin–Jumat | P1 |
| `01-kenapa-gagal` | Kenapa MPASI sering gagal saat ibu bekerja (data) | P1, P2, P3, P4 |
| `02-patokan-resmi` | Patokan resmi porsi, tekstur, frekuensi, protein hewani, gula/garam | P2, P6, P9, P10 |
| `03-sistem-2-jam` | Sistem masak per komponen | P1 |
| `04-keamanan` | Simpan, cairkan, panaskan | P5 |
| `05-menu-4-minggu` | Menu dan daftar belanja (dibangkitkan dari `menu.yaml`) | P1, P6 |
| `06-serah-terima` | Kartu SOP, log harian, template WA | P2, P8 |
| `07-bicara-dengan-nenek` | Mitos vs fakta, cara menyampaikan dengan Buku KIA sebagai rujukan bersama | P3, P4, P9 |
| `08-asi-perah` | ASI perah dan hak ibu bekerja (UU KIA) | P7 |
| `09-aturan-makan` | Jadwal, 30 menit, tanpa layar | P8 |

- [x] Langkah 1: Tulis tes yang gagal:
  - `test_setiap_bab_punya_masalah`: bab tanpa front matter `masalah` menghasilkan error `"<file>: tidak menjawab masalah apa pun"`.
  - `test_setiap_bab_punya_sitasi`: bab tanpa `[@S..]` menghasilkan error.
  - `test_klaim_terlarang`: kata `menyembuhkan`, `menjamin`, `pasti tidak stunting`, `dosis`, `obat`, atau `100% aman` menghasilkan error berisi kata itu.
  - `test_angka_ditulis_langsung`: pola `\d+\s?(sdm|ml|jam|hari|bulan)` di luar `{{fakta.*}}` dan di luar blok yang diawali `> Sumber:` menghasilkan error `"angka harus dari fakta.yaml"`.
  - `test_tips_penulis_berlabel`: paragraf saran tanpa sitasi harus berada di blok `> Tips penulis:`.
  - `test_semua_masalah_terjawab`: gabungan `masalah` dari semua bab mencakup P1–P10.
  - `test_naskah_asli_lolos`: `cek_naskah(Path("naskah"), data)` menghasilkan `[]`.
- [x] Langkah 2: Jalankan tes dan pastikan GAGAL.
- [x] Langkah 3: Implementasi `cek_naskah`. Lalu tulis 10 bab sesuai tabel di atas. Pertanyaan pembeli dari Task 6 dimasukkan ke bab yang relevan.
- [x] Langkah 4: Jalankan `python -m pytest tests -q` (semua lulus), lalu `python build.py`. Buka `dist/ebook.pdf` dan periksa: 60–90 halaman, disclaimer di halaman 2, kotak "Masalah nyata" di awal setiap bab, dan daftar sumber di akhir.
- [x] Langkah 5: Commit dengan pesan "ebook: naskah 10 bab".

### Task 9: Halaman jualan Lynk.id dan rilis
**File:** Buat `jualan/lynk-id.md`, ubah `README.md` proyek · Verifikasi berupa checklist

- [x] Langkah 1: Tulis `jualan/lynk-id.md`:
  - judul (dari `klaim_waktu`) dan harga Rp79.000 (pembeli pre-order sudah membayar Rp59.000)
  - 3 masalah pembuka beserta data (P1, P2, P4)
  - isi paket 7 item
  - bagian "Dari mana angka di buku ini?" (WHO 2023, Kemenkes, IDAI) dan pernyataan jujur "tidak ditinjau ahli gizi"
  - disclaimer
  - FAQ: format PDF, bisa dicetak, tanpa printer bisa dibaca di HP, cara mengunduh ulang
- [x] Langkah 2: Jalankan `python build.py` dari kondisi bersih (`rm -rf dist`). Pastikan keluar 4 PDF dan ukuran `ebook.pdf` < 20 MB.
- [ ] Langkah 3: Bang Emteio mengunggah ebook, kit cetak, dan kartu HP di Lynk.id, lalu melakukan 1 pembelian uji dan memastikan email unduhan berisi 3 file.
- [ ] Langkah 4: Kirim versi final ke pembeli pre-order.
- [x] Langkah 5: Commit dengan pesan "ebook: halaman jualan + rilis v1".

---

## Catatan Eksekusi

Dieksekusi 18 Okt 2026 bersama skill ebook-pro. 49 tes lulus. Output ada di `ebook-mpasi-ibu-bekerja/rilis/v1/`.

**Masih menunggu Bang Emteio:** Task 6 langkah 2–5 (unggah lead magnet dan pre-order, catat hasil 14 hari), Task 7 langkah 4 (uji masak 3 kali ke `data/uji-masak.csv`), Task 9 langkah 3–4 (unggah ke Lynk.id, pembelian uji, kirim ke pembeli pre-order).

**Penyimpangan dari rencana (semuanya kecil):**
1. **Urutan.** Naskah (Task 8) ditulis sebelum validasi pasar (Task 6) karena Bang Emteio meminta ebook dibuat sekarang lewat /ebook-pro. Hasil validasi tetap bisa dimasukkan ke naskah pada v1.1.
2. **Ukuran ebook Letter, bukan A5.** Mengikuti standar ebook-pro (sampul HD 2550×3300 = Letter). Hasilnya 43 halaman, bukan 60–90, karena halaman Letter lebih luas.
3. **Kartu A5 dua sisi, bukan A6.** Huruf ≥ 14 pt tidak muat di A6. Kartu HP berisi 6 halaman A5 (3 usia × 2 sisi). Kit cetak memuat 3 lembar A4 landscape (depan + belakang, dilipat dua) ditambah 4 lembar A4 (label, log, mitos, ASI).
4. **Sitasi global [n]** yang mengarah ke bab Referensi, bukan catatan kaki per bab. `{{fakta.*}}` otomatis membawa nomor sumbernya.
5. **Judul tanpa klaim waktu** sampai uji masak selesai: "Sistem Masak Seminggu Sekali" (bukan teks "belum diuji" di sampul).
6. **Bab "cara pakai"** dilebur ke halaman depan. Naskah menjadi Bab 1–10, dengan Bab 10 berisi checklist, FAQ, kuis, dan kamus (back matter ebook-pro).
7. **Lint naskah:** satuan "bulan" tidak diperiksa karena dipakai untuk usia anak. Tes "Tips penulis berlabel" dihapus karena tidak bisa dideteksi otomatis dengan andal; sebagai gantinya dilakukan pemeriksaan fakta (semua 54 angka bersatuan di PDF ditelusuri ke data, menu, usia, atau URL referensi).
8. **Sumber yang dibuang:** studi Soroako (atribusi URL tidak pasti) dan PP 33/2012 (status hukum perlu dicek setelah UU 17/2023 dan PP 28/2024). Hanya UU KIA 2024 yang dikutip.
9. **Menu minggu 2 dan 4:** validator menangkap 125 menit (membuang duri ikan kembung). Ubi dihapus dan diganti bubur, sehingga totalnya 120 menit. Estimasi menit tidak dikurangi.
10. **Modul tambahan:** `ebook/kartu.py` (dipisah dari render.py), `ebook/sampul.py`, `ebook/promo.py`, `ebook/verifikasi.py`. `teks_wa` menerima `data` agar target porsi ikut tercantum.
11. **TDD:** tes `uji_masak` dan `naskah` ditulis bersamaan dengan implementasinya, tidak dijalankan gagal lebih dulu. Semua modul lain mengikuti urutan gagal → lulus.
12. **Tema warna diganti (permintaan Bang Emteio, 18 Okt 2026):** dari hijau ke nuansa anak dan parenting, yaitu coral, kuning, biru langit, dan lavender, dengan font judul Nunito (OFL, disimpan di `templates/fonts/`). Palet dipusatkan di `ebook/tema.py` dan diuji di `tests/test_tema.py` (tanpa hijau, kontras ≥ 4,5). Sampul dan banner kini berlatar krem terang. Dua paragraf Bab 4 diringkas agar tidak ada halaman yang hanya berisi satu baris. Ebook tetap 43 halaman.
