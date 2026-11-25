import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *

STEPS = [
    ("List all outcomes", "grid or tree; make them equally likely", INK),
    ("Count and divide", "outcomes you want ÷ all outcomes", AQUA),
    ("NOT", "1 − P(A)", BLUE_),
    ("OR", "add, then remove the overlap", AQUA),
    ("AND", "multiply along the path (updated chances)", ORANGE_),
    ("AT LEAST ONE", "1 − P(none)", WARN),
    ("GIVEN", "shrink the world, then count", VIOLET),
    ("LONG RUN", "patterns over many tries, not one try", WARN),
]


class S26Recipe(PBase):
    CHAPTER = "Recipe"

    def construct(self):
        self.at("s427")
        title = TB("Your probability recipe", 48, VIOLET).move_to(UP * 2.75)
        self.play(Write(title), run_time=0.8)
        rows = VGroup()
        for k, (h, d, c) in enumerate(STEPS):
            num = Circle(0.27, stroke_width=0, fill_color=c, fill_opacity=1); num.qa_container = True
            nt = TB(str(k + 1), 26, BG).move_to(num)
            ht = T(h, 28, c, weight=BOLD)
            dt = T(d, 26, INK2)
            r = VGroup(VGroup(num, nt), ht, dt).arrange(RIGHT, buff=0.3)
            rows.add(r)
        col1 = VGroup(*rows[:4]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        col2 = VGroup(*rows[4:]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        cols = VGroup(col1, col2).arrange(RIGHT, buff=0.6, aligned_edge=UP)
        if cols.width > 13.2: cols.scale_to_fit_width(13.2)
        cols.move_to(DOWN * 0.15)
        bx = card(cols.width + 0.7, cols.height + 0.7, VIOLET).move_to(cols)
        self.play(FadeIn(bx), run_time=0.4)
        sids = ["s428", "s429", "s430", "s431", "s432", "s433", "s434", "s435"]
        for k, sid in enumerate(sids):
            self.at(sid)
            self.play(FadeIn(rows[k], shift=RIGHT * 0.3), run_time=0.5)
        # s436–s438 run it on game night
        self.at("s436")
        self.play(FadeOut(VGroup(bx, cols)), run_time=0.5)
        g = DiceGrid(0.5, fs=22).move_to(LEFT * 3.6 + DOWN * 0.2)
        sums = g.sums(fs=18)
        e = TB("6 × 6 = 36", 44, WARN).move_to(RIGHT * 3.2 + UP * 1.3)
        self.play(FadeIn(g), FadeIn(sums), run_time=0.6)
        self.w("s436", "six", nth=1)
        self.play(Write(e), run_time=0.7)
        self.at("s437")
        self.w("s437", "twelve")
        self.play(g.c(6, 6).animate.set_fill(ORANGE_, 0.9), run_time=0.4)
        self.w("s437", "seven")
        self.play(*g.tint(lambda a, b: a + b == 7, BLUE_, 0.9), run_time=0.4)
        cmp_ = MathTex(r"{1 \over 36}", r"\;\text{vs}\;", r"{6 \over 36}", font_size=64).move_to(RIGHT * 3.2 + DOWN * 0.1)
        cmp_[0].set_color(ORANGE_); cmp_[2].set_color(BLUE_)
        self.w("s437", "one")
        self.play(Write(cmp_), run_time=1.0)
        self.at("s438")
        tal = T("over many game nights: friend wins ≈ 6× as often", 28, WARN, weight=BOLD).move_to(RIGHT * 3.0 + DOWN * 1.4)
        if tal.width > 7.4: tal.scale_to_fit_width(7.4)
        tal.set_x(3.0)
        self.play(FadeIn(tal), run_time=0.6)
        # s439 final line
        self.at("s439")
        self.clear()
        d1, d2 = die(3, ORANGE_, 1.3), die(4, BLUE_, 1.3)
        dd = VGroup(d1, d2).arrange(RIGHT, buff=0.6).move_to(UP * 0.8)
        self.play(FadeIn(dd, shift=DOWN * 0.5), run_time=0.5)
        self.play(Rotate(d1, TAU), Rotate(d2, -TAU), run_time=0.9)
        ln = T("You can't control the dice.\nBut now, you can understand them.", 38, INK, line_spacing=1.2).move_to(DOWN * 1.1)
        self.play(FadeIn(ln), run_time=0.8)
        self.finish()
