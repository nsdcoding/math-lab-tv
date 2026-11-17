import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def bars_pair(ax, a_vals, b_vals, w, ca=BLUE_, cb=ORANGE_, x0=0):
    """Two distributions side by side on one axis (a slightly left, b slightly right of each tick)."""
    A = VGroup(*[bar(ax, x0 + k - w * 0.55, v, ca, width=w, opacity=0.9) for k, v in enumerate(a_vals)])
    B = VGroup(*[bar(ax, x0 + k + w * 0.55, v, cb, width=w, opacity=0.9) for k, v in enumerate(b_vals)])
    return A, B


def bars_icon(color=INK2):
    p_ = person(color, 0.8)
    bars_ = VGroup(*[Line(UP * 0.45, DOWN * 0.45).set_stroke(MUTED, 4).shift(RIGHT * x) for x in (-0.3, -0.1, 0.1, 0.3)])
    bars_.move_to(p_)
    return VGroup(p_, bars_)


class S08Errors(Base):
    CHAPTER = "Two Ways to Be Wrong"

    def construct(self):
        rng = np.random.default_rng(8)
        # ── s070 a 2 × 2 table: truth (columns) × our verdict (rows) ──
        self.at("s070", 0.0)
        cw, chh = 4.0, 1.75
        cells = {}
        for r, rl in enumerate(["we say rigged", "we say fair"]):
            for c, cl in enumerate(["fair", "rigged"]):
                b = card(cw, chh, INK2).move_to(RIGHT * (c * (cw + 0.2) + 0.6) + UP * (1.2 - r * (chh + 0.2)))
                cells[(r, c)] = b
        grid = VGroup(*cells.values())
        h1 = T("coin really fair", 30, BLUE_, weight=BOLD).next_to(cells[(0, 0)], UP, buff=0.25)
        h2 = T("coin really rigged", 30, ORANGE_, weight=BOLD).next_to(cells[(0, 1)], UP, buff=0.25)
        r1 = T("we say\nrigged", 28, INK, weight=BOLD).next_to(cells[(0, 0)], LEFT, buff=0.35)
        r2 = T("we say\nfair", 28, INK, weight=BOLD).next_to(cells[(1, 0)], LEFT, buff=0.35)
        self.play(LaggedStart(*[FadeIn(b, scale=0.85) for b in grid], lag_ratio=0.15), run_time=0.8)
        self.play(FadeIn(h1, shift=DOWN * 0.2), FadeIn(h2, shift=DOWN * 0.2), run_time=0.4)
        self.word("s070", "wrong", dt=-0.6)
        self.play(FadeIn(r1, shift=RIGHT * 0.2), FadeIn(r2, shift=RIGHT * 0.2), run_time=0.4)
        two = VGroup(*[TB("?", 56, RED_).move_to(cells[k]) for k in ((0, 0), (1, 1))])
        self.play(LaggedStart(*[FadeIn(q, scale=0.4) for q in two], lag_ratio=0.3), run_time=0.6)
        self.idle(lambda: LaggedStart(*[Wiggle(q, scale_value=1.3) for q in two], lag_ratio=0.3))

        # ── s071 type I: fair coin called rigged = a false alarm ──
        self.at("s071", 0.0)
        self.idle()
        c00 = cells[(0, 0)]
        self.word("s071", "fair", dt=-0.2)
        self.play(Indicate(h1, color=BLUE_, scale_factor=1.15), run_time=0.5)
        self.word("s071", "rigged", dt=-0.2)
        self.play(Indicate(r1, color=INK, scale_factor=1.15), c00.animate.set_stroke(RED_, 4), run_time=0.5)
        bell = VGroup(Arc(radius=0.3, start_angle=0, angle=PI).set_stroke(RED_, 5),
                      Line(LEFT * 0.36, RIGHT * 0.36).set_stroke(RED_, 5), Dot(radius=0.07, color=RED_))
        bell[0].stretch(1.3, 1); bell[1].next_to(bell[0], DOWN, buff=0); bell[2].next_to(bell[1], DOWN, buff=0.02)
        bell.move_to(c00.get_left() + RIGHT * 0.6)
        fa = T("false alarm", 30, RED_, weight=BOLD).move_to(c00.get_center() + RIGHT * 0.35 + UP * 0.25)
        self.word("s071", "false", dt=-0.3)
        self.play(FadeOut(two[0]), FadeIn(bell, scale=0.5), FadeIn(fa, shift=LEFT * 0.2), run_time=0.5)
        self.play(Wiggle(bell, scale_value=1.3, rotation_angle=0.08 * TAU), run_time=0.6)
        t1 = T("type I error", 26, INK, weight=BOLD).next_to(fa, DOWN, buff=0.2)
        self.word("s071", "type", dt=-0.3)
        self.play(FadeIn(t1, shift=UP * 0.2), run_time=0.4)
        self.idle(lambda: Wiggle(bell, scale_value=1.25, rotation_angle=0.08 * TAU))

        # ── s072 in court: convicting an innocent person ──
        self.at("s072", 0.0)
        self.idle()
        jail = bars_icon(BLUE_).scale(0.7).move_to(c00.get_left() + RIGHT * 0.6)
        self.play(FadeOut(bell), FadeIn(jail, shift=DOWN * 0.3), run_time=0.5)
        ci = pill("innocent convicted", RED_, 24).next_to(grid, DOWN, buff=0.35).align_to(c00, LEFT)
        self.play(FadeIn(ci, shift=UP * 0.2), run_time=0.4)
        self.idle(lambda: pulse(jail, 1.15))

        # ── s073 type II: rigged coin called fair = a miss ──
        self.at("s073", 0.0)
        self.idle()
        c11 = cells[(1, 1)]
        self.word("s073", "rigged", dt=-0.2)
        self.play(Indicate(h2, color=ORANGE_, scale_factor=1.15), run_time=0.5)
        self.word("s073", "fair", dt=-0.2)
        self.play(Indicate(r2, color=INK, scale_factor=1.15), c11.animate.set_stroke(RED_, 4), run_time=0.5)
        miss = T("a miss", 30, RED_, weight=BOLD).move_to(c11.get_center() + RIGHT * 0.35 + UP * 0.25)
        tgt = VGroup(Circle(0.32).set_stroke(RED_, 4), Circle(0.16).set_stroke(RED_, 4), Dot(radius=0.05, color=RED_))
        tgt.move_to(c11.get_left() + RIGHT * 0.6)
        arrow_m = Arrow(tgt.get_center() + LEFT * 0.9 + UP * 0.6, tgt.get_center() + UP * 0.45 + RIGHT * 0.1, buff=0, color=INK2, stroke_width=4)
        arrow_m.qa_ignore = True
        self.word("s073", "miss", dt=-0.3)
        self.play(FadeOut(two[1]), FadeIn(tgt, scale=0.5), FadeIn(miss, shift=LEFT * 0.2), run_time=0.4)
        self.play(GrowArrow(arrow_m), run_time=0.35)
        t2 = T("type II error", 26, INK, weight=BOLD).next_to(miss, DOWN, buff=0.2)
        self.word("s073", "type", dt=-0.3)
        self.play(FadeIn(t2, shift=UP * 0.2), run_time=0.4)
        self.idle(lambda: pulse(tgt, 1.2))

        # ── s074 in court: a guilty person walks free; the other two cells are correct ──
        self.at("s074", 0.0)
        self.idle()
        walker = person(ORANGE_, 0.65).move_to(c11.get_left() + RIGHT * 0.6)
        self.play(FadeOut(VGroup(tgt, arrow_m)), FadeIn(walker), run_time=0.35)
        self.play(walker.animate.shift(RIGHT * 0.5).set_opacity(0.2), run_time=0.8)
        gf = pill("guilty walks free", RED_, 24).next_to(grid, DOWN, buff=0.35).align_to(c11, RIGHT)
        oks = VGroup(*[VGroup(check(AQUA, 0.3), T("correct", 28, AQUA, weight=BOLD)).arrange(RIGHT, buff=0.2).move_to(cells[k])
                       for k in ((1, 0), (0, 1))])
        self.play(FadeIn(gf, shift=UP * 0.2), LaggedStart(*[FadeIn(o, scale=0.6) for o in oks], lag_ratio=0.3), run_time=0.6)
        self.idle(lambda: LaggedStart(*[pulse(o, 1.15) for o in oks], lag_ratio=0.3))

        # ── s075 what alpha controls: a fair coin is falsely accused ≈ 2 times in 100 ──
        self.at("s075", 0.0)
        self.idle()
        table = VGroup(grid, h1, h2, r1, r2, fa, t1, jail, ci, miss, t2, walker, gf, oks)
        ch = dist_chart().move_to(RIGHT * 0.6 + UP * 0.3)
        ax = ch.ax
        bars = dist_bars(ax, BLUE_)
        push(self, table, VGroup(ch, bars), LEFT, run_time=0.8)
        cut = Line(ax.c2p(14.5, 0), ax.c2p(14.5, 200)).set_stroke(VIOLET, 5)
        cut_l = T("call it rigged at 15+", 26, VIOLET, weight=BOLD).next_to(cut, UP, buff=0.12).shift(RIGHT * 1.4)
        self.word("s075", "rule", dt=-0.3)
        self.play(Create(cut), FadeIn(cut_l), run_time=0.6)
        self.word("s075", "fair", dt=-0.3)
        self.play(LaggedStart(*[bars[k].animate.set_fill(RED_, 1) for k in range(15, 21)], lag_ratio=0.12),
                  ripple(ax.c2p(16, 5), RED_, r=0.3, scale=4), run_time=0.7)
        far = pill("false alarms ≈ 2 in 100", RED_, 26).move_to(ax.c2p(3.8, 150))
        self.word("s075", "two", dt=-0.3)
        self.play(FadeIn(far, scale=0.6), run_time=0.45)
        self.idle(lambda: LaggedStart(*[drop_into(ax, int(k_), BLUE_, 185) for k_ in rng.choice([6, 7, 8, 12, 13], 8)], lag_ratio=0.1),
                  lambda: pulse(far, 1.1))

        # ── s075a two in 100, not five: the line can only sit on whole heads ──
        self.at("s075a", 0.0)
        self.idle()
        st = xy_axes([0, 4, 1], [0, 15, 5], 6.4, 3.4, "call it rigged at …", "false alarms (%)", font_size=22, y_vertical=True, x_labels={})
        st.move_to(RIGHT * 0.2 + DOWN * 0.1)
        sax = st.ax
        fas = [13.2, 5.8, 2.1, 0.6]
        sb = VGroup(*[bar(sax, i + 0.5, v, MUTED, width=1.0) for i, v in enumerate(fas)])
        sl = VGroup(*[T(f"{c_}+ heads", 22, INK2).next_to(sax.c2p(i + 0.5, 0), DOWN, buff=0.14) for i, c_ in enumerate((13, 14, 15, 16))])
        st.xt.next_to(sl, DOWN, buff=0.15).align_to(sax.x_axis, RIGHT)
        vals = VGroup(*[T(f"{v}%", 24, INK, weight=BOLD).next_to(b_, UP, buff=0.1) for v, b_ in zip(fas, sb)])
        five = DashedLine(sax.c2p(0, 5), sax.c2p(4, 5), color=VIOLET, stroke_width=4)
        fl = T("1 in 20 = 5%", 24, VIOLET, weight=BOLD).next_to(five, RIGHT, buff=0.15)
        push(self, VGroup(ch, bars, cut, cut_l, far), VGroup(st, sl), LEFT, run_time=0.8)
        self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in sb], lag_ratio=0.15), LaggedStart(*[FadeIn(v_) for v_ in vals], lag_ratio=0.15), run_time=0.9)
        self.word("s075a", "five", dt=-0.3)
        self.play(Create(five), FadeIn(fl), run_time=0.6)
        self.word("s075a", "whole", dt=-0.3)
        self.play(LaggedStart(*[Indicate(l_, color=WARN, scale_factor=1.3) for l_ in sl], lag_ratio=0.15), run_time=0.8)
        self.word("s075a", "exactly", dt=-0.3)
        gapa = DoubleArrow(sax.c2p(1.5, 5.8) + RIGHT * 0.65, sax.c2p(2.5, 2.1) + LEFT * 0.65, buff=0, color=WARN, stroke_width=4, tip_length=0.16)
        self.play(GrowFromCenter(gapa), sb[1].animate.set_fill(RED_, 0.8), run_time=0.6)
        self.word("s075a", "nearest", dt=-0.3)
        safe = pill("nearest safe step", AQUA, 26).move_to(sax.c2p(3.05, 11.5))
        self.play(sb[2].animate.set_fill(AQUA, 1), FadeIn(safe, shift=DOWN * 0.2), run_time=0.5)
        self.idle(lambda: pulse(safe, 1.1), lambda: pulse(sb[2], 1.15))

        # ── s076 what about misses? a rigged coin that lands heads 70% of the time ──
        self.at("s076", 0.0)
        self.idle()
        ch2 = dist_chart().move_to(RIGHT * 0.6 + UP * 0.3)
        ax2 = ch2.ax
        A, B = bars_pair(ax2, EXP, EXP70, 0.22)
        push(self, VGroup(st, sl, sb, vals, five, fl, gapa, safe), VGroup(ch2, A), LEFT, run_time=0.8)
        lgA = pill("fair coin", BLUE_, 26).move_to(ax2.c2p(3.2, 190))
        lgB = pill("rigged: 70% heads", ORANGE_, 26).next_to(lgA, DOWN, buff=0.2).align_to(lgA, LEFT)
        self.play(FadeIn(lgA), run_time=0.3)
        self.word("s076", "rigged", dt=-0.3)
        self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in B], lag_ratio=0.03), FadeIn(lgB, shift=RIGHT * 0.2), run_time=1.1)
        self.word("s076", "seventy", dt=-0.3)
        self.play(Indicate(B[14], color=ORANGE_, scale_factor=1.15), ripple(B[14].get_top(), ORANGE_, r=0.25, scale=4), run_time=0.7)
        self.idle(lambda: LaggedStart(*[pulse(b_, 1.15) for b_ in B[11:18]], lag_ratio=0.08))

        # ── s077 15+ happens only ≈ 42% of the time: we miss it 58% ──
        self.at("s077", 0.0)
        self.idle()
        cut2 = Line(ax2.c2p(14.5, 0), ax2.c2p(14.5, 200)).set_stroke(VIOLET, 5)
        self.play(Create(cut2), run_time=0.4)
        self.word("s077", "forty", dt=-0.3)
        self.play(LaggedStart(*[B[k].animate.set_fill(AQUA, 1) for k in range(15, 21)], lag_ratio=0.12), run_time=0.6)
        caught = pill("caught ≈ 42%", AQUA, 28).move_to(ax2.c2p(3.4, 105))
        self.play(FadeIn(caught, scale=0.6), run_time=0.35)
        self.word("s077", "miss", dt=-0.5)
        self.play(LaggedStart(*[B[k].animate.set_fill(RED_, 0.75) for k in range(8, 15)], lag_ratio=0.1), run_time=0.6)
        missed = pill("missed ≈ 58%", RED_, 28).next_to(caught, DOWN, buff=0.2)
        self.play(FadeIn(missed, scale=0.6), run_time=0.35)
        self.idle(lambda: pulse(missed, 1.12), lambda: LaggedStart(*[pulse(B[k], 1.12) for k in range(8, 15)], lag_ratio=0.06))

        # ── s078 twenty flips: the two pictures overlap a lot ──
        self.at("s078", 0.0)
        self.idle()
        ov = Rectangle(width=ax2.c2p(16.5, 0)[0] - ax2.c2p(8.5, 0)[0], height=ax2.c2p(0, 200)[1] - ax2.c2p(0, 0)[1])
        ov.move_to(ax2.c2p(12.5, 100)).set_stroke(WARN, 3).set_fill(WARN, 0.08)
        ov.qa_ignore = True
        ovl = pill("overlap", WARN, 28).next_to(ov, UP, buff=0.12)
        self.word("s078", "overlap", dt=-0.6)
        self.play(Create(ov), FadeIn(ovl, shift=DOWN * 0.2), run_time=0.7)
        self.idle(lambda: ov.animate(rate_func=there_and_back).set_fill(opacity=0.25), lambda: pulse(ovl, 1.12))

        # ── s079 a hundred flips: the pictures pull apart; cut-off at 59 ──
        self.at("s079", 0.0)
        self.idle()
        ch3 = xy_axes([30, 90, 1], [0, 100, 25], 11.0, 3.6, "number of heads in 100 flips", "coins (of 1,000)",
                      x_labels={v: str(v) for v in range(40, 91, 10)}, font_size=22, y_vertical=True)
        ch3.move_to(RIGHT * 0.6 + UP * 0.2)
        ax3 = ch3.ax
        f100 = pmf_list(100, 0.5); r100 = pmf_list(100, 0.7)
        A3 = VGroup(*[bar(ax3, k, f100[k], BLUE_, width=0.14) for k in range(30, 91)])
        B3 = VGroup(*[bar(ax3, k, r100[k], ORANGE_, width=0.14) for k in range(30, 91)])
        for b_ in B3: b_.shift(RIGHT * 0.07)
        for b_ in A3: b_.shift(LEFT * 0.07)
        push(self, VGroup(ch2, A, B, lgA, lgB, cut2, caught, missed, ov, ovl), VGroup(ch3), UP, run_time=0.8)
        self.word("s079", "hundred", dt=-0.3)
        self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in A3], lag_ratio=0.01),
                  LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in B3], lag_ratio=0.01), run_time=1.2)
        apart = DoubleArrow(ax3.c2p(50, 92), ax3.c2p(70, 92), buff=0, color=WARN, stroke_width=4, tip_length=0.16)
        apl = T("pulled apart", 24, WARN, weight=BOLD).next_to(apart, UP, buff=0.1)
        self.word("s079", "apart", dt=-0.3)
        self.play(GrowFromCenter(apart), FadeIn(apl), run_time=0.5)
        cut3 = Line(ax3.c2p(58.5, 0), ax3.c2p(58.5, 80)).set_stroke(VIOLET, 5)
        c3l = T("cut-off: 59 heads", 24, VIOLET, weight=BOLD).next_to(cut3, UP, buff=0.1).shift(RIGHT * 0.2)
        self.word("s079", "fifty", dt=-0.3)
        self.play(Create(cut3), FadeIn(c3l), FadeOut(VGroup(apart, apl)), run_time=0.5)
        self.word("s079", "falsely", dt=-0.3)
        self.play(*[A3[k - 30].animate.set_fill(RED_, 1) for k in range(59, 70)], run_time=0.5)
        fa3 = pill("false alarms ≈ 4.4%", RED_, 26).move_to(ax3.c2p(44, 100))
        self.play(FadeIn(fa3, scale=0.6), run_time=0.35)
        self.idle(lambda: pulse(fa3, 1.1))

        # ── s080 the rigged coin is caught ≈ 99% ──
        self.at("s080", 0.0)
        self.idle()
        self.play(LaggedStart(*[B3[k - 30].animate.set_fill(AQUA, 1) for k in range(59, 91)], lag_ratio=0.02), run_time=0.8)
        c99 = pill("caught ≈ 99%", AQUA, 28).move_to(ax3.c2p(83, 97))
        self.play(FadeIn(c99, scale=0.6), ripple(c99.get_center(), AQUA, r=0.5, scale=3), run_time=0.5)
        self.idle(lambda: pulse(c99, 1.12))

        # ── s081 the trade-off: stricter line ↔ more misses; more data cuts both ──
        self.at("s081", 0.0)
        self.idle()
        tr = xy_axes([0, 3, 1], [0, 80, 20], 6.0, 3.3, None, "%", font_size=22, y_vertical=True, x_labels={})
        tr.move_to(LEFT * 1.0 + DOWN * 0.1)
        tax = tr.ax
        FA = bar(tax, 1.0, 2.1, RED_, width=0.8); MS = bar(tax, 2.0, 58.4, ORANGE_, width=0.8)
        labs = VGroup(T("false alarms", 24, RED_, weight=BOLD).next_to(tax.c2p(1.0, 0), DOWN, buff=0.15),
                      T("misses", 24, ORANGE_, weight=BOLD).next_to(tax.c2p(2.0, 0), DOWN, buff=0.15))
        vFA = always_redraw(lambda: T(f"{tax.p2c(FA.get_top())[1]:.1f}%", 24, INK, weight=BOLD).next_to(FA, UP, buff=0.1))
        vMS = always_redraw(lambda: T(f"{tax.p2c(MS.get_top())[1]:.1f}%", 24, INK, weight=BOLD).next_to(MS, UP, buff=0.1))
        state = pill("20 flips · cut-off 15", INK, 26).move_to(RIGHT * 4.2 + UP * 1.6)
        push(self, VGroup(ch3, A3, B3, cut3, c3l, fa3, c99), VGroup(tr, labs, FA, MS), LEFT, run_time=0.8)
        self.add(vFA, vMS)
        self.play(FadeIn(state, shift=LEFT * 0.2), run_time=0.4)
        def to(b, v):
            return b.animate.stretch_to_fit_height(max(1e-3, tax.c2p(0, v)[1] - tax.c2p(0, 0)[1]), about_edge=DOWN)
        self.word("s081", "stricter", dt=-0.3)
        s2 = pill("stricter: cut-off 16", VIOLET, 26).move_to(state)
        self.play(ReplacementTransform(state, s2), to(FA, 0.6), to(MS, 76.2), run_time=0.9)
        self.word("s081", "main", dt=-0.3)
        s3 = pill("100 flips · cut-off 59", AQUA, 26).move_to(s2)
        self.play(ReplacementTransform(s2, s3), to(FA, 4.4), to(MS, 0.7), run_time=1.0)
        both = pill("more data cuts both", AQUA, 28).next_to(s3, DOWN, buff=0.35)
        self.play(FadeIn(both, scale=0.6), run_time=0.4)
        self.idle(lambda: pulse(both, 1.1))
        self.until(SEGS["s081"]["end"] + 0.2)
        self.idle()
        vFA.clear_updaters(); vMS.clear_updaters()
        self.play(FadeOut(VGroup(tr, labs, FA, MS, vFA, vMS, s3, both), shift=LEFT * 1.0), run_time=0.5)
        self.finish()
