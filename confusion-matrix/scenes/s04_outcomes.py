import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cm import *

# warm-up: ten payments, three fraud (1, 4, 7); where each one lands
WARM = {1: "TP", 2: "TN", 3: "FP", 4: "FN", 5: "TN", 6: "FP", 7: "TP", 8: "TN", 9: "TN", 10: "TN"}


def clean_grid():
    """The grid as it is left at the end of this scene and picked up by 'Filling the Grid'."""
    return grid_at()


class S04Outcomes(Base):
    CHAPTER = "The Four Outcomes"

    def construct(self):
        # ── s029 one payment, two facts ──
        self.at("s029", 0.0)
        pc = payment_card(INK2, 1.6).move_to(UP * 1.2)
        self.play(FadeIn(pc, shift=UP * 0.2), run_time=0.6)
        # ── s030 / s031 the truth and the guess ──
        self.at("s030", 0.0)
        t1 = pill("the truth: fraud or not?", ORANGE_, 30).move_to(LEFT * 3.4 + DOWN * 0.6)
        self.play(FadeIn(t1, shift=UP * 0.2), run_time=0.5)
        self.at("s031", 0.0)
        t2 = pill("what it said: alarm or quiet?", VIOLET, 30).move_to(RIGHT * 3.4 + DOWN * 0.6)
        self.play(FadeIn(t2, shift=UP * 0.2), run_time=0.5)
        # ── s032 2 × 2 = 4 ──
        self.at("s032", 0.0)
        four = VGroup(TB("2", 64, ORANGE_), T("×", 50, INK2), TB("2", 64, VIOLET), T("=", 50, INK2), TB("4", 72, AQUA)
                      ).arrange(RIGHT, buff=0.3).move_to(DOWN * 1.9)
        self.word("s032", "Two")
        self.play(FadeIn(four[:3]), run_time=0.5)
        self.word("s032", "four")
        self.play(FadeIn(four[3:], shift=LEFT * 0.2), run_time=0.5)
        ol = T("possible outcomes", 26, AQUA).next_to(four, RIGHT, buff=0.35)
        self.play(FadeIn(ol), run_time=0.4)

        # ── s033 rows = the truth ──
        self.at("s033", 0.0)
        g = grid_at()
        for k in KEYS:
            g.name[k].set_opacity(0)
        self.play(FadeOut(VGroup(pc, t1, t2, four, ol)), run_time=0.5)
        self.word("s033", "grid")
        self.play(LaggedStart(*[Create(g.cell[k]) for k in KEYS], lag_ratio=0.15), run_time=0.9)
        self.word("s033", "rows")
        self.play(FadeIn(g.rowtitle), run_time=0.4)
        self.word("s033", "top")
        self.play(FadeIn(g.rowlab[0], shift=RIGHT * 0.2), highlight(g.row0(), color=ORANGE_), run_time=0.9)
        self.word("s033", "bottom")
        self.play(FadeIn(g.rowlab[1], shift=RIGHT * 0.2), highlight(g.row1(), color=INK2), run_time=0.9)
        # ── s034 columns = what it said ──
        self.at("s034", 0.0)
        self.play(FadeIn(g.coltitle), run_time=0.4)
        self.word("s034", "left")
        self.play(FadeIn(g.collab[0], shift=DOWN * 0.2), run_time=0.5)
        self.word("s034", "right")
        self.play(FadeIn(g.collab[1], shift=DOWN * 0.2), run_time=0.5)

        # ── s035 name each box ──
        self.at("s035", 0.0)
        self.word("s035", "name")
        self.play(LaggedStart(*[highlight(g.cell[k], color=INK2) for k in KEYS], lag_ratio=0.25), run_time=1.6)

        def explain(lines, color):
            c = side_card(lines, color, 28)
            c.move_to(RIGHT * PANEL_X + UP * 0.55)
            return c

        # ── s036 true positive ──
        self.at("s036", 0.0)
        e = explain(["really fraud", "→ alarm  ✓"], AQUA)
        self.word("s036", "fraud")
        self.play(g.light("TP"), FadeIn(e, shift=LEFT * 0.2), run_time=0.6)
        self.word("s036", "true")
        self.play(g.name["TP"].animate.set_opacity(1), run_time=0.5)
        # ── s037 decoding the words ──
        self.at("s037", 0.0)
        d = VGroup(
            VGroup(T("POSITIVE", 28, VIOLET, weight=BOLD), T("= it said yes", 28, INK)).arrange(RIGHT, buff=0.2),
            VGroup(T("TRUE", 28, AQUA, weight=BOLD), T("= it was right", 28, INK)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        dc = side_card([d], INK2).move_to(RIGHT * PANEL_X + DOWN * 1.45)
        self.word("s037", "Positive")
        self.play(FadeIn(dc, shift=UP * 0.2), run_time=0.5)
        # ── s038 true negative ──
        self.at("s038", 0.0)
        e2 = explain(["really fine", "→ quiet  ✓"], AQUA)
        self.play(FadeOut(dc), FadeOut(e), FadeIn(e2), run_time=0.5)
        e = e2
        self.word("s038", "quiet")
        self.play(g.light("TN"), run_time=0.5)
        self.word("s038", "true")
        self.play(g.name["TN"].animate.set_opacity(1), run_time=0.5)
        # ── s039 / s040 false positive ──
        self.at("s039", 0.0)
        e2 = explain(["really fine", "→ alarm  ✗"], ORANGE_)
        self.word("s039", "left")
        self.play(FadeOut(e), FadeIn(e2), g.cell["FP"].animate.set_stroke(ORANGE_, 4), run_time=0.6)
        e = e2
        self.at("s040", 0.0)
        self.word("s040", "false", nth=1)
        self.play(g.light("FP"), g.name["FP"].animate.set_opacity(1), run_time=0.6)
        fa = T("a false alarm", 26, ORANGE_).next_to(e, DOWN, buff=0.3)
        self.play(FadeIn(fa), run_time=0.4)
        # ── s041 / s042 false negative ──
        self.at("s041", 0.0)
        e2 = explain(["really fraud", "→ quiet  ✗"], BLUE_)
        self.word("s041", "right")
        self.play(FadeOut(fa), FadeOut(e), FadeIn(e2), g.cell["FN"].animate.set_stroke(BLUE_, 4), run_time=0.6)
        e = e2
        self.at("s042", 0.0)
        self.word("s042", "false")
        self.play(g.light("FN"), g.name["FN"].animate.set_opacity(1), run_time=0.6)
        ms = T("a miss", 26, BLUE_).next_to(e, DOWN, buff=0.3)
        self.play(FadeIn(ms), run_time=0.4)

        # ── s043 the trick: second word = what it said, first word = right or wrong ──
        self.at("s043", 0.0)
        self.play(FadeOut(VGroup(e, ms)), run_time=0.4)
        w1 = TB("FALSE", 36, RED_); w2 = TB("POSITIVE", 36, VIOLET)
        words = VGroup(w1, w2).arrange(RIGHT, buff=0.35).move_to(RIGHT * PANEL_X + UP * 1.2)
        self.play(FadeIn(words), run_time=0.5)
        a2 = Arrow(w2.get_bottom(), w2.get_bottom() + DOWN * 1.7, buff=0.12, color=VIOLET, stroke_width=4)
        l2 = T("what it said", 26, VIOLET, weight=BOLD).next_to(a2, DOWN, buff=0.12)
        a1 = Arrow(w1.get_bottom(), w1.get_bottom() + DOWN * 0.7, buff=0.12, color=RED_, stroke_width=4)
        l1 = T("right or wrong?", 26, RED_, weight=BOLD).next_to(a1, DOWN, buff=0.12)
        self.word("s043", "second")
        self.play(GrowArrow(a2), FadeIn(l2), run_time=0.6)
        self.word("s043", "first")
        self.play(GrowArrow(a1), FadeIn(l1), run_time=0.6)
        # ── s044 applied to false negative ──
        self.at("s044", 0.0)
        w2n = TB("NEGATIVE", 36, BLUE_).move_to(w2, aligned_edge=LEFT)
        l2n = T("it said no", 26, BLUE_, weight=BOLD).move_to(l2)
        l1n = VGroup(T("…and that", 26, RED_, weight=BOLD), T("was wrong", 26, RED_, weight=BOLD)).arrange(DOWN, buff=0.1)
        l1n.next_to(a1, DOWN, buff=0.12)
        a2n = a2.copy().set_color(BLUE_)
        self.play(ReplacementTransform(w2, w2n), ReplacementTransform(l2, l2n), ReplacementTransform(a2, a2n), run_time=0.6)
        self.word("s044", "false", nth=1)
        self.play(ReplacementTransform(l1, l1n), run_time=0.5)
        ans = pill("it was really fraud", ORANGE_, 26).next_to(VGroup(l1n, l2n), DOWN, buff=0.45)
        self.word("s044", "yes")
        self.play(FadeIn(ans, shift=UP * 0.15), highlight(g.cell["FN"], color=BLUE_), run_time=0.8)

        # ── s045 warm-up: ten payments, three fraud ──
        self.at("s045", 0.0)
        self.play(FadeOut(VGroup(w1, w2n, a1, a2n, l1n, l2n, ans)), run_time=0.4)
        wu = pill("warm-up: 10 payments", INK2, 26).move_to(RIGHT * PANEL_X + UP * 2.25)
        cards = VGroup()
        for n in range(1, 11):
            c = payment_card(INK2, 0.62, fraud=(n in (1, 4, 7)))
            lab = T(str(n), 20, MUTED).next_to(c, DOWN, buff=0.1)
            cards.add(VGroup(c, lab))
        cards.arrange_in_grid(2, 5, buff=(0.2, 0.3)).move_to(RIGHT * PANEL_X + UP * 0.55)
        self.play(FadeIn(wu), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards], lag_ratio=0.06), run_time=1.0)
        fr = T("3 are fraud", 26, RED_, weight=BOLD).next_to(cards, DOWN, buff=0.3)
        self.word("s045", "Three")
        self.play(FadeIn(fr), run_time=0.4)
        counts = {k: 0 for k in KEYS}

        def send(n, rt=0.7):
            k = WARM[n]
            c = cards[n - 1]
            self.qa_mute(c)
            counts[k] += 1
            self.play(c.animate.scale(0.8).move_to(g.cell[k].get_center() + DOWN * 0.1), run_time=rt,
                      rate_func=rate_functions.ease_in_out_sine)
            self.play(FadeOut(c), g.set_num(k, counts[k]), run_time=0.35)

        for sid, n, w in (("s046", 1, "alarm"), ("s047", 2, "stays"), ("s048", 3, "panics"), ("s049", 4, "slips")):
            self.at(sid, 0.0)
            self.word(sid, w)
            send(n)
        # ── s050 the rest ──
        self.at("s050", 0.0)
        self.play(FadeOut(fr), run_time=0.3)
        for n in range(5, 11):
            send(n, rt=0.45)
        # ── s051 totals ──
        self.at("s051", 0.0)
        tot = VGroup(seq(("2", AQUA), ("+", INK2), ("1", BLUE_), ("+", INK2), ("2", ORANGE_), ("+", INK2), ("5", AQUA),
                         ("=", INK2), ("10", INK), size=40), check(AQUA, 0.3)).arrange(RIGHT, buff=0.3)
        tot.move_to(RIGHT * PANEL_X + UP * 0.4)
        for k in KEYS:
            self.word("s051", {"TP": "true", "FN": "false", "FP": "false", "TN": "true"}[k],
                      nth={"TP": 0, "FN": 0, "FP": 1, "TN": 1}[k])
            self.play(highlight(g.num[k], color=COL[k]), run_time=0.8)
        self.word("s051", "plus")
        self.play(FadeIn(tot[0]), run_time=0.6)
        self.word("s051", "ten")
        self.play(Create(tot[1]), run_time=0.4)
        home = T("every payment: one box", 24, INK2).next_to(tot, DOWN, buff=0.35)
        self.word("s051", "Every")
        self.play(FadeIn(home), run_time=0.4)

        # ── s052 diagonals: right vs wrong ──
        self.at("s052", 0.0)
        self.play(FadeOut(VGroup(tot, home, wu)), run_time=0.4)
        good = pill("✓  correct: TP, TN", AQUA, 28).move_to(RIGHT * PANEL_X + UP * 0.6)
        bad = pill("✗  mistakes: FP, FN", RED_, 28).move_to(RIGHT * PANEL_X + DOWN * 0.6)
        self.word("s052", "correct")
        self.play(highlight(g.cell["TP"], g.cell["TN"], color=AQUA), FadeIn(good), run_time=0.9)
        self.word("s052", "mistake")
        self.play(highlight(g.cell["FP"], g.cell["FN"], color=RED_), FadeIn(bad), run_time=0.9)
        # hand over a clean grid (names, no counts) to the next scene
        self.until(SEGS["s052"]["end"] - 0.2)
        self.play(FadeOut(VGroup(good, bad)), *[FadeOut(g.num[k]) for k in KEYS],
                  *[g.unlight(k) for k in KEYS], run_time=0.5)
        self.finish()
