#!/usr/bin/env python3
"""Two 1280x720 thumbnails (A/B) for YouTube Test & compare, rendered from HTML with Playwright.
Generated stickers (scripts/sticker.py) may be placed with <img src="file://..."> when they add a human element.

Both lead with the keyword headline "PROSECUTOR'S FALLACY / EXPLAINED VISUALLY" and the colour-coded
P(match | innocent) ≠ P(innocent | match) (LaTeX -> SVG):
  A: where you'll use it: Machine Learning, Data Science, Finance and CS tiles, plus the hook "1 in a million match → 8 in 9 innocent".
  B: the city of 8 million (8 blocks, one innocent match each + the culprit) -> 9 people match -> 1 in 9 guilty.
"""
import json, pathlib, re, subprocess
import numpy as np

HERE = pathlib.Path(__file__).parent
OUT = HERE / "out" / "youtube"; OUT.mkdir(parents=True, exist_ok=True)
MINS = round(json.loads((HERE / "timings.json").read_text())["total"] / 60)
C = dict(bg="#1a1a19", blue="#3987e5", orange="#d95926", aqua="#199e70", violet="#9085e9", warn="#fab219",
         ink="#f0efec", ink2="#c3c2b7", muted="#898781", red="#d03b3b", card="#22221f")

# ── per video ─────────────────────────────────────────────────────────
HEADLINE = ("PROSECUTOR'S<br>FALLACY", "EXPLAINED VISUALLY")    # keyword headline (big, 2 lines) + subline
HEAD_SIZE = 86                                                 # px; "PROSECUTOR'S" must fit the left column
HEADLINE_ONE_LINE = "PROSECUTOR'S FALLACY"                     # thumbnail B
HEAD_B_SIZE = 82
FORMULA_TEX = (r"P({\color{wa}\text{match}}\mid{\color{bl}\text{innocent}}) \;{\color{rd}\neq}\; "
               r"{\color{vio}P(}{\color{bl}\text{innocent}}\mathrel{\color{vio}\mid}{\color{wa}\text{match}}{\color{vio})}")
FORMULA_LABELS = [("what the expert gave", "blue", 20), ("what the jury needs", "violet", 300)]
TILES = [("MACHINE LEARNING", "face alerts: 1 in 6 right", "violet", "ICON_ML"),
         ("DATA SCIENCE", "p value ≠ P(no effect)", "aqua", "ICON_DS"),
         ("FINANCE", "fraud flags: 1 in 12 real", "warn", "ICON_FIN"),
         ("COMPUTER SCIENCE", "big searches, false hits", "blue", "ICON_CS")]
HOOK_HTML = ("<span style='color:#fab219'>1 in a million</span> match → <span style='color:#9085e9'>8 in 9 innocent</span>")


