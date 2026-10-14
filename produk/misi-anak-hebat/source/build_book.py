#!/usr/bin/env python3
"""Generate book.html (cover + fixed A4 pages) for "Misi Anak Hebat"."""
import os, pathlib
import svgart as A
from calc import SLEEP_TABLE, READ_15_30, READ_15_30_H, WATER_GLASS

HERE = pathlib.Path(__file__).resolve().parent
FONTS = pathlib.Path(os.environ.get("FONT_DIR", HERE / "node_modules" / "@fontsource"))
TITLE = "Misi Anak Hebat"
SUBTITLE = "Jurnal Juara 30 Hari · 7 Kebiasaan Anak Indonesia Hebat"
YEAR = 2026
URL = "https://gosatset.xyz/"

H = {
    1: ("Bangun Pagi", "#e07b00", "#fff3e0"),
    2: ("Beribadah", "#0f9d78", "#e4f6ef"),
    3: ("Berolahraga", "#2b7de9", "#e8f1fe"),
    4: ("Makan Sehat & Bergizi", "#e5484d", "#fdeced"),
    5: ("Gemar Belajar", "#7c4dff", "#f0ebff"),
    6: ("Bermasyarakat", "#d6409f", "#fcebf5"),
    7: ("Tidur Cepat", "#4b55d6", "#eceefd"),
}
BRAND = ("#16a34a", "#e9f8ee")
RB = ["#e5484d", "#e07b00", "#16a34a", "#2b7de9", "#7c4dff", "#d6409f", "#0f9d78"]


def font_css():
    out = ""
    for fam, key, weights in (("Fredoka", "fredoka", (400, 500, 600, 700)), ("Nunito", "nunito", (400, 600, 700, 800))):
        for w in weights:
            for sub in ("latin", "latin-ext"):
                f = FONTS / key / "files" / f"{key}-{sub}-{w}-normal.woff2"
                if f.exists():
                    out += f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('{f.as_uri()}') format('woff2');}}\n"
    return out


CSS = """
@page{size:A4;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:'Nunito',sans-serif;color:#2b2d3a;font-size:13px;line-height:1.45}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;break-after:page;background:#fff}
.page:last-child{break-after:auto}
.frame{position:absolute;inset:7mm;border:2.5px dashed var(--c);border-radius:24px;opacity:.5}
.inner{position:absolute;left:14mm;right:14mm;top:13mm;bottom:17mm;display:flex;flex-direction:column}
.foot{position:absolute;left:15mm;right:15mm;bottom:9.6mm;display:flex;justify-content:space-between;align-items:center;font:500 9.5px 'Fredoka';color:#8a8fa3}
.foot a{color:#8a8fa3;text-decoration:none}
.pnum{background:var(--c);color:#fff;border-radius:10px;padding:1px 9px;font-weight:600}
.deco{position:absolute;z-index:0}
.inner>*{position:relative;z-index:1}
h1,h2,h3{font-family:'Fredoka';margin:0;line-height:1.05}
h1{font-weight:700;font-size:40px;letter-spacing:.5px}
h2{font-weight:600;font-size:20px;color:var(--c);margin:12px 0 6px}
h3{font-weight:600;font-size:15px;margin:0 0 4px;color:#2b2d3a}
p{margin:0 0 6px}
.c{color:var(--c)}
.kicker{font:600 12px 'Fredoka';letter-spacing:.12em;text-transform:uppercase;color:var(--c)}
.sub{color:#5b6070;font-size:13.5px;margin:4px 0 0}
.hd{display:flex;align-items:center;gap:14px;margin-bottom:6px}
.hd .ico{flex:none;width:86px;height:86px}
.hd .ico svg{width:100%;height:100%}
.center{text-align:center}
.bulan{display:flex;gap:10px;align-items:flex-end;margin:6px 0 10px}
.tag{background:var(--c);color:#fff;font:600 13px 'Fredoka';padding:4px 14px;border-radius:999px;white-space:nowrap}
.ln{flex:1;border-bottom:2px dashed #c4c9d6;height:22px}
.instr{background:var(--t);border-radius:14px;padding:7px 14px;font:500 13.5px 'Fredoka';color:#3b3f4f;text-align:center;margin-bottom:10px}
.box{border:2px solid var(--c);border-radius:16px;padding:10px 12px;background:#fff}
.tint{background:var(--t);border-radius:16px;padding:10px 14px}
.grid{display:grid;gap:8px}
.num{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;border:2px solid var(--c);color:var(--c);font:600 14px 'Fredoka';flex:none;background:#fff}
.numf{background:var(--c);color:#fff}
.line{border-bottom:1.6px dotted #aab0bf;height:22px}
.lines .line{height:24px}
.chk{display:inline-block;width:16px;height:16px;border:2px solid var(--c);border-radius:5px;vertical-align:-3px;margin-right:6px;background:#fff;flex:none}
.circ{display:inline-flex;width:26px;height:26px;border-radius:50%;border:1.8px solid var(--c);align-items:center;justify-content:center;font:500 12px 'Fredoka';color:var(--c);background:#fff}
table{border-collapse:collapse;width:100%}
th{background:var(--c);color:#fff;font:600 13px 'Fredoka';padding:6px 6px;text-align:center}
td{border:1.4px solid #d5d9e3;padding:4px 6px}
.pill{display:inline-block;background:var(--t);color:var(--c);font:600 12px 'Fredoka';padding:3px 12px;border-radius:999px;margin:2px 4px 2px 0}
.fact{border-left:6px solid var(--c);background:var(--t);border-radius:0 14px 14px 0;padding:9px 14px}
.fact b.c{font-family:'Fredoka';font-weight:600}
.small{font-size:11px;color:#6b7080}
.rb span{display:inline-block}
ul.tick{list-style:none;padding:0;margin:0}
ul.tick li{display:flex;align-items:center;gap:6px;padding:4px 0;font-size:13.5px}
.cards3{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.card{border:2px solid var(--t);border-radius:16px;padding:10px 12px;background:#fff}
.card .ic{font:700 24px 'Fredoka';color:var(--c)}
.cards3 .card h3{font-size:16px}.cards3 .card p{font-size:13px!important}
.flex{display:flex;gap:10px}
.grow{flex:1}
.sig{border-top:2px solid #9aa0b1;padding-top:4px;text-align:center;font:500 12px 'Fredoka';color:#5b6070}
.face5{display:flex;gap:6px}
"""


def rainbow(text, start=0):
    out, k = "", start
    text = text.replace("&amp;", "&")
    for ch in text:
        if ch == "&":
            out += f'<span style="color:{RB[k % len(RB)]}">&amp;</span>'
            k += 1
            continue
        if ch == " ":
            out += " "
            continue
        out += f'<span style="color:{RB[k % len(RB)]}">{ch}</span>'
        k += 1
    return f'<span class="rb">{out}</span>'


class Book:
    def __init__(self):
        self.pages = []      # html strings
        self.marks = []      # (label, page index in body numbering) for bookmarks/TOC

    def add(self, body, c=BRAND, deco="", bookmark=None, frame=True):
        n = len(self.pages)  # cover is page 0 -> body numbering starts at 1
        if bookmark:
            self.marks.append((bookmark, n))
        fr = '<div class="frame"></div>' if frame else ""
        foot = (f'<div class="foot"><a href="{URL}">{TITLE} · GoSatSet.xyz</a><span class="pnum">{n}</span></div>' if n else "")
        self.pages.append(f'<section class="page" style="--c:{c[0]};--t:{c[1]}">{fr}{deco}<div class="inner">{body}</div>{foot}</section>')
        return n


def hc(k):
    return (H[k][1], H[k][2])


def deco(items):
    """items: list of (svg, left/right css, top/bottom css)"""
    return "".join(f'<div class="deco" style="{pos}">{svg}</div>' for svg, pos in items)


def header(k, title, sub, bulan=True, kicker=None):
    kick = kicker or f"Misi {k} · {H[k][0]}"
    b = (f'<div class="hd"><div class="ico">{A.MASCOT[k](86)}</div><div class="grow">'
         f'<div class="kicker">{kick}</div><h1>{rainbow(title, k)}</h1><p class="sub">{sub}</p></div></div>')
    if bulan:
        b += '<div class="bulan"><span class="tag">Bulan</span><span class="ln"></span><span class="tag">Tahun</span><span class="ln" style="flex:.45"></span></div>'
    return b


# ---------------------------------------------------------------- cover
def cover_html():
    badges = "".join(
        f'<div class="bdg"><div class="bi" style="background:{H[k][2]};border-color:{H[k][1]}">{A.MASCOT[k](54)}</div>'
        f'<div class="bl" style="color:{H[k][1]}">{H[k][0].replace(" & Bergizi","")}</div></div>' for k in H)
    title1 = "".join(f'<span style="color:{RB[i % 7]}">{ch}</span>' for i, ch in enumerate("MISI"))
    title2 = "".join(f'<span style="color:{RB[(i+4) % 7]}">{ch}</span>' if ch != " " else " " for i, ch in enumerate("ANAK HEBAT"))
    hills = ('<svg class="hills" viewBox="0 0 794 330" preserveAspectRatio="none">'
             '<path d="M0 120 Q140 40 300 110 T600 90 T794 70 V330 H0 Z" fill="#9fdc7c"/>'
             '<path d="M0 190 Q200 110 420 180 T794 150 V330 H0 Z" fill="#72c457"/>'
             '<path d="M0 260 Q260 200 520 250 T794 240 V330 H0 Z" fill="#4fae3f"/></svg>')
    flowers = "".join(f'<div class="fl" style="left:{x}px;bottom:{y}px">{A.star(s, fill=c, stroke="#fff", with_face=False)}</div>'
                      for x, y, s, c in [(40, 70, 22, "#ff9eb0"), (250, 90, 16, "#fff"), (560, 60, 20, "#ff9eb0"), (650, 110, 16, "#ffd23f"), (360, 52, 18, "#ffd23f"), (20, 150, 18, "#fff")])
    return f"""
<div class="cv">
  <div class="sky"></div>
  <div class="d" style="left:18px;top:14px">{A.sun(150)}</div>
  <div class="d" style="right:-10px;top:30px">{A.rainbow(250)}</div>
  <div class="d" style="left:200px;top:36px;opacity:.95">{A.cloud(120)}</div>
  <div class="d" style="right:150px;top:112px">{A.cloud(100)}</div>
  <div class="d" style="left:-20px;top:300px">{A.cloud(110)}</div>
  <div class="d" style="right:-24px;top:420px">{A.cloud(110)}</div>
  <div class="d" style="left:46px;top:500px">{A.sparkle(26,'#fff')}</div>
  <div class="d" style="right:52px;top:360px">{A.sparkle(22,'#ffd23f')}</div>
  <div class="card">
    <div class="kpill">JURNAL JUARA 30 HARI</div>
    <div class="t1">{title1}</div>
    <div class="t2">{title2}</div>
    <div class="st">7 Kebiasaan Anak Indonesia Hebat</div>
    <div class="badges">{badges}</div>
    <div class="pills"><span>✔ Tracker 31 hari</span><span>✔ Aktivitas &amp; bingo seru</span><span>✔ Panduan Ayah-Bunda</span></div>
    <div class="nm"><b>Nama</b><i></i></div>
    <div class="nm"><b>Kelas</b><i></i></div>
  </div>
  {hills}
  <div class="d" style="left:70px;bottom:62px">{A.kid(185, girl=False, shirt='#2b7de9')}</div>
  <div class="d" style="right:70px;bottom:62px">{A.kid(185, girl=True, shirt='#d6409f')}</div>
  <div class="d" style="left:300px;bottom:70px">{A.apple(86)}</div>
  <div class="d" style="left:400px;bottom:64px">{A.book(84)}</div>
  {flowers}
  <div class="cf"><span>Edisi {YEAR} · Siap cetak A4</span><span>GoSatSet.xyz</span></div>
</div>"""


