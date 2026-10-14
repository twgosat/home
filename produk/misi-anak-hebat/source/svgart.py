"""Original inline-SVG mascots and decorations for "Misi Anak Hebat"."""
import math

INK = "#3b2f2f"
CHEEK = "#ff9eb0"


def _svg(body, vb="0 0 100 100", w=100, h=None, cls=""):
    h = h if h is not None else w
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w}" height="{h}">{body}</svg>'


def face(cx, cy, s, mood="smile"):
    ex = 0.32 * s
    ey = cy - 0.08 * s
    er = 0.075 * s
    out = (f'<ellipse cx="{cx-ex:.1f}" cy="{ey:.1f}" rx="{er:.1f}" ry="{er*1.25:.1f}" fill="{INK}"/>'
           f'<ellipse cx="{cx+ex:.1f}" cy="{ey:.1f}" rx="{er:.1f}" ry="{er*1.25:.1f}" fill="{INK}"/>'
           f'<circle cx="{cx-ex+er*0.35:.1f}" cy="{ey-er*0.45:.1f}" r="{er*0.35:.1f}" fill="#fff"/>'
           f'<circle cx="{cx+ex+er*0.35:.1f}" cy="{ey-er*0.45:.1f}" r="{er*0.35:.1f}" fill="#fff"/>'
           f'<ellipse cx="{cx-ex-0.06*s:.1f}" cy="{cy+0.14*s:.1f}" rx="{0.11*s:.1f}" ry="{0.065*s:.1f}" fill="{CHEEK}" opacity=".8"/>'
           f'<ellipse cx="{cx+ex+0.06*s:.1f}" cy="{cy+0.14*s:.1f}" rx="{0.11*s:.1f}" ry="{0.065*s:.1f}" fill="{CHEEK}" opacity=".8"/>')
    if mood == "sleep":
        out = (f'<path d="M{cx-ex-er*1.3:.1f} {ey:.1f} q{er*1.3:.1f} {er*1.4:.1f} {er*2.6:.1f} 0" stroke="{INK}" stroke-width="{0.04*s:.1f}" fill="none" stroke-linecap="round"/>'
               f'<path d="M{cx+ex-er*1.3:.1f} {ey:.1f} q{er*1.3:.1f} {er*1.4:.1f} {er*2.6:.1f} 0" stroke="{INK}" stroke-width="{0.04*s:.1f}" fill="none" stroke-linecap="round"/>'
               f'<ellipse cx="{cx-ex-0.06*s:.1f}" cy="{cy+0.14*s:.1f}" rx="{0.11*s:.1f}" ry="{0.065*s:.1f}" fill="{CHEEK}" opacity=".8"/>'
               f'<ellipse cx="{cx+ex+0.06*s:.1f}" cy="{cy+0.14*s:.1f}" rx="{0.11*s:.1f}" ry="{0.065*s:.1f}" fill="{CHEEK}" opacity=".8"/>')
    out += (f'<path d="M{cx-0.14*s:.1f} {cy+0.1*s:.1f} q{0.14*s:.1f} {0.16*s:.1f} {0.28*s:.1f} 0" '
            f'stroke="{INK}" stroke-width="{0.045*s:.1f}" fill="{"#e85d6f" if mood=="smile" else "none"}" stroke-linecap="round" stroke-linejoin="round"/>')
    return out


