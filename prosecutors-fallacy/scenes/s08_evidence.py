import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


class S08Evidence(Base):
    CHAPTER = "When Other Evidence Counts"

    def construct(self):
        # ── s069 assumption 3 returns ──
        self.at("s069", 0.0)
        a3 = VGroup(TB("3", 44, AQUA), T("no other evidence about Sam (yet)", 34, INK)).arrange(RIGHT, buff=0.35)
        b3 = card(a3.width + 0.9, a3.height + 0.7, AQUA); a3.move_to(b3)
        g3 = VGroup(b3, a3).move_to(UP * 1.6)
        self.play(FadeIn(g3, shift=DOWN * 0.3), run_time=0.6)
        self.word("s069", "except")
        self.play(pulse(g3, s=1.06), run_time=0.6)

        # ── s070 more evidence: seen near the scene ──
        self.at("s070", 0.0)
        e1 = pill("DNA match", WARN, 32); e2 = pill("seen near the scene", INK, 32)
        ev = VGroup(e1, e2).arrange(RIGHT, buff=0.5).move_to(UP * 0.1)
        self.play(FadeIn(e1, shift=UP * 0.2), run_time=0.4)
        self.word("s070", "seen")
        self.play(FadeIn(e2, shift=LEFT * 0.3), ripple(e2.get_center(), INK, r=0.5, scale=3), run_time=0.6)

        # ── s071 other evidence shrinks the crowd ──
        self.at("s071", 0.0)
        self.idle()
        self.play(FadeOut(g3), ev.animate.scale(0.8).move_to(UP * 2.3 + RIGHT * 1.0), run_time=0.5)
        big = VGroup(*[Square(0.13, stroke_width=0, fill_color=BLUE_, fill_opacity=0.7) for _ in range(20 * 60)])
        big.arrange_in_grid(20, 60, buff=0.05).move_to(DOWN * 0.15 + RIGHT * 0.3)
        bl = T("8,000,000 possible people", 26, AQUA, weight=BOLD).next_to(big, DOWN, buff=0.15)
        self.word("s071", "shrinking")
        self.play(FadeIn(big, lag_ratio=0.0005), FadeIn(bl), run_time=0.8)
        rng = np.random.default_rng(9)
        near_idx = set(int(i) for i in rng.choice(len(big), 300, replace=False)) | {840}
        cluster = VGroup(*[Square(0.2, stroke_width=0, fill_color=BLUE_, fill_opacity=0.85) for _ in range(300)])
        cluster.arrange_in_grid(12, 25, buff=0.07).move_to(DOWN * 0.15 + LEFT * 1.6)
        cluster[160].set_fill(ORANGE_, 1)
        cl = T("a few hundred nearby (illustration)", 26, AQUA, weight=BOLD).next_to(cluster, DOWN, buff=0.2)
        self.word("s071", "few")
        self.play(ReplacementTransform(VGroup(*[big[i] for i in sorted(near_idx)][:300]), cluster),
                  FadeOut(VGroup(*[big[i] for i in range(len(big)) if i not in near_idx])), FadeOut(VGroup(*[big[i] for i in sorted(near_idx)][300:])),
                  ReplacementTransform(bl, cl), run_time=1.4)

        # ── s072 smaller crowd: the match becomes much stronger ──
        self.at("s072", 0.0)
        scan = Line(cluster.get_corner(UL), cluster.get_corner(DL)).set_stroke(WARN, 5)
        scan.qa_ignore = True
        self.play(Create(scan), run_time=0.2)
        self.play(scan.animate.move_to(cluster.get_right()), run_time=1.3, rate_func=linear)
        ring_ = Circle(0.2).set_stroke(WARN, 4).move_to(cluster[160]); ring_.qa_ignore = True
        self.play(FadeOut(scan), Create(ring_), run_time=0.4)
        pn = T("innocent matches here: ≈ none", 30, INK, weight=BOLD)
        px = 2.6
        pn.move_to(UP * 1.05).set_x(px + pn.width / 2)
        if pn.get_right()[0] > 6.6:
            pn.scale_to_fit_width(6.6 - px)
            pn.move_to(UP * 1.05).set_x(px + pn.width / 2)
        mt = NumberLine(x_range=[0, 100, 25], length=3.6, include_tip=False, color=INK2, stroke_width=3, tick_size=0.07)
        mt.move_to(DOWN * 0.75).set_x(px + 1.8)
        mtl = VGroup(*[T(f"{v}%", 20, INK2).next_to(mt.n2p(v), DOWN, buff=0.12) for v in (0, 50, 100)])
        mtt = T("chance of guilt (illustration)", 22, MUTED).next_to(mtl, DOWN, buff=0.15)
        bar_ = Rectangle(width=0.05, height=0.3).set_stroke(width=0).set_fill(VIOLET, 1).move_to(mt.n2p(0), aligned_edge=LEFT).shift(UP * 0.3)
        self.word("s072", "fewer")
        self.play(FadeIn(pn, shift=LEFT * 0.2), run_time=0.5)
        self.play(Create(mt), FadeIn(mtl), FadeIn(mtt), FadeIn(bar_), run_time=0.5)
        self.word("s072", "stronger")
        self.play(bar_.animate.stretch_to_fit_width(mt.n2p(90)[0] - mt.n2p(0)[0]).align_to(mt.n2p(0), LEFT), run_time=1.0)
        vs = pill("much stronger", VIOLET, 26).next_to(pn, DOWN, buff=0.28).align_to(pn, LEFT)
        self.play(FadeIn(vs, scale=0.6), run_time=0.4)

        # ── s073 one piece, combined honestly ──
        self.at("s073", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(cluster, cl, ring_, pn, mt, mtl, mtt, bar_, vs, ev)), run_time=0.5)
        pcs = VGroup(pill("DNA match", WARN, 34), pill("seen nearby", INK, 34), pill("other facts", AQUA, 34))
        pcs.arrange(RIGHT, buff=1.2).move_to(UP * 0.4)
        self.word("s073", "useless")
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.3) for p in pcs], lag_ratio=0.25), run_time=0.9)
        self.word("s073", "combined")
        self.play(pcs.animate.arrange(RIGHT, buff=0.12).move_to(UP * 0.4), run_time=0.7)
        hon = T("combined, honestly", 32, INK2).next_to(pcs, DOWN, buff=0.45)
        self.play(FadeIn(hon, shift=UP * 0.2), ripple(pcs.get_center(), AQUA, r=0.8, scale=3), run_time=0.6)

        # ── s073a before the match: 1 in 8,000,000 (log meter) ──
        self.at("s073a", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(pcs, hon)), run_time=0.4)
        lg = NumberLine(x_range=[-7, 0, 1], length=11.0, include_tip=False, color=INK2, stroke_width=3, tick_size=0.07)
        lg.move_to(DOWN * 0.7)
        lbl = {-7: "1 in 10 million", -5: "1 in 100,000", -3: "1 in 1,000", -1: "1 in 10", 0: "certain"}
        lgl = VGroup(*[T(t, 20, INK2).next_to(lg.n2p(v), DOWN, buff=0.14) for v, t in lbl.items()])
        lgt = T("Sam's chance of guilt (log scale)", 22, MUTED).next_to(lgl, DOWN, buff=0.15)
        self.play(Create(lg), FadeIn(lgl), FadeIn(lgt), run_time=0.6)
        x0 = np.log10(1 / 8e6)
        mk0 = Triangle().scale(0.17).rotate(PI).set_stroke(width=0).set_fill(ORANGE_, 1).move_to(lg.n2p(x0) + UP * 0.32)
        c0 = pill("before: 1 in 8,000,000", ORANGE_, 28).next_to(mk0, UP, buff=0.25)
        if c0.get_left()[0] < -6.5:
            c0.shift(RIGHT * (-6.5 - c0.get_left()[0]))
        self.word("s073a", "Before")
        self.play(FadeIn(mk0, shift=DOWN * 0.3), FadeIn(c0, shift=DOWN * 0.2), run_time=0.6)

        # ── s073b after: 1 in 9 — ~889,000 times higher ──
        self.at("s073b", 0.0)
        x1 = np.log10(1 / 9)
        mk1 = mk0.copy().set_fill(VIOLET, 1).move_to(lg.n2p(x1) + UP * 0.32)
        c1 = pill("after: 1 in 9", VIOLET, 28).next_to(mk1, UP, buff=0.25)
        if c1.get_right()[0] > 6.6:
            c1.shift(LEFT * (c1.get_right()[0] - 6.6))
        arc = CurvedArrow(c0.get_top() + UP * 0.12, c1.get_top() + UP * 0.12, angle=-PI / 5, color=WARN, stroke_width=5)
        arc.qa_ignore = True
        self.word("s073b", "nine")
        self.play(TransformFromCopy(mk0, mk1), FadeIn(c1, shift=DOWN * 0.2), run_time=0.8)
        self.word("s073b", "jumped")
        x_ = pill("≈ 889,000 × higher", WARN, 30).move_to(UP * 2.35 + RIGHT * 0.5)
        self.play(Create(arc), FadeIn(x_, scale=0.6), run_time=0.8)
        self.qa_mute(arc)

        # ── s073c strong, not proof ──
        self.at("s073c", 0.0)
        sp = pill("strong evidence ≠ proof", VIOLET, 34).move_to(DOWN * 2.2)
        self.play(FadeOut(lgt), FadeIn(sp, shift=UP * 0.2), run_time=0.5)
        self.idle(lambda: pulse(sp, s=1.1))
        self.finish()
