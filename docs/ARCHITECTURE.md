# Arsitektur Open-Core: library gratis, aplikasi berbayar

Prinsip: **library open source adalah mesin; produk berbayar adalah layanan di atas mesin itu.** Pengguna membayar untuk kenyamanan, kecepatan, dan notifikasi, bukan untuk rumus yang sebenarnya bisa mereka jalankan sendiri.

```
┌──────────────────────────── repo publik (MIT) ───────────────────────────┐
│ cuanlens: providers → preprocessing → StockBrief → LLM/offline → Analysis │
└──────────────────────────────────▲──────────────────────────────────────┘
                                   │ pip install cuanlens  (dependency biasa)
┌──────────────────────── repo privat (produk berbayar) ───────────────────┐
│ Web app (FastAPI/Next.js) · auth · kuota harian · billing                 │
│ Worker: jadwal analisis, watchlist, alert → Telegram Bot                  │
│ Data berlisensi (DataProvider kustom) · cache Redis · database pengguna   │
└───────────────────────────────────────────────────────────────────────────┘
```

## Apa yang open source, apa yang berbayar

| Open source (menarik star & kontributor) | Premium (menghasilkan uang) |
|---|---|
| Ambil data, indikator, fundamental, brief, prompt, screener, CLI | Akun, riwayat analisis, watchlist |
| Narator offline & integrasi Gemini/OpenAI (bawa key sendiri) | Analisis tanpa batas **tanpa** perlu API key sendiri |
| Provider Yahoo & demo | Data berlisensi/real-time yang lebih andal |
| | Notifikasi Telegram real-time, alert harga/sinyal, ringkasan pagi |
| | Screener tersimpan, laporan mingguan, riwayat skor |

Garis pemisahnya: **jangan menyandera fitur inti.** Jika library dibuat sengaja pincang, komunitas akan melihatnya dan kredibilitas (yang justru ingin dibangun) hilang. Kunci premium ada di *operasional* (kuota, notifikasi, data, hosting), bukan di algoritma.

## Titik sambung di library (sudah tersedia)

| Kebutuhan produk | Pakai |
|---|---|
| Sumber data berlisensi | Implementasikan `DataProvider.fetch(instrument, period) -> RawData` |
| Cache lintas pengguna | `CachedProvider` (satu proses) atau `DataProvider` kustom berbasis Redis |
| Simpan hasil / kirim ke frontend | `analysis.to_dict()` → JSON stabil |
| Model & biaya | `GeminiLLM` / `OpenAILLM`; atau `LLM` kustom (mis. rute model murah untuk gratis, model lebih baik untuk berbayar) |
| Gagal dari LLM tapi pengguna tetap dilayani | `fallback_to_offline=True` |
| Peringkat watchlist | `screen()` → DataFrame |

Konteks yang dikirim ke LLM sekitar **900 token per analisis** (prompt sistem + data), sehingga biaya per analisis kecil dan mudah diperkirakan; cek harga model terbaru di penyedia masing-masing sebelum menetapkan harga paket.

## Sketsa lapisan freemium (di repo privat, ilustrasi)

```python
# quota.py: 3 analisis/hari untuk gratis, tak terbatas untuk berbayar
def analyze_for_user(user, symbol):
    if user.plan == "free" and usage_today(user.id) >= 3:
        raise QuotaExceeded("Batas harian tercapai. Upgrade untuk analisis tanpa batas.")
    result = analyze(symbol, llm=llm_for(user.plan), provider=LICENSED_CACHED_PROVIDER, fallback_to_offline=True)
    record_usage(user.id, symbol)
    return result.to_dict()

# worker.py: notifikasi Telegram untuk pelanggan berbayar
for sub in paid_subscriptions():
    brief = build_brief(provider.fetch(resolve(sub.symbol)))
    if crossed_alert(brief, sub.last_brief):          # mis. golden cross, RSI <30, skor berubah >=10
        telegram.send(sub.chat_id, summary(brief))    # ringkas; narasi LLM hanya bila diminta
```

Tips biaya: cache hasil per `(symbol, tanggal)`, karena 1.000 pengguna yang membuka BBCA hari ini cukup memicu **satu** panggilan LLM, bukan 1.000.

## Risiko yang harus diselesaikan SEBELUM menarik bayaran

1. **Lisensi data.** Yahoo Finance (lewat `yfinance`) tidak resmi dan ketentuannya melarang redistribusi/penggunaan komersial. Library boleh memakainya untuk eksperimen, tetapi **produk berbayar harus memakai sumber data berlisensi** (vendor data pasar, atau data IDX melalui jalur resmi). Ini biaya nyata; hitung ke dalam harga.
2. **Regulasi OJK.** Memberi rekomendasi/nasihat investasi sebagai bisnis di Indonesia bisa memerlukan izin (mis. penasihat investasi). Desain saat ini sengaja menghindari rekomendasi (hanya deskripsi kondisi, skor sebagai alat penyaring, disclaimer wajib). Tetap **konsultasikan ke ahli hukum** sebelum menjual, terutama untuk alert yang terkesan sebagai "sinyal beli/jual". Kripto di Indonesia berada di bawah rezim berbeda (aset keuangan digital); cek juga.
3. **Kualitas & kejujuran.** Skor heuristik belum divalidasi. Sebelum memasarkannya sebagai "alat bantu keputusan", backtest dan publikasikan hasilnya, apa pun hasilnya. Itu juga bahan konten yang kuat.
4. **Keamanan.** Isi berita masuk ke prompt. Guardrail sudah ada di library, tetapi di produk tetap batasi output LLM (tidak ada tool/aksi yang bisa dipicu oleh teks berita) dan jangan pernah menaruh rahasia di prompt.
5. **Pembayaran.** Gunakan payment gateway lokal (mis. Midtrans/Xendit) atau Stripe/Lemon Squeezy; jangan menyimpan data kartu sendiri.

## Urutan membangun (disarankan)

1. Rilis library + CLI (selesai di repo ini), dapatkan umpan balik dari pengguna nyata.
2. Validasi: tanyakan ke 10–20 investor ritel apakah narasinya berguna dan apa yang kurang. Ukur sebelum membangun web app.
3. Bot Telegram **gratis** dulu (perintah `/analisa BBCA`), karena distribusinya paling dekat dengan target pengguna. Jadikan batas harian di sini.
4. Web app + akun + paywall untuk "tak terbatas" dan alert.
5. Ganti data ke sumber berlisensi sebelum penarikan bayaran pertama.
