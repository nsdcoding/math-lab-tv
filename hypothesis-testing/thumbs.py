#!/usr/bin/env python3
"""Two 1280x720 thumbnails (A/B) for YouTube Test & compare, rendered from HTML with Playwright.
Generated stickers (scripts/sticker.py) may be placed with <img src="file://..."> when they add a human element.

Both lead with the keyword headline "HYPOTHESIS TESTING / EXPLAINED VISUALLY" and the colour-coded formula
(typeset with LaTeX -> SVG), plus a picture from the running example:
  A: where you'll use it: Machine Learning, Data Science, Finance and CS tiles with hand-drawn SVG icons,
     plus the hook "15 heads in 20 flips: rigged? p ≈ 0.02".
  B: the fair-coin distribution from the video with the tail from 15 heads up filled in -> ≈ 21 of 1,000 -> p ≈ 0.02.
"""
import json, pathlib, re, subprocess
import numpy as np

HERE = pathlib.Path(__file__).parent
OUT = HERE / "out" / "youtube"; OUT.mkdir(parents=True, exist_ok=True)
MINS = round(json.loads((HERE / "timings.json").read_text())["total"] / 60)
C = dict(bg="#1a1a19", blue="#3987e5", orange="#d95926", aqua="#199e70", violet="#9085e9", warn="#fab219",
         ink="#f0efec", ink2="#c3c2b7", muted="#898781", red="#d03b3b", card="#22221f")

# ── this video ────────────────────────────────────────────────────
HEADLINE = ("HYPOTHESIS<br>TESTING", "EXPLAINED VISUALLY")      # keyword headline (big, 2 lines) + subline
HEADLINE_ONE_LINE = "HYPOTHESIS TESTING"                        # thumbnail B
FORMULA_TEX = (r"{\color{aq}p} = P(\,{\color{wa}\text{data this extreme}}\;\mid\;{\color{bl}H_0}\,)")
FORMULA_LABELS = [("p value", "aqua", 54), ("as extreme or more", "warn", 196), ("fair coin", "blue", 452)]
TILES = [("MACHINE LEARNING", "is model B really better?", "violet", "ICON_ML"),
         ("DATA SCIENCE", "A/B tests that hold up", "aqua", "ICON_DS"),
         ("FINANCE", "real edge, or luck?", "warn", "ICON_FIN"),
         ("COMPUTER SCIENCE", "real speed-up, or noise?", "blue", "ICON_CS")]
HOOK_HTML = ("15 heads in 20 flips. Rigged? <span style='color:#199e70'>p ≈ 0.02</span>")
from math import comb
EXP = [1000 * comb(20, k) / 2 ** 20 for k in range(21)]     # fair coin, 20 flips, friends of 1,000 (as in the video)


