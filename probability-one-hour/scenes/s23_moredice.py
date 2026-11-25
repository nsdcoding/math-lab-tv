import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *
from itertools import product
from math import comb


def dist(n):
    c = {}
    for o in product(range(1, 7), repeat=n) if n <= 4 else []:
        c[sum(o)] = c.get(sum(o), 0) + 1
    if n > 4:   # exact counts by convolution
        c = {0: 1}
        for _ in range(n):
            nc = {}
            for s, w in c.items():
                for f in range(1, 7):
                    nc[s + f] = nc.get(s + f, 0) + w
            c = nc
    tot = 6 ** n
    ks = sorted(c)
    return ks, [c[k] / tot for k in ks]


class S23MoreDice(PBase):
    CHAPTER = "More Dice, New Shapes"

    def chart(self, n, col=AQUA):
        ks, ps = dist(n)
        ax = Axes(x_range=[0, len(ks) + 1, 1], y_range=[0, max(ps) * 1.15, max(ps) * 1.15], x_length=9.0, y_length=3.6,
                  axis_config=dict(color=INK2, stroke_width=3, include_tip=False, include_ticks=False)).move_to(DOWN * 0.1)
        w = 9.0 / (len(ks) + 1) * 0.75
        bb = VGroup(*[bar(ax, i + 1, p, col, width=w) for i, p in enumerate(ps)])
        step = 1 if len(ks) <= 16 else (5 if len(ks) <= 40 else 10)
        labs = VGroup(*[T(str(k), 22, INK2).next_to(ax.c2p(i + 1, 0), DOWN, buff=0.12) for i, k in enumerate(ks) if k % step == 0 or len(ks) <= 16])
        xt = T("total", 24, MUTED).next_to(labs, DOWN, buff=0.1)
        return VGroup(ax, bb, labs, xt), ax, bb, ks, ps

    def construct(self):
        self.at("s380")
        g, ax, bb, ks, ps = self.chart(2)
        hd = header("two dice: the mountain", AQUA, 32)
        self.play(FadeIn(hd), FadeIn(g), run_time=0.8)
        q = T("more dice?", 40, WARN, weight=BOLD).move_to(RIGHT * 4.6 + UP * 1.6)
        self.w("s380", "more")
        self.play(FadeIn(q), run_time=0.4)
        cur, curh = g, hd
        for sid, n, title in (("s381", 1, "one die: flat, like a table"), ("s382", 2, "two dice: a triangle, peak at 7"),
                              ("s383", 3, "three dice: 216 outcomes, rounder, peak at 10 and 11"),
                              ("s384", 10, "ten dice: smoother and rounder (shape only)")):
            self.at(sid)
            ng = self.chart(n)[0]
            nh = header(title, AQUA, 30)
            self.play(FadeOut(curh), FadeIn(nh), FadeOut(cur), FadeIn(ng), *([FadeOut(q)] if sid == "s381" else []), run_time=0.9)
            cur, curh = ng, nh
            if sid == "s384":
                g5 = self.chart(5)[0]
                self.play(FadeOut(cur), FadeIn(g5), run_time=0.6)
                self.play(FadeOut(g5), FadeIn(ng), run_time=0.6)
        # s385 bell curve
        self.at("s385")
        _, ax, bb, ks, ps = self.chart(10)
        mu, sd = 35, np.sqrt(10 * 35 / 12)
        curve = ax.plot(lambda x: (1 / (sd * np.sqrt(TAU))) * np.exp(-((x + 9 - mu) ** 2) / (2 * sd ** 2)), x_range=[1, len(ks), 0.1], color=VIOLET, stroke_width=6)
        curve.qa_ignore = True
        self.play(Create(curve), run_time=1.5)
        bl = pill("the bell curve", VIOLET, 36)
        self.play(FadeOut(curh), FadeIn(bl.move_to(UP * 2.85)), run_time=0.5)
        curh = bl
        nat = T("heights · measurement errors", 26, INK2).move_to(RIGHT * 3.7 + UP * 1.4)
        self.w("s385", "heights")
        self.play(FadeIn(nat), run_time=0.5)
        # s386 extremes rare
        self.at("s386")
        self.clear()
        a = VGroup(T("all sixes (total 60)", 30, RED_, weight=BOLD), T("1 way", 44, RED_, weight=BOLD)).arrange(DOWN, buff=0.3)
        b = VGroup(T("a middle total (35)", 30, AQUA, weight=BOLD), T("4,395,456 ways", 44, AQUA, weight=BOLD)).arrange(DOWN, buff=0.3)
        row = VGroup(boxed(a, RED_, pad=0.4), boxed(b, AQUA, pad=0.4)).arrange(RIGHT, buff=1.0).move_to(UP * 0.4)
        tl = T("ten dice", 28, MUTED).next_to(row, UP, buff=0.35)
        self.play(FadeIn(tl), FadeIn(row[0]), run_time=0.6)
        self.w("s386", "middle")
        self.play(FadeIn(row[1]), run_time=0.6)
        # s387 same reason as 7 vs 12
        self.at("s387")
        same = pill("same reason 7 beats 12", WARN, 36).move_to(DOWN * 1.6)
        self.play(FadeIn(same), run_time=0.6)
        self.finish()
