import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cm import *

NAMES = ["A", "B", "C", "lazy"]
COLS = [AQUA, VIOLET, ORANGE_, MUTED]
COST1 = [5150, 27525, 2005, 50000]
COST2 = [11000, 28500, 60700, 50000]


class S11Costs(Base):
    CHAPTER = "Which Error Is Worse?"

    def construct(self):
        # ── s134 which mistake would you rather make? ──
        self.at("s134", 0.0)
        fp = side_card(["a false alarm"], ORANGE_, 30, title="FALSE POSITIVE", title_color=ORANGE_).move_to(LEFT * 3.0 + UP * 0.6)
        fn = side_card(["a missed fraud"], BLUE_, 30, title="FALSE NEGATIVE", title_color=BLUE_).move_to(RIGHT * 3.0 + UP * 0.6)
        vs = T("or", 34, INK2).move_to(UP * 0.6)
        self.play(FadeIn(fp, shift=RIGHT * 0.2), FadeIn(fn, shift=LEFT * 0.2), FadeIn(vs), run_time=0.7)
        q = T("which mistake would you rather make?", 32, INK, weight=BOLD).move_to(DOWN * 1.3)
        self.word("s134", "mistake")
        self.play(FadeIn(q), run_time=0.5)
        # ── s135 made-up prices ──
        self.at("s135", 0.0)
        il = pill("illustration: made-up costs", MUTED, 24).move_to(UP * 2.3)
        self.word("s135", "made")
        self.play(FadeIn(il), FadeOut(q), run_time=0.5)
        # ── s136 $500 vs $5 ──
        self.at("s136", 0.0)
        p_fn = TB("$500 each", 40, BLUE_).next_to(fn, DOWN, buff=0.4)
        p_fp = TB("$5 each", 40, ORANGE_).next_to(fp, DOWN, buff=0.4)
        self.word("s136", "five")
        self.play(FadeIn(p_fn, shift=UP * 0.15), run_time=0.5)
        self.word("s136", "five", nth=1)
        self.play(FadeIn(p_fp, shift=UP * 0.15), run_time=0.5)
        why = T("a few minutes on the phone", 24, INK2).next_to(p_fp, DOWN, buff=0.2)
        self.word("s136", "minutes")
        self.play(FadeIn(why), run_time=0.4)

        # ── s137 – s140 the bill for each detector ──
        self.at("s137", 0.0)
        tag_fn = pill("miss $500", BLUE_, 24); tag_fp = pill("false alarm $5", ORANGE_, 24)
        tags = VGroup(tag_fn, tag_fp).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(RIGHT * 4.4 + UP * 2.15)
        self.play(FadeOut(VGroup(fp, fn, vs, why)), ReplacementTransform(p_fn, tag_fn), ReplacementTransform(p_fp, tag_fp),
                  il.animate.move_to(LEFT * 0.6 + UP * 2.35), run_time=0.6)
        ax = xy_axes([0, 4, 1], [0, 70000, 10000], 6.4, 3.8, None, "total cost ($)", x_labels={}, font_size=20)
        ax.move_to(LEFT * 2.3 + DOWN * 0.05)
        for t in ax.labs:
            v = t.text
            if v.isdigit() and int(v) >= 1000:
                t.become(T(f"{int(v) // 1000}k", 20, INK2).move_to(t, aligned_edge=RIGHT))
        xl = VGroup(*[T(n, 24, c, weight=BOLD).next_to(ax.ax.c2p(i + 0.5, 0), DOWN, buff=0.18) for i, (n, c) in enumerate(zip(NAMES, COLS))])
        self.play(FadeIn(ax), FadeIn(xl), run_time=0.5)
        bars, vals = [None] * 4, [None] * 4
        eqs = ["10 × 500 + 30 × 5", "55 × 500 + 5 × 5", "1 × 500 + 301 × 5", "100 × 500"]
        eqm = None
        for i, (sid, w) in enumerate((("s137", "Five"), ("s138", "Twenty-seven"), ("s139", "Only"), ("s140", "Fifty"))):
            self.at(sid, 0.0)
            e = VGroup(T(f"{NAMES[i]}:", 28, COLS[i], weight=BOLD), T(eqs[i], 28, INK)).arrange(RIGHT, buff=0.2)
            e.move_to(RIGHT * 4.3 + UP * 1.0)
            self.play(*( [FadeOut(eqm)] if eqm else []), FadeIn(e), run_time=0.5)
            eqm = e
            self.word(sid, w)
            bars[i] = vbar(ax.ax, i + 0.5, COST1[i], COLS[i], 0.8)
            vals[i] = value_label(bars[i], f"${COST1[i]:,}", COLS[i], 22)
            self.play(GrowFromEdge(bars[i], DOWN), FadeIn(vals[i]), run_time=0.7)
        # ── s141 the cheapest is C ──
        self.at("s141", 0.0)
        self.play(FadeOut(eqm), run_time=0.3)
        best = VGroup(T("cheapest: C", 30, ORANGE_, weight=BOLD), T("(worst accuracy!)", 24, INK2),
                      T("misses are expensive", 24, INK), T("→ you want high recall", 24, ORANGE_, weight=BOLD)
                      ).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to(RIGHT * 4.4 + UP * 0.5)
        self.word("s141", "C,")
        self.play(FadeIn(best[:2]), highlight(bars[2], color=ORANGE_), run_time=0.8)
        self.word("s141", "Because")
        self.play(FadeIn(best[2:]), run_time=0.5)
        # ── s142 change the prices ──
        self.at("s142", 0.0)
        self.play(FadeOut(best), run_time=0.3)
        tag_fp2 = pill("false alarm $200", RED_, 24).move_to(tag_fp, aligned_edge=LEFT)
        why2 = VGroup(T("a frozen card at the checkout", 24, INK2), T("= an annoyed, lost customer", 24, INK2)
                      ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to(RIGHT * 4.4 + UP * 0.9)
        self.word("s142", "freezes")
        self.play(FadeIn(why2), run_time=0.5)
        self.word("s142", "two")
        self.play(FadeOut(tag_fp), FadeIn(tag_fp2), run_time=0.5)
        # ── s143 C is now the worst; A wins ──
        self.at("s143", 0.0)
        self.play(FadeOut(why2), run_time=0.3)
        anims = []
        for i in range(4):
            nb = vbar(ax.ax, i + 0.5, COST2[i], COLS[i], 0.8)
            nv = value_label(nb, f"${COST2[i]:,}", COLS[i], 22)
            anims += [Transform(bars[i], nb), Transform(vals[i], nv)]
        self.play(*anims, run_time=1.2, rate_func=rate_functions.ease_in_out_sine)
        aw = VGroup(T("now A wins", 30, AQUA, weight=BOLD), T("C is the worst", 24, ORANGE_)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        aw.move_to(RIGHT * 4.4 + UP * 0.7)
        self.word("s143", "A")
        self.play(FadeIn(aw), highlight(bars[0], color=AQUA), run_time=0.8)
        # ── s144 counts are maths, costs are your call ──
        self.at("s144", 0.0)
        cap = VGroup(T("the counts are math", 30, INK, weight=BOLD), T("the costs are your call", 30, WARN, weight=BOLD)
                     ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(RIGHT * 4.4 + DOWN * 0.6)
        self.word("s144", "counts.")
        self.play(FadeIn(cap[0]), run_time=0.5)
        self.word("s144", "decide")
        self.play(FadeIn(cap[1]), run_time=0.5)
        self.until(SEGS["s144"]["end"] + 0.1)
        self.play(FadeOut(VGroup(ax, xl, *bars, *vals, aw, cap, tag_fn, tag_fp2, il)), run_time=0.5)
        self.finish()
