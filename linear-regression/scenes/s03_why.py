import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

PAIRS = [("size → price", ORANGE_), ("ads → sales", AQUA), ("hours studied → score", BLUE_), ("input size → run time", WARN)]


def mini_scatter(seed, color, slope=0.7):
    rng = np.random.default_rng(seed)
    ax = Axes(x_range=[0, 10, 2], y_range=[0, 10, 2], x_length=3.4, y_length=1.75,
              axis_config=dict(color=INK2, stroke_width=2.5, include_tip=False, tick_size=0.04))
    xs = np.linspace(1, 9, 9)
    ys = 1.2 + slope * xs + rng.normal(0, 0.8, len(xs))
    ds = VGroup(*[Dot(ax.c2p(x, min(9.6, max(0.4, y))), radius=0.055, color=INK) for x, y in zip(xs, ys)])
    b, a = np.polyfit(xs, ys, 1)
    ln = Line(ax.c2p(0.5, a + b * 0.5), ax.c2p(9.5, a + b * 9.5), color=color, stroke_width=3.5)
    tri = VGroup(Line(ax.c2p(6, a + b * 6), ax.c2p(8, a + b * 6)), Line(ax.c2p(8, a + b * 6), ax.c2p(8, a + b * 8))).set_stroke(color, 3)
    g = VGroup(ax, ds, ln); g.tri = tri; g.ax = ax
    return g


class S03Why(Base):
    CHAPTER = "Why It Matters"

    def construct(self):
        # ── s017 a school exercise? ──
        self.at("s017", 0.0)
        axg = lesson_axes(); ax = axg.ax
        dots = house_dots(ax); ln = price_line(ax, *BEST, 300, 3400)
        chart = VGroup(axg.ax, dots, ln)
        self.play(FadeIn(axg), FadeIn(dots, lag_ratio=0.15), run_time=0.9)
        self.play(Create(ln), run_time=0.8)
        self.until(word_time("s017", word_index("s017", "actually")))
        tag = pill("one of the most used tools in the world", WARN, 30).move_to(UP * 2.55 + RIGHT * 2.0)
        self.play(FadeOut(axg.labs), FadeOut(axg.xt), FadeOut(axg.yt), run_time=0.3)
        self.play(chart.animate.scale(0.55).move_to(LEFT * 4.3 + DOWN * 0.3), FadeIn(tag, shift=DOWN * 0.2), run_time=0.9)

        # ── s018 pairs that move together ──
        self.at("s018", 0.0)
        cells = VGroup()
        for i, (txt, col) in enumerate(PAIRS):
            box = card(5.0, 2.75)
            lab = T(txt, 26, col, weight=BOLD).move_to(box.get_top() + DOWN * 0.38)
            cells.add(VGroup(box, lab))
        cells.arrange_in_grid(2, 2, buff=(0.35, 0.3)).move_to(RIGHT * 2.3 + DOWN * 0.35)
        self.play(FadeOut(tag), FadeOut(chart, shift=LEFT * 0.5), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cells], lag_ratio=0.2), run_time=1.4)
        self.play(cells.animate.move_to(DOWN * 0.35), run_time=0.6)

        # ── s019 each gets a scatter ──
        self.at("s019", 0.0)
        minis = VGroup()
        for i, (txt, col) in enumerate(PAIRS):
            m = mini_scatter(i + 3, col, slope=[0.85, 0.6, 0.7, 0.9][i])
            c0 = m.get_center(); m.move_to(cells[i][0].get_center() + DOWN * 0.25); m.tri.shift(m.get_center() - c0)
            minis.add(m)
        words = ["Price", "Sales", "Exam", "How"]
        for i, w in enumerate(words):
            self.until(word_time("s019", word_index("s019", w)) - 0.05)
            m = minis[i]
            self.play(FadeIn(m[0]), FadeIn(m[1], lag_ratio=0.1), Create(m[2]), run_time=0.9)
        ill = T("illustrations", 22, MUTED).next_to(cells, UP, buff=0.18).align_to(cells, RIGHT)
        self.play(FadeIn(ill), run_time=0.4)

        # ── s021a one step → how much more ──
        self.at("s021a", 0.0)
        self.play(LaggedStart(*[Create(m.tri) for m in minis], lag_ratio=0.2), run_time=1.2)
        q = pill("one step more  →  how much more?", VIOLET, 32).move_to(UP * 3.15 + RIGHT * 1.6)
        self.until(word_time("s021a", word_index("s021a", "If")))
        self.play(FadeOut(ill), FadeIn(q, shift=DOWN * 0.2), run_time=0.6)
        self.play(*[Indicate(m.tri, color=WARN, scale_factor=1.3) for m in minis], run_time=1.0)

        # ── s020 machine learning, model number one ──
        self.at("s020", 0.0)
        grp = VGroup(cells, minis, *[m.tri for m in minis])
        self.play(FadeOut(q), grp.animate.scale(0.56).move_to(UP * 1.2), run_time=0.9)
        lab = T("machine learning · model number one", 28, VIOLET, weight=BOLD)
        frame = card(max(grp.width + 0.6, lab.width + 0.9), grp.height + 1.45, color=VIOLET, fill=BG)
        frame.move_to(grp.get_center() + DOWN * 0.5)
        lab.move_to(frame.get_bottom() + UP * 0.4)
        self.add(frame); self.bring_to_front(grp)
        self.play(Create(frame), FadeIn(lab), run_time=0.8)
        chain = VGroup(pill("misses", ORANGE_, 28), T("→", 32, MUTED), pill("a score", WARN, 28), T("→", 32, MUTED),
                       pill("smallest score", VIOLET, 28)).arrange(RIGHT, buff=0.25).next_to(frame, DOWN, buff=0.3)
        self.until(word_time("s020", word_index("s020", "misses,")))
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in chain], lag_ratio=0.35), run_time=1.8)

        # ── s021 back to our five houses ──
        self.at("s021", 0.0)
        self.play(FadeOut(VGroup(grp, frame, lab, chain), shift=UP * 0.3), run_time=0.7)
        axg2 = lesson_axes(); dots2 = house_dots(axg2.ax)
        self.play(FadeIn(axg2), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots2], lag_ratio=0.15), run_time=1.0)
        self.finish()
