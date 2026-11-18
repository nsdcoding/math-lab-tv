import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def word_frac(num, den, ncol, dcol, size=40, w=None):
    n = T(num, size, ncol, weight=BOLD); d = T(den, size, dcol, weight=BOLD)
    ln = Line(LEFT, RIGHT).set_stroke(INK, 4)
    ln.set_width(max(n.width, d.width) + 0.3 if w is None else w)
    g = VGroup(n, ln, d).arrange(DOWN, buff=0.18)
    g.num, g.line, g.den = n, ln, d
    return g


class S06Formula(Base):
    CHAPTER = "The Formula Behind It"

    def construct(self):
        # ── s055 the counting rule ──
        self.at("s055", 0.0)
        hd = TB("the counting rule", 48, INK).move_to(UP * 2.3)
        self.play(FadeIn(hd, shift=DOWN * 0.2), run_time=0.6)

        # ── s056 P(guilty | match) = guilty matches ÷ all matches ──
        self.at("s056", 0.0)
        lhs = cond("guilty", "match", 44)
        eq = T("=", 48, INK2)
        fr = word_frac("guilty people who match", "everyone who matches", ORANGE_, WARN, 38)
        row = VGroup(lhs, eq, fr).arrange(RIGHT, buff=0.45).move_to(UP * 1.05)
        self.play(FadeIn(lhs, shift=RIGHT * 0.3), run_time=0.6)
        self.word("s056", "equals")
        self.play(FadeIn(eq), FadeIn(fr.num, shift=DOWN * 0.2), Create(fr.line), run_time=0.6)
        self.word("s056", "everyone")
        self.play(FadeIn(fr.den, shift=UP * 0.2), run_time=0.5)
        self.idle(lambda: glint(fr.line, INK))

        # ── s057 1 / (1 + 8) = 1/9 ──
        self.at("s057", 0.0)
        self.idle()
        nums = VGroup(T("=", 48, INK2), word_frac("1", "1 + 8", ORANGE_, WARN, 52), T("=", 48, INK2),
                      frac(1, 9, VIOLET, 96)).arrange(RIGHT, buff=0.45)
        nums.next_to(row, DOWN, buff=0.35).align_to(eq, LEFT)
        self.word("s057", "top")
        self.play(FadeIn(nums[0]), FadeIn(nums[1].num, shift=DOWN * 0.2), Create(nums[1].line), run_time=0.5)
        self.word("s057", "bottom")
        self.play(FadeIn(nums[1].den, shift=UP * 0.2), run_time=0.5)
        self.word("s057", "ninth")
        self.play(FadeIn(nums[2]), FadeIn(nums[3], scale=0.6), ripple(nums[3].get_center(), VIOLET, r=0.5, scale=3), run_time=0.7)
        self.idle(lambda: pulse(nums[3], s=1.12))

        # ── s058 the Bayes formula says the same thing ──
        self.at("s058", 0.0)
        self.idle()
        frm = chip("from: Bayes' Theorem", AQUA, 26).to_edge(UP, buff=0.45).to_edge(RIGHT, buff=0.5)
        self.play(FadeOut(VGroup(hd, row, nums)), FadeIn(frm, shift=LEFT * 0.4), run_time=0.6)
        bayes = MathTex(r"P(G \mid M) = {P(M \mid G)\,P(G) \over P(M)}", font_size=50, color=INK)
        bl = T("Bayes' formula", 28, MUTED, weight=BOLD)
        left = VGroup(bl, bayes).arrange(DOWN, buff=0.35)
        mini = lineup(9, 6, 0.36, 0.1)
        ml = T("count the crowd", 28, MUTED, weight=BOLD)
        mres = TB("1 in 9", 44, VIOLET)
        right = VGroup(ml, mini, mres).arrange(DOWN, buff=0.3)
        eqs = TB("=", 64, VIOLET)
        VGroup(left, eqs, right).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.1)
        print("bayes row width", VGroup(left, eqs, right).width)
        defs = T("G = guilty,  M = match", 24, INK2).next_to(left, DOWN, buff=0.3)
        self.word("s058", "formula")
        self.play(FadeIn(left, shift=UP * 0.2), FadeIn(defs), run_time=0.7)
        self.word("s058", "counting")
        self.play(FadeIn(ml), LaggedStart(*[FadeIn(p, scale=0.5) for p in mini], lag_ratio=0.05), run_time=0.8)
        self.word("s058", "same")
        self.play(FadeIn(eqs, scale=0.5), FadeIn(mres, shift=UP * 0.2), run_time=0.6)
        self.idle(lambda: pulse(eqs, s=1.2))

        # ── s059 the eight came from the crowd ──
        self.at("s059", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(left, defs, eqs, right, frm)), run_time=0.5)
        f2 = word_frac("1", "1 + 8", ORANGE_, WARN, 72).move_to(LEFT * 2.4 + UP * 0.2)
        self.play(FadeIn(f2), run_time=0.5)
        eight = f2.den[-1]
        self.word("s059", "eight")
        circ = Circle(radius=0.5).set_stroke(AQUA, 5).move_to(eight)
        circ.qa_ignore = True
        self.play(Create(circ), run_time=0.5)
        crowd_c = pill("8,000,000 people × 1 in a million", AQUA, 32).move_to(RIGHT * 2.9 + DOWN * 1.6)
        ar = Arrow(crowd_c.get_left(), circ.get_right(), buff=0.15, color=AQUA, stroke_width=5)
        self.word("s059", "size")
        self.play(FadeIn(crowd_c, shift=LEFT * 0.3), GrowArrow(ar), run_time=0.7)
        nb = pill("not from the expert's number alone", MUTED, 26).next_to(crowd_c, UP, buff=0.35)
        self.play(FadeIn(nb, shift=DOWN * 0.2), run_time=0.4)
        self.idle(lambda: ShowPassingFlash(ar.copy().set_stroke(WARN, 8), time_width=0.4))
        self.finish()
