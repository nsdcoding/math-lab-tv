import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

DOMAINS = [("Machine Learning", VIOLET), ("Data Science", AQUA), ("Finance", ORANGE_), ("Computer Science", BLUE_)]


def small_tile(text, color, active=False):
    t = T(text, 20, color if active else MUTED, weight=BOLD)
    b = RoundedRectangle(corner_radius=0.12, width=t.width + 0.5, height=0.55,
                         stroke_color=color if active else GRID, stroke_width=2.5, fill_color="#22221f", fill_opacity=1)
    b.qa_container = True
    t.move_to(b)
    return VGroup(b, t)


def strip(active):
    g = VGroup(*[small_tile(n, c, i == active) for i, (n, c) in enumerate(DOMAINS)]).arrange(RIGHT, buff=0.25)
    return g.move_to(UP * 2.45 + RIGHT * 0.6)


def card_icon(color=ORANGE_):
    b = RoundedRectangle(corner_radius=0.08, width=0.9, height=0.56).set_stroke(color, 3).set_fill("#22221f", 1)
    s = Rectangle(width=0.9, height=0.1).set_stroke(width=0).set_fill(color, 0.9).move_to(b.get_top() + DOWN * 0.15)
    return VGroup(b, s)


def database(color=BLUE_):
    top = Ellipse(width=1.6, height=0.45).set_stroke(color, 4)
    side = VGroup(Line(LEFT * 0.8, LEFT * 0.8 + DOWN * 1.4), Line(RIGHT * 0.8, RIGHT * 0.8 + DOWN * 1.4)).set_stroke(color, 4)
    bot = Arc(radius=0.8, start_angle=PI, angle=PI).stretch(0.28, 1).set_stroke(color, 4).move_to(DOWN * 1.4 + DOWN * 0.11)
    mid = Arc(radius=0.8, start_angle=PI, angle=PI).stretch(0.28, 1).set_stroke(color, 2).move_to(DOWN * 0.7 + DOWN * 0.11)
    return VGroup(top, side, mid, bot)


