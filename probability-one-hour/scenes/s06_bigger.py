import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *


def shirt(color, s=0.55):
    pts = [(-0.5, 0.35), (-0.2, 0.5), (0.2, 0.5), (0.5, 0.35), (0.65, 0.05), (0.42, -0.05), (0.42, -0.55), (-0.42, -0.55), (-0.42, -0.05), (-0.65, 0.05)]
    return Polygon(*[np.array([x, y, 0]) * s for x, y in pts], stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.25)


def trousers(color, s=0.55):
    pts = [(-0.35, 0.55), (0.35, 0.55), (0.42, -0.6), (0.1, -0.6), (0.0, 0.05), (-0.1, -0.6), (-0.42, -0.6)]
    return Polygon(*[np.array([x, y, 0]) * s for x, y in pts], stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.25)


class S06Bigger(PBase):
    CHAPTER = "Counting Bigger Things"

    def construct(self):
        self.at("s096")
        root, lv = Dot(radius=0.08, color=INK2).move_to(LEFT * 5 + UP * 0.1), []
        edges = VGroup()
        pts = [root.get_center()]
        for d in range(4):
            new = []
            for p in pts:
                for s_ in (-1, 1):
                    q = p + RIGHT * 2.2 + UP * s_ * 2.2 / (2 ** (d + 0.4))
                    edges.add(Line(p, q, color=INK2, stroke_width=2)); new.append(q)
            pts = new
        self.add(root)
        self.play(Create(edges, lag_ratio=0.02), run_time=2.0)
        fast = pill("a faster way to count", WARN, 36).move_to(UP * 2.85)
        self.w("s096", "shortcut")
        self.play(edges.animate.set_opacity(0.2), FadeIn(fast), run_time=0.6)
        # s097 shirts & trousers
        self.at("s097")
        self.play(FadeOut(VGroup(edges, root)), run_time=0.4)
        cols_s = [ORANGE_, AQUA, VIOLET]; cols_t = [BLUE_, WARN, INK2, RED_]
        cell = 1.05
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 3, 1], x_length=4 * cell, y_length=3 * cell,
                  axis_config=dict(color=INK2, stroke_width=3, include_tip=False, include_ticks=False)).move_to(RIGHT * 0.9 + DOWN * 0.45)
        sh = VGroup(*[shirt(c).move_to(ax.c2p(0, k + 0.5) + LEFT * 0.6) for k, c in enumerate(cols_s)])
        tr = VGroup(*[trousers(c).move_to(ax.c2p(k + 0.5, 3) + UP * 0.6) for k, c in enumerate(cols_t)])
        self.w("s097", "three")
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in sh], lag_ratio=0.2), run_time=0.8)
        self.w("s097", "four")
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.2) for s in tr], lag_ratio=0.2), run_time=0.8)
        # s098 grid
        self.at("s098")
        cells = VGroup()
        for r in range(3):
            for c in range(4):
                s = Square(cell * 0.88, stroke_width=0, fill_color=CELL_FILL, fill_opacity=1).move_to(ax.c2p(c + 0.5, r + 0.5))
                s.qa_container = True; cells.add(s)
        xt = T("trousers", 26, MUTED).next_to(tr, RIGHT, buff=0.35)
        yt = T("shirt", 26, MUTED).next_to(sh, LEFT, buff=0.3)
        self.play(Create(ax), FadeIn(xt), FadeIn(yt), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(s, scale=0.6) for s in cells], lag_ratio=0.06), run_time=1.2)
        # s099 12
        self.at("s099")
        nums = VGroup(*[T(str(k + 1), 30, INK).move_to(s) for k, s in enumerate(cells)])
        self.play(LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.06), run_time=1.0)
        eq = TB("3 × 4 = 12", 56, WARN).move_to(LEFT * 4.6 + DOWN * 2.0)
        self.w("s099", "three")
        self.play(Write(eq), run_time=0.7)
        # s100 rule
        self.at("s100")
        grid = VGroup(ax, cells, nums, sh, tr, xt, yt)
        self.play(grid.animate.scale(0.62).move_to(LEFT * 4.3 + UP * 0.35), eq.animate.scale(0.75).move_to(LEFT * 4.3 + DOWN * 1.95), run_time=0.7)
        rule = rule_card(["ways for choice 1", "×", "ways for choice 2", "=", "total ways"], WARN, 32, title="the multiplication rule")
        rule.move_to(RIGHT * 2.9 + UP * 0.2)
        self.w("s100", "multiplication")
        self.play(FadeIn(rule, shift=LEFT * 0.3), run_time=0.8)
        # s101 shoes
        self.at("s101")
        self.play(FadeOut(rule), run_time=0.4)
        layer2 = VGroup(ax, cells, nums).copy().set_opacity(0.45)
        self.qa_mute(layer2)
        self.play(layer2.animate.shift(RIGHT * 0.45 + UP * 0.35), run_time=0.7)
        shoes = T("+ 2 pairs of shoes", 32, INK2).move_to(RIGHT * 2.4 + UP * 1.3)
        e2 = TB("12 × 2 = 24", 56, WARN).move_to(RIGHT * 2.4 + DOWN * 0.1)
        self.play(FadeIn(shoes), run_time=0.4)
        self.w("s101", "twelve", nth=1)
        self.play(Write(e2), run_time=0.7)
        # s102 1/24
        self.at("s102")
        one = cells[6].copy().set_fill(AQUA, 0.9)
        self.play(FadeIn(one), run_time=0.4)
        a24 = MathTex(r"{1 \over 24}", font_size=84, color=VIOLET).move_to(RIGHT * 2.4 + DOWN * 1.7)
        self.w("s102", "one", nth=1)
        self.play(Write(a24), run_time=0.7)
        # s103–s108 phone code
        self.at("s103")
        self.clear()
        ph = ic_phone(INK2, 1.6).move_to(LEFT * 5.2 + UP * 0.2)
        slots = VGroup(*[RoundedRectangle(corner_radius=0.15, width=1.4, height=1.6, stroke_color=INK2, stroke_width=3,
                                          fill_color=PANEL, fill_opacity=1) for _ in range(4)]).arrange(RIGHT, buff=0.35).move_to(RIGHT * 0.9 + UP * 0.9)
        for s in slots: s.qa_container = True
        ch = VGroup(*[T("10 choices", 24, MUTED).next_to(s, DOWN, buff=0.2) for s in slots])
        self.play(FadeIn(ph), FadeIn(slots, lag_ratio=0.1), run_time=0.8)
        dg = T("0 1 2 3 4 5 6 7 8 9", 30, INK2).move_to(RIGHT * 0.9 + DOWN * 1.1)
        self.w("s103", "zero")
        self.play(FadeIn(dg), run_time=0.5)
        self.w("s103", "ten")
        self.play(LaggedStart(*[FadeIn(c) for c in ch], lag_ratio=0.15), run_time=0.8)
        self.at("s104")
        tens = VGroup(*[TB("10", 54, WARN).move_to(s) for s in slots])
        for k, w in enumerate(("first", "second", "third", "fourth")):
            self.w("s104", w)
            self.play(FadeIn(tens[k], scale=0.6), run_time=0.35)
        self.at("s105")
        e = TB("10 × 10 × 10 × 10 = 10,000", 52, WARN).move_to(RIGHT * 0.9 + DOWN * 1.1)
        self.play(FadeOut(dg), Write(e), run_time=1.2)
        self.at("s106")
        self.play(FadeOut(ch), e.animate.scale(0.7).move_to(RIGHT * 0.9 + DOWN * 0.45), run_time=0.5)
        f1 = MathTex(r"P(\text{one guess}) = {1 \over 10{,}000}", font_size=60, color=VIOLET).move_to(RIGHT * 0.9 + DOWN * 1.75)
        self.play(Write(f1), run_time=0.9)
        self.at("s107")
        f3 = MathTex(r"P(\text{3 guesses}) = {3 \over 10{,}000}", font_size=60, color=VIOLET).move_to(f1)
        self.play(ReplacementTransform(f1, f3), run_time=0.7)
        self.w("s107", "tiny")
        self.play(Indicate(f3, color=VIOLET), run_time=0.6)
        self.at("s108")
        lk = ic_lock(RED_, 1.0).move_to(ph.get_center() + UP * 0.1)
        tm = T("too many tries", 28, RED_, weight=BOLD).next_to(ph, DOWN, buff=0.3)
        self.play(FadeIn(lk, scale=0.6), FadeIn(tm), run_time=0.6)
        # s109–s110 dice
        self.at("s109")
        self.clear()
        g = DiceGrid(0.55).move_to(RIGHT * 2.8 + DOWN * 0.1)
        dd = VGroup(die(5, ORANGE_, 1.0), die(2, BLUE_, 1.0)).arrange(RIGHT, buff=0.4).move_to(LEFT * 3.6 + UP * 1.0)
        e = TB("6 × 6 = 36", 60, WARN).move_to(LEFT * 3.6 + DOWN * 0.6)
        self.play(FadeIn(dd), run_time=0.5)
        self.w("s109", "six", nth=1)
        self.play(FadeIn(g), Write(e), run_time=1.0)
        self.at("s110")
        ch_ = pill("multiply the choices = size of the world", AQUA, 32).move_to(UP * 2.85)
        self.play(FadeIn(ch_), *g.tint(lambda o, b: True, AQUA, 0.5), run_time=0.8)
        self.finish()
