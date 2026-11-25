import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *

WAYS = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]


class S09Many(PBase):
    CHAPTER = "Try It Many Times"

    def construct(self):
        self.at("s156")
        hd = header("does real life follow the counting?", INK, 32)
        th = bar_axes([str(s) for s in range(2, 13)], 6, 2, 5.0, 3.0, "total", "")
        th.move_to(LEFT * 3.5 + DOWN * 0.2)
        tb = bars(th.ax, WAYS, AQUA, width=0.32)
        rl = bar_axes([str(s) for s in range(2, 13)], 6, 2, 5.0, 3.0, "total", "")
        rl.move_to(RIGHT * 3.5 + DOWN * 0.2)
        l1 = T("counting (paper)", 30, AQUA, weight=BOLD).next_to(th, UP, buff=0.3)
        l2 = T("real rolls", 30, WARN, weight=BOLD).next_to(rl, UP, buff=0.3)
        self.play(FadeIn(hd), FadeIn(th), FadeIn(tb), FadeIn(l1), run_time=0.8)
        self.w("s156", "test")
        self.play(FadeIn(rl), FadeIn(l2), run_time=0.6)
        # s157–s160 ten flips
        self.at("s157")
        self.clear()
        flips = SIM["ten_flips"]
        slots = VGroup(*[coin("?", MUTED, 0.42) for _ in range(10)]).arrange(RIGHT, buff=0.2).move_to(UP * 1.4)
        self.play(FadeIn(slots, lag_ratio=0.05), run_time=0.8)
        self.at("s158")
        half = T("chance of heads = 1/2 … so exactly 5 heads?", 32, INK2).move_to(DOWN * 0.1)
        self.play(FadeIn(half), run_time=0.5)
        cnt = T("heads: 0 of 10", 36, WARN, weight=BOLD).move_to(DOWN * 1.2)
        self.w("s158", "not")
        self.add(cnt)
        h = 0
        for k, f in enumerate(flips):
            h += f == "H"
            nc = coin(f, WARN if f == "H" else BLUE_, 0.42).move_to(slots[k])
            self.play(Transform(slots[k], nc), Transform(cnt, T(f"heads: {h} of {k + 1}", 36, WARN, weight=BOLD).move_to(cnt)), run_time=0.22)
        sim = T("simulation", 24, MUTED).next_to(slots, UP, buff=0.25)
        self.play(FadeIn(sim), run_time=0.3)
        self.at("s159")
        self.play(FadeOut(half), FadeOut(cnt), run_time=0.3)
        pl = prob_line(9.0, fs=26, title="share of heads", labels=(0, 0.5, 1), percent=True).move_to(DOWN * 0.9)
        dash = DashedLine(pl.nl.n2p(0.5) + UP * 0.9, pl.nl.n2p(0.5), color=INK2)
        p7 = pin(pl.nl, 0.7, WARN, "70%", h=0.75, fs=32)
        self.play(FadeIn(pl), Create(dash), run_time=0.5)
        self.w("s159", "seventy")
        self.play(FadeIn(p7, shift=DOWN * 0.2), run_time=0.5)
        self.at("s160")
        wob = pill("10 flips: big wobbles", WARN, 32).move_to(DOWN * 2.15)
        self.play(FadeIn(wob), run_time=0.5)
        self.play(Wiggle(p7), run_time=0.8)
        # s161–s164 settling curve
        self.at("s161")
        self.clear()
        hs = SIM["heads_share"]
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 1, 0.25], x_length=10, y_length=3.8,
                  axis_config=dict(color=INK2, stroke_width=3, include_tip=False, tick_size=0.06)).move_to(UP * 0.15)
        xl = VGroup(*[T(s, 24, INK2).next_to(ax.c2p(v, 0), DOWN, buff=0.15) for v, s in zip(range(5), ("1", "10", "100", "1,000", "10,000"))])
        yl = VGroup(*[T(s, 24, INK2).next_to(ax.c2p(0, v), LEFT, buff=0.12) for v, s in zip((0, 0.25, 0.5, 0.75, 1), ("0%", "25%", "50%", "75%", "100%"))])
        xt = T("number of flips", 24, MUTED).next_to(xl, DOWN, buff=0.12)
        yt = T("share of heads", 24, MUTED).rotate(PI / 2).next_to(yl, LEFT, buff=0.15)
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(4, 0.5), color=INK2, dash_length=0.12)
        self.play(FadeIn(VGroup(ax, xl, yl, xt, yt)), Create(half), run_time=0.8)
        pts = [(np.log10(int(n)), v) for n, v in hs.items()]
        path = VMobject(stroke_color=WARN, stroke_width=5).set_points_as_corners([ax.c2p(x, y) for x, y in pts])
        path.qa_ignore = True
        self.at("s162")
        k1 = [i for i, (x, _) in enumerate(pts) if x <= 1.01][-1]
        p1 = VMobject(stroke_color=WARN, stroke_width=5).set_points_as_corners([ax.c2p(x, y) for x, y in pts[:k1 + 1]])
        p1.qa_ignore = True
        self.play(Create(p1), run_time=1.5, rate_func=linear)
        wild = T("jumps around", 28, WARN, weight=BOLD).move_to(ax.c2p(0.8, 0.95))
        self.play(FadeIn(wild), run_time=0.4)
        self.at("s163")
        self.remove(p1)
        self.add(path)
        path2 = path.copy()
        self.play(Create(path), run_time=2.6, rate_func=linear)
        settle = pill("settles near 1/2", AQUA, 30).move_to(ax.c2p(3.2, 0.82))
        self.play(FadeIn(settle), run_time=0.5)
        self.at("s164")
        lln = def_card("LAW OF LARGE NUMBERS", "over many tries, results get close to the probability", VIOLET, 28)
        lln.scale_to_fit_width(min(lln.width, 12.6)).move_to(UP * 2.85)
        self.play(FadeIn(lln, shift=DOWN * 0.2), run_time=0.7)
        # s165–s168 dice runs
        self.at("s165")
        self.clear()
        rl = bar_axes([str(s) for s in range(2, 13)], 0.25, 0.05, 9.0, 3.6, "total", "share of rolls", y_fmt=lambda v: f"{int(round(v * 100))}%")
        rl.move_to(DOWN * 0.1)
        self.play(FadeIn(rl), run_time=0.6)
        theory = VMobject(stroke_color=AQUA, stroke_width=5).set_points_as_corners(
            [rl.ax.c2p(i + 1, WAYS[i] / 36) for i in range(11)])
        theory.qa_ignore = True
        cur = None
        tag = None
        for sid, n, word in (("s166", 36, "thirty"), ("s167", 360, "three"), ("s168", 36000, "thirty")):
            self.at(sid)
            cnt = SIM[f"sums_{n}"]
            vals = [cnt[str(s)] / n for s in range(2, 13)]
            nb = bars(rl.ax, vals, WARN, width=0.55, op=0.85)
            nt = pill(f"simulation · {n:,} rolls", WARN, 30).move_to(UP * 2.85)
            if cur is None:
                self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in nb], lag_ratio=0.05), FadeIn(nt), run_time=1.0)
            else:
                if n == 360:
                    self.play(FadeOut(zl), run_time=0.3)
                self.play(ReplacementTransform(cur, nb), FadeOut(tag), FadeIn(nt), run_time=1.0)
            cur, tag = nb, nt
            if n == 36:
                zeros = [i for i, v in enumerate(vals) if v == 0]
                zl = VGroup(*[T("0", 26, RED_, weight=BOLD).next_to(rl.ax.c2p(i + 1, 0), UP, buff=0.3) for i in zeros])
                self.w(sid, "some")
                self.play(FadeIn(zl), run_time=0.4)
        self.w("s168", "mountain")
        tl = T("counting predicted this", 28, AQUA, weight=BOLD).move_to(rl.ax.c2p(9.3, 0.175))
        self.play(Create(theory), FadeIn(tl), run_time=1.0)
        # s169 paper predicts reality
        self.at("s169")
        self.clear()
        pg = DiceGrid(0.3, fs=14, titles=False)
        dd = VGroup(die(3, ORANGE_, 0.9), die(4, BLUE_, 0.9)).arrange(RIGHT, buff=0.25)
        row = VGroup(pg, dd).arrange(RIGHT, buff=3.0).move_to(UP * 0.2)
        ar = Arrow(pg.get_right(), dd.get_left(), color=INK2, buff=0.3)
        l1 = T("paper", 28, AQUA).next_to(pg, DOWN, buff=0.3); l2 = T("real dice", 28, WARN).next_to(dd, DOWN, buff=0.5)
        tg = pill("paper predicts reality", VIOLET, 34).move_to(DOWN * 1.8)
        self.play(FadeIn(pg), FadeIn(l1), run_time=0.5)
        self.play(GrowArrow(ar), FadeIn(dd), FadeIn(l2), run_time=0.7)
        self.w("s169", "power")
        self.play(FadeIn(tg), run_time=0.5)
        # s170 two routes
        self.at("s170")
        self.clear()
        pl = prob_line(9.0, fs=26, title="a probability").move_to(DOWN * 1.2)
        r1 = pill("count outcomes", AQUA, 34).move_to(LEFT * 3.2 + UP * 1.4)
        r2 = pill("try many times", WARN, 34).move_to(RIGHT * 3.2 + UP * 1.4)
        a1 = Arrow(r1.get_bottom(), pl.nl.n2p(0.35) + UP * 0.25, color=AQUA, buff=0.15)
        a2 = Arrow(r2.get_bottom(), pl.nl.n2p(0.65) + UP * 0.25, color=WARN, buff=0.15)
        self.play(FadeIn(pl), FadeIn(r1), GrowArrow(a1), run_time=0.7)
        self.w("s170", "try")
        self.play(FadeIn(r2), GrowArrow(a2), run_time=0.7)
        # s128a try it tonight
        self.at("s128a")
        self.clear()
        def tally(name, flips, col):
            hcount = flips.count("H")
            marks = VGroup(*[Line(UP * 0.2, DOWN * 0.2, color=col, stroke_width=4) for _ in range(hcount)]).arrange(RIGHT, buff=0.12)
            t = T(name, 30, col, weight=BOLD)
            n = T(f"{hcount} heads of 20", 30, INK)
            g = VGroup(t, marks, n).arrange(DOWN, buff=0.3)
            return boxed(g, col, pad=0.35)
        you = tally("you", "HHTHTTHHTHHTHTTHHHTH", ORANGE_).move_to(LEFT * 3.2 + UP * 0.3)
        fr_ = tally("your friend", "HTTHTHTTHTHHTTTHTHTH", BLUE_).move_to(RIGHT * 3.2 + UP * 0.3)
        il = T("illustration", 22, MUTED).move_to(DOWN * 1.7)
        self.play(FadeIn(you, shift=UP * 0.2), FadeIn(il), run_time=0.7)
        self.w("s128a", "friend")
        self.play(FadeIn(fr_, shift=UP * 0.2), run_time=0.7)
        nm = pill("different, and that's normal", AQUA, 32).move_to(DOWN * 2.2)
        self.w("s128a", "normal")
        self.play(FadeOut(il), FadeIn(nm), run_time=0.5)
        # s171 weather forecast
        self.at("s171")
        self.clear()
        cal = VGroup()
        rng = np.random.default_rng(5); rr = set(rng.choice(30, 21, replace=False))
        for k in range(30):
            c_ = card(0.75, 0.75, GRID).move_to(RIGHT * (k % 10) * 0.85 + DOWN * (k // 10) * 0.85)
            ic = (ic_cloud(BLUE_, 0.38) if k in rr else ic_sun(WARN, 0.45)).move_to(c_)
            cal.add(VGroup(c_, ic))
        cal.move_to(UP * 0.5)
        ft = MathTex(r"{\text{rainy days}", r"\over", r"\text{similar days}}", "=", r"{21 \over 30}", font_size=48).move_to(DOWN * 1.75)
        ft[0].set_color(BLUE_); ft[2].set_color(WARN); ft[4].set_color(VIOLET)
        cl = T("illustration", 22, MUTED).next_to(cal, UP, buff=0.2)
        self.play(FadeIn(cal, lag_ratio=0.02), FadeIn(cl), run_time=1.2)
        self.w("s171", "how")
        self.play(Write(ft), run_time=1.0)
        # s172 pocket idea
        self.at("s172")
        self.clear()
        pk = pill("patterns over many tries", WARN, 40).move_to(UP * 0.8)
        nx = T("says nothing about the next single flip", 32, INK2).next_to(pk, DOWN, buff=0.6)
        self.play(FadeIn(pk, scale=0.8), run_time=0.6)
        self.play(Circumscribe(pk, color=WARN), run_time=1.0)
        self.w("s172", "nothing")
        self.play(FadeIn(nx), run_time=0.5)
        # s173–s174 streaks
        self.at("s173")
        self.clear()
        f20 = SIM["twenty_flips"]
        row = VGroup(*[coin(f, WARN if f == "H" else BLUE_, 0.27) for f in f20]).arrange(RIGHT, buff=0.08).move_to(UP * 0.9)
        self.play(LaggedStart(*[FadeIn(c) for c in row], lag_ratio=0.05), run_time=1.4)
        i = f20.index("HHHH")
        br = SurroundingRectangle(VGroup(*row[i:i + 4]), color=AQUA, buff=0.1, corner_radius=0.1)
        br.qa_ignore = True
        self.play(Create(br), run_time=0.5)
        self.at("s174")
        st = pill("4+ heads in a row: in about 48% of 20-flip runs", AQUA, 30).move_to(DOWN * 0.7)
        self.w("s174", "nearly")
        self.play(FadeIn(st), run_time=0.6)
        # s175 random is clumpy
        self.at("s175")
        self.clear()
        neat = VGroup(*[coin("HT"[k % 2], (WARN, BLUE_)[k % 2], 0.24) for k in range(20)]).arrange(RIGHT, buff=0.07)
        real = VGroup(*[coin(f, WARN if f == "H" else BLUE_, 0.24) for f in f20]).arrange(RIGHT, buff=0.07)
        neat.move_to(UP * 1.4); real.move_to(DOWN * 0.6)
        ln = T("looks random, but too tidy", 28, MUTED).next_to(neat, UP, buff=0.25)
        lr = T("real randomness: clumpy", 28, AQUA, weight=BOLD).next_to(real, UP, buff=0.25)
        self.play(FadeIn(neat), FadeIn(ln), run_time=0.7)
        self.w("s175", "unpredictable")
        self.play(FadeIn(real), FadeIn(lr), run_time=0.7)
        self.finish()
