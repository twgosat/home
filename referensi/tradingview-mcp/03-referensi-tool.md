# 03 · Referensi tool (84 tool MCP)

Dihitung dari panggilan `server.tool(...)` di `src/tools/*.js` pada commit `c05b8f5`.
Semua tool mengembalikan JSON `{ success: true|false, ... }`.

Ringkasan: health 5 · chart 10 · data 12 · capture 1 · drawing 5 · alerts 3 · replay 6 · indicators 4 ·
watchlist 4 · ui 12 · pane 4 · tab 5 · pine 12 · batch 1 = **84**.

## Koneksi & kesehatan (5) — `tools/health.js`

| Tool | Fungsi | Parameter |
|---|---|---|
| `tv_health_check` | Cek koneksi CDP dan state chart | — |
| `tv_discover` | Laporkan jalur API internal TradingView mana yang tersedia | — |
| `tv_ui_state` | Panel yang terbuka, tombol terlihat/aktif | — |
| `tv_launch` | Luncurkan TradingView dengan CDP; auto-deteksi Mac/Win/Linux termasuk MSIX | `port?` (9222), `kill_existing?` (**default true**) |
| `tv_update` | Update server ini: fast-forward `origin/main` + `npm ci` bila lockfile berubah | — |

## Chart (10) — `tools/chart.js`

| Tool | Fungsi | Parameter |
|---|---|---|
| `chart_get_state` | Simbol, timeframe, tipe chart, daftar indikator + entity ID | — |
| `chart_set_symbol` | Ganti simbol | `symbol` (`AAPL`, `ES1!`, `NYMEX:CL1!`) |
| `chart_set_timeframe` | Ganti resolusi | `timeframe` (`1`,`5`,`15`,`60`,`D`,`W`,`M`) |
| `chart_set_type` | Ganti tipe | `chart_type` nama atau angka: Bars 0, Candles 1, Line 2, Area 3, Renko 4, Kagi 5, PointAndFigure 6, LineBreak 7, HeikinAshi 8, HollowCandles 9 |
| `chart_manage_indicator` | Tambah/hapus indikator | `action` add/remove, `indicator` (nama lengkap), `entity_id` (untuk remove), `inputs?` (JSON string) |
| `chart_get_visible_range` | Rentang tanggal dan bar yang terlihat | — |
| `chart_set_visible_range` | Zoom ke rentang | `from`, `to` (unix detik) |
| `chart_scroll_to_date` | Tengahkan pada tanggal | `date` (ISO atau unix string) |
| `symbol_info` | Metadata simbol (nama, bursa, tipe, deskripsi) | — |
| `symbol_search` | Cari simbol | `query`, `type?` (stock/futures/crypto/forex). *Memanggil `symbol-search.tradingview.com`* |

## Data (12) — `tools/data.js`

| Tool | Fungsi | Parameter |
|---|---|---|
| `quote_get` | Harga, OHLC, volume | `symbol?` — jika beda dari chart, chart dialihkan sebentar lalu dipulihkan (+1–2 dtk) |
| `data_get_ohlcv` | Bar harga | `count?` (maks 500, default 100), `summary?` |
| `data_get_study_values` | Nilai semua indikator terlihat dari Data Window | — |
| `data_get_indicator` | Info + input satu indikator | `entity_id` |
| `data_get_pine_lines` | Level horizontal `line.new` (dedup, urut tinggi→rendah) | `study_filter?`, `verbose?` |
| `data_get_pine_labels` | Teks + harga `label.new` | `study_filter?`, `max_labels?` (50), `verbose?` |
| `data_get_pine_tables` | Baris tabel `table.new` | `study_filter?` |
| `data_get_pine_boxes` | Zona `box.new` sebagai {high, low} | `study_filter?`, `verbose?` |
| `data_get_strategy_results` | Metrik Strategy Tester (otomatis membuka panel dan un-hide strategi) | — |
| `data_get_trades` | Daftar trade Strategy Tester | `max_trades?` (batas 20) |
| `data_get_equity` | Kurva ekuitas | — |
| `depth_get` | Order book / DOM | — |

