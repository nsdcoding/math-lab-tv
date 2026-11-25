import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *


def words3(active=None):
    g = VGroup(*[pill(w, c, 44) for w, c in (("NOT", BLUE_), ("OR", AQUA), ("AND", ORANGE_))]).arrange(RIGHT, buff=0.8)
    return g


class S12Not(PBase):
    CHAPTER = "The Word NOT"

    def construct(self):
        self.at("s191")
        w = words3().move_to(UP * 0.4)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.2) for x in w], lag_ratio=0.2), run_time=0.9)
        self.w("s191", "not")
        self.play(w[1].animate.set_opacity(0.25), w[2].animate.set_opacity(0.25), w[0].animate.scale(1.3), run_time=0.6)
        self.play(FadeOut(w[1:]), w[0].animate.scale(0.75).move_to(UP * 2.85), run_time=0.6)
        nb = w[0]
        # s192 happens / doesn't
        self.at("s192")
        rect = VGroup(Rectangle(width=4.0, height=1.2, stroke_width=0, fill_color=AQUA, fill_opacity=0.8),
                      Rectangle(width=6.0, height=1.2, stroke_width=0, fill_color=GRID, fill_opacity=1)).arrange(RIGHT, buff=0.06).move_to(UP * 0.6)
        for r in rect: r.qa_container = True
        lt = VGroup(T("happens", 32, BG, weight=BOLD).move_to(rect[0]), T("doesn't happen", 32, INK, weight=BOLD).move_to(rect[1]))
        self.play(FadeIn(rect), FadeIn(lt), run_time=0.7)
        no3 = T("no third option", 30, MUTED).next_to(rect, DOWN, buff=0.35)
        self.w("s192", "third")
        self.play(FadeIn(no3), run_time=0.4)
        # s193 add to one
        self.at("s193")
        br = Brace(rect, DOWN, color=WARN)
        one = TB("together = 1", 40, WARN).next_to(br, DOWN, buff=0.2)
        self.play(FadeOut(no3), GrowFromCenter(br), FadeIn(one), run_time=0.8)
        # s194 formula
        self.at("s194")
        fm = MathTex(r"P(\text{not } A)", "=", "1", "-", r"P(A)", font_size=80)
        fm[0].set_color(BLUE_); fm[4].set_color(AQUA); fm[2].set_color(WARN)
        fb = boxed(fm, VIOLET, pad=0.4).move_to(DOWN * 1.3)
        self.play(FadeOut(VGroup(br, one)), run_time=0.3)
        self.play(FadeIn(fb[0]), Write(fm), run_time=1.2)
        # s195 A is any event
        self.at("s195")
        da = def_card("A", "any event, e.g. rolling a 7", AQUA, 32).move_to(UP * 2.0)
        self.play(FadeOut(VGroup(rect, lt)), FadeIn(da), run_time=0.6)
        # s196–s197 on the grid
        self.at("s196")
        self.play(FadeOut(da), fb.animate.scale(0.6).move_to(RIGHT * 3.8 + UP * 1.9), run_time=0.5)
        g = DiceGrid(0.6, fs=26).move_to(LEFT * 3.0 + DOWN * 0.1)
        sums = g.sums()
        self.play(FadeIn(g), FadeIn(sums), run_time=0.6)
        self.w("s196", "seven")
        self.play(*g.tint(lambda o, b: o + b == 7, AQUA, 0.9), run_time=0.5)
        e1 = MathTex(r"1 - {1 \over 6} = {5 \over 6}", font_size=60, color=VIOLET).move_to(RIGHT * 3.6 + UP * 0.45)
        self.w("s196", "not")
        self.play(*g.tint(lambda o, b: o + b != 7, BLUE_, 0.35), run_time=0.5)
        self.w("s196", "minus")
        self.play(Write(e1), run_time=1.0)
        self.at("s197")
        cnt = T("not 7: 30 squares", 34, BLUE_, weight=BOLD).move_to(RIGHT * 3.6 + DOWN * 0.85)
        self.play(FadeIn(cnt), run_time=0.5)
        e2 = MathTex(r"{30 \over 36} = {5 \over 6}\ \checkmark", font_size=50, color=VIOLET).next_to(cnt, DOWN, buff=0.25)
        self.w("s197", "thirty", nth=1)
        self.play(Write(e2), run_time=0.8)
        # s198 hard vs easy
        self.at("s198")
        self.play(FadeOut(VGroup(g, sums, e1, cnt, e2)), run_time=0.4)
        rng = np.random.default_rng(2)
        messy = VGroup(*[Square(0.3, stroke_width=0, fill_color=BLUE_, fill_opacity=0.7).move_to(
            [rng.uniform(-1.3, 1.3), rng.uniform(-1.0, 1.0), 0]).rotate(rng.uniform(0, 1)) for _ in range(35)]).move_to(LEFT * 3.3 + UP * 0.1)
        neat = Square(0.45, stroke_width=0, fill_color=AQUA, fill_opacity=0.9).move_to(RIGHT * 3.3 + UP * 0.1)
        lh = T("hard to count", 30, BLUE_, weight=BOLD).next_to(messy, DOWN, buff=0.4)
        le = T("easy to count", 30, AQUA, weight=BOLD).next_to(neat, DOWN, buff=0.4).set_y(lh.get_y())
        self.play(FadeIn(messy, lag_ratio=0.02), FadeIn(lh), run_time=0.8)
        self.w("s198", "opposite")
        self.play(FadeIn(neat, scale=0.5), FadeIn(le), run_time=0.5)
        # s199–s200 not twelve
        self.at("s199")
        self.play(FadeOut(VGroup(messy, neat, lh, le)), run_time=0.4)
        g = DiceGrid(0.6, fs=26).move_to(LEFT * 3.0 + DOWN * 0.1)
        sums = g.sums()
        q = T("not 12?", 40, BLUE_, weight=BOLD).move_to(RIGHT * 3.6 + UP * 0.6)
        self.play(FadeIn(g), FadeIn(sums), FadeIn(q), run_time=0.6)
        self.at("s200")
        ctr = TB("0", 48, BLUE_).move_to(RIGHT * 3.6 + DOWN * 0.3)
        self.add(ctr)
        others = [k for k in sorted(g.cells, key=lambda x: (-x[1], x[0])) if k != (6, 6)]
        self.play(LaggedStart(*[g.cells[k].animate.set_fill(BLUE_, 0.35) for k in others], lag_ratio=0.04),
                  ChangeDecimalToValue(DecimalNumber(0), 35) if False else Transform(ctr, TB("35", 48, BLUE_).move_to(ctr)), run_time=2.2)
        self.w("s200", "twelve", nth=1)
        self.play(g.c(6, 6).animate.set_fill(AQUA, 0.9), Indicate(g.num(6, 6), scale_factor=1.6), run_time=0.7)
        e = MathTex(r"1 - {1 \over 36} = {35 \over 36}", font_size=60, color=VIOLET).move_to(RIGHT * 3.6 + DOWN * 1.4)
        self.w("s200", "minus")
        self.play(FadeOut(ctr), Write(e), run_time=1.0)
        # s201 flip it around
        self.at("s201")
        self.play(FadeOut(VGroup(g, sums, q, e)), run_time=0.4)
        fl = CurvedArrow(LEFT * 1.6 + UP * 0.2, RIGHT * 1.6 + UP * 0.2, angle=-PI / 1.5, color=WARN, stroke_width=8)
        fl2 = CurvedArrow(RIGHT * 1.6 + DOWN * 0.2, LEFT * 1.6 + DOWN * 0.2, angle=-PI / 1.5, color=WARN, stroke_width=8)
        tg = pill("count the opposite, take it from 1", WARN, 36).move_to(DOWN * 1.9)
        self.play(Create(fl), Create(fl2), run_time=0.8)
        self.w("s201", "count")
        self.play(FadeIn(tg), run_time=0.5)
        # s202 superpower
        self.at("s202")
        sp = badge("NOT = 1 − P", BLUE_, 24)
        self.play(FadeOut(VGroup(fl, fl2)), tg.animate.move_to(UP * 0.4), run_time=0.5)
        self.play(FadeIn(sp, shift=LEFT * 0.4), run_time=0.6)
        self.finish()
