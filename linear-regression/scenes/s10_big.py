import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

TW, TH = 6.5, 2.5


def tile(title, color):
    box = card(TW, TH, color=color)
    t = T(title, 26, color, weight=BOLD).move_to(box.get_corner(UL) + RIGHT * 0.3 + DOWN * 0.32, aligned_edge=LEFT)
    g = VGroup(box, t); g.box = box
    return g


def mini(x_lab, y_lab, pts, line, color, seed=0):
    ax = Axes(x_range=[0, 10, 2], y_range=[0, 10, 2], x_length=2.7, y_length=1.45,
              axis_config=dict(color=INK2, stroke_width=2.5, include_tip=False, tick_size=0.04))
    xl = T(x_lab, 18, MUTED).next_to(ax.x_axis, DOWN, buff=0.1).align_to(ax.x_axis, RIGHT)
    yl = T(y_lab, 18, MUTED).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.1)
    ds = VGroup(*[Dot(ax.c2p(x, y), radius=0.05, color=INK) for x, y in pts])
    a, b = line
    ln = Line(ax.c2p(0.3, a + b * 0.3), ax.c2p(9.7, min(9.8, a + b * 9.7)), color=color, stroke_width=3.5)
    g = VGroup(ax, xl, yl, ds, ln); g.ax = ax; g.ln = ln
    return g


def noisy(seed, a, b, s=0.7, n=10):
    rng = np.random.default_rng(seed)
    xs = np.linspace(1, 9, n)
    return [(x, float(np.clip(a + b * x + rng.normal(0, s), 0.3, 9.7))) for x in xs]


