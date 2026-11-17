import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def p_meter(length=10.0):
    """A p-value number line 0 … 0.10 (ticks every 0.01, labels every 0.02)."""
    nl = NumberLine(x_range=[0, 0.10, 0.01], length=length, color=INK2, stroke_width=3, include_tip=False, tick_size=0.08)
    nums = VGroup(*[T(f"{v:.2f}", 22, INK2).next_to(nl.n2p(v), DOWN, buff=0.16) for v in np.arange(0, 0.101, 0.02)])
    tt = T("p value", 24, MUTED).next_to(nums, DOWN, buff=0.18).align_to(nl, RIGHT)
    g = VGroup(nl, nums, tt); g.nl = nl
    return g


def alpha_line(nl, v=0.05, h=1.6, color=VIOLET):
    ln = Line(nl.n2p(v) + UP * 0.12, nl.n2p(v) + UP * h).set_stroke(color, 6)
    lab = MathTex(r"\alpha = 0.05", font_size=40, color=color).next_to(ln, UP, buff=0.12)
    return VGroup(ln, lab)


class S06Line(Base):
    CHAPTER = "Drawing the Line"

    def construct(self):
        rng = np.random.default_rng(6)
        # ── s048 two in a hundred: rare enough? ──
        self.at("s048", 0.0)
        ch = dist_chart().move_to(RIGHT * 0.6 + UP * 0.3)
        ax = ch.ax
        bars = dist_bars(ax, BLUE_)
        for k in range(15, 21): bars[k].set_fill(AQUA, 1)
        self.play(FadeIn(ch, shift=LEFT * 0.6), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), run_time=0.9)
        pv = pill("p ≈ 0.021", AQUA, 34).move_to(ax.c2p(17, 120))
        self.play(FadeIn(pv, scale=0.6), ripple(ax.c2p(16, 5), AQUA, r=0.3, scale=4), run_time=0.6)
        q = pill("rare enough to call it rigged?", WARN, 30).move_to(UP * 3.2 + RIGHT * 2.6)
        self.word("s048", "rare", dt=-0.3)
        self.play(FadeIn(q, shift=DOWN * 0.3), run_time=0.5)
        self.idle(lambda: LaggedStart(*[drop_into(ax, int(k_), BLUE_, 185) for k_ in rng.choice([5, 6, 7, 13, 14, 15, 16], 9)], lag_ratio=0.1),
                  lambda: pulse(q, 1.08))

        # ── s049 choose a cut-off before looking: the significance level, alpha ──
        self.at("s049", 0.0)
        self.idle()
        mt = p_meter(11.0).move_to(DOWN * 0.6)
        stage = VGroup(ch, bars, pv)
        self.play(FadeOut(q), run_time=0.2)
        push(self, stage, mt, LEFT, run_time=0.8)
        al = alpha_line(mt.nl, 0.10, 1.6)
        al.shift(mt.nl.n2p(0.10) - mt.nl.n2p(0.10))
        self.word("s049", "cut", dt=-0.3)
        self.play(Create(al[0]), run_time=0.4)
        self.play(al[0].animate.move_to(mt.nl.n2p(0.05) + UP * (al[0].height / 2 + 0.12)), run_time=0.9, rate_func=smooth)
        lid = VGroup(Arc(radius=0.45, start_angle=PI * 0.15, angle=PI * 0.7).set_stroke(INK, 5),
                     *[Line(UP * 0, DOWN * 0.18).set_stroke(INK, 4).shift(RIGHT * x) for x in (-0.25, 0, 0.25)])
        lid.move_to(UP * 2.6 + LEFT * 3.2)
        before = T("chosen BEFORE looking", 30, INK, weight=BOLD).next_to(lid, RIGHT, buff=0.4)
        self.word("s049", "before", dt=-0.2)
        self.play(FadeIn(lid, scale=0.6), FadeIn(before, shift=LEFT * 0.3), run_time=0.5)
        dA = defcard(r"\alpha", "significance level: the cut-off", VIOLET, fs=30).move_to(UP * 1.75 + LEFT * 2.6)
        self.word("s049", "significance", dt=-0.2)
        self.play(FadeIn(dA, shift=UP * 0.2), run_time=0.5)
        self.word("s049", "Greek", dt=-0.2)
        self.play(Indicate(dA[1][0], color=VIOLET, scale_factor=1.5), run_time=0.7)
        self.idle(lambda: pulse(dA, 1.08), lambda: al[0].animate(rate_func=there_and_back).shift(RIGHT * 0.25))

        # ── s050 the common choice: 0.05, one in twenty ──
        self.at("s050", 0.0)
        self.idle()
        al[1].next_to(al[0].get_top(), RIGHT, buff=0.18).shift(DOWN * 0.15)
        self.play(FadeOut(VGroup(lid, before)), dA.animate.move_to(UP * 2.75 + LEFT * 1.6), Write(al[1]), run_time=0.6)
        row = VGroup(*[Square(0.34).set_stroke(MUTED, 2).set_fill(VIOLET if i == 0 else "#22221f", 1) for i in range(20)]).arrange(RIGHT, buff=0.06)
        row.move_to(UP * 1.95 + RIGHT * 0.3)
        for s_ in row: s_.qa_joined = True
        one20 = T("1 in 20", 30, VIOLET, weight=BOLD).next_to(row, RIGHT, buff=0.3)
        self.word("s050", "One", dt=-0.3)
        self.play(LaggedStart(*[FadeIn(s_, scale=0.4) for s_ in row], lag_ratio=0.04), FadeIn(one20), run_time=0.9)
        self.idle(lambda: Indicate(row[0], color=VIOLET, scale_factor=1.5), lambda: pulse(al[1], 1.12))

        # ── s051 the rule: p < alpha → significant → reject the boring explanation ──
        self.at("s051", 0.0)
        self.idle()
        rule = VGroup(MathTex("p", font_size=72, color=AQUA), MathTex("<", font_size=72, color=INK),
                      MathTex(r"\alpha", font_size=72, color=VIOLET), T("→", 56, INK2),
                      T("statistically significant", 40, INK, weight=BOLD)).arrange(RIGHT, buff=0.3)
        rbox = card(rule.width + 0.8, rule.height + 0.6, INK2)
        rule_c = VGroup(rbox, rule).scale(0.85).move_to(UP * 2.35)
        rule.move_to(rbox)
        self.play(FadeOut(VGroup(row, one20, dA), shift=UP * 0.3), run_time=0.4)
        self.play(FadeIn(rbox), LaggedStart(*[FadeIn(x_, shift=UP * 0.2) for x_ in rule[:3]], lag_ratio=0.25), run_time=0.8)
        self.word("s051", "significant", dt=-0.4)
        self.play(FadeIn(rule[3:], shift=LEFT * 0.3), run_time=0.5)
        nullc = pill("H₀: the coin is fair", BLUE_, 30).move_to(UP * 0.6 + LEFT * 3.6)
        self.word("s051", "reject", dt=-0.4)
        self.play(FadeIn(nullc, shift=RIGHT * 0.3), run_time=0.35)
        self.play(nullc.animate.shift(LEFT * 1.2).set_opacity(0.3), run_time=0.6, rate_func=rate_functions.ease_in_back)
        rej = pill("reject H₀", RED_, 30).next_to(nullc, RIGHT, buff=0.4)
        self.play(FadeIn(rej, scale=1.5), run_time=0.4)
        self.idle(lambda: pulse(rule_c, 1.05), lambda: pulse(rej, 1.12))

        # ── s052 our p = 0.021 lands below 0.05: reject ──
        self.at("s052", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(nullc, rej)), rule_c.animate.scale(0.75).move_to(UP * 2.9 + RIGHT * 1.8), run_time=0.5)
        mk = marker(mt.nl, 0.10, AQUA, "our p = 0.021", height=1.0, fs=28)
        self.word("s052", "zero", dt=-0.3)
        self.play(FadeIn(mk, shift=DOWN * 0.4), run_time=0.4)
        self.play(mk.animate.shift(mt.nl.n2p(0.021) - mt.nl.n2p(0.10)), run_time=1.4, rate_func=smooth)
        zone = Rectangle(width=mt.nl.n2p(0.05)[0] - mt.nl.n2p(0)[0], height=0.5).set_stroke(width=0).set_fill(AQUA, 0.18)
        zone.move_to(mt.nl.n2p(0.025) + UP * 0.25); zone.qa_ignore = True
        zl = T("significant zone", 24, AQUA, weight=BOLD).next_to(zone, DOWN, buff=0.75)
        self.word("s052", "below", dt=-0.2)
        self.play(FadeIn(zone), FadeIn(zl), ripple(mt.nl.n2p(0.021), AQUA, r=0.2, scale=5), run_time=0.6)
        stamp = pill("reject “the coin is fair”", RED_, 30).rotate(-3 * DEGREES).move_to(DOWN * 2.05 + RIGHT * 3.4)
        self.word("s052", "reject", dt=-0.3)
        self.play(FadeIn(stamp, scale=1.6), run_time=0.4, rate_func=rate_functions.ease_out_cubic)
        self.idle(lambda: pulse(stamp, 1.1), lambda: mk.animate(rate_func=there_and_back).shift(UP * 0.2))

        # ── s053 the line is not a law of nature: somebody chose it ──
        self.at("s053", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(stamp, zone, zl, mk)), run_time=0.4)
        self.word("s053", "line", dt=-0.2)
        self.play(Wiggle(al, scale_value=1.15, rotation_angle=0.05 * TAU), run_time=0.9)
        law = pill("not a law of nature", INK, 30).move_to(DOWN * 2.05 + LEFT * 3.4)
        self.word("s053", "law", dt=-0.3)
        self.play(FadeIn(law, shift=LEFT * 0.3), run_time=0.4)
        hand = person(INK, 0.9).next_to(al[0], RIGHT, buff=0.15).shift(DOWN * 0.55)
        chose = T("somebody chose it", 30, VIOLET, weight=BOLD).next_to(hand, RIGHT, buff=0.3)
        self.word("s053", "Somebody", dt=-0.2)
        self.play(FadeIn(hand, shift=LEFT * 0.4), FadeIn(chose), run_time=0.5)
        self.idle(lambda: AnimationGroup(al.animate(rate_func=there_and_back).shift(LEFT * 0.4), hand.animate(rate_func=there_and_back).shift(LEFT * 0.4)))

        # ── s054 Fisher: 1 in 20, a 1920s rule of thumb, and it stuck ──
        self.at("s054", 0.0)
        self.idle()
        tl_ = NumberLine(x_range=[1920, 2030, 10], length=10.5, color=INK2, stroke_width=3, include_tip=False, tick_size=0.07).move_to(DOWN * 1.0)
        yrs = VGroup(*[T(str(y), 22, INK2).next_to(tl_.n2p(y), DOWN, buff=0.15) for y in (1920, 1950, 1980, 2010)])
        ytt = T("year", 24, MUTED).next_to(yrs, DOWN, buff=0.15).align_to(tl_, RIGHT)
        stage2 = VGroup(mt, al, law, hand, chose, rule_c)
        push(self, stage2, VGroup(tl_, yrs, ytt), LEFT, run_time=0.8)
        f1 = diamond(tl_, 1925, VIOLET, "Fisher: “1 in 20”", height=1.2, fs=28)
        self.word("s054", "Fisher", dt=-0.2)
        self.play(FadeIn(f1, shift=DOWN * 0.5), run_time=0.5)
        span = DoubleArrow(tl_.n2p(1925) + UP * 0.45, tl_.n2p(2026) + UP * 0.45, buff=0, color=WARN, stroke_width=4, tip_length=0.18)
        span_l = T("about 100 years", 26, WARN, weight=BOLD).next_to(span, UP, buff=0.12).shift(RIGHT * 2.2)
        self.word("s054", "hundred", dt=-0.3)
        self.play(GrowFromEdge(span, LEFT), FadeIn(span_l), run_time=0.8)
        rot = pill("a convenient rule of thumb", INK, 28).move_to(UP * 2.3 + RIGHT * 2.0)
        self.word("s054", "convenient", dt=-0.3)
        self.play(FadeIn(rot, shift=DOWN * 0.2), run_time=0.4)
        stuck = pill("it stuck", WARN, 30).rotate(-5 * DEGREES).next_to(tl_.n2p(2026), UP, buff=1.25)
        self.word("s054", "stuck", dt=-0.3)
        self.play(FadeIn(stuck, scale=1.6), run_time=0.35, rate_func=rate_functions.ease_out_cubic)
        self.idle(lambda: pulse(stuck, 1.12), lambda: pulse(f1, 1.1))

        # ── s055 other fields draw the line elsewhere: a ladder of thresholds ──
        self.at("s055", 0.0)
        self.idle()
        lad = NumberLine(x_range=[1, 7, 1], length=10.5, color=INK2, stroke_width=3, include_tip=False, tick_size=0.08).move_to(DOWN * 0.9)
        llab = VGroup(*[T(s, 22, INK2).next_to(lad.n2p(v), DOWN, buff=0.15) for v, s in
                        [(1, "1 in 10"), (2, "1 in 100"), (3, "1 in 1,000"), (4, "1 in 10k"), (5, "1 in 100k"), (6, "1 in 1M"), (7, "1 in 10M")]])
        ltt = T("how rare a result must be (each step is 10× stricter)", 24, MUTED).next_to(llab, DOWN, buff=0.2)
        push(self, VGroup(tl_, yrs, ytt, f1, span, span_l, rot, stuck), VGroup(lad, llab, ltt), LEFT, run_time=0.8)
        m1 = marker(lad, np.log10(20), VIOLET, "common: 1 in 20", height=1.0, fs=26)
        m2 = marker(lad, np.log10(3.5e6), RED_, "particle physics: 1 in 3.5 million", height=2.0, fs=26)
        m2.lab.shift(LEFT * 1.6)
        self.word("s055", "different", dt=-0.3)
        self.play(FadeIn(m1, shift=DOWN * 0.5), run_time=0.5)
        self.word("s055", "Particle", dt=-0.2)
        self.play(FadeIn(m2, shift=DOWN * 0.5), run_time=0.6)
        jump = DoubleArrow(lad.n2p(np.log10(20)) + DOWN * 0.0 + UP * 0.35, lad.n2p(np.log10(3.5e6)) + UP * 0.35, buff=0.25, color=WARN, stroke_width=4, tip_length=0.18)
        jl = T("about 175,000 times stricter", 24, WARN, weight=BOLD).next_to(jump, UP, buff=0.1).shift(RIGHT * 0.6)
        self.word("s055", "million", dt=-0.3)
        self.play(GrowFromCenter(jump), FadeIn(jl), run_time=0.8)
        self.idle(lambda: pulse(m2.lab, 1.1), lambda: ShowPassingFlash(jump.copy().set_stroke(WARN, 9), time_width=0.6))

        # ── s056 watch what the line does: 15 heads → p = 0.021, significant ──
        self.at("s056", 0.0)
        self.idle()
        ch3 = dist_chart(x_len=8.0, y_len=2.4, x_title="").move_to(UP * 1.4 + LEFT * 1.6)
        bars3 = dist_bars(ch3.ax, BLUE_)
        mt2 = p_meter(5.4).move_to(DOWN * 1.75 + RIGHT * 3.6)
        al2 = alpha_line(mt2.nl, 0.05, 0.9)
        al2[1].scale(0.8).next_to(al2[0], UP, buff=0.1)
        push(self, VGroup(lad, llab, ltt, m1, m2, jump, jl), VGroup(ch3, bars3, mt2, al2), LEFT, run_time=0.8)
        self.word("s056", "Fifteen", dt=-0.2)
        self.play(LaggedStart(*[bars3[k].animate.set_fill(AQUA, 1) for k in range(15, 21)], lag_ratio=0.15), run_time=0.6)
        pm = marker(mt2.nl, 0.021, AQUA, "0.021", height=0.6, fs=26)
        pm.lab.next_to(pm.tri, LEFT, buff=0.12)
        self.play(FadeIn(pm, shift=DOWN * 0.4), run_time=0.4)
        sig = pill("significant ✓", AQUA, 30).move_to(UP * 2.0 + RIGHT * 4.4)
        self.word("s056", "Significant", dt=-0.3)
        self.play(FadeIn(sig, scale=1.5), ripple(sig.get_center(), AQUA, r=0.5, scale=3), run_time=0.5)
        self.idle(lambda: pulse(sig, 1.1), lambda: LaggedStart(*[pulse(b_, 1.3) for b_ in bars3[15:]], lag_ratio=0.1))

        # ── s057 14 heads → p = 0.058: not significant ──
        self.at("s057", 0.0)
        self.idle()
        self.play(bars3[14].animate.set_fill(AQUA, 1), ripple(ch3.ax.c2p(14, 40), AQUA, r=0.2, scale=4), run_time=0.6)
        self.play(VGroup(pm[0], pm[1]).animate.shift(mt2.nl.n2p(0.058) - mt2.nl.n2p(0.021)), FadeOut(pm.lab), run_time=0.8)
        pm2l = T("0.058", 26, AQUA, weight=BOLD).next_to(pm.tri, RIGHT, buff=0.12)
        nsig = pill("not significant ✗", RED_, 30).move_to(sig)
        self.play(FadeIn(pm2l, shift=LEFT * 0.2), ReplacementTransform(sig, nsig), run_time=0.5)
        pm.remove(pm.lab); pm.add(pm2l)
        self.idle(lambda: pulse(nsig, 1.1), lambda: pm.animate(rate_func=there_and_back).shift(UP * 0.2))

        # ── s058 one flip apart: the verdict flipped ──
        self.at("s058", 0.0)
        self.idle()
        def verdict(h, p, ok):
            c = card(4.6, 2.3, AQUA if ok else RED_)
            a_ = TB(f"{h} heads", 40, WARN)
            b_ = T(f"p ≈ {p}", 32, AQUA, weight=BOLD)
            v_ = T("significant" if ok else "not significant", 30, AQUA if ok else RED_, weight=BOLD)
            VGroup(a_, b_, v_).arrange(DOWN, buff=0.2).move_to(c)
            return VGroup(c, a_, b_, v_)
        v14 = verdict(14, "0.058", False).move_to(LEFT * 2.9 + UP * 0.5)
        v15 = verdict(15, "0.021", True).move_to(RIGHT * 2.9 + UP * 0.5)
        push(self, VGroup(ch3, bars3, mt2, al2, pm, nsig), VGroup(v14, v15), UP, run_time=0.8)
        gap = DoubleArrow(v14[0].get_right(), v15[0].get_left(), buff=0.1, color=WARN, stroke_width=4, tip_length=0.18)
        gl = T("1 flip", 26, WARN, weight=BOLD).next_to(gap, UP, buff=0.1)
        self.word("s058", "apart", dt=-0.3)
        self.play(GrowFromCenter(gap), FadeIn(gl), run_time=0.5)
        self.word("s058", "flipped", dt=-0.3)
        self.play(v14[3].animate(rate_func=there_and_back).scale(1.3), v15[3].animate(rate_func=there_and_back).scale(1.3), run_time=0.6)
        self.idle(lambda: AnimationGroup(pulse(v14, 1.06), pulse(v15, 1.06)))

        # ── s059 a rough sign, not a magic switch: look at p itself, and the effect size ──
        self.at("s059", 0.0)
        self.idle()
        sw = VGroup(RoundedRectangle(corner_radius=0.3, width=1.4, height=0.6).set_stroke(INK2, 4),
                    Circle(0.22).set_stroke(width=0).set_fill(INK2, 1))
        sw[1].move_to(sw[0].get_left() + RIGHT * 0.32)
        swg = VGroup(sw, T("magic switch?", 26, INK2, weight=BOLD).next_to(sw, DOWN, buff=0.2)).move_to(LEFT * 3.4 + UP * 0.6)
        push(self, VGroup(v14, v15, gap, gl), swg, LEFT, run_time=0.7)
        self.play(sw[1].animate.move_to(sw[0].get_right() + LEFT * 0.32), run_time=0.3)
        self.play(sw[1].animate.move_to(sw[0].get_left() + RIGHT * 0.32), run_time=0.3)
        xx = pill("no: a rough sign", RED_, 26).next_to(swg, DOWN, buff=0.3)
        self.word("s059", "rough", dt=-0.3)
        self.play(FadeIn(xx, scale=1.4), run_time=0.4)
        chk = VGroup(VGroup(check(AQUA, 0.3), T("the p value itself", 32, INK, weight=BOLD)).arrange(RIGHT, buff=0.3),
                     VGroup(check(ORANGE_, 0.3), T("the size of the effect", 32, INK, weight=BOLD)).arrange(RIGHT, buff=0.3)
                     ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(RIGHT * 2.8 + UP * 0.4)
        self.word("s059", "itself", dt=-0.5)
        self.play(FadeIn(chk[0], shift=LEFT * 0.3), run_time=0.5)
        self.word("s059", "size", dt=-0.3)
        self.play(FadeIn(chk[1], shift=LEFT * 0.3), run_time=0.5)
        self.idle(lambda: LaggedStart(*[pulse(c_, 1.08) for c_ in chk], lag_ratio=0.3))
        self.until(SEGS["s059"]["end"] + 0.2)
        self.idle()
        self.play(FadeOut(VGroup(swg, xx, chk), shift=LEFT * 1.0), run_time=0.5)
        self.finish()
