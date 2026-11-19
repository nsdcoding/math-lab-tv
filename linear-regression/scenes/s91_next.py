import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

NEXT_TOPIC = "gradient descent"


def bowl_ax():
    ax = Axes(x_range=[-3, 3, 1], y_range=[0, 9, 3], x_length=6.0, y_length=3.2,
              axis_config=dict(color=INK2, stroke_width=3, include_tip=False, tick_size=0.05))
    return ax


class S91Next(Base):
    CHAPTER = "Next Time"

    def construct(self):
        lg = logo(1.1).move_to(UP * 1.1).scale(0.42).to_edge(UP, buff=0.32)   # carried over from Subscribe
        self.add(lg)
        # ── s125 a puzzle ──
        self.at("s125", 0.0)
        q = VGroup(RoundedRectangle(corner_radius=0.25, width=1.6, height=1.6).set_stroke(VIOLET, 4), TB("?", 90, VIOLET))
        q.move_to(UP * 0.2)
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        # ── s126 a formula for one line; millions of settings, no formula ──
        self.at("s126", 0.0)
        nx = chip(f"next:  {NEXT_TOPIC}", AQUA, 30).next_to(lg, DOWN, buff=0.3)
        ax = Axes(x_range=[0, 3500, 500], y_range=[0, 400, 100], x_length=4.0, y_length=2.4,
                  axis_config=dict(color=INK2, stroke_width=3, include_tip=False, tick_size=0.05))
        left = VGroup(ax, house_dots(ax, r=0.08), price_line(ax, *BEST, 0, 3500, width=4))
        left.move_to(LEFT * 3.6 + UP * 0.1)
        ok = VGroup(check(AQUA, 0.3), T("a formula", 28, AQUA, weight=BOLD)).arrange(RIGHT, buff=0.2).next_to(left, DOWN, buff=0.35)
        self.play(FadeOut(q), FadeIn(nx, shift=DOWN * 0.2), FadeIn(left), run_time=0.7)
        self.play(FadeIn(ok), run_time=0.4)
        dials = VGroup()
        for i in range(9):
            for j in range(14):
                c = Circle(radius=0.11).set_stroke(INK2, 2)
                tick = Line(ORIGIN, UP * 0.1).rotate(((i * 7 + j * 3) % 11) * 0.55, about_point=ORIGIN).set_stroke(WARN, 2)
                dials.add(VGroup(c, tick).move_to([j * 0.3, -i * 0.3, 0]))
        dials.move_to(RIGHT * 3.4 + UP * 0.25)
        no = VGroup(cross(RED_, 0.16), T("millions of settings, no formula", 26, RED_, weight=BOLD)).arrange(RIGHT, buff=0.2)
        no.next_to(dials, DOWN, buff=0.35)
        self.until(word_time("s126", word_index("s126", "But")))
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dials], lag_ratio=0.01), run_time=1.6)
        self.until(word_time("s126", word_index("s126", "no")))
        self.play(FadeIn(no), run_time=0.5)
        # ── s127 roll downhill ──
        self.at("s127", 0.0)
        self.play(FadeOut(VGroup(left, ok, dials, no)), run_time=0.5)
        bx = bowl_ax().move_to(DOWN * 0.15)
        curve = bx.plot(lambda x: x * x, x_range=[-3, 3], color=WARN, stroke_width=4)
        lab = T("score", 22, MUTED).next_to(bx.y_axis, UP, buff=0.1)
        lab2 = T("illustration", 20, MUTED).next_to(bx, RIGHT, buff=0.2).align_to(bx, DOWN)
        self.play(Create(bx), Create(curve), FadeIn(lab), FadeIn(lab2), run_time=0.8)
        xs = [-2.7, -1.7, -1.05, -0.6, -0.3, -0.1, 0.0]
        ball = Dot(bx.c2p(xs[0], xs[0] ** 2), radius=0.15, color=VIOLET)
        self.until(word_time("s127", word_index("s127", "feels")))
        self.play(FadeIn(ball, scale=0.4), run_time=0.3)
        for x in xs[1:]:
            self.play(ball.animate.move_to(bx.c2p(x, x * x)), run_time=0.45)
        gd = T("gradient descent", 40, AQUA, weight=BOLD).move_to(DOWN * 2.2)
        self.until(word_time("s127", word_index("s127", "gradient")) - 0.2)
        self.play(FadeIn(gd, shift=UP * 0.2), run_time=0.5)
        # ── s128 see you ──
        self.at("s128", 0.0)
        self.play(Indicate(nx, color=AQUA, scale_factor=1.08), run_time=1.0)
        self.finish()
