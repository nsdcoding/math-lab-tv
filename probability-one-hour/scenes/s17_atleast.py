import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *


class S17AtLeast(PBase):
    CHAPTER = "At Least One"

    def construct(self):
        self.at("s264")
        a = pill("NOT", BLUE_, 48); b = pill("AND", ORANGE_, 48)
        VGroup(a, b).arrange(RIGHT, buff=2.5).move_to(UP * 0.3)
        self.play(FadeIn(a), FadeIn(b), run_time=0.5)
        self.w("s264", "combine")
        self.play(a.animate.shift(RIGHT * 1.2), b.animate.shift(LEFT * 1.2), run_time=0.6)
        # s265 question
        self.at("s265")
        self.play(FadeOut(VGroup(a, b)), run_time=0.3)
        hd = header("4 rolls: at least one 6?", INK, 34)
        slots = VGroup(*[die_q(ORANGE_, 1.1) for _ in range(4)]).arrange(RIGHT, buff=0.5).move_to(UP * 1.0)
        self.play(FadeIn(hd), FadeIn(slots, lag_ratio=0.15), run_time=0.8)
        # s266 cases pile
        self.at("s266")
        cases = ["6 _ _ _", "_ 6 _ _", "_ _ 6 _", "_ _ _ 6", "6 6 _ _", "6 _ 6 _", "_ 6 6 _", "6 6 6 _", "…"]
        cs = VGroup(*[T(c, 28, INK2) for c in cases]).arrange_in_grid(3, 3, buff=(0.8, 0.25)).move_to(DOWN * 1.1)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cs], lag_ratio=0.15), run_time=1.8)
        lot = T("a lot of cases!", 30, WARN, weight=BOLD).next_to(slots, RIGHT, buff=0.3)
        self.w("s266", "lot")
        self.play(FadeIn(lot), run_time=0.4)
        # s267 tempting shortcut
        self.at("s267")
        self.play(FadeOut(VGroup(cs, lot)), run_time=0.4)
        sc = MathTex(r"{1 \over 6} + {1 \over 6} + {1 \over 6} + {1 \over 6} = {4 \over 6} \approx 67\%\ ?", font_size=56, color=MUTED).move_to(DOWN * 1.0)
        self.w("s267", "add")
        self.play(Write(sc), run_time=1.6)
        # s268 six rolls -> 100%
        self.at("s268")
        slots6 = VGroup(*[die_q(ORANGE_, 0.95) for _ in range(6)]).arrange(RIGHT, buff=0.35).move_to(UP * 1.0)
        self.play(ReplacementTransform(slots, slots6), FadeOut(sc), run_time=0.6)
        s6 = MathTex(r"6 \times {1 \over 6} = 1 = 100\%\ ?", font_size=56, color=MUTED).move_to(DOWN * 0.45)
        self.w("s268", "six", nth=1)
        self.play(Write(s6), run_time=1.0)
        trap = stamp("guaranteed? no!", RED_, 34).next_to(s6, DOWN, buff=0.25)
        self.w("s268", "guarantee")
        self.play(FadeIn(trap, scale=1.4), run_time=0.4)
        # s269 six rolls, no six
        self.at("s269")
        rolls = SIM["no_six_in_six"]
        real = VGroup(*[die(n, ORANGE_, 0.95) for n in rolls]).arrange(RIGHT, buff=0.35).move_to(slots6)
        self.play(*[Transform(slots6[k], real[k]) for k in range(6)], run_time=0.8)
        ns = T("no six at all", 30, RED_, weight=BOLD).next_to(slots6, UP, buff=0.3)
        self.play(FadeIn(ns), run_time=0.4)
        # s270 overlaps
        self.at("s270")
        self.play(FadeOut(VGroup(s6, trap, ns)), run_time=0.3)
        circ = VGroup(*[Circle(0.8, stroke_color=c, stroke_width=4, fill_color=c, fill_opacity=0.2).move_to(DOWN * 1.1 + RIGHT * (k - 1.5) * 0.9)
                        for k, c in enumerate((ORANGE_, BLUE_, AQUA, VIOLET))])
        for c in circ: c.qa_ignore = True
        ov = T("they overlap", 28, WARN, weight=BOLD).next_to(circ, RIGHT, buff=0.4)
        self.play(LaggedStart(*[DrawBorderThenFill(c) for c in circ], lag_ratio=0.2), FadeIn(ov), run_time=1.2)
        # s271 flip it
        self.at("s271")
        self.play(FadeOut(VGroup(circ, ov, slots6)), run_time=0.4)
        hd2 = header("flip it around", WARN, 34)
        self.play(FadeOut(hd), FadeIn(hd2), run_time=0.4); hd = hd2
        r1 = pill("at least one 6", AQUA, 40); r2 = pill("no 6 at all", BLUE_, 40)
        VGroup(r1, r2).arrange(RIGHT, buff=2.4).move_to(UP * 0.8)
        fa = CurvedArrow(r1.get_top() + UP * 0.1, r2.get_top() + UP * 0.1, angle=-PI / 3, color=WARN, stroke_width=5)
        self.play(FadeIn(r1), run_time=0.4)
        self.w("s271", "opposite")
        self.play(Create(fa), FadeIn(r2), run_time=0.7)
        # s272 5/6
        self.at("s272")
        faces = VGroup(*[die(k, ORANGE_, 0.7) for k in range(1, 7)]).arrange(RIGHT, buff=0.2).move_to(DOWN * 0.9)
        for k in range(5): faces[k][0].set_fill(AQUA, 0.3)
        faces[5].set_opacity(0.3)
        f56 = MathTex(r"P(\text{not } 6) = {5 \over 6}", font_size=52, color=VIOLET).next_to(faces, DOWN, buff=0.3)
        self.play(FadeIn(faces), Write(f56), run_time=0.9)
        # s273 4 times
        self.at("s273")
        self.play(FadeOut(VGroup(faces, f56, fa, r1)), r2.animate.move_to(UP * 2.05), run_time=0.5)
        sl = VGroup(*[VGroup(die_q(BLUE_, 0.9), MathTex(r"\tfrac{5}{6}", font_size=44, color=BLUE_)).arrange(DOWN, buff=0.2) for _ in range(4)])
        sl.arrange(RIGHT, buff=0.9).move_to(UP * 0.45)
        times = VGroup(*[MathTex(r"\times", font_size=44, color=INK2).move_to((sl[k][1].get_center() + sl[k + 1][1].get_center()) / 2) for k in range(3)])
        self.w("s273", "five")
        for k in range(4):
            self.play(FadeIn(sl[k], shift=UP * 0.2), *([FadeIn(times[k - 1])] if k else []), run_time=0.4)
        # s274 625/1296
        self.at("s274")
        e = MathTex(r"\left({5 \over 6}\right)^4 = {625 \over 1296} \approx 48\%", font_size=52, color=BLUE_).move_to(DOWN * 1.7)
        self.play(Write(e), run_time=1.3)
        # s275 1 minus
        self.at("s275")
        self.play(FadeOut(VGroup(sl, times, r2)), e.animate.move_to(UP * 1.5), run_time=0.5)
        e2 = MathTex(r"1 - {625 \over 1296} = {671 \over 1296} \approx 52\%", font_size=56, color=VIOLET).move_to(DOWN * 0.2)
        self.play(Write(e2), run_time=1.3)
        # s276 vs 67
        self.at("s276")
        w = T("67%", 60, RED_, weight=BOLD).move_to(LEFT * 2.5 + DOWN * 1.95)
        xx = cross(RED_, 0.5).move_to(w); [setattr(m, "qa_ignore", True) for m in xx]
        r = T("52%", 72, VIOLET, weight=BOLD).move_to(RIGHT * 2.5 + DOWN * 1.95)
        lw = T("adding (wrong)", 24, RED_).next_to(w, UP, buff=0.2); lr = T("flipping (right)", 24, VIOLET).next_to(r, UP, buff=0.2)
        self.play(FadeIn(w), FadeIn(lw), Create(xx), FadeIn(r), FadeIn(lr), run_time=0.8)
        # s277–s278 curve
        self.at("s277")
        self.clear()
        ax = Axes(x_range=[0, 12, 1], y_range=[0, 1, 0.25], x_length=10, y_length=3.9,
                  axis_config=dict(color=INK2, stroke_width=3, include_tip=False, tick_size=0.06)).move_to(UP * 0.05)
        xl = VGroup(*[T(str(v), 24, INK2).next_to(ax.c2p(v, 0), DOWN, buff=0.14) for v in range(2, 13, 2)])
        yl = VGroup(*[T(f"{int(v * 100)}%", 24, INK2).next_to(ax.c2p(0, v), LEFT, buff=0.12) for v in (0, 0.25, 0.5, 0.75, 1)])
        xt = T("number of rolls", 24, MUTED).next_to(xl, DOWN, buff=0.1)
        yt = T("chance of at least one 6", 24, MUTED).rotate(PI / 2).next_to(yl, LEFT, buff=0.15)
        top = DashedLine(ax.c2p(0, 1), ax.c2p(12, 1), color=INK2, dash_length=0.12)
        pts = [ax.c2p(n, 1 - (5 / 6) ** n) for n in range(0, 13)]
        dots_ = VGroup(*[Dot(p, radius=0.07, color=VIOLET) for p in pts[1:]])
        cv = VMobject(stroke_color=VIOLET, stroke_width=4).set_points_as_corners(pts)
        cv.qa_ignore = True
        self.play(FadeIn(VGroup(ax, xl, yl, xt, yt)), Create(top), run_time=0.7)
        self.play(Create(cv), FadeIn(dots_, lag_ratio=0.1), run_time=1.6)
        p6 = pts[6]
        l6 = T("6 rolls: 66.5%", 28, VIOLET, weight=BOLD).next_to(p6, DR, buff=0.2)
        self.w("s277", "sixty")
        self.play(Indicate(dots_[5], scale_factor=2.0), FadeIn(l6), run_time=0.7)
        self.at("s278")
        nv = T("never quite reaches 100%", 28, WARN, weight=BOLD).move_to(ax.c2p(6.5, 0.2))
        self.play(FadeIn(nv), Indicate(top, color=WARN), run_time=0.9)
        # s279 rule
        self.at("s279")
        self.clear()
        rl = MathTex(r"P(\text{at least one})", "=", "1", "-", r"P(\text{none})", font_size=72)
        rl[0].set_color(AQUA); rl[4].set_color(BLUE_)
        rb = boxed(rl, VIOLET, pad=0.4).move_to(UP * 0.3)
        self.play(FadeIn(rb[0]), Write(rl), run_time=1.3)
        # s280–s282 quiz
        self.at("s280")
        self.play(rb.animate.scale(0.6).move_to(UP * 2.15), run_time=0.5)
        qz = VGroup(*[ic_quiz(INK2, 0.9, None) for _ in range(3)]).arrange(RIGHT, buff=0.6).move_to(LEFT * 3.6 + DOWN * 0.3)
        ql = T("3 guesses, 4 choices each", 26, INK2).next_to(qz, DOWN, buff=0.3)
        self.play(FadeIn(qz, lag_ratio=0.2), FadeIn(ql), run_time=0.8)
        self.at("s281")
        e1 = MathTex(r"P(\text{wrong}) = {3 \over 4}", font_size=46, color=BLUE_).move_to(RIGHT * 3.0 + UP * 1.1)
        e2 = MathTex(r"\left({3 \over 4}\right)^3 = {27 \over 64}", font_size=52, color=BLUE_).next_to(e1, DOWN, buff=0.35)
        self.play(Write(e1), run_time=0.7)
        self.w("s281", "cubed")
        self.play(Write(e2), run_time=0.9)
        self.at("s282")
        e3 = MathTex(r"1 - {27 \over 64} = {37 \over 64} \approx 58\%", font_size=52, color=VIOLET).next_to(e2, DOWN, buff=0.35)
        self.play(Write(e3), run_time=1.0)
        # s283 banner
        self.at("s283")
        self.clear()
        bn = big_word("AT LEAST ONE → FLIP IT", WARN, 72).move_to(UP * 0.3)
        self.play(FadeIn(bn, scale=0.8), run_time=0.7)
        self.finish()
