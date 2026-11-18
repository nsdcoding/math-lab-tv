import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

STOPS = {1_000: "1,000", 1_000_000: "1,000,000", 8_000_000: "8,000,000", 60_000_000: "60,000,000"}


class S07BaseRate(Base):
    CHAPTER = "The Missing Piece"

    def construct(self):
        # ── s060 the base rate ──
        self.at("s060", 0.0)
        hd = TB("the base rate", 60, AQUA).move_to(UP * 1.0)
        sub = T("how big is the crowd of possible suspects?", 34, INK).next_to(hd, DOWN, buff=0.4)
        self.play(FadeIn(hd, scale=0.8), run_time=0.6)
        self.word("s060", "name")
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.5)
        self.word("s060", "left")
        lo = pill("the piece the prosecutor left out", RED_, 28).next_to(sub, DOWN, buff=0.45)
        self.play(FadeIn(lo, scale=0.7), run_time=0.5)

        # ── s061 same trace, change the crowd: a crowd-size slider (log axis) ──
        self.at("s061", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(hd, sub, lo)), run_time=0.4)
        nl = NumberLine(x_range=[3, 8, 1], length=9.0, include_tip=False, color=INK2, stroke_width=3, tick_size=0.06)
        nl.move_to(UP * 2.05 + RIGHT * 0.9)
        tl = VGroup(*[T(t, 20, INK2).next_to(nl.n2p(np.log10(v)), DOWN, buff=0.34) for v, t in STOPS.items()])
        tm = VGroup(*[Line(UP * 0.12, DOWN * 0.12).set_stroke(INK, 3).move_to(nl.n2p(np.log10(v))) for v in STOPS])
        ttl = T("crowd size (log scale)", 22, MUTED).next_to(nl, UP, buff=0.32).align_to(nl, LEFT)
        knob = Circle(0.2).set_stroke(INK, 3).set_fill(AQUA, 1).move_to(nl.n2p(6.903))
        knob.qa_dot = True
        tr = pill("trace: 1 in a million", WARN, 26).next_to(nl, UP, buff=0.3).align_to(nl, RIGHT)
        self.play(Create(nl), FadeIn(tl), FadeIn(tm), FadeIn(ttl), FadeIn(knob, scale=0.4), run_time=0.7)
        self.word("s061", "trace")
        self.play(FadeIn(tr, shift=LEFT * 0.3), run_time=0.4)
        self.word("s061", "change")
        self.play(knob.animate.move_to(nl.n2p(4.0)), run_time=0.6)
        self.play(knob.animate.move_to(nl.n2p(6.903)), run_time=0.6)

        # ── s062 a village of 1,000 ──
        self.at("s062", 0.0)
        self.play(knob.animate.move_to(nl.n2p(3)), run_time=0.7)
        vil = VGroup(*[Square(0.09, stroke_width=0, fill_color=BLUE_, fill_opacity=0.85) for _ in range(1000)])
        vil.arrange_in_grid(25, 40, buff=0.035).move_to(LEFT * 2.6 + DOWN * 0.8)
        vil[517].set_fill(ORANGE_, 1)
        vl = T("village: 1,000 people", 26, AQUA, weight=BOLD).next_to(vil, UP, buff=0.2)
        self.word("s062", "village")
        self.play(FadeIn(vil, lag_ratio=0.001), FadeIn(vl), run_time=0.9)
        self.word("s062", "nobody")
        self.play(ripple(vil[517].get_center(), ORANGE_, r=0.15, scale=4), run_time=0.6)

        # ── s063 chance any innocent matches ≈ 1 in 1,000 ──
        self.at("s063", 0.0)
        scan = Line(vil.get_corner(UL), vil.get_corner(DL)).set_stroke(WARN, 5)
        scan.qa_ignore = True
        self.play(Create(scan), run_time=0.3)
        self.play(scan.animate.move_to(vil.get_right()), run_time=1.6, rate_func=linear)
        self.play(FadeOut(scan), run_time=0.2)
        px = 1.6
        im = result_card("innocent matches expected", "≈ 0.001", WARN, 26, 44)
        im.move_to(UP * 0.35).set_x(px + im.width / 2)
        self.word("s063", "thousand")
        self.play(FadeIn(im, shift=LEFT * 0.3), run_time=0.5)

        # ── s064 almost certainly the culprit: 999 in 1,000 ──
        self.at("s064", 0.0)
        r1 = result_card("P(guilty | match)", "≈ 999 in 1,000", VIOLET, 26, 44)
        r1.next_to(im, DOWN, buff=0.35).align_to(im, LEFT)
        lu1 = lineup(1, 0, 0.6).next_to(r1, LEFT, buff=0.35)
        self.word("s064", "culprit")
        self.play(FadeIn(r1, shift=UP * 0.2), FadeIn(lu1, scale=0.5), run_time=0.6)
        self.idle(lambda: pulse(r1.value, s=1.1))

        # ── s065 back to the city: 1 in 9 ──
        self.at("s065", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(vil, vl, im, r1, lu1)), knob.animate.move_to(nl.n2p(np.log10(8e6))), run_time=0.8)
        lu9 = lineup(9, 6, 0.6, 0.18).move_to(LEFT * 2.0 + DOWN * 0.3)
        r9 = result_card("P(guilty | match)", "≈ 1 in 9", VIOLET, 26, 44).next_to(lu9, RIGHT, buff=0.6)
        cl = T("city: 8,000,000 people", 26, AQUA, weight=BOLD).next_to(lu9, UP, buff=0.35)
        self.play(FadeIn(cl), LaggedStart(*[FadeIn(p, scale=0.5) for p in lu9], lag_ratio=0.05), run_time=0.8)
        self.play(FadeIn(r9, shift=LEFT * 0.2), run_time=0.5)

        # ── s066 a country of 60 million: 60 innocent matches, 1 in 61 ──
        self.at("s066", 0.0)
        self.play(FadeOut(VGroup(lu9, r9, cl)), knob.animate.move_to(nl.n2p(np.log10(6e7))), run_time=0.8)
        lu61 = VGroup(*[matcher(i == 33, 0.36) for i in range(61)]).arrange_in_grid(4, 16, buff=(0.12, 0.14))
        lu61.move_to(LEFT * 2.0 + DOWN * 0.35)
        ctl = T("country: 60,000,000 people", 26, AQUA, weight=BOLD).next_to(lu61, UP, buff=0.3)
        self.word("s066", "country")
        self.play(FadeIn(ctl), run_time=0.4)
        self.word("s066", "sixty", nth=1)
        self.play(LaggedStart(*[FadeIn(p, scale=0.4) for p in lu61], lag_ratio=0.015), run_time=1.2)
        r61 = result_card("P(guilty | match)", "≈ 1 in 61", VIOLET, 26, 44).next_to(lu61, RIGHT, buff=0.6)
        self.word("s066", "drops")
        self.play(FadeIn(r61, shift=LEFT * 0.2), run_time=0.5)
        self.idle(lambda: pulse(lu61[33], s=1.3))

        # ── s067 / s066a evidence fixed, crowd changed: three answers ──
        self.at("s067", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(lu61, ctl, r61)), run_time=0.5)
        res = VGroup(result_card("village · 1,000", "999 in 1,000", VIOLET, 26, 46, 3.9),
                     result_card("city · 8,000,000", "1 in 9", VIOLET, 26, 46, 3.9),
                     result_card("country · 60,000,000", "1 in 61", VIOLET, 26, 46, 3.9)).arrange(RIGHT, buff=0.35)
        res.move_to(DOWN * 0.5)
        fixed = pill("same trace: 1 in a million", WARN, 28).next_to(res, DOWN, buff=0.4)
        self.word("s067", "evidence")
        self.play(FadeOut(tr), FadeIn(fixed, shift=DOWN * 0.2), run_time=0.5)
        self.word("s067", "crowd")
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.3) for r in res], lag_ratio=0.25), run_time=1.1)
        self.word("s067", "certain")
        self.play(pulse(res[0], s=1.08), run_time=0.6)
        self.word("s067", "not")
        self.play(pulse(res[2], s=1.08), run_time=0.6)

        self.at("s066a", 0.0)
        self.word("s066a", "trace")
        self.play(pulse(fixed, s=1.1), run_time=0.5)
        self.word("s066a", "Three")
        self.play(LaggedStart(*[pulse(r, s=1.08) for r in res], lag_ratio=0.3), run_time=1.2)

        # ── s068 evidence + crowd → answer ──
        self.at("s068", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(res, fixed, nl, tl, tm, ttl, knob)), run_time=0.5)
        eqn = VGroup(pill("evidence", WARN, 40), T("+", 48, INK2), pill("crowd", AQUA, 40), T("→", 48, INK2),
                     pill("chance of guilt", VIOLET, 40)).arrange(RIGHT, buff=0.35).move_to(UP * 0.3)
        self.word("s068", "own")
        self.play(FadeIn(eqn[0]), run_time=0.4)
        self.word("s068", "need")
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in eqn[1:]], lag_ratio=0.2), run_time=0.9)
        self.play(ripple(eqn[2].get_center(), AQUA, r=0.6, scale=3), run_time=0.6)
        self.idle(lambda: pulse(eqn[2], s=1.12))
        self.finish()
