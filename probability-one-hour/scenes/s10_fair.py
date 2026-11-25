import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *

FAIR = [8, 11, 9, 12, 7, 13]
LOADED = [7, 6, 8, 7, 7, 25]


class S10Fair(PBase):
    CHAPTER = "Is This Die Fair?"

    def construct(self):
        self.at("s176")
        d = die(6, ORANGE_, 1.6).move_to(UP * 0.3)
        q = T("fair?", 48, WARN, weight=BOLD).next_to(d, RIGHT, buff=0.5)
        self.play(FadeIn(d, scale=0.6), run_time=0.6)
        self.w("s176", "fair")
        self.play(FadeIn(q), Wiggle(d), run_time=0.9)
        # s177 expected 10 each
        self.at("s177")
        self.play(FadeOut(VGroup(d, q)), run_time=0.4)
        ax = bar_axes([str(k) for k in range(1, 7)], 25, 5, 7.5, 3.8, "face", "times rolled")
        ax.move_to(DOWN * 0.1)
        dash = DashedLine(ax.ax.c2p(0.4, 10), ax.ax.c2p(6.6, 10), color=AQUA, dash_length=0.12)
        el = T("expected: 60 × 1/6 = 10", 30, AQUA, weight=BOLD).move_to(UP * 2.85)
        self.play(FadeIn(ax), run_time=0.5)
        self.w("s177", "sixty")
        self.play(Create(dash), FadeIn(el), run_time=0.8)
        # s178 fair bars
        self.at("s178")
        bb = VGroup()
        words = ["eight", "eleven", "nine", "twelve", "seven", "thirteen"]
        for k, v in enumerate(FAIR):
            b = bar(ax.ax, k + 1, v, ORANGE_, width=0.8, opacity=0.85)
            n = T(str(v), 28, INK, weight=BOLD).next_to(b, UP, buff=0.1)
            bb.add(VGroup(b, n))
        self.play(dash.animate.set_stroke(opacity=0.25), run_time=0.3)
        self.qa_mute(dash)
        for k in range(6):
            self.w("s178", words[k])
            self.play(GrowFromEdge(bb[k][0], DOWN), FadeIn(bb[k][1]), run_time=0.35)
        sim = T("simulation of a fair die", 24, MUTED).move_to(ax.ax.c2p(5.2, 23))
        self.play(FadeIn(sim), run_time=0.4)
        # s179 normal wobble
        self.at("s179")
        band = Rectangle(width=ax.ax.c2p(6.6, 0)[0] - ax.ax.c2p(0.4, 0)[0], height=ax.ax.c2p(0, 14)[1] - ax.ax.c2p(0, 6)[1],
                         stroke_width=0, fill_color=AQUA, fill_opacity=0.12).move_to(ax.ax.c2p(3.5, 10))
        band.qa_ignore = True
        nw = pill("normal wobble", AQUA, 32).move_to(UP * 2.85)
        self.w("s179", "normal")
        self.play(FadeIn(band), FadeOut(el), FadeIn(nw), run_time=0.7)
        # s180 loaded die
        self.at("s180")
        lb = VGroup()
        for k, v in enumerate(LOADED):
            b = bar(ax.ax, k + 1, v, ORANGE_ if k < 5 else RED_, width=0.8, opacity=0.85)
            n = T(str(v), 28, INK if k < 5 else RED_, weight=BOLD).next_to(b, UP, buff=0.1)
            lb.add(VGroup(b, n))
        nd = pill("a different die", RED_, 32).move_to(UP * 2.85)
        self.play(FadeOut(VGroup(band, sim, nw)), FadeIn(nd), run_time=0.4)
        self.play(*[Transform(bb[k], lb[k]) for k in range(6)], run_time=1.0)
        # s181 suspicious
        self.at("s181")
        sus = pill("very unlikely for a fair die → suspicious", WARN, 30).move_to(UP * 2.85)
        self.play(FadeOut(nd), FadeIn(sus), Indicate(bb[5], color=RED_), run_time=0.8)
        # s182 predict then compare
        self.at("s182")
        self.clear()
        a = pill("predict what fair looks like", AQUA, 34); b = pill("compare with reality", WARN, 34)
        VGroup(a, b).arrange(RIGHT, buff=1.4).move_to(UP * 0.3)
        ar = Arrow(a.get_right(), b.get_left(), color=INK2, buff=0.12)
        self.play(FadeIn(a), run_time=0.5)
        self.w("s182", "compared")
        self.play(GrowArrow(ar), FadeIn(b), run_time=0.6)
        # s183 small vs big gap
        self.at("s183")
        self.play(VGroup(a, ar, b).animate.scale(0.8).move_to(UP * 2.1), run_time=0.5)
        def gap(real, lab, col):
            ax_ = bar_axes(["predicted", "real"], 25, 5, 3.4, 2.4, "", "")
            b1 = bar(ax_.ax, 1, 10, AQUA, width=0.9); b2 = bar(ax_.ax, 2, real, col, width=0.9)
            t = T(lab, 28, col, weight=BOLD).next_to(ax_, DOWN, buff=0.15)
            return VGroup(ax_, b1, b2, t)
        g1 = gap(12, "small gap: shrug", AQUA).move_to(LEFT * 3.3 + DOWN * 0.6)
        g2 = gap(25, "huge gap: suspicious", RED_).move_to(RIGHT * 3.3 + DOWN * 0.6)
        self.w("s183", "small")
        self.play(FadeIn(g1), run_time=0.6)
        self.w("s183", "huge")
        self.play(FadeIn(g2), run_time=0.6)
        self.finish()
