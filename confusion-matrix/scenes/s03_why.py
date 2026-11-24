import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cm import *


def icon_card(label, icon, color, w=2.9, h=2.4):
    box = card(w, h, color)
    icon.move_to(box.get_center() + UP * 0.35)
    t = T(label, 26, INK, weight=BOLD).move_to(box.get_center() + DOWN * 0.55)
    rare = T("rare", 22, color).move_to(box.get_center() + DOWN * 0.92)
    g = VGroup(box, icon, t, rare); g.box = box
    return g


def gear(color, r=0.42):
    teeth = VGroup(*[Rectangle(width=0.16, height=0.2).set_stroke(width=0).set_fill(color, 1)
                     .move_to(np.array([np.cos(a), np.sin(a), 0]) * r).rotate(a) for a in np.linspace(0, 2 * PI, 8, endpoint=False)])
    ring_ = Circle(r * 0.8).set_stroke(color, 6)
    g = VGroup(teeth, ring_, Circle(r * 0.25).set_stroke(color, 4))
    for x in g.get_family(): x.qa_ignore = True
    return g


def heart(color):
    h = VMobject().set_points_smoothly([np.array(p) * 0.42 for p in [(0, -0.9, 0), (-0.9, 0.05, 0), (-0.55, 0.7, 0), (0, 0.35, 0),
                                                                    (0.55, 0.7, 0), (0.9, 0.05, 0), (0, -0.9, 0)]]).set_stroke(color, 5)
    h.qa_ignore = True
    return h


def laptop(color):
    sc = RoundedRectangle(corner_radius=0.05, width=0.9, height=0.58).set_stroke(color, 5)
    base = Line(LEFT * 0.62, RIGHT * 0.62).set_stroke(color, 6).next_to(sc, DOWN, buff=0.06)
    g = VGroup(sc, base)
    for x in g.get_family(): x.qa_ignore = True
    return g