COVER_CSS = """
.cv{position:relative;width:210mm;height:297mm;overflow:hidden;font-family:'Fredoka'}
.cv .sky{position:absolute;inset:0;background:linear-gradient(180deg,#8fd3ff 0%,#c9ecff 45%,#eaf9ff 70%)}
.cv .d{position:absolute}
.cv .card{position:absolute;left:62px;right:62px;top:150px;background:rgba(255,255,255,.96);border-radius:36px;padding:26px 30px 24px;
  text-align:center;box-shadow:0 14px 0 rgba(43,125,233,.18);border:4px dashed #9fdc7c}
.cv .kpill{display:inline-block;background:#16a34a;color:#fff;font-weight:600;font-size:17px;letter-spacing:.16em;padding:6px 20px;border-radius:999px}
.cv .t1,.cv .t2{font-weight:700;line-height:.95;letter-spacing:2px;-webkit-text-stroke:2px #fff;paint-order:stroke fill;text-shadow:0 6px 0 rgba(0,0,0,.10)}
.cv .t1{font-size:132px;margin-top:6px}
.cv .t2{font-size:92px}
.cv .st{display:inline-block;margin-top:12px;background:#fff4c2;color:#7a4b00;font-weight:600;font-size:24px;padding:6px 20px;border-radius:14px}
.cv .badges{display:flex;justify-content:space-between;margin:18px 0 6px}
.cv .bdg{width:82px;text-align:center}
.cv .bi{width:70px;height:70px;border-radius:50%;border:3px solid;margin:0 auto;display:flex;align-items:center;justify-content:center}
.cv .bl{font-weight:600;font-size:11.5px;margin-top:4px;line-height:1.1}
.cv .pills{margin:10px 0 12px}
.cv .pills span{display:inline-block;background:#e9f8ee;color:#127a3a;font-weight:600;font-size:14px;padding:5px 12px;border-radius:999px;margin:2px}
.cv .nm{display:flex;align-items:flex-end;gap:12px;margin:8px 30px 0;font-size:20px;color:#127a3a}
.cv .nm b{width:70px;text-align:left;font-weight:600}
.cv .nm i{flex:1;border-bottom:3px dashed #9fdc7c;height:24px}
.cv .hills{position:absolute;left:0;bottom:0;width:100%;height:330px}
.cv .fl{position:absolute}
.cv .cf{position:absolute;left:30px;right:30px;bottom:18px;display:flex;justify-content:space-between;color:#fff;font-weight:600;font-size:16px;text-shadow:0 1px 3px rgba(0,0,0,.35)}
"""


# ---------------------------------------------------------------- pages
def p_identitas(b):
    c = BRAND
    fields = "".join(f'<div class="flex" style="align-items:flex-end;margin-bottom:14px;font-size:15px"><b style="width:118px;font-family:Fredoka;font-weight:600">{f}</b><span class="ln"></span></div>'
                     for f in ("Nama lengkap", "Panggilan", "Kelas", "Sekolah", "Umur", "Tanggal lahir"))
    about = "".join(f'<div class="card" style="border-color:{H[k][2]}"><h3 style="color:{H[k][1]}">{t}</h3><div class="line"></div><div class="line"></div><div class="line"></div></div>'
                    for k, t in ((1, "Cita-citaku"), (3, "Hobiku"), (4, "Makanan favoritku"), (6, "Sahabatku")))
    body = f"""
<div class="center"><div class="kicker">Halo, Anak Hebat!</div><h1 style="font-size:46px">{rainbow("Jurnal Ini Milik…")}</h1>
<p class="sub">Isi halaman ini dulu, ya. Kamu adalah tokoh utama misi ini!</p></div>
<div class="flex" style="margin-top:18px;gap:18px">
  <div style="width:210px;height:260px;border:3px dashed {c[0]};border-radius:22px;display:flex;flex-direction:column;align-items:center;justify-content:center;background:{c[1]}">
    {A.star(70)}<div style="font:600 15px Fredoka;color:{c[0]};margin-top:8px;text-align:center">Tempel fotomu<br>atau gambar dirimu<br>di sini</div></div>
  <div class="grow" style="padding-top:8px">{fields}</div>
</div>
<h2>Tentang Aku</h2>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:10px">{about}</div>
<h2>Kebiasaan yang paling ingin aku kuasai bulan ini</h2>
<div class="box"><div class="line"></div><div class="line"></div><div class="line"></div></div>
<div class="flex" style="margin-top:auto;align-items:flex-end;gap:30px">
  <div class="grow small">Simpan jurnal ini di tempat yang mudah dilihat, misalnya di dekat meja belajar, supaya kamu ingat mengisinya setiap malam.</div>
  <div style="width:230px"><div style="height:56px"></div><div class="sig">Tanda tangan Anak Hebat</div></div>
</div>"""
    b.add(body, c, deco([(A.sun(90), "right:30px;top:24px"), (A.sparkle(22), "left:40px;top:60px")]), bookmark="Jurnal Ini Milik…")


def p_toc(b, entries):
    c = BRAND
    rows = ""
    for grp, items in entries:
        rows += f'<div style="font:600 13px Fredoka;letter-spacing:.1em;color:#8a8fa3;text-transform:uppercase;margin:10px 0 4px">{grp}</div>'
        for label, pg, col in items:
            rows += (f'<div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1.5px dotted #dfe3ea">'
                     f'<span style="width:12px;height:12px;border-radius:50%;background:{col};flex:none"></span>'
                     f'<span class="grow" style="font-size:15px">{label}</span><b style="font-family:Fredoka;font-size:15px;color:{col}">{pg}</b></div>')
    steps = [("1", "Persiapan", "Isi identitas, kontrak, peta awal &amp; target", "#16a34a"), ("2", "Misi Harian", "Isi tracker 7 misi setiap malam", "#2b7de9"),
             ("3", "Refleksi", "Setiap akhir pekan + paraf", "#7c4dff"), ("4", "Perayaan", "Peta akhir, bintang &amp; sertifikat", "#e07b00")]
    flow = "".join(f'<div style="flex:1;border:2.5px solid {col};border-radius:16px;padding:10px;text-align:center"><div style="font:700 26px Fredoka;color:{col}">{n}</div>'
                   f'<div style="font:600 15px Fredoka;color:{col}">{t}</div><div class="small">{d}</div></div>' + ('<div style="align-self:center;font:700 22px Fredoka;color:#c4c9d6">›</div>' if n != "4" else "")
                   for n, t, d, col in steps)
    legend = "".join(f'<div style="text-align:center;width:84px"><div style="width:52px;height:52px;margin:0 auto;border-radius:50%;background:{H[k][2]};border:2.5px solid {H[k][1]};display:flex;align-items:center;justify-content:center">{A.MASCOT[k](38)}</div>'
                     f'<div style="font:600 11px Fredoka;color:{H[k][1]};margin-top:3px;line-height:1.1">{H[k][0].replace(" & Bergizi","")}</div></div>' for k in H)
    body = f"""
<div class="center"><div class="kicker">Peta Petualangan</div><h1>{rainbow("Daftar Isi")}</h1></div>
<div class="flex" style="justify-content:space-between;margin:14px 0 6px">{legend}</div>
<p class="small center">Setiap misi punya warna sendiri. Cari warnanya di pojok bawah halaman!</p>
<div style="columns:2;column-gap:26px;margin-top:4px">{rows}</div>
<h2 style="margin-top:auto">Alur Misi 30 Hari</h2>
<div class="flex" style="align-items:stretch;gap:6px">{flow}</div>"""
    b.add(body, c, bookmark="Daftar Isi")


def p_guide1(b):
    c = BRAND
    steps = [("Mulai bersama", "Isi identitas, Kontrak Janji, dan Peta Awal bersama anak di hari pertama."),
             ("Tentukan target", "Sepakati target kecil dan hadiah di halaman Target &amp; Hadiahku."),
             ("5 menit tiap malam", "Sebelum tidur, isi tracker hari itu bersama anak. Biarkan anak yang menulis atau mewarnai."),
             ("Refleksi akhir pekan", "Isi Refleksi Mingguan, beri paraf, dan tempel/warnai bintang yang didapat."),
             ("Rayakan di akhir bulan", "Isi Peta Akhir, hitung bintang, lalu berikan Sertifikat Anak Hebat.")]
    st = "".join(f'<div class="card" style="border-color:{RB[i]}33"><div class="flex" style="align-items:center;gap:8px"><span class="num numf" style="background:{RB[i]};border-color:{RB[i]}">{i+1}</span><h3>{t}</h3></div><p style="margin:6px 0 0;font-size:12.5px">{d}</p></div>'
                 for i, (t, d) in enumerate(steps))
    tips = [("Puji usahanya, secara spesifik.", "“Kamu bangun sendiri tanpa dibangunkan, hebat!” lebih bermakna daripada “pintar”."),
            ("Mulai dari yang paling mudah.", "Fokus pada 1–2 kebiasaan dulu, lalu tambah bertahap."),
            ("Jadilah teladan.", "Anak meniru. Ikut bangun pagi, berolahraga, dan menyimpan gawai bersama."),
            ("Kolom kosong bukan kegagalan.", "Tidak perlu menghukum. Besok adalah kesempatan baru."),
            ("Hadiah tidak harus barang.", "Waktu bermain bersama, memilih menu makan malam, atau piknik kecil juga istimewa.")]
    tp = "".join(f'<li style="align-items:flex-start"><span style="color:{c[0]};font:700 16px Fredoka">✔</span><span><b>{t}</b> {d}</span></li>' for t, d in tips)
    body = f"""
<div class="kicker">Untuk Ayah, Bunda &amp; Guru</div><h1 style="font-size:34px">{rainbow("Selamat Datang di Misi Anak Hebat")}</h1>
<div class="fact" style="margin-top:10px"><b class="c">Tentang Gerakan 7 Kebiasaan Anak Indonesia Hebat.</b>
Pada 27 Desember 2024, Kementerian Pendidikan Dasar dan Menengah (Kemendikdasmen) meluncurkan gerakan pembiasaan karakter dengan tujuh kebiasaan:
<b>bangun pagi, beribadah, berolahraga, makan sehat dan bergizi, gemar belajar, bermasyarakat, dan tidur cepat</b> [1]. Gerakan ini dijalankan bersama oleh sekolah, keluarga, masyarakat, dan media, yang disebut Catur Pusat Pendidikan [2].
Rumah adalah tempat terbaik untuk melatihnya setiap hari, dan jurnal ini dibuat untuk membantu proses itu.</div>
<h2>Cara Memakai Jurnal (5 langkah)</h2>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:9px">{st}
<div class="tint" style="display:flex;align-items:center;gap:10px">{A.trophy(54)}<div style="font-size:12.5px"><b>Untuk TK–SD (±5–12 tahun).</b> Anak TK cukup mewarnai; anak SD bisa menulis sendiri.</div></div></div>
<h2>Tips Mendampingi</h2>
<ul class="tick">{tp}</ul>
<h2>Cara Mencetak</h2>
<p style="font-size:12.5px">Cetak di kertas A4. Halaman putih dirancang <b>hemat tinta</b>. Halaman tracker dan refleksi boleh dicetak ulang setiap bulan untuk dipakai lagi. Bisa juga diisi langsung di tablet dengan aplikasi anotasi PDF.</p>
<p class="small" style="margin-top:auto">Jurnal ini adalah produk independen untuk mendukung pembiasaan di rumah dan sekolah, bukan terbitan resmi Kemendikdasmen.</p>"""
    b.add(body, c, deco([(A.sparkle(24, "#ffd23f"), "right:34px;top:34px")]), bookmark="Panduan Ayah, Bunda & Guru")


