import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cm import *


def model_card(p, r):
    box = card(1.05, 1.5, GRID)
    ax = Line(LEFT * 0.35, RIGHT * 0.35).set_stroke(INK2, 2)
    b1 = Rectangle(width=0.22, height=max(0.02, 0.9 * p)).set_stroke(width=0).set_fill(VIOLET, 0.9)
    b2 = Rectangle(width=0.22, height=max(0.02, 0.9 * r)).set_stroke(width=0).set_fill(ORANGE_, 0.9)
    b1.move_to(ax.get_center() + LEFT * 0.15, aligned_edge=DOWN)
    b2.move_to(ax.get_center() + RIGHT * 0.15, aligned_edge=DOWN)
    inner = VGroup(ax, b1, b2).move_to(box)
    for x in inner.get_family():
        x.qa_ignore = True
    return VGroup(box, inner)


class S10F1(Base):
    CHAPTER = "The F1 Score"

    def construct(self):
        # ── s122 ten models, one number? ──
        self.at("s122", 0.0)
        rng = np.random.default_rng(2)
        cards = VGroup(*[model_card(rng.uniform(0.3, 0.95), rng.uniform(0.3, 0.95)) for _ in range(10)]).arrange(RIGHT, buff=0.18)
        cards.move_to(UP * 0.9)
        self.word("s122", "number.")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.06), run_time=0.9)
        q = T("rank them with one number?", 30, INK2).next_to(cards, DOWN, buff=0.45)
        self.word("s122", "rank")
        self.play(FadeIn(q), run_time=0.4)
        # ── s123 the F1 score ──
        self.at("s123", 0.0)
        self.play(FadeOut(VGroup(cards, q)), run_time=0.4)
        ttl = VGroup(TB("F1 SCORE", 64, VIOLET), T("one number, two questions", 30, INK2)).arrange(DOWN, buff=0.25).move_to(UP * 1.6)
        self.word("s123", "F")
        self.play(FadeIn(ttl, shift=DOWN * 0.15), run_time=0.6)
        bl = VGroup(T("precision", 30, VIOLET, weight=BOLD), T("+", 30, INK2), T("recall", 30, ORANGE_, weight=BOLD),
                    T("→", 30, INK2), T("one number", 30, INK, weight=BOLD)).arrange(RIGHT, buff=0.25).move_to(DOWN * 0.1)
        self.word("s123", "blends")
        self.play(FadeIn(bl), run_time=0.5)
        # ── s124 just average? ──
        self.at("s124", 0.0)
        self.play(FadeOut(bl), ttl.animate.scale(0.7).move_to(UP * 2.35), run_time=0.5)
        av = VGroup(T("plain average:", 30, INK2), seq(("(75 + 90) ÷ 2", INK), ("=", INK2), ("82.5", INK), size=36)
                    ).arrange(RIGHT, buff=0.3).move_to(UP * 1.45)
        self.word("s124", "seventy-five")
        self.play(FadeIn(av), run_time=0.6)
        # ── s125 the flag-everything detector fools it ──
        self.at("s125", 0.0)
        self.word("s125", "flags")
        ax = xy_axes([0, 2, 1], [0, 100, 50], 4.2, 2.5, None, "percent", x_labels={}, font_size=20).move_to(LEFT * 2.8 + DOWN * 0.5)
        b1 = vbar(ax.ax, 0.5, 1, VIOLET, 0.8); b2 = vbar(ax.ax, 1.5, 100, ORANGE_, 0.8)
        l1 = T("precision 1", 22, VIOLET, weight=BOLD).next_to(ax.ax.c2p(0.5, 0), DOWN, buff=0.18)
        l2 = T("recall 100", 22, ORANGE_, weight=BOLD).next_to(ax.ax.c2p(1.5, 0), DOWN, buff=0.18)
        fe = pill("flags everything", RED_, 24).next_to(ax, RIGHT, buff=0.6).shift(UP * 0.6)
        self.play(FadeIn(ax), FadeIn(fe), run_time=0.5)
        self.word("s125", "Recall")
        self.play(GrowFromEdge(b2, DOWN), FadeIn(l2), run_time=0.6)
        self.word("s125", "precision")
        self.play(GrowFromEdge(b1, DOWN), FadeIn(l1), run_time=0.5)
        avl = DashedLine(ax.ax.c2p(0, 50.5), ax.ax.c2p(2, 50.5), color=INK2, stroke_width=3)
        avl.qa_ignore = True
        avt = VGroup(T("plain average 50.5", 24, INK, weight=BOLD), T("too kind", 24, RED_, weight=BOLD)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        avt.next_to(fe, DOWN, buff=0.4).align_to(fe, LEFT)
        self.word("s125", "fifty")
        self.play(Create(avl), FadeIn(avt[0]), run_time=0.6)
        self.word("s125", "useless")
        self.play(FadeIn(avt[1]), run_time=0.4)
        # ── s126 the harmonic mean is dragged down ──
        self.at("s126", 0.0)
        hl = Line(ax.ax.c2p(0, 2), ax.ax.c2p(2, 2)).set_stroke(VIOLET, 5)
        hl.qa_ignore = True
        ht = T("F1 (harmonic mean): about 2", 24, VIOLET, weight=BOLD).next_to(avt, DOWN, buff=0.35).align_to(fe, LEFT)
        self.word("s126", "harmonic")
        self.play(ReplacementTransform(avl.copy(), hl), FadeIn(ht), run_time=1.0)
        dn = T("dragged down by the worse number", 22, INK2).next_to(ht, DOWN, buff=0.15).align_to(fe, LEFT)
        self.word("s126", "dragged")
        self.play(FadeIn(dn), run_time=0.4)

        # ── s127 the friendly formula ──
        self.at("s127", 0.0)
        self.play(FadeOut(VGroup(ax, b1, b2, l1, l2, fe, avl, avt, hl, ht, dn, av, ttl)), run_time=0.5)
        f = ratio("F1", "2 TP", "2 TP + FP + FN", VIOLET, AQUA, INK, 56).move_to(UP * 0.5)
        self.play(FadeIn(f), run_time=0.6)
        # ── s128 in words ──
        self.at("s128", 0.0)
        w1 = T("true positives, counted twice", 26, AQUA).next_to(f, UP, buff=0.3).shift(RIGHT * 0.6)
        w2 = T("…compared with both kinds of mistake", 26, RED_).next_to(f, DOWN, buff=0.3).shift(RIGHT * 0.6)
        self.word("s128", "twice,")
        self.play(FadeIn(w1), run_time=0.4)
        self.word("s128", "mistakes.")
        self.play(FadeIn(w2), run_time=0.4)
        # ── s129 / s130 Detector A ──
        self.at("s129", 0.0)
        self.play(FadeOut(VGroup(w1, w2)), f.animate.scale(0.8).move_to(UP * 1.6), run_time=0.5)
        ea = seq(("A:", AQUA), ("2 × 90 = 180", INK), size=34).move_to(UP * 0.2)
        self.word("s129", "two")
        self.play(FadeIn(ea), run_time=0.5)
        eb = seq(("180 + 30 + 10 = 220", INK), size=34).next_to(ea, DOWN, buff=0.3)
        self.word("s129", "Plus")
        self.play(FadeIn(eb), run_time=0.5)
        self.at("s130", 0.0)
        r = VGroup(nfrac("180", "220", INK, 52), T("=", 36, INK2), nfrac("9", "11", INK, 52), T("≈", 36, INK2), TB("82%", 54, VIOLET)
                   ).arrange(RIGHT, buff=0.25).next_to(eb, DOWN, buff=0.4)
        self.play(FadeIn(r[:3]), run_time=0.6)
        self.word("s130", "About")
        self.play(FadeIn(r[3:]), run_time=0.5)
        # ── s131 Detector B ──
        self.at("s131", 0.0)
        self.play(FadeOut(VGroup(ea, eb, r)), run_time=0.4)
        b_ = seq(("B:", VIOLET), ("2 × 45 = 90", INK), ("·", INK2), ("90 + 5 + 55 = 150", INK), size=32).move_to(UP * 0.2)
        self.play(FadeIn(b_), run_time=0.6)
        rb = VGroup(nfrac("90", "150", INK, 52), T("=", 36, INK2), TB("60%", 54, VIOLET)).arrange(RIGHT, buff=0.25).next_to(b_, DOWN, buff=0.45)
        self.word("s131", "Sixty")
        self.play(FadeIn(rb), run_time=0.5)
        # ── s132 flag everything ──
        self.at("s132", 0.0)
        e_ = seq(("flag everything:", RED_), ("200 ÷ 10,100", INK), ("≈", INK2), ("2%", RED_), size=32).next_to(rb, DOWN, buff=0.45)
        self.word("s132", "two")
        self.play(FadeIn(e_), run_time=0.5)
        nf = T("not fooled", 26, VIOLET, weight=BOLD).next_to(e_, RIGHT, buff=0.3)
        self.word("s132", "fooled.")
        self.play(FadeIn(nf), run_time=0.4)
        # ── s133 A wins, but… ──
        self.at("s133", 0.0)
        self.play(FadeOut(VGroup(b_, rb, e_, nf)), run_time=0.4)
        rk = VGroup(seq(("A", AQUA), ("82%", VIOLET), size=40), seq(("B", VIOLET), ("60%", VIOLET), size=40)).arrange(DOWN, buff=0.25)
        rk.move_to(LEFT * 3.2 + DOWN * 0.3)
        win = pill("A wins on F1", AQUA, 26).next_to(rk, DOWN, buff=0.35)
        self.word("s133", "wins.")
        self.play(FadeIn(rk), FadeIn(win), run_time=0.6)
        cau = side_card(["F1 treats a miss and a", "false alarm as equally bad.", "In real life, they rarely are."], WARN, 26,
                        title="CAREFUL", title_color=WARN).move_to(RIGHT * 2.6 + DOWN * 0.3)
        self.word("s133", "careful.")
        self.play(FadeIn(cau, shift=LEFT * 0.2), run_time=0.6)
        self.until(SEGS["s133"]["end"] + 0.1)
        self.play(FadeOut(VGroup(rk, win, cau, f)), run_time=0.5)
        self.finish()
