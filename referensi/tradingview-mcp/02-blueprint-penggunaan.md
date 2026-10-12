# 02 · Blueprint penggunaan

## Prasyarat

- TradingView **Desktop** (bukan browser) dengan langganan yang sesuai kebutuhan data.
- Node.js 18+.
- Claude Code (untuk tool MCP) atau terminal biasa (untuk CLI `tv`).
- macOS, Windows, atau Linux.

> Repo ini tidak bisa dijalankan di sandbox cloud/CI tanpa TradingView Desktop. Pasang di mesin Anda sendiri.

## A. Setup (±10 menit)

### 1. Pasang

```bash
git clone https://github.com/tradesdontlie/tradingview-mcp.git ~/tradingview-mcp
cd ~/tradingview-mcp
npm install
```

Saran: setelah clone, catat commit yang Anda periksa (`git rev-parse HEAD`) dan **jangan** otomatis ikut `main`
(lihat [05](05-keamanan-dan-risiko.md) soal `tv_update`).

### 2. Jalankan TradingView dengan port debug

| OS | Perintah |
|---|---|
| macOS | `./scripts/launch_tv_debug_mac.sh` atau `/Applications/TradingView.app/Contents/MacOS/TradingView --remote-debugging-port=9222` |
| Windows | `scripts\launch_tv_debug.bat` (menemukan paket MSIX lewat `Get-AppxPackage`) |
| Linux | `./scripts/launch_tv_debug_linux.sh` atau `/opt/TradingView/tradingview --remote-debugging-port=9222` |
| Semua | Setelah MCP tersambung: minta Claude "pakai `tv_launch`" |

Port harus tetap di `localhost`. Jangan dibuka ke jaringan.

### 3. Daftarkan ke Claude Code

`~/.claude/.mcp.json` (global) atau `.mcp.json` (per proyek). Gabungkan dengan isi yang sudah ada, jangan menimpa:

```json
{
  "mcpServers": {
    "tradingview": {
      "command": "node",
      "args": ["/jalur/absolut/ke/tradingview-mcp/src/server.js"]
    }
  }
}
```

Port lain / host lain (opsional):

```json
{
  "mcpServers": {
    "tradingview": {
      "command": "node",
      "args": ["/jalur/absolut/ke/tradingview-mcp/src/server.js"],
      "env": { "TV_CDP_PORT": "9333" }
    }
  }
}
```

### 4. Restart Claude Code, lalu verifikasi

Minta: *"Gunakan tv_health_check"*. Hasil sehat:

```json
{ "success": true, "cdp_connected": true, "chart_symbol": "...", "api_available": true }
```

### 5. CLI (opsional)

```bash
cd ~/tradingview-mcp && npm link   # setelah itu `tv` tersedia di mana saja
tv status
```

### Pemecahan masalah

| Gejala | Tindakan |
|---|---|
| `cdp_connected: false` / `ECONNREFUSED` | TradingView belum jalan dengan `--remote-debugging-port=9222`, atau portnya bentrok |
| Server MCP tidak muncul | Periksa sintaks JSON dan jalur absolut; restart Claude Code |
| Data basi / kosong | Chart masih memuat; tunggu beberapa detik |
| Tool Pine gagal | Buka panel dulu: `ui_open_panel pine-editor open` |
| Windows "Access is denied" dari `WindowsApps` | Pakai `tv_launch` (menyalin paket otomatis); jangan ubah ACL `WindowsApps` dengan `icacls` |
| Tool pine graphics kosong | Indikator harus terlihat di chart; cek `study_filter` |
| `tv` tidak ditemukan | `npm link` dari folder proyek |

## B. Aturan hemat konteks (wajib diingat)

1. `data_get_ohlcv` selalu dengan `summary: true` kecuali butuh bar satu per satu.
2. Tool `data_get_pine_*` selalu dengan `study_filter`.
3. Jangan `verbose: true` kecuali butuh ID/warna mentah.
4. Hindari `pine_get_source` pada skrip besar (bisa 200 KB+); baca hanya bila akan mengedit.
5. Hindari `data_get_indicator` pada indikator terproteksi (input berupa blob terenkode); pakai `data_get_study_values`.
6. Untuk gambaran visual, `capture_screenshot` (mengembalikan **path file**, bukan data gambar) lebih murah daripada menarik banyak data.
7. Panggil `chart_get_state` **sekali** di awal dan pakai ulang `entity_id`.
8. `count` OHLCV: 20 untuk cepat, 100 untuk analisis, 500 hanya jika perlu.
9. `chart_manage_indicator` butuh **nama lengkap**: "Relative Strength Index" (bukan RSI), "Moving Average Exponential" (bukan EMA), "Bollinger Bands", "MACD", "Volume", "Moving Average" (SMA).

## C. Resep alur kerja

### 1. "Apa yang ada di chart saya?"

`chart_get_state` → `data_get_study_values` → `quote_get`

