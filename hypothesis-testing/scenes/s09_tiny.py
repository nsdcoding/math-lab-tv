import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *
from math import erfc, sqrt


def gear(r=0.5, color=INK2, teeth=8):
    pts = []
    for k in range(teeth * 2):
        a = TAU * k / (teeth * 2)
        rr = r if k % 2 == 0 else r * 0.78
        pts += [np.array([rr * np.cos(a - 0.12), rr * np.sin(a - 0.12), 0]), np.array([rr * np.cos(a + 0.12), rr * np.sin(a + 0.12), 0])]
    g = Polygon(*pts).set_stroke(color, 4).set_fill("#22221f", 1)
    h = Circle(r * 0.28).set_stroke(color, 4)
    return VGroup(g, h)


class S09Tiny(Base):
    CHAPTER = "Tiny p, Tiny Effect"

    def construct(self):
        # ── s082 back to "not a measure of size" ──
        self.at("s082", 0.0)
        c2 = VGroup(card(5.2, 2.0, RED_), TB("NOT", 40, RED_), T("how big the effect is", 34, INK, weight=BOLD))
        VGroup(c2[1], c2[2]).arrange(DOWN, buff=0.22).move_to(c2[0])
        c2.move_to(UP * 0.6)
        self.play(FadeIn(c2, scale=0.8), run_time=0.6)
        self.word("s082", "size", dt=-0.3)
        ruler = VGroup(Rectangle(width=3.6, height=0.5).set_stroke(WARN, 3).set_fill("#22221f", 1),
                       *[Line(UP * 0.25, UP * (0.25 - (0.22 if k % 2 == 0 else 0.12))).set_stroke(WARN, 2).shift(LEFT * 1.8 + RIGHT * 0.36 * k)
                         for k in range(11)])
        ruler[0].qa_container = True
        for x in ruler[1:]: x.qa_ignore = True
        ruler.next_to(c2, DOWN, buff=0.45)
        self.play(FadeIn(ruler[0], shift=UP * 0.2), LaggedStart(*[Create(x) for x in ruler[1:]], lag_ratio=0.06), run_time=0.7)
        self.idle(lambda: pulse(c2, 1.06))

        # ── s083 an almost-fair coin: 50.2% heads ──
        self.at("s083", 0.0)
        self.idle()
        ax = NumberLine(x_range=[49, 51, 0.5], length=8.0, color=INK2, stroke_width=3, include_tip=False, tick_size=0.08).move_to(DOWN * 1.0 + RIGHT * 0.8)
        axl = VGroup(*[T(f"{v:g}%", 22, INK2).next_to(ax.n2p(v), DOWN, buff=0.15) for v in (49, 49.5, 50, 50.5, 51)])
        axt = T("chance of heads (zoomed in)", 24, MUTED).next_to(axl, DOWN, buff=0.15).align_to(ax, RIGHT)
        bf = Rectangle(width=ax.n2p(50)[0] - ax.n2p(49)[0], height=0.45).set_stroke(width=0).set_fill(BLUE_, 0.9)
        bt = Rectangle(width=ax.n2p(50.2)[0] - ax.n2p(49)[0], height=0.45).set_stroke(width=0).set_fill(ORANGE_, 0.9)
        bf.move_to(ax.n2p(49), aligned_edge=LEFT).shift(UP * 1.6)
        bt.move_to(ax.n2p(49), aligned_edge=LEFT).shift(UP * 0.9)
        lf = T("fair coin: 50%", 26, BLUE_, weight=BOLD).next_to(bf, LEFT, buff=0.25)
        lt = T("this coin: 50.2%", 26, ORANGE_, weight=BOLD).next_to(bt, LEFT, buff=0.25)
        self.play(FadeOut(VGroup(c2, ruler), shift=UP * 0.4), run_time=0.4)
        self.play(Create(ax), FadeIn(axl), FadeIn(axt), run_time=0.5)
        self.play(GrowFromEdge(bf, LEFT), FadeIn(lf), run_time=0.5)
        self.word("s083", "fifty", dt=-0.3)
        self.play(GrowFromEdge(bt, LEFT), FadeIn(lt), run_time=0.7)
        hair = Brace(VGroup(Line(bf.get_right(), bf.get_right() + UP * 0.01), Line(bt.get_right(), bt.get_right())), RIGHT, buff=0.1, color=WARN)
        hl = T("a hair", 26, WARN, weight=BOLD).next_to(hair, RIGHT, buff=0.12)
        self.word("s083", "hair", dt=-0.3)
        diff = DoubleArrow(ax.n2p(50) + UP * 2.25, ax.n2p(50.2) + UP * 2.25, buff=0, color=WARN, stroke_width=4, tip_length=0.12)
        dl = T("0.2%", 26, WARN, weight=BOLD).next_to(diff, UP, buff=0.08)
        self.play(GrowFromCenter(diff), FadeIn(dl), run_time=0.5)
        self.idle(lambda: pulse(bt, 1.05), lambda: Indicate(dl, color=WARN, scale_factor=1.3))

        # ── s084 twenty flips: you'd never notice; a machine flips a million ──
        self.at("s084", 0.0)
        self.idle()
        stage = VGroup(ax, axl, axt, bf, bt, lf, lt, diff, dl)
        g = gear(0.7).move_to(LEFT * 4.0 + UP * 0.6)
        never = pill("20 flips: you'd never notice", MUTED, 28).move_to(UP * 2.4)
        push(self, stage, never, UP, run_time=0.6)
        self.word("s084", "machine", dt=-0.3)
        self.play(FadeIn(g, scale=0.5), never.animate.set_opacity(0.3), run_time=0.4)
        nf = ValueTracker(0); nh = ValueTracker(0)
        cf = always_redraw(lambda: T(f"{int(nf.get_value()):,} flips", 46, INK, weight=BOLD).move_to(RIGHT * 1.6 + UP * 1.0))
        chh = always_redraw(lambda: T(f"{int(nh.get_value()):,} heads", 46, WARN, weight=BOLD).move_to(RIGHT * 1.6 + DOWN * 0.1))
        self.add(cf, chh)
        self.play(nf.animate.set_value(1_000_000), nh.animate.set_value(502_000), Rotate(g, -4 * TAU), run_time=2.2, rate_func=rate_functions.ease_in_out_sine)
        cf.clear_updaters(); chh.clear_updaters()
        self.play(ripple(chh.get_center(), WARN, r=0.6, scale=3), run_time=0.5)
        self.idle(lambda: Rotate(g, -TAU / 3), lambda: pulse(chh, 1.08))

        # ── s085 fair-coin spread over a million flips ≈ 500; 2,000 extra = 4 spreads ──
        self.at("s085", 0.0)
        self.idle()
        bx = xy_axes([497500, 503000, 500], [0, 1, 0.25], 11.0, 3.2, "heads in 1,000,000 flips",
                     "runs per 1,000", x_labels={v: f"{v // 1000}k" for v in range(498000, 503001, 1000)}, font_size=22, y_vertical=True)
        bx.move_to(RIGHT * 0.5 + UP * 0.2)
        bax = bx.ax
        def dens(x): return 1000 * np.exp(-((x - 500000) / 500) ** 2 / 2) / (500 * np.sqrt(TAU))
        curve = bax.plot(dens, x_range=[497500, 503000, 20], color=BLUE_, stroke_width=5)
        push(self, VGroup(g, never, cf, chh), VGroup(bx), LEFT, run_time=0.7)
        self.play(Create(curve), run_time=0.9)
        self.word("s085", "spread", dt=-0.3)
        sps = VGroup(*[DoubleArrow(bax.c2p(500000 + 500 * i, 0.9), bax.c2p(500000 + 500 * (i + 1), 0.9), buff=0, color=VIOLET,
                                   stroke_width=3, tip_length=0.12) for i in range(4)])
        spl = T("1 spread ≈ 500 heads", 24, VIOLET, weight=BOLD).next_to(sps[0], UP, buff=0.1).shift(LEFT * 0.6)
        self.play(GrowFromCenter(sps[0]), FadeIn(spl), run_time=0.5)
        self.word("s085", "Two", dt=-0.3)
        pin = marker(bax.x_axis, 502000, WARN, "502,000", height=0.6, fs=26)
        self.play(FadeIn(pin, shift=DOWN * 0.5), run_time=0.4)
        self.word("s085", "four", dt=-0.3)
        self.play(LaggedStart(*[GrowFromEdge(s_, LEFT) for s_ in sps[1:]], lag_ratio=0.3), run_time=0.8)
        fourl = T("4 spreads", 26, VIOLET, weight=BOLD).next_to(sps[3], RIGHT, buff=0.15)
        self.play(FadeIn(fourl), run_time=0.3)
        self.idle(lambda: LaggedStart(*[Indicate(s_, color=VIOLET, scale_factor=1.15) for s_ in sps], lag_ratio=0.2))

        # ── s086 p ≈ 0.00003: incredibly significant ──
        self.at("s086", 0.0)
        self.idle()
        area = bax.get_area(curve, x_range=[502000, 503000], color=AQUA, opacity=0.9)
        area.qa_ignore = True
        self.play(FadeIn(area), ripple(bax.c2p(502300, 0.02), AQUA, r=0.2, scale=5), run_time=0.6)
        pbig = glow(TB("p ≈ 0.00003", 48, AQUA), AQUA).move_to(bax.c2p(502050, 0.72))
        self.play(FadeOut(VGroup(sps, spl, fourl)), run_time=0.3)
        self.word("s086", "zero", dt=-0.3)
        self.play(FadeIn(pbig, scale=0.6), run_time=0.5)
        sub = T("3 in 100,000", 30, AQUA, weight=BOLD).next_to(pbig, DOWN, buff=0.2)
        self.word("s086", "Three", dt=-0.3)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.4)
        hs = pill("incredibly significant", AQUA, 28).rotate(-4 * DEGREES).move_to(bax.c2p(498500, 0.62))
        self.word("s086", "Incredibly", dt=-0.3)
        self.play(FadeIn(hs, scale=1.6), run_time=0.35, rate_func=rate_functions.ease_out_cubic)
        self.idle(lambda: pulse(pbig, 1.08), lambda: pulse(hs, 1.12))

        # ── s087 but does it matter? ≈ 2 extra coffees per 1,000 ──
        self.at("s087", 0.0)
        self.idle()
        cx = xy_axes([0, 3, 1], [0, 600, 100], 5.0, 3.4, None, "coffees you pay for (of 1,000)", x_labels={}, font_size=22, y_vertical=True)
        cx.move_to(LEFT * 1.6 + DOWN * 0.05)
        cax = cx.ax
        b500 = bar(cax, 1, 500, BLUE_, width=1.1); b502 = bar(cax, 2, 502, ORANGE_, width=1.1)
        l1 = T("fair coin\n500", 24, BLUE_, weight=BOLD).next_to(cax.c2p(1, 0), DOWN, buff=0.15)
        l2 = T("this coin\n502", 24, ORANGE_, weight=BOLD).next_to(cax.c2p(2, 0), DOWN, buff=0.15)
        push(self, VGroup(bx, curve, pin, area, pbig, sub, hs), VGroup(cx, l1, l2), LEFT, run_time=0.7)
        self.word("s087", "coffee", dt=-0.3)
        self.play(GrowFromEdge(b500, DOWN), GrowFromEdge(b502, DOWN), run_time=0.8)
        cups = VGroup(*[cup(WARN, 0.55) for _ in range(2)]).arrange(RIGHT, buff=0.3).move_to(RIGHT * 4.0 + UP * 0.7)
        two = T("+2 per 1,000", 34, WARN, weight=BOLD).next_to(cups, DOWN, buff=0.3)
        self.word("s087", "two", dt=-0.3)
        self.play(LaggedStart(*[FadeIn(c_, shift=DOWN * 0.5) for c_ in cups], lag_ratio=0.3), FadeIn(two), run_time=0.7)
        shrug = pill("hardly matters", MUTED, 28).next_to(two, DOWN, buff=0.35)
        self.play(FadeIn(shrug, shift=UP * 0.2), run_time=0.4)
        self.idle(lambda: LaggedStart(*[pulse(c_, 1.2) for c_ in cups], lag_ratio=0.3), lambda: pulse(b502, 1.03))

        # ── s087a the other way: big effect, little data → big p (the 70% coin) ──
        self.at("s087a", 0.0)
        self.idle()
        def mini(title, sub_, color, tag, tagc):
            c = card(5.6, 3.2, color)
            t_ = TB(title, 32, color)
            s_ = T(sub_, 26, INK)
            tg = pill(tag, tagc, 28)
            VGroup(t_, s_, tg).arrange(DOWN, buff=0.3).move_to(c)
            return VGroup(c, t_, s_, tg)
        L = mini("tiny effect, huge data", "50.2% coin · 1,000,000 flips", AQUA, "tiny p", AQUA).move_to(LEFT * 3.1 + UP * 0.5)
        R = mini("big effect, little data", "70% coin · 20 flips", ORANGE_, "often a big p", RED_).move_to(RIGHT * 3.1 + UP * 0.5)
        push(self, VGroup(cx, b500, b502, l1, l2, cups, two, shrug), L, LEFT, run_time=0.7)
        self.word("s087a", "big", dt=-0.3)
        self.play(FadeIn(R, shift=LEFT * 0.6), run_time=0.6)
        miss = pill("missed > half the time", RED_, 26).next_to(R, DOWN, buff=0.3)
        self.word("s087a", "missed", dt=-0.3)
        self.play(FadeIn(miss, shift=UP * 0.2), run_time=0.4)
        self.idle(lambda: pulse(R, 1.05), lambda: pulse(L, 1.05))

        # ── s088 two questions: is it there? how big is it? ──
        self.at("s088", 0.0)
        self.idle()
        q1 = VGroup(card(5.6, 2.4, AQUA), TB("is it there?", 40, AQUA), T("→ the p value", 30, INK, weight=BOLD))
        q2 = VGroup(card(5.6, 2.4, ORANGE_), TB("how big is it?", 40, ORANGE_), T("→ the effect size", 30, INK, weight=BOLD))
        for q in (q1, q2):
            VGroup(q[1], q[2]).arrange(DOWN, buff=0.3).move_to(q[0])
        q1.move_to(LEFT * 3.1 + UP * 0.5); q2.move_to(RIGHT * 3.1 + UP * 0.5)
        push(self, VGroup(L, R, miss), q1, LEFT, run_time=0.7)
        self.word("s088", "not", dt=-0.3)
        self.play(FadeIn(q2, shift=LEFT * 0.6), run_time=0.5)
        self.idle(lambda: pulse(q1, 1.06), lambda: pulse(q2, 1.06))

        # ── s089 with enough data, any tiny difference becomes significant ──
        self.at("s089", 0.0)
        self.idle()
        px = xy_axes([1, 6, 1], [0, 0.5, 0.1], 8.0, 3.3, "number of flips", "p value", x_labels={2: "100", 3: "1,000", 4: "10,000", 5: "100,000", 6: "1 million"},
                     font_size=22, y_vertical=True)
        px.move_to(LEFT * 0.9 + DOWN * 0.1)
        pax = px.ax
        def pv(e): return 0.5 * erfc((0.002 * sqrt(10 ** e) / 0.5) / sqrt(2))
        pc = pax.plot(pv, x_range=[2, 6, 0.02], color=AQUA, stroke_width=5)
        tl = T("50.2% coin (approximation)", 22, MUTED).next_to(px, UP, buff=0.05).align_to(px, RIGHT)
        push(self, VGroup(q1, q2), VGroup(px, tl), LEFT, run_time=0.7)
        aline = DashedLine(pax.c2p(1, 0.05), pax.c2p(6, 0.05), color=VIOLET, stroke_width=4)
        al_ = T("α = 0.05", 24, VIOLET, weight=BOLD).next_to(aline, RIGHT, buff=0.1)
        self.play(Create(aline), FadeIn(al_), run_time=0.4)
        self.word("s089", "tiny", dt=-0.4)
        self.play(Create(pc), run_time=1.4)
        cross_pt = Dot(pax.c2p(5.228, 0.05), radius=0.1, color=WARN)
        cl = T("significant!", 24, WARN, weight=BOLD).next_to(cross_pt, UP + RIGHT, buff=0.1)
        self.play(FadeIn(cross_pt, scale=2), FadeIn(cl), run_time=0.4)
        chk = VGroup(VGroup(check(AQUA, 0.28), T("p value", 28, INK, weight=BOLD)).arrange(RIGHT, buff=0.2),
                     VGroup(check(ORANGE_, 0.28), T("effect size", 28, INK, weight=BOLD)).arrange(RIGHT, buff=0.2)
                     ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 5.0 + UP * 1.4)
        chk_box = card(chk.width + 0.6, chk.height + 0.5, INK2).move_to(chk)
        self.word("s089", "both", dt=-0.3)
        self.play(FadeIn(chk_box), FadeIn(chk[0], shift=LEFT * 0.2), run_time=0.4)
        self.play(FadeIn(chk[1], shift=LEFT * 0.2), run_time=0.4)
        self.idle(lambda: pulse(chk_box, chk, s=1.12), lambda: AnimationGroup(Indicate(cross_pt, color=WARN, scale_factor=2.2), pulse(cl, 1.2)))
        self.until(self.ch["t1"] - 0.55)
        self.idle()
        self.play(FadeOut(VGroup(px, tl, pc, aline, al_, cross_pt, cl, chk, chk_box), shift=LEFT * 1.0), run_time=0.5)
        self.finish()