def p_guide2(b):
    c = BRAND
    sleep_rows = "".join(f'<tr><td class="center"><b>{w}</b></td><td class="center">{b9}</td><td class="center">{b10}</td></tr>' for w, b9, b10 in SLEEP_TABLE)
    refs = [
        "Guru Inovatif, “Kemendikdasmen Luncurkan Program Gerakan 7 Kebiasaan Anak Indonesia Hebat”, 30 Des 2024 — guruinovatif.id; NU Online, Des 2024 — nu.or.id",
        "Good News From Indonesia, “7 Kebiasaan Anak Indonesia Hebat (KAIH) Wujudkan Pendidikan Karakter”, 14 Agu 2025 — goodnewsfromindonesia.id",
        "Paruthi S. dkk. (AASM), Recommended Amount of Sleep for Pediatric Populations, J Clin Sleep Med 2016;12(6):785–786 — didukung American Academy of Pediatrics",
        "WHO, Guidelines on Physical Activity and Sedentary Behaviour, 2020 — who.int; ringkasan di ncbi.nlm.nih.gov/books/NBK566046",
        "Kementerian Kesehatan RI, Pedoman Gizi Seimbang “Isi Piringku” — kemkes.go.id",
        "Permenkes No. 28 Tahun 2019 tentang Angka Kecukupan Gizi (AKG) yang Dianjurkan untuk Masyarakat Indonesia",
    ]
    rf = "".join(f'<li style="margin-bottom:2px">{r}</li>' for r in refs)
    body = f"""
<div class="kicker">Untuk Ayah, Bunda &amp; Guru</div><h1 style="font-size:34px">{rainbow("Angka Rujukan Ringkas")}</h1>
<p class="sub">Pedoman umum dari lembaga resmi. Kebutuhan tiap anak bisa berbeda; diskusikan dengan dokter atau tenaga gizi bila ragu.</p>
<table style="margin-top:10px;font-size:12.5px">
<tr><th style="width:110px">Kebiasaan</th><th>Pedoman</th><th style="width:150px">Sumber</th></tr>
<tr><td><b style="color:{H[7][1]}">Tidur cepat</b></td><td>Usia 6–12 tahun: <b>9–12 jam</b> per 24 jam secara teratur. Usia 3–5 tahun: 10–13 jam (termasuk tidur siang). Tidur cukup berkaitan dengan perhatian, perilaku, belajar, memori, dan pengelolaan emosi yang lebih baik.</td><td>AASM 2016 [3]</td></tr>
<tr><td><b style="color:{H[3][1]}">Berolahraga</b></td><td>Usia 5–17 tahun: rata-rata <b>60 menit per hari</b> aktivitas fisik intensitas sedang–berat; aktivitas berat serta penguatan otot dan tulang setidaknya 3 hari per minggu. Batasi waktu duduk lama, terutama layar untuk hiburan.</td><td>WHO 2020 [4]</td></tr>
<tr><td><b style="color:{H[4][1]}">Makan sehat</b></td><td>Isi Piringku: <b>½ piring sayur dan buah</b> (sayur lebih banyak), <b>½ piring makanan pokok dan lauk pauk</b> (makanan pokok lebih banyak). Cuci tangan pakai sabun sebelum dan sesudah makan.</td><td>Kemenkes [5]</td></tr>
<tr><td><b style="color:#2b8fd6">Minum air</b></td><td>AKG 2019 mencantumkan kebutuhan air <b>±1.650 mL per hari</b> untuk anak 7–9 tahun (setara ±{WATER_GLASS:.0f} gelas kecil 200 mL).</td><td>Permenkes 28/2019 [6]</td></tr>
</table>
<h2>Hitung Mundur Jam Tidur</h2>
<div class="flex" style="gap:16px;align-items:flex-start">
<table style="width:54%;font-size:13px"><tr><th>Jam bangun</th><th>Tidur 9 jam:<br>naik ranjang</th><th>Tidur 10 jam:<br>naik ranjang</th></tr>{sleep_rows}</table>
<div class="tint grow" style="font-size:12.5px"><b>Cara pakai:</b> tentukan jam bangun dulu, lalu hitung mundur. Contoh: bangun 05.30 dan butuh 9 jam tidur, berarti sudah tidur pukul 20.30. Beri waktu tambahan untuk rutinitas malam dan waktu sampai terlelap.</div></div>
<h2>Referensi</h2>
<ol style="margin:0;padding-left:20px;font-size:10.5px;color:#4b5060">{rf}</ol>
<h2>Siapkan Rumah Ramah Kebiasaan</h2>
<div class="box"><ul class="tick" style="columns:2;font-size:12.5px">
<li><span class="chk"></span>Jam weker untuk anak</li><li><span class="chk"></span>Botol minum milik sendiri</li>
<li><span class="chk"></span>Sudut baca yang tenang</li><li><span class="chk"></span>Tempat mengisi daya gawai di luar kamar</li>
<li><span class="chk"></span>Jadwal harian ditempel di dinding</li><li><span class="chk"></span>Krayon/stiker bintang untuk jurnal</li></ul></div>
<div class="fact" style="margin-top:auto;font-size:11.5px"><b class="c">Catatan penting.</b> Jurnal ini adalah alat bantu pembiasaan dan edukasi, bukan pengganti saran dokter, psikolog, atau ahli gizi. Angka di atas adalah pedoman umum per Oktober {YEAR}; selalu cek pembaruan dari sumber resmi.</div>"""
    b.add(body, c, bookmark="Angka Rujukan & Referensi")


def p_kontrak(b):
    c = ("#e07b00", "#fff3e0")
    promises = ["bangun pagi tanpa banyak menunda", "beribadah dan berdoa dengan sungguh-sungguh", "bergerak aktif dan berolahraga",
                "makan sayur, buah, dan minum air putih", "belajar dan membaca setiap hari", "membantu dan bersikap baik kepada orang lain",
                "tidur cepat agar badan segar esok hari"]
    pr = "".join(f'<li style="padding:11px 0;border-bottom:1.5px dotted #f1d9b5"><span class="num" style="border-color:{H[i+1][1]};color:{H[i+1][1]};width:30px;height:30px">{i+1}</span><span style="font-size:17px">Aku akan <b>{p}</b>.</span></li>' for i, p in enumerate(promises))
    body = f"""
<div class="center">{A.medal(90)}<div class="kicker" style="margin-top:4px">Langkah pertama</div><h1 style="font-size:44px">{rainbow("Kontrak Janji Anak Hebat")}</h1></div>
<div class="box" style="margin-top:14px;padding:20px 24px;border-width:3px;border-style:dashed;font-size:15px">
<div class="flex" style="align-items:flex-end;font:500 17px Fredoka"><span>Aku,</span><span class="ln"></span><span>,</span></div>
<p style="font-size:15px;margin-top:10px">berjanji menjalankan <b>Misi 30 Hari</b> dengan semangat. Selama misi ini:</p>
<ul class="tick">{pr}</ul>
<div class="flex" style="justify-content:center;gap:18px;margin:12px 0 4px">{''.join(A.MASCOT[k](48) for k in H)}</div>
<p style="font-size:14px;margin-top:10px">Kalau ada hari yang terlewat, aku <b>tidak menyerah</b>. Aku akan mencoba lagi besok!</p>
<div class="flex" style="align-items:flex-end;margin-top:6px;font:500 14px Fredoka"><span>Mulai tanggal</span><span class="ln"></span><span>sampai</span><span class="ln"></span></div>
</div>
<div class="grid" style="grid-template-columns:repeat(3,1fr);gap:22px;margin-top:auto">
<div><div style="height:90px"></div><div class="sig">Anak Hebat</div></div>
<div><div style="height:70px"></div><div class="sig">Ayah / Bunda</div></div>
<div><div style="height:70px"></div><div class="sig">Guru / Wali Kelas</div></div></div>"""
    b.add(body, c, deco([(A.star(60), "left:36px;top:40px"), (A.star(46), "right:40px;top:60px"), (A.sparkle(22), "right:90px;top:30px")]), bookmark="Kontrak Janji Anak Hebat")


def p_poster(b):
    c = BRAND
    desc = {
        1: "Bangun saat matahari terbit membuat pagi lebih tenang: ada waktu bersiap, sarapan, dan tidak terburu-buru.",
        2: "Berdoa dan beribadah sesuai agama mengajarkan kita bersyukur, jujur, dan sabar.",
        3: "Bergerak setiap hari membuat tubuh kuat, tidur nyenyak, dan hati gembira.",
        4: "Isi piring dengan sayur, buah, nasi, dan lauk. Jangan lupa air putih!",
        5: "Membaca dan bertanya setiap hari membuat otak terus tumbuh dan penasaran.",
        6: "Menyapa, menolong, dan berbagi membuat kita disayang teman dan tetangga.",
        7: "Tidur lebih awal memberi waktu tubuh dan otak beristirahat, tumbuh, dan mengingat pelajaran.",
    }
    rows = "".join(f'<div style="display:flex;align-items:center;gap:14px;background:{H[k][2]};border-radius:18px;padding:8px 14px">'
                   f'<div style="font:700 34px Fredoka;color:{H[k][1]};width:30px;text-align:center">{k}</div>'
                   f'<div style="width:70px;height:70px;flex:none">{A.MASCOT[k](70)}</div>'
                   f'<div class="grow"><div style="font:700 21px Fredoka;color:{H[k][1]}">{H[k][0]}</div><div style="font-size:13.5px">{desc[k]}</div></div></div>' for k in H)
    body = f"""<div class="center"><div class="kicker">Poster untuk ditempel</div><h1 style="font-size:44px">{rainbow("7 Kebiasaan Anak Hebat")}</h1></div>
<div style="display:flex;flex-direction:column;gap:9px;margin-top:14px;flex:1;justify-content:space-between">{rows}</div>"""
    b.add(body, c, deco([(A.sun(70), "left:26px;top:22px"), (A.rainbow(110), "right:24px;top:30px")]), bookmark="Poster 7 Kebiasaan")


