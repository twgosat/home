# 05 · Keamanan, risiko, dan kepatuhan

Bagian ini membedakan **apa yang diklaim README** dan **apa yang terlihat di kode** (commit `c05b8f5`).
Tidak ada pengujian dinamis; semua dari membaca source.

## 1. Model ancaman singkat

Setelah TradingView dijalankan dengan `--remote-debugging-port=9222`, **proses apa pun di mesin itu** yang bisa
membuka `127.0.0.1:9222` dapat mengendalikan TradingView Anda, termasuk menjalankan JavaScript di sesi
yang sedang login. CDP tidak punya autentikasi. Server MCP ini hanya salah satu klien dari port tersebut.

| Risiko | Penjelasan | Mitigasi |
|---|---|---|
| Port 9222 terbuka | Jika di-bind ke antarmuka lain atau diteruskan (SSH forward, container, WSL), orang lain bisa mengendalikan akun | Biarkan hanya loopback; jangan diteruskan; matikan TradingView mode debug saat tidak dipakai |
| `ui_evaluate` | Menjalankan JS bebas di halaman TradingView; agen yang kena *prompt injection* (misal dari teks label/judul skrip komunitas) bisa memanggilnya | Tolak/izinkan per panggilan di Claude Code (jangan pre-approve tool ini); tinjau argumen |
| Tool mutasi tanpa konfirmasi | `chart_set_symbol`, `alert_create`/`alert_delete(delete_all)`, `watchlist_remove`, `draw_clear`, `pine_save`, `layout_switch`, `tab_close` langsung dieksekusi | Izinkan manual untuk tool destruktif; ekspor/catat watchlist sebelum eksperimen |
| `tv_launch` default mematikan TradingView | `kill_existing` bernilai true jika tidak diisi (`health.js`: `kill_existing !== false`) | Simpan pekerjaan dulu; panggil dengan `kill_existing: false` bila perlu |
| `tv_update` menarik kode dari `origin/main` | Eksekusi kode terbaru dari repo pihak ketiga tanpa tinjauan; ada guard (hanya git fast-forward, tolak tree kotor / bukan `main` / history menyimpang) dan menjalankan `npm ci` bila lockfile berubah | Pin ke commit yang sudah Anda baca; jangan izinkan `tv_update` otomatis; tinjau diff sebelum `git pull` manual |
| Rantai pasok npm | Dependensi: `@modelcontextprotocol/sdk`, `chrome-remote-interface` (+ transitif) | Pakai `npm ci` dari lockfile, `npm audit`, hindari menjalankan sebagai admin/root |
| Data pasar ke konteks LLM | Isi chart (termasuk skrip pribadi yang dibaca `pine_get_source`) dikirim ke penyedia model | Pertimbangkan sensitivitas skrip berbayar/proprietari |
| Injeksi lewat teks chart | Label/tabel/judul indikator adalah teks pihak ketiga yang masuk ke konteks | Perlakukan sebagai data, bukan instruksi (aturan yang sama dengan `<berita>` di CuanLens) |

## 2. Yang README klaim vs. yang kode lakukan

README: *"Tidak terhubung ke server TradingView"* dan *"semua pemrosesan data terjadi secara lokal"*.
Pada kode, sebagian tool memang memanggil endpoint TradingView (sebagian lewat sesi login aplikasi):

| Tool | Endpoint di kode |
|---|---|
| `alert_create` / `alert_list` / `alert_delete` | `https://pricealerts.tradingview.com/{create_alert,list_alerts,delete_alerts}` (dengan `credentials: 'include'`, sesi aplikasi) |
| `symbol_search` | `https://symbol-search.tradingview.com/symbol_search/v3/` (dari proses Node, header `Origin`/`Referer` ditiru) |
| `pine_check` | `https://pine-facade.tradingview.com/pine-facade/translate_light?user_name=Guest&...` (dari proses Node) |
| `pine_list_scripts`, `pine_open` | `https://pine-facade.tradingview.com/pine-facade/list/?filter=saved` dan `/get/<id>/<ver>` (dengan sesi aplikasi) |

