import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *

RAIN = "#6f8fb8"


def days_grid():
    ax = Axes(x_range=[0, 10, 1], y_range=[0, 10, 1], x_length=4.0, y_length=4.0,
              axis_config=dict(color=INK2, stroke_width=2, include_tip=False, include_ticks=False))
    cells = VGroup()
    for k in range(100):
        r_, c_ = k // 10, k % 10
        s = Square(0.34, stroke_width=0, fill_color=CELL_FILL, fill_opacity=1).move_to(ax.c2p(c_ + 0.5, 9.5 - r_))
        s.k = k; cells.add(s)
    # rainy = first 30 (rows 0-2); late rainy = 15 of them; late dry = 7 of the dry ones
    for s in cells:
        s.rain = s.k < 30
        s.late = (s.k < 30 and s.k % 2 == 0) or (s.k >= 30 and s.k in (33, 42, 51, 66, 75, 84, 97))
    g = VGroup(ax, cells); g.ax, g.cells = ax, cells
    return g


class S19Trees(PBase):
    CHAPTER = "Two Step Trees"

    def construct(self):
        self.at("s299")
        hd = header("chains of events: a tree", INK, 32)
        self.play(FadeIn(hd), run_time=0.5)
        root = Dot(radius=0.1, color=INK2).move_to(LEFT * 5.6 + DOWN * 0.1)
        nR = pill("rain", BLUE_, 32).move_to(LEFT * 2.4 + UP * 1.3)
        nD = pill("dry", WARN, 32).move_to(LEFT * 2.4 + DOWN * 1.5)
        eR = Line(root.get_center(), nR.get_left(), color=INK2, stroke_width=4)
        eD = Line(root.get_center(), nD.get_left(), color=INK2, stroke_width=4)
        leaves = [("late", AQUA, UP * 2.0), ("on time", MUTED, UP * 0.6), ("late", AQUA, DOWN * 0.8), ("on time", MUTED, DOWN * 2.2)]
        L, E = [], []
        for k, (t, c, y) in enumerate(leaves):
            n = pill(t, c, 28).move_to(RIGHT * 1.6 + y)
            par = nR if k < 2 else nD
            L.append(n); E.append(Line(par.get_right(), n.get_left(), color=INK2, stroke_width=3))
        self.play(FadeIn(root), Create(eR), Create(eD), run_time=0.6)
        # s300 rain 3/10
        self.at("s300")
        wR = MathTex(r"\tfrac{3}{10}", font_size=46, color=BLUE_).next_to(eR.get_center(), UL, buff=0.08)
        wD = MathTex(r"\tfrac{7}{10}", font_size=46, color=WARN).next_to(eD.get_center(), DL, buff=0.08)
        self.play(FadeIn(nR), FadeIn(nD), run_time=0.5)
        self.w("s300", "three")
        self.play(Write(wR), Write(wD), run_time=0.7)
        # s301 bus
        self.at("s301")
        ws = [r"\tfrac{1}{2}", r"\tfrac{1}{2}", r"\tfrac{1}{10}", r"\tfrac{9}{10}"]
        W = [MathTex(ws[k], font_size=42, color=AQUA if k % 2 == 0 else MUTED).next_to(E[k].get_center(), UP if k % 2 == 0 else DOWN, buff=0.06) for k in range(4)]
        self.w("s301", "rains")
        self.play(*[Create(E[k]) for k in (0, 1)], *[FadeIn(L[k]) for k in (0, 1)], *[Write(W[k]) for k in (0, 1)], run_time=0.8)
        self.w("s301", "dry")
        self.play(*[Create(E[k]) for k in (2, 3)], *[FadeIn(L[k]) for k in (2, 3)], *[Write(W[k]) for k in (2, 3)], run_time=0.8)
        bus = ic_bus(WARN, 1.1).move_to(RIGHT * 4.9 + UP * 0.3)
        self.play(FadeIn(bus), run_time=0.4)
        # s302 illustration
        self.at("s302")
        il = T("illustration:\nmade-up numbers", 24, MUTED).next_to(bus, DOWN, buff=0.4)
        self.play(FadeIn(il), run_time=0.5)
        tree = VGroup(root, nR, nD, eR, eD, wR, wD, *L, *E, *W)
        # s303 question
        self.at("s303")
        hd2 = header("on a random school day: bus late?", INK, 32)
        self.play(FadeOut(hd), FadeIn(hd2), Indicate(L[0], color=AQUA), Indicate(L[2], color=AQUA), run_time=0.8); hd = hd2
        # s304 100 days
        self.at("s304")
        self.play(FadeOut(VGroup(bus, il)), tree.animate.scale(0.62).move_to(LEFT * 4.1 + UP * 0.1), run_time=0.7)
        dg = days_grid().move_to(RIGHT * 1.5 + UP * 0.25)
        dl = T("100 school days", 26, INK2).next_to(dg, DOWN, buff=0.15)
        self.play(FadeIn(dg), FadeIn(dl), run_time=0.7)
        cells = dg.cells
        # s305 30 rainy
        self.at("s305")
        self.play(*[s.animate.set_fill(RAIN, 0.75) for s in cells if s.rain], run_time=0.7)
        c1 = T("rainy: 30", 28, BLUE_, weight=BOLD).move_to(RIGHT * 4.0 + UP * 1.2, aligned_edge=LEFT)
        self.play(FadeIn(c1), run_time=0.3)
        # s306 15 late
        self.at("s306")
        mk = VGroup(*[Dot(s.get_center(), radius=0.1, color=AQUA) for s in cells if s.rain and s.late])
        self.play(LaggedStart(*[FadeIn(m, scale=0.4) for m in mk], lag_ratio=0.05), run_time=0.9)
        c2 = T("late: 15", 28, AQUA, weight=BOLD).next_to(c1, DOWN, buff=0.25)
        self.play(FadeIn(c2), run_time=0.3)
        # s307 dry 7 late
        self.at("s307")
        self.w("s307", "seventy")
        self.play(*[s.animate.set_fill(WARN, 0.35) for s in cells if not s.rain], run_time=0.6)
        mk2 = VGroup(*[Dot(s.get_center(), radius=0.1, color=AQUA) for s in cells if (not s.rain) and s.late])
        self.w("s307", "seven")
        self.play(LaggedStart(*[FadeIn(m, scale=0.4) for m in mk2], lag_ratio=0.08), run_time=0.7)
        c3 = T("dry & late: 7", 28, AQUA, weight=BOLD).next_to(c2, DOWN, buff=0.25)
        c3.align_to(c1, LEFT); c2.align_to(c1, LEFT)
        self.play(FadeIn(c3), run_time=0.3)
        # s308 22
        self.at("s308")
        res = VGroup(T("late: 15 + 7", 28, VIOLET, weight=BOLD), T("= 22 of 100", 34, VIOLET, weight=BOLD)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(c3, DOWN, buff=0.5).align_to(c1, LEFT)
        self.play(Write(res), run_time=1.1)
        # s309 multiply along paths
        self.at("s309")
        self.play(FadeOut(VGroup(dg, dl, mk, mk2, c1, c2, c3, res)), tree.animate.scale(1 / 0.62).move_to(LEFT * 2.0 + DOWN * 0.1), run_time=0.7)
        p1 = MathTex(r"\tfrac{3}{10} \times \tfrac{1}{2} = \tfrac{15}{100}", font_size=40, color=AQUA).next_to(L[0], RIGHT, buff=0.3)
        p2 = MathTex(r"\tfrac{7}{10} \times \tfrac{1}{10} = \tfrac{7}{100}", font_size=40, color=AQUA).next_to(L[2], RIGHT, buff=0.3)
        self.w("s309", "multiply")
        self.play(Write(p1), run_time=0.8)
        self.play(Write(p2), run_time=0.8)
        sm = MathTex(r"\tfrac{15}{100} + \tfrac{7}{100} = \tfrac{22}{100}", font_size=44, color=VIOLET).move_to(RIGHT * 3.9 + DOWN * 2.1)
        self.w("s309", "add")
        self.play(Write(sm), run_time=0.9)
        # s310 AND along, OR across
        self.at("s310")
        an = pill("AND: along a path", ORANGE_, 28).move_to(LEFT * 4.6 + UP * 2.2)
        orr = pill("OR: across paths", AQUA, 28).move_to(LEFT * 4.6 + DOWN * 2.2)
        self.w("s310", "multiply")
        self.play(FadeIn(an), Indicate(VGroup(eR, E[0]), color=ORANGE_), run_time=0.8)
        self.w("s310", "add")
        self.play(FadeIn(orr), run_time=0.5)
        # s297a check: all leaves add to 100
        self.at("s297a")
        self.play(FadeOut(VGroup(p1, p2, sm)), run_time=0.4)
        vals = ["15", "15", "7", "63"]
        lv = VGroup(*[T(v + " days", 28, INK, weight=BOLD).next_to(L[k], RIGHT, buff=0.35) for k, v in enumerate(vals)])
        for k, w in enumerate(("fifteen", "fifteen", "seven", "sixty")):
            self.w("s297a", w, nth=1 if k == 1 else 0)
            self.play(FadeIn(lv[k], shift=LEFT * 0.2), run_time=0.35)
        tot = MathTex(r"15 + 15 + 7 + 63 = 100\ \checkmark", font_size=44, color=VIOLET).move_to(RIGHT * 3.4 + DOWN * 2.15)
        tot.move_to(UP * 2.85)
        self.w("s297a", "hundred", nth=1)
        self.play(FadeOut(hd), Write(tot), run_time=0.9)
        # s311
        self.at("s311")
        tg = pill("tree = AND along, OR across", VIOLET, 32).move_to(UP * 2.85)
        self.play(FadeOut(tot), FadeIn(tg), run_time=0.5)
        # s312 sneaky
        self.at("s312")
        self.clear()
        q = boxed(T("the bus was late today.\nwas it raining?", 44, INK, line_spacing=1.2), WARN, pad=0.45).move_to(UP * 0.3)
        self.play(FadeIn(q, scale=0.9), run_time=0.7)
        # s313 world = 22 late days
        self.at("s313")
        self.play(FadeOut(q), run_time=0.4)
        dg = days_grid().move_to(LEFT * 2.6 + DOWN * 0.05)
        cells = dg.cells
        for s in cells:
            if s.rain: s.set_fill(RAIN, 0.75)
            else: s.set_fill(WARN, 0.35)
        mk = VGroup(*[Dot(s.get_center(), radius=0.1, color=AQUA) for s in cells if s.late])
        self.play(FadeIn(dg), FadeIn(mk), run_time=0.6)
        self.w("s313", "late")
        self.play(*[s.animate.set_opacity(0.12) for s in cells if not s.late], run_time=0.8)
        wl = T("our world: 22 late days", 32, WARN, weight=BOLD).move_to(RIGHT * 3.6 + UP * 1.4)
        self.play(FadeIn(wl), run_time=0.4)
        # s314 15 rainy
        self.at("s314")
        rl = T("rainy ones: 15", 32, BLUE_, weight=BOLD).next_to(wl, DOWN, buff=0.35)
        self.play(FadeIn(rl), *[Indicate(s, color=BLUE_) for s in cells if s.late and s.rain], run_time=0.8)
        # s315 15/22
        self.at("s315")
        a = MathTex(r"P(\text{rain} \mid \text{late}) = {15 \over 22} \approx 68\%", font_size=50, color=VIOLET).next_to(rl, DOWN, buff=0.5)
        if a.width > 6.6: a.scale_to_fit_width(6.6)
        a.set_x(3.6)
        self.play(Write(a), run_time=1.3)
        # s316 30% -> 68%
        self.at("s316")
        ba = T("before: 30%   →   after the clue: 68%", 32, WARN, weight=BOLD).move_to(RIGHT * 3.6 + DOWN * 1.6)
        if ba.width > 6.0: ba.scale_to_fit_width(6.0)
        self.play(FadeIn(ba), run_time=0.6)
        # s317 next: given
        self.at("s317")
        nx = pill("next: GIVEN THAT", VIOLET, 36).move_to(UP * 2.85)
        self.play(FadeIn(nx, shift=LEFT * 0.3), run_time=0.6)
        self.finish()