class S10Big(Base):
    CHAPTER = "Big Picture"

    def construct(self):
        # ── s097 four tiles ──
        self.at("s097", 0.0)
        tiles = VGroup(tile("MACHINE LEARNING", VIOLET), tile("DATA SCIENCE", AQUA),
                       tile("FINANCE", WARN), tile("COMPUTER SCIENCE", BLUE_))
        tiles.arrange_in_grid(2, 2, buff=(0.3, 0.3)).move_to(UP * 0.25)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.3) for t in tiles], lag_ratio=0.15), run_time=1.3)

        def place(t, m, lines):
            m.move_to(t.box.get_left() + RIGHT * 1.75 + DOWN * 0.22)
            tx = VGroup(*lines).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
            tx.move_to(t.box.get_center() + RIGHT * 1.45 + DOWN * 0.15)
            return tx

        # ── s098 ML: training data, model ──
        self.at("s098", 0.0)
        ml = tiles[0]
        hp = [(1 + 2 * i, (y - 100) / 30) for i, (x, y) in enumerate(HOUSES)]
        m1 = mini("size", "price", hp, (50 / 30 - 100 / 30 + 0.0, 0), VIOLET)
        # best line in mini coordinates: x_m = (x - 750)/250, y_m = (y - 100)/30  →  y = 50 + 0.1x
        a_m = (50 + 0.1 * 750 - 100) / 30; b_m = 0.1 * 250 / 30
        m1.ln.become(Line(m1.ax.c2p(0.3, a_m + b_m * 0.3), m1.ax.c2p(9.7, a_m + b_m * 9.7), color=VIOLET, stroke_width=3.5))
        t1 = place(ml, m1, [T("dots = training data", 22, INK), T("line = the model", 22, VIOLET, weight=BOLD)])
        self.play(ml.box.animate.set_stroke(width=4), FadeIn(m1[:4]), run_time=0.6)
        self.until(word_time("s098", word_index("s098", "training")))
        self.play(FadeIn(t1[0]), run_time=0.4)
        self.until(word_time("s098", word_index("s098", "line")))
        self.play(Create(m1.ln), FadeIn(t1[1]), run_time=0.6)

        # ── s099 loss and training ──
        self.at("s099", 0.0)
        t1b = VGroup(T("score = the loss", 20, WARN, weight=BOLD), T("training = smallest loss", 20, INK)).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        t1b.move_to(t1, aligned_edge=UL)
        self.play(FadeOut(t1), FadeIn(t1b), run_time=0.5)
        piv = m1.ax.c2p(5, a_m + b_m * 5)
        self.until(word_time("s099", word_index("s099", "Training")))
        self.play(Rotate(m1.ln, 0.12, about_point=piv), run_time=0.7)
        self.play(Rotate(m1.ln, -0.22, about_point=piv), run_time=0.8)
        self.play(Rotate(m1.ln, 0.10, about_point=piv), run_time=0.6)

        # ── s100 DS: ads → sales ──
        self.at("s100", 0.0)
        ds = tiles[1]
        m2 = mini("ad spend", "sales", noisy(5, 1.5, 0.75), (1.5, 0.75), AQUA)
        t2 = place(ds, m2, [T("the trend line", 22, INK), T("slope = sales per", 22, AQUA, weight=BOLD), T("$1k of ads", 22, AQUA, weight=BOLD)])
        il2 = T("illustration", 16, MUTED).move_to(ds.box.get_corner(UR) + LEFT * 0.75 + DOWN * 0.3)
        self.play(ml.box.animate.set_stroke(width=2.5), ds.box.animate.set_stroke(width=4), FadeIn(m2[:4]), FadeIn(il2), run_time=0.6)
        self.play(Create(m2.ln), FadeIn(t2[0]), run_time=0.6)
        self.until(word_time("s100", word_index("s100", "slope")))
        self.play(FadeIn(t2[1:]), run_time=0.5)

        # ── s101 Finance: beta ──
        self.at("s101", 0.0)
        fi = tiles[2]
        m3 = mini("market move", "stock move", noisy(9, 0.2, 1.05, 0.8, 12), (0.2, 1.0), WARN)
        t3 = place(fi, m3, [T("slope = beta", 22, WARN, weight=BOLD), T("beta above 1:", 22, INK), T("swings more than", 22, INK), T("the market", 22, INK)])
        il3 = T("illustration", 16, MUTED).move_to(fi.box.get_corner(UR) + LEFT * 0.75 + DOWN * 0.3)
        self.play(ds.box.animate.set_stroke(width=2.5), fi.box.animate.set_stroke(width=4), FadeIn(m3[:4]), FadeIn(il3), run_time=0.6)
        self.until(word_time("s101", word_index("s101", "slope")))
        self.play(Create(m3.ln), FadeIn(t3[0]), run_time=0.6)
        self.until(word_time("s101", word_index("s101", "A")))
        self.play(FadeIn(t3[1:]), run_time=0.6)

        # ── s102 CS: time per item ──
        self.at("s102", 0.0)
        cs = tiles[3]
        m4 = mini("input size", "run time", [(x, 0.4 + 0.8 * x) for x in (1, 2, 3, 4, 5)], (0.4, 0.8), BLUE_)
        t4 = place(cs, m4, [T("slope = time per item", 22, BLUE_, weight=BOLD), T("predicts a huge job", 22, INK)])
        self.play(fi.box.animate.set_stroke(width=2.5), cs.box.animate.set_stroke(width=4), FadeIn(m4[:4]), run_time=0.6)
        self.until(word_time("s102", word_index("s102", "fit")))
        self.play(Create(m4.ln), run_time=0.6)
        self.until(word_time("s102", word_index("s102", "slope")))
        self.play(FadeIn(t4[0]), run_time=0.5)
        self.until(word_time("s102", word_index("s102", "huge")))
        self.play(FadeIn(t4[1]), run_time=0.5)

        # ── s103 that's an extrapolation ──
        self.at("s103", 0.0)
        ax4 = m4.ax
        rz = Rectangle(width=ax4.c2p(10, 0)[0] - ax4.c2p(5.5, 0)[0], height=ax4.c2p(0, 10)[1] - ax4.c2p(0, 0)[1],
                       stroke_width=0, fill_color=RED_, fill_opacity=0.2).move_to(ax4.c2p(7.75, 5))
        rz.qa_ignore = True
        self.add(rz); self.bring_to_front(m4)
        ex = T("extrapolation: check it", 20, RED_, weight=BOLD).move_to(t4[1], aligned_edge=LEFT)
        self.play(FadeIn(rz), FadeOut(t4[1]), FadeIn(ex), run_time=0.6)
        self.play(rz.animate.set_fill(opacity=0.35), rate_func=there_and_back, run_time=0.8)

        # ── s104 how good is the line: later video ──
        self.at("s104", 0.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
        bax = xy_axes([0, 3, 1], [0, 30000, 10000], 6.6, 3.9, None, "sum of squared errors", x_labels={},
                      font_size=22, y_vertical=True, y_fmt=lambda v: f"{int(v):,}")
        bax.move_to(LEFT * 2.6 + DOWN * 0.05)
        b1 = bar(bax.ax, 1, 26000, INK2, width=1.1)
        b2 = bar(bax.ax, 2, 1000, VIOLET, width=1.1)
        l1 = T("flat line", 24, INK2).next_to(bax.ax.c2p(1, 0), DOWN, buff=0.2)
        l2 = T("least squares", 24, VIOLET).next_to(bax.ax.c2p(2, 0), DOWN, buff=0.2)
        v1 = T("26,000", 26, INK2, weight=BOLD).next_to(b1, UP, buff=0.12)
        v2 = T("1,000", 26, VIOLET, weight=BOLD).next_to(b2, UP, buff=0.12)
        self.play(FadeIn(bax), FadeIn(l1), FadeIn(l2), run_time=0.6)
        nl = pill("later: R squared, MSE and RMSE", MUTED, 26).move_to(RIGHT * 3.9 + UP * 1.6)
        self.play(FadeIn(nl), run_time=0.5)
        self.until(word_time("s104", word_index("s104", "twenty")))
        self.play(GrowFromEdge(b1, DOWN), FadeIn(v1), run_time=0.7)
        self.until(word_time("s104", word_index("s104", "one")))
        self.play(GrowFromEdge(b2, DOWN), FadeIn(v2), run_time=0.6)
        self.until(SEGS["s104"]["end"] + 0.15)
        self.play(FadeOut(VGroup(bax, b1, b2, l1, l2, v1, v2, nl)), run_time=0.45)
        self.finish()