def formula_svg(width):
    """Typeset the formula with LaTeX (colours: posterior violet, likelihood aqua, prior yellow)."""
    d = HERE / "build" / "tex"; d.mkdir(parents=True, exist_ok=True)
    (d / "f.tex").write_text(r"""\documentclass[preview,border=2pt]{standalone}
\usepackage{xcolor,amsmath}
\definecolor{vio}{HTML}{9085E9}\definecolor{aq}{HTML}{199E70}\definecolor{wa}{HTML}{FAB219}\definecolor{ink}{HTML}{F0EFEC}\definecolor{bl}{HTML}{3987E5}\definecolor{rd}{HTML}{D03B3B}
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


def city_svg(cell=9, cells=12, gap=14):
    """Eight blocks of a million people; one innocent match lit in each block (warn) and the culprit (orange)."""
    rng = np.random.default_rng(4)
    bw = cells * cell
    out = []
    for k in range(8):
        bx, by = (k % 4) * (bw + gap), (k // 4) * (bw + gap)
        out.append(f'<rect x="{bx - 3}" y="{by - 3}" width="{bw + 6}" height="{bw + 6}" fill="none" stroke="{C["ink2"]}" stroke-width="1.5" rx="3"/>')
        hit = int(rng.integers(cells * cells)); cul = 77 if k == 5 else -1
        for i in range(cells * cells):
            x, y = bx + (i % cells) * cell, by + (i // cells) * cell
            col, op = (C["warn"], 1) if i == hit else (C["orange"], 1) if i == cul else (C["blue"], 0.55)
            out.append(f'<rect x="{x + 1}" y="{y + 1}" width="{cell - 2}" height="{cell - 2}" fill="{col}" opacity="{op}"/>')
    return "\n".join(out), 4 * bw + 3 * gap, 2 * bw + gap


def lineup_svg(r=20, gap=14):
    out = []
    for i in range(9):
        cx = r + 4 + i * (2 * r + gap); col = C["orange"] if i == 6 else C["blue"]
        out.append(f'<circle cx="{cx}" cy="{r + 4}" r="{r}" fill="none" stroke="{C["warn"]}" stroke-width="3"/>')
        out.append(f'<circle cx="{cx}" cy="{r - 3}" r="{r * 0.3:.1f}" fill="{col}"/>')
        out.append(f'<rect x="{cx - r * 0.42:.1f}" y="{r + 3}" width="{r * 0.84:.1f}" height="{r * 0.62:.1f}" rx="5" fill="{col}"/>')
    return "\n".join(out), 9 * (2 * r) + 8 * gap + 8, 2 * r + 8


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
    f, fh = formula_svg(500)
    body = f"""
<div class="h" style="position:absolute;left:50px;top:40px;font-size:{HEAD_SIZE}px;color:{C['violet']}">{HEADLINE[0]}</div>
<div class="h" style="position:absolute;left:54px;top:228px;font-size:58px;letter-spacing:-1px;color:{C['warn']}">{HEADLINE[1]}</div>
<div class="card" style="position:absolute;left:50px;top:330px;width:620px;height:{fh + 92:.0f}px">
  <div style="position:absolute;left:50px;top:22px">{f}</div>
  {"".join(f'<div class="lab" style="position:absolute;left:{x}px;bottom:16px;color:{C[col]}">{txt}</div>' for txt, col, x in FORMULA_LABELS)}
</div>
<div style="position:absolute;left:54px;top:{330 + fh + 92 + 26:.0f}px" class="badge">Explained in {MINS} minutes</div>
<div style="position:absolute;left:720px;top:40px;font-size:30px;font-weight:900;letter-spacing:1px;color:{C['ink2']}">WHERE YOU'LL USE IT</div>
<div style="position:absolute;left:720px;top:96px;display:grid;grid-template-columns:250px 250px;gap:18px">
  {"".join(tile(a, b, C[col], globals()[ic]) for a, b, col, ic in TILES)}
</div>
<div style="position:absolute;left:720px;top:532px;font-size:30px;font-weight:800;color:{C['ink']}">
  {HOOK_HTML}</div>"""
    return BASE % dict(C, body=body)


def thumb_b():
    f, fh = formula_svg(560)
    city, cw, chh = city_svg()
    lu, lw, lh = lineup_svg()
    body = f"""
<div class="h" style="position:absolute;left:50px;top:30px;font-size:{HEAD_B_SIZE}px;color:{C['violet']}">{HEADLINE_ONE_LINE}</div>
<div class="h" style="position:absolute;left:54px;top:122px;font-size:52px;letter-spacing:-1px;color:{C['warn']}">{HEADLINE[1]}</div>
<div class="card" style="position:absolute;left:54px;top:196px;width:{560 + 40}px;height:{fh + 34:.0f}px">
  <div style="position:absolute;left:20px;top:17px">{f}</div></div>
<div style="position:absolute;left:54px;top:{196 + fh + 58:.0f}px;font-size:28px;font-weight:800">a city of <span style="color:{C['aqua']}">8,000,000</span> · a <span style="color:{C['warn']}">1 in a million</span> match</div>
<svg style="position:absolute;left:58px;top:{196 + fh + 108:.0f}px" width="{cw}" height="{chh}" viewBox="-4 -4 {cw + 8} {chh + 8}">{city}</svg>
<div style="position:absolute;left:{58 + cw + 34}px;top:{196 + fh + 150:.0f}px;font-size:64px;color:{C['ink2']}">→</div>
<div style="position:absolute;left:{58 + cw + 120}px;top:{196 + fh + 96:.0f}px;line-height:1.05">
  <div style="font-size:30px;font-weight:800;color:{C['warn']}">9 people match</div>
  <svg style="margin-top:14px" width="{lw * 0.82:.0f}" height="{lh * 0.82:.0f}" viewBox="0 0 {lw} {lh}">{lu}</svg>
  <div style="margin-top:12px;display:flex;align-items:baseline;gap:14px">
    <span class="h" style="font-size:92px;color:{C['violet']}">1 in 9</span>
    <span style="font-size:30px;font-weight:800;color:{C['violet']}">guilty</span></div>
</div>
<div style="position:absolute;left:880px;top:212px" class="badge">Explained in {MINS} minutes</div>"""
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
