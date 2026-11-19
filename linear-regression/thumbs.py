#!/usr/bin/env python3
"""Two 1280x720 thumbnails (A/B) for YouTube Test & compare, rendered from HTML with Playwright.
Linear regression: keyword headline, y-hat = a + b x colour-coded, tiles (A) and the five-house fit (B).
Generated stickers (scripts/sticker.py) may be placed with <img src="file://..."> when they add a human element.

  A: headline, formula with plain-word labels, where you'll use it (ML, DS, Finance, CS), hook "$260k or $200k? → $230k".
  B: the five houses, best line, misses and their squares; 1,800 sq ft → $230k.
"""
import json, pathlib, re, subprocess

HERE = pathlib.Path(__file__).parent
OUT = HERE / "out" / "youtube"; OUT.mkdir(parents=True, exist_ok=True)
MINS = round(json.loads((HERE / "timings.json").read_text())["total"] / 60)
C = dict(bg="#1a1a19", blue="#3987e5", orange="#d95926", aqua="#199e70", violet="#9085e9", warn="#fab219",
         ink="#f0efec", ink2="#c3c2b7", muted="#898781", red="#d03b3b", card="#22221f")

# ── per video ────────────────────────────────────────────────────
HEADLINE = ("LINEAR<br>REGRESSION", "EXPLAINED VISUALLY")       # keyword headline (big, 2 lines) + subline
HEADLINE_ONE_LINE = "LINEAR REGRESSION"                         # thumbnail B
FORMULA_TEX = r"{\color{vio}\hat{y}} = {\color{wa}a} + {\color{aq}b}\,x"  # colours: vio aq wa ink
FORMULA_LABELS = [("price", "violet", 40), ("start", "warn", 196), ("rate × size", "aqua", 360)]  # (text, colour, x)
TILES = [("MACHINE LEARNING", "the first model you train", "violet", "ICON_ML"),
         ("DATA SCIENCE", "trend lines", "aqua", "ICON_DS"),
         ("FINANCE", "a stock's beta", "warn", "ICON_FIN"),
         ("COMPUTER SCIENCE", "cost per item", "blue", "ICON_CS")]
HOOK_HTML = ("<span style='color:#d95926'>$260k</span> or <span style='color:#3987e5'>$200k</span>? "
             "the line says <span style='color:#9085e9'>$230k</span>")
HOUSES = [(1000, 140), (1500, 220), (2000, 250), (2500, 280), (3000, 360)]


def formula_svg(width):
    """Typeset the formula with LaTeX (colours: posterior violet, likelihood aqua, prior yellow)."""
    d = HERE / "build" / "tex"; d.mkdir(parents=True, exist_ok=True)
    (d / "f.tex").write_text(r"""\documentclass[preview,border=2pt]{standalone}
\usepackage{xcolor,amsmath}
\definecolor{vio}{HTML}{9085E9}\definecolor{aq}{HTML}{199E70}\definecolor{wa}{HTML}{FAB219}\definecolor{ink}{HTML}{F0EFEC}
\begin{document}
\color{ink}$\displaystyle """ + FORMULA_TEX + r"""$
\end{document}
""")
    subprocess.run(["latex", "-interaction=nonstopmode", "f.tex"], cwd=d, check=True, capture_output=True)
    subprocess.run(["dvisvgm", "--no-fonts", "--exact", "f.dvi", "-o", "formula.svg"], cwd=d, check=True, capture_output=True)
    svg = (d / "formula.svg").read_text()
    svg = svg[svg.index("<svg"):]
    vb = [float(x) for x in re.search(r"viewBox='([^']+)'", svg).group(1).split()]
    h = width * vb[3] / vb[2]
    svg = re.sub(r"width='[^']+' height='[^']+'", f"width='{width:.0f}' height='{h:.0f}'", svg, count=1)
    return svg, h