def star_points(cx, cy, R, r, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        rad = R if i % 2 == 0 else r
        a = math.radians(rot + i * 180 / n)
        pts.append(f"{cx+rad*math.cos(a):.1f},{cy+rad*math.sin(a):.1f}")
    return " ".join(pts)


def sun(w=100, cls=""):
    rays = "".join(
        f'<line x1="{50+36*math.cos(math.radians(a)):.1f}" y1="{50+36*math.sin(math.radians(a)):.1f}" '
        f'x2="{50+47*math.cos(math.radians(a)):.1f}" y2="{50+47*math.sin(math.radians(a)):.1f}" '
        f'stroke="#ffb703" stroke-width="6" stroke-linecap="round"/>' for a in range(0, 360, 30))
    return _svg(rays + '<circle cx="50" cy="50" r="30" fill="#ffd23f" stroke="#ffb703" stroke-width="3"/>' + face(50, 52, 30), w=w, cls=cls)


def star(w=100, fill="#ffd23f", stroke="#f4a300", with_face=True, cls=""):
    b = f'<polygon points="{star_points(50,54,46,22)}" fill="{fill}" stroke="{stroke}" stroke-width="4" stroke-linejoin="round"/>'
    if with_face:
        b += face(50, 58, 22)
    return _svg(b, w=w, cls=cls)


def star_outline(w=40, num=None, color="#f4a300"):
    b = f'<polygon points="{star_points(50,54,46,22)}" fill="#fff" stroke="{color}" stroke-width="5" stroke-linejoin="round"/>'
    if num is not None:
        b += f'<text x="50" y="66" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="26" fill="{color}">{num}</text>'
    return _svg(b, w=w)


def clock(w=100, color="#f59e0b", cls=""):
    b = (f'<line x1="30" y1="86" x2="24" y2="96" stroke="{color}" stroke-width="6" stroke-linecap="round"/>'
         f'<line x1="70" y1="86" x2="76" y2="96" stroke="{color}" stroke-width="6" stroke-linecap="round"/>'
         f'<circle cx="24" cy="22" r="12" fill="{color}"/><circle cx="76" cy="22" r="12" fill="{color}"/>'
         f'<rect x="46" y="8" width="8" height="10" rx="3" fill="{color}"/>'
         f'<circle cx="50" cy="56" r="36" fill="#fff" stroke="{color}" stroke-width="7"/>'
         f'<line x1="50" y1="56" x2="50" y2="32" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
         f'<line x1="50" y1="56" x2="64" y2="56" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
         + "".join(f'<circle cx="{50+29*math.cos(math.radians(a)):.1f}" cy="{56+29*math.sin(math.radians(a)):.1f}" r="2" fill="{color}"/>' for a in range(0, 360, 30))
         + face(50, 68, 20))
    return _svg(b, w=w, cls=cls)


def moon(w=100, cls=""):
    b = ('<path d="M62 10 A42 42 0 1 0 92 70 A34 34 0 1 1 62 10 Z" fill="#ffe066" stroke="#f4b400" stroke-width="3" stroke-linejoin="round"/>'
         '<path d="M18 30 Q30 4 58 12 L46 30 Z" fill="#7c83f2"/><circle cx="58" cy="12" r="6" fill="#fff"/>'
         + face(36, 58, 20, "sleep")
         + '<text x="72" y="30" font-family="Fredoka" font-weight="600" font-size="14" fill="#7c83f2">z</text>'
           '<text x="82" y="18" font-family="Fredoka" font-weight="600" font-size="11" fill="#7c83f2">z</text>')
    return _svg(b, w=w, cls=cls)


def apple(w=100, cls=""):
    b = ('<path d="M50 28 C30 14 8 26 10 52 C12 80 32 96 50 88 C68 96 88 80 90 52 C92 26 70 14 50 28 Z" fill="#ef4444" stroke="#c81e1e" stroke-width="3"/>'
         '<path d="M50 28 Q52 14 58 6" stroke="#7c4a1e" stroke-width="5" fill="none" stroke-linecap="round"/>'
         '<path d="M56 16 Q72 2 86 12 Q72 26 56 16 Z" fill="#34c759" stroke="#1f9d48" stroke-width="2"/>'
         '<ellipse cx="28" cy="40" rx="6" ry="10" fill="#fff" opacity=".35"/>' + face(50, 58, 24))
    return _svg(b, w=w, cls=cls)


def drop(w=100, cls=""):
    b = ('<path d="M50 6 C50 6 16 46 16 66 A34 34 0 0 0 84 66 C84 46 50 6 50 6 Z" fill="#5ab4f0" stroke="#2b8fd6" stroke-width="3"/>'
         '<ellipse cx="34" cy="56" rx="5" ry="10" fill="#fff" opacity=".5"/>' + face(50, 70, 22))
    return _svg(b, w=w, cls=cls)


def book(w=100, color="#8b5cf6", cls=""):
    b = (f'<rect x="16" y="12" width="70" height="80" rx="8" fill="{color}" stroke="#5b34c9" stroke-width="3"/>'
         '<rect x="78" y="18" width="10" height="68" rx="3" fill="#fff" stroke="#5b34c9" stroke-width="2"/>'
         '<rect x="16" y="12" width="12" height="80" rx="6" fill="#5b34c9" opacity=".35"/>'
         '<rect x="36" y="22" width="40" height="12" rx="6" fill="#fff" opacity=".9"/>' + face(53, 64, 24).replace(INK, "#fff").replace("#e85d6f", "#ffd1dc"))
    return _svg(b, w=w, cls=cls)


def ball(w=100, cls=""):
    b = ('<circle cx="50" cy="52" r="42" fill="#fff" stroke="#2b7de9" stroke-width="5"/>'
         '<polygon points="50,14 62,24 58,38 42,38 38,24" fill="#2b7de9"/>'
         '<polygon points="14,44 24,40 30,52 24,64 13,60" fill="#2b7de9"/>'
         '<polygon points="86,44 76,40 70,52 76,64 87,60" fill="#2b7de9"/>' + face(50, 62, 22))
    return _svg(b, w=w, cls=cls)


def heart(w=100, fill="#ec4899", stroke="#c0267a", with_face=True, cls=""):
    b = f'<path d="M50 90 C14 66 6 44 14 28 C22 12 44 12 50 30 C56 12 78 12 86 28 C94 44 86 66 50 90 Z" fill="{fill}" stroke="{stroke}" stroke-width="4" stroke-linejoin="round"/>'
    if with_face:
        b += face(50, 50, 22)
    return _svg(b, w=w, cls=cls)


def mosque(w=100, cls=""):
    b = ('<rect x="20" y="52" width="60" height="40" rx="4" fill="#d9f2e6" stroke="#0f9d78" stroke-width="3"/>'
         '<path d="M24 54 Q24 22 50 16 Q76 22 76 54 Z" fill="#10b981" stroke="#0f9d78" stroke-width="3"/>'
         '<line x1="50" y1="16" x2="50" y2="6" stroke="#0f9d78" stroke-width="3"/>'
         '<path d="M53 2 A5 5 0 1 0 53 10 A4 4 0 1 1 53 2 Z" fill="#f4b400"/>'
         '<rect x="6" y="34" width="10" height="58" rx="3" fill="#10b981" stroke="#0f9d78" stroke-width="2"/>'
         '<rect x="84" y="34" width="10" height="58" rx="3" fill="#10b981" stroke="#0f9d78" stroke-width="2"/>'
         '<path d="M42 92 V74 Q50 64 58 74 V92 Z" fill="#0f9d78"/>')
    return _svg(b, w=w, cls=cls)


def hands(w=100, cls=""):
    """praying/open hands with a small heart — neutral for every religion"""
    b = ('<path d="M50 94 L50 46 Q46 26 36 18 Q30 14 28 22 L34 48 L22 30 Q16 26 14 34 L30 72 Q36 88 50 94 Z" fill="#ffd7b5" stroke="#d9925f" stroke-width="3" stroke-linejoin="round"/>'
         '<path d="M50 94 L50 46 Q54 26 64 18 Q70 14 72 22 L66 48 L78 30 Q84 26 86 34 L70 72 Q64 88 50 94 Z" fill="#ffd7b5" stroke="#d9925f" stroke-width="3" stroke-linejoin="round"/>'
         '<path d="M50 30 C42 22 36 26 38 32 C40 38 50 42 50 42 C50 42 60 38 62 32 C64 26 58 22 50 30 Z" fill="#10b981"/>')
    return _svg(b, w=w, cls=cls)


def carrot(w=100, cls=""):
    b = ('<path d="M40 14 Q30 2 22 8 Q30 14 38 20 M50 12 Q50 0 58 2 Q56 12 52 20 M60 16 Q72 6 78 14 Q68 18 58 22" stroke="#22a55a" stroke-width="7" fill="none" stroke-linecap="round"/>'
         '<path d="M26 26 Q50 14 74 26 L54 94 Q50 100 46 94 Z" fill="#fb8c2b" stroke="#d96a0c" stroke-width="3" stroke-linejoin="round"/>'
         + face(50, 44, 20))
    return _svg(b, w=w, cls=cls)


def broccoli(w=100, cls=""):
    b = ('<rect x="38" y="56" width="24" height="38" rx="10" fill="#b7e07a" stroke="#6fa832" stroke-width="3"/>'
         + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#34a853" stroke="#1e7e34" stroke-width="3"/>' for x, y, r in
                   [(28, 40, 18), (72, 40, 18), (50, 26, 20), (38, 52, 16), (62, 52, 16), (50, 46, 20)])
         + face(50, 46, 18))
    return _svg(b, w=w, cls=cls)


