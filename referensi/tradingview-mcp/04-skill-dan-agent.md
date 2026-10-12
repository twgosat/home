# 04 · Skill dan agent bawaan

Repo menyertakan 5 **skill** (`skills/*/SKILL.md`) dan 1 **agent** (`agents/performance-analyst.md`).
Skill adalah instruksi alur kerja bertahap yang dimuat Claude saat topiknya cocok; agent adalah subagen
dengan peran tetap. Semuanya hanya memerintahkan urutan pemanggilan tool, tanpa kode tambahan.

| Nama | Dipakai saat | Urutan inti |
|---|---|---|
| `chart-analysis` | Analisis teknikal / review chart | `chart_set_symbol` → `chart_set_timeframe` → `chart_manage_indicator` (+ `indicator_set_inputs`) → `chart_scroll_to_date` / `chart_set_visible_range` → `draw_shape` → `capture_screenshot` + `data_get_ohlcv` + `quote_get` + `symbol_info` → laporan (harga, support/resistance, bacaan indikator, bias) → **bersihkan** indikator/gambar yang Anda tambahkan sendiri |
| `pine-develop` | Membuat indikator/strategi Pine | Klarifikasi tujuan → `node scripts/pine_pull.js` (jika memodifikasi) → tulis `scripts/current.pine` (`//@version=6`, `input.*`, komentar) → `node scripts/pine_push.js` → perbaiki error → `capture_screenshot` / `data_get_strategy_results` → iterasi. **Jangan klaim selesai tanpa compile bersih.** |
| `replay-practice` | Latihan manual di replay | Setup simbol/timeframe → `replay_start` → konteks `data_get_ohlcv` + screenshot → `replay_step`/`replay_autoplay` → `replay_trade` → `replay_status` → review (jumlah trade, win/loss, net P&L, pelajaran) → `replay_stop` |
| `multi-symbol-scan` | Membandingkan banyak instrumen | Tentukan simbol (atau `watchlist_get`), timeframe, kriteria → `batch_run` (`get_strategy_results` / `screenshot`) atau loop manual → tabel perbandingan terurut → screenshot 1–2 teratas → opsional `watchlist_add` |
| `strategy-report` | Setelah backtest strategi | `data_get_strategy_results` + `data_get_trades` + `data_get_equity` + `chart_get_state` + `symbol_info` → screenshot `chart` dan `strategy_tester` → template laporan (ringkasan, metrik, kekuatan, kelemahan, rekomendasi) → heuristik saran |
| agent `performance-analyst` | Meninjau hasil backtest | Mengumpulkan data yang sama, lalu menilai profitabilitas, konsistensi, risiko, dan kualitas edge. Model `sonnet`, `tools: ["*"]` |

## Heuristik saran dari `strategy-report`

- Win rate < 50% tetapi profit factor > 1 → perketat entry.
- Max drawdown > 20% → ukuran posisi / stop loss.
- Profit factor < 1,2 → strategi mungkin perlu diubah mendasar.
- Trade sedikit → lebarkan lookback atau longgarkan kriteria entry.
- Target profit factor yang disebut skill: > 1,5.

## Cara memasangnya

Skill/agent di repo ini hanya terbaca otomatis jika Claude Code dijalankan di dalam folder repo tersebut
(selain `CLAUDE.md`, yang dimuat saat bekerja di sana). Agar tersedia di proyek lain, salin ke:

- `~/.claude/skills/<nama>/SKILL.md` dan `~/.claude/agents/<nama>.md` (semua proyek), atau
- `.claude/skills/<nama>/SKILL.md` dan `.claude/agents/<nama>.md` (satu proyek).

Catatan: skill `pine-develop` merujuk `node scripts/pine_pull.js` / `pine_push.js`, jalur relatif ke repo
`tradingview-mcp`. Jika disalin ke proyek lain, ubah menjadi jalur absolut atau pakai tool MCP `pine_set_source`
+ `pine_smart_compile`.

## Pola yang layak ditiru untuk skill buatan sendiri

1. Frontmatter `name` + `description` yang menyebut **kapan dipakai**.
2. Langkah bernomor dengan nama tool persis.
3. Tabel/templat keluaran supaya laporan konsisten.
4. Bagian "Cleanup" untuk mengembalikan keadaan chart.
5. Aturan penutup yang tak boleh dilanggar (contoh: "selalu compile setelah setiap perubahan").

## Hal yang tidak ada di sana

Tidak ada skill untuk Pine Script v6 sebagai bahasa (referensi sintaks), screening fundamental, atau manajemen risiko.
Skill hanya mengatur tool; kualitas Pine yang dihasilkan bergantung pada model.
