import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

RUN = "HTHHTTHTHHTHTHTTHHTH"   # one illustrative fair-coin run: 11 heads
assert RUN.count("H") == 11


class S05Coins(Base):
    CHAPTER = "A Thousand Fair Coins"

    def construct(self):
        fr = self.camera.frame
        rng = np.random.default_rng(3)

        # ── s028 one fair coin, twenty flips ──
        self.at("s028", 0.0)
        c = coin("H", BLUE_, 0.85).move_to(LEFT * 2.6 + UP * 0.6)
        tag = T("one fair coin · 20 flips (illustration)", 26, MUTED).next_to(c, DOWN, buff=0.45)
        h = ValueTracker(0)
        cnt = always_redraw(lambda: T(f"heads: {int(round(h.get_value()))}", 44, BLUE_, weight=BOLD)
                            .move_to(RIGHT * 2.8 + UP * 0.6))
        self.play(FadeIn(c, scale=0.6), FadeIn(tag), run_time=0.5)
        self.add(cnt)
        tiles = VGroup(*[Square(0.42).set_stroke(BLUE_ if f == "H" else MUTED, 2.5).set_fill("#22221f", 1) for f in RUN])
        tiles.arrange(RIGHT, buff=0.08).move_to(DOWN * 1.55)
        for s_ in tiles: s_.qa_container = True
        tl_ = VGroup(*[T(f, 22, BLUE_ if f == "H" else MUTED, weight=BOLD).move_to(s_) for f, s_ in zip(RUN, tiles)])
        heads = 0
        for k, f in enumerate(RUN):
            heads += f == "H"
            self.play(flipping(c), h.animate.set_value(heads), FadeIn(tiles[k], scale=1.5), FadeIn(tl_[k]), run_time=0.15)
        cnt.clear_updaters()
        self.play(Indicate(cnt, color=BLUE_, scale_factor=1.2), run_time=0.5)

        # ── s029 a thousand friends ──
        self.at("s029", 0.0)
        pen = xy_axes([0, 40, 10], [0, 25, 5], 6.0, 3.75, "friend (column)", "row", font_size=20, y_vertical=True)
        pen.move_to(LEFT * 2.4 + UP * 0.35)
        cell = 6.0 / 40
        dots_ = VGroup(*[Dot(radius=cell * 0.32, color=BLUE_).move_to(pen.ax.c2p(i % 40 + 0.5, 24 - i // 40 + 0.5))
                         for i in range(1000)])
        info = VGroup(TB("1,000 friends", 44, BLUE_),
                      T("each flips a fair coin", 30, INK), T("20 times", 30, INK)).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        info.move_to(RIGHT * 4.3 + UP * 0.6)
        self.play(FadeOut(VGroup(c, tag, cnt, tiles, tl_), shift=UP * 0.4), run_time=0.4)
        self.play(Create(pen.ax), FadeIn(pen.labs), FadeIn(pen.xt), FadeIn(pen.yt), run_time=0.6)
        self.until(word_time("s029", word_index("s029", "thousand")) - 0.2)
        self.play(LaggedStart(*[FadeIn(d) for d in dots_], lag_ratio=0.002), FadeIn(info[0]), run_time=1.6)
        self.play(FadeIn(info[1:], shift=UP * 0.2), run_time=0.6)
        self.idle(lambda: AnimationGroup(*[dots_[i].animate(rate_func=there_and_back).set_color(WARN).scale(1.6)
                                           for i in rng.choice(1000, 60, replace=False)]))

        # ── s030 stack them by number of heads ──
        self.at("s030", 0.0)
        ch = dist_chart().move_to(RIGHT * 0.6 + UP * 0.3)
        ax = ch.ax
        bars = dist_bars(ax, BLUE_)
        order = rng.permutation(1000)
        ks = np.repeat(np.arange(21), COUNTS)          # friend -> heads
        targets = []
        for j, i in enumerate(order):
            k = ks[j]
            b = bars[k]
            x = b.get_center()[0] + rng.uniform(-0.35, 0.35) * b.width
            y = ax.c2p(0, 0)[1] + rng.uniform(0.02, 0.98) * max(b.height, 0.02)
            targets.append((dots_[i], np.array([x, y, 0])))
        self.idle()
        self.qa_mute(dots_)   # dots wait over the new chart and cross its tick labels in flight
        self.play(FadeOut(VGroup(pen, info)), Create(ax), FadeIn(ch.labs), FadeIn(ch.xt), FadeIn(ch.yt), run_time=0.6)
        self.play(LaggedStart(*[d.animate.move_to(p).scale(0.6) for d, p in targets], lag_ratio=0.0015), run_time=2.2)
        self.play(FadeIn(bars), FadeOut(dots_), run_time=0.6)

        # ── s031 a distribution ──
        self.at("s031", 0.3)
        dc = VGroup(TB("distribution", 32, INK), T("every result + how often it happens", 23, INK2)).arrange(DOWN, buff=0.14)
        dbox = card(dc.width + 0.7, dc.height + 0.4)
        dcard = VGroup(dbox, dc).move_to(UP * 3.12 + RIGHT * 3.95)
        dc.move_to(dbox)
        self.until(word_time("s031", word_index("s031", "distribution")) - 0.2)
        self.play(FadeIn(dcard, shift=DOWN * 0.2), run_time=0.6)
        self.play(LaggedStart(*[Indicate(l, color=WARN, scale_factor=1.6) for l in ch.labs[:5]], lag_ratio=0.15), run_time=0.9)
        self.idle(lambda: LaggedStart(*[drop_into(ax, int(k_), BLUE_, 185) for k_ in rng.choice([4, 5, 6, 7, 8, 12, 13, 14, 15, 16], 10)], lag_ratio=0.1))

        # ── s032 most land near ten: ~176 ──
        self.at("s032", 0.0)
        self.until(word_time("s032", word_index("s032", "ten")) - 0.2)
        b10g = glow(bars[10].copy().set_fill(opacity=0), INK, width=10, opacity=0.1)
        l176 = T("≈ 176 friends", 26, INK, weight=BOLD).next_to(bars[10], UP, buff=0.15)
        self.idle()
        self.play(bars[10].animate.set_fill(BLUE_, 1), FadeIn(b10g), ripple(bars[10].get_top(), INK, r=0.3, scale=4), run_time=0.5)
        self.until(word_time("s032", word_index("s032", "hundred")) - 0.4)
        c176 = ValueTracker(0)
        l176_ = always_redraw(lambda: T(f"≈ {int(round(c176.get_value()))} friends", 26, INK, weight=BOLD).next_to(bars[10], UP, buff=0.15))
        self.add(l176_)
        self.play(c176.animate.set_value(176), run_time=0.8)
        l176_.clear_updaters(); self.remove(l176_); self.add(l176)
        self.idle(lambda: LaggedStart(*[drop_into(ax, int(k_), BLUE_, 185) for k_ in rng.choice([4, 5, 6, 7, 8, 12, 13, 14, 15, 16], 10)], lag_ratio=0.1),
                  lambda: pulse(bars[10], b10g, s=1.08))

        # ── s033 rarer on both sides ──
        self.at("s033", 0.0)
        aL = Arrow(ax.c2p(8.6, 175), ax.c2p(4.2, 25), buff=0, color=WARN, stroke_width=7, max_tip_length_to_length_ratio=0.08)
        aR = Arrow(ax.c2p(11.4, 175), ax.c2p(15.8, 25), buff=0, color=WARN, stroke_width=7, max_tip_length_to_length_ratio=0.08)
        self.play(GrowArrow(aL), GrowArrow(aR), run_time=1.0)
        self.play(LaggedStart(*[AnimationGroup(bars[10 - d].animate(rate_func=there_and_back).set_fill(WARN),
                                               bars[10 + d].animate(rate_func=there_and_back).set_fill(WARN)) for d in range(1, 9)],
                              lag_ratio=0.35), run_time=1.8)

        # ── s034 standard deviation: spread ≈ 2.2 heads ──
        self.at("s034", 0.0)
        frm = card_cue("Standard Deviation", mini_sd())
        self.play(FadeOut(VGroup(aL, aR, dcard)), FadeIn(frm, shift=LEFT * 1.2), run_time=0.6)
        self.idle(lambda: pulse(frm, 1.08))
        # ── s034a: it is in the card at the top ──
        self.at("s034a", 0.0)
        cue_lab = T("card at the top", 26, VIOLET, weight=BOLD).next_to(frm, LEFT, buff=1.1)
        cue_arr = Arrow(cue_lab.get_right() + RIGHT * 0.1, frm.get_left() + LEFT * 0.05, color=VIOLET, stroke_width=5, buff=0.05)
        self.play(GrowArrow(cue_arr), FadeIn(cue_lab, shift=RIGHT * 0.2), run_time=0.5)
        self.idle(lambda: pulse(frm, 1.1), lambda: ShowPassingFlash(cue_arr.copy().set_stroke(VIOLET, 10), time_width=0.6))
        # ── s034b the typical spread ──
        self.at("s034b", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(cue_arr, cue_lab)), FadeOut(frm, shift=RIGHT), run_time=0.3)
        sd = np.sqrt(5)
        yb = 190
        sp = DoubleArrow(ax.c2p(10 - sd, yb), ax.c2p(10 + sd, yb), buff=0, color=VIOLET, stroke_width=4,
                         max_tip_length_to_length_ratio=0.12, tip_length=0.18)
        self.word("s034b", "typical", dt=-0.2)
        spl = VGroup(T("typical spread", 24, VIOLET, weight=BOLD), T("≈ 2.2 heads", 24, VIOLET, weight=BOLD)).arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(sp, RIGHT, buff=0.25)
        self.play(l176.animate.next_to(bars[10], RIGHT, buff=0.12).shift(UP * 1.2).set_opacity(0), run_time=0.3)
        self.play(GrowFromCenter(sp), FadeIn(spl), run_time=0.8)
        self.idle(lambda: LaggedStart(*[drop_into(ax, int(k_), BLUE_, 170) for k_ in rng.choice([4, 5, 6, 7, 8, 12, 13, 14, 15, 16], 10)], lag_ratio=0.1))

        # ── s035 where does fifteen land? ──
        self.at("s035", 0.0)
        pin = marker(ax.x_axis, 15, WARN, "15", height=1.35, fs=32)
        self.idle()
        self.play(FadeIn(pin, shift=DOWN * 0.8), run_time=0.6, rate_func=rate_functions.ease_out_bounce)
        self.play(ripple(ax.c2p(15, 0), WARN, r=0.2, scale=5), run_time=0.5)

        # ── s036 way out here: two spreads; ≈ 15 friends ──
        self.at("s036", 0.0)
        s1 = DoubleArrow(ax.c2p(10, 140), ax.c2p(10 + sd, 140), buff=0, color=VIOLET, stroke_width=3, tip_length=0.14)
        s2 = DoubleArrow(ax.c2p(10 + sd, 140), ax.c2p(10 + 2 * sd, 140), buff=0, color=VIOLET, stroke_width=3, tip_length=0.14)
        two = T("2 spreads", 24, VIOLET, weight=BOLD).next_to(VGroup(s1, s2), RIGHT, buff=0.2)
        for m in (s1, s2): m.set_z_index(3)
        self.play(GrowFromEdge(s1, LEFT), run_time=0.5)
        self.play(GrowFromEdge(s2, LEFT), FadeIn(two), run_time=0.5)
        self.until(word_time("s036", word_index("s036", "Only")) - 0.6)
        # zoom on the right tail: fade everything the zoom would cut
        zc = np.array([ax.c2p(16.4, 0)[0], ax.c2p(0, 0)[1] + 0.95, 0])
        self.play(FadeOut(VGroup(sp, spl, ch.xt, ch.yt, two, s1, s2, b10g, pin.lab)),
                  ch.labs.animate.set_opacity(0), run_time=0.4)
        self.remove(l176)
        zl = VGroup(*[T(str(v), 13, INK2).next_to(ax.c2p(v, 0), DOWN, buff=0.13) for v in range(12, 21)])
        self.play(fr.animate.scale(0.5).move_to(zc), FadeIn(zl),
                  *[bars[k].animate.set_fill(opacity=0.3) for k in range(12)], run_time=1.0)   # dim the middle: it runs under the chapter label
        self.play(*[bars[k].animate.set_fill(opacity=0.55) for k in (12, 13, 14)], run_time=0.3)
        pin2 = VGroup(pin[0], pin[1])
        self.play(bars[15].animate.set_fill(WARN, 1), run_time=0.4)
        l15 = T("≈ 15 friends", 15, WARN, weight=BOLD).next_to(bars[15], UP, buff=0.1).shift(RIGHT * 0.5)
        self.play(FadeOut(pin2), FadeIn(l15, shift=DOWN * 0.08), run_time=0.5)

        # ── s037 at least this well: outline 15..20, counting up ──
        self.at("s037", 0.0)
        cum = np.cumsum([EXP[k] for k in range(15, 21)])
        outl = VGroup(*[Rectangle(width=bars[k].width + 0.04, height=max(bars[k].height, 0.012) + 0.04)
                        .move_to(bars[k], aligned_edge=DOWN).shift(DOWN * 0.02).set_stroke(WARN, 2.5)
                        for k in range(15, 21)])
        for o in outl: o.qa_ignore = True   # thin outlines hug the bars
        tot = ValueTracker(EXP[15])
        tl = always_redraw(lambda: T(f"15 heads or more: ≈ {int(round(tot.get_value()))} friends", 17, INK, weight=BOLD)
                           .move_to(zc + UP * 1.35 + RIGHT * 0.2))
        self.add(tl)
        self.play(FadeOut(l15), run_time=0.3)
        self.until(word_time("s037", word_index("s037", "Fifteen")) - 0.2)
        for j, o in enumerate(outl):
            self.play(Create(o), tot.animate.set_value(cum[j]), run_time=0.55)
        tl.clear_updaters()

        # ── s038 fill in the tail ──
        self.at("s038", 0.0)
        self.play(LaggedStart(*[bars[k].animate.set_fill(AQUA, 1) for k in range(15, 21)], lag_ratio=0.25),
                  FadeOut(outl), run_time=1.0)
        tailg = glow(VGroup(*bars[15:]).copy().set_fill(opacity=0), AQUA, width=10, opacity=0.12)
        self.play(FadeIn(tailg), run_time=0.4)

        # ── s039 ≈ 21 of 1,000 → ≈ 2 in 100 ──
        self.at("s039", 0.0)
        n21 = TB("≈ 21 of 1,000", 30, AQUA).move_to(zc + UP * 0.75 + RIGHT * 0.2)
        self.play(FadeOut(tl), FadeIn(n21, scale=0.8), run_time=0.5)
        self.until(word_time("s039", word_index("s039", "roughly")) - 0.2)
        n2 = TB("≈ 2 in 100", 30, AQUA).move_to(n21)
        g100 = VGroup(*[Square(0.1, stroke_width=0, fill_color=(AQUA if i in (0, 1) else MUTED), fill_opacity=(1 if i < 2 else 0.5))
                        for i in range(100)]).arrange_in_grid(10, 10, buff=0.03)
        g100.next_to(n2, DOWN, buff=0.2)
        self.play(ReplacementTransform(n21, n2), LaggedStart(*[FadeIn(s_, scale=0.3) for s_ in g100], lag_ratio=0.01), run_time=0.9)
        self.play(*[Indicate(g100[i], color=AQUA, scale_factor=2.0) for i in (0, 1)], run_time=0.6)

        # ── s040 that is the p value ──
        self.at("s040", 0.0)
        pv = glow(TB("p ≈ 0.021", 44, AQUA), AQUA).move_to(zc + UP * 0.75 + RIGHT * 0.2)
        self.play(n2.animate.shift(UP * 0.45).scale(0.6).set_opacity(0.8), FadeOut(g100), run_time=0.4)
        self.until(word_time("s040", word_index("s040", "Zero")) - 0.2)
        self.play(FadeIn(pv, scale=0.6), run_time=0.6)
        self.play(ripple(pv.get_center(), AQUA, r=0.5, scale=3), run_time=0.6)
        self.idle(lambda: pulse(pv, 1.12), lambda: LaggedStart(*[bars[k].animate(rate_func=there_and_back).set_fill(opacity=0.4) for k in range(15, 21)], lag_ratio=0.15))

        # ── s041 in plain words ──
        self.at("s041", 0.0)
        self.idle()
        self.play(fr.animate.restore(), FadeOut(VGroup(pv, n2, zl, tailg)), run_time=1.0)
        self.play(FadeOut(VGroup(ax, bars, ch.labs)), run_time=0.4)
        lines = VGroup(
            T("IF the coin were fair,", 44, BLUE_, weight=BOLD),
            T("a result THIS EXTREME OR MORE", 44, WARN, weight=BOLD),
            T("happens only ≈ 2 times in 100", 44, AQUA, weight=BOLD)).arrange(DOWN, buff=0.4).move_to(UP * 0.5)
        for k, l in enumerate(lines):
            if k:
                self.until(word_time("s041", word_index("s041", ["fair,", "result", "happen"][k])) - 0.2)
            self.play(FadeIn(l, shift=UP * 0.2), run_time=0.5)

        # ── s042 about a million sequences ──
        self.at("s042", 0.0)
        self.play(FadeOut(lines, shift=UP * 0.3), run_time=0.5)
        seqs = VGroup(*[T(s, 24, MUTED) for s in ["HHTHTTHTHHTHHTTHTHHT", "TTHHTHHHTHTTHTHHTHTT", "HTTHHTHTHHHTTHTHHTHT",
                                                   "THHTHTTHHHTHTTHHHTHT", "…"]]).arrange(DOWN, buff=0.16).move_to(LEFT * 3.7 + UP * 0.5)
        big = VGroup(MathTex(r"2^{20}", font_size=96, color=INK), T("= 1,048,576", 52, INK, weight=BOLD)).arrange(RIGHT, buff=0.3)
        roll = ValueTracker(2)
        sub = VGroup(T("ways 20 flips can land,", 28, INK2), T("all equally likely", 28, INK2)).arrange(DOWN, buff=0.12)
        VGroup(big, sub).arrange(DOWN, buff=0.35).move_to(RIGHT * 3.4 + UP * 0.5)
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in seqs], lag_ratio=0.2), run_time=1.0)
        self.idle(lambda: LaggedStart(*[Indicate(s, color=INK, scale_factor=1.06) for s in seqs[:4]], lag_ratio=0.2))
        self.until(word_time("s042", word_index("s042", "million")) - 0.3)
        self.idle()
        rl = always_redraw(lambda: T(f"= {int(roll.get_value()):,}", 52, INK, weight=BOLD).move_to(big[1], aligned_edge=LEFT))
        self.play(FadeIn(big[0], scale=0.8), run_time=0.3)
        self.add(rl)
        self.play(roll.animate.set_value(1048576), run_time=1.2, rate_func=rate_functions.ease_in_expo)
        rl.clear_updaters(); self.remove(rl); self.add(big[1])
        self.play(FadeIn(sub), run_time=0.5)

        # ── s043 21,700 of them; divide ──
        self.at("s043", 0.0)
        eq = VGroup(MathTex("p", font_size=72, color=AQUA), T("=", 48, INK),
                    frac(r"\text{21,700}", r"\text{1,048,576}", WARN, 64), T("≈ 0.021", 52, AQUA, weight=BOLD)).arrange(RIGHT, buff=0.35)
        eq.move_to(DOWN * 0.1)
        self.play(FadeOut(seqs), VGroup(big, sub).animate.scale(0.7).move_to(UP * 2.4 + RIGHT * 1.6), run_time=0.6)
        w = T("sequences with 15+ heads", 26, WARN).next_to(eq[2], UP, buff=0.3)
        self.play(FadeIn(eq[2]), FadeIn(w), run_time=0.7)
        self.until(word_time("s043", word_index("s043", "Divide")) - 0.2)
        self.play(FadeIn(eq[0]), FadeIn(eq[1]), FadeIn(eq[3], shift=LEFT * 0.2), run_time=0.7)
        self.play(Circumscribe(eq[3], color=AQUA), run_time=0.8)
        full = Rectangle(width=9.0, height=0.36).set_stroke(MUTED, 2).set_fill("#22221f", 1).move_to(DOWN * 1.9)
        full.qa_container = True
        sliver = Rectangle(width=9.0 * 21700 / 1048576, height=0.36).set_stroke(width=0).set_fill(AQUA, 1).align_to(full, LEFT).move_to(full, coor_mask=[0, 1, 0])
        sliver.qa_joined = True
        bl_ = T("all 1,048,576 sequences", 22, MUTED).next_to(full, UP, buff=0.12).align_to(full, RIGHT)
        sl_ = T("15+ heads", 22, AQUA, weight=BOLD).next_to(full, UP, buff=0.12).align_to(full, LEFT)
        self.play(FadeIn(full), FadeIn(bl_), run_time=0.4)
        self.play(GrowFromEdge(sliver, LEFT), FadeIn(sl_), run_time=0.5)
        self.idle(lambda: pulse(sliver, 1.6), lambda: pulse(eq[3], 1.12))

        # ── s044 the symbols ──
        self.at("s044", 0.0)
        ftex = MathTex("p", "=", "P(", r"\text{data this extreme or more}", r"\;\mid\;", "H_0", ")", font_size=64)
        ftex[0].set_color(AQUA); ftex[3].set_color(WARN); ftex[5].set_color(BLUE_)
        ftex.move_to(UP * 1.9)
        self.idle()
        self.play(FadeOut(VGroup(big, sub, eq, w, full, sliver, bl_, sl_)), run_time=0.5)
        self.play(Write(ftex), run_time=1.6)
        self.word("s044", "probability", dt=-0.2)
        u1 = Underline(VGroup(ftex[2], ftex[3]), color=WARN, buff=0.08, stroke_width=5)
        self.play(Create(u1), run_time=0.5)
        self.word("s044", "given", dt=-0.2)
        u2 = Underline(VGroup(ftex[4], ftex[5], ftex[6]), color=BLUE_, buff=0.08, stroke_width=5)
        self.play(Create(u2), run_time=0.4)
        self.idle(lambda: pulse(ftex, 1.05))

        # ── s045 what each symbol means ──
        self.at("s045", 0.0)
        dP = defcard("P", "probability", INK, fs=28)
        dH = defcard("H_0", "the null hypothesis: the coin is fair", BLUE_, fs=28)
        dB = defcard(r"\mid", "given / assuming", INK, fs=28)
        defs = VGroup(dP, dH, dB).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(DOWN * 0.55)
        self.idle()
        self.play(FadeOut(VGroup(u1, u2)), run_time=0.3)
        links = VGroup()
        for d, word, part in zip(defs, ["capital", "zero", "straight"], [2, 5, 4]):
            self.until(word_time("s045", word_index("s045", word)) - 0.3)
            ln = DashedLine(ftex[part].get_bottom() + DOWN * 0.08, d.get_top() + UP * 0.05 + RIGHT * (ftex[part].get_x() - d.get_x()) * 0.0,
                            color=MUTED, stroke_width=2)
            ln.qa_ignore = True
            links.add(ln)
            self.play(Indicate(ftex[part], color=WARN, scale_factor=1.3), FadeIn(d, shift=UP * 0.2), run_time=0.6)

        # ── s046 remember the straight line ──
        self.at("s046", 0.0)
        self.play(ftex[4].animate.set_color(WARN), dB[0].animate.set_stroke(WARN, 3), dB[1][0].animate.set_color(WARN), run_time=0.5)
        bg_ = glow(ftex[4].copy(), WARN, width=16, opacity=0.1)
        assume = pill("assuming the coin is fair", WARN, 26).next_to(dB, RIGHT, buff=0.5)
        self.play(FadeIn(bg_), FadeIn(assume, shift=LEFT * 0.2), run_time=0.6)
        self.play(Indicate(ftex[4], color=WARN, scale_factor=1.4), run_time=0.8)
        self.idle(lambda: pulse(assume, 1.12))

        # ── s047 one honest detail: two-sided ──
        self.at("s047", 0.0)
        ch2 = dist_chart().move_to(RIGHT * 0.6 + UP * 0.3)
        bars2 = dist_bars(ch2.ax, BLUE_)
        for k in range(15, 21): bars2[k].set_fill(AQUA, 1)
        self.idle()
        self.play(FadeOut(VGroup(ftex, defs, bg_, assume)), run_time=0.5)
        self.play(FadeIn(ch2), FadeIn(bars2), run_time=0.7)
        one = T("one-sided: p ≈ 0.021", 28, AQUA, weight=BOLD).move_to(ch2.ax.c2p(16.5, 120))
        self.play(FadeIn(one), run_time=0.4)
        self.until(word_time("s047", word_index("s047", "either")) - 0.2)
        bl = VGroup(*[bars2[k] for k in range(0, 6)])
        self.play(LaggedStart(*[b_.animate.set_fill(AQUA, 0.8) for b_ in reversed(bl)], lag_ratio=0.2),
                  ripple(ch2.ax.c2p(4, 10), AQUA, r=0.2, scale=5), run_time=0.8)
        lt = T("other tail: 5 heads or fewer", 20, AQUA).next_to(ch2.ax.c2p(0.4, 98), RIGHT, buff=0)
        self.play(FadeIn(lt), run_time=0.4)
        self.until(word_time("s047", word_index("s047", "double")) - 0.2)
        two_s = TB("two-sided: p ≈ 0.041", 34, AQUA).move_to(UP * 3.25 + RIGHT * 1.6)
        self.play(FadeIn(two_s, shift=DOWN * 0.2), run_time=0.6)
        self.idle(lambda: pulse(two_s, 1.12), lambda: LaggedStart(*[pulse(b_, 1.3) for b_ in list(bl) + list(bars2[15:])], lag_ratio=0.05))
        self.until(SEGS["s047"]["end"] - 0.6)
        self.idle()
        self.play(FadeOut(VGroup(ch2, bars2, one, lt, two_s), shift=LEFT * 1.0), run_time=0.6)
        self.finish()