def glass(w=22, color="#5ab4f0"):
    b = f'<path d="M14 10 L86 10 L76 92 Q75 96 70 96 L30 96 Q25 96 24 92 Z" fill="#fff" stroke="{color}" stroke-width="7" stroke-linejoin="round"/>'
    return _svg(b, w=w)


def cloud(w=120, fill="#ffffff", cls=""):
    b = f'<path d="M20 60 A16 16 0 0 1 30 32 A22 22 0 0 1 70 26 A18 18 0 0 1 100 46 A14 14 0 0 1 98 72 L22 72 A12 12 0 0 1 20 60 Z" fill="{fill}"/>'
    return _svg(b, vb="0 0 120 80", w=w, h=w * 80 / 120, cls=cls)


def trophy(w=100, cls=""):
    b = ('<path d="M26 14 H74 V40 A24 24 0 0 1 26 40 Z" fill="#ffd23f" stroke="#f4a300" stroke-width="3"/>'
         '<path d="M26 20 H12 Q10 42 30 46 M74 20 H88 Q90 42 70 46" stroke="#f4a300" stroke-width="5" fill="none"/>'
         '<rect x="44" y="62" width="12" height="14" fill="#f4a300"/><rect x="30" y="76" width="40" height="14" rx="4" fill="#ffb703" stroke="#f4a300" stroke-width="3"/>'
         f'<polygon points="{star_points(50,36,12,5.5)}" fill="#fff"/>')
    return _svg(b, w=w, cls=cls)