class S11Uses(Base):
    CHAPTER = "Where You'll Use It"

    def construct(self):
        # ── s088 four fields ──
        self.at("s088", 0.0)
        tiles = VGroup(*[domain_tile(n.replace(" ", "\n"), c, 2.9, 1.6, 32) for n, c in DOMAINS]).arrange(RIGHT, buff=0.3)
        tiles.move_to(UP * 0.3)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.3) for t in tiles], lag_ratio=0.15), run_time=1.0)
        self.word("s088", "everywhere")
        self.play(LaggedStart(*[pulse(t, s=1.08) for t in tiles], lag_ratio=0.15), run_time=1.0)

        # ── s089 ML: face matching at a stadium ──
        self.at("s089", 0.0)
        self.idle()
        st = strip(0)
        self.play(ReplacementTransform(tiles, st), run_time=0.7)
        rng = np.random.default_rng(3)
        crowd = VGroup(*[dot(BLUE_, 0.09) for _ in range(22 * 11)]).arrange_in_grid(11, 22, buff=0.15)
        crowd.move_to(LEFT * 2.9 + DOWN * 0.3)
        wanted = 128
        crowd[wanted].set_color(ORANGE_)
        cap = T("50,000 fans (illustration)", 24, INK2).next_to(crowd, DOWN, buff=0.2)
        self.word("s089", "stadium")
        self.play(FadeIn(crowd, lag_ratio=0.003), FadeIn(cap), run_time=0.9)
        self.word("s089", "wanted")
        self.play(highlight(crowd[wanted], color=ORANGE_), ripple(crowd[wanted].get_center(), ORANGE_, r=0.2, scale=4), run_time=0.6)
        px = crowd.get_right()[0] + 0.5
        fm = pill("false match: 1 in 10,000", WARN, 26)
        fm.move_to(UP * 1.25).set_x(px + fm.width / 2)
        self.play(FadeIn(fm, shift=LEFT * 0.2), run_time=0.5)

        # ── s090 about five false matches plus the real one ──
        self.at("s090", 0.0)
        false_idx = [17, 64, 141, 199, 230]
        self.word("s090", "fifty")
        scan = Line(crowd.get_corner(UL), crowd.get_corner(DL)).set_stroke(WARN, 4); scan.qa_ignore = True
        self.play(Create(scan), run_time=0.2)
        self.play(scan.animate.move_to(crowd.get_right()), run_time=1.4, rate_func=linear)
        rings = VGroup(*[Circle(0.16).set_stroke(WARN, 3).move_to(crowd[i]) for i in false_idx + [wanted]])
        for r in rings:
            r.qa_ignore = True
        self.word("s090", "five")
        self.play(FadeOut(scan), LaggedStart(*[Create(r) for r in rings], lag_ratio=0.12), run_time=0.9)
        al = VGroup(T("alerts", 26, WARN, weight=BOLD), T("≈ 5 false + 1 real = 6", 30, INK, weight=BOLD)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        al.next_to(fm, DOWN, buff=0.4).align_to(fm, LEFT)
        self.play(FadeIn(al, shift=LEFT * 0.2), run_time=0.5)

        # ── s091 right person only 1 time in 6 ──
        self.at("s091", 0.0)
        r6 = result_card("P(right person | alert)", "≈ 1 in 6", VIOLET, 24, 44)
        r6.next_to(al, DOWN, buff=0.4).align_to(fm, LEFT)
        self.word("s091", "alarm")
        self.play(FadeIn(r6, scale=0.8), run_time=0.6)
        self.idle(lambda: pulse(rings[-1], s=1.3))

        # ── s092 DS: the p value ──
        self.at("s092", 0.0)
        self.idle()
        st2 = strip(1)
        self.play(FadeOut(VGroup(crowd, cap, fm, rings, al, r6)), ReplacementTransform(st, st2), run_time=0.6)
        frm = chip("from: Hypothesis Testing", AQUA, 22)
        pm = [comb(20, k) / 2 ** 20 * 100 for k in range(21)]
        g = xy_axes([0, 20, 5], [0, 20, 10], 6.0, 2.4, "heads in 20 flips", "chance (%)", y_vertical=True)
        g.move_to(LEFT * 2.9 + DOWN * 0.55)
        frm.next_to(g, UP, buff=0.3).align_to(g, LEFT)
        ax = g[0]
        bars = VGroup(*[Rectangle(width=0.22, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.001)).set_stroke(width=0)
                        .set_fill(AQUA if k >= 15 else BLUE_, 0.9).move_to(ax.c2p(k, 0), aligned_edge=DOWN) for k, v in enumerate(pm)])
        self.word("s092", "coin")
        self.play(FadeIn(frm), FadeIn(g), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), run_time=0.9)
        pv = cond_box("this extreme", "fair", value="p ≈ 0.021", color=AQUA, size=24)
        pv.move_to(UP * 1.25).set_x(1.4 + pv.width / 2)
        self.word("s092", "chance")
        self.play(FadeIn(pv, shift=LEFT * 0.2), run_time=0.6)
        self.play(pulse(VGroup(*bars[15:]), s=1.15), run_time=0.6)

        # ── s093 not the chance nothing is going on: ≈ 83 in 100 fair ──
        self.at("s093", 0.0)
        pf = cond_box("fair", "this extreme", value="≈ 83 in 100", color=VIOLET, size=24, vcol=VIOLET,
                      caption=None)
        pf.next_to(pv, DOWN, buff=0.35).align_to(pv, LEFT)
        pfc = T("if 1 coin in 100 is rigged (illustration)", 22, INK2).next_to(pf, DOWN, buff=0.2).align_to(pf, LEFT)
        ne = TB("≠", 44, RED_).move_to([pv.get_left()[0] - 0.35, (pv.get_bottom()[1] + pf.get_top()[1]) / 2, 0])
        self.word("s093", "not")
        self.play(FadeIn(ne, scale=0.5), run_time=0.4)
        self.word("s093", "rigged")
        self.play(FadeIn(pf, shift=UP * 0.2), FadeIn(pfc), run_time=0.6)
        self.word("s093", "eighty")
        self.play(pulse(pf.value, s=1.15), run_time=0.6)

        # ── s094 Finance: fraud flags ──
        self.at("s094", 0.0)
        self.idle()
        st3 = strip(2)
        self.play(FadeOut(VGroup(frm, g, bars, pv, pf, pfc, ne)), ReplacementTransform(st2, st3), run_time=0.6)
        cards = VGroup(*[card_icon(INK2) for _ in range(7)]).arrange(RIGHT, buff=0.35).move_to(UP * 1.0)
        self.word("s094", "flags")
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.6) for c in cards], lag_ratio=0.1), run_time=0.9)
        self.play(cards[3][0].animate.set_stroke(WARN, 4), cards[3][1].animate.set_fill(WARN, 1), run_time=0.4)
        ff = pill("false flag: 1 honest payment in 1,000", WARN, 28).next_to(cards, DOWN, buff=0.45)
        self.word("s094", "wrongly")
        self.play(FadeIn(ff, shift=UP * 0.2), run_time=0.5)

        # ── s095 per million honest payments: 100 frauds, 90 caught, 1,000 false flags ──
        self.at("s095", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(cards, ff)), run_time=0.4)
        g2 = xy_axes([0, 2, 1], [0, 1000, 250], 4.4, 3.4, None, "payments flagged", x_labels={}, y_vertical=True)
        g2.move_to(LEFT * 2.4 + DOWN * 0.25)
        a2 = g2[0]
        def vbar(x, v, col):
            return Rectangle(width=1.1, height=max(a2.c2p(0, v)[1] - a2.c2p(0, 0)[1], 0.001)).set_stroke(width=0).set_fill(col, 0.95)\
                .move_to(a2.c2p(x, 0), aligned_edge=DOWN)
        bf = vbar(0.55, 90, ORANGE_); bh = vbar(1.45, 1000, BLUE_)
        lf = T("real fraud\ncaught: 90", 22, ORANGE_, weight=BOLD).next_to(a2.c2p(0.55, 0), DOWN, buff=0.15)
        lh = T("honest but\nflagged: 1,000", 22, BLUE_, weight=BOLD).next_to(a2.c2p(1.45, 0), DOWN, buff=0.15)
        self.play(FadeIn(g2), run_time=0.4)
        self.word("s095", "catches")
        self.play(GrowFromEdge(bf, DOWN), FadeIn(lf), run_time=0.6)
        self.word("s095", "thousand")
        self.play(GrowFromEdge(bh, DOWN), FadeIn(lh), run_time=0.9)

        # ── s096 only about 1 flag in 12 is fraud ──
        self.at("s096", 0.0)
        rf = result_card("P(fraud | flagged)", "90 ÷ 1,090 ≈ 1 in 12", VIOLET, 26, 40)
        rf.move_to(UP * 0.4).set_x(1.3 + rf.width / 2)
        self.word("s096", "twelve")
        self.play(FadeIn(rf, shift=LEFT * 0.2), run_time=0.6)
        bl = pill("the rest: blocked customers", BLUE_, 26).next_to(rf, DOWN, buff=0.4).align_to(rf, LEFT)
        self.word("s096", "customers")
        self.play(FadeIn(bl, shift=UP * 0.2), run_time=0.5)

        # ── s097 CS: searching a huge database ──
        self.at("s097", 0.0)
        self.idle()
        st4 = strip(3)
        self.play(FadeOut(VGroup(g2, bf, bh, lf, lh, rf, bl)), ReplacementTransform(st3, st4), run_time=0.6)
        db = database(BLUE_).move_to(LEFT * 4.6 + DOWN * 0.1)
        dl = T("5,000,000 DNA profiles", 24, INK2, weight=BOLD).next_to(db, DOWN, buff=0.25)
        self.word("s097", "database")
        self.play(Create(db), FadeIn(dl), run_time=0.8)

        # ── s098 about five innocent hits ──
        self.at("s098", 0.0)
        rows = VGroup(*[RoundedRectangle(corner_radius=0.05, width=2.6, height=0.2).set_stroke(GRID, 1.5).set_fill("#22221f", 1)
                        for _ in range(12)]).arrange(DOWN, buff=0.07).move_to(LEFT * 0.8 + DOWN * 0.1)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.05), run_time=0.6)
        hl = Rectangle(width=2.8, height=0.28).set_stroke(WARN, 3).move_to(rows[0]); hl.qa_ignore = True
        self.word("s098", "Search")
        self.play(Create(hl), run_time=0.2)
        self.play(hl.animate.move_to(rows[-1]), run_time=1.4, rate_func=linear)
        hits = VGroup(*[rows[i] for i in (1, 4, 6, 9, 11)])
        self.word("s098", "five")
        self.play(FadeOut(hl), *[r.animate.set_stroke(WARN, 3).set_fill(BLUE_, 0.9) for r in hits], run_time=0.6)
        hp = pill("≈ 5 innocent hits", WARN, 28).move_to(UP * 0.9).set_x(1.1 + 1.6)
        np_ = pill("culprit not in the database", RED_, 26).next_to(hp, DOWN, buff=0.35).align_to(hp, LEFT)
        self.play(FadeIn(hp, shift=LEFT * 0.2), run_time=0.4)
        self.word("s098", "culprit")
        self.play(FadeIn(np_, shift=LEFT * 0.2), run_time=0.4)

        # ── s099 bigger search, more coincidences ──
        self.at("s099", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(rows, hp, np_)), run_time=0.4)
        g3 = xy_axes([0, 5, 1], [0, 5, 1], 5.6, 3.2, "profiles searched (millions)", "innocent hits", y_vertical=True)
        g3.move_to(RIGHT * 1.7 + DOWN * 0.35)
        a3 = g3[0]
        ln = a3.plot(lambda x: x, x_range=[0, 5], color=WARN, stroke_width=5)
        self.play(FadeIn(g3), run_time=0.4)
        self.word("s099", "bigger")
        self.play(Create(ln), run_time=1.2)
        dd = dot(WARN, 0.12).move_to(a3.c2p(5, 5))
        self.play(FadeIn(dd, scale=2), run_time=0.3)

        # ── s100 four fields, one trap ──
        self.at("s100", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(db, dl, g3, ln, dd, st4)), run_time=0.5)
        res = [("Machine Learning", VIOLET, "1 in 6 alerts right"), ("Data Science", AQUA, "83 in 100 fair"),
               ("Finance", ORANGE_, "1 in 12 flags fraud"), ("Computer Science", BLUE_, "≈ 5 innocent hits")]
        cols = VGroup()
        for n, c, r in res:
            t = TB(n.replace(" ", "\n"), 28, c)
            v = T(r, 24, INK, weight=BOLD)
            inner = VGroup(t, v).arrange(DOWN, buff=0.3)
            b = card(3.05, inner.height + 0.7, c); inner.move_to(b)
            cols.add(VGroup(b, inner))
        cols.arrange(RIGHT, buff=0.25).move_to(UP * 0.55)
        self.word("s100", "Four")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cols], lag_ratio=0.15), run_time=1.0)
        cap = pill("rare false match × big crowd = lots of false matches", RED_, 28).next_to(cols, DOWN, buff=0.45)
        self.word("s100", "rare")
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.5)
        self.idle(lambda: LaggedStart(*[pulse(c, s=1.05) for c in cols], lag_ratio=0.2))
        self.finish()
