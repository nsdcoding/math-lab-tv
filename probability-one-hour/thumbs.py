#!/usr/bin/env python3
"""Two 1280x720 thumbnails (A/B) for YouTube Test & compare, rendered from HTML with Playwright.
Owner override for this video: no ML / DS / Finance / CS tiles (everyday examples only).
Both lead with the keyword headline "PROBABILITY / EXPLAINED VISUALLY" and the colour-coded counting rule
(typeset with LaTeX -> SVG), plus a real diagram from the running example (two dice):
  A: the 6x6 dice grid with the seven-diagonal lit, "7 beats 12 six times over".
  B: the three magic words NOT / OR / AND and the two-dice "mountain" of totals.
"""
import json, pathlib, re, subprocess
import numpy as np

HERE = pathlib.Path(__file__).parent
OUT = HERE / "out" / "youtube"; OUT.mkdir(parents=True, exist_ok=True)
MINS = round(json.loads((HERE / "timings.json").read_text())["total"] / 60)
C = dict(bg="#1a1a19", blue="#3987e5", orange="#d95926", aqua="#199e70", violet="#9085e9", warn="#fab219",
         ink="#f0efec", ink2="#c3c2b7", muted="#898781", red="#d03b3b", card="#22221f")

# ── per video ─────────────────────────────────────────────────────────
FORMULA_TEX = r"P = \frac{{\color{aq}\text{outcomes you want}}}{{\color{wa}\text{all outcomes}}}"
WAYS = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]


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


def dice_grid_svg(cell):
    """Two-dice grid from the video: total 7 (aqua) and total 12 (orange); axes labelled 1–6."""
    out = []
    pad = 34
    for b in range(1, 7):
        for o in range(1, 7):
            x, y = pad + (o - 1) * cell, (6 - b) * cell
            s = o + b
            col = C["aqua"] if s == 7 else (C["orange"] if s == 12 else "#2c2c29")
            out.append(f'<rect x="{x + 3}" y="{y + 3}" width="{cell - 6}" height="{cell - 6}" rx="6" fill="{col}"/>')
            out.append(f'<text x="{x + cell / 2}" y="{y + cell / 2 + 11}" font-size="30" font-weight="800" text-anchor="middle" fill="{C['ink'] if s in (7, 12) else C['muted']}">{s}</text>')
    for k in range(1, 7):
        out.append(f'<text x="{pad + (k - 0.5) * cell}" y="{6 * cell + 30}" font-size="24" font-weight="800" text-anchor="middle" fill="{C['orange']}">{k}</text>')
        out.append(f'<text x="14" y="{(6 - k + 0.5) * cell + 9}" font-size="24" font-weight="800" text-anchor="middle" fill="{C['blue']}">{k}</text>')
    return "\n".join(out), pad + 6 * cell, 6 * cell + 40


def mountain_svg(w, h):
    bw = w / 11
    out = []
    for i, v in enumerate(WAYS):
        bh = v / 6 * (h - 40)
        col = C["violet"] if i == 5 else C["aqua"]
        out.append(f'<rect x="{i * bw + 4}" y="{h - 40 - bh}" width="{bw - 8}" height="{bh}" rx="4" fill="{col}"/>')
        out.append(f'<text x="{i * bw + bw / 2}" y="{h - 10}" font-size="22" font-weight="700" text-anchor="middle" fill="{C['ink2']}">{i + 2}</text>')
    return "\n".join(out)


BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:1280px;height:720px;background:%(bg)s;overflow:hidden;font-family:'Inter','Inter Display',sans-serif;color:%(ink)s}
.h{font-family:'Inter Display','Inter';font-weight:900;letter-spacing:-2px;line-height:.9}
.badge{display:inline-block;border:3px solid %(aqua)s;color:%(aqua)s;border-radius:14px;padding:8px 18px;font-weight:800;font-size:30px}
.card{background:%(card)s;border:3px solid #3a3a37;border-radius:22px}
.lab{font-size:22px;font-weight:700}
svg text{font-family:'Inter'}
</style></head><body>%(body)s</body></html>"""


def thumb_a():
    f, fh = formula_svg(520)
    grid, gw, gh = dice_grid_svg(60)
    body = f"""
<div class="h" style="position:absolute;left:50px;top:46px;font-size:112px;color:{C['violet']}">PROBABILITY</div>
<div class="h" style="position:absolute;left:54px;top:168px;font-size:58px;letter-spacing:-1px;color:{C['warn']}">EXPLAINED VISUALLY</div>
<div style="position:absolute;left:56px;top:262px;font-size:34px;font-weight:800;color:{C['ink']}">from absolute zero</div>
<div class="card" style="position:absolute;left:50px;top:330px;width:610px;height:{fh + 50:.0f}px">
  <div style="position:absolute;left:44px;top:25px">{f}</div></div>
<div style="position:absolute;left:54px;top:{330 + fh + 50 + 28:.0f}px" class="badge">Explained in {MINS} minutes</div>
<svg style="position:absolute;left:830px;top:40px" width="{gw}" height="{gh}" viewBox="0 0 {gw} {gh}">{grid}</svg>
<div style="position:absolute;left:830px;top:{40 + gh + 14}px;font-size:34px;font-weight:900;line-height:1.15">
  <span style="color:{C['aqua']}">7</span> beats <span style="color:{C['orange']}">12</span><br>
  <span style="color:{C['violet']}">6 times</span> over</div>"""
    return BASE % dict(C, body=body)


def thumb_b():
    f, fh = formula_svg(440)
    body = f"""
<div class="h" style="position:absolute;left:50px;top:40px;font-size:132px;color:{C['violet']}">PROBABILITY</div>
<div class="h" style="position:absolute;left:54px;top:178px;font-size:60px;letter-spacing:-1px;color:{C['warn']}">EXPLAINED VISUALLY</div>
<div style="position:absolute;left:54px;top:282px;display:flex;gap:18px">
  {"".join(f'<div style="border:4px solid {c};color:{c};border-radius:16px;padding:6px 22px;font-size:46px;font-weight:900">{w}</div>' for w, c in (("NOT", C["blue"]), ("OR", C["aqua"]), ("AND", C["orange"])))}
</div>
<div class="card" style="position:absolute;left:50px;top:396px;width:540px;height:{fh + 46:.0f}px">
  <div style="position:absolute;left:50px;top:23px">{f}</div></div>
<div style="position:absolute;left:54px;top:{396 + fh + 46 + 26:.0f}px" class="badge">Explained in {MINS} minutes</div>
<div style="position:absolute;left:690px;top:300px;font-size:30px;font-weight:800;color:{C['ink2']}">two dice: the totals</div>
<svg style="position:absolute;left:690px;top:350px" width="520" height="250" viewBox="0 0 520 250">{mountain_svg(520, 250)}</svg>"""
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
