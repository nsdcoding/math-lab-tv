import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *


def blocks(n, col, size=0.55, label=None):
    g = VGroup(*[Square(size, stroke_width=0, fill_color=col, fill_opacity=0.9) for _ in range(n)]).arrange(RIGHT, buff=0.08)
    return g


class S13Odds(PBase):
    CHAPTER = "Odds Versus Probability"

    def construct(self):
        self.at("s203")
        o = TB("odds", 96, WARN).move_to(UP * 0.3)
        self.play(FadeIn(o, scale=0.6), run_time=0.7)
        self.at("s204")
        cp = card(5.2, 2.2, VIOLET).move_to(LEFT * 3.3 + UP * 0.5); co = card(5.2, 2.2, WARN).move_to(RIGHT * 3.3 + UP * 0.5)
        tp = TB("probability", 44, VIOLET).move_to(cp.get_center() + UP * 0.45)
        to = TB("odds", 44, WARN).move_to(co.get_center() + UP * 0.45)
        ne = TB("≠", 80, RED_).move_to(UP * 0.5)
        self.play(FadeOut(o), FadeIn(cp), FadeIn(co), FadeIn(tp), FadeIn(to), run_time=0.7)
        self.w("s204", "not")
        self.play(FadeIn(ne, scale=0.5), run_time=0.4)
        # s205 definitions
        self.at("s205")
        dp = T("happens ÷ everything", 30, INK).move_to(cp.get_center() + DOWN * 0.45)
        do = T("happens : doesn't happen", 26, INK).move_to(co.get_center() + DOWN * 0.45)
        self.play(FadeIn(dp), run_time=0.5)
        self.w("s205", "odds")
        self.play(FadeIn(do), run_time=0.5)
        # s206 grid
        self.at("s206")
        self.play(VGroup(cp, co, tp, to, ne, dp, do).animate.scale(0.62).move_to(UP * 2.35), run_time=0.6)
        self.qa_mute(ne)
        g = DiceGrid(0.5, fs=22).move_to(LEFT * 4.3 + DOWN * 0.75)
        sums = g.sums(fs=18)
        self.play(FadeIn(g), FadeIn(sums), run_time=0.5)
        self.w("s206", "six")
        self.play(*g.tint(lambda a, b: a + b == 7, AQUA, 0.9), run_time=0.4)
        self.w("s206", "thirty")
        self.play(*g.tint(lambda a, b: a + b != 7, GRID, 1), run_time=0.4)
        c6 = T("6 make 7", 30, AQUA, weight=BOLD).move_to(RIGHT * 0.4 + UP * 0.3)
        c30 = T("30 don't", 30, MUTED, weight=BOLD).next_to(c6, DOWN, buff=0.3)
        self.play(FadeIn(c6), FadeIn(c30), run_time=0.5)
        # s207 probability
        self.at("s207")
        pr = MathTex(r"P = {6 \over 36} = {1 \over 6}", font_size=56, color=VIOLET).move_to(RIGHT * 4.3 + UP * 0.35)
        self.play(Write(pr), run_time=0.9)
        # s208 odds 6:30 = 1:5
        self.at("s208")
        od = TB("odds  6 : 30  =  1 : 5", 44, WARN).move_to(RIGHT * 3.0 + DOWN * 0.8)
        self.play(Write(od), run_time=1.0)
        bl = VGroup(blocks(1, AQUA), blocks(5, GRID)).arrange(RIGHT, buff=0.3).move_to(RIGHT * 3.0 + DOWN * 1.85)
        bt = VGroup(T("win", 22, AQUA).next_to(bl[0], LEFT, buff=0.15), T("lose", 22, MUTED).next_to(bl[1], RIGHT, buff=0.15))
        self.w("s208", "every")
        self.play(FadeIn(bl), FadeIn(bt), run_time=0.6)
        # s209 same chance
        self.at("s209")
        self.play(FadeOut(VGroup(g, sums, c6, c30, od, bl, bt)), pr.animate.move_to(RIGHT * 3.4 + DOWN * 0.3), run_time=0.5)
        conv = MathTex(r"1 : 5", r"\;\rightarrow\;", r"{1 \over 1 + 5}", "=", r"{1 \over 6}", font_size=72)
        conv[0].set_color(WARN); conv[2].set_color(INK); conv[4].set_color(VIOLET)
        conv.move_to(LEFT * 2.6 + DOWN * 0.3)
        self.play(Write(conv), run_time=1.2)
        tot = T("1 + 5 = 6, the total", 30, WARN).next_to(conv, DOWN, buff=0.35)
        self.w("s209", "plus")
        self.play(FadeIn(tot), run_time=0.5)
        # s210 coin evens
        self.at("s210")
        self.play(FadeOut(VGroup(conv, tot, pr)), run_time=0.4)
        cn = coin("H", WARN, 0.8).move_to(LEFT * 3.0 + DOWN * 0.4)
        ev = VGroup(TB("1 : 1", 64, WARN), T("“evens”", 34, INK2), MathTex(r"P = {1 \over 2}", font_size=56, color=VIOLET)).arrange(DOWN, buff=0.3)
        ev.move_to(RIGHT * 2.0 + DOWN * 0.45)
        self.play(FadeIn(cn), FadeIn(ev[0]), run_time=0.6)
        self.w("s210", "evens")
        self.play(FadeIn(ev[1]), FadeIn(ev[2]), run_time=0.6)
        # s211 rule
        self.at("s211")
        self.play(FadeOut(VGroup(cn, ev)), run_time=0.4)
        rl = MathTex(r"\text{odds } a : b", r"\;\rightarrow\;", r"P = {a \over a + b}", font_size=72)
        rl[0].set_color(WARN); rl[2].set_color(VIOLET)
        rb = boxed(rl, VIOLET, pad=0.4).move_to(DOWN * 0.4)
        self.play(FadeIn(rb[0]), Write(rl), run_time=1.3)
        # s212 3:1 against
        self.at("s212")
        self.play(rb.animate.scale(0.7).move_to(UP * 0.4), run_time=0.5)
        ag = MathTex(r"3 : 1 \text{ against}", r"\;\rightarrow\;", r"{1 \over 1 + 3}", "=", r"{1 \over 4}", font_size=60)
        ag[0].set_color(WARN); ag[4].set_color(VIOLET)
        ag.move_to(DOWN * 1.4)
        self.play(Write(ag[0]), run_time=0.6)
        self.w("s212", "one", nth=1)
        self.play(Write(ag[1:3]), run_time=0.8)
        self.w("s212", "probability")
        self.play(Write(ag[3:]), run_time=0.6)
        # s213 ask
        self.at("s213")
        self.clear()
        qq = pill("compared to the whole, or to the other side?", WARN, 36).move_to(UP * 0.3)
        self.play(FadeIn(qq, scale=0.9), run_time=0.7)
        self.finish()
