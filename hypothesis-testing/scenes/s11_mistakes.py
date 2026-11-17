import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def mistake_card(n, text, w=3.9, h=2.2):
    down = VGroup(card(w, h, RED_), TB(f"mistake {n}", 40, RED_))
    down[1].move_to(down[0])
    face = VGroup(card(w, h, RED_), TB(f"mistake {n}", 30, RED_), T(text, 26, INK, weight=BOLD))
    VGroup(face[1], face[2]).arrange(DOWN, buff=0.2).move_to(face[0])
    return down, face


class S11Mistakes(Base):
    CHAPTER = "Common Mistakes"

    def construct(self):
        rng = np.random.default_rng(11)
        texts = ["p = chance the\nnull is true?", "test many things,\nreport one", "not significant\n= no effect?"]
        pairs = [mistake_card(i + 1, tx) for i, tx in enumerate(texts)]
        downs = VGroup(*[p_[0] for p_ in pairs]).arrange(RIGHT, buff=0.45).move_to(UP * 0.4)
        for d, f in pairs: f.move_to(d)

        def flip(i, big=False):
            d, f = pairs[i]
            if big:
                f.scale(1.25).move_to(UP * 0.4)
            w0 = f.width
            self.qa_mute(d); self.qa_mute(f)
            self.play(d.animate.stretch(0.02, 0), run_time=0.2)
            f.stretch(0.02, 0)
            self.remove(d); self.add(f)
            self.play(f.animate.stretch_to_fit_width(w0), run_time=0.22)
            self.qa_mute(f, False)

        # ── s099 the most common mistakes: three face-down cards ──
        self.at("s099", 0.0)
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.6) for d in downs], lag_ratio=0.2), run_time=0.9)
        self.word("s099", "beginners", dt=-0.3)
        self.play(LaggedStart(*[Wiggle(d) for d in downs], lag_ratio=0.2), run_time=0.9)
        self.idle(lambda: LaggedStart(*[pulse(d, 1.06) for d in downs], lag_ratio=0.2))

        # ── s100 mistake one: reading p as the chance the boring explanation is true ──
        self.at("s100", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(downs[1], downs[2]), shift=DOWN * 0.4), downs[0].animate.move_to(UP * 0.4), run_time=0.5)
        pairs[0][1].move_to(UP * 0.4)
        self.word("s100", "one", dt=-0.2)
        flip(0)
        self.play(ripple(pairs[0][1].get_center(), RED_, r=0.6, scale=3), run_time=0.5)
        self.idle(lambda: pulse(pairs[0][1], 1.08))

        # ── s101 a town where 1 coin in 100 is rigged (70% heads): 10,000 coins ──
        self.at("s101", 0.0)
        self.idle()
        gx = xy_axes([0, 100, 25], [0, 100, 25], 4.2, 4.2, "coin (column)", "row", font_size=18, y_vertical=True)
        gx.move_to(LEFT * 3.3 + UP * 0.25)
        cell = 4.2 / 100
        rig_idx = set(rng.choice(10000, 100, replace=False).tolist())
        sq = VGroup(*[Square(cell * 0.8).set_stroke(width=0).set_fill(ORANGE_ if i in rig_idx else BLUE_, 1 if i in rig_idx else 0.75)
                      .move_to(gx.ax.c2p(i % 100 + 0.5, i // 100 + 0.5)) for i in range(10000)])
        for s_ in sq: s_.qa_ignore = True   # 10,000 data squares inside their own axes (keeps the checker fast)
        ill = T("illustration", 22, MUTED).next_to(gx, DOWN, buff=0.05).align_to(gx.ax, LEFT)
        self.play(FadeOut(pairs[0][1], shift=UP * 0.4), run_time=0.4)
        self.play(Create(gx.ax), FadeIn(gx.labs), FadeIn(gx.xt), FadeIn(gx.yt), FadeIn(ill), run_time=0.5)
        self.word("s101", "town", dt=-0.3)
        self.play(FadeIn(sq, lag_ratio=0.0002), run_time=1.2)
        info = VGroup(TB("10,000 coins", 40, INK),
                      T("1 in 100 is rigged", 32, ORANGE_, weight=BOLD),
                      T("(lands heads 70% of the time)", 26, INK2)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(RIGHT * 3.0 + UP * 0.9)
        self.word("s101", "one", dt=-0.3)
        self.play(FadeIn(info[0]), FadeIn(info[1], shift=LEFT * 0.2), run_time=0.5)
        rigged = VGroup(*[sq[i] for i in sorted(rig_idx)])
        self.play(LaggedStart(*[Indicate(s_, color=ORANGE_, scale_factor=3) for s_ in list(rigged)[:40]], lag_ratio=0.02), run_time=0.9)
        self.word("s101", "seventy", dt=-0.3)
        self.play(FadeIn(info[2], shift=UP * 0.15), run_time=0.4)
        self.idle(lambda: LaggedStart(*[Indicate(rigged[int(k)], color=ORANGE_, scale_factor=3) for k in rng.choice(100, 30)], lag_ratio=0.03))

        # ── s102 count, like the Bayes video: which coins give 15+ heads? ──
        self.at("s102", 0.0)
        self.idle()
        cue = card_cue("Bayes' Theorem", mini_bayes())
        self.play(FadeIn(cue, shift=LEFT * 1.0), info.animate.shift(DOWN * 0.5), run_time=0.5)
        self.word("s102", "card", dt=-0.3)
        self.play(pulse(cue, 1.12), run_time=0.6)
        sx = xy_axes([0, 3, 1], [0, 250, 50], 4.8, 3.2, None, "coins with 15+ heads", x_labels={}, font_size=22, y_vertical=True)
        sx.move_to(RIGHT * 2.7 + UP * 0.2)
        fairs = stack(sx.ax, 1, 205, BLUE_, per_row=6, unit=1)
        rigs = stack(sx.ax, 2, 42, ORANGE_, per_row=6, unit=1)
        fl = T("fair\n≈ 205", 26, BLUE_, weight=BOLD).next_to(sx.ax.c2p(1, 0), DOWN, buff=0.18)
        rl = T("rigged\n≈ 42", 26, ORANGE_, weight=BOLD).next_to(sx.ax.c2p(2, 0), DOWN, buff=0.18)
        self.word("s102", "count", dt=-0.3)
        self.play(FadeOut(info, shift=RIGHT * 0.5), FadeIn(sx), run_time=0.5)
        self.play(sq.animate.set_opacity(0.25), LaggedStart(*[FadeIn(s_, shift=DOWN * 0.3) for s_ in fairs], lag_ratio=0.004), FadeIn(fl), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(s_, shift=DOWN * 0.3) for s_ in rigs], lag_ratio=0.02), FadeIn(rl), run_time=0.8)
        p83 = pill("≈ 83% fair", BLUE_, 28).next_to(fairs, UP, buff=0.2)
        p17 = pill("≈ 17% rigged", ORANGE_, 28).next_to(rigs, UP, buff=0.2).shift(UP * 0.3)
        self.word("s102", "eighty", dt=-0.3)
        self.play(FadeIn(p83, scale=0.6), run_time=0.4)
        self.word("s102", "seventeen", dt=-0.3)
        self.play(FadeIn(p17, scale=0.6), run_time=0.4)
        self.idle(lambda: pulse(p83, 1.1), lambda: pulse(p17, 1.1))

        # ── s103 p was 2%, but the chance it's rigged is about 1 in 6 ──
        self.at("s103", 0.0)
        self.idle()
        a = VGroup(card(4.6, 2.2, AQUA), T("p value", 30, INK2, weight=BOLD), TB("≈ 2%", 64, AQUA))
        b = VGroup(card(4.6, 2.2, VIOLET), T("chance it's rigged", 30, INK2, weight=BOLD), TB("≈ 17%", 64, VIOLET))
        for c_ in (a, b):
            VGroup(c_[1], c_[2]).arrange(DOWN, buff=0.25).move_to(c_[0])
        a.move_to(LEFT * 3.1 + UP * 0.5); b.move_to(RIGHT * 3.1 + UP * 0.5)
        ne = MathTex(r"\neq", font_size=96, color=RED_).move_to(UP * 0.5)
        push(self, VGroup(gx, sq, ill, sx, fairs, rigs, fl, rl, p83, p17, cue), a, LEFT, run_time=0.7)
        self.word("s103", "rigged", dt=-0.3)
        self.play(FadeIn(b, shift=LEFT * 0.5), FadeIn(ne, scale=1.5), run_time=0.5)
        six = T("about 1 in 6", 30, VIOLET, weight=BOLD).next_to(b, DOWN, buff=0.3)
        self.play(FadeIn(six, shift=UP * 0.2), run_time=0.4)
        same = pill("same evidence, very different numbers", WARN, 28).move_to(DOWN * 2.0)
        self.word("s103", "Same", dt=-0.3)
        self.play(FadeIn(same, shift=UP * 0.2), run_time=0.4)
        self.idle(lambda: Wiggle(ne, scale_value=1.3), lambda: pulse(same, 1.08))

        # ── s104 mistake two: test lots, report the winner ──
        self.at("s104", 0.0)
        self.idle()
        d2, f2 = pairs[1]
        d2.move_to(UP * 0.4); f2.move_to(UP * 0.4)
        push(self, VGroup(a, b, ne, six, same), d2, LEFT, run_time=0.6)
        self.word("s104", "two", dt=-0.2)
        flip(1)
        self.idle(lambda: pulse(f2, 1.08))

        # ── s105 twenty null tests at 1 in 20: ≈ 64% chance of a false alarm ──
        self.at("s105", 0.0)
        self.idle()
        minis = VGroup()
        for i in range(20):
            box = RoundedRectangle(corner_radius=0.1, width=1.55, height=0.88).set_stroke(MUTED, 2).set_fill("#22221f", 1)
            box.qa_container = True
            xs = np.linspace(-0.6, 0.6, 30)
            cv = VMobject().set_points_smoothly([np.array([x, -0.28 + 0.5 * np.exp(-(x / 0.25) ** 2), 0]) for x in xs]).set_stroke(BLUE_, 3)
            cv.move_to(box)
            minis.add(VGroup(box, cv))
        minis.arrange_in_grid(4, 5, buff=(0.2, 0.18)).move_to(LEFT * 2.6 + UP * 0.3)
        push(self, f2, minis, LEFT, run_time=0.6)
        self.word("s105", "twenty", dt=-0.3)
        self.play(LaggedStart(*[Indicate(m[1], color=BLUE_, scale_factor=1.15) for m in minis], lag_ratio=0.04), run_time=1.0)
        hit = minis[13]
        dotp = Dot(radius=0.08, color=RED_).move_to(hit[0].get_right() + LEFT * 0.3 + DOWN * 0.24)
        self.word("s105", "significant", dt=-0.4)
        self.play(hit[0].animate.set_stroke(RED_, 4), FadeIn(dotp, scale=2), ripple(hit.get_center(), RED_, r=0.4, scale=4), run_time=0.6)
        ch64 = VGroup(T("chance of at least", 26, INK2, weight=BOLD), T("one false alarm", 26, INK2, weight=BOLD), TB("≈ 64%", 64, RED_))
        ch64.arrange(DOWN, buff=0.12).move_to(RIGHT * 4.6 + UP * 1.4)
        self.word("s105", "sixty", dt=-0.3)
        self.play(FadeIn(ch64, shift=LEFT * 0.3), run_time=0.5)
        self.idle(lambda: pulse(ch64[2], 1.12), lambda: Indicate(dotp, color=RED_, scale_factor=2))

        # ── s105a p-hacking: analysis after analysis until something crosses the line ──
        self.at("s105a", 0.0)
        self.idle()
        ph = pill("p-hacking", RED_, 40).rotate(-5 * DEGREES).move_to(RIGHT * 4.6 + DOWN * 0.3)
        self.word("s105a", "hacking", dt=-0.4)
        self.play(FadeIn(ph, scale=1.8), run_time=0.4, rate_func=rate_functions.ease_out_cubic)
        cnt = ValueTracker(0.31)
        pt = always_redraw(lambda: T(f"try again: p = {cnt.get_value():.2f}", 26, INK, weight=BOLD).move_to(RIGHT * 4.6 + DOWN * 1.4))
        self.add(pt)
        self.word("s105a", "analysis", dt=-0.2)
        for v in (0.22, 0.13, 0.09, 0.07, 0.049):
            self.play(cnt.animate.set_value(v), Indicate(minis[int(rng.integers(20))][1], color=WARN, scale_factor=1.2), run_time=0.45)
        pt.clear_updaters()
        self.play(pt.animate.set_color(RED_), ripple(pt.get_center(), RED_, r=0.4, scale=3), run_time=0.5)
        self.idle(lambda: pulse(ph, 1.1))

        # ── s106 lucky strategies and surprising headlines: test many → stricter line ──
        self.at("s106", 0.0)
        self.idle()
        hl = VGroup(card(3.4, 1.1, INK2), T("SHOCK STUDY!", 28, WARN, weight=BOLD)); hl[1].move_to(hl[0])
        hl.move_to(RIGHT * 4.6 + UP * 2.2)
        self.word("s106", "headline", dt=-0.3)
        self.play(FadeIn(hl, shift=DOWN * 0.3), FadeOut(VGroup(pt, ch64, ph)), run_time=0.4)
        noise = pill("from pure noise", RED_, 26).next_to(hl, DOWN, buff=0.2)
        self.play(FadeIn(noise, scale=0.6), run_time=0.35)
        nl = NumberLine(x_range=[0, 0.06, 0.01], length=4.0, color=INK2, stroke_width=3, include_tip=False, tick_size=0.07).move_to(RIGHT * 4.5 + DOWN * 0.9)
        nll = VGroup(*[T(f"{v:.2f}", 20, INK2).next_to(nl.n2p(v), DOWN, buff=0.12) for v in (0, 0.02, 0.04, 0.06)])
        aln = Line(nl.n2p(0.05), nl.n2p(0.05) + UP * 0.9).set_stroke(VIOLET, 6)
        alt = T("α", 30, VIOLET, weight=BOLD).next_to(aln, UP, buff=0.08)
        self.word("s106", "stricter", dt=-0.6)
        self.play(FadeIn(nl), FadeIn(nll), FadeIn(aln), FadeIn(alt), run_time=0.4)
        self.play(VGroup(aln, alt).animate.shift(nl.n2p(0.0025) - nl.n2p(0.05)), run_time=1.0)
        stl = T("stricter line", 24, VIOLET, weight=BOLD).next_to(VGroup(aln, alt), RIGHT, buff=0.2)
        self.play(FadeIn(stl), run_time=0.3)
        self.idle(lambda: pulse(hl, 1.06))

        # ── s107 mistake three: not significant ≠ no effect ──
        self.at("s107", 0.0)
        self.idle()
        d3, f3 = pairs[2]
        d3.move_to(UP * 0.4); f3.move_to(UP * 0.4)
        push(self, VGroup(minis, dotp, hl, noise, nl, nll, aln, alt, stl), d3, LEFT, run_time=0.6)
        self.word("s107", "three", dt=-0.2)
        flip(2)
        self.idle(lambda: pulse(f3, 1.08))

        # ── s108 remember the 70% coin: with 20 flips we missed it more than half the time ──
        self.at("s108", 0.0)
        self.idle()
        ch = dist_chart(x_len=10.0, y_len=3.2).move_to(RIGHT * 0.4 + UP * 0.4)
        A = VGroup(*[bar(ch.ax, k - 0.13, v, BLUE_, width=0.22) for k, v in enumerate(EXP)])
        B = VGroup(*[bar(ch.ax, k + 0.13, v, ORANGE_, width=0.22) for k, v in enumerate(EXP70)])
        for k in range(8, 15): B[k].set_fill(RED_, 0.75)
        push(self, f3, VGroup(ch, A, B), LEFT, run_time=0.6)
        ms = pill("missed ≈ 58%", RED_, 30).move_to(ch.ax.c2p(3.2, 175))
        self.word("s108", "missed", dt=-0.3)
        self.play(FadeIn(ms, scale=0.6), LaggedStart(*[pulse(B[k], 1.2) for k in range(8, 15)], lag_ratio=0.06), run_time=0.6)
        ne2 = pill("not enough data", WARN, 30).next_to(ms, DOWN, buff=0.25)
        self.word("s108", "enough", dt=-0.3)
        self.play(FadeIn(ne2, shift=UP * 0.2), run_time=0.4)
        self.idle(lambda: pulse(ne2, 1.1))

        # ── s109 bonus: moving the line after seeing the data ──
        self.at("s109", 0.0)
        self.idle()
        bonus = pill("bonus mistake", RED_, 30).move_to(UP * 2.9 + RIGHT * 1.6)
        mt = NumberLine(x_range=[0, 0.10, 0.01], length=10.0, color=INK2, stroke_width=3, include_tip=False, tick_size=0.08).move_to(DOWN * 0.6)
        mtl = VGroup(*[T(f"{v:.2f}", 22, INK2).next_to(mt.n2p(v), DOWN, buff=0.15) for v in np.arange(0, 0.101, 0.02)])
        mtt = T("p value", 24, MUTED).next_to(mtl, DOWN, buff=0.15).align_to(mt, RIGHT)
        push(self, VGroup(ch, A, B, ms, ne2), VGroup(mt, mtl, mtt), LEFT, run_time=0.6)
        self.play(FadeIn(bonus, shift=DOWN * 0.2), run_time=0.35)
        mk = marker(mt, 0.07, AQUA, "your p = 0.07", height=1.3, fs=26)
        al = Line(mt.n2p(0.05), mt.n2p(0.05) + UP * 0.8).set_stroke(VIOLET, 6)
        all_ = T("α", 32, VIOLET, weight=BOLD).next_to(al, LEFT, buff=0.1).shift(UP * 0.2)
        self.play(FadeIn(mk, shift=DOWN * 0.3), Create(al), FadeIn(all_), run_time=0.5)
        self.word("s109", "move", dt=-0.3)
        self.play(VGroup(al, all_).animate.shift(mt.n2p(0.08) - mt.n2p(0.05)), run_time=1.0, rate_func=smooth)
        no = pill("no! choose α before you look", RED_, 30).move_to(DOWN * 2.05 + LEFT * 2.6)
        self.play(FadeIn(no, scale=1.5), Wiggle(VGroup(al, all_)), run_time=0.6)
        self.play(VGroup(al, all_).animate.shift(mt.n2p(0.05) - mt.n2p(0.08)), run_time=0.7)
        mean_ = pill("p stops meaning anything", WARN, 26).move_to(UP * 1.6 + RIGHT * 3.4)
        self.word("s109", "meaning", dt=-0.4)
        self.play(FadeIn(mean_, shift=DOWN * 0.2), run_time=0.4)
        self.idle(lambda: pulse(no, 1.08))
        self.until(self.ch["t1"] - 0.55)
        self.idle()
        self.play(FadeOut(VGroup(bonus, mt, mtl, mtt, mk, al, all_, no, mean_), shift=LEFT * 1.0), run_time=0.5)
        self.finish()
