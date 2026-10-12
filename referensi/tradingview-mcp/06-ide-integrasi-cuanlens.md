# 06 · Ide integrasi dengan CuanLens

> **Status: usulan.** Tidak ada bagian dari ini yang sudah dibuat atau diuji. Ia disusun dari membaca
> `docs/ARCHITECTURE.md`, `CONTRIBUTING.md`, dan layout `src/cuanlens/` repo ini, dibandingkan dengan
> kemampuan `tradingview-mcp` ([03](03-referensi-tool.md)).

## Batas yang tidak boleh dilanggar

`docs/ARCHITECTURE.md` merencanakan produk berbayar, dan menyebut sendiri bahwa sumber data produk harus
**berlisensi**. Disclaimer `tradingview-mcp` melarang redistribusi/komersialisasi data TradingView dan
menyatakan alat ini hanya untuk penggunaan pribadi, edukasi, dan riset ([05](05-keamanan-dan-risiko.md)).
Maka:

| Boleh dipertimbangkan | Jangan |
|---|---|
| Alat bantu **pengembangan** di mesin Anda: mencocokkan angka, memprototipe, memeriksa visual | Menjadikan TradingView sebagai `DataProvider` di library atau di produk berbayar |
| Membandingkan hasil secara manual, mencatat selisihnya sebagai angka toleransi | Menyimpan/menyajikan data OHLCV atau indikator TradingView di repo, fixture, dataset, atau layanan |
| Memakai Pine Script buatan sendiri sebagai referensi visual | Menjalankannya di server/worker yang melayani pengguna lain |
| | Mengotomasi keputusan/order dari keluarannya |

Dan CuanLens menargetkan **IDX & kripto**: mengikuti `CONTRIBUTING.md`, prompt tidak boleh memberi rekomendasi
beli/jual. Prinsip itu sejalan dengan batasan `tradingview-mcp`.

## Ide 1 — Verifikasi indikator CuanLens terhadap TradingView

Dokumentasi CuanLens menyebut RSI & ATR memakai smoothing Wilder "sama dengan TradingView" dan aturan emas #5
meminta indikator diuji terhadap hitungan manual. Alur pemeriksaan satu kali (bukan bagian suite tes):

1. `tv_health_check`, lalu `chart_set_symbol` ke emiten (mis. `IDX:BBCA`) dan `chart_set_timeframe D`.
2. `chart_manage_indicator add "Relative Strength Index"`, `"MACD"`, `"Bollinger Bands"`, `"Average True Range"`.
3. `data_get_study_values` dan `data_get_ohlcv {count: 60}` untuk tanggal yang sama.
4. Jalankan `cuanlens analyze BBCA --json` dan bandingkan RSI/MACD/Bollinger/ATR pada bar terakhir yang sama.
5. Catat selisih sebagai **angka saja** (mis. "RSI beda 0,3 poin; sumber: beda penyedia harga"). Jangan menaruh data
   mentah TradingView ke repo; sumber tes tetap hitungan manual atau data sintetis.

Hasil yang berguna: deteksi perbedaan definisi (periode, sumber harga *close* vs *adjusted close*, penyesuaian
corporate action) antara Yahoo dan TradingView, yang sering menjadi sumber selisih angka.

## Ide 2 — Memprototipe sinyal sebagai Pine Script untuk pengecekan visual

Aturan emas #2: "sinyal harus bisa dijelaskan". Sebelum menulis sinyal baru di `signals.py`:

1. Dengan skill `pine-develop`/loop `pine_set_source` → `pine_smart_compile`, buat indikator Pine kecil yang
   menandai kapan sinyal akan menyala (misal golden cross dengan filter volume).
2. `capture_screenshot` dan telusuri tanggal-tanggal menyala di berbagai emiten.
3. Setelah yakin, tulis ulang di Python dengan alasan satu kalimat berbahasa Indonesia + tes yang membuktikan
   kapan menyala dan kapan tidak.

Pine Script hanya prototipe visual; implementasi dan tes tetap di Python.

## Ide 3 — Kandidat ambang `Thresholds` per sektor

`CONTRIBUTING.md` meminta ambang per sektor IDX (bank, tambang, consumer, properti). Dengan `batch_run`
(`get_ohlcv`) atau `pane_set_layout 2x2` + `pane_set_symbol`, Anda bisa melihat bentuk distribusi RSI/volatilitas
beberapa emiten sejenis sambil menimbang ambang. Tetap: hasilkan ambang dari data yang **boleh** dipakai di repo
(Yahoo untuk eksperimen, atau data berlisensi), bukan dari data TradingView.

## Ide 4 — Meniru pola desainnya (tanpa mengambil kodenya)

Pola dari `tradingview-mcp` yang selaras dengan prinsip CuanLens:

| Pola | Padanan di CuanLens |
|---|---|
| Output ringkas default, rinci bila diminta (`summary`, `verbose`) | `StockBrief` ±900 token; `--json` untuk rinci |
| `core` terpisah dari transport (MCP/CLI) | `analyze()` / `screen()` terpisah dari `cli.py` |
| Respons seragam `{success, error}` | `errors.py` dan atribut `df.attrs["errors"]` pada `screen()` |
| Panduan pemilihan tool di server `instructions` | Bila kelak CuanLens menyediakan server MCP sendiri, pakai pola yang sama |
| Sanitasi di perbatasan | Pagar `<berita>` dan data tak tepercaya di prompt |

**Ide besar (opsional):** server MCP milik CuanLens sendiri, dengan tool `analyze_stock`, `screen_stocks`,
`get_brief`, bersumber dari provider yang Anda punya lisensinya. Sudah ada struktur yang cocok (`analyze()`,
`screen()`, `to_dict()`). Itu pekerjaan terpisah dari studi ini.

## Ide 5 — Yang sebaiknya dihindari

- **Meniru `ui_evaluate`/injeksi JS ke aplikasi pihak ketiga** di produk. Ia rapuh dan berisiko kepatuhan.
- **Alert dari keluaran TradingView.** Rencana alert Telegram di arsitektur harus berbasis data berlisensi Anda.
- **Menjadikannya jalur "otomatis kirim sinyal"**: bertentangan dengan Disclaimer repo itu dan dengan kehati-hatian
  OJK yang dicatat di `docs/ARCHITECTURE.md`.

## Langkah berikutnya yang masuk akal

1. Pasang `tradingview-mcp` di mesin Anda dengan checklist di [05](05-keamanan-dan-risiko.md).
2. Lakukan Ide 1 untuk 3–5 emiten IDX dan satu kripto; catat selisih sebagai angka.
3. Dari temuan itu, putuskan apakah ada perbaikan di `indicators.py` atau catatan di dokumentasi.
4. Baru pertimbangkan Ide 2 dan 3.
