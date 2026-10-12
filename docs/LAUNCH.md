# Playbook peluncuran

Tujuan: orang yang tepat (developer + investor ritel yang melek teknis di Indonesia) menemukan, mencoba, dan memberi bintang pada CuanLens. Bintang adalah akibat, bukan target. Yang membangun kredibilitas adalah repo yang rapi, cepat dicoba, dan maintainer yang responsif.

## Sebelum posting (checklist, ±1 hari)

- [ ] **Ganti nama repo menjadi `cuanlens`** (Settings → General → Repository name). URL di `pyproject.toml`, badge CI, dan README sudah memakai `twgosat/cuanlens`. Nama `home` tidak bisa ditemukan siapa pun.
- [ ] Isi *About*: deskripsi satu kalimat + **Topics**: `python`, `idx`, `saham`, `indonesia`, `stock-analysis`, `llm`, `gemini`, `openai`, `yfinance`, `crypto`, `fintech`.
- [ ] **Uji dengan data live** di mesin Anda: `cuanlens analyze BBCA`, `BBRI`, `GOTO`, `BTC`, dan `cuanlens screen --universe idx-starter`. Perbaiki apa pun yang gagal. (Library diuji offline; adapter Yahoo belum diuji live oleh pembuatnya, jadi langkah ini wajib.)
- [ ] Ganti contoh keluaran di README dengan **keluaran data asli** (ticker nyata, tanggal nyata) dari satu LLM. Ini aset pemasaran terpenting.
- [ ] Rekam GIF/video 20 detik: `pip install` → `cuanlens analyze BBCA --llm gemini` → narasi muncul. Taruh di atas README.
- [ ] Buat *social preview image* (Settings → Social preview) dan rilis `v0.1.0` (GitHub Releases).
- [ ] Publikasikan ke PyPI (`python -m build && twine upload dist/*`; nama `cuanlens` tersedia saat dicek) agar `pip install cuanlens` benar-benar bekerja.
- [ ] Buat 5–8 *good first issue* (provider CSV, ambang per sektor, terjemahan, dsb.), karena kontributor pertama menaikkan kepercayaan.
- [ ] Aktifkan GitHub Discussions untuk pertanyaan non-bug.

## Kanal & format

| Kanal | Pendekatan |
|---|---|
| **Grup Telegram developer / Python ID** | Posting singkat + GIF + 1 perintah untuk dicoba. Cek aturan grup dulu; banyak yang melarang promosi, jadi minta izin admin atau posting sebagai "tools open source". |
| **Reddit** (mis. r/indonesia, r/Python, r/algotrading, r/CryptoCurrency sesuai aturan tiap sub) | Tampilkan masalah dan hasil, bukan iklan. Sebut batasan secara terbuka. Patuhi aturan self-promotion tiap subreddit. |
| **Hacker News "Show HN"** | Judul faktual, tautan ke repo, komentar pertama berisi motivasi dan batasan. |
| **X/Twitter fintwit Indonesia, LinkedIn** | Thread: masalah → demo → cara coba → ajakan kontribusi. |
| **Artikel dev.to / Medium (Bahasa Indonesia)** | "Cara saya membuat analis saham AI yang tidak berhalusinasi": bahas desain brief + guardrail. Konten teknis seperti ini yang bertahan lama. |
| **Forum investor (Kaskus, komunitas saham)** | Hati-hati: fokus pada alat edukasi, jangan menyebut "sinyal"/"rekomendasi". |

## Draf posting (Indonesia)

**Judul:** CuanLens: library Python open source untuk mengubah data saham IDX & kripto jadi narasi yang mudah dipahami (Gemini/ChatGPT)

**Isi:**

> Saya membuat CuanLens, library Python open source (MIT) yang menarik data emiten IDX (via Yahoo Finance), menghitung indikator teknikal & fundamental, membersihkan berita, lalu mengubahnya jadi ringkasan terstruktur untuk dijelaskan oleh Gemini/ChatGPT dalam bahasa awam.
>
> Yang saya coba selesaikan: LLM sering mengarang angka dan sok memberi rekomendasi. Di sini model hanya diberi angka dari "brief" (±900 token), dilarang memberi rekomendasi beli/jual, dan berita diperlakukan sebagai data tak tepercaya.
>
> - `cuanlens analyze BBCA --llm gemini`
> - Screener: `cuanlens screen --universe idx-starter --trend uptrend`
> - Tanpa API key pun jalan (narator offline), dan ada mode demo tanpa internet.
>
> Masih alpha dan datanya Yahoo (tidak resmi), jadi mungkin ada ticker yang gagal. Laporkan lewat Issue. Saya sangat butuh masukan soal ambang per sektor dan sumber data IDX yang lebih baik. PR sangat diterima.
>
> Repo: https://github.com/twgosat/cuanlens
> *Bukan nasihat investasi.*

**Telegram (versi pendek):**

> 🔎 CuanLens: tool open source Python, data saham IDX → narasi mudah dipahami pakai Gemini/ChatGPT. `pip install cuanlens` lalu `cuanlens analyze BBCA`. Ada mode demo offline. Butuh feedback & kontributor 🙏 https://github.com/twgosat/cuanlens (edukasi, bukan nasihat investasi)

## Hal yang sebaiknya TIDAK dilakukan

- **Jangan membeli bintang/fork atau mengatur "star exchange".** GitHub menindaknya dan komunitas developer cepat mengenalinya; merusak kredibilitas yang justru Anda bangun.
- **Jangan menjanjikan hasil** ("cuan pasti", "akurasi X%") tanpa backtest yang dipublikasikan.
- **Jangan spam grup.** Satu posting bagus per kanal, lalu balas setiap komentar dalam 24 jam.
- Jangan menyembunyikan batasan. Kejujuran soal "alpha" dan "data Yahoo" justru memancing kontributor.

## Ukur & ulangi

Pantau mingguan: stars, unduhan PyPI, jumlah Issue/PR dari orang luar, dan pertanyaan yang berulang (itu daftar fitur Anda berikutnya). Setelah ±2 minggu, tulis artikel hasil pembelajaran dan rilis `v0.2.0`. Di sinilah daftar tunggu untuk versi premium (alert Telegram, tanpa batas) bisa mulai dikumpulkan, misalnya satu baris di README yang menautkan ke formulir minat, **setelah** ada pengguna yang benar-benar memakai versi gratisnya.
