import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cm import *

GA = np.array([-3.0, 0.05, 0])     # cells centre of the small Detector A grid
GB = np.array([3.9, 0.05, 0])      # … and of Detector B
S = 0.6

# illustration for the dial: suspicion scores of 20 fraud and 40 normal payments
_r = np.random.default_rng(5)
FRAUD_SC = np.sort(_r.uniform(0.32, 0.98, 20))
FINE_SC = np.sort(_r.uniform(0.02, 0.72, 40))


def side_lines(rows, anchor, color=INK):
    g = VGroup(*[T(t, 26, c, weight=BOLD) for t, c in rows]).arrange(DOWN, buff=0.12)
    return g.next_to(anchor, DOWN, buff=0.35)


class S09Tradeoff(Base):
    CHAPTER = "The Trade-off"

    def construct(self):
        g = grid_at(counts=A_COUNTS)
        show_grid(self, g)
        # ── s104 two grids side by side ──
        self.at("s104", 0.0)
        a = grid_at(S, GA, counts=A_COUNTS, names=False, rows=("fraud", "fine"), col_title="", row_title="",
                    label_size=40, num_size=70)
        self.play(FadeOut(g.names), run_time=0.3)
        self.play(ReplacementTransform(VGroup(g.cells, *[g.num[k] for k in KEYS], g.collab, g.rowlab),
                                       VGroup(a.cells, *[a.num[k] for k in KEYS], a.collab, a.rowlab)),
                  FadeOut(VGroup(g.coltitle, g.rowtitle)), run_time=0.9)
        ca = pill("Detector A", AQUA, 28).move_to(GA + UP * 2.25)
        b = grid_at(S, GB, names=False, rows=("fraud", "fine"), col_title="", row_title="", label_size=40, num_size=70)
        cb = pill("Detector B", VIOLET, 28).move_to(GB + UP * 2.25)
        self.word("s104", "Detector")
        self.play(FadeIn(ca), FadeIn(cb), FadeIn(VGroup(b.cells, b.collab, b.rowlab)), run_time=0.7)
        # ── s105 / s106 B raises 50 alarms: 45 real, 5 false ──
        self.at("s105", 0.0)
        fc = b.frame_of(b.col0(), VIOLET)
        self.word("s105", "fifty")
        self.play(Create(fc), run_time=0.6)
        self.at("s106", 0.0)
        self.word("s106", "Forty-five")
        self.play(b.set_num("TP", 45), b.light("TP"), run_time=0.5)
        self.word("s106", "Five")
        self.play(b.set_num("FP", 5), b.light("FP"), run_time=0.5)
        pb = T("precision  45/50 = 90%", 26, VIOLET, weight=BOLD).move_to(GB + DOWN * 1.4)
        self.word("s106", "precision")
        self.play(FadeIn(pb), run_time=0.5)
        ok = pill("claim true ✓", VIOLET, 24).next_to(cb, LEFT, buff=0.35)
        self.word("s106", "true")
        self.play(FadeIn(ok), run_time=0.4)
        # ── s107 / s108 the top row: 55 missed ──
        self.at("s107", 0.0)
        self.play(FadeOut(fc), run_time=0.3)
        fr = b.frame_of(b.row0(), ORANGE_)
        self.word("s107", "top")
        self.play(Create(fr), run_time=0.5)
        self.word("s107", "fifty-five")
        self.play(b.set_num("FN", 55, BLUE_), b.light("FN"), run_time=0.5)
        self.at("s108", 0.0)
        rb = T("recall  45/100 = 45%", 26, ORANGE_, weight=BOLD).next_to(pb, DOWN, buff=0.15)
        self.play(FadeIn(rb), run_time=0.5)
        self.word("s108", "half")
        self.play(highlight(b.num["FN"], color=BLUE_), run_time=0.8)
        # ── s109 accuracy still 99.4% ──
        self.at("s109", 0.0)
        self.play(FadeOut(fr), run_time=0.3)
        self.word("s109", "nine")
        self.play(b.set_num("TN", 9895), b.light("TN"), run_time=0.5)
        ab = T("accuracy  99.4%", 26, WARN, weight=BOLD).next_to(rb, DOWN, buff=0.15)
        self.word("s109", "point")
        self.play(FadeIn(ab), run_time=0.5)
        # ── s110 side by side ──
        self.at("s110", 0.0)
        pa = T("precision  90/120 = 75%", 26, VIOLET, weight=BOLD).move_to(GA + DOWN * 1.4)
        ra = T("recall  90/100 = 90%", 26, ORANGE_, weight=BOLD).next_to(pa, DOWN, buff=0.15)
        aa = T("accuracy  99.6%", 26, WARN, weight=BOLD).next_to(ra, DOWN, buff=0.15)
        self.word("s110", "A:")
        self.play(FadeIn(VGroup(pa, ra, aa)), run_time=0.6)
        self.word("s110", "B:")
        self.play(highlight(pb, rb, color=INK2), run_time=0.8)

        # ── s111 each quoted their good number: a bar chart ──
        self.at("s111", 0.0)
        self.play(FadeOut(VGroup(grid_mobs(a), grid_mobs(b), pa, ra, aa, pb, rb, ab, ok)), FadeOut(VGroup(ca, cb)), run_time=0.5)
        ax = bars_axes(2, ["Detector A", "Detector B"], 100, 25, 6.0, 3.6, "percent").move_to(LEFT * 1.6 + DOWN * 0.1)
        bars = VGroup(vbar(ax.ax, 0.38, 75, VIOLET, 0.55), vbar(ax.ax, 0.62, 90, ORANGE_, 0.55),
                      vbar(ax.ax, 1.38, 90, VIOLET, 0.55), vbar(ax.ax, 1.62, 45, ORANGE_, 0.55))
        vals = VGroup(*[value_label(bb, t, c) for bb, t, c in zip(bars, ["75", "90", "90", "45"], [VIOLET, ORANGE_, VIOLET, ORANGE_])])
        leg = VGroup(VGroup(Square(0.25, stroke_width=0, fill_color=VIOLET, fill_opacity=1), T("precision", 26, VIOLET, weight=BOLD)).arrange(RIGHT, buff=0.15),
                     VGroup(Square(0.25, stroke_width=0, fill_color=ORANGE_, fill_opacity=1), T("recall", 26, ORANGE_, weight=BOLD)).arrange(RIGHT, buff=0.15)
                     ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(RIGHT * 4.3 + UP * 1.6)
        self.play(FadeIn(ax), FadeIn(leg), run_time=0.5)
        self.play(*[GrowFromEdge(x, DOWN) for x in bars], run_time=0.9)
        self.play(FadeIn(vals), run_time=0.4)
        q1 = pill("A quoted its recall", AQUA, 24).move_to(RIGHT * 4.3 + UP * 0.1)
        q2 = pill("B quoted its precision", VIOLET, 24).next_to(q1, DOWN, buff=0.3)
        self.word("s111", "quoted")
        self.play(FadeIn(q1), highlight(bars[1], color=AQUA), run_time=0.8)
        self.play(FadeIn(q2), highlight(bars[2], color=VIOLET), run_time=0.8)
        dq = T("different questions", 26, INK2).next_to(q2, DOWN, buff=0.35)
        self.word("s111", "different")
        self.play(FadeIn(dq), run_time=0.4)
        # ── s112 the same swap as the prosecutor's fallacy ──
        self.at("s112", 0.0)
        self.play(FadeOut(VGroup(ax, bars, vals, leg, q1, q2, dq)), run_time=0.5)
        chipf = pill("from: The Prosecutor's Fallacy", INK2, 26).move_to(UP * 1.9)
        self.play(FadeIn(chipf), run_time=0.4)
        s1 = VGroup(T("an alarm  →  fraud?", 34, INK, weight=BOLD), T("precision", 30, VIOLET, weight=BOLD)).arrange(RIGHT, buff=0.6)
        s2 = VGroup(T("fraud  →  an alarm?", 34, INK, weight=BOLD), T("recall", 30, ORANGE_, weight=BOLD)).arrange(RIGHT, buff=0.6)
        VGroup(s1, s2).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(DOWN * 0.1)
        self.word("s112", "alarm")
        self.play(FadeIn(s1[0]), run_time=0.4)
        self.play(FadeIn(s1[1]), run_time=0.3)
        self.word("s112", "versus")
        self.play(FadeIn(s2[0]), run_time=0.4)
        self.play(FadeIn(s2[1]), run_time=0.3)

        # ── s113 / s114 one model, a score, a cut-off ──
        self.at("s113", 0.0)
        self.play(FadeOut(VGroup(chipf, s1, s2)), run_time=0.4)
        same = TB("A and B: often the same model", 40, INK).move_to(UP * 1.9)
        self.play(FadeIn(same), run_time=0.5)
        self.at("s114", 0.0)
        nl = NumberLine(x_range=[0, 1, 0.1], length=7.0, include_tip=False, color=INK2, stroke_width=3, tick_size=0.07)
        nl.move_to(LEFT * 1.7 + DOWN * 1.25)
        ticks = VGroup(*[T(f"{v:.1f}" if v not in (0, 1) else str(v), 20, INK2).next_to(nl.n2p(v), DOWN, buff=0.14) for v in (0, 0.5, 1)])
        nt = T("suspicion score (illustration)", 22, MUTED).next_to(ticks, DOWN, buff=0.08)
        jit = np.random.default_rng(9)
        fdots = VGroup(*[Dot(nl.n2p(v) + UP * (1.25 + 0.22 * (i % 3)), radius=0.07, color=RED_) for i, v in enumerate(FRAUD_SC)])
        ndots = VGroup(*[Dot(nl.n2p(v) + UP * (0.25 + 0.22 * (i % 3)), radius=0.07, color=INK2) for i, v in enumerate(FINE_SC)])
        lf = T("fraud", 22, RED_, weight=BOLD)
        lfine = T("normal", 22, INK2, weight=BOLD)
        lf.move_to([nl.get_left()[0] - 0.3 - lf.width / 2, fdots.get_y(), 0])
        lfine.move_to([nl.get_left()[0] - 0.3 - lfine.width / 2, ndots.get_y(), 0])
        self.play(FadeOut(same), Create(nl), FadeIn(ticks), FadeIn(nt), run_time=0.6)
        self.word("s114", "score,")
        self.play(LaggedStart(*[FadeIn(d) for d in list(fdots) + list(ndots)], lag_ratio=0.01), FadeIn(lf), FadeIn(lfine), run_time=1.0)
        cut = ValueTracker(0.55)
        def mk_line():
            x = nl.n2p(cut.get_value())[0]
            ln = DashedLine([x, nl.get_y() + 0.05, 0], [x, nl.get_y() + 2.15, 0], color=WARN, stroke_width=4)
            ln.qa_ignore = True
            return ln
        cl = always_redraw(mk_line)
        def mk_zone():
            x = nl.n2p(cut.get_value())[0]
            r = Rectangle(width=max(0.01, nl.n2p(1)[0] - x), height=2.1).set_stroke(width=0).set_fill(WARN, 0.08)
            r.move_to([x, nl.get_y() + 1.1, 0], aligned_edge=LEFT)
            r.qa_ignore = True
            return r
        zone = always_redraw(mk_zone)
        self.word("s114", "cut-off.")
        self.add(zone)
        self.play(Create(cl), run_time=0.5)
        al = T("alarm →", 24, WARN, weight=BOLD).next_to(nl.n2p(1), UP, buff=2.35).shift(LEFT * 0.6)
        qu = T("← quiet", 24, INK2, weight=BOLD).next_to(nl.n2p(0), UP, buff=2.35).shift(RIGHT * 0.6)
        self.word("s114", "Above")
        self.play(FadeIn(al), run_time=0.3)
        self.word("s114", "Below")
        self.play(FadeIn(qu), run_time=0.3)
        # live precision / recall bars
        pax = xy_axes([0, 2, 1], [0, 100, 50], 2.6, 2.4, None, "percent", x_labels={}, font_size=20).move_to(RIGHT * 4.6 + DOWN * 0.2)
        pl = VGroup(T("precision", 22, VIOLET, weight=BOLD).next_to(pax.ax.c2p(0.5, 0), DOWN, buff=0.15),
                    T("recall", 22, ORANGE_, weight=BOLD).next_to(pax.ax.c2p(1.5, 0), DOWN, buff=0.15))
        def pr():
            c = cut.get_value()
            tp = int((FRAUD_SC >= c).sum()); fp = int((FINE_SC >= c).sum())
            return (100 * tp / max(1, tp + fp)), (100 * tp / len(FRAUD_SC))
        pbar = always_redraw(lambda: vbar(pax.ax, 0.5, max(0.5, pr()[0]), VIOLET, 0.7))
        rbar = always_redraw(lambda: vbar(pax.ax, 1.5, max(0.5, pr()[1]), ORANGE_, 0.7))
        self.play(FadeIn(pax), FadeIn(pl), FadeIn(pbar), FadeIn(rbar), run_time=0.5)

        # ── s115 cut-off high: Detector B ──
        self.at("s115", 0.0)
        self.word("s115", "high,")
        self.play(cut.animate.set_value(0.8), run_time=1.6, rate_func=rate_functions.ease_in_out_sine)
        tb_ = pill("= Detector B", VIOLET, 24).move_to(RIGHT * 4.6 + UP * 1.75)
        self.word("s115", "That's")
        self.play(FadeIn(tb_), run_time=0.4)
        # ── s116 cut-off low: Detector A ──
        self.at("s116", 0.0)
        ta_ = pill("= Detector A", AQUA, 24).move_to(tb_)
        self.word("s116", "low,")
        self.play(FadeOut(tb_), cut.animate.set_value(0.42), run_time=1.6, rate_func=rate_functions.ease_in_out_sine)
        self.word("s116", "That's")
        self.play(FadeIn(ta_), run_time=0.4)
        # ── s117 even lower: Detector C ──
        self.at("s117", 0.0)
        tc_ = pill("= Detector C", ORANGE_, 24).move_to(ta_)
        self.word("s117", "lower,")
        self.play(FadeOut(ta_), cut.animate.set_value(0.28), run_time=1.3, rate_func=rate_functions.ease_in_out_sine)
        self.play(FadeIn(tc_), run_time=0.3)
        self.word("s117", "four")
        dial = VGroup(nl, ticks, nt, fdots, ndots, lf, lfine, al, qu, pax, pl, tc_)
        self.play(FadeOut(dial), FadeOut(cl), FadeOut(zone), FadeOut(pbar), FadeOut(rbar), run_time=0.5)
        self.remove(cl, zone, pbar, rbar)
        c = grid_at(0.75, np.array([-2.2, -0.3, 0]), counts=C_COUNTS, names=False, rows=("fraud", "fine"),
                    row_title="", col_title="", label_size=36, num_size=64, show_lit=True)
        cc = pill("Detector C · nervous", ORANGE_, 28).move_to(np.array([-2.2, 2.2, 0]))
        self.play(FadeIn(grid_mobs(c)), FadeIn(cc), run_time=0.6)
        # ── s118 99% recall, ~25% precision ──
        self.at("s118", 0.0)
        r1 = T("recall  99/100 = 99%", 30, ORANGE_, weight=BOLD)
        p1 = T("precision  99/400 ≈ 25%", 30, VIOLET, weight=BOLD)
        VGroup(r1, p1).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 4.0 + UP * 0.9)
        fr_ = c.frame_of(c.row0(), ORANGE_)
        self.play(FadeIn(r1), Create(fr_), run_time=0.6)
        fc_ = c.frame_of(c.col0(), VIOLET)
        self.word("s118", "only")
        self.play(FadeIn(p1), ReplacementTransform(fr_, fc_), run_time=0.6)
        # ── s119 accuracy points the wrong way ──
        self.at("s119", 0.0)
        a1 = T("accuracy  96.98%", 30, WARN, weight=BOLD).next_to(p1, DOWN, buff=0.3).align_to(p1, LEFT)
        lz = T("lazy detector: 99%", 26, MUTED).next_to(a1, DOWN, buff=0.2).align_to(p1, LEFT)
        self.play(FadeOut(fc_), FadeIn(a1), run_time=0.5)
        self.word("s119", "lazy")
        self.play(FadeIn(lz), run_time=0.4)
        wr = pill("accuracy points the wrong way", RED_, 22).next_to(lz, DOWN, buff=0.35).align_to(p1, LEFT)
        self.word("s119", "wrong")
        self.play(FadeIn(wr), run_time=0.4)

        # ── s120 the seesaw ──
        self.at("s120", 0.0)
        self.play(FadeOut(VGroup(grid_mobs(c), cc, r1, p1, a1, lz, wr)), run_time=0.5)
        beam, th, L, R = beam_scale(6.0)
        beam.move_to(DOWN * 0.2)
        for x in beam.get_family():
            x.qa_ignore = True
        lp = T("precision", 30, VIOLET, weight=BOLD)
        rp = T("recall", 30, ORANGE_, weight=BOLD)
        lp.add_updater(lambda m: m.next_to(L[0], DOWN, buff=0.3))
        rp.add_updater(lambda m: m.next_to(R[0], DOWN, buff=0.3))
        self.add(beam, lp, rp)
        self.play(FadeIn(beam), FadeIn(lp), FadeIn(rp), run_time=0.6)
        self.word("s120", "way,")
        self.play(th.animate.set_value(-0.22), run_time=1.0, rate_func=rate_functions.ease_in_out_sine)
        self.word("s120", "back,")
        self.play(th.animate.set_value(0.22), run_time=1.2, rate_func=rate_functions.ease_in_out_sine)
        ff = T("you almost never get both for free", 30, INK2).move_to(UP * 2.3)
        self.word("s120", "never")
        self.play(FadeIn(ff), th.animate.set_value(0.0), run_time=0.8, rate_func=rate_functions.ease_in_out_sine)
        # ── s121 the ROC curve, later ──
        self.at("s121", 0.0)
        roc = pill("later: the ROC curve traces this whole dial", MUTED, 26).move_to(DOWN * 2.2)
        self.word("s121", "curve,")
        self.play(FadeIn(roc), run_time=0.5)
        self.until(SEGS["s121"]["end"] + 0.1)
        lp.clear_updaters(); rp.clear_updaters()
        self.play(FadeOut(VGroup(beam, lp, rp, ff, roc)), run_time=0.5)
        self.finish()
