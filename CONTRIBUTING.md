# Berkontribusi ke CuanLens

Terima kasih! Siapa pun boleh membantu, dari memperbaiki typo sampai menambah provider data.

## Setup

```bash
git clone https://github.com/twgosat/cuanlens && cd cuanlens
python -m venv .venv && source .venv/bin/activate
pip install -e ".[all,dev]"
pytest          # semua test berjalan offline, tanpa API key
ruff check src tests
cuanlens analyze BBCA --demo
```

## Aturan emas

1. **Test harus offline.** Jangan memanggil Yahoo/LLM di test; pakai `DemoProvider`, data sintetis, atau fake. Jika menemukan bug dari data live, simpan *potongan* dict/DataFrame penyebabnya sebagai fixture.
2. **Sinyal harus bisa dijelaskan.** Sinyal baru = nama, stance, alasan satu kalimat dalam bahasa Indonesia, poin kecil, dan test yang membuktikan kapan ia menyala dan kapan tidak.
3. **Tidak ada rekomendasi.** Prompt dan narasi tidak boleh berbunyi "beli/jual/target harga". Guardrail di `prompts.py` ada tes yang menjaganya; jangan dilonggarkan.
4. **Jangan percaya teks pihak ketiga.** Apa pun dari berita/feed masuk ke prompt hanya di dalam blok `<berita>` dan tidak pernah ke prompt sistem.
5. **Angka harus bisa diverifikasi.** Indikator baru diuji terhadap nilai hitungan manual (lihat `tests/test_indicators.py`).

## Ide yang paling dibutuhkan

- Provider data lain (IDX resmi, broker, Binance/Indodax, CSV).
- Ambang `Thresholds` per sektor IDX (bank, tambang, consumer, properti).
- Sumber berita berbahasa Indonesia (RSS) sebagai provider berita.
- Terjemahan prompt (Inggris sudah ada) dan narator offline berbahasa Inggris.
- Backtest sederhana untuk menguji apakah skor heuristik punya daya prediksi (jujur apa pun hasilnya).

## Pull request

Satu perubahan per PR, sertakan test, jalankan `pytest` dan `ruff check`. Untuk perubahan besar, buka Issue dulu.