class S03Why(Base):
    CHAPTER = "Why Accuracy Isn't Enough"

    def construct(self):
        # ── s017 the lazy detector ──
        self.at("s017", 0.0)
        Z = detector_box("Detector Zero", MUTED, w=3.8).move_to(UP * 1.6)
        self.play(FadeIn(Z, shift=DOWN * 0.2), run_time=0.6)

        # ── s018 says NOT FRAUD to everything ──
        self.at("s018", 0.0)
        cards = VGroup(*[payment_card(INK2, 0.8, fraud=(k == 5)) for k in range(8)]).arrange(RIGHT, buff=0.35).move_to(DOWN * 0.1)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.08), run_time=0.8)
        self.word("s018", "not")
        st = pill("every payment  →  NOT FRAUD", MUTED, 32).move_to(DOWN * 1.4)
        self.play(FadeIn(st, shift=UP * 0.15), run_time=0.5)

        # ── s019 / s020 a bar of 10,000 payments ──
        self.at("s019", 0.0)
        self.play(FadeOut(VGroup(cards, st)), Z.animate.scale(0.8).move_to(UP * 2.25 + RIGHT * 4.6), run_time=0.6)
        nl = NumberLine(x_range=[0, 10000, 2000], length=11, color=INK2, include_tip=False, stroke_width=3, tick_size=0.08)
        nl.move_to(DOWN * 0.9)
        nums = VGroup(*[T(fmt(v), 22, INK2).next_to(nl.n2p(v), DOWN, buff=0.15) for v in range(0, 10001, 2000)])
        nt = T("payments", 24, MUTED).next_to(nums, DOWN, buff=0.15).align_to(nl, RIGHT)
        self.play(Create(nl), FadeIn(nums), FadeIn(nt), run_time=0.7)
        fine = Rectangle(width=nl.n2p(9900)[0] - nl.n2p(0)[0], height=0.7).set_stroke(width=0).set_fill(INK2, 0.55)
        fine.move_to(nl.n2p(0), aligned_edge=LEFT).shift(UP * 0.45)
        self.word("s019", "nine")
        self.play(GrowFromEdge(fine, LEFT), run_time=1.0, rate_func=rate_functions.ease_out_cubic)
        fl = T("9,900 fine", 30, INK, weight=BOLD).next_to(fine, UP, buff=0.25).align_to(fine, LEFT)
        ck = check(AQUA, 0.3).next_to(fl, RIGHT, buff=0.25)
        self.play(FadeIn(fl), run_time=0.4)
        self.word("s019", "right")
        self.play(Create(ck), run_time=0.4)
        self.at("s020", 0.0)
        fr = Rectangle(width=nl.n2p(10000)[0] - nl.n2p(9900)[0], height=0.7).set_stroke(width=0).set_fill(RED_, 1)
        fr.next_to(fine, RIGHT, buff=0)
        frl = T("100 fraud", 30, RED_, weight=BOLD).next_to(fr, UP, buff=0.25).align_to(fr, RIGHT)
        self.play(FadeIn(fr), FadeIn(frl), run_time=0.5)
        self.word("s020", "wrong")
        cr = cross(RED_, 0.16).next_to(frl, LEFT, buff=0.25)
        self.play(Create(cr), run_time=0.4)

        # ── s021 99% accuracy ──
        self.at("s021", 0.0)
        acc = VGroup(nfrac("9,900", "10,000", WARN, 56), T("=", 44, INK2), TB("99%", 64, WARN),
                     T("accurate", 34, WARN, weight=BOLD)).arrange(RIGHT, buff=0.3).move_to(UP * 2.0 + LEFT * 1.2)
        self.word("s021", "Nine")
        self.play(FadeIn(acc[0]), run_time=0.6)
        self.word("s021", "ninety-nine")
        self.play(FadeIn(acc[1:], shift=LEFT * 0.2), run_time=0.6)

        # ── s022 zero caught ──
        self.at("s022", 0.0)
        zero = TB("0 fraud caught", 40, RED_).next_to(nl, DOWN, buff=0.95)
        self.play(FadeIn(zero, shift=UP * 0.15), run_time=0.5)
        self.word("s022", "Not")
        self.play(highlight(zero, color=RED_), run_time=0.8)

        # ── s023 can't tell useless from good ──
        self.at("s023", 0.0)
        self.play(FadeOut(VGroup(nl, nums, nt, fine, fl, ck, fr, frl, cr, acc, zero, Z)), run_time=0.5)
        g1 = gauge(99, WARN, "Detector Zero (useless)")
        g2 = gauge(99, WARN, "a good detector?")
        G = VGroup(g1, g2).arrange(RIGHT, buff=2.2).move_to(UP * 0.4)
        self.play(FadeIn(g1[0]), FadeIn(g2[0]), FadeIn(g1[3]), FadeIn(g2[3]), run_time=0.5)
        self.play(Create(g1[1]), Create(g2[1]), FadeIn(g1[2]), FadeIn(g2[2]), run_time=1.0)
        q = T("same number", 30, INK2).next_to(G, DOWN, buff=0.5)
        self.word("s023", "useless")
        self.play(FadeIn(q), run_time=0.4)

        # ── s024 rare things ──
        self.at("s024", 0.0)
        self.play(FadeOut(VGroup(G, q)), run_time=0.4)
        ax = NumberLine(x_range=[0, 10, 1], length=10, include_tip=False, include_ticks=False, color=INK2, stroke_width=3).move_to(UP * 0.4)
        lc = T("common", 26, INK2).next_to(ax.n2p(0), DOWN, buff=0.25)
        lr = T("rare", 26, RED_, weight=BOLD).next_to(ax.n2p(10), DOWN, buff=0.25)
        at = T("how rare is the thing you look for?", 26, MUTED).next_to(ax, UP, buff=1.0).shift(LEFT * 2.0)
        zone = Rectangle(width=3.0, height=0.5).set_stroke(width=0).set_fill(RED_, 0.35).move_to(ax.n2p(8.5))
        zone.qa_ignore = True
        zl = T("accuracy misleads here", 24, RED_).next_to(zone, UP, buff=0.25)
        self.play(Create(ax), FadeIn(lc), FadeIn(lr), FadeIn(at), run_time=0.7)
        self.word("s024", "rare")
        self.play(FadeIn(zone), FadeIn(zl), run_time=0.6)

        # ── s025 four rare things ──
        self.at("s025", 0.0)
        self.play(FadeOut(VGroup(ax, lc, lr, at, zone, zl)), run_time=0.4)
        items = [("fraud", payment_card(ORANGE_, 1.0), ORANGE_), ("disease", heart(RED_), RED_),
                 ("faulty parts", gear(WARN), WARN), ("hackers", laptop(BLUE_), BLUE_)]
        C = VGroup(*[icon_card(l, i, c) for l, i, c in items]).arrange(RIGHT, buff=0.35).move_to(UP * 0.2)
        for k, w in enumerate(["Fraud", "diseases", "Faulty", "Hackers"]):
            self.word("s025", w)
            self.play(FadeIn(C[k], shift=UP * 0.2), run_time=0.5)

        # ── s026 costly mistakes ──
        self.at("s026", 0.0)
        cost = T("where mistakes cost the most", 30, RED_, weight=BOLD).next_to(C, DOWN, buff=0.45)
        self.word("s026", "wrong")
        self.play(*[c.box.animate.set_stroke(RED_, 4) for c in C], FadeIn(cost), run_time=0.7)

        # ── s027 the Bayes callback ──
        self.at("s027", 0.0)
        self.play(FadeOut(VGroup(C, cost)), run_time=0.4)
        cue = card_cue("Bayes' Theorem", mini_bayes(), VIOLET)
        self.play(FadeIn(cue, shift=LEFT * 0.2), run_time=0.5)
        axg = xy_axes([0, 2, 1], [0, 100, 25], 5.2, 3.6, None, "people who tested positive", x_labels={}, font_size=22)
        axg.move_to(LEFT * 1.6 + DOWN * 0.1)
        b1 = vbar(axg.ax, 0.5, 9, AQUA, 0.9); b2 = vbar(axg.ax, 1.5, 99, ORANGE_, 0.9)
        l1 = T("9 sick", 24, AQUA, weight=BOLD).next_to(axg.ax.c2p(0.5, 0), DOWN, buff=0.2)
        l2 = T("99 false alarms", 24, ORANGE_, weight=BOLD).next_to(axg.ax.c2p(1.5, 0), DOWN, buff=0.2)
        self.play(FadeIn(axg), run_time=0.5)
        self.word("s027", "positive")
        self.play(GrowFromEdge(b1, DOWN), GrowFromEdge(b2, DOWN), FadeIn(l1), FadeIn(l2), run_time=0.9)
        res = VGroup(TB("1 in 12", 60, VIOLET), T("chance of being sick", 26, INK2)).arrange(DOWN, buff=0.15)
        res.move_to(RIGHT * 4.0 + DOWN * 0.3)
        self.word("s027", "twelve")
        self.play(FadeIn(res, shift=LEFT * 0.2), run_time=0.5)

        # ── s028 one place for all the numbers ──
        self.at("s028", 0.0)
        g = grid_at(0.75, center=np.array([0.0, -0.2, 0]), names=False, rows=("", ""), cols=("", ""), row_title="", col_title="")
        self.play(FadeOut(VGroup(axg, b1, b2, l1, l2, res, cue)), run_time=0.5)
        self.word("s028", "tool")
        self.play(LaggedStart(*[Create(g.cell[k]) for k in KEYS], lag_ratio=0.15), run_time=1.0)
        nh = T("nothing hidden", 30, INK2).next_to(g.cells, DOWN, buff=0.35)
        self.word("s028", "nothing")
        self.play(FadeIn(nh), run_time=0.5)
        self.finish()
