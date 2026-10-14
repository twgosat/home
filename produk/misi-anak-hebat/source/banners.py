#!/usr/bin/env python3
"""Cover HD + 5 promo banners for Misi Anak Hebat. Usage: banners.py <outdir> <page_count>"""
import sys, pathlib, logging
logging.disable(logging.WARNING)
from playwright.sync_api import sync_playwright
from PIL import Image
import build_book as BB
import svgart as A

HERE = pathlib.Path(__file__).resolve().parent
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
PAGES = int(sys.argv[2])
CHROME = "/opt/pw-browsers/chromium"
cover_png = out / "00-cover-HD-2480x3508.png"
mock_png = HERE / "cover_mock.png"

BASE = BB.font_css() + """
*{box-sizing:border-box}html,body{margin:0;padding:0}
body{font-family:'Fredoka';color:#24324a;overflow:hidden}
.bg{position:absolute;inset:0;background:linear-gradient(180deg,#8fd3ff 0%,#c9ecff 50%,#eefaff 100%)}
.grid{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.55) 2px,transparent 2px);background-size:34px 34px}
.d{position:absolute}
.hills{position:absolute;left:0;bottom:0;width:100%}
.book{position:absolute;perspective:1800px}
.book .b{width:100%;height:100%;transform:rotateY(-22deg) rotateX(3deg);position:relative;border-radius:6px 14px 14px 6px;
  box-shadow:-26px 34px 60px rgba(20,60,110,.40),0 0 70px rgba(255,255,255,.6)}
.book img{width:100%;height:100%;display:block;border-radius:6px 14px 14px 6px}
.book .b:before{content:'';position:absolute;left:0;top:0;bottom:0;width:5%;background:linear-gradient(90deg,rgba(0,0,0,.35),rgba(255,255,255,.18),transparent);z-index:2}
.kp{display:inline-block;background:#16a34a;color:#fff;font-weight:600;letter-spacing:.12em;border-radius:999px}
.hl{font-weight:700;line-height:1.02;color:#1d3557}
.rb span{-webkit-text-stroke:3px #fff;paint-order:stroke fill}
.pill{display:inline-block;background:#fff;color:#127a3a;font-weight:600;border-radius:999px;border:3px solid #9fdc7c;margin:0 8px 10px 0}
.cta{display:inline-block;background:linear-gradient(180deg,#ff8a3d,#e5484d);color:#fff;font-weight:700;border-radius:999px;box-shadow:0 8px 0 #b8323a}
.brand{font-weight:600;color:#127a3a}
"""


def hills(h):
    return (f'<svg class="hills" style="height:{h}px" viewBox="0 0 1000 300" preserveAspectRatio="none">'
            '<path d="M0 110 Q180 40 380 100 T760 80 T1000 60 V300 H0 Z" fill="#9fdc7c"/>'
            '<path d="M0 180 Q260 110 520 170 T1000 140 V300 H0 Z" fill="#72c457"/>'
            '<path d="M0 250 Q320 200 640 240 T1000 230 V300 H0 Z" fill="#4fae3f"/></svg>')


def rbw(text):
    return BB.rainbow(text)


def book(left, top, w, extra=""):
    h = w * 297 / 210
    return f'<div class="book" style="left:{left}px;top:{top}px;width:{w}px;height:{h:.0f}px;{extra}"><div class="b"><img src="{mock_png.as_uri()}"></div></div>'


def page(w, h, body):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE}html,body{{width:{w}px;height:{h}px}}</style></head><body><div class="bg"></div><div class="grid"></div>{body}</body></html>'


PILLS4 = ["Tracker 31 hari", "7 misi harian", "Bingo &amp; aktivitas seru", "Sertifikat Anak Hebat"]