def rating_page(b, final=False):
    c = ("#7c4dff", "#f0ebff") if not final else ("#16a34a", "#e9f8ee")
    qs = {1: "Aku bangun pagi tanpa dibangunkan berkali-kali.", 2: "Aku beribadah dan berdoa dengan rajin.",
          3: "Aku bergerak aktif / berolahraga setiap hari.", 4: "Aku makan sayur, buah, dan minum air putih.",
          5: "Aku belajar dan membaca setiap hari.", 6: "Aku suka menolong dan menyapa orang lain.",
          7: "Aku tidur tepat waktu tanpa main gawai."}
    stars = "".join(A.star_outline(34) for _ in range(5))
    rows = "".join(f'<div style="display:flex;align-items:center;gap:12px;padding:8px 10px;border-bottom:1.5px dotted #dfe3ea">'
                   f'<div style="width:54px;height:54px;flex:none">{A.MASCOT[k](54)}</div>'
                   f'<div class="grow"><div style="font:600 17px Fredoka;color:{H[k][1]}">{H[k][0]}</div><div style="font-size:14px">{qs[k]}</div></div>'
                   f'<div class="face5">{stars}</div></div>' for k in H)
    if not final:
        title, kick, sub = "Peta Awalku", "Sebelum misi dimulai", "Warnai bintang sesuai dirimu SEKARANG. 1 bintang = jarang, 5 bintang = selalu. Jujur saja, tidak ada yang salah!"
        extra = """<h2>Kebiasaan yang paling mudah untukku</h2><div class="box"><div class="line"></div></div>
<h2>Kebiasaan yang paling ingin kuperbaiki</h2><div class="box"><div class="line"></div><div class="line"></div></div>"""
        bm = "Peta Awalku"
    else:
        title, kick, sub = "Peta Akhirku", "Setelah 30 hari", "Warnai lagi bintangmu, lalu bandingkan dengan Peta Awal. Lihat, kamu sudah tumbuh!"
        extra = """<div class="grid" style="grid-template-columns:1fr 1fr;gap:10px;margin-top:10px">
<div class="box"><h3 class="c">Kebiasaan yang paling naik bintangnya</h3><div class="line"></div><div class="line"></div></div>
<div class="box"><h3 class="c">Aku paling bangga karena…</h3><div class="line"></div><div class="line"></div></div></div>
<div class="tint" style="margin-top:10px"><h3 class="c">Pesan dari Ayah / Bunda</h3><div class="line"></div><div class="line"></div></div>"""
        bm = "Peta Akhirku"
    body = f"""<div class="center"><div class="kicker">{kick}</div><h1 style="font-size:44px">{rainbow(title)}</h1><p class="sub">{sub}</p></div>
<div style="margin-top:10px;flex:1;display:flex;flex-direction:column;justify-content:space-around">{rows}</div>{extra}"""
    b.add(body, c, deco([(A.star(54), "right:36px;top:32px")]), bookmark=bm)


def p_target(b):
    c = ("#e07b00", "#fff3e0")
    rows = "".join(f'<tr><td style="width:150px"><b style="color:{H[k][1]};font-family:Fredoka">{k}. {H[k][0].replace(" & Bergizi","")}</b></td><td style="height:50px"><span class="small">{ex}</span></td></tr>'
                   for k, ex in ((1, "contoh: bangun pukul 05.30"), (2, "contoh: berdoa sebelum makan &amp; tidur"), (3, "contoh: main bola 30 menit"),
                                 (4, "contoh: habiskan sayur saat makan siang"), (5, "contoh: membaca 15 menit"), (6, "contoh: membantu ibu menyiram tanaman"),
                                 (7, "contoh: tidur sebelum pukul 20.30")))
    ladder = "".join(f'<div style="flex:1;text-align:center;border:2.5px solid {col};border-radius:18px;padding:10px 6px;background:#fff;margin-top:{mt}px">'
                     f'<div style="font:700 26px Fredoka;color:{col}">{d}</div><div style="font:600 12px Fredoka;color:{col}">BINTANG</div>'
                     f'<div style="margin:6px auto 0;width:40px">{A.star_outline(40, color=col)}</div><div class="line" style="margin-top:8px"></div><div class="line"></div><div class="line"></div><div class="small">hadiahku</div></div>'
                     for d, col, mt in ((7, "#2b7de9", 120), (14, "#0f9d78", 80), (21, "#7c4dff", 40), (30, "#e5484d", 0)))
    body = f"""<div class="center"><div class="kicker">Sepakati bersama Ayah / Bunda</div><h1 style="font-size:44px">{rainbow("Target &amp; Hadiahku")}</h1></div>
<h2>Target kecilku untuk tiap misi</h2>
<table style="font-size:13px"><tr><th>Misi</th><th>Targetku bulan ini</th></tr>{rows}</table>
<h2>Tangga Hadiah</h2>
<p style="font-size:13px">Setiap hari semua misi selesai (atau sesuai kesepakatan), kamu dapat 1 bintang di halaman <b>Koleksi Bintang</b>. Tulis hadiah yang disepakati di setiap anak tangga.</p>
<div class="flex" style="align-items:flex-start;gap:12px">{ladder}</div>
<div class="tint" style="margin-top:auto;font-size:12.5px"><b class="c">Ide hadiah tanpa belanja:</b> memilih menu makan malam, main bersama Ayah/Bunda 30 menit, piknik di taman, membaca cerita tambahan, menginap di rumah kakek-nenek, atau memilih film keluarga.</div>"""
    b.add(body, c, deco([(A.trophy(64), "right:34px;top:30px")]), bookmark="Target & Hadiahku")


def p_jadwal(b):
    c = ("#2b7de9", "#e8f1fe")
    times = [f"{h:02d}.00" for h in range(5, 22)]
    rows = "".join(f'<div style="display:flex;align-items:center;gap:10px;height:100%;border-bottom:1.5px dotted #d5dbe8">'
                   f'<span style="width:62px;font:600 15px Fredoka;color:{c[0]}">{t}</span><span class="grow"></span>'
                   f'<span style="display:flex;gap:4px">' + "".join(f'<span style="width:13px;height:13px;border-radius:50%;border:2px solid {H[k][1]}"></span>' for k in H) + '</span></div>'
                   for t in times)
    legend = " ".join(f'<span class="pill" style="background:{H[k][2]};color:{H[k][1]}">● {H[k][0].replace(" & Bergizi","")}</span>' for k in H)
    body = f"""{header(3, "Jadwal Harianku", "Tulis kegiatanmu dari bangun sampai tidur. Warnai bulatan misi yang kamu lakukan di jam itu.", bulan=False, kicker="Rencana hari sekolah")}
<div style="margin:2px 0 6px">{legend}</div>
<div class="box" style="flex:1;display:grid;grid-template-rows:repeat({len(times)},1fr);padding:4px 14px">{rows}</div>
<p class="small" style="margin-top:6px">Tips: tempel jadwal ini di dinding kamar. Jadwal libur boleh dibuat di halaman cetak ulang.</p>"""
    b.add(body, c, bookmark="Jadwal Harianku")


def intro(b, k, tagline, why, missions, fact, tip, draw="Gambar dirimu saat menjalankan misi ini!"):
    c = hc(k)
    draw = {1: "Gambar suasana pagimu: apa yang kamu lihat saat bangun?",
            2: "Gambar atau tulis hal-hal yang kamu syukuri hari ini",
            3: "Gambar olahraga atau permainan favoritmu!",
            4: "Gambar sayur dan buah kesukaanmu, lalu beri warna",
            5: "Gambar atau tulis cita-citamu dan ilmu yang kamu butuhkan",
            6: "Gambar dirimu sedang menolong orang lain",
            7: "Gambar kamar tidurmu yang nyaman dan rapi"}.get(k, draw)
    whys = "".join(f'<div class="card" style="border-color:{c[1]}"><div class="ic">{i+1}</div><h3>{t}</h3><p style="font-size:12.5px;margin:0">{d}</p></div>' for i, (t, d) in enumerate(why))
    ms = "".join(f'<li><span class="chk"></span>{m}</li>' for m in missions)
    body = f"""
<div style="background:{c[1]};border-radius:26px;padding:18px 22px;display:flex;align-items:center;gap:18px">
  <div style="width:150px;height:150px;flex:none">{A.MASCOT[k](150)}</div>
  <div><div class="kicker">Misi {k} dari 7</div><h1 style="font-size:{50 if len(H[k][0]) < 14 else 38}px">{rainbow(H[k][0], k)}</h1><p style="font:500 16px Fredoka;margin:6px 0 0;color:#3b3f4f">{tagline}</p></div>
</div>
<h2>Kenapa ini penting?</h2>
<div class="cards3">{whys}</div>
<h2>Misi kecilku hari ini</h2>
<div class="box"><ul class="tick" style="columns:2">{ms}</ul></div>
<h2>Tahukah kamu?</h2>
<div class="fact" style="font-size:13.5px">{fact}</div>
<h2>{draw}</h2>
<div style="flex:1;border:2.5px dashed {c[0]}88;border-radius:20px;position:relative;min-height:120px">
<div style="position:absolute;right:12px;bottom:10px;opacity:.9">{A.sparkle(26)}</div></div>
<div class="tint" style="margin-top:10px;font-size:12.5px"><b class="c">Untuk Ayah / Bunda:</b> {tip}</div>"""
    b.add(body, c, deco([(A.sparkle(26), "right:40px;top:36px")]), bookmark=f"Misi {k}: {H[k][0]}")


def p_time_log(b, k, title, sub, instr, label):
    c = hc(k)
    cols = [range(1, 12), range(12, 22), range(22, 32)]
    def row(d):
        return (f'<div style="display:flex;align-items:center;gap:6px">'
                f'<span class="num" style="width:32px;height:32px">{d}</span>'
                f'<span style="flex:1;height:34px;border:2px dashed {c[0]}88;border-radius:10px 4px 4px 10px;clip-path:polygon(0 0,88% 0,100% 50%,88% 100%,0 100%);'
                f'background:{c[1]};display:flex;align-items:center;padding-left:8px;font:500 12px Fredoka;color:{c[0]}99">..... : .....</span>'
                f'<span style="width:28px;height:28px;flex:none">{A.star_outline(28, color=c[0])}</span></div>')
    colhtml = "".join(f'<div style="display:grid;grid-template-rows:repeat(11,1fr);gap:4px">{"".join(row(d) for d in rg)}</div>' for rg in cols)
    body = f"""{header(k, title, sub)}<div class="instr">{instr}</div>
<div style="flex:1;display:grid;grid-template-columns:repeat(3,1fr);gap:14px">{colhtml}</div>
<div class="flex" style="margin-top:8px;align-items:center;font-size:12.5px"><span style="width:22px">{A.star_outline(22, color=c[0])}</span><span>{label}</span></div>"""
    b.add(body, c)


