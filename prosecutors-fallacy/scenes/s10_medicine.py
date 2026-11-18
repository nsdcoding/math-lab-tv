import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


class S10Medicine(Base):
    CHAPTER = "The Same Swap in Medicine"

    def construct(self):
        # ── s081 the same swap at the doctor's ──
        self.at("s081", 0.0)
        cross_ = VGroup(Rectangle(width=0.4, height=1.2), Rectangle(width=1.2, height=0.4)).set_stroke(width=0).set_fill(RED_, 1)
        clinic = VGroup(card(2.2, 2.2, INK2), cross_).move_to(UP * 0.6)
        cross_.move_to(clinic[0])
        self.play(FadeIn(clinic, scale=0.8), run_time=0.6)
        hd = T("same swap, doctor's office", 34, INK).next_to(clinic, DOWN, buff=0.4)
        self.word("s081", "doctors'")
        self.play(FadeIn(hd, shift=UP * 0.2), run_time=0.5)

        # ── s082 a false alarm for 1 in 10 healthy people ──
        self.at("s082", 0.0)
        self.idle()
        frm = chip("from: Bayes' Theorem", AQUA, 26).to_edge(UP, buff=0.45).to_edge(RIGHT, buff=0.5)
        self.play(FadeOut(VGroup(clinic, hd)), FadeIn(frm, shift=LEFT * 0.4), run_time=0.5)
        b1 = cond_box("positive", "healthy", value="1 in 10", color=BLUE_, size=36)
        b1.move_to(UP * 0.4).set_x(-0.4 - b1.width / 2)
        self.word("s082", "false")
        self.play(FadeIn(b1, shift=UP * 0.2), run_time=0.6)

        # ── s083 swap it: given a positive, how likely healthy? ──
        self.at("s083", 0.0)
        b2 = cond_box("healthy", "positive", value="?", color=VIOLET, size=36)
        b2.move_to(UP * 0.4).set_x(0.4 + b2.width / 2)
        b2.value.match_y(b1.value)
        self.word("s083", "Swap")
        self.play(TransformFromCopy(b1.box, b2.box), TransformFromCopy(b1.expr, b2.expr), run_time=0.8)
        self.play(FadeIn(b2.value, scale=0.5), run_time=0.4)
        self.idle(lambda: Wiggle(b2.value, scale_value=1.2, n_wiggles=4))

        # ── s084 1,000 people: 99 false alarms, 9 real positives ──
        self.at("s084", 0.0)
        self.idle()
        self.play(VGroup(b1, b2).animate.scale(0.7).move_to(UP * 2.0), run_time=0.5)
        grid = VGroup(*[Square(0.12, stroke_width=0, fill_color=BLUE_, fill_opacity=0.5) for _ in range(1000)])
        grid.arrange_in_grid(20, 50, buff=0.04).move_to(DOWN * 0.85 + LEFT * 1.3)
        rng = np.random.default_rng(7)
        sick = list(range(10))   # first ten cells: sick (illustration of the Bayes video's grid)
        healthy = [i for i in range(1000) if i not in sick]
        fp = sorted(int(i) for i in rng.choice(healthy, 99, replace=False))
        for i in sick:
            grid[i].set_fill(ORANGE_, 0.9)
        gl = T("1,000 people", 26, INK2, weight=BOLD).next_to(grid, UP, buff=0.18).align_to(grid, LEFT)
        self.play(FadeIn(grid, lag_ratio=0.0008), FadeIn(gl), run_time=0.8)
        self.word("s084", "ninety")
        self.play(LaggedStart(*[grid[i].animate.set_fill(WARN, 1) for i in fp], lag_ratio=0.01), run_time=1.2)
        px = grid.get_right()[0] + 0.45
        c1 = VGroup(T("healthy, positive", 26, BLUE_, weight=BOLD), TB("99", 48, BLUE_)).arrange(DOWN, buff=0.1)
        c1.move_to(UP * 0.35).set_x(px + c1.width / 2)
        self.play(FadeIn(c1, shift=LEFT * 0.2), run_time=0.4)
        self.word("s084", "nine", nth=1)
        self.play(*[grid[i].animate.set_fill(WARN, 1).set_stroke(ORANGE_, 3) for i in sick[:9]], run_time=0.6)
        c2 = VGroup(T("sick, positive", 26, ORANGE_, weight=BOLD), TB("9", 48, ORANGE_)).arrange(DOWN, buff=0.1)
        c2.next_to(c1, DOWN, buff=0.35).align_to(c1, LEFT)
        self.play(FadeIn(c2, shift=LEFT * 0.2), run_time=0.4)

        # ── s085 11 in 12 of positives were healthy ──
        self.at("s085", 0.0)
        res = T("99 ÷ 108 = 11 in 12", 34, VIOLET, weight=BOLD).move_to(b2.value).scale(0.8)
        self.word("s085", "eleven")
        self.play(FadeOut(b2.value), FadeIn(res, scale=0.6), run_time=0.6)
        self.play(ripple(res.get_center(), VIOLET, r=0.6, scale=3), run_time=0.5)
        self.word("s085", "world")
        self.play(pulse(b1.value, s=1.2), run_time=0.6)

        # ── s086 the courtroom again ──
        self.at("s086", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(grid, gl, c1, c2, b1, b2, res, frm)), run_time=0.5)
        left = VGroup(T("courtroom", 28, INK2, weight=BOLD), lineup(9, 6, 0.42, 0.1),
                      T("8 innocent + 1 culprit", 26, INK)).arrange(DOWN, buff=0.3)
        hb = VGroup(*[Square(0.11, stroke_width=0, fill_color=WARN, fill_opacity=1) for _ in range(99)]).arrange_in_grid(9, 11, buff=0.04)
        sb = VGroup(*[Square(0.11, stroke_width=0, fill_color=ORANGE_, fill_opacity=1) for _ in range(9)]).arrange_in_grid(9, 1, buff=0.04)
        blk = VGroup(hb, sb).arrange(RIGHT, buff=0.15)
        right = VGroup(T("clinic", 28, INK2, weight=BOLD), blk, T("99 healthy + 9 sick", 26, INK)).arrange(DOWN, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=1.6).move_to(UP * 0.45)
        self.word("s086", "courtroom")
        self.play(FadeIn(left, shift=UP * 0.2), run_time=0.5)
        self.word("s086", "rare")
        self.play(FadeIn(right, shift=UP * 0.2), run_time=0.5)
        cap = pill("rare false alarm × big crowd = many false alarms", AQUA, 28).move_to(DOWN * 1.95)
        self.word("s086", "adds")
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.5)

        # ── s087 a second test shrinks the crowd ──
        self.at("s087", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(left, cap, right[2])), run_time=0.35)
        self.play(right[:2].animate.move_to(LEFT * 3.0 + UP * 0.6), run_time=0.5)
        filt = VGroup(Polygon(LEFT * 0.9 + UP * 0.6, RIGHT * 0.9 + UP * 0.6, RIGHT * 0.2 + DOWN * 0.4, LEFT * 0.2 + DOWN * 0.4),
                      Rectangle(width=0.4, height=0.5).shift(DOWN * 0.65)).set_stroke(INK2, 3)
        filt.move_to(UP * 0.5)
        ft = T("second, different test", 26, INK2, weight=BOLD).next_to(filt, DOWN, buff=0.3)
        self.word("s087", "second")
        self.play(Create(filt), FadeIn(ft), run_time=0.6)
        after = VGroup(VGroup(*[Square(0.11, stroke_width=0, fill_color=WARN, fill_opacity=1) for _ in range(10)]).arrange_in_grid(2, 5, buff=0.04),
                       VGroup(*[Square(0.11, stroke_width=0, fill_color=ORANGE_, fill_opacity=1) for _ in range(8)]).arrange_in_grid(2, 4, buff=0.04)
                       ).arrange(RIGHT, buff=0.15).move_to(RIGHT * 3.2 + UP * 0.6)
        al = T("smaller crowd (illustration)", 26, AQUA, weight=BOLD).next_to(after, DOWN, buff=0.35)
        a1 = Arrow(right[1].get_right(), filt.get_left(), buff=0.2, color=INK2, stroke_width=4)
        a2 = Arrow(filt.get_right(), after.get_left(), buff=0.2, color=INK2, stroke_width=4)
        self.word("s087", "shrinks")
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(after, scale=0.6), FadeIn(al), run_time=0.9)
        jc = pill("just like extra evidence in court", VIOLET, 26).move_to(DOWN * 1.9)
        self.word("s087", "court")
        self.play(FadeIn(jc, shift=UP * 0.2), run_time=0.4)

        # ── s084a ask the flipped question ──
        self.at("s084a", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(right[:2], filt, ft, after, al, a1, a2, jc)), run_time=0.5)
        q = T("Out of everyone who tests positive,\nhow many really have it?", 40, INK, weight=BOLD)
        qb = card(q.width + 1.0, q.height + 0.9, VIOLET); q.move_to(qb)
        qg = VGroup(qb, q).move_to(UP * 0.4)
        tag = pill("ask the flipped question", VIOLET, 28).next_to(qg, UP, buff=0.4)
        self.word("s084a", "scary")
        self.play(FadeIn(tag, shift=DOWN * 0.2), run_time=0.4)
        self.word("s084a", "Out")
        self.play(FadeIn(qg, scale=0.85), run_time=0.6)
        self.idle(lambda: glint(qb, VIOLET))
        self.finish()