def medal(w=100, cls=""):
    b = ('<path d="M30 4 L46 44 L38 48 L20 8 Z" fill="#2b7de9"/><path d="M70 4 L54 44 L62 48 L80 8 Z" fill="#ef4444"/>'
         '<circle cx="50" cy="64" r="30" fill="#ffd23f" stroke="#f4a300" stroke-width="5"/>'
         f'<polygon points="{star_points(50,66,18,8)}" fill="#fff" stroke="#f4a300" stroke-width="2"/>')
    return _svg(b, w=w, cls=cls)


def kid(w=160, girl=False, shirt="#2b7de9", cls=""):
    """Simple chibi kid, waving. viewBox 0 0 100 130"""
    hair = "#4a2c1a"
    skin = "#ffd7b5"
    b = ""
    if girl:
        b += f'<path d="M18 46 Q14 90 26 92 L74 92 Q86 90 82 46 Z" fill="{hair}"/>'
    # body
    b += (f'<path d="M30 84 Q30 72 50 72 Q70 72 70 84 L72 118 L28 118 Z" fill="{shirt}"/>'
          f'<path d="M30 86 Q16 78 12 60" stroke="{skin}" stroke-width="9" fill="none" stroke-linecap="round"/>'
          f'<circle cx="12" cy="58" r="6" fill="{skin}"/>'
          f'<path d="M70 86 Q80 100 78 112" stroke="{skin}" stroke-width="9" fill="none" stroke-linecap="round"/>'
          f'<rect x="34" y="116" width="12" height="12" rx="4" fill="#5b4636"/><rect x="54" y="116" width="12" height="12" rx="4" fill="#5b4636"/>'
          f'<circle cx="50" cy="46" r="30" fill="{skin}"/>')
    if girl:
        b += (f'<path d="M20 44 Q22 14 50 14 Q78 14 80 44 Q66 30 50 32 Q34 30 20 44 Z" fill="{hair}"/>'
              f'<circle cx="74" cy="22" r="7" fill="#ec4899"/><circle cx="82" cy="18" r="5" fill="#ec4899"/>')
    else:
        b += f'<path d="M20 42 Q18 14 48 14 Q80 12 80 40 Q70 26 56 30 Q60 22 50 24 Q40 30 20 42 Z" fill="{hair}"/>'
    b += face(50, 50, 22)
    return _svg(b, vb="0 0 100 130", w=w, h=w * 1.3, cls=cls)