### 2. Analisis lengkap

```
quote_get
data_get_study_values
data_get_pine_lines   (study_filter)
data_get_pine_labels  (study_filter)
data_get_pine_tables  (study_filter)
data_get_ohlcv        (summary: true)
capture_screenshot    (region: chart)
```

Contoh prompt:
> Analisis BBCA timeframe D. Baca RSI dan MACD, level dari indikator "NY Levels", lalu ringkas bias
> (bullish/bearish/netral) dengan alasannya. Jangan beri rekomendasi beli/jual.

### 3. Mengembangkan Pine Script (penggunaan terkuat)

Dua jalur:

**Via tool MCP** (tanpa file lokal)
```
pine_new {type}  →  pine_set_source  →  pine_smart_compile  →  pine_get_errors  →  (perbaiki)  →  pine_save
                                                    ↘ pine_get_console (membaca log.info)
```

**Via skrip file** (dipakai skill `pine-develop`)
```bash
node scripts/pine_pull.js     # editor → scripts/current.pine
# edit scripts/current.pine
node scripts/pine_push.js     # file → editor, lalu klik compile & laporkan error
```

Validasi tanpa menyentuh chart:
- `pine_analyze` — analisis statis offline (array di luar batas, `array.first()/last()` tak terjaga, batas loop, cast bool implisit).
- `pine_check` — compile via API server TradingView, tanpa chart (memanggil jaringan, lihat [05](05-keamanan-dan-risiko.md)).

Aturan emas dari skill: skrip wajib `//@version=6`, input lewat `input.*()` bergrup, dan **jangan pernah menyatakan selesai tanpa compile bersih**.

### 4. Replay / latihan trading simulasi

```
chart_set_symbol → chart_set_timeframe → replay_start {date: "2025-03-01"}
→ data_get_ohlcv (konteks) → capture_screenshot
→ loop: replay_step (atau replay_autoplay {speed}) → replay_status
→ replay_trade {action: buy|sell|close}
→ replay_status (P&L) → replay_stop
```

Kecepatan autoplay yang valid (ms): 100, 143, 200, 300, 1000, 2000, 3000, 5000, 10000. Trade hanya di mode replay (simulasi).

### 5. Scan banyak simbol

```
batch_run { symbols: ["BBCA","BBRI","BMRI"], timeframes: ["D"], action: "get_ohlcv", ohlcv_count: 50, delay_ms: 2000 }
```
Aksi yang didukung: `screenshot`, `get_ohlcv`, `get_strategy_results`. Untuk metrik kustom, lakukan loop manual:
`chart_set_symbol` → `chart_set_timeframe` → baca data → catat. Daftar simbol bisa dari `watchlist_get`.

### 6. Laporan performa strategi

`data_get_strategy_results` → `data_get_trades` (maks 20) → `data_get_equity` → `chart_get_state` → `symbol_info`
→ `capture_screenshot` region `chart` dan `strategy_tester`. Agen `performance-analyst` mengotomatiskannya.

### 7. Grid multi-chart

`pane_set_layout {layout: "2x2"}` → `pane_set_symbol {index: 0, symbol: "ES1!"}` … → `tv stream all` untuk memantau semua pane.
Kode layout: `s`, `2h`, `2v`, `2-1`, `1-2`, `3h`, `3v`, `4` (2x2), `6`, `8`.

### 8. Menggambar dan alert

- `draw_shape {shape: "horizontal_line", point: {time, price}}`; bentuk: `horizontal_line`, `vertical_line`, `trend_line` (butuh `point2`), `rectangle`, `text`.
- `alert_create {condition: "crossing"|"greater_than"|"less_than", price, message}`; `alert_list`; `alert_delete {alert_id | delete_all}`.

### 9. Memakai CLI dari terminal

```bash
tv status
tv quote | jq '.last'
tv symbol AAPL && tv timeframe D
tv ohlcv --summary
tv screenshot -r chart
tv pine compile
tv pane layout 2x2 && tv pane symbol 1 ES1!
tv stream quote | jq '.close'
```

### 10. Membaca indikator terproteksi / kustom lewat UI

`ui_find_element` → `ui_click` / `ui_mouse_click` / `ui_keyboard` / `ui_type_text`. `ui_evaluate` adalah jalan terakhir (JS bebas).

## D. Prinsip pakai yang aman

- Anggap setiap tool yang mengubah chart (ganti simbol, tambah indikator, gambar, alert) langsung dieksekusi tanpa konfirmasi.
- Minta Claude **membersihkan** yang ia tambahkan (`chart_manage_indicator remove`, `draw_clear`).
- Simpan layout penting sebelum eksperimen (`layout_list`/`layout_switch`), karena `tv_launch` bisa menutup TradingView.
- Jangan lanjutkan ke eksekusi order otomatis dari keluaran agen. Repo ini melarangnya di bagian Disclaimer.