def scatter_svg(w, h):
    """The five houses on axes, the best line (violet), misses (orange) and their squares (aqua)."""
    X = lambda x: 90 + (x / 3500) * (w - 100)
    Y = lambda y: h - 40 - ((y - 100) / 300) * (h - 60)
    out = [f'<line x1="{X(0)}" y1="{Y(100)}" x2="{X(3500)}" y2="{Y(100)}" stroke="{C["ink2"]}" stroke-width="3"/>',
           f'<line x1="{X(0)}" y1="{Y(100)}" x2="{X(0)}" y2="{Y(400)}" stroke="{C["ink2"]}" stroke-width="3"/>']
    for v in (1000, 2000, 3000):
        out.append(f'<text x="{X(v)}" y="{Y(100) + 30}" fill="{C["ink2"]}" font-size="20" text-anchor="middle">{v:,}</text>')
    for v in (100, 200, 300, 400):
        out.append(f'<text x="{X(0) - 10}" y="{Y(v) + 7}" fill="{C["ink2"]}" font-size="20" text-anchor="end">${v}k</text>')
    out.append(f'<line x1="{X(500)}" y1="{Y(100)}" x2="{X(3500)}" y2="{Y(400)}" stroke="{C["violet"]}" stroke-width="6"/>')
    u = (Y(0) - Y(1))
    for x, y in HOUSES:
        g = 50 + 0.1 * x; r = y - g
        if r:
            s = abs(r) * u
            sx = X(x) + 6
            out.append(f'<rect x="{sx}" y="{min(Y(y), Y(g))}" width="{s}" height="{s}" fill="{C["aqua"]}" fill-opacity="0.35" stroke="{C["aqua"]}" stroke-width="2"/>')
            out.append(f'<line x1="{X(x)}" y1="{Y(g)}" x2="{X(x)}" y2="{Y(y)}" stroke="{C["orange"]}" stroke-width="5"/>')
        out.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="9" fill="{C["ink"]}" stroke="{C["bg"]}" stroke-width="2"/>')
    out.append(f'<line x1="{X(1800)}" y1="{Y(100)}" x2="{X(1800)}" y2="{Y(230)}" stroke="{C["ink2"]}" stroke-width="3" stroke-dasharray="7 6"/>')
    out.append(f'<circle cx="{X(1800)}" cy="{Y(230)}" r="10" fill="{C["violet"]}" stroke="{C["ink"]}" stroke-width="2"/>')
    return "\n".join(out)


def tile(title, outcome, col, icon):
    return f"""<div style="width:250px;height:200px;background:{C['card']};border:3px solid {col};border-radius:20px;position:relative;box-sizing:border-box">
  <svg style="position:absolute;left:0;right:0;margin:auto;top:16px" width="110" height="80" viewBox="0 0 110 80">{icon(col)}</svg>
  <div style="position:absolute;left:0;right:0;top:110px;text-align:center;font-size:21px;font-weight:900;white-space:nowrap;letter-spacing:0;color:{col}">{title}</div>
  <div style="position:absolute;left:0;right:0;top:148px;text-align:center;font-size:18px;font-weight:600;white-space:nowrap;color:{C['ink2']}">{outcome}</div>
</div>"""


def ICON_ML(col):   # small neural network: 3 -> 4 -> 2 nodes
    L = [[(15, y) for y in (16, 40, 64)], [(55, y) for y in (10, 30, 50, 70)], [(95, y) for y in (28, 52)]]
    lines = "".join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{C["muted"]}" stroke-width="1.5"/>'
                    for l1, l2 in zip(L, L[1:]) for a in l1 for b in l2)
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="{col}"/>' for l in L for x, y in l)
    return lines + dots


def ICON_DS(col):   # scatter with a trend line
    pts = [(14, 62), (28, 54), (40, 58), (52, 42), (64, 40), (78, 28), (92, 22)]
    return (f'<line x1="6" y1="74" x2="106" y2="74" stroke="{C["ink2"]}" stroke-width="3"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="{C["ink"]}"/>' for x, y in pts)
            + f'<line x1="8" y1="68" x2="102" y2="16" stroke="{col}" stroke-width="4"/>')


def ICON_FIN(col):  # market vs stock: two zig-zag lines, the stock swinging more
    return (f'<polyline points="6,48 24,40 40,46 58,34 76,40 94,28 106,32" fill="none" stroke="{C["ink2"]}" stroke-width="3"/>'
            f'<polyline points="6,52 24,30 40,60 58,18 76,46 94,8 106,20" fill="none" stroke="{col}" stroke-width="4"/>'
            f'<text x="70" y="76" fill="{col}" font-size="20" font-weight="800">β</text>')


def ICON_CS(col):   # run time bars growing with input size
    return "".join(f'<rect x="{10 + 20 * i}" y="{70 - 12 * (i + 1)}" width="14" height="{12 * (i + 1)}" fill="{col}" opacity="0.85"/>'
                   for i in range(5)) + f'<line x1="6" y1="72" x2="110" y2="8" stroke="{C["ink2"]}" stroke-width="3" stroke-dasharray="6 5"/>'


BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:1280px;height:720px;background:%(bg)s;overflow:hidden;font-family:'Inter','Inter Display',sans-serif;color:%(ink)s}
.h{font-family:'Inter Display','Inter';font-weight:900;letter-spacing:-2px;line-height:.9}
.badge{display:inline-block;border:3px solid %(aqua)s;color:%(aqua)s;border-radius:14px;padding:8px 18px;font-weight:800;font-size:30px}
.card{background:%(card)s;border:3px solid #3a3a37;border-radius:22px}
.lab{font-size:22px;font-weight:700}
svg text{font-family:'Inter'}
</style></head><body>%(body)s</body></html>"""


def thumb_a():
    f, fh = formula_svg(470)
    body = f"""
<div class="h" style="position:absolute;left:50px;top:34px;font-size:104px;color:{C['violet']}">{HEADLINE[0]}</div>
<div class="h" style="position:absolute;left:54px;top:236px;font-size:58px;letter-spacing:-1px;color:{C['warn']}">{HEADLINE[1]}</div>
<div class="card" style="position:absolute;left:50px;top:330px;width:600px;height:{fh + 92:.0f}px">
  <div style="position:absolute;left:62px;top:22px">{f}</div>
  {"".join(f'<div class="lab" style="position:absolute;left:{x}px;bottom:16px;color:{C[col]}">{txt}</div>' for txt, col, x in FORMULA_LABELS)}
</div>
<div style="position:absolute;left:54px;top:{330 + fh + 92 + 26:.0f}px" class="badge">Explained in {MINS} minutes</div>
<div style="position:absolute;left:720px;top:40px;font-size:30px;font-weight:900;letter-spacing:1px;color:{C['ink2']}">WHERE YOU'LL USE IT</div>
<div style="position:absolute;left:720px;top:96px;display:grid;grid-template-columns:250px 250px;gap:18px">
  {"".join(tile(a, b, C[col], globals()[ic]) for a, b, col, ic in TILES)}
</div>
<div style="position:absolute;left:720px;top:534px;font-size:27px;font-weight:800;color:{C['ink']}">
  {HOOK_HTML}</div>"""
    return BASE % dict(C, body=body)


def thumb_b():
    f, fh = formula_svg(330)
    W, H = 640, 420
    body = f"""
<div class="h" style="position:absolute;left:50px;top:30px;font-size:96px;color:{C['violet']}">{HEADLINE_ONE_LINE}</div>
<div class="h" style="position:absolute;left:54px;top:132px;font-size:52px;letter-spacing:-1px;color:{C['warn']}">{HEADLINE[1]}</div>
<div style="position:absolute;left:54px;top:212px;font-size:28px;font-weight:800;color:{C['ink2']}">5 house sales, one best line</div>
<svg style="position:absolute;left:30px;top:250px" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{scatter_svg(W, H)}</svg>
<div class="card" style="position:absolute;left:730px;top:220px;width:420px;height:{fh + 40:.0f}px">
  <div style="position:absolute;left:40px;top:20px">{f}</div></div>
<div style="position:absolute;left:740px;top:{220 + fh + 70:.0f}px;line-height:1.1">
  <div style="font-size:30px;font-weight:800;color:{C['orange']}">smallest squared misses</div>
  <div style="font-size:30px;font-weight:800;color:{C['ink']};margin-top:16px">1,800 sq ft →</div>
  <div class="h" style="font-size:104px;color:{C['violet']};margin-top:6px">$230k</div>
</div>
<div style="position:absolute;left:740px;top:560px" class="badge">Explained in {MINS} minutes</div>"""
    return BASE % dict(C, body=body)


if __name__ == "__main__":
    shots = []
    for name, html in (("thumbnail_A.png", thumb_a()), ("thumbnail_B.png", thumb_b())):
        h = HERE / "build" / name.replace(".png", ".html"); h.write_text(html); shots.append((str(h.resolve()), str(OUT / name)))
    js = HERE / "build" / "shot.js"
    js.write_text("""const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1280,height:720}, deviceScaleFactor:1});
for (const [src, dst] of JSON.parse(process.argv[2])) { await p.goto('file://' + src); await p.waitForTimeout(500); await p.screenshot({path: dst}); }
await b.close(); })();""")
    subprocess.run(["node", str(js), json.dumps(shots)], check=True)
    from PIL import Image
    for n in ("A", "B"):
        im = Image.open(OUT / f"thumbnail_{n}.png"); print(n, im.size)
        im.resize((320, 180), Image.LANCZOS).save(HERE / "build" / f"thumb_{n}_phone.png")
