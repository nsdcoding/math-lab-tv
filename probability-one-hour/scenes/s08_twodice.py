import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *

WAYS = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]


class S08TwoDice(PBase):
    CHAPTER = "Two Dice"

    def construct(self):
        self.at("s126")
        cy = pill("you need: 12", ORANGE_, 36); cf = pill("friend needs: 7", BLUE_, 36)
        VGroup(cy, cf).arrange(RIGHT, buff=1.2).move_to(UP * 0.3)
        self.play(FadeIn(cy, shift=UP * 0.2), FadeIn(cf, shift=UP * 0.2), run_time=0.7)
        # s127 two dice
        self.at("s127")
        do, db = die(3, ORANGE_, 1.3), die(5, BLUE_, 1.3)
        VGroup(do, db).arrange(RIGHT, buff=1.0).move_to(DOWN * 0.3)
        self.play(VGroup(cy, cf).animate.move_to(UP * 2.85), run_time=0.5)
        self.w("s127", "orange")
        self.play(FadeIn(do, shift=DOWN * 0.5), run_time=0.4)
        self.w("s127", "blue")
        self.play(FadeIn(db, shift=DOWN * 0.5), run_time=0.4)
        # s128 axes faces
        self.at("s128")
        g = DiceGrid(0.66, fs=28).move_to(LEFT * 2.6 + UP * 0.1)
        self.play(FadeOut(VGroup(do, db)), Create(g.ax), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.2) for x in g.xl], lag_ratio=0.08), FadeIn(g.titles[0]), run_time=0.8)
        self.w("s128", "blue")
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in g.yl], lag_ratio=0.08), FadeIn(g.titles[1]), run_time=0.8)
        # s129 grid
        self.at("s129")
        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in g.sq], lag_ratio=0.02), run_time=1.6)
        eo = T("every square = one outcome", 28, INK2).move_to(RIGHT * 3.7 + UP * 1.2)
        self.w("s129", "every")
        self.play(FadeIn(eo), run_time=0.5)
        # s130 (3,5)
        self.at("s130")
        self.play(g.c(3, 5).animate.set_fill(VIOLET, 0.9), run_time=0.4)
        l35 = T("orange 3, blue 5", 32, VIOLET, weight=BOLD).move_to(RIGHT * 3.8 + UP * 0.4)
        self.play(FadeIn(l35), Indicate(g.xl[2], color=ORANGE_), Indicate(g.yl[4], color=BLUE_), run_time=0.8)
        # s131 36
        self.at("s131")
        e36 = TB("6 × 6 = 36", 60, WARN).move_to(RIGHT * 3.8 + DOWN * 0.7)
        self.w("s131", "six", nth=2)
        self.play(Write(e36), run_time=0.9)
        # s132 (5,3) different
        self.at("s132")
        self.play(FadeOut(VGroup(eo, e36)), run_time=0.3)
        self.w("s132", "five")
        self.play(g.c(5, 3).animate.set_fill(AQUA, 0.9), run_time=0.4)
        l53 = T("orange 5, blue 3", 32, AQUA, weight=BOLD).next_to(l35, DOWN, buff=0.35)
        nt = pill("two different squares", WARN, 32).next_to(l53, DOWN, buff=0.5)
        self.play(FadeIn(l53), run_time=0.4)
        self.w("s132", "two")
        self.play(FadeIn(nt), run_time=0.4)
        # s133 equally likely
        self.at("s133")
        self.play(FadeOut(VGroup(l35, l53, nt)), *g.reset(), run_time=0.4)
        el = T("all 36 equally likely", 34, WARN, weight=BOLD).move_to(RIGHT * 3.8 + UP * 0.6)
        self.play(*g.tint(lambda o, b: True, WARN, 0.45), FadeIn(el), run_time=0.6)
        self.play(*g.reset(), run_time=0.5)
        # s134 sums
        self.at("s134")
        self.play(FadeOut(el), run_time=0.3)
        sums = g.sums()
        order = sorted(range(36), key=lambda i: (-sums[i].ob[1], sums[i].ob[0]))
        self.play(LaggedStart(*[FadeIn(sums[i]) for i in order], lag_ratio=0.03), run_time=2.2)
        # s135 diagonals
        self.at("s135")
        for s_ in (4, 7, 10):
            d = g.where(lambda o, b, s_=s_: o + b == s_)
            self.play(d.animate.set_fill(AQUA, 0.6), run_time=0.3)
            self.play(d.animate.set_fill(CELL_FILL, 1), run_time=0.25)
        # s136–s138 twelve
        self.at("s136")
        q = T("total of 12?", 40, ORANGE_, weight=BOLD).move_to(RIGHT * 3.8 + UP * 1.9)
        self.play(FadeIn(q), run_time=0.4)
        self.at("s137")
        self.w("s137", "one")
        self.play(g.c(6, 6).animate.set_fill(AQUA, 0.9), run_time=0.5)
        self.play(Indicate(g.num(6, 6), scale_factor=1.6), run_time=0.7)
        self.at("s138")
        f12 = colfrac(1, 36, fs=68).next_to(q, DOWN, buff=0.3)
        self.play(Write(f12), run_time=0.7)
        self.play(f12.animate.set_color(VIOLET), run_time=0.4)
        # s139–s141 seven
        self.at("s139")
        q7 = T("total of 7?", 40, BLUE_, weight=BOLD).move_to(RIGHT * 3.8 + DOWN * 0.35)
        self.play(FadeIn(q7), run_time=0.4)
        self.at("s140")
        ctr = TB("0", 60, AQUA).next_to(q7, DOWN, buff=0.5)
        self.add(ctr)
        words = ["one", "two", "three", "four", "five", "six"]
        for k in range(6):
            o = k + 1
            self.w("s140", words[k], nth=0 if k < 3 else 1) if k >= 3 else self.w("s140", words[k])
            self.play(g.c(o, 7 - o).animate.set_fill(AQUA, 0.9), Transform(ctr, TB(str(k + 1), 60, AQUA).move_to(ctr)), run_time=0.3)
        self.at("s141")
        f7 = MathTex(r"{6 \over 36}", "=", r"{1 \over 6}", font_size=68, color=VIOLET).next_to(q7, DOWN, buff=0.35)
        self.play(ReplacementTransform(ctr, f7[0]), run_time=0.5)
        self.w("s141", "sixth")
        self.play(Write(f7[1:]), run_time=0.6)
        # s142 6 ways vs 1 way
        self.at("s142")
        w6 = pill("7: six ways", BLUE_, 34).move_to(RIGHT * 3.8 + UP * 0.6)
        w1 = pill("12: one way", ORANGE_, 34).next_to(w6, DOWN, buff=0.4)
        self.play(FadeOut(VGroup(q, f12, q7, f7)), FadeIn(w6), run_time=0.6)
        self.w("s142", "twelve")
        self.play(FadeIn(w1), run_time=0.5)
        x6 = TB("6× more likely", 44, VIOLET).next_to(w1, DOWN, buff=0.6)
        self.w("s142", "six", nth=1)
        self.play(FadeIn(x6, scale=0.8), run_time=0.6)
        # s143
        self.at("s143")
        mw = pill("most ways to be made", AQUA, 32).move_to(RIGHT * 3.8 + UP * 1.7)
        self.play(FadeOut(VGroup(w6, w1, x6)), FadeIn(mw), run_time=0.5)
        self.play(Indicate(g.where(lambda o, b: o + b == 7), color=AQUA, scale_factor=1.08), run_time=1.0)
        # s144–s148 build the chart
        self.at("s144")
        self.play(FadeOut(mw), *g.reset(), run_time=0.4)
        grid = VGroup(g, sums)
        self.play(grid.animate.scale(0.62).move_to(LEFT * 4.9 + UP * 0.2), FadeOut(VGroup(cy, cf)), run_time=0.7)
        bx = bar_axes([str(s) for s in range(2, 13)], 6, 1, 7.4, 3.9, "total", "number of ways")
        bx.move_to(RIGHT * 2.2 + DOWN * 0.05)
        self.play(FadeIn(bx), run_time=0.6)
        stacks = []
        for i, s_ in enumerate(range(2, 13)):
            col = VGroup()
            for k in range(WAYS[i]):
                sq = Square(bx.ax.c2p(0, 1)[1] - bx.ax.c2p(0, 0)[1], stroke_width=0, fill_color=AQUA, fill_opacity=0.85)
                sq.scale(0.86).move_to(bx.ax.c2p(i + 1, k + 0.5))
                col.add(sq)
            stacks.append(col)
        self.at("s145")
        wd = ["two", "three", "four", "five", "six", "seven"]
        for i in range(6):
            self.w("s145", wd[i])
            src = g.where(lambda o, b, s_=i + 2: o + b == s_)
            self.play(ReplacementTransform(src.copy(), stacks[i]), run_time=0.5)
        self.at("s146")
        wd = ["eight", "nine", "ten", "eleven", "twelve"]
        for i in range(6, 11):
            self.w("s146", wd[i - 6])
            src = g.where(lambda o, b, s_=i + 2: o + b == s_)
            self.play(ReplacementTransform(src.copy(), stacks[i]), run_time=0.45)
        self.at("s147")
        top = VMobject(stroke_color=WARN, stroke_width=5).set_points_as_corners(
            [bx.ax.c2p(0.5, 0)] + [bx.ax.c2p(i + 1, WAYS[i]) for i in range(11)] + [bx.ax.c2p(11.5, 0)])
        top.qa_ignore = True
        self.play(Create(top), run_time=1.0)
        pk = T("peak: 7", 30, WARN, weight=BOLD).next_to(bx.ax.c2p(6, 6), UP, buff=0.2)
        self.play(FadeIn(pk), run_time=0.4)
        self.at("s148")
        sm = T("1+2+3+4+5+6+5+4+3+2+1 = 36", 32, WARN).move_to(UP * 2.85)
        self.play(FadeOut(top), FadeOut(pk), Write(sm), run_time=1.2)
        # s149 relabel as probability
        self.at("s149")
        newy = VGroup(*[MathTex(r"\tfrac{%d}{36}" % v if v else "0", font_size=30, color=INK2).move_to(l).align_to(l, RIGHT) for v, l in zip(range(7), bx.ylabs)])
        ny = T("probability", 26, MUTED).rotate(PI / 2).move_to(bx.yt).shift(LEFT * 0.2)
        self.w("s149", "divide")
        self.play(ReplacementTransform(bx.ylabs, newy), ReplacementTransform(bx.yt, ny), FadeOut(sm), run_time=0.9)
        dist = pill("probability distribution", VIOLET, 34).move_to(UP * 2.85)
        self.w("s149", "probability", nth=1)
        self.play(FadeIn(dist, shift=DOWN * 0.2), run_time=0.6)
        # s150 definition
        self.at("s150")
        dc = def_card("DISTRIBUTION", "how the chances are spread out", VIOLET, 30).move_to(UP * 2.85)
        self.play(FadeOut(dist), FadeIn(dc, shift=DOWN * 0.2), run_time=0.6)
        # s151 eight
        self.at("s151")
        self.play(FadeOut(dc), FadeIn(dist), run_time=0.4)
        self.w("s151", "eight")
        self.play(stacks[6].animate.set_fill(VIOLET, 0.95), run_time=0.4)
        a8 = T("P(8) = 5/36", 38, VIOLET, weight=BOLD).move_to(UP * 2.85)
        self.play(FadeOut(dist), Write(a8), run_time=0.7)
        # s152 2 or 12
        self.at("s152")
        self.play(stacks[6].animate.set_fill(AQUA, 0.85), FadeOut(a8), run_time=0.3)
        self.play(stacks[0].animate.set_fill(VIOLET, 0.95), stacks[10].animate.set_fill(VIOLET, 0.95), run_time=0.4)
        a2 = T("2 and 12: 1/36 each", 34, VIOLET, weight=BOLD).move_to(UP * 2.85)
        self.play(FadeIn(a2), run_time=0.5)
        rare = T("the rarest rolls", 30, WARN, weight=BOLD).move_to(LEFT * 4.9 + DOWN * 2.15)
        self.w("s152", "rarest")
        self.play(FadeIn(rare), run_time=0.4)
        # s153 doubles
        self.at("s153")
        self.play(FadeOut(VGroup(a2, rare, bx, *stacks, newy, ny)), run_time=0.5)
        self.play(grid.animate.scale(1 / 0.62).move_to(LEFT * 2.6 + UP * 0.1), run_time=0.7)
        qd = T("a double?", 40, INK, weight=BOLD).move_to(RIGHT * 3.8 + UP * 1.4)
        self.play(FadeIn(qd), run_time=0.4)
        self.w("s153", "diagonal")
        self.play(LaggedStart(*[g.c(k, k).animate.set_fill(AQUA, 0.9) for k in range(1, 7)], lag_ratio=0.12), run_time=1.0)
        ad = MathTex(r"{6 \over 36} = {1 \over 6}", font_size=72, color=VIOLET).next_to(qd, DOWN, buff=0.4)
        self.w("s153", "six", nth=0)
        self.play(Write(ad), run_time=0.7)
        # s154 four or less
        self.at("s154")
        self.play(FadeOut(VGroup(qd, ad)), *g.reset(), run_time=0.4)
        q4 = T("a total of 4 or less?", 40, INK, weight=BOLD).move_to(RIGHT * 3.8 + UP * 1.4)
        self.play(FadeIn(q4), run_time=0.4)
        for s_, w in ((2, "two"), (3, "three"), (4, "four")):
            self.w("s154", w)
            self.play(g.where(lambda o, b, s_=s_: o + b == s_).animate.set_fill(AQUA, 0.9), run_time=0.35)
        a4 = MathTex(r"{6 \over 36} = {1 \over 6}", font_size=72, color=VIOLET).next_to(q4, DOWN, buff=0.4)
        self.w("s154", "squares")
        self.play(Write(a4), run_time=0.7)
        # s155 board games
        self.at("s155")
        self.play(FadeOut(VGroup(q4, a4)), *g.reset(), run_time=0.4)
        bxm = bar_axes([str(s) for s in range(2, 13)], 6, 2, 5.0, 2.6, "total", "")
        bxm.move_to(RIGHT * 3.6 + DOWN * 0.1)
        mb = bars(bxm.ax, WAYS, AQUA, width=0.32)
        gm = T("board games are built on this mountain", 26, INK2).next_to(bxm, UP, buff=0.35).set_x(3.3)
        self.play(FadeIn(bxm), LaggedStart(*[GrowFromEdge(b, DOWN) for b in mb], lag_ratio=0.06), FadeIn(gm), run_time=1.2)
        self.finish()
