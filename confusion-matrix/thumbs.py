#!/usr/bin/env python3
"""Two 1280x720 thumbnails (A/B) for YouTube Test & compare, rendered from HTML with Playwright.
Both lead with the keyword headline "CONFUSION MATRIX / EXPLAINED VISUALLY" and the colour-coded precision and
recall formulas (typeset with LaTeX -> SVG):
  A: where you'll use it: Machine Learning, Data Science, Finance and CS tiles, plus the hook
     "99% accurate, 0 fraud caught".
  B: Detector A's confusion matrix from the video (90 · 10 · 30 · 9,870) with the precision column and the
     recall row lit up -> precision 75%, recall 90%.
"""
import json, pathlib, re, subprocess
import numpy as np

HERE = pathlib.Path(__file__).parent
OUT = HERE / "out" / "youtube"; OUT.mkdir(parents=True, exist_ok=True)
MINS = round(json.loads((HERE / "timings.json").read_text())["total"] / 60)
C = dict(bg="#1a1a19", blue="#3987e5", orange="#d95926", aqua="#199e70", violet="#9085e9", warn="#fab219",
         ink="#f0efec", ink2="#c3c2b7", muted="#898781", red="#d03b3b", card="#22221f")

# ── per video ────────────────────────────────────────────────────
HEADLINE = ("CONFUSION<br>MATRIX", "EXPLAINED VISUALLY")
HEADLINE_ONE_LINE = "CONFUSION MATRIX"
FORMULA_TEX = (r"{\color{vio}\text{precision}} = \frac{{\color{aq}TP}}{{\color{aq}TP} + {\color{or}FP}}\qquad"
               r"{\color{or}\text{recall}} = \frac{{\color{aq}TP}}{{\color{aq}TP} + {\color{bl}FN}}")
FORMULA_LABELS = [("alarms that were real", "violet", 60), ("real ones caught", "orange", 380)]
TILES = [("MACHINE LEARNING", "judge any classifier", "violet", "ICON_ML"),
         ("DATA SCIENCE", "explain models plainly", "aqua", "ICON_DS"),
         ("FINANCE", "fraud &amp; credit risk", "warn", "ICON_FIN"),
         ("COMPUTER SCIENCE", "spam &amp; malware filters", "blue", "ICON_CS")]
HOOK_HTML = ("<span style='color:#fab219'>99% accurate</span> … and <span style='color:#d03b3b'>0 fraud</span> caught")
A = dict(TP=90, FN=10, FP=30, TN=9870)