def isi_piringku(w=300):
    """Isi Piringku (Kemenkes): 1/2 plate = sayur (2/3) + buah (1/3); 1/2 = makanan pokok (2/3) + lauk (1/3)."""
    cx, cy, r = 150, 150, 112
    parts = [  # (fraction of plate, colour, label)
        (1 / 3, "#7cc96b", "Sayur"),
        (1 / 6, "#ffb84d", "Buah"),
        (1 / 6, "#f08a7a", "Lauk pauk"),
        (1 / 3, "#ffe08a", "Makanan pokok"),
    ]
    a0 = -90.0
    segs, labels = "", ""
    for frac, col, lab in parts:
        a1 = a0 + frac * 360
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
        large = 1 if frac > 0.5 else 0
        segs += f'<path d="M{cx} {cy} L{x0:.1f} {y0:.1f} A{r} {r} 0 {large} 1 {x1:.1f} {y1:.1f} Z" fill="{col}" stroke="#fff" stroke-width="4"/>'
        am = math.radians((a0 + a1) / 2)
        lx, ly = cx + r * 0.6 * math.cos(am), cy + r * 0.6 * math.sin(am)
        labels += (f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="17" fill="#3b2f2f">{lab}</text>')
        a0 = a1
    plate = (f'<circle cx="{cx}" cy="{cy}" r="{r+22}" fill="#fff" stroke="#cfd8dc" stroke-width="4"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r+6}" fill="none" stroke="#e3e9ec" stroke-width="3"/>')
    return _svg(plate + segs + labels, vb="0 0 300 300", w=w)


def rainbow(w=200, cls=""):
    cols = ["#ef4444", "#f59e0b", "#ffd23f", "#34c759", "#2b7de9", "#8b5cf6"]
    b = "".join(f'<path d="M{10+i*9} 100 A{90-i*9} {90-i*9} 0 0 1 {190-i*9} 100" stroke="{c}" stroke-width="9" fill="none"/>' for i, c in enumerate(cols))
    return _svg(b, vb="0 0 200 104", w=w, h=w * 104 / 200, cls=cls)


def sparkle(w=24, color="#ffd23f"):
    return _svg(f'<path d="M50 4 Q56 44 96 50 Q56 56 50 96 Q44 56 4 50 Q44 44 50 4 Z" fill="{color}"/>', w=w)


MASCOT = {
    1: lambda w=150: clock(w),
    2: lambda w=150: hands(w),
    3: lambda w=150: ball(w),
    4: lambda w=150: apple(w),
    5: lambda w=150: book(w),
    6: lambda w=150: heart(w),
    7: lambda w=150: moon(w),
}
