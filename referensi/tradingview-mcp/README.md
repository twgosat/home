# Studi: tradesdontlie/tradingview-mcp

Catatan pembelajaran dan blueprint penggunaan dari repo
[tradesdontlie/tradingview-mcp](https://github.com/tradesdontlie/tradingview-mcp).

- **Versi yang dipelajari**: commit `c05b8f5` (branch `main`, 28 Jul 2026), lisensi MIT.
- **Cara belajar**: seluruh README, `CLAUDE.md`, `SETUP_GUIDE.md`, `SECURITY.md`, `RESEARCH.md`,
  5 skill, 1 agent, serta source `src/server.js`, `src/connection.js`, `src/tools/*`, `src/core/*`,
  dan `scripts/*` dibaca langsung. Jumlah tool dihitung dari kode, bukan dari README.
- **Yang belum dilakukan**: tool tidak dijalankan. Ia butuh TradingView Desktop berbayar yang berjalan
  lokal, yang tidak ada di lingkungan ini. Semua isi dokumen berasal dari membaca kode, bukan dari uji coba.

## Satu paragraf

`tradingview-mcp` adalah server **MCP** (Model Context Protocol, stdio) dan CLI `tv` berbasis Node.js
yang membuat aplikasi **TradingView Desktop** yang berjalan di komputer Anda bisa dibaca dan dikendalikan
oleh Claude. Ia tidak memakai API resmi TradingView. Ia menyambung ke port debug Chromium/Electron
(**Chrome DevTools Protocol**, `127.0.0.1:9222`) lalu mengeksekusi JavaScript di dalam halaman TradingView.
Hasilnya 84 tool: baca state chart, nilai indikator, level/label/tabel hasil `line.new`/`label.new`/`table.new`
dari indikator Pine, OHLCV; ganti simbol/timeframe; tulis dan compile Pine Script; replay; screenshot; alert;
dan otomasi UI.

## Isi folder

| File | Isi |
|---|---|
| [01-arsitektur.md](01-arsitektur.md) | Cara kerja, struktur kode, alur satu panggilan tool, pola desain |
| [02-blueprint-penggunaan.md](02-blueprint-penggunaan.md) | Setup langkah demi langkah dan resep alur kerja (analisis, Pine, replay, scan, CLI) |
| [03-referensi-tool.md](03-referensi-tool.md) | Seluruh 84 tool MCP per kelompok, plus perintah CLI dan `stream` |
| [04-skill-dan-agent.md](04-skill-dan-agent.md) | 5 skill dan 1 agent bawaan repo, dan pola yang bisa ditiru |
| [05-keamanan-dan-risiko.md](05-keamanan-dan-risiko.md) | Risiko, hal yang README klaim tapi kode tidak persis begitu, ToS, rekomendasi hardening |
| [06-ide-integrasi-cuanlens.md](06-ide-integrasi-cuanlens.md) | Usulan memakainya bersama CuanLens (repo ini). Ini usulan, bukan fitur yang sudah ada |

## Ringkasan penilaian

**Kuat**
- Desain tool yang hemat konteks: output ringkas secara default (`summary`, `study_filter`, dedup level Pine).
- Pemisahan `core/` (logika) dari `tools/` (MCP) dan `cli/` (CLI) membuat satu logika dipakai dua antarmuka.
- Loop pengembangan Pine Script (set source → compile → baca error → perbaiki) adalah penggunaan paling bernilai.
- Ada sanitasi input untuk kode yang disuntikkan ke CDP (`safeString`, `requireFinite`) dan tes untuk itu.

**Perlu hati-hati**
- Bergantung pada API internal TradingView yang tidak terdokumentasi; bisa rusak di setiap update TradingView.
- Port debug 9222 tidak punya autentikasi; tool `ui_evaluate` mengeksekusi JS bebas di sesi TradingView Anda yang sedang login.
- Beberapa tool memanggil server TradingView (alert, pencarian simbol, Pine), berlawanan dengan kesan di README.
- `tv_launch` secara default **mematikan** instance TradingView yang sedang berjalan; `tv_update` menarik kode baru dari `origin/main`.
- Penulis sendiri menyatakan pemakaian ini dapat bertentangan dengan Terms of Use TradingView.
- Bukan alat trading otomatis; README melarang pemakaian untuk keputusan/eksekusi algoritmik otomatis.

> Dokumen ini bukan nasihat investasi atau hukum. Cek sendiri Terms of Use TradingView sebelum memakainya.
