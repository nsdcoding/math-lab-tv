import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def price_line(seed, w=2.6, h=0.9, n=26, drift=0.0, color=INK2, width=4):
    r = np.random.default_rng(seed)
    y = np.cumsum(r.normal(drift, 1.0, n)); y = (y - y.min()) / (np.ptp(y) + 1e-9) * h - h / 2
    pts = [np.array([x, yy, 0]) for x, yy in zip(np.linspace(-w / 2, w / 2, n), y)]
    return VMobject().set_points_as_corners(pts).set_stroke(color, width)


def btn(label, color, w=1.6, h=0.7):
    b = RoundedRectangle(corner_radius=0.14, width=w, height=h).set_stroke(color, 3).set_fill("#22221f", 1)
    b.qa_container = True
    t = TB(label, 32, color).move_to(b)
    return VGroup(b, t)


class S10Real(Base):
    CHAPTER = "Real World"

    def construct(self):
        rng = np.random.default_rng(10)
        # ── s090 where will you meet this? four tiles around the coffee coin ──
        self.at("s090", 0.0)
        tiles = VGroup(domain_tile("Data Science", AQUA, w=4.9, h=1.3, size=34), domain_tile("Machine Learning", VIOLET, w=4.9, h=1.3, size=34),
                       domain_tile("Finance", WARN, w=4.9, h=1.3, size=34), domain_tile("Computer Science", BLUE_, w=4.9, h=1.3, size=34))
        tiles.arrange_in_grid(2, 2, buff=(1.3, 1.1)).move_to(UP * 0.5)
        cc = coin("H", BLUE_, 0.45).move_to(tiles.get_center())
        self.play(FadeIn(cc, scale=0.5), LaggedStart(*[FadeIn(t_, shift=(t_.get_center() - tiles.get_center()) * 0.15) for t_ in tiles], lag_ratio=0.12),
                  run_time=0.9)
        self.idle(lambda: flipping(cc))

        # ── s091 data science: an A/B test ──
        self.at("s091", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(tiles[1:], cc)), tiles[0].animate.scale(0.7).move_to(UP * 3.0 + RIGHT * 3.9), run_time=0.6)
        bA = btn("A", BLUE_).move_to(LEFT * 2.6 + UP * 0.9); bB = btn("B", ORANGE_).move_to(RIGHT * 2.6 + UP * 0.9)
        cA = T("old button", 24, BLUE_, weight=BOLD).next_to(bA, UP, buff=0.2); cB = T("new button", 24, ORANGE_, weight=BOLD).next_to(bB, UP, buff=0.2)
        self.word("s091", "test", dt=-0.3)
        self.play(FadeIn(bA, scale=0.6), FadeIn(bB, scale=0.6), FadeIn(cA), FadeIn(cB), run_time=0.5)
        src = UP * 0.0 + DOWN * 1.6
        crowd_ = VGroup(*[person(INK2, 0.7) for _ in range(9)]).arrange(RIGHT, buff=0.25).move_to(DOWN * 1.7)
        self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.2) for p_ in crowd_], lag_ratio=0.06), run_time=0.5)
        def visitors():
            ds = []
            for i in range(10):
                d = Dot(radius=0.07, color=INK2).move_to(crowd_.get_top() + RIGHT * rng.uniform(-1.6, 1.6))
                d.qa_ignore = True
                tgt = bA if i % 2 == 0 else bB
                ds.append(FadeOut(d, shift=tgt.get_bottom() + DOWN * 0.1 - d.get_center()))
            return LaggedStart(*ds, lag_ratio=0.08)
        self.word("s091", "Half", dt=-0.3)
        self.play(visitors(), run_time=1.0)
        self.idle(visitors)

        # ── s092 the null: the button makes no difference; how often would a gap this big appear by chance? ──
        self.at("s092", 0.0)
        self.idle()
        nulc = pill("H₀: the button makes no difference", BLUE_, 28).move_to(DOWN * 1.1)
        self.play(FadeOut(crowd_), FadeIn(nulc, shift=UP * 0.2), run_time=0.5)
        clicksA = ValueTracker(0); clicksB = ValueTracker(0)
        kA = always_redraw(lambda: T(f"{int(clicksA.get_value())} clicks", 26, BLUE_, weight=BOLD).next_to(bA, DOWN, buff=0.2))
        kB = always_redraw(lambda: T(f"{int(clicksB.get_value())} clicks", 26, ORANGE_, weight=BOLD).next_to(bB, DOWN, buff=0.2))
        self.add(kA, kB)
        self.word("s092", "clicks", dt=-0.5)
        self.play(clicksA.animate.set_value(48), clicksB.animate.set_value(61), run_time=1.0)
        kA.clear_updaters(); kB.clear_updaters()
        # a small null distribution of gaps (illustration: shape only)
        gx = xy_axes([-20, 20, 5], [0, 10, 5], 6.0, 1.4, "gap B − A by chance", "runs", x_labels={0: "0", 20: "+20"},
                     font_size=20)
        gx.move_to(DOWN * 1.5 + LEFT * 1.6)
        gx.xt.next_to(gx.ax.x_axis, RIGHT, buff=0.25).shift(UP * 0.1)
        gb = VGroup(*[bar(gx.ax, x, 9.5 * np.exp(-(x / 7) ** 2), BLUE_, width=0.26) for x in range(-20, 21, 1)])
        ill = T("illustration", 20, MUTED).next_to(gx.xt, UP, buff=0.15).align_to(gx.xt, LEFT)
        self.word("s092", "gap", dt=-0.3)
        self.play(FadeOut(nulc), Create(gx.ax), FadeIn(gx.labs), FadeIn(gx.xt), FadeIn(ill), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in gb], lag_ratio=0.02), run_time=0.9)
        obs = marker(gx.ax.x_axis, 13, WARN, "+13", height=0.9, fs=24)
        self.play(FadeIn(obs, shift=DOWN * 0.3), *[gb[k].animate.set_fill(AQUA, 1) for k in range(33, 41)], run_time=0.6)
        self.idle(lambda: pulse(obs, 1.15), lambda: LaggedStart(*[pulse(gb[k], 1.3) for k in range(33, 41)], lag_ratio=0.06))

        # ── s093 machine learning: two models, a little apart ──
        self.at("s093", 0.0)
        self.idle()
        ml_hdr = tiles[1].copy().scale(0.7).move_to(UP * 3.0 + RIGHT * 3.9)
        m1 = VGroup(card(3.6, 1.8, VIOLET), TB("model 1", 32, VIOLET), T("accuracy 91.2%", 28, INK, weight=BOLD))
        m2 = VGroup(card(3.6, 1.8, VIOLET), TB("model 2", 32, VIOLET), T("accuracy 91.6%", 28, INK, weight=BOLD))
        for m_ in (m1, m2):
            VGroup(m_[1], m_[2]).arrange(DOWN, buff=0.2).move_to(m_[0])
        m1.move_to(LEFT * 3.0 + UP * 0.6); m2.move_to(RIGHT * 3.0 + UP * 0.6)
        ill2 = T("illustration", 20, MUTED).next_to(VGroup(m1, m2), DOWN, buff=0.2)
        stage = VGroup(bA, bB, cA, cB, kA, kB, gx, gb, ill, obs)
        push(self, stage, VGroup(m1, m2, ill2), LEFT, run_time=0.7)
        self.play(ReplacementTransform(tiles[0], ml_hdr), run_time=0.4)
        self.word("s093", "higher", dt=-0.3)
        self.play(Indicate(m2[2], color=WARN, scale_factor=1.15), run_time=0.6)
        cmid = coin("?", WARN, 0.4).move_to(UP * 0.6)
        self.word("s093", "luckier", dt=-0.3)
        self.play(FadeIn(cmid, scale=0.5), run_time=0.3)
        self.play(flipping(cmid), run_time=0.4)
        self.idle(lambda: flipping(cmid), lambda: pulse(m2, 1.05))

        # ── s094 a shuffle test: swap the labels, see what gaps chance makes ──
        self.at("s094", 0.0)
        self.idle()
        sx = xy_axes([-1, 1, 0.5], [0, 10, 5], 5.0, 1.4, "gap after shuffling labels (points)", "runs", x_labels={0: "0", 1: "+1"}, font_size=20)
        sx.move_to(DOWN * 1.5 + LEFT * 1.8)
        sx.xt.next_to(sx.ax.x_axis, RIGHT, buff=0.25).shift(UP * 0.1)
        self.play(FadeOut(ill2), Create(sx.ax), FadeIn(sx.labs), FadeIn(sx.xt), run_time=0.5)
        hist = [0] * 21
        sdots = []
        def shuffle_once():
            k = int(np.clip(rng.normal(10, 3.2), 0, 20)); hist[k] += 1
            d = Square(0.2).set_stroke(width=0).set_fill(VIOLET, 0.9).move_to(sx.ax.c2p(-1 + k * 0.1, 0) + UP * (0.12 + 0.22 * (hist[k] - 1)))
            d.qa_joined = True
            sdots.append(d)
            return AnimationGroup(m1[1].animate(rate_func=there_and_back).shift(RIGHT * 6.0),
                                  m2[1].animate(rate_func=there_and_back).shift(LEFT * 6.0), FadeIn(d, shift=DOWN * 0.5))
        self.qa_mute(m1[1]); self.qa_mute(m2[1])
        self.word("s094", "shuffle", dt=-0.3)
        for _ in range(4):
            self.play(shuffle_once(), run_time=0.45)
        obs2 = marker(sx.ax.x_axis, 0.4, WARN, "real gap +0.4", height=1.1, fs=22)
        obs2.lab.next_to(obs2.tri, RIGHT, buff=0.12)
        self.play(FadeIn(obs2, shift=DOWN * 0.3), run_time=0.4)
        self.idle(lambda: shuffle_once())

        # ── s094a linear regression: every input gets its own p value ──
        self.at("s094a", 0.0)
        self.idle()
        self.qa_mute(m1[1], False); self.qa_mute(m2[1], False)
        rows = [("input", "slope", "p value"), ("house size", "+1.8", "0.001"), ("house age", "−0.3", "0.04"), ("paint colour", "+0.1", "0.62")]
        tbl = VGroup()
        for r_, row in enumerate(rows):
            rr = VGroup(*[T(c, 28, (MUTED if r_ == 0 else (AQUA if j == 2 else INK)), weight=BOLD) for j, c in enumerate(row)])
            for j, c in enumerate(rr):
                c.move_to(RIGHT * [-3.2, 0.2, 3.0][j] + DOWN * 0.62 * r_)
            tbl.add(rr)
        tbox = card(9.6, 3.0, VIOLET).move_to(tbl.get_center())
        reg = VGroup(tbox, tbl).move_to(UP * 0.3)
        ill3 = T("illustration", 20, MUTED).next_to(reg, DOWN, buff=0.15).align_to(reg, RIGHT)
        push(self, VGroup(m1, m2, cmid, sx, obs2, *sdots), VGroup(tbox, tbl[0], ill3), LEFT, run_time=0.7)   # rows fade in after
        self.word("s094a", "input", dt=-0.3)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.3) for r_ in tbl[1:]], lag_ratio=0.25), run_time=0.8)
        self.word("s094a", "no", dt=-0.3)
        self.play(LaggedStart(*[Indicate(r_[2], color=AQUA, scale_factor=1.3) for r_ in tbl[1:]], lag_ratio=0.2), run_time=0.9)
        self.word("s094a", "slope", dt=-0.3)
        self.play(LaggedStart(*[Indicate(r_[1], color=WARN, scale_factor=1.3) for r_ in tbl[1:]], lag_ratio=0.2), run_time=0.8)
        self.idle(lambda: pulse(tbl[3][2], 1.25), lambda: pulse(tbl[1][2], 1.25))

        # ── s095 finance: a strategy beats the market — or was it luck? ──
        self.at("s095", 0.0)
        self.idle()
        fin_hdr = tiles[2].copy().scale(0.7).move_to(UP * 3.0 + RIGHT * 3.9)
        pl = price_line(3, w=7.0, h=2.0, n=40, drift=0.25, color=WARN, width=5).move_to(UP * 0.5 + LEFT * 1.4)
        push(self, VGroup(reg, ill3), pl, LEFT, run_time=0.6)
        self.play(ReplacementTransform(ml_hdr, fin_hdr), Create(pl), run_time=1.0)
        prof = pill("+ profit", AQUA, 28).next_to(pl.get_end(), RIGHT, buff=0.2)
        self.word("s095", "beats", dt=-0.3)
        self.play(FadeIn(prof, shift=LEFT * 0.2), run_time=0.4)
        self.word("s095", "noisy", dt=-0.3)
        self.play(Wiggle(pl, scale_value=1.05, rotation_angle=0.02 * TAU), run_time=0.7)
        noedge = pill("H₀: no real edge — the profit was luck", BLUE_, 28).move_to(DOWN * 1.6)
        self.word("s095", "null", dt=-0.3)
        self.play(FadeIn(noedge, shift=UP * 0.2), run_time=0.5)
        self.idle(lambda: ShowPassingFlash(pl.copy().set_stroke(INK, 9), time_width=0.4), lambda: pulse(noedge, 1.06))

        # ── s096 try enough strategies and some look brilliant by luck ──
        self.at("s096", 0.0)
        self.idle()
        many = VGroup(*[price_line(100 + i, w=2.2, h=0.6, n=18, color=MUTED, width=3) for i in range(20)]).arrange_in_grid(4, 5, buff=(0.45, 0.35))
        many.move_to(UP * 0.45)
        push(self, VGroup(pl, prof, noedge), many, LEFT, run_time=0.6)
        best = many[13]
        self.word("s096", "brilliant", dt=-0.3)
        self.play(best.animate.set_stroke(WARN, 5), ripple(best.get_center(), WARN, r=0.4, scale=4), run_time=0.6)
        luck = pill("pure luck?", RED_, 28).move_to(DOWN * 1.85)
        self.play(FadeIn(luck, shift=UP * 0.2), run_time=0.35)
        self.idle(lambda: LaggedStart(*[ShowPassingFlash(m.copy().set_stroke(INK, 5), time_width=0.5) for m in many[::3]], lag_ratio=0.1),
                  lambda: pulse(best, 1.2))

        # ── s097 computer science: is the new code really faster? ──
        self.at("s097", 0.0)
        self.idle()
        cs_hdr = tiles[3].copy().scale(0.7).move_to(UP * 3.0 + RIGHT * 3.9)
        tx = NumberLine(x_range=[80, 120, 10], length=9.0, color=INK2, stroke_width=3, include_tip=False, tick_size=0.08).move_to(DOWN * 1.3)
        txl = VGroup(*[T(f"{v} ms", 22, INK2).next_to(tx.n2p(v), DOWN, buff=0.15) for v in range(80, 121, 10)])
        txt = T("run time", 24, MUTED).next_to(txl, DOWN, buff=0.12).align_to(tx, RIGHT)
        lo = T("old code", 26, BLUE_, weight=BOLD).move_to(LEFT * 5.6 + UP * 0.85)
        ln_ = T("new code", 26, ORANGE_, weight=BOLD).move_to(LEFT * 5.6 + DOWN * 0.15)
        push(self, VGroup(many, luck), VGroup(tx, txl, txt, lo, ln_), LEFT, run_time=0.6)
        self.play(ReplacementTransform(fin_hdr, cs_hdr), run_time=0.4)
        oldt = rng.normal(104, 6, 14); newt = rng.normal(99, 6, 14)
        def runs(vals, y, color):
            return [FadeIn(Dot(tx.n2p(float(np.clip(v, 81, 119))) + UP * (y + 1.3), radius=0.09, color=color), scale=2.5) for v in vals]
        self.word("s097", "Timing", dt=-0.3)
        self.play(LaggedStart(*runs(oldt[:7], 0.85, BLUE_), *runs(newt[:7], -0.15, ORANGE_), lag_ratio=0.08), run_time=1.0)
        self.word("s097", "many", dt=-0.3)
        self.play(LaggedStart(*runs(oldt[7:], 0.85, BLUE_), *runs(newt[7:], -0.15, ORANGE_), lag_ratio=0.06), run_time=0.9)
        mo = Line(tx.n2p(float(oldt.mean())) + UP * 2.4, tx.n2p(float(oldt.mean())) + UP * 1.8).set_stroke(BLUE_, 6)
        mn = Line(tx.n2p(float(newt.mean())) + UP * 1.4, tx.n2p(float(newt.mean())) + UP * 0.8).set_stroke(ORANGE_, 6)
        q_ = pill("speed-up, or noise?", WARN, 26).move_to(RIGHT * 3.8 + UP * 1.75)
        self.word("s097", "speed", dt=-0.4)
        self.play(Create(mo), Create(mn), FadeIn(q_, scale=0.6), run_time=0.6)
        self.idle(lambda: pulse(q_, 1.12))

        # ── s098 different worlds, same question ──
        self.at("s098", 0.0)
        self.idle()
        tiles2 = VGroup(domain_tile("Data Science", AQUA, w=4.9, h=1.3, size=34), domain_tile("Machine Learning", VIOLET, w=4.9, h=1.3, size=34),
                        domain_tile("Finance", WARN, w=4.9, h=1.3, size=34), domain_tile("Computer Science", BLUE_, w=4.9, h=1.3, size=34))
        tiles2.arrange_in_grid(2, 2, buff=(1.3, 1.1)).move_to(UP * 0.5)
        cc2 = coin("H", BLUE_, 0.45).move_to(tiles2.get_center())
        allold = VGroup(*[m for m in self.mobjects if isinstance(m, VMobject)])
        self.play(FadeOut(allold, shift=LEFT * 1.0), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(t_, scale=0.8) for t_ in tiles2], lag_ratio=0.1), FadeIn(cc2, scale=0.5), run_time=0.7)
        qq = pill("real effect, or just chance?", WARN, 34).move_to(DOWN * 2.0)
        self.word("s098", "Real", dt=-0.3)
        self.play(tiles2.animate.scale(0.85).move_to(UP * 0.7), FadeIn(qq, scale=0.6), run_time=0.6)
        self.idle(lambda: flipping(cc2), lambda: pulse(qq, 1.1))
        self.until(self.ch["t1"] - 0.55)
        self.idle()
        self.play(FadeOut(VGroup(tiles2, cc2, qq), shift=LEFT * 1.0), run_time=0.5)
        self.finish()