Jadi klaim yang lebih tepat adalah: data chart dibaca dari aplikasi lokal; **beberapa fitur** (alert, cari simbol,
cek Pine, daftar skrip) membuat permintaan jaringan ke domain TradingView. Ini penting untuk penilaian kepatuhan
ToS dan untuk lingkungan dengan firewall ketat. Data tidak dikirim ke pihak lain oleh kode ini; ia mengalir ke
Claude (penyedia model) lewat hasil tool.

## 3. Kepatuhan (ToS & lisensi data)

Penulis menulis sendiri di Disclaimer:

- Proyek **tidak berafiliasi** dengan TradingView Inc. atau Anthropic.
- ToS TradingView membatasi pengumpulan data otomatis, scraping, dan pemakaian non-tampilan; alat ini **mungkin
  bertentangan** dengan itu. Risiko akun (ban/suspend) ditanggung pengguna.
- **Tidak boleh dipakai** untuk: redistribusi/penjualan data pasar, menembus batas langganan, **trading otomatis
  atau pengambilan keputusan algoritmik dari data hasil ekstraksi**, melanggar hak cipta penulis indikator Pine,
  atau menyambung ke infrastruktur TradingView (poin terakhir bertabrakan dengan bagian 2 di atas).
- Data pasar tunduk pada lisensi bursa/penyedia data; jangan disimpan atau didistribusikan.
- Kode berlisensi MIT, tetapi lisensi itu **tidak** memberi hak apa pun atas perangkat lunak, data, atau merek TradingView.
- Menggunakan API internal tak terdokumentasi: bisa rusak di setiap pembaruan TradingView.

Implikasi praktis untuk repo CuanLens: jangan menyimpan data TradingView ke dataset/repo publik, jangan memasukkannya
ke paket yang didistribusikan, dan jangan menjalankan alat ini sebagai bagian layanan yang melayani pihak lain.

## 4. Kualitas rekayasa yang terlihat

Positif
- `safeString()` / `requireFinite()` untuk semua nilai yang masuk ke ekspresi JS; ada `tests/sanitization.test.js`.
- `tv_update` berhati-hati: menolak pada tree kotor, branch bukan `main`, atau history menyimpang.
- Banner peringatan ke stderr; `SECURITY.md` dengan jalur laporan privat.
- Unit test tidak butuh TradingView (`npm run test:unit`); CI menjalankan lint dan unit test.

Catatan
- Escaping tidak seragam di satu helper: `chart`, `data`, `drawing`, `indicators`, `alerts`, `batch`, `pane` memakai
  `safeString()`; `pine`, `ui`, `tab` memakai `JSON.stringify(...)` langsung (hasilnya setara untuk string).
  Yang tidak terlindungi memang disengaja: `ui_evaluate` mengeksekusi ekspresi apa adanya.
- Tes e2e butuh TradingView hidup sehingga tidak dijalankan di CI (CI menjalankan lint, `test:unit` pada Node 20 dan 22,
  dan `npm audit --audit-level=high` yang diset `continue-on-error`, jadi temuan audit tidak menggagalkan build).
- Tidak ada evaluasi formal; temuan di `RESEARCH.md` bersifat observasi.

## 5. Daftar periksa hardening sebelum dipakai

- [ ] Clone, baca diff, **pin commit** (`git checkout <sha>`), jangan pakai `tv_update`.
- [ ] `npm ci` (bukan `npm install`) dan `npm audit`.
- [ ] Jalankan TradingView mode debug hanya saat sesi kerja; pastikan 9222 hanya loopback (`ss -ltnp | grep 9222`).
- [ ] Jangan pre-approve `ui_evaluate`, `alert_delete`, `watchlist_remove`, `tv_launch`, `tv_update` di izin Claude Code.
- [ ] Gunakan akun/layout TradingView terpisah untuk eksperimen jika memungkinkan.
- [ ] Putuskan sejak awal: alat ini untuk **analisis dan pengembangan Pine**, bukan untuk eksekusi order.
- [ ] Baca ulang ToS TradingView; hentikan jika ragu (saran penulis sendiri).