def formula_svg(width):
    """Typeset the formula with LaTeX (colours: posterior violet, likelihood aqua, prior yellow)."""
    d = HERE / "build" / "tex"; d.mkdir(parents=True, exist_ok=True)
    (d / "f.tex").write_text(r"""\documentclass[preview,border=2pt]{standalone}
\usepackage{xcolor,amsmath}
\definecolor{vio}{HTML}{9085E9}\definecolor{aq}{HTML}{199E70}\definecolor{wa}{HTML}{FAB219}\definecolor{ink}{HTML}{F0EFEC}\definecolor{or}{HTML}{D95926}\definecolor{bl}{HTML}{3987E5}
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


def grid_svg(cell_w=210, cell_h=130):
    """Detector A's confusion matrix: precision column (violet) and recall row (orange) lit."""
    names = dict(TP=("TRUE POSITIVE", C["aqua"]), FN=("FALSE NEGATIVE", C["blue"]), FP=("FALSE POSITIVE", C["orange"]), TN=("TRUE NEGATIVE", C["aqua"]))
    pos = dict(TP=(0, 0), FN=(1, 0), FP=(0, 1), TN=(1, 1))
    ox, oy = 150, 50
    out = [f'<text x="{ox + cell_w / 2}" y="34" text-anchor="middle" font-size="26" font-weight="800" fill="{C["ink"]}">alarm</text>',
           f'<text x="{ox + cell_w * 1.5}" y="34" text-anchor="middle" font-size="26" font-weight="800" fill="{C["ink"]}">quiet</text>',
           f'<text x="{ox - 16}" y="{oy + cell_h / 2 + 9}" text-anchor="end" font-size="26" font-weight="800" fill="{C["ink"]}">fraud</text>',
           f'<text x="{ox - 16}" y="{oy + cell_h * 1.5 + 9}" text-anchor="end" font-size="26" font-weight="800" fill="{C["ink"]}">fine</text>']
    for k, (c, r) in pos.items():
        x, y = ox + c * cell_w, oy + r * cell_h
        nm, col = names[k]
        out.append(f'<rect x="{x + 5}" y="{y + 5}" width="{cell_w - 10}" height="{cell_h - 10}" rx="14" fill="{C["card"]}" stroke="{col}" stroke-width="3"/>')
        out.append(f'<text x="{x + cell_w / 2}" y="{y + 36}" text-anchor="middle" font-size="17" font-weight="800" fill="{col}">{nm}</text>')
        out.append(f'<text x="{x + cell_w / 2}" y="{y + 96}" text-anchor="middle" font-size="54" font-weight="900" fill="{C["ink"]}">{A[k]:,}</text>')
    out.append(f'<rect x="{ox - 2}" y="{oy - 2}" width="{cell_w + 4}" height="{2 * cell_h + 4}" rx="18" fill="none" stroke="{C["violet"]}" stroke-width="6"/>')
    out.append(f'<rect x="{ox - 9}" y="{oy - 9}" width="{2 * cell_w + 18}" height="{cell_h + 18}" rx="20" fill="none" stroke="{C["orange"]}" stroke-width="6"/>')
    return "\n".join(out), ox + 2 * cell_w + 20, oy + 2 * cell_h + 20


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


def ICON_DS(col):   # prior (wide) narrowing into posterior (tall)
    import math
    def path(mu, sd, peak):
        pts = [(x, 72 - peak * math.exp(-0.5 * ((x - mu) / sd) ** 2)) for x in range(4, 107, 3)]
        return "M" + " L".join(f"{x:.0f},{y:.1f}" for x, y in pts)
    return (f'<line x1="4" y1="72" x2="106" y2="72" stroke="{C["ink2"]}" stroke-width="3"/>'
            f'<path d="{path(62, 22, 26)}" fill="none" stroke="{C["warn"]}" stroke-width="4"/>'
            f'<path d="{path(48, 9, 60)}" fill="none" stroke="{C["violet"]}" stroke-width="4"/>')


def ICON_FIN(col):  # credit card with an alert badge
    return (f'<rect x="6" y="14" width="76" height="50" rx="8" fill="none" stroke="{col}" stroke-width="4"/>'
            f'<rect x="6" y="26" width="76" height="10" fill="{col}" opacity="0.7"/>'
            f'<circle cx="86" cy="58" r="17" fill="{C["red"]}"/>'
            f'<rect x="83.5" y="47" width="5" height="13" rx="2" fill="{C["ink"]}"/><circle cx="86" cy="66" r="3" fill="{C["ink"]}"/>')


def ICON_CS(col):   # envelope with a red flag
    return (f'<rect x="8" y="18" width="70" height="48" rx="5" fill="none" stroke="{col}" stroke-width="4"/>'
            f'<polyline points="8,20 43,46 78,20" fill="none" stroke="{col}" stroke-width="4"/>'
            f'<line x1="92" y1="10" x2="92" y2="70" stroke="{C["ink2"]}" stroke-width="4"/>'
            f'<polygon points="92,10 108,17 92,26" fill="{C["red"]}"/>')


BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:1280px;height:720px;background:%(bg)s;overflow:hidden;font-family:'Inter','Inter Display',sans-serif;color:%(ink)s}
.h{font-family:'Inter Display','Inter';font-weight:900;letter-spacing:-2px;line-height:.9}
.badge{display:inline-block;border:3px solid %(aqua)s;color:%(aqua)s;border-radius:14px;padding:8px 18px;font-weight:800;font-size:30px}
.card{background:%(card)s;border:3px solid #3a3a37;border-radius:22px}
.lab{font-size:22px;font-weight:700}
svg text{font-family:'Inter'}
</style></head><body>%(body)s</body></html>"""


def thumb_a():
    f, fh = formula_svg(560)
    body = f"""
<div class="h" style="position:absolute;left:50px;top:34px;font-size:104px;color:{C['violet']}">{HEADLINE[0]}</div>
<div class="h" style="position:absolute;left:54px;top:236px;font-size:54px;letter-spacing:-1px;color:{C['warn']}">{HEADLINE[1]}</div>
<div class="card" style="position:absolute;left:50px;top:320px;width:620px;height:{fh + 92:.0f}px">
  <div style="position:absolute;left:30px;top:22px">{f}</div>
  {"".join(f'<div class="lab" style="position:absolute;left:{x}px;bottom:16px;color:{C[col]}">{txt}</div>' for txt, col, x in FORMULA_LABELS)}
</div>
<div style="position:absolute;left:54px;top:{320 + fh + 92 + 26:.0f}px" class="badge">Explained in {MINS} minutes</div>
<div style="position:absolute;left:720px;top:40px;font-size:30px;font-weight:900;letter-spacing:1px;color:{C['ink2']}">WHERE YOU'LL USE IT</div>
<div style="position:absolute;left:720px;top:96px;display:grid;grid-template-columns:250px 250px;gap:18px">
  {"".join(tile(a, b, C[col], globals()[ic]) for a, b, col, ic in TILES)}
</div>
<div style="position:absolute;left:720px;top:532px;font-size:30px;font-weight:800;color:{C['ink']}">
  {HOOK_HTML}</div>"""
    return BASE % dict(C, body=body)


def thumb_b():
    f, fh = formula_svg(560)
    grid, gw, gh = grid_svg()
    body = f"""
<div class="h" style="position:absolute;left:50px;top:30px;font-size:104px;color:{C['violet']}">{HEADLINE_ONE_LINE}</div>
<div class="h" style="position:absolute;left:54px;top:140px;font-size:54px;letter-spacing:-1px;color:{C['warn']}">{HEADLINE[1]}</div>
<svg style="position:absolute;left:30px;top:230px" width="{gw}" height="{gh}" viewBox="0 0 {gw} {gh}">{grid}</svg>
<div style="position:absolute;left:650px;top:250px;line-height:1.0">
  <div style="font-size:28px;font-weight:800;color:{C['ink2']}">fraud detector, 10,000 payments</div>
  <div style="margin-top:18px;display:flex;align-items:baseline;gap:16px">
    <span class="h" style="font-size:92px;color:{C['violet']}">75%</span>
    <span style="font-size:32px;font-weight:800;color:{C['violet']}">precision</span></div>
  <div style="margin-top:8px;display:flex;align-items:baseline;gap:16px">
    <span class="h" style="font-size:92px;color:{C['orange']}">90%</span>
    <span style="font-size:32px;font-weight:800;color:{C['orange']}">recall</span></div>
  <div style="margin-top:14px;font-size:30px;font-weight:800;color:{C['warn']}">99.6% accurate. So what?</div>
</div>
<div style="position:absolute;left:54px;top:{230 + gh + 20:.0f}px" class="badge">Explained in {MINS} minutes</div>"""
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