def p_salat(b):
    k = 2
    c = hc(k)
    names = [("Subuh", "#f59e0b"), ("Zuhur", "#e07b00"), ("Asar", "#d97706"), ("Magrib", "#d6409f"), ("Isya", "#4b55d6")]
    def block(n, col):
        circles = "".join(f'<span class="circ" style="border-color:{c[0]};width:34px;height:34px;font-size:14px">{d}</span>' for d in range(1, 32))
        return (f'<div style="display:flex;gap:10px;align-items:center;border:2px solid {c[1]};border-radius:18px;padding:8px 10px;background:#fff">'
                f'<div style="width:96px;text-align:center"><div style="font:700 21px Fredoka;color:{col}">{n}</div>'
                f'<div style="margin:4px auto 0;width:56px">{A.hands(56)}</div></div>'
                f'<div style="display:grid;grid-template-columns:repeat(11,1fr);gap:7px 4px;flex:1;justify-items:center">{circles}</div></div>')
    body = f"""{header(k, "Salat 5 Waktu", "Untuk keluarga Muslim. Warnai bulatan tanggal setiap kali selesai salat.")}
<div class="instr">Beri tanda centang atau warnai bulatan sesuai tanggalnya.</div>
<div style="flex:1;display:flex;flex-direction:column;justify-content:space-between;gap:8px">{"".join(block(n, col) for n, col in names)}</div>
<div class="tint" style="margin-top:8px;font-size:12.5px;text-align:center">Beribadah dengan ikhlas, hati tenang, hari pun berkah! Keluarga dengan agama lain bisa memakai halaman <b>Pohon Syukur &amp; Doa</b>.</div>"""
    b.add(body, c, deco([(A.mosque(70), "right:34px;top:26px")]))


def p_pohon_syukur(b):
    k = 2
    c = hc(k)
    import math
    leaves = ""
    # 31 leaves in rings inside a crown centred at (340,250)
    rings = [(0, 1), (70, 7), (135, 11), (195, 12)]
    d = 1
    for r, n in rings:
        for i in range(n):
            if d > 31:
                break
            a = math.radians(-90 + i * 360 / n + (15 if r == 135 else 0))
            x, y = 340 + r * 1.45 * math.cos(a), 245 + r * math.sin(a)
            leaves += (f'<g transform="translate({x:.0f},{y:.0f}) rotate({(i*37)%60-30})"><path d="M0 -22 Q20 -8 0 22 Q-20 -8 0 -22Z" fill="#fff" stroke="{c[0]}" stroke-width="2.5"/>'
                       f'<text x="0" y="6" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="14" fill="{c[0]}" transform="rotate({-((i*37)%60-30)})">{d}</text></g>')
            d += 1
    tree = (f'<svg viewBox="0 0 680 520" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">'
            f'<ellipse cx="340" cy="245" rx="330" ry="235" fill="{c[1]}"/>'
            f'<path d="M318 520 L326 380 Q300 340 250 330 M326 380 L330 300 M354 520 L350 380 Q380 340 430 330 M350 380 L346 300" stroke="#8a5a36" stroke-width="16" fill="none" stroke-linecap="round"/>'
            f'<rect x="312" y="430" width="56" height="90" rx="10" fill="#8a5a36"/>{leaves}</svg>')
    weeks = "".join(f'<div class="box" style="padding:8px 10px"><h3 class="c">Minggu {w}: doa / harapanku</h3><div class="line"></div><div class="line"></div></div>' for w in range(1, 5))
    body = f"""{header(k, "Pohon Syukur &amp; Doa", "Untuk semua agama. Setiap malam, sebutkan satu hal yang kamu syukuri lalu warnai daun bertanggal hari itu.")}
<div style="flex:1;min-height:0">{tree}</div>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:8px;margin-top:8px">{weeks}</div>"""
    b.add(body, c)