B = {}
B["01-feed-square-1080x1080"] = (1080, 1080, f"""
<div class="d" style="left:24px;top:20px">{A.sun(130)}</div><div class="d" style="right:-20px;top:30px">{A.rainbow(240)}</div>
{hills(300)}
<div class="d" style="left:60px;top:170px;width:560px">
 <div class="kp" style="font-size:20px;padding:8px 22px">PRINTABLE A4 · {PAGES} HALAMAN</div>
 <div class="hl rb" style="font-size:96px;margin-top:16px">{rbw("MISI ANAK HEBAT")}</div>
 <div class="hl" style="font-size:36px;margin-top:14px">Jurnal 30 hari untuk membangun <span style="color:#e5484d">7 Kebiasaan Anak Indonesia Hebat</span></div>
 <div style="margin-top:22px">{''.join(f'<span class="pill" style="font-size:22px;padding:8px 18px">✔ {p}</span>' for p in PILLS4)}</div>
 <div class="cta" style="font-size:34px;padding:16px 40px;margin-top:14px">Download Sekarang</div>
</div>
{book(650, 250, 380)}
<div class="d" style="left:60px;bottom:26px;font-size:24px;color:#fff;font-weight:600;text-shadow:0 2px 4px rgba(0,0,0,.3)">GoSatSet.xyz</div>
""")

B["02-story-1080x1920"] = (1080, 1920, f"""
<div class="d" style="left:40px;top:250px">{A.sun(150)}</div><div class="d" style="right:-20px;top:260px">{A.rainbow(260)}</div>
{hills(420)}
{book(300, 330, 480)}
<div class="d" style="left:70px;right:70px;top:1040px;text-align:center">
 <div class="kp" style="font-size:24px;padding:8px 24px">JURNAL JUARA 30 HARI</div>
 <div class="hl rb" style="font-size:100px;margin-top:14px">{rbw("MISI ANAK HEBAT")}</div>
 <div class="hl" style="font-size:38px;margin-top:10px">7 Kebiasaan Anak Indonesia Hebat</div>
 <div style="text-align:left;margin:26px auto 0;width:760px;font-size:34px;font-weight:600;line-height:1.7;background:rgba(255,255,255,.92);border-radius:28px;padding:18px 34px">
  ✅ {PAGES} halaman siap cetak A4<br>✅ Tracker 31 hari untuk 7 misi<br>✅ Halaman ibadah untuk 6 agama<br>✅ Panduan Ayah-Bunda + sertifikat</div>
 <div class="cta" style="font-size:40px;padding:18px 54px;margin-top:30px">Ambil Sekarang</div>
</div>
""")

B["03-landscape-1200x630"] = (1200, 630, f"""
<div class="d" style="left:16px;top:10px">{A.sun(100)}</div><div class="d" style="right:330px;top:14px">{A.cloud(110)}</div>
{hills(200)}
<div class="d" style="left:70px;top:90px;width:700px">
 <div class="kp" style="font-size:17px;padding:6px 18px">PRINTABLE A4 · {PAGES} HALAMAN</div>
 <div class="hl rb" style="font-size:84px;margin-top:10px">{rbw("MISI ANAK HEBAT")}</div>
 <div class="hl" style="font-size:26px;margin-top:8px;white-space:nowrap">Jurnal Juara 30 Hari · 7 Kebiasaan Anak Indonesia Hebat</div>
 <div style="font-size:21px;font-weight:600;color:#127a3a;margin-top:12px">Tracker 31 hari · Bingo seru · Panduan Ayah-Bunda · Sertifikat</div>
 <div class="cta" style="font-size:28px;padding:12px 34px;margin-top:20px">Download Sekarang</div>
</div>
{book(860, 70, 290)}
""")

B["04-header-web-1920x600"] = (1920, 600, f"""
<div class="d" style="left:30px;top:20px">{A.sun(120)}</div><div class="d" style="left:640px;top:24px">{A.cloud(130)}</div>
<div class="d" style="right:60px;top:20px">{A.rainbow(260)}</div>
{hills(190)}
<div class="d" style="left:200px;top:80px;width:1000px">
 <div class="kp" style="font-size:19px;padding:7px 20px">JURNAL JUARA 30 HARI · SIAP CETAK A4</div>
 <div class="hl rb" style="font-size:100px;margin-top:10px">{rbw("MISI ANAK HEBAT")}</div>
 <div class="hl" style="font-size:34px;margin-top:8px">Satu jurnal, tujuh kebiasaan hebat, tiga puluh hari petualangan.</div>
 <div style="margin-top:16px"><span class="pill" style="font-size:22px;padding:8px 20px">✔ {PAGES} halaman</span><span class="pill" style="font-size:22px;padding:8px 20px">✔ Untuk rumah &amp; kelas</span>
 <span class="cta" style="font-size:28px;padding:12px 36px;margin-left:10px">Download Sekarang</span></div>
</div>
{book(1330, 70, 300)}
""")

