import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *


class S11Recap(PBase):
    CHAPTER = "Quick Recap"

    def construct(self):
        self.at("s184")
        hd = header("how far we've come", INK, 32)
        road = Line(LEFT * 6.2, RIGHT * 6.2, color=INK2, stroke_width=5).move_to(DOWN * 1.9)
        stops = [-5.2, -2.8, -0.4, 2.0, 4.4]
        dots = VGroup(*[Dot(radius=0.13, color=INK2).move_to([x, -1.9, 0]) for x in stops])
        self.play(FadeIn(hd), Create(road), FadeIn(dots), run_time=0.8)
        pinm = Triangle(color=VIOLET, fill_opacity=1, stroke_width=0).scale(0.2).rotate(PI).move_to([stops[0] - 0.9, -1.5, 0])
        self.play(FadeIn(pinm), run_time=0.3)
        # milestone mini visuals
        def m1():
            pl = prob_line(2.0, fs=20, title="", labels=(0, 1))
            return VGroup(pl, T("0 to 1", 26, INK, weight=BOLD).next_to(pl, UP, buff=0.3))
        def m2():
            return VGroup(colfrac("want", "all", fs=42).set_color(INK), T("count & divide", 26, INK, weight=BOLD)).arrange(DOWN, buff=0.3)
        def m3():
            g = DiceGrid(0.22, fs=12, titles=False)
            return VGroup(g, T("tree · grid · ×", 26, INK, weight=BOLD)).arrange(DOWN, buff=0.25)
        def m4():
            ax = bar_axes([""] * 11, 6, 6, 2.0, 1.2, "", "", fs=14)
            ax.ylabs.set_opacity(0)
            b = bars(ax.ax, [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1], AQUA, width=0.12)
            return VGroup(VGroup(ax.ax, b), T("7 is most likely", 26, INK, weight=BOLD)).arrange(DOWN, buff=0.25)
        def m5():
            ax = Axes(x_range=[0, 4, 1], y_range=[0, 1, 0.5], x_length=2.0, y_length=1.2,
                      axis_config=dict(color=INK2, stroke_width=2, include_tip=False, include_ticks=False))
            pts = [(0, 0.9), (0.4, 0.2), (0.8, 0.7), (1.3, 0.4), (1.8, 0.57), (2.5, 0.47), (3.2, 0.51), (4, 0.5)]
            c = VMobject(stroke_color=WARN, stroke_width=3).set_points_smoothly([ax.c2p(x, y) for x, y in pts])
            c.qa_ignore = True
            return VGroup(VGroup(ax, c), T("settles over many tries", 26, INK, weight=BOLD)).arrange(DOWN, buff=0.25)
        ms = [m1(), m2(), m3(), m4(), m5()]
        for k, (sid, m) in enumerate(zip(("s185", "s186", "s187", "s188", "s189"), ms)):
            self.at(sid)
            m.move_to([stops[k], 0.35, 0])
            if m.width > 2.3:
                m.scale_to_fit_width(2.3)
            self.play(pinm.animate.move_to([stops[k], -1.5, 0]), dots[k].animate.set_color(VIOLET), FadeIn(m, shift=UP * 0.3), run_time=0.7)
        # s190 the foundation
        self.at("s190")
        nxt = T("next: NOT · OR · AND · GIVEN · EXPECTED VALUE", 28, MUTED).move_to(DOWN * 2.35)
        nxt.move_to(UP * 2.1)
        self.play(FadeOut(hd), run_time=0.3)
        fd = pill("the foundation", AQUA, 34).move_to(UP * 2.85)
        self.play(FadeIn(fd), FadeIn(nxt), run_time=0.7)
        self.play(pinm.animate.move_to([5.9, -1.5, 0]), run_time=0.8)
        self.finish()