def p_calendar(b, k, title, sub, instr, cols, fields, extra_cells=None, footer=""):
    c = hc(k)
    rows_n = -(-(31 + len(extra_cells or [])) // cols)
    def cell(d):
        f = "".join(f'<div style="display:flex;align-items:flex-end;gap:4px;font-size:10.5px;color:#7b8090;margin-top:3px"><span>{x}</span><span style="flex:1;border-bottom:1.3px dotted #aab0bf;height:13px"></span></div>' for x in fields)
        return (f'<div style="border:2px solid {c[0]}66;border-radius:14px;padding:5px 7px;background:#fff;display:flex;flex-direction:column">'
                f'<span class="num numf" style="width:24px;height:24px;font-size:12.5px">{d}</span>{f}</div>')
    cells = "".join(cell(d) for d in range(1, 32))
    for lab in (extra_cells or []):
        cells += f'<div style="border:2px dashed {c[0]};border-radius:14px;padding:6px 8px;background:{c[1]};font:600 12.5px Fredoka;color:{c[0]}">{lab}</div>'
    body = f"""{header(k, title, sub)}<div class="instr">{instr}</div>
<div style="flex:1;display:grid;grid-template-columns:repeat({cols},1fr);grid-template-rows:repeat({rows_n},1fr);gap:7px">{cells}</div>{footer}"""
    b.add(body, c)


def p_bingo(b, k, title, sub, items, n, footer_html=""):
    c = hc(k)
    cells = ""
    for i, it in enumerate(items):
        if it == "FREE":
            cells += f'<div style="background:{c[0]};border-radius:14px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;font:700 18px Fredoka">{A.star(44)}BEBAS!</div>'
        else:
            cells += (f'<div style="border:2.5px solid {c[0]}77;border-radius:14px;display:flex;align-items:center;justify-content:center;text-align:center;padding:6px;'
                      f'font:500 {14 if n == 5 else 15}px Fredoka;background:{c[1] if i % 2 else "#fff"}">{it}</div>')
    body = f"""{header(k, title, sub, bulan=False)}
<div class="instr">Silang atau warnai kotak yang sudah kamu lakukan. Dapat satu baris lurus? <b>BINGO!</b> Warnai 1 bintang bonus.</div>
<div style="height:{560 if n == 5 else 470}px;display:grid;grid-template-columns:repeat({n},1fr);grid-template-rows:repeat({n},1fr);gap:7px">{cells}</div>
{footer_html}"""
    b.add(body, c)


def p_food_log(b, k, days, with_header, extra=None):
    c = hc(k)
    def card(d):
        meals = "".join(f'<div style="display:flex;align-items:flex-end;gap:6px"><b style="width:46px;font:600 13.5px Fredoka;color:{col}">{m}</b><span style="flex:1;border-bottom:1.4px dotted #aab0bf;height:20px"></span></div>'
                        for m, col in (("Pagi", "#e07b00"), ("Siang", "#e5484d"), ("Malam", "#4b55d6")))
        glasses = "".join(A.glass(21) for _ in range(8))
        return (f'<div style="border:2px solid {c[0]}55;border-radius:16px;padding:7px 10px;background:#fff;display:flex;flex-direction:column;justify-content:space-between">'
                f'<div style="display:flex;gap:8px;flex:1"><span class="num numf" style="width:30px;height:30px">{d}</span><div class="grow" style="display:flex;flex-direction:column;justify-content:space-evenly">{meals}</div></div>'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-top:5px"><span style="display:flex;gap:3px">{glasses}</span>'
                f'<span style="font:600 11px Fredoka;color:#16a34a"><span class="chk" style="width:13px;height:13px;border-color:#16a34a"></span>sayur <span class="chk" style="width:13px;height:13px;border-color:#e07b00;margin-left:4px"></span>buah</span></div></div>')
    cells = "".join(card(d) for d in days)
    if extra:
        cells += extra
    nrows = -(-(len(days) + (1 if extra else 0)) // 2)
    top = header(k, "Catatan Makan &amp; Minum", "Tulis menu makanmu, warnai 1 gelas setiap minum air putih, dan centang jika makan sayur atau buah.") if with_header else ""
    body = f"""{top}<div style="flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat({nrows},1fr);gap:9px">{cells}</div>"""
    b.add(body, c, deco([] if with_header else [(A.drop(46), "right:22px;top:16px")]))


def p_piringku(b):
    k = 4
    c = hc(k)
    plate_empty = (f'<svg viewBox="0 0 220 220" width="210" height="210"><circle cx="110" cy="110" r="104" fill="#fff" stroke="#cfd8dc" stroke-width="5"/>'
                   f'<circle cx="110" cy="110" r="86" fill="none" stroke="#e3e9ec" stroke-width="3" stroke-dasharray="6 6"/></svg>')
    checks = ["Ada sayur", "Ada buah", "Ada makanan pokok (nasi, jagung, ubi, roti)", "Ada lauk (ikan, telur, ayam, tahu, tempe)", "Cuci tangan pakai sabun", "Minum air putih"]
    ck = "".join(f'<li><span class="chk"></span>{x}</li>' for x in checks)
    body = f"""{header(k, "Isi Piringku", "Pedoman gizi seimbang dari Kementerian Kesehatan: setengah piring sayur dan buah, setengah piring makanan pokok dan lauk pauk.", bulan=False)}
<div class="flex" style="align-items:center;gap:20px">
<div style="width:300px;flex:none">{A.isi_piringku(300)}</div>
<div class="grow"><div class="fact" style="font-size:13.5px"><b class="c">Cara membaca piring:</b><br>
• <b>Sayur</b> lebih banyak dari buah (sepertiga piring).<br>• <b>Buah</b> seperenam piring.<br>• <b>Makanan pokok</b> sepertiga piring.<br>• <b>Lauk pauk</b> seperenam piring.</div>
<p class="small" style="margin-top:6px">Ukuran porsi menyesuaikan usia dan aktivitas anak.</p></div></div>
<h2>Gambar piring makan siangmu!</h2>
<div class="flex" style="gap:18px;align-items:center">
<div class="center">{plate_empty}<div style="font:600 14px Fredoka;color:{c[0]}">Piringku hari ini</div><div class="small">Tanggal: ..................</div></div>
<div class="center">{plate_empty}<div style="font:600 14px Fredoka;color:{c[0]}">Piring impianku yang seimbang</div><div class="small">Tanggal: ..................</div></div></div>
<h2>Cek piringku</h2><div class="box"><ul class="tick" style="columns:2">{ck}</ul></div>"""
    b.add(body, c, deco([(A.carrot(56), "right:30px;bottom:60px")]))


def p_pelangi(b):
    k = 4
    c = hc(k)
    groups = [("Merah", "#e5484d", "tomat, semangka, jambu biji merah, paprika merah"),
              ("Oranye &amp; Kuning", "#f59e0b", "wortel, pepaya, jeruk, jagung, pisang, labu"),
              ("Hijau", "#16a34a", "bayam, kangkung, brokoli, buncis, sawi, alpukat"),
              ("Ungu &amp; Biru", "#7c4dff", "terong, ubi ungu, anggur, kol ungu"),
              ("Putih &amp; Cokelat", "#8a6a4f", "kembang kol, jamur, tauge, salak, kentang")]
    rows = "".join(f'<div style="display:flex;align-items:center;gap:12px;border-radius:16px;padding:8px 12px;border:2.5px solid {col}55">'
                   f'<div style="width:20px;align-self:stretch;border-radius:10px;background:{col}"></div>'
                   f'<div class="grow"><div style="font:700 18px Fredoka;color:{col}">{n}</div><div class="small">contoh: {ex}</div>'
                   f'<div class="flex" style="align-items:flex-end;margin-top:4px;font-size:12px"><span>Yang kumakan:</span><span class="ln" style="height:18px"></span></div></div>'
                   f'<div style="text-align:center"><div class="small">Minggu</div><div style="display:flex;gap:5px">' +
                   "".join(f'<span class="circ" style="border-color:{col};color:{col}">{w}</span>' for w in range(1, 5)) + '</div></div></div>' for n, col, ex in groups)
    body = f"""{header(k, "Pelangi Sayur &amp; Buah", "Makan beragam warna setiap minggu. Warnai bulatan minggu saat kamu sudah makan warna itu.", bulan=False)}
<div style="flex:1;display:flex;flex-direction:column;justify-content:space-between;gap:8px">{rows}</div>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:10px;margin-top:10px">
<div class="box"><h3 class="c">Sayur/buah baru yang kucoba</h3><div class="line"></div><div class="line"></div></div>
<div class="box"><h3 class="c">Rasanya menurutku…</h3><div class="line"></div><div class="line"></div></div></div>"""
    b.add(body, c, deco([(A.rainbow(110), "right:26px;top:24px")]))


def p_reading(b):
    k = 5
    c = hc(k)
    rows = "".join(f'<tr><td class="center" style="font:600 13px Fredoka;color:{c[0]}">{i}</td><td></td><td></td><td></td><td style="white-space:nowrap">{"".join(A.star_outline(18, color=c[0]) for _ in range(5))}</td></tr>' for i in range(1, 13))
    body = f"""{header(k, "Buku yang Kubaca", "Catat setiap buku atau cerita yang selesai kamu baca, lalu beri bintang!", bulan=True)}
<table style="font-size:13px"><tr><th style="width:34px">No</th><th>Judul buku</th><th style="width:130px">Penulis</th><th style="width:70px">Tanggal selesai</th><th style="width:110px">Nilaiku</th></tr>
{rows.replace('<td></td>', '<td style="height:36px"></td>')}</table>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:10px;margin-top:12px;flex:1">
<div class="box"><h3 class="c">Kata baru yang kupelajari</h3><div class="lines">{'<div class="line"></div>'*5}</div></div>
<div class="box"><h3 class="c">Gambar tokoh favoritku</h3></div></div>"""
    b.add(body, c)


def p_sleep_table(b):
    k = 7
    c = hc(k)
    def tbl(days):
        r = "".join(f'<tr><td class="center" style="font:600 13px Fredoka;color:{c[0]}">{d}</td><td class="center" style="color:#b4b9c6">.... : ....</td><td class="center" style="color:#b4b9c6">.... : ....</td><td></td><td class="center">{A.star_outline(18, color=c[0])}</td></tr>' for d in days)
        return f'<table style="font-size:12.5px"><tr><th style="width:36px">Tgl</th><th>Jam tidur</th><th>Jam bangun</th><th style="width:52px">Total jam</th><th style="width:36px">☆</th></tr>{r}</table>'
    body = f"""{header(k, "Jam Tidurku", "Tulis jam tidur dan jam bangun, lalu hitung berapa jam kamu tidur. Warnai bintang jika tidur 9 jam atau lebih (usia 6–12 tahun).")}
<div class="flex" style="gap:14px;flex:1;align-items:flex-start">{tbl(range(1, 17))}{tbl(range(17, 32))}</div>
<div class="tint" style="font-size:12.5px;text-align:center">Cara menghitung: dari jam tidur sampai jam bangun. Contoh: tidur 20.30, bangun 05.30 = <b>9 jam</b>.</div>"""
    b.add(body.replace("<td></td>", '<td style="height:43px"></td>'), c)


def chart_page(b, k, title, sub, ylabels, band=None, kind="dot", note=""):
    c = hc(k)
    W, Hh, L, T = 680, 600, 64, 16
    gw, gh = W - L - 10, Hh - T - 40
    n = len(ylabels)
    g = ""
    for i, lab in enumerate(ylabels):
        y = T + gh - i * gh / (n - 1)
        g += f'<line x1="{L}" y1="{y:.1f}" x2="{W-10}" y2="{y:.1f}" stroke="rgba(0,0,0,.14)" stroke-width="1"/>'
        g += f'<text x="{L-8}" y="{y+4:.1f}" text-anchor="end" font-family="Fredoka" font-size="12" fill="#51675b">{lab}</text>'
    for d in range(1, 32):
        x = L + (d - 0.5) * gw / 31
        g += f'<line x1="{x:.1f}" y1="{T}" x2="{x:.1f}" y2="{T+gh}" stroke="rgba(0,0,0,.07)" stroke-width="1"/>'
        g += f'<text x="{x:.1f}" y="{T+gh+18}" text-anchor="middle" font-family="Fredoka" font-size="11" fill="#51675b">{d}</text>'
    if band:
        lo, hi, lab = band
        y1 = T + gh - hi * gh / (n - 1)
        y0 = T + gh - lo * gh / (n - 1)
        g = f'<rect x="{L}" y="{y1:.1f}" width="{gw}" height="{y0-y1:.1f}" fill="{c[1]}"/><text x="{W-16}" y="{y1+16:.1f}" text-anchor="end" font-family="Fredoka" font-weight="600" font-size="13" fill="{c[0]}">{lab}</text>' + g
    g += f'<text x="{L+gw/2}" y="{Hh-2}" text-anchor="middle" font-family="Fredoka" font-size="12" fill="#51675b">Tanggal</text>'
    svg = f'<svg viewBox="0 0 {W} {Hh}" width="100%" style="display:block">{g}</svg>'
    body = f"""{header(k, title, sub)}
<div class="instr">{"Beri titik pada jam bangunmu setiap hari, lalu sambungkan titik-titiknya menjadi garis." if kind == "dot" else "Warnai batang dari bawah sampai jumlah jam tidurmu setiap hari."}</div>
<div class="box" style="padding:10px 8px">{svg}</div>
{note}"""
    b.add(body, c)


def p_rekap(b):
    c = BRAND
    head = "".join(f'<th style="background:{H[k][1]};padding:4px 2px"><div style="width:30px;height:30px;margin:0 auto">{A.MASCOT[k](30)}</div><div style="font-size:9.5px;line-height:1.05">{H[k][0].replace(" & Bergizi","")}</div></th>' for k in H)
    rows = "".join(f'<tr><td class="center" style="font:600 12px Fredoka;color:{c[0]};padding:0">{d}</td>' + "".join('<td style="padding:0"></td>' for _ in H) + f'<td style="padding:0"></td></tr>' for d in range(1, 32))
    body = f"""<div class="center"><div class="kicker">Satu halaman, semua misi</div><h1 style="font-size:38px">{rainbow("Tracker Gabungan 7 Misi")}</h1>
<p class="sub">Centang setiap misi yang selesai hari itu. Hitung totalnya di kolom terakhir.</p></div>
<div class="bulan"><span class="tag">Bulan</span><span class="ln"></span><span class="tag">Tahun</span><span class="ln" style="flex:.45"></span></div>
<table style="flex:1;table-layout:fixed"><tr><th style="width:44px">Tgl</th>{head}<th style="width:54px">Total<br>/7</th></tr>{rows}</table>"""
    b.add(body.replace('<td style="padding:0"></td>', '<td style="padding:0;height:24px"></td>'), c, bookmark="Tracker Gabungan 7 Misi")


def p_refleksi(b, weeks):
    c = ("#7c4dff", "#f0ebff")
    def blk(w, rng):
        moods = "".join(f'<div style="text-align:center"><svg viewBox="0 0 40 40" width="34" height="34"><circle cx="20" cy="20" r="17" fill="#fff" stroke="{c[0]}" stroke-width="2.2"/></svg><div class="small">{d}</div></div>' for d in ("Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"))
        return f"""<div class="box" style="flex:1;display:flex;flex-direction:column;gap:6px;border-width:2.5px">
<div class="flex" style="align-items:center"><span class="tag">Minggu {w}</span><span class="small">hari ke-{rng}</span><span class="grow"></span><span style="display:flex;gap:2px">{"".join(A.star_outline(24, color=c[0]) for _ in range(5))}</span></div>
<div><b style="font-family:Fredoka">Perasaanku minggu ini</b> <span class="small">(gambar wajah di tiap bulatan: senang, biasa, sedih)</span><div class="flex" style="justify-content:space-between;margin-top:4px">{moods}</div></div>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:10px">
<div><b style="font-family:Fredoka;color:#16a34a">Misi paling mudah</b><div class="line"></div></div>
<div><b style="font-family:Fredoka;color:#e5484d">Misi paling sulit</b><div class="line"></div></div></div>
<div><b style="font-family:Fredoka">Aku bangga karena…</b><div class="line"></div><div class="line"></div></div>
<div><b style="font-family:Fredoka">Minggu depan aku akan…</b><div class="line"></div></div>
<div class="flex" style="align-items:flex-end"><b style="font-family:Fredoka;white-space:nowrap">Pesan Ayah/Bunda:</b><span class="ln"></span><span class="small">paraf</span><span style="width:60px;border-bottom:2px solid #c4c9d6;height:22px"></span></div>
</div>"""
    body = f"""{header(5, "Refleksi Mingguan", "Lihat kembali minggumu. Apa yang berhasil? Apa yang ingin dicoba lagi?", bulan=False, kicker="Akhir pekan").replace(A.MASCOT[5](86), A.star(86))}
<div style="flex:1;display:flex;flex-direction:column;gap:12px">{"".join(blk(w, r) for w, r in weeks)}</div>"""
    b.add(body, c, bookmark="Refleksi Mingguan" if weeks[0][0] == 1 else None)


def p_bintang(b):
    c = ("#e07b00", "#fff3e0")
    cells = ""
    for d in range(1, 32):
        mile = d in (7, 14, 21, 30)
        cells += (f'<div style="text-align:center;position:relative">{A.star_outline(72, num=d, color=("#e5484d" if mile else c[0]))}'
                  + (f'<div style="font:600 10.5px Fredoka;color:#e5484d;margin-top:-4px">🎁 hadiah!</div>' if mile else "") + '</div>')
    body = f"""<div class="center"><div class="kicker">Kumpulkan semuanya!</div><h1 style="font-size:44px">{rainbow("Koleksi Bintangku")}</h1>
<p class="sub">Warnai atau tempel stiker bintang setiap hari misimu tuntas. Bintang merah berarti waktunya hadiah dari Tangga Hadiah!</p></div>
<div style="flex:1;display:grid;grid-template-columns:repeat(6,1fr);align-content:space-evenly;gap:6px;margin-top:10px">{cells}
<div style="grid-column:span 5;display:flex;align-items:center;justify-content:center;gap:10px;font:600 18px Fredoka;color:{c[0]}">{A.trophy(64)} Total bintangku: <span style="width:80px;border-bottom:3px dashed {c[0]};height:30px"></span> / 31</div></div>"""
    b.add(body, c, bookmark="Koleksi Bintangku")


def p_paraf(b):
    c = ("#0f9d78", "#e4f6ef")
    rows = "".join(f'<tr><td style="height:70px"><b style="font-family:Fredoka;color:{c[0]}">{w}</b></td><td></td><td></td><td></td><td></td></tr>' for w in ("Minggu 1", "Minggu 2", "Minggu 3", "Minggu 4", "Akhir bulan"))
    body = f"""<div class="center"><div class="kicker">Jembatan rumah &amp; sekolah</div><h1 style="font-size:40px">{rainbow("Lembar Paraf Ayah-Bunda &amp; Guru")}</h1>
<p class="sub">Bawa jurnal ke sekolah setiap akhir pekan (bila diminta guru) untuk diparaf.</p></div>
<table style="margin-top:14px;font-size:13px"><tr><th style="width:96px">Pekan</th><th style="width:90px">Tanggal</th><th style="width:110px">Paraf Ayah/Bunda</th><th style="width:100px">Paraf Guru</th><th>Catatan</th></tr>{rows}</table>
<h2>Catatan perkembangan dari guru</h2>
<div class="box lines" style="flex:1">{'<div class="line"></div>'*8}</div>
<h2>Catatan dari Ayah / Bunda</h2>
<div class="box lines">{'<div class="line"></div>'*4}</div>"""
    b.add(body, c, bookmark="Lembar Paraf Ayah-Bunda & Guru")


def p_sertifikat(b):
    c = ("#e07b00", "#fff3e0")
    badges = "".join(f'<div style="width:58px;height:58px;border-radius:50%;background:{H[k][2]};border:2.5px solid {H[k][1]};display:flex;align-items:center;justify-content:center">{A.MASCOT[k](42)}</div>' for k in H)
    body = f"""<div style="flex:1;border:6px double #e07b00;border-radius:28px;padding:30px 34px;display:flex;flex-direction:column;align-items:center;text-align:center">
{A.medal(130)}
<div class="kicker" style="font-size:15px;margin-top:6px">Sertifikat Penghargaan</div>
<h1 style="font-size:62px;margin-top:6px">{rainbow("ANAK HEBAT")}</h1>
<p style="font:500 18px Fredoka;margin-top:18px">dengan bangga diberikan kepada</p>
<div style="width:80%;border-bottom:3px dashed #e07b00;height:56px"></div>
<p style="font-size:16px;margin-top:18px;max-width:520px">karena telah menyelesaikan <b>Misi 30 Hari 7 Kebiasaan Anak Indonesia Hebat</b> dengan semangat, kejujuran, dan pantang menyerah.</p>
<div class="flex" style="gap:10px;margin:18px 0">{badges}</div>
<div class="flex" style="align-items:flex-end;font:500 15px Fredoka;width:70%"><span>Jumlah bintang:</span><span class="ln"></span><span>Tanggal:</span><span class="ln"></span></div>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:60px;width:85%;margin-top:auto">
<div><div style="height:60px"></div><div class="sig">Ayah / Bunda</div></div><div><div style="height:60px"></div><div class="sig">Guru / Wali Kelas</div></div></div>
</div>"""
    b.add(body, c, deco([(A.star(50), "left:30px;top:30px"), (A.star(50), "right:30px;top:30px"), (A.sparkle(26), "left:60px;bottom:90px"), (A.sparkle(26), "right:60px;bottom:90px")]), bookmark="Sertifikat Anak Hebat", frame=False)


def p_penutup(b):
    c = BRAND
    body = f"""<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:10px">
<div class="flex" style="gap:16px;align-items:flex-end">{A.kid(120)}{A.star(90)}{A.kid(120, girl=True, shirt='#d6409f')}</div>
<h1 style="font-size:46px">{rainbow("Terima Kasih, Anak Hebat!")}</h1>
<p style="font:500 17px Fredoka;max-width:520px;color:#3b3f4f">Kebiasaan kecil yang diulang setiap hari akan menjadi kekuatan besar. Teruskan misimu bulan depan, ya!</p>
<div class="tint" style="max-width:560px;font-size:13px;text-align:left;margin-top:10px"><b class="c">Mau melanjutkan?</b> Cetak ulang halaman tracker, refleksi, Koleksi Bintang, dan Sertifikat untuk bulan berikutnya. Lisensi: untuk penggunaan pribadi, keluarga, dan kelas sendiri. Dilarang menjual ulang file ini.</div>
<div style="margin-top:22px;font:600 18px Fredoka;color:{c[0]}"><a href="{URL}" style="color:{c[0]};text-decoration:none">www.GoSatSet.xyz</a></div>
<div class="small">© {YEAR} www.GoSatSet.xyz · {TITLE}: {SUBTITLE}</div></div>"""
    b.add(body, c, deco([(A.sun(80), "left:30px;top:26px"), (A.rainbow(130), "right:26px;top:36px")]), bookmark="Penutup")


# ---------------------------------------------------------------- assemble
def build(toc_pages=None):
    b = Book()
    b.pages.append(f'<section class="page" style="--c:#16a34a">{cover_html()}</section>')
    toc_pages = toc_pages or {}

    p_identitas(b)
    toc_slot = len(b.pages)
    b.pages.append(None)  # placeholder for TOC
    b.marks.append(("Daftar Isi", toc_slot))
    p_guide1(b); p_guide2(b); p_kontrak(b); p_poster(b); rating_page(b); p_target(b); p_jadwal(b)

    # Misi 1
    intro(b, 1, "Pagi yang cerah dimulai dari bangun tepat waktu!",
          [("Tidak terburu-buru", "Ada waktu mandi, sarapan, dan bersiap dengan tenang."), ("Sempat sarapan", "Perut terisi membuat badan bertenaga sampai siang."), ("Badan segar", "Cahaya pagi dan udara segar membuatmu semangat.")],
          ["Bangun tanpa menunda", "Merapikan tempat tidur", "Cuci muka &amp; sikat gigi", "Minum segelas air putih", "Sarapan", "Menyiapkan tas sendiri"],
          f"Anak usia 6–12 tahun butuh tidur <b>9–12 jam</b> [3]. Kalau ingin bangun pukul <b>05.30</b> dan tidur 9 jam, berarti harus sudah tidur pukul <b>{SLEEP_TABLE[1][1]}</b>. Jadi, rahasia bangun pagi adalah tidur cepat!",
          "letakkan jam weker agak jauh dari ranjang dan buka tirai di pagi hari. Pujilah setiap kali anak bangun sendiri.")
    p_time_log(b, 1, "Jam Bangunku", "Tulis jam berapa kamu bangun setiap hari.", "Tuliskan jam bangun pada tanggal tersebut. Warnai bintang jika kamu bangun sesuai target!", "= bangun sesuai target (lihat Target &amp; Hadiahku)")
    chart_page(b, 1, "Grafik Bangun Pagi", "Lihat garis jam bangunmu. Makin rata, makin teratur!",
               ["04.30", "05.00", "05.30", "06.00", "06.30", "07.00", "07.30"],
               note='<div class="grid" style="grid-template-columns:1fr 1fr;gap:10px;margin-top:12px"><div class="box"><h3 class="c">Jam bangun paling pagi bulan ini</h3><div class="line"></div></div><div class="box"><h3 class="c">Yang membantuku bangun pagi</h3><div class="line"></div></div></div>')
    # Misi 2
    intro(b, 2, "Hati yang bersyukur membuat hari terasa indah.",
          [("Hati tenang", "Berdoa membantu kita lebih tenang saat senang maupun sedih."), ("Belajar bersyukur", "Kita jadi ingat hal-hal baik yang kita punya."), ("Berbuat baik", "Ajaran agama mengajak kita jujur, sabar, dan menolong.")],
          ["Berdoa saat bangun tidur", "Beribadah tepat waktu", "Berdoa sebelum makan", "Membaca kitab suci", "Mengucap terima kasih", "Berdoa sebelum tidur"],
          "Beribadah adalah kebiasaan kedua dalam Gerakan 7 Kebiasaan Anak Indonesia Hebat [1]. Setiap keluarga bisa mengisi misi ini <b>sesuai agama dan keyakinannya</b>: ada halaman Salat 5 Waktu dan halaman Pohon Syukur &amp; Doa untuk semua agama.",
          "beribadah bersama lebih menyenangkan daripada disuruh. Ajak anak berdoa bersama dan ceritakan kisah teladan dari agama keluarga.")
    p_salat(b); p_pohon_syukur(b)
    # Misi 3
    intro(b, 3, "Ayo bergerak! Tubuh kuat, hati gembira.",
          [("Tubuh kuat", "Otot dan tulang tumbuh lebih kuat saat sering bergerak."), ("Tidur nyenyak", "Badan yang aktif di siang hari lebih mudah tidur di malam hari."), ("Banyak teman", "Bermain bola, lompat tali, dan gobak sodor seru dilakukan bersama.")],
          ["Pemanasan sebelum main", "Bergerak 60 menit hari ini", "Minum air setelah olahraga", "Main di luar rumah", "Peregangan sebelum tidur", "Mengurangi duduk lama"],
          "Badan Kesehatan Dunia (WHO) menganjurkan anak usia 5–17 tahun bergerak aktif <b>rata-rata 60 menit setiap hari</b>, dengan aktivitas yang lebih berat setidaknya <b>3 hari seminggu</b> [4]. 60 menit itu boleh dicicil: 20 menit main pagi + 20 menit sore + 20 menit main bersama keluarga.",
          "tidak harus ikut klub olahraga. Jalan kaki ke warung, bersepeda di kompleks, atau menari bersama di rumah sudah termasuk bergerak aktif.")
    p_calendar(b, 3, "Catatan Olahragaku", "Tulis jenis olahraga dan berapa menit kamu bergerak.", "Isi jenis olahraga dan lamanya. Targetnya rata-rata 60 menit sehari!", 5,
               ["Jenis:", "Menit:"], ["Total menit<br>minggu 1–2:", "Total menit<br>minggu 3–4:", "Olahraga<br>favoritku:", "Rekor terbaikku:"])
    bingo3 = ["Lompat tali 50 kali", "Bersepeda", "Jalan kaki keliling rumah", "Lari kecil 10 menit", "Senam pagi",
              "Menari 1 lagu", "Main sepak bola", "Bulu tangkis", "Petak umpet", "Engklek",
              "Gobak sodor", "Lompat bintang 20 kali", "FREE", "Main lompat karet", "Jongkok-berdiri 10 kali",
              "Berdiri satu kaki 30 detik", "Main basket", "Main layangan", "Peregangan 5 menit", "Naik turun tangga 5 kali",
              "Main kejar-kejaran", "Menyapu halaman", "Hula hoop", "Berenang (didampingi)", "Main bola bersama Ayah"]
    rekor = ("<h2>Rekor Pribadiku</h2><table style='font-size:13px'><tr><th>Tantangan</th><th>Minggu 1</th><th>Minggu 2</th><th>Minggu 3</th><th>Minggu 4</th></tr>"
             + "".join(f"<tr><td style='height:34px'>{t}</td><td></td><td></td><td></td><td></td></tr>" for t in ("Lompat tali dalam 1 menit (kali)", "Lompat bintang tanpa berhenti (kali)", "Berdiri satu kaki (detik)")) + "</table>")
    p_bingo(b, 3, "Bingo Gerak Seru", "25 ide bergerak. Bisa kamu selesaikan semua bulan ini?", bingo3, 5, rekor)
    # Misi 4
    intro(b, 4, "Piring berwarna, tubuh bertenaga!",
          [("Tumbuh optimal", "Makanan bergizi membantu tubuh tumbuh tinggi dan kuat."), ("Fokus belajar", "Sarapan dan makan teratur membuat kita tidak lemas di kelas."), ("Jarang sakit", "Sayur, buah, dan cuci tangan membantu menjaga tubuh.")],
          ["Sarapan sebelum sekolah", "Makan sayur", "Makan buah", "Minum air putih", "Cuci tangan pakai sabun", "Mengurangi jajan manis"],
          f"Menurut pedoman <b>Isi Piringku</b> dari Kementerian Kesehatan, setengah piring diisi sayur dan buah, setengahnya lagi makanan pokok dan lauk pauk [5]. Anak 7–9 tahun butuh air sekitar <b>1.650 mL</b> sehari, kira-kira {WATER_GLASS:.0f} gelas kecil [6].",
          "ajak anak memilih sayur di pasar dan ikut menyiapkan makanan. Anak lebih mau mencoba makanan yang ia bantu buat sendiri.")
    p_piringku(b)
    p_food_log(b, 4, range(1, 9), True)
    p_food_log(b, 4, range(9, 21), False)
    tipbox = (f'<div style="border:2px dashed {H[4][1]};border-radius:16px;padding:10px 12px;background:{H[4][2]};display:flex;align-items:center;gap:10px">'
              f'<div style="width:60px;flex:none">{A.drop(60)}</div><div style="font:500 13px Fredoka">Jangan lupa minum air putih yang cukup agar tubuh sehat, kuat, dan bersemangat!</div></div>')
    p_food_log(b, 4, range(21, 32), False, extra=tipbox)
    p_pelangi(b)
    # Misi 5
    intro(b, 5, "Setiap hari ada hal baru yang bisa dipelajari!",
          [("Otak tumbuh", "Belajar dan membaca melatih otak seperti olahraga melatih otot."), ("Rasa ingin tahu", "Bertanya “kenapa?” membuat dunia terasa seru."), ("Cita-cita dekat", "Ilmu adalah bekal untuk meraih cita-citamu.")],
          ["Mengulang pelajaran hari ini", "Membaca 15 menit", "Mengerjakan PR sendiri", "Bertanya hal yang belum paham", "Merapikan meja belajar", "Belajar tanpa gawai"],
          f"Membaca <b>15 menit</b> setiap hari selama 30 hari = <b>{READ_15_30} menit</b>, atau <b>{READ_15_30_H:.1f} jam</b> membaca dalam sebulan! Sedikit demi sedikit, lama-lama menjadi bukit.",
          "temani anak membaca, lalu ajukan satu pertanyaan tentang ceritanya. Sediakan sudut belajar yang tenang dan jauh dari televisi.")
    p_calendar(b, 5, "Catatan Belajarku", "Tulis apa yang kamu pelajari dan berapa lama.", "Catat kegiatan belajar pada tanggal tersebut. Warnai wajah senang jika kamu paham!", 4,
               ["Belajar:", "Lama:", "Paham? ☺ / ☹"], ["Total waktu belajarku bulan ini:<br><br>...... jam"])
    p_reading(b)
    # Misi 6
    intro(b, 6, "Kebaikan kecil membuat dunia lebih hangat.",
          [("Disayang teman", "Anak yang ramah dan suka menolong mudah punya teman."), ("Lingkungan bersih", "Bergotong royong membuat rumah dan kampung nyaman."), ("Belajar peduli", "Kita belajar memahami perasaan orang lain.")],
          ["Menyapa tetangga", "Membantu pekerjaan rumah", "Berbagi dengan teman", "Membuang sampah di tempatnya", "Mengucap tolong, maaf, terima kasih", "Antre dengan sabar"],
          "Gerakan 7 Kebiasaan Anak Indonesia Hebat dijalankan bersama oleh <b>sekolah, keluarga, masyarakat, dan media</b> [2]. Artinya, lingkungan sekitarmu juga tempat belajar!",
          "libatkan anak dalam kegiatan RT, kerja bakti, atau menjenguk tetangga. Ceritakan kebaikan yang Ayah/Bunda lakukan hari ini.")
    p_calendar(b, 6, "Catatan Kebaikanku", "Tulis kebaikan atau kegiatan bersama orang lain setiap hari.", "Catat kegiatan bermasyarakat pada tanggal tersebut, lalu lingkari tempatnya: R = rumah, S = sekolah, L = lingkungan.", 4,
               ["Kegiatan:", "", "Di: R / S / L"], ["Orang yang paling<br>sering kubantu:<br><br>.........................."])
    bingo6 = ["Menyapa tetangga", "Membantu memasak", "Membuang sampah pada tempatnya", "Berbagi bekal",
              "Merapikan alas kaki", "Ikut kerja bakti", "Menanyakan kabar teman yang sakit", "Membantu teman belajar",
              "Menyiram tanaman", "Antre dengan sabar", "Meminta maaf saat salah", "Mengajak teman baru bermain",
              "Membawakan barang orang tua", "Mendoakan orang lain", "Menjaga kebersihan kelas", "Mengucap terima kasih"]
    teman = ("<div class='grid' style='grid-template-columns:1fr 1fr;gap:10px;margin-top:12px;flex:1'>"
             "<div class='box'><h3 class='c'>Teman baru bulan ini</h3>" + "<div class='line'></div>" * 4 + "</div>"
             "<div class='box'><h3 class='c'>Kebaikan yang kuterima dari orang lain</h3>" + "<div class='line'></div>" * 4 + "</div></div>")
    p_bingo(b, 6, "Bingo Kebaikan", "16 kebaikan kecil untuk orang-orang di sekitarmu.", bingo6, 4, teman)
    # Misi 7
    intro(b, 7, "Tidur cepat, bangun semangat!",
          [("Tubuh tumbuh", "Saat tidur, tubuh beristirahat dan memulihkan tenaga."), ("Mudah mengingat", "Tidur cukup membantu kita belajar dan mengingat pelajaran."), ("Hati ceria", "Kurang tidur membuat kita mudah rewel dan marah.")],
          ["Simpan gawai sebelum tidur", "Sikat gigi", "Siapkan tas &amp; baju besok", "Berdoa", "Membaca buku cerita", "Lampu diredupkan"],
          "Para ahli tidur Amerika (AASM) menganjurkan anak usia 6–12 tahun tidur <b>9–12 jam</b> setiap hari secara teratur. Tidur yang cukup berkaitan dengan perhatian, perilaku, belajar, dan daya ingat yang lebih baik [3].",
          "buat rutinitas malam yang sama setiap hari, misalnya mandi → sikat gigi → baca buku → doa → lampu dimatikan. Matikan layar beberapa saat sebelum tidur.")
    p_sleep_table(b)
    chart_page(b, 7, "Grafik Tidurku", "Batang yang masuk zona ungu berarti tidurmu sudah cukup.",
               [f"{h} jam" for h in range(6, 14)], band=(3, 6, "Zona cukup tidur: 9–12 jam (usia 6–12 th)"), kind="bar",
               note=('<h2>Rutinitas malamku</h2><div class="box"><ul class="tick" style="columns:3">'
                     + "".join(f'<li><span class="chk"></span>{x}</li>' for x in ("Mandi", "Sikat gigi", "Siapkan tas", "Gawai disimpan", "Baca buku", "Berdoa")) + "</ul></div>"))
    # Rekap
    p_rekap(b)
    p_refleksi(b, [(1, "1–7"), (2, "8–14")])
    p_refleksi(b, [(3, "15–21"), (4, "22–31")])
    p_bintang(b)
    rating_page(b, final=True)
    p_paraf(b)
    p_sertifikat(b)
    p_penutup(b)

    # TOC
    pg = {lab: n for lab, n in b.marks}
    def P(lab):
        return str(pg[lab])
    entries = [
        ("Persiapan", [("Jurnal Ini Milik…", P("Jurnal Ini Milik…"), BRAND[0]), ("Panduan Ayah, Bunda &amp; Guru", P("Panduan Ayah, Bunda & Guru"), BRAND[0]),
                       ("Angka Rujukan &amp; Referensi", P("Angka Rujukan & Referensi"), BRAND[0]), ("Kontrak Janji Anak Hebat", P("Kontrak Janji Anak Hebat"), "#e07b00"),
                       ("Poster 7 Kebiasaan", P("Poster 7 Kebiasaan"), BRAND[0]), ("Peta Awalku", P("Peta Awalku"), "#7c4dff"),
                       ("Target &amp; Hadiahku", P("Target & Hadiahku"), "#e07b00"), ("Jadwal Harianku", P("Jadwal Harianku"), "#2b7de9")]),
        ("7 Misi Harian", [(f"Misi {k}: {H[k][0].replace('&', '&amp;')}", P(f"Misi {k}: {H[k][0]}"), H[k][1]) for k in H]),
        ("Rekap &amp; Perayaan", [("Tracker Gabungan 7 Misi", P("Tracker Gabungan 7 Misi"), BRAND[0]), ("Refleksi Mingguan", P("Refleksi Mingguan"), "#7c4dff"),
                                 ("Koleksi Bintangku", P("Koleksi Bintangku"), "#e07b00"), ("Peta Akhirku", P("Peta Akhirku"), BRAND[0]),
                                 ("Lembar Paraf Ayah-Bunda &amp; Guru", P("Lembar Paraf Ayah-Bunda & Guru"), "#0f9d78"), ("Sertifikat Anak Hebat", P("Sertifikat Anak Hebat"), "#e07b00")]),
    ]
    tb = Book()
    tb.pages = [None] * toc_slot
    p_toc(tb, entries)
    b.pages[toc_slot] = tb.pages[toc_slot]
    b.marks.sort(key=lambda m: m[1])
    html = f"""<!doctype html><html lang="id"><head><meta charset="utf-8"><title>{TITLE}: {SUBTITLE}</title>
<style>{font_css()}{CSS}{COVER_CSS}</style></head><body>{''.join(b.pages)}</body></html>"""
    return html, b.marks, len(b.pages)


def cover_page_html():
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{font_css()}{CSS}{COVER_CSS}
html,body{{width:210mm;height:297mm;overflow:hidden}}</style></head><body>{cover_html()}</body></html>"""


if __name__ == "__main__":
    html, marks, n = build()
    (HERE / "book.html").write_text(html, encoding="utf-8")
    (HERE / "cover.html").write_text(cover_page_html(), encoding="utf-8")
    print("pages:", n)
    for m in marks:
        print(m)
