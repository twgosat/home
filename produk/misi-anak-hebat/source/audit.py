import sys, json, pathlib, logging
logging.disable(logging.WARNING)
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
JS = r"""() => {
 const out = [];
 const pages = [...document.querySelectorAll('section.page')];
 const R = el => el.getBoundingClientRect();
 const inter = (a,b) => Math.max(0, Math.min(a.right,b.right)-Math.max(a.left,b.left)) * Math.max(0, Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top));
 pages.forEach((pg, i) => {
   const inner = pg.querySelector('.inner'); if (!inner) return;
   const ir = R(inner), pr = R(pg);
   const foot = pg.querySelector('.foot'); const fr = foot ? R(foot) : null;
   // 1 elements outside inner / page
   inner.querySelectorAll('*').forEach(el => {
     if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') return;
     const r = R(el); if (r.width === 0 || r.height === 0) return;
     if (r.right > ir.right + 2 || r.left < ir.left - 2 || r.bottom > ir.bottom + 2)
       out.push([i, 'outside-inner', el.tagName + '.' + el.className, Math.round(r.left-ir.left), Math.round(ir.right-r.right), Math.round(ir.bottom-r.bottom)]);
     if (fr && inter(r, fr) > 4 && !el.closest('.foot')) out.push([i, 'hits-footer', el.tagName + '.' + el.className]);
     const cs = getComputedStyle(el);
     if (el.scrollWidth > el.clientWidth + 2 && cs.overflow !== 'visible' && el.clientWidth > 0) out.push([i, 'h-clipped', el.tagName + '.' + el.className, (el.textContent||'').slice(0,40)]);
   });
   // 2 text leaves overlapping each other
   const leaves = [...inner.querySelectorAll('*')].filter(el => !el.closest('svg') && [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()));
   const rs = leaves.map(el => { const rg = document.createRange(); rg.selectNodeContents(el); return [...rg.getClientRects()]; });
   for (let a = 0; a < leaves.length; a++) for (let b = a+1; b < leaves.length; b++) {
     if (leaves[a].contains(leaves[b]) || leaves[b].contains(leaves[a])) continue;
     for (const ra of rs[a]) for (const rb of rs[b]) if (inter(ra, rb) > 12 && (Math.min(ra.bottom,rb.bottom)-Math.max(ra.top,rb.top)) > 0.35*Math.min(ra.height,rb.height) && (Math.min(ra.right,rb.right)-Math.max(ra.left,rb.left)) > 2) { out.push([i, 'text-overlap', (leaves[a].textContent||'').trim().slice(0,30), (leaves[b].textContent||'').trim().slice(0,30)]); }
   }
   // 3 deco over text
   pg.querySelectorAll('.deco').forEach(d => { const dr = R(d);
     leaves.forEach((el, k) => rs[k].forEach(r => { if (inter(dr, r) > 20) out.push([i, 'deco-over-text', (el.textContent||'').trim().slice(0,30)]); })); });
   // 4 headings wrapping
   inner.querySelectorAll('h1,h2,h3').forEach(h => { const lh = parseFloat(getComputedStyle(h).fontSize);
     const lines = h.getClientRects(); const rg = document.createRange(); rg.selectNodeContents(h);
     const tops = new Set([...rg.getClientRects()].map(r => Math.round(r.top/4)));
     if (tops.size > 1 && h.tagName === 'H1') out.push([i, 'h1-wraps', h.textContent.slice(0,40), tops.size]);
     if (tops.size > 2) out.push([i, 'heading-3lines', h.textContent.slice(0,40)]); });
   // 5 aligned siblings: sig + grid children tops/heights
   const sigs = [...pg.querySelectorAll('.sig')].map(R);
   for (let a = 0; a < sigs.length; a++) for (let b = a+1; b < sigs.length; b++)
     if (Math.abs(sigs[a].top - sigs[b].top) > 1 && Math.abs(sigs[a].top - sigs[b].top) < 80) out.push([i, 'sig-misaligned', Math.round(sigs[a].top - sigs[b].top)]);
   inner.querySelectorAll('.grid,.cards3').forEach(g => { const kids = [...g.children].map(R);
     const rows = {}; kids.forEach(r => { const k = Math.round(r.top); (rows[k] = rows[k] || []).push(r); });
     const tops = kids.map(r=>r.top); 
     // children that start within 30px of each other should share top & height
     for (let a = 0; a < kids.length; a++) for (let b = a+1; b < kids.length; b++) {
       const dt = Math.abs(kids[a].top - kids[b].top);
       if (dt > 1 && dt < 30) out.push([i, 'grid-top-mismatch', g.className, Math.round(dt)]);
       if (dt <= 1 && Math.abs(kids[a].height - kids[b].height) > 2) out.push([i, 'grid-height-mismatch', g.className, Math.round(kids[a].height), Math.round(kids[b].height)]);
     }});
   // 6 empty space at bottom of inner
   const kids = [...inner.children].filter(e => !e.classList.contains('deco'));
   const lastBottom = Math.max(...kids.map(e => R(e).bottom));
   const gap = ir.bottom - lastBottom; if (gap > 60) out.push([i, 'bottom-gap', Math.round(gap)]);
 });
 return out;
}"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    pg = b.new_page(viewport={"width": 794, "height": 1123})
    pg.goto((HERE / "book.html").as_uri(), wait_until="networkidle"); pg.evaluate("document.fonts.ready")
    pg.emulate_media(media="print")
    res = pg.evaluate(JS)
    b.close()
seen = set()
for r in res:
    k = json.dumps(r)
    if k in seen: continue
    seen.add(k); print(r)
print("total", len(seen))