def formula_svg(width):
    """Typeset the formula with LaTeX (colours: posterior violet, likelihood aqua, prior yellow)."""
    d = HERE / "build" / "tex"; d.mkdir(parents=True, exist_ok=True)
    (d / "f.tex").write_text(r"""\documentclass[preview,border=2pt]{standalone}
\usepackage{xcolor,amsmath}
\definecolor{bl}{HTML}{3987E5}\definecolor{vio}{HTML}{9085E9}\definecolor{aq}{HTML}{199E70}\definecolor{wa}{HTML}{FAB219}\definecolor{ink}{HTML}{F0EFEC}
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


def chart_svg(w=520, h=250):
    """The fair-coin distribution from the video: bars for 0–20 heads, the tail from 15 up in aqua, a pin at 15."""
    out = [f'<line x1="30" y1="{h}" x2="{w}" y2="{h}" stroke="{C["ink2"]}" stroke-width="3"/>',
           f'<line x1="30" y1="10" x2="30" y2="{h}" stroke="{C["ink2"]}" stroke-width="3"/>']
    bw = (w - 40) / 21
    for k, v in enumerate(EXP):
        x = 35 + k * bw; bh = v / 190 * (h - 20)
        col = C["aqua"] if k >= 15 else C["blue"]
        out.append(f'<rect x="{x + 3:.1f}" y="{h - bh:.1f}" width="{bw - 6:.1f}" height="{bh:.1f}" fill="{col}"/>')
    for k in (0, 5, 10, 15, 20):
        out.append(f'<text x="{35 + k * bw + bw / 2:.1f}" y="{h + 30}" font-size="22" fill="{C["ink2"]}" text-anchor="middle">{k}</text>')
    px = 35 + 15 * bw + bw / 2
    out.append(f'<line x1="{px:.1f}" y1="{h - 95}" x2="{px:.1f}" y2="{h - 8}" stroke="{C["warn"]}" stroke-width="3" stroke-dasharray="6 5"/>')
    out.append(f'<polygon points="{px - 12:.1f},{h - 110} {px + 12:.1f},{h - 110} {px:.1f},{h - 94}" fill="{C["warn"]}"/>')
    out.append(f'<text x="{px:.1f}" y="{h - 120}" font-size="26" font-weight="800" fill="{C["warn"]}" text-anchor="middle">15 heads</text>')
    return "\n".join(out), w + 10, h + 40


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


def ICON_DS(col):   # A/B buttons with a cursor
    return (f'<rect x="4" y="22" width="42" height="30" rx="7" fill="none" stroke="{C["blue"]}" stroke-width="4"/>'
            f'<text x="25" y="45" font-size="22" font-weight="900" fill="{C["blue"]}" text-anchor="middle">A</text>'
            f'<rect x="58" y="22" width="42" height="30" rx="7" fill="none" stroke="{C["orange"]}" stroke-width="4"/>'
            f'<text x="79" y="45" font-size="22" font-weight="900" fill="{C["orange"]}" text-anchor="middle">B</text>'
            f'<polygon points="80,50 80,76 87,69 93,80 98,77 92,67 101,66" fill="{C["ink"]}" stroke="{C["bg"]}" stroke-width="2"/>')


def ICON_FIN(col):  # a rising price line with a question mark
    return (f'<polyline points="6,66 24,52 36,58 54,34 68,42 86,16" fill="none" stroke="{col}" stroke-width="5"/>'
            f'<text x="98" y="40" font-size="34" font-weight="900" fill="{C["ink2"]}" text-anchor="middle">?</text>')


def ICON_CS(col):   # stopwatch
    return (f'<circle cx="52" cy="44" r="28" fill="none" stroke="{col}" stroke-width="5"/>'
            f'<rect x="45" y="6" width="14" height="8" rx="2" fill="{col}"/>'
            f'<line x1="52" y1="44" x2="66" y2="30" stroke="{C["warn"]}" stroke-width="5" stroke-linecap="round"/>')


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
<div class="h" style="position:absolute;left:50px;top:40px;font-size:104px;color:{C['aqua']}">{HEADLINE[0]}</div>
<div class="h" style="position:absolute;left:54px;top:252px;font-size:58px;letter-spacing:-1px;color:{C['warn']}">{HEADLINE[1]}</div>
<div class="card" style="position:absolute;left:50px;top:362px;width:600px;height:{fh + 92:.0f}px">
  <div style="position:absolute;left:62px;top:22px">{f}</div>
  {"".join(f'<div class="lab" style="position:absolute;left:{x}px;bottom:16px;color:{C[col]}">{txt}</div>' for txt, col, x in FORMULA_LABELS)}
</div>
<div style="position:absolute;left:54px;top:{362 + fh + 92 + 26:.0f}px" class="badge">Explained in {MINS} minutes</div>
<div style="position:absolute;left:720px;top:40px;font-size:30px;font-weight:900;letter-spacing:1px;color:{C['ink2']}">WHERE YOU'LL USE IT</div>
<div style="position:absolute;left:720px;top:96px;display:grid;grid-template-columns:250px 250px;gap:18px">
  {"".join(tile(a, b, C[col], globals()[ic]) for a, b, col, ic in TILES)}
</div>
<div style="position:absolute;left:720px;top:536px;font-size:27px;font-weight:800;color:{C['ink']}">
  {HOOK_HTML}</div>"""
    return BASE % dict(C, body=body)


def thumb_b():   # the running example: the fair-coin picture, the tail at 15+ heads, and the p value
    f, fh = formula_svg(420)
    chart, cw, chh = chart_svg()
    body = f"""
<div class="h" style="position:absolute;left:50px;top:30px;font-size:100px;color:{C['aqua']}">{HEADLINE_ONE_LINE}</div>
<div class="h" style="position:absolute;left:54px;top:140px;font-size:54px;letter-spacing:-1px;color:{C['warn']}">{HEADLINE[1]}</div>
<div style="position:absolute;left:54px;top:228px;font-size:30px;font-weight:800">1,000 friends flip a <span style="color:{C['blue']}">fair</span> coin 20 times</div>
<svg style="position:absolute;left:44px;top:280px" width="{cw}" height="{chh}" viewBox="0 0 {cw} {chh}">{chart}</svg>
<div style="position:absolute;left:640px;top:250px;line-height:1.05">
  <div style="font-size:32px;font-weight:800;color:{C['ink2']}">15+ heads by luck alone:</div>
  <div class="h" style="font-size:84px;margin-top:10px;color:{C['aqua']}">≈ 21 of 1,000</div>
  <div style="margin-top:22px;display:flex;align-items:baseline;gap:16px">
    <span class="h" style="font-size:100px;color:{C['aqua']}">p ≈ 0.02</span></div>
  <div class="card" style="margin-top:22px;width:470px;height:{fh + 34:.0f}px;position:relative">
    <div style="position:absolute;left:24px;top:17px">{f}</div></div>
</div>
<div style="position:absolute;left:54px;top:{280 + chh + 22:.0f}px" class="badge">Explained in {MINS} minutes</div>"""
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