## Capture (1) — `tools/capture.js`

| Tool | Fungsi | Parameter |
|---|---|---|
| `capture_screenshot` | Simpan screenshot ke `screenshots/` (mengembalikan path) | `region?` full/chart/strategy_tester, `filename?`, `method?` cdp/api, `wait_for_render?` (pakai setelah ganti simbol/timeframe) |

## Gambar (5) — `tools/drawing.js`

| Tool | Fungsi | Parameter |
|---|---|---|
| `draw_shape` | Gambar | `shape` horizontal_line/vertical_line/trend_line/rectangle/text, `point` {time, price}, `point2?`, `overrides?` (JSON gaya), `text?` |
| `draw_list` | Daftar gambar | — |
| `draw_get_properties` | Properti satu gambar | `entity_id` |
| `draw_remove_one` | Hapus satu | `entity_id` |
| `draw_clear` | Hapus semua | — |

## Alert (3) — `tools/alerts.js`

| Tool | Fungsi | Parameter |
|---|---|---|
| `alert_create` | Alert harga pada simbol aktif (via `pricealerts.tradingview.com` dengan sesi aplikasi) | `condition` crossing/greater_than/less_than, `price`, `message?` |
| `alert_list` | Alert aktif | — |
| `alert_delete` | Hapus | `alert_id?` atau `delete_all?` |

## Replay (6) — `tools/replay.js`

| Tool | Fungsi | Parameter |
|---|---|---|
| `replay_start` | Masuk mode replay | `date?` (YYYY-MM-DD) |
| `replay_step` | Maju satu bar | — |
| `replay_autoplay` | Toggle autoplay | `speed?` ms ∈ {100,143,200,300,1000,2000,3000,5000,10000} |
| `replay_trade` | Order simulasi | `action` buy/sell/close |
| `replay_status` | Posisi, P&L, tanggal | — |
| `replay_stop` | Kembali ke realtime | — |

## Indikator (4) — `tools/indicators.js`

| Tool | Fungsi | Parameter |
|---|---|---|
| `indicator_set_inputs` | Ubah input | `entity_id`, `inputs` (JSON string, kunci = ID input) |
| `indicator_toggle_visibility` | Tampil/sembunyi | `entity_id`, `visible` |
| `indicator_search` | Cari di dialog Indicators (built-in, komunitas, My scripts) | `query`, `limit?` (25) |
| `indicator_add` | Cari lalu tambahkan (termasuk strategi/skrip komunitas); mengembalikan `entity_id` | `query`, `match?`, `section?` |

## Watchlist (4) — `tools/watchlist.js`

`watchlist_get` (simbol + harga + perubahan) · `watchlist_add {symbol}` · `watchlist_add_bulk {symbols[]}` · `watchlist_remove {symbols[]}`

## UI & layout (12) — `tools/ui.js`

| Tool | Fungsi | Parameter |
|---|---|---|
| `ui_click` | Klik elemen | `by` aria-label/data-name/text/class-contains, `value` |
| `ui_open_panel` | Buka/tutup panel | `panel` pine-editor/strategy-tester/watchlist/alerts/trading, `action` open/close/toggle |
| `ui_fullscreen` | Toggle layar penuh | — |
| `layout_list` | Layout tersimpan | — |
| `layout_switch` | Pindah layout | `name` (nama atau ID) |
| `ui_keyboard` | Tekan tombol | `key`, `modifiers?` ctrl/alt/shift/meta |
| `ui_type_text` | Ketik ke input terfokus | `text` |
| `ui_hover` | Hover elemen | `by`, `value` |
| `ui_scroll` | Scroll | `direction`, `amount?` (300 px) |
| `ui_mouse_click` | Klik koordinat | `x`, `y`, `button?`, `double_click?` |
| `ui_find_element` | Cari elemen + posisinya | `query`, `strategy?` text/aria-label/css |
| `ui_evaluate` | **Eksekusi JavaScript bebas** di halaman TradingView | `expression` |

