# 01 · Arsitektur

## Diagram

```
Claude Code ──stdio (MCP)──► src/server.js ──► src/tools/*.js ──► src/core/*.js ──┐
                                                                                  ├─► src/connection.js
Terminal ────► `tv` CLI ───► src/cli/index.js ─► src/cli/commands/* ─► src/core/*─┘        │
                                                                                            ▼
                                                    Chrome DevTools Protocol (127.0.0.1:9222, WebSocket)
                                                                                            ▼
                                                    TradingView Desktop (Electron) – halaman chart
```

Satu logika (`core`), dua pintu masuk (MCP dan CLI). Karena itu "setiap tool MCP juga perintah `tv`".

## Peta kode

| Path | Peran |
|---|---|
| `src/server.js` | Membuat `McpServer` bernama `tradingview` v2.0.0, memasang blok `instructions` (panduan memilih tool), mendaftarkan 14 kelompok tool, lalu menyambung ke `StdioServerTransport`. Banner peringatan ditulis ke **stderr** supaya tidak merusak protokol stdio. |
| `src/connection.js` | Klien CDP singleton. Mencari target halaman `tradingview.com/chart`, retry 5x dengan backoff eksponensial (500 ms, maks 30 s), `evaluate()` / `evaluateAsync()`. Host/port bisa diganti lewat `TV_CDP_HOST` / `TV_CDP_PORT` (atau `CDP_HOST` / `CDP_PORT`); default `127.0.0.1:9222`. Menyimpan `KNOWN_PATHS`: jalur objek internal seperti `window.TradingViewApi._activeChartWidgetWV.value()`. |
| `src/tools/*.js` | Lapisan MCP tipis: skema parameter `zod` + deskripsi, memanggil `core`, membungkus hasil lewat `jsonResult()` (`{ success, ... }`, `isError` jika gagal). |
| `src/core/*.js` | Logika sebenarnya: `chart`, `data`, `pine`, `replay`, `drawing`, `alerts`, `indicators`, `watchlist`, `pane`, `tab`, `ui`, `capture`, `batch`, `health`, `stream`, `update`. Terbesar: `data.js` (632 baris), `pine.js` (619), `health.js` (401). |
| `src/cli/` | Router CLI kecil; tiap file di `commands/` mendaftarkan perintah. Output selalu JSON agar bisa dipipa ke `jq`. |
| `src/wait.js` | Utilitas menunggu chart selesai dimuat setelah ganti simbol/timeframe. |
| `scripts/` | Peluncur TradingView per OS (`.sh`, `.bat`, `.vbs`) dan `pine_push.js` / `pine_pull.js` untuk bolak-balik file `scripts/current.pine` ↔ editor Pine. |
| `skills/`, `agents/` | Skill dan agent Claude Code (lihat [04](04-skill-dan-agent.md)). |
| `tests/` | `node --test`. Unit test berjalan tanpa TradingView; `e2e.test.js` butuh TradingView hidup. |

Dependensi runtime hanya `@modelcontextprotocol/sdk` dan `chrome-remote-interface` (`zod` dipakai lewat SDK). Dev: `eslint`.

## Alur satu panggilan tool

Contoh `chart_set_symbol { symbol: "AAPL" }`:

1. Claude mengirim `tools/call` lewat stdio ke `server.js`.
2. `tools/chart.js` memvalidasi argumen dengan `zod`, memanggil `core.setSymbol`.
3. `core/chart.js` membangun ekspresi JavaScript. Input pengguna **tidak** ditempel mentah; dipakai
   `safeString()` (`JSON.stringify`) untuk string dan `requireFinite()` untuk angka.
4. `connection.evaluate()` mengirim `Runtime.evaluate` via CDP. Klien dicek hidup dulu (`1` dievaluasi);
   bila mati, sambung ulang.
5. Ekspresi memanggil objek internal TradingView, misalnya `chartApi.setSymbol(...)`.
6. `wait.js` menunggu chart stabil, hasil `{ success: true, ... }` dikembalikan sebagai teks JSON.

## Cara membaca data indikator Pine

Indikator kustom yang menggambar dengan `line.new`/`label.new`/`table.new`/`box.new` tidak muncul di data
OHLCV biasa. Repo ini membaca langsung dari koleksi grafis internal chart:

```
study._graphics._primitivesCollection.dwglines.get('lines').get(false)._primitivesDataById
```

Konsekuensi: indikatornya harus **terlihat** di chart, dan jalur ini adalah detail internal yang bisa berubah.

## Pola desain yang layak ditiru

1. **Ringkas secara default, rinci jika diminta.** `summary: true`, `study_filter`, `verbose: false`,
   label dibatasi 50 per studi, OHLCV maksimal 500 bar, trade maksimal 20 per permintaan.
   Penulis mengukur: alur "analisis chart" turun dari ±80 KB ke 5–10 KB konteks.
2. **Banyak tool granular + panduan pemilihan.** 84 tool tidak membingungkan model karena ada blok
   `instructions` di server dan decision tree di `CLAUDE.md`.
3. **`core` terpisah dari transport.** Mudah dites dan dipakai ulang (`exports["./core"]` di `package.json`).
4. **Respons seragam** `{ success, error? }`, kegagalan ditandai `isError`.
5. **Sanitasi di perbatasan.** Setiap string yang masuk ke JS yang dieksekusi di halaman lewat `JSON.stringify`.
6. **Graceful fallback.** Misal `tv_launch` di Windows MSIX menyalin paket ke `%LOCALAPPDATA%\tradingview-mcp\`
   bila peluncuran dari `WindowsApps` ditolak ("Access is denied").
7. **Entity ID per sesi.** ID dari `chart_get_state` tidak boleh di-cache lintas sesi.

## Streaming

`tv stream quote|bars|values|lines|labels|tables|all` (hanya CLI, **bukan** tool MCP) melakukan poll-and-diff
pada interval tertentu (default 300–2000 ms) dan menulis JSONL ke stdout, hanya saat ada perubahan. Dari
`RESEARCH.md`: untuk agen LLM, streaming cepat membuat penalaran basi sebelum jawaban selesai; arahkan
streaming ke dasbor/skrip lokal, bukan ke konteks agen.

## Temuan kecil dari membaca kode

- `scripts/pine_push.js` memakai `localhost:9222` yang di-hardcode, sedangkan `connection.js` memakai
  `127.0.0.1` dan mendukung env override. Di Windows tertentu `localhost` bisa resolve ke IPv6 `::1`
  sementara Electron hanya listen IPv4; README/komentar kode membahas hal ini.
- README menyebut "78 tools" di satu tempat dan "84" di tempat lain. Hitungan dari kode: **84** panggilan
  `server.tool(...)`.
