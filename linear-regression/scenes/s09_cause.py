import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def sun(r=0.42):
    c = Circle(radius=r, stroke_width=0, fill_color=WARN, fill_opacity=1)
    rays = VGroup(*[Line(UP * (r + 0.12), UP * (r + 0.32)).rotate(a, about_point=ORIGIN) for a in np.arange(0, TAU, TAU / 10)]).set_stroke(WARN, 4)
    return VGroup(c, rays)


class S09Cause(Base):
    CHAPTER = "A Line Is Not a Cause"

    def construct(self):
        # ── s090 move together ≠ cause ──
        self.at("s090", 0.0)
        warn = T("one big warning", 36, RED_, weight=BOLD).move_to(UP * 2.3)
        self.play(FadeIn(warn, shift=DOWN * 0.2), run_time=0.5)
        mt = VGroup(check(AQUA, 0.35), T("move together", 40, AQUA, weight=BOLD)).arrange(RIGHT, buff=0.3)
        cs = VGroup(cross(RED_, 0.25), T("one causes the other", 40, RED_, weight=BOLD)).arrange(RIGHT, buff=0.3)
        grp = VGroup(mt, cs).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(UP * 0.4)
        self.until(word_time("s090", word_index("s090", "move")))
        self.play(FadeIn(mt, shift=RIGHT * 0.2), run_time=0.6)
        self.until(word_time("s090", word_index("s090", "why.")) - 0.3)
        self.play(FadeIn(cs, shift=RIGHT * 0.2), run_time=0.6)

        # ── s091 houses: common sense, not the line ──
        self.at("s091", 0.0)
        self.play(FadeOut(VGroup(warn, grp)), run_time=0.4)
        axg = lesson_axes(); ax = axg.ax
        dots = house_dots(ax); best = price_line(ax, *BEST, 0, 3500)
        self.play(FadeIn(axg), FadeIn(dots), Create(best), run_time=0.8)
        a1 = VGroup(T("more space → higher price", 24, INK), T("we know it from", 26, MUTED), T("common sense", 32, AQUA, weight=BOLD))
        a1.arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([2.3, 1.6, 0], aligned_edge=LEFT)
        self.play(FadeIn(a1[0]), run_time=0.5)
        nl = T("not proven by the line", 28, RED_, weight=BOLD).next_to(a1[0], DOWN, buff=0.3).align_to(a1, LEFT)
        self.until(word_time("s091", word_index("s091", "But")))
        self.play(FadeIn(nl), run_time=0.5)
        a1[1:].next_to(nl, DOWN, buff=0.3).align_to(a1, LEFT)
        self.until(word_time("s091", word_index("s091", "We")))
        self.play(FadeIn(a1[1:]), run_time=0.5)

        # ── s092 ice cream and sunburn ──
        self.at("s092", 0.0)
        self.play(FadeOut(VGroup(axg, dots, best, a1, nl)), run_time=0.5)
        iax = xy_axes([0, 10, 2], [0, 10, 2], 6.0, 3.8, "ice cream sales", "sunburn cases", x_labels={}, font_size=20, y_vertical=True)
        iax.move_to(LEFT * 2.3 + DOWN * 0.15)
        for l in iax.labs: l.set_opacity(0)
        rng = np.random.default_rng(11)
        xs = np.linspace(1, 9, 12); ys = 0.9 * xs + 0.6 + rng.normal(0, 0.6, 12)
        idots = VGroup(*[dot(INK, 0.09).move_to(iax.ax.c2p(x, y)) for x, y in zip(xs, ys)])
        b, a = np.polyfit(xs, ys, 1)
        il = Line(iax.ax.c2p(0.5, a + b * 0.5), iax.ax.c2p(9.6, a + b * 9.6), color=VIOLET, stroke_width=4)
        tag = T("illustration", 22, MUTED).move_to(iax.ax.c2p(8.4, 1.2))
        self.play(FadeIn(iax), FadeIn(tag), run_time=0.6)
        self.until(word_time("s092", word_index("s092", "Ice")))
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in idots], lag_ratio=0.08), run_time=1.2)
        self.until(word_time("s092", word_index("s092", "lovely")))
        self.play(Create(il), run_time=0.8)

        # ── s093 hot sunny days cause both ──
        self.at("s093", 0.0)
        x_ = cross(RED_, 0.22).move_to(il.get_center() + UP * 0.6 + LEFT * 0.3)
        nc = T("does not cause", 24, RED_, weight=BOLD).next_to(x_, UP, buff=0.12)
        self.play(Create(x_), FadeIn(nc), run_time=0.5)
        s = sun().move_to([4.4, 1.8, 0])
        hd = T("hot sunny days", 28, WARN, weight=BOLD).next_to(s, DOWN, buff=0.25)
        ar1 = Arrow(hd.get_bottom() + LEFT * 0.4, iax.xt.get_right() + RIGHT * 0.15, buff=0.15, color=WARN, stroke_width=4, max_tip_length_to_length_ratio=0.07)
        ar2 = CurvedArrow(s.get_left() + LEFT * 0.1, iax.yt.get_top() + UP * 0.15, angle=0.35, color=WARN, stroke_width=4)
        self.until(word_time("s093", word_index("s093", "Hot")))
        self.play(FadeIn(s, scale=0.6), FadeIn(hd), run_time=0.5)
        self.play(GrowArrow(ar1), Create(ar2), run_time=0.7)
        hc = T("the hidden cause", 26, WARN).next_to(s, UP, buff=0.15)
        self.play(FadeIn(hc), run_time=0.4)

        # ── s094 houses: newer, better area ──
        self.at("s094", 0.0)
        self.play(FadeOut(VGroup(iax, idots, il, tag, x_, nc, s, hd, ar1, ar2, hc)), run_time=0.5)
        sz = pill("size", INK, 34).move_to(LEFT * 3.4 + UP * 0.4)
        pc = pill("price", VIOLET, 34).move_to(RIGHT * 3.4 + UP * 0.4)
        main = Arrow(sz.get_right(), pc.get_left(), buff=0.25, color=INK2, stroke_width=5)
        self.play(FadeIn(sz), FadeIn(pc), GrowArrow(main), run_time=0.7)
        nw = pill("newer?", AQUA, 30).move_to(LEFT * 1.2 + DOWN * 1.4)
        ba = pill("better area?", AQUA, 30).move_to(RIGHT * 1.6 + DOWN * 1.4)
        an = Arrow(nw.get_right(), pc.get_bottom() + LEFT * 0.3, buff=0.2, color=AQUA, stroke_width=4)
        aa = Arrow(ba.get_top(), pc.get_bottom() + RIGHT * 0.1, buff=0.2, color=AQUA, stroke_width=4)
        self.until(word_time("s094", word_index("s094", "newer,")))
        self.play(FadeIn(nw), GrowArrow(an), run_time=0.6)
        self.until(word_time("s094", word_index("s094", "better")))
        self.play(FadeIn(ba), GrowArrow(aa), run_time=0.6)
        sh = T("some of the $100 per sq ft may belong to these", 28, INK).move_to(UP * 2.0)
        self.until(word_time("s094", word_index("s094", "Some")))
        self.play(FadeIn(sh), run_time=0.6)

        # ── s095 later: multiple regression ──
        self.at("s095", 0.0)
        lt = pill("later: multiple regression", MUTED, 28).move_to(DOWN * 2.3 + LEFT * 3.2)
        self.play(FadeIn(lt, shift=UP * 0.2), run_time=0.6)

        # ── s096 how to read the slope ──
        self.at("s096", 0.0)
        self.play(FadeOut(VGroup(sz, pc, main, nw, ba, an, aa, sh, lt)), run_time=0.5)
        c1 = VGroup(check(AQUA, 0.35), T("bigger houses tend to cost more", 34, AQUA, weight=BOLD)).arrange(RIGHT, buff=0.3)
        c2 = VGroup(cross(RED_, 0.24), T("adding a room adds exactly $10k", 34, RED_, weight=BOLD)).arrange(RIGHT, buff=0.3)
        cc = VGroup(c1, c2).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to(UP * 0.4)
        self.play(FadeIn(c1, shift=RIGHT * 0.2), run_time=0.6)
        self.until(word_time("s096", word_index("s096", "Not,")))
        self.play(FadeIn(c2, shift=RIGHT * 0.2), run_time=0.6)
        self.until(SEGS["s096"]["end"] + 0.2)
        self.play(FadeOut(cc), run_time=0.45)
        self.finish()