CARDS = [(1, "Tracker 31 Hari", "Jam bangun, ibadah, olahraga, makan, belajar, kebaikan, jam tidur"),
         (4, "Isi Piringku &amp; Pelangi", "Belajar gizi seimbang sesuai pedoman Kemenkes"),
         (3, "Bingo Gerak &amp; Kebaikan", "40 ide aktivitas seru tanpa gawai"),
         (2, "Ibadah 6 Agama", "Islam, Kristen, Katolik, Hindu, Buddha, Khonghucu + Pohon Syukur"),
         (5, "Refleksi Mingguan", "Grafik, log buku, paraf Ayah-Bunda &amp; guru"),
         (7, "Bintang &amp; Sertifikat", "Tangga hadiah, koleksi bintang, sertifikat")]
cards = "".join(f'<div style="background:#fff;border-radius:28px;border:4px solid {BB.H[k][1]}55;padding:20px 22px;display:flex;gap:18px;align-items:center">'
                f'<div style="width:96px;height:96px;flex:none;border-radius:50%;background:{BB.H[k][2]};display:flex;align-items:center;justify-content:center">{A.MASCOT[k](72)}</div>'
                f'<div><div style="font-size:34px;font-weight:700;color:{BB.H[k][1]}">{t}</div><div style="font-size:24px;color:#41506a;font-family:Nunito;font-weight:600">{d}</div></div></div>' for k, t, d in CARDS)
B["05-portrait-isi-1080x1350"] = (1080, 1350, f"""
<div class="d" style="left:20px;top:16px">{A.sun(110)}</div><div class="d" style="right:-10px;top:24px">{A.rainbow(200)}</div>
{hills(220)}
<div class="d" style="left:60px;right:60px;top:70px;text-align:center">
 <div class="kp" style="font-size:20px;padding:7px 20px">MISI ANAK HEBAT · {PAGES} HALAMAN</div>
 <div class="hl rb" style="font-size:76px;margin-top:12px">{rbw("Apa isinya?")}</div>
</div>
<div class="d" style="left:60px;right:60px;top:250px;bottom:110px;display:grid;grid-template-columns:1fr;grid-template-rows:repeat(6,1fr);gap:16px">{cards}</div>
""")


with sync_playwright() as p:
    br = p.chromium.launch(executable_path=CHROME)
    # cover HD (A4 @300dpi) + mockup texture
    pg = br.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=3.125)
    pg.goto((HERE / "cover.html").as_uri(), wait_until="networkidle"); pg.evaluate("document.fonts.ready")
    tmp = HERE / "cover_raw.png"; pg.screenshot(path=str(tmp), clip={"x": 0, "y": 0, "width": 794, "height": 1123})
    im = Image.open(tmp).convert("RGB").resize((2480, 3508), Image.LANCZOS); im.save(cover_png, optimize=True)
    im.resize((827, 1170), Image.LANCZOS).save(mock_png)
    pg.close()
    for name, (w, h, body) in B.items():
        f = HERE / f"{name}.html"; f.write_text(page(w, h, body), encoding="utf-8")
        pg = br.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
        pg.goto(f.as_uri(), wait_until="networkidle"); pg.evaluate("document.fonts.ready")
        raw = HERE / f"{name}_raw.png"; pg.screenshot(path=str(raw))
        Image.open(raw).convert("RGB").resize((w, h), Image.LANCZOS).save(out / f"{name}.png", optimize=True)
        pg.close()
    br.close()
print("ok", sorted(x.name for x in out.iterdir()))
