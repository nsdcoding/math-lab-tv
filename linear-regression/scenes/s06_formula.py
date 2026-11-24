import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

DX = [-10, -5, 0, 5, 10]
DY = [-110, -30, 0, 30, 110]


def sgn(v):
    return ("+" if v > 0 else ("−" if v < 0 else "")) + f"{abs(v):,}"


class S06Formula(Base):
    CHAPTER = "The Formula"

    def construct(self):
        axg = lesson_axes(); ax = axg.ax
        dots = house_dots(ax)
        best = price_line(ax, *BEST, 0, 3500)
        self.add(axg, best, dots)

        # ── s059 a formula lands on it directly ──
        self.at("s059", 0.0)
        self.play(best.animate.set_stroke(opacity=0.25), run_time=0.5)
        f1 = T("no searching:", 30, INK2)
        f2 = T("a formula", 40, VIOLET, weight=BOLD)
        fg = VGroup(f1, f2).arrange(DOWN, buff=0.2).move_to(RIGHT * PANEL_X + UP * 1.2)
        self.until(word_time("s059", word_index("s059", "formula")))
        self.play(FadeIn(fg, shift=UP * 0.2), run_time=0.6)

        # ── s060 step one: the average house ──
        self.at("s060", 0.0)
        s1 = step_chip(1, "find the average house", BLUE_, 24).move_to([2.25, 2.3, 0], aligned_edge=LEFT)
        self.play(FadeOut(fg), FadeIn(s1), run_time=0.5)
        hv = DashedLine(ax.c2p(2000, 0), ax.c2p(2000, 250), color=BLUE_, stroke_width=3)
        hh = DashedLine(ax.c2p(0, 250), ax.c2p(2000, 250), color=BLUE_, stroke_width=3)
        av = Dot(ax.c2p(2000, 250), radius=0.17, color=BLUE_).set_stroke(INK, 3)
        av.qa_dot = True
        cs = T("average size  2,000 sq ft", 28, INK)
        cp = T("average price  $250k", 28, INK)
        cg = VGroup(cs, cp).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(RIGHT * PANEL_X + UP * 1.0)
        self.until(word_time("s060", word_index("s060", "average")) + 0.3)
        self.play(Create(hv), FadeIn(cs), run_time=0.7)
        self.until(word_time("s060", word_index("s060", "price")))
        self.play(Create(hh), FadeIn(cp), run_time=0.7)
        self.play(FadeIn(av, scale=0.4), run_time=0.4)
        al = T("average house", 24, BLUE_, weight=BOLD).next_to(av, DR, buff=0.12)
        self.play(FadeIn(al), run_time=0.4)

        # ── s061 the best line passes through it ──
        self.at("s061", 0.0)
        self.play(best.animate.set_stroke(opacity=1), run_time=0.8)
        pin = T("always passes through it", 28, VIOLET, weight=BOLD).move_to(RIGHT * PANEL_X + DOWN * 0.4)
        self.play(FadeIn(pin), Flash(av, color=VIOLET, line_length=0.25), run_time=0.7)
        tilt = T("we only need its tilt", 28, INK).next_to(pin, DOWN, buff=0.3)
        self.until(word_time("s061", word_index("s061", "So")))
        self.play(FadeIn(tilt), run_time=0.5)

        # ── s062 step two: distances from the average ──
        self.at("s062", 0.0)
        self.play(FadeOut(VGroup(pin, tilt, cg)), run_time=0.4)
        s2 = step_chip(2, "distance from average", BLUE_, 24).move_to(s1, aligned_edge=LEFT)
        arrows = VGroup()
        for (x, y), d in zip(HOUSES, dots):
            if x == 2000: continue
            arrows.add(Arrow(av.get_center(), d.get_center(), buff=0.2, color=MUTED, stroke_width=3,
                             max_tip_length_to_length_ratio=0.12))
        self.play(ReplacementTransform(s1, s2), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=1.2)
        self.qa_mute(arrows)

        # ── move to the table ──
        chart = VGroup(axg, best, dots, av, hv, hh, al, arrows)
        self.until(word_time("s062", word_index("s062", "both")))
        self.play(FadeOut(VGroup(axg.labs, axg.xt, axg.yt, al)), run_time=0.3)
        self.play(VGroup(axg.ax, best, dots, av, hv, hh, arrows).animate.scale(0.42).move_to(LEFT * 5.45 + UP * 1.35),
                  s2.animate.scale(0.85).move_to([-6.7, -0.9, 0], aligned_edge=LEFT), run_time=0.9)
        self.qa_mute(arrows, False)
        # table: size | price | Δsize | Δprice | product | Δsize²
        heads = ["size", "price", "size\n− avg", "price\n− avg", "multiply", "(size\n− avg)²"]
        cols_x = [-1.95, -0.55, 0.95, 2.6, 4.25, 5.95]
        hy, ry = 2.35, [1.55, 0.95, 0.35, -0.25, -0.85]
        H = VGroup(*[T(h, 22, MUTED, weight=BOLD).move_to([x, hy, 0]) for h, x in zip(heads, cols_x)])
        rows = [[T(f"{x // 100}", 30, INK), T(f"{y}", 30, INK)] for x, y in HOUSES]
        rows_m = VGroup(*[VGroup(*r) for r in rows])
        for r, y in zip(rows_m, ry):
            for c, x in zip(r, cols_x[:2]):
                c.move_to([x, y, 0])
        rule = Line([-2.6, hy - 0.42, 0], [6.8, hy - 0.42, 0], color=GRID, stroke_width=2)
        self.play(FadeIn(H[:2]), Create(rule), LaggedStart(*[FadeIn(r) for r in rows_m], lag_ratio=0.1), run_time=0.9)

        # ── s063 units ──
        self.at("s063", 0.0)
        u1 = T("size: hundreds of sq ft", 22, BLUE_).move_to([-6.7, 0.1, 0], aligned_edge=LEFT)
        u2 = T("price: thousands of $", 22, BLUE_).move_to([-6.7, -0.4, 0], aligned_edge=LEFT)
        self.play(FadeIn(u1), run_time=0.4)
        self.until(word_time("s063", word_index("s063", "price")))
        self.play(FadeIn(u2), run_time=0.4)
        avg_r = VGroup(T("← average", 22, BLUE_), T("20", 28, BLUE_, weight=BOLD), T("250", 28, BLUE_, weight=BOLD))
        avg_r[1].move_to([cols_x[0], -1.5, 0]); avg_r[2].move_to([cols_x[1], -1.5, 0])
        avg_r[0].next_to(avg_r[2], RIGHT, buff=0.35)
        self.play(FadeIn(avg_r), run_time=0.5)
        dcol = VGroup(*[T(sgn(v), 30, INK2).move_to([cols_x[2], y, 0]) for v, y in zip(DX, ry)])
        ecol = VGroup(*[T(sgn(v), 30, INK2).move_to([cols_x[3], y, 0]) for v, y in zip(DY, ry)])
        self.play(FadeIn(H[2:4]), LaggedStart(*[FadeIn(a, shift=RIGHT * 0.2) for a in dcol], lag_ratio=0.12),
                  LaggedStart(*[FadeIn(a, shift=RIGHT * 0.2) for a in ecol], lag_ratio=0.12), run_time=1.3)

        # ── s064 step three: multiply and add ──
        self.at("s064", 0.0)
        s3 = step_chip(3, "multiply, then add", WARN, 26).scale(0.85).move_to(s2, aligned_edge=LEFT)
        P = [a * b for a, b in zip(DX, DY)]
        pcol = VGroup(*[T(f"{v:,}", 30, WARN).move_to([cols_x[4], y, 0]) for v, y in zip(P, ry)])
        self.play(ReplacementTransform(s2, s3), FadeIn(H[4]), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(p, shift=LEFT * 0.2) for p in pcol], lag_ratio=0.15), run_time=1.2)
        sig = VGroup(MathTex(r"\Sigma", color=WARN, font_size=56), T("means add them all up", 24, INK)).arrange(RIGHT, buff=0.2)
        sig.scale(0.9).move_to([-6.7, -1.45, 0], aligned_edge=LEFT)
        self.until(word_time("s064", word_index("s064", "add")))
        self.play(FadeIn(sig), run_time=0.5)

        # ── s065 running total 2,500 ──
        self.at("s065", 0.0)
        tot1 = T("2,500", 34, WARN, weight=BOLD).move_to([cols_x[4], -1.5, 0])
        line1 = Line([cols_x[4] - 0.65, -1.15, 0], [cols_x[4] + 0.65, -1.15, 0], color=WARN, stroke_width=2)
        self.play(LaggedStart(*[Indicate(p, color=WARN) for p in pcol], lag_ratio=0.3), run_time=3.0)
        self.until(word_time("s065", word_index("s065", "That")))
        self.play(Create(line1), FadeIn(tot1, scale=0.6), run_time=0.6)

        # ── s066 bigger and pricier → positive ──
        self.at("s066", 0.0)
        hl = VGroup(*[SurroundingRectangle(VGroup(dcol[i], ecol[i], pcol[i]), color=ORANGE_, buff=0.1, corner_radius=0.08) for i in (3, 4)])
        for h in hl: h.qa_ignore = True  # highlight boxes
        self.play(Create(hl), run_time=0.6)
        up = T("pulls the line up", 26, ORANGE_, weight=BOLD).move_to([-6.7, -2.15, 0], aligned_edge=LEFT)
        self.until(word_time("s066", word_index("s066", "That")))
        self.play(FadeIn(up), run_time=0.4)

        # ── s066a minus times minus ──
        self.at("s066a", 0.0)
        hl2 = VGroup(*[SurroundingRectangle(VGroup(dcol[i], ecol[i], pcol[i]), color=BLUE_, buff=0.1, corner_radius=0.08) for i in (0, 1)])
        for h in hl2: h.qa_ignore = True
        self.play(ReplacementTransform(hl, hl2), run_time=0.6)
        mm = T("−10 × −110 = +1,100", 26, BLUE_, weight=BOLD).move_to([-6.7, -2.15, 0], aligned_edge=LEFT)
        self.until(word_time("s066a", word_index("s066a", "Minus")))
        self.play(FadeOut(up), FadeIn(mm), run_time=0.5)
        bc = VGroup(T("bigger but cheaper?", 24, RED_, weight=BOLD), T("would give a minus", 24, RED_)).arrange(DOWN, buff=0.1)
        bc.move_to([-6.7, -2.15, 0], aligned_edge=LEFT)
        self.until(word_time("s066a", word_index("s066a", "Only")))
        self.play(FadeOut(mm), FadeIn(bc), run_time=0.5)

        # ── s067 step four: square the size distances ──
        self.at("s067", 0.0)
        s4 = step_chip(4, "square, then add", AQUA, 26).scale(0.85).move_to(s3, aligned_edge=LEFT)
        self.play(FadeOut(VGroup(hl2, bc)), ReplacementTransform(s3, s4), FadeIn(H[5]), run_time=0.6)
        Q = [v * v for v in DX]
        qcol = VGroup(*[T(f"{v}", 30, AQUA).move_to([cols_x[5], y, 0]) for v, y in zip(Q, ry)])
        self.until(word_time("s067", word_index("s067", "One")))
        self.play(LaggedStart(*[FadeIn(q, shift=LEFT * 0.2) for q in qcol], lag_ratio=0.35), run_time=3.2)
        tot2 = T("250", 34, AQUA, weight=BOLD).move_to([cols_x[5], -1.5, 0])
        line2 = Line([cols_x[5] - 0.6, -1.15, 0], [cols_x[5] + 0.6, -1.15, 0], color=AQUA, stroke_width=2)
        self.until(word_time("s067", word_index("s067", "That")))
        self.play(Create(line2), FadeIn(tot2, scale=0.6), run_time=0.6)

        # ── s068 spread of sizes ──
        self.at("s068", 0.0)
        sp = VGroup(T("the spread of the sizes", 24, AQUA), T("(a cousin of variance)", 24, AQUA)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        sp.move_to([-6.7, -2.15, 0], aligned_edge=LEFT)
        self.play(FadeIn(sp), Indicate(tot2, color=AQUA), run_time=0.8)

        # ── s069 step five: divide → slope 10 ──
        self.at("s069", 0.0)
        s5 = step_chip(5, "divide", VIOLET, 26).scale(0.85).move_to(s4, aligned_edge=LEFT)
        self.play(ReplacementTransform(s4, s5), FadeOut(sp), FadeOut(sig), run_time=0.5)
        fr_ = MathTex(r"{2{,}500 \over 250}", r"= 10", font_size=64)
        fr_[0].set_color(INK); fr_[1].set_color(VIOLET)
        fr_.scale(0.75).move_to([-6.7, -1.55, 0], aligned_edge=LEFT)
        self.play(TransformFromCopy(VGroup(tot1, tot2), fr_[0]), run_time=0.9)
        self.until(word_time("s069", word_index("s069", "ten.")))
        self.play(FadeIn(fr_[1], shift=LEFT * 0.2), run_time=0.5)
        slc = pill("slope = 10", VIOLET, 28).move_to([-6.7, -2.35, 0], aligned_edge=LEFT)
        self.until(word_time("s069", word_index("s069", "slope.")))
        self.play(FadeIn(slc, scale=0.7), run_time=0.5)

        # ── s070 last step: the intercept ──
        self.at("s070", 0.0)
        table = VGroup(H, rule, rows_m, u1, u2, avg_r, dcol, ecol, pcol, qcol, tot1, tot2, line1, line2, fr_)
        small = VGroup(axg.ax, best, dots, av, hv, hh, arrows)
        self.play(FadeOut(table), FadeOut(s5), FadeOut(VGroup(axg.ax, best, dots, av, hv, hh, arrows)), run_time=0.6)
        self.drop(axg, best, dots, av, hv, hh, arrows, table, s5)
        # rebuild the full chart exactly where lesson_axes() puts it
        axg2 = lesson_axes(); ax2 = axg2.ax
        dots2 = house_dots(ax2); best2 = price_line(ax2, *BEST, 0, 3500)
        av2 = Dot(ax2.c2p(2000, 250), radius=0.17, color=BLUE_).set_stroke(INK, 3); av2.qa_dot = True
        self.play(FadeIn(axg2), FadeIn(best2), FadeIn(dots2), FadeIn(av2), slc.animate.move_to(RIGHT * PANEL_X + UP * 2.3), run_time=0.7)
        s6 = step_chip(6, "walk back to zero size", VIOLET, 24).move_to([2.25, 1.5, 0], aligned_edge=LEFT)
        self.play(FadeIn(s6), run_time=0.4)
        ar = T("250 − 10 × 20 = 50", 34, INK, weight=BOLD).move_to(RIGHT * PANEL_X + UP * 0.5)
        self.until(word_time("s070", word_index("s070", "Two")))
        self.play(Write(ar), run_time=1.2)
        icp = Dot(ax2.c2p(0, 50), radius=0.14, color=VIOLET).set_stroke(INK, 2); icp.qa_dot = True
        ic = pill("intercept = 50", VIOLET, 30).next_to(ar, DOWN, buff=0.35)
        self.until(word_time("s070", word_index("s070", "intercept.")))
        self.play(FadeIn(icp, scale=0.4), FadeIn(ic, scale=0.7), run_time=0.6)

        # ── s071a walk the steps on the picture ──
        self.at("s071a", 0.0)
        cnt = T("−$10k × 0", 30, WARN, weight=BOLD).move_to(RIGHT * PANEL_X + DOWN * 1.35)
        self.play(FadeIn(cnt), Indicate(av2, color=BLUE_), run_time=0.6)
        self.until(word_time("s071a", word_index("s071a", "Walk")))
        steps = VGroup()
        for i in range(20):
            x0 = 2000 - 100 * i; x1 = x0 - 100
            st = VGroup(Line(ax2.c2p(x0, 50 + 0.1 * x0), ax2.c2p(x1, 50 + 0.1 * x0)),
                        Line(ax2.c2p(x1, 50 + 0.1 * x0), ax2.c2p(x1, 50 + 0.1 * x1))).set_stroke(WARN, 3)
            steps.add(st)
        tr = ValueTracker(0)
        cnt.add_updater(lambda m: m.become(T(f"−$10k × {int(tr.get_value())}", 30, WARN, weight=BOLD).move_to(RIGHT * PANEL_X + DOWN * 1.35)))
        self.play(LaggedStart(*[Create(s) for s in steps], lag_ratio=0.7), tr.animate.set_value(20), run_time=5.0, rate_func=linear)
        cnt.clear_updaters()
        res = T("= −$200k", 30, WARN, weight=BOLD).next_to(cnt, DOWN, buff=0.2)
        self.play(FadeIn(res), run_time=0.4)
        self.until(word_time("s071a", word_index("s071a", "Fifty")))
        self.play(Flash(icp, color=VIOLET, line_length=0.25), Indicate(ic, color=VIOLET), run_time=0.8)

        # ── s071 the whole recipe as symbols ──
        self.at("s071", 0.0)
        self.play(FadeOut(VGroup(axg2, best2, dots2, av2, icp, steps, cnt, res, s6, ar, ic, slc)), run_time=0.6)
        self.drop(axg2, best2, dots2, av2, icp, steps, cnt, res, s6, ar, ic, slc)
        fb = MathTex(r"b", r"=", r"{\Sigma", r"(x-\bar{x})(y-\bar{y})", r"\over", r"\Sigma", r"(x-\bar{x})^2}", font_size=72)
        fb[0].set_color(VIOLET); fb[2].set_color(WARN); fb[5].set_color(WARN)
        fa = MathTex(r"a", r"=", r"\bar{y}", r"-", r"b", r"\,\bar{x}", font_size=72)
        fa[0].set_color(VIOLET); fa[4].set_color(VIOLET)
        form = VGroup(fb, fa).arrange(RIGHT, buff=1.4).move_to(UP * 1.55)
        box = card(form.width + 1.0, form.height + 0.8, color=VIOLET).move_to(form)
        self.play(FadeIn(box), Write(fb), run_time=1.4)
        self.play(Write(fa), run_time=0.9)

        # ── s072 every symbol in words ──
        self.at("s072", 0.0)
        defs = [("x", "size", "x"), ("y", "price", "y"), (r"\bar{x}", "average size", "bar"),
                (r"\bar{y}", "average price", "bar"), (r"\Sigma", "add them all up", "sigma")]
        cards = VGroup(*[defcard(s, w, color=(WARN if s == r"\Sigma" else (BLUE_ if "bar" in s else INK)), fs=26) for s, w, _ in defs])
        cards[:3].arrange(RIGHT, buff=0.3)
        cards[3:].arrange(RIGHT, buff=0.3)
        VGroup(cards[:3], cards[3:]).arrange(DOWN, buff=0.3).move_to(DOWN * 1.15)
        when = ["x", "y", "x", "averages.", "sigma"]
        ws = [w.strip(",.").lower() for w in SEGS["s072"]["text"].split()]
        idxs = [ws.index("x"), ws.index("y"), ws.index("bar"), ws.index("averages"), ws.index("sigma")]
        for c, j in zip(cards, idxs):
            self.until(word_time("s072", j) - 0.1)
            self.play(FadeIn(c, shift=UP * 0.2), run_time=0.45)

        # ── s073 b = 10, a = 50 ──
        self.at("s073", 0.0)
        self.play(FadeOut(cards), run_time=0.4)
        bl = T("b = 10   slope", 34, VIOLET, weight=BOLD)
        al_ = T("a = 50   intercept", 34, VIOLET, weight=BOLD)
        ans = VGroup(bl, al_).arrange(RIGHT, buff=1.2).move_to(DOWN * 0.85)
        self.play(FadeIn(bl, shift=UP * 0.2), run_time=0.5)
        self.until(word_time("s073", word_index("s073", "a")) + 0.2)
        self.play(FadeIn(al_, shift=UP * 0.2), run_time=0.5)
        ok = VGroup(check(AQUA, 0.35), T("exactly the line our search found", 30, INK)).arrange(RIGHT, buff=0.3).next_to(ans, DOWN, buff=0.5)
        self.until(word_time("s073", word_index("s073", "Exactly")))
        self.play(FadeIn(ok), run_time=0.5)
        self.until(SEGS["s073"]["end"] - 0.1)
        self.play(FadeOut(VGroup(box, fb, fa, ans, ok)), run_time=0.45)
        self.finish()
