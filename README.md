# 🔎 CuanLens

**Ubah data saham IDX & kripto yang rumit menjadi narasi yang mudah dipahami.**

> *English: an open-source Python library that fetches IDX stock / crypto data, preprocesses it into a compact, hallucination-resistant brief (technicals, fundamentals, news), and feeds it to Gemini or ChatGPT to produce plain-language analysis. Works fully offline too.*

[![CI](https://github.com/twgosat/cuanlens/actions/workflows/ci.yml/badge.svg)](https://github.com/twgosat/cuanlens/actions)
![Python](https://img.shields.io/badge/python-3.10%E2%80%933.13-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Investor ritel tidak kekurangan data; mereka kekurangan *terjemahan*. RSI 71, PER 25x, MACD di bawah sinyal… lalu apa artinya? CuanLens mengerjakan bagian yang membosankan (menarik data, menghitung indikator, membersihkan berita) lalu menyerahkan ringkasan numerik yang rapi ke LLM supaya penjelasannya akurat, murah, dan konsisten.

```
data emiten ─► preprocessing ─► StockBrief (±900 token) ─► Gemini / ChatGPT / narator offline ─► narasi
 (Yahoo, dll)   indikator,        angka + sinyal + berita
                fundamental,      terstruktur
                berita
```

## Fitur

- **Satu panggilan, dari ticker ke narasi**: `analyze("BBCA")`.
- **Fokus IDX** (`BBCA` → `BBCA.JK` otomatis), dengan dukungan dasar kripto (`BTC` → `BTC-USD`).
- **Preprocessing yang sadar konteks IDX**: bank tidak dinilai dengan DER; satuan aneh Yahoo (DER dalam persen, dividend yield yang berubah-ubah) sudah dinormalisasi.
- **Indikator tanpa TA-Lib**: SMA/EMA, RSI & ATR (smoothing Wilder, sama dengan TradingView), MACD, Bollinger, rasio volume, drawdown, volatilitas, golden/death cross.
- **Sinyal yang bisa dijelaskan**: setiap sinyal punya alasan satu kalimat dan poin yang transparan → skor heuristik 0–100 untuk *screening* (bukan prediksi).
- **LLM anti-halusinasi**: model hanya diberi angka dari brief, dilarang memberi rekomendasi beli/jual atau target harga, dan judul berita dipagari sebagai data tak tepercaya (mitigasi *prompt injection*).
- **Bring your own LLM / data**: Gemini & OpenAI (juga endpoint kompatibel OpenAI seperti Ollama/OpenRouter) lewat extras; atau implementasikan `LLM` / `DataProvider` sendiri (cukup satu method).
- **Tanpa API key pun jalan**: narator offline berbasis aturan, deterministik.
- **Screener**: saring dan urutkan puluhan emiten sekaligus; satu ticker rusak tidak menggagalkan batch.
- **CLI** + **mode demo offline** (data sintetis) untuk mencoba tanpa jaringan.
- Disclaimer **selalu** ditambahkan ke setiap narasi oleh library.

## Cara menjalankan (dari nol)

Butuh **Python 3.10+** dan internet (kecuali mode demo). Belum ada di PyPI, jadi pasang dari source:

**macOS / Linux**

```bash
git clone https://github.com/twgosat/cuanlens
cd cuanlens
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[all]"
```

**Windows (PowerShell)**

```powershell
git clone https://github.com/twgosat/cuanlens
cd cuanlens
py -m venv .venv ; .venv\Scripts\Activate.ps1
pip install -e ".[all]"
```

> Hanya butuh salah satu LLM? Pakai `".[gemini]"` atau `".[openai]"`; tanpa extras (`pip install -e .`) tetap jalan dengan narator offline. Nama repo di URL di atas mengikuti nama repo Anda setelah di-rename; sebelum itu pakai `twgosat/home`.

**Langkah 1: coba tanpa jaringan dan tanpa API key** (data *sintetis*, hanya untuk melihat alur):

```bash
cuanlens analyze BBCA --demo
cuanlens screen BBCA BBRI BMRI TLKM ASII --demo
```

**Langkah 2: periksa jalur data live.** Perintah ini mengecek Python, harga/fundamental/berita dari Yahoo, dan kesiapan API key, lalu memberi tahu persis apa yang gagal dan cara memperbaikinya:

```bash
cuanlens doctor
```

**Langkah 3: data sungguhan** (narasi offline, tanpa LLM):

```bash
cuanlens analyze BBCA
cuanlens analyze BTC --market crypto
```

**Langkah 4 (opsional): narasi LLM.** Ambil API key di Google AI Studio (Gemini) atau platform OpenAI, lalu:

```bash
export GEMINI_API_KEY=...            # Windows PowerShell: $env:GEMINI_API_KEY="..."
cuanlens analyze BBRI --llm gemini
cuanlens analyze BBRI --llm openai --model gpt-4o-mini --fallback   # butuh OPENAI_API_KEY
```

Nama model bawaan bisa usang; ganti dengan `--model` atau variabel `CUANLENS_GEMINI_MODEL` / `CUANLENS_OPENAI_MODEL`. `--fallback` memakai narasi offline jika LLM gagal (kuota habis, key salah).

**Pengembangan:** `pip install -e ".[all,dev]"` lalu `pytest` (semua test berjalan offline) dan `ruff check src tests`.

### Masalah umum

| Gejala | Penyebab & solusi |
|---|---|
| `doctor` menampilkan `[FAIL] Harga ...` | Jaringan/VPN/proxy memblokir Yahoo (`query1/query2.finance.yahoo.com`, `fc.yahoo.com`), atau Yahoo sedang membatasi laju. Tunggu beberapa menit, matikan VPN, atau pakai `--demo`. |
| `Fundamental ... hanya N metrik` | Yahoo sering kosong/terlambat untuk emiten kecil. Analisis tetap jalan hanya dengan teknikal. |
| `Set GEMINI_API_KEY` / `needs: pip install` | API key belum di-export di terminal yang sama, atau extras belum dipasang. |
| `Cannot infer market for ...` | IDX = 4 huruf (`BBCA`). Kripto: `BTC`, `ETH-USD`, atau `--market crypto`. |

### Fitur CLI lainnya

Lihat persis apa yang dikirim ke LLM (tanpa memanggilnya) atau ambil JSON terstruktur:

```bash
cuanlens analyze TLKM --prompt
cuanlens analyze TLKM --json
```

Saring banyak emiten:

```bash
cuanlens screen --universe idx-starter --trend uptrend --min-score 55
cuanlens screen BBCA BBRI BMRI BBNI --max-pe 15 --min-roe 12
```

### Dari Python

```python
from cuanlens import analyze, screen
from cuanlens.llm import get_llm

result = analyze("BBCA", llm=get_llm("gemini"), fallback_to_offline=True)
print(result.to_markdown())

result.brief.overall_score        # 0-100, alat penyaring
result.brief.to_dict()            # semua angka & sinyal, siap disimpan / dikirim ke API

df = screen(["BBCA", "BBRI", "BMRI"], min_score=50)   # pandas DataFrame
print(df[["symbol", "trend", "pe", "roe_pct", "overall_score"]])
print(df.attrs["errors"])         # ticker yang gagal, tanpa menggagalkan batch
```

### Contoh keluaran (narator offline, **data sintetis**)

```markdown
# BBCA - BBCA (demo)
_Data per 2026-10-09 · skor gabungan 42/100 (lemah)_

## Ringkasan
BBCA ditutup di Rp 4.348; kondisi saat ini: tren mendatar/campuran. Dalam 1 bulan harga berubah +5,0% dan +7,5% dalam 3 bulan. ...

## Teknikal
- **RSI**: RSI 60,7 (zona wajar).
- **MACD**: Momentum MACD di bawah garis sinyal.

## Fundamental
- **PER**: PER 25,0x tergolong mahal; ekspektasi pertumbuhan sudah tinggi.
- **Pertumbuhan laba**: Laba turun 8,0% YoY.
...
⚠️ Bukan nasihat investasi. ...
```

Dengan LLM, bagian-bagian yang sama ditulis ulang dalam bahasa awam yang lebih mengalir.

## Cara kerja & titik perluasan

| Modul | Tugas |
|---|---|
| `providers/` | Ambil data (`YahooProvider`, `DemoProvider`, `CachedProvider`). Implementasikan `DataProvider.fetch()` untuk sumber lain (IDX, broker, Binance, CSV). |
| `technical.py`, `indicators.py` | OHLCV → indikator → sinyal teknikal |
| `fundamentals.py` | `info` Yahoo → fundamental bersih + sinyal; `Thresholds` bisa disesuaikan per sektor |
| `news.py` | Dedupe, buang HTML, batasi umur & jumlah, petunjuk sentimen leksikon |
| `brief.py` | Menyatukan semuanya jadi `StockBrief` (`to_dict`, `to_json`, `to_prompt_context`) |
| `prompts.py` | Prompt sistem ID/EN dengan guardrail |
| `llm/` | `GeminiLLM`, `OpenAILLM`; antarmuka `LLM.generate(system, prompt)` |
| `narrator.py` | `analyze()`, `narrate()`, narator offline |
| `screener.py` | `screen()` untuk banyak simbol |

Mengubah ambang valuasi:

```python
from cuanlens import Thresholds, analyze
analyze("ADRO", thresholds=Thresholds(pe_expensive=12, der_high=1.5))
```

## Status & batasan (baca ini)

- **Alpha (0.1)**. Logika inti punya test offline (tanpa jaringan atau API key). Data Yahoo bersifat tidak resmi dan formatnya sering berubah; adapter sudah dibuat defensif, tetapi **laporkan lewat Issue** jika ada field yang berubah atau ticker yang gagal.
- Yahoo Finance dipakai untuk penggunaan pribadi/riset sesuai ketentuannya. Untuk produk komersial, pakai sumber data berlisensi lewat `DataProvider`.
- Fundamental IDX di Yahoo kadang kosong atau terlambat, terutama emiten kecil. Library akan menyebutkannya di `notes`, bukan menebak.
- Skor 0–100 adalah heuristik transparan untuk menyaring, **bukan** prediksi, **bukan** sinyal beli/jual.
- Ambang bawaan bersifat generik. Sektor berbeda (bank, tambang, properti) layak punya ambang berbeda.

## ⚠️ Disclaimer

CuanLens adalah alat edukasi dan riset, **bukan nasihat investasi, rekomendasi, atau ajakan membeli/menjual efek maupun aset kripto**. Data dapat tertunda atau keliru, dan keluaran LLM bisa salah. Investasi mengandung risiko kehilangan modal. Anda bertanggung jawab penuh atas keputusan Anda.

## Berkontribusi

PR dan Issue sangat diterima, terutama: provider data baru, ambang per sektor, sinyal baru (dengan test), dan terjemahan prompt. Lihat [CONTRIBUTING.md](CONTRIBUTING.md). Arsitektur untuk membangun produk di atas library ini ada di [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Lisensi

[MIT](LICENSE)