## Pane (4) & Tab (5)

| Tool | Fungsi | Parameter |
|---|---|---|
| `pane_list` | Pane + simbol + status aktif | — |
| `pane_set_layout` | Ubah grid | `layout` s, 2h, 2v, 2-1, 1-2, 3h, 3v, 4, 6, 8 (alias: single, 2x1, 1x2, 2x2, quad) |
| `pane_focus` | Fokus pane | `index` (mulai 0) |
| `pane_set_symbol` | Simbol per pane | `index`, `symbol` |
| `tab_list` | Tab terbuka | — |
| `tab_new` | Tab baru | `layout?` ("new" atau nama layout), `name?` |
| `layout_new` | Layout kosong baru (tab baru) | `name?` |
| `tab_close` | Tutup tab aktif | — |
| `tab_switch` | Pindah tab; klien CDP ikut menyambung ulang ke tab itu | `index` |

## Pine Script (12) — `tools/pine.js`

| Tool | Fungsi | Parameter |
|---|---|---|
| `pine_set_source` | Suntik kode ke editor | `source` |
| `pine_smart_compile` | Compile cerdas: deteksi tombol, cek error, laporkan perubahan studi | — |
| `pine_compile` | Compile / add to chart (versi dasar) | — |
| `pine_get_errors` | Error compile dari marker Monaco | — |
| `pine_get_console` | Log editor (`log.info()`, pesan compile) | — |
| `pine_get_source` | Baca kode (bisa 200 KB+) | — |
| `pine_save` | Simpan (Ctrl+S) ke cloud TradingView | — |
| `pine_new` | Skrip kosong | `type` indicator/strategy/library |
| `pine_open` | Buka skrip tersimpan | `name` |
| `pine_list_scripts` | Daftar skrip tersimpan (via `pine-facade.tradingview.com`) | — |
| `pine_analyze` | Analisis statis **offline** tanpa compile | `source` |
| `pine_check` | Compile lewat API server TradingView tanpa chart | `source` |

## Batch (1) — `tools/batch.js`

`batch_run { symbols[], timeframes?[], action: screenshot|get_ohlcv|get_strategy_results, delay_ms? (2000), ohlcv_count? (100) }`

## Perintah CLI `tv` (setara tool + `stream`)

```
tv status / launch / state / symbol / timeframe / type / info / search
tv quote / ohlcv / values
tv data lines|labels|tables|boxes|strategy|trades|equity|depth|indicator
tv pine get|set|compile|analyze|check|save|new|open|list|errors|console
tv draw shape|list|get|remove|clear
tv alert list|create|delete
tv watchlist get|add
tv indicator add|remove|toggle|set|get
tv layout list|switch
tv pane list|layout|focus|symbol
tv tab list|new|close|switch
tv replay start|step|stop|status|autoplay|trade
tv stream quote|bars|values|lines|labels|tables|all      # JSONL tanpa henti; --interval/-i ms, --filter/-f
tv ui click|keyboard|hover|scroll|find|eval|type|panel|fullscreen|mouse
tv screenshot / discover / ui-state / range / scroll
```

`tv stream` tidak punya padanan tool MCP. Default interval: `quote` 300 ms, `bars`/`values`/`all` 500 ms, `lines`/`labels` 1000 ms, `tables` 2000 ms.

## Perkiraan ukuran keluaran (mode ringkas)

| Tool | Ukuran |
|---|---|
| `quote_get` | ~200 B |
| `data_get_study_values` | ~500 B |
| `data_get_pine_lines` | 1–3 KB per studi |
| `data_get_pine_labels` | 2–5 KB per studi |
| `data_get_pine_tables` | 1–4 KB per studi |
| `data_get_pine_boxes` | 1–2 KB per studi |
| `data_get_ohlcv` summary / 100 bar | ~500 B / ~8 KB |
| `pine_get_source` skrip kompleks | bisa >200 KB |
