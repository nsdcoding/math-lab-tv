import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

VX = 2.4   # centre of the visual area (right of the mistake list)


def slot(n, text):
    num = TB(str(n), 30, RED_)
    t = T(text, 24, INK, weight=BOLD)
    return VGroup(num, t).arrange(RIGHT, buff=0.25)


class S11Mistakes(Base):
    CHAPTER = "Common Mistakes"

    def construct(self):
        # ── s105 header + empty slots ──
        self.at("s105", 0.0)
        head = T("COMMON MISTAKES", 30, RED_, weight=BOLD).move_to([-6.7, 2.45, 0], aligned_edge=LEFT)
        rule = Line([-6.7, 2.1, 0], [-2.4, 2.1, 0], color=RED_, stroke_width=2)
        self.play(FadeIn(head), Create(rule), run_time=0.6)
        ys = [1.5, 0.75, 0.0, -0.75]
        texts = [(1, "a line on a curve"), (2, "one point pulls the line"), (3, "outside the data, or cause"), ("+", "slanted misses")]
        slots = VGroup(*[slot(n, t).move_to([-6.7, y, 0], aligned_edge=LEFT) for (n, t), y in zip(texts, ys)])
        ghosts = VGroup(*[Line([-6.7, y - 0.2, 0], [-2.6, y - 0.2, 0], color=GRID, stroke_width=2) for y in ys[:3]])
        self.play(Create(ghosts), run_time=0.5)

        # ── s106 mistake one ──
        self.at("s106", 0.0)
        self.play(FadeIn(slots[0], shift=RIGHT * 0.2), ghosts[0].animate.set_stroke(RED_), run_time=0.6)

        # ── s107 the formula always gives a line ──
        self.at("s107", 0.0)
        cax = xy_axes([0, 10, 2], [0, 10, 2], 6.4, 3.5, "hours studied", "test score", x_labels={}, font_size=20, y_vertical=True)
        for l in cax.labs: l.set_opacity(0)
        cax.move_to([VX, 0.0, 0])
        xs = np.linspace(0.8, 9.6, 12)
        ys_ = 9.4 * (1 - np.exp(-xs / 2.3))
        cd = VGroup(*[dot(INK, 0.09).move_to(cax.ax.c2p(x, y)) for x, y in zip(xs, ys_)])
        b, a = np.polyfit(xs, ys_, 1)
        cl = Line(cax.ax.c2p(0.3, a + b * 0.3), cax.ax.c2p(9.9, a + b * 9.9), color=VIOLET, stroke_width=4)
        so = T("shape only", 20, MUTED).move_to(cax.ax.c2p(8.6, 1.0))
        self.play(FadeIn(cax), FadeIn(so), LaggedStart(*[FadeIn(d, scale=0.4) for d in cd], lag_ratio=0.06), run_time=1.0)
        self.until(word_time("s107", word_index("s107", "line,")))
        self.play(Create(cl), run_time=0.7)
        look = pill("always look at the picture first", WARN, 26).move_to([VX, 2.65, 0])
        self.until(word_time("s107", word_index("s107", "So")))
        self.play(FadeIn(look, shift=DOWN * 0.2), run_time=0.5)

        # ── s115a the bend ──
        self.at("s115a", 0.0)
        bars = VGroup()
        for x, y, d in zip(xs, ys_, cd):
            r = y - (a + b * x)
            bars.add(Line(cax.ax.c2p(x, a + b * x), cax.ax.c2p(x, y), color=ORANGE_ if r > 0 else BLUE_, stroke_width=5))
        self.add(bars); self.bring_to_front(cd)
        self.until(word_time("s115a", word_index("s115a", "straight")))
        self.play(LaggedStart(*[Create(b_) for b_ in bars], lag_ratio=0.08), run_time=1.4)
        lo = T("line too low", 22, ORANGE_, weight=BOLD).move_to(cax.ax.c2p(5.0, 9.6))
        hi = T("too high at the ends", 22, BLUE_, weight=BOLD).move_to(cax.ax.c2p(7.6, 6.4))
        self.until(word_time("s115a", word_index("s115a", "too")))
        self.play(FadeIn(lo), run_time=0.4)
        self.until(word_time("s115a", word_index("s115a", "ends.")) - 0.3)
        self.play(FadeIn(hi), run_time=0.4)

        # ── s108 a pattern in the misses ──
        self.at("s108", 0.0)
        pt = pill("a pattern in the misses = the wrong shape", RED_, 24).move_to(look)
        self.play(FadeOut(look), FadeIn(pt, shift=UP * 0.2), run_time=0.5)
        self.play(LaggedStart(*[Indicate(b_, scale_factor=1.1) for b_ in bars], lag_ratio=0.06), run_time=1.6)

        # ── s109 mistake two ──
        self.at("s109", 0.0)
        self.play(FadeOut(VGroup(cax, cd, cl, so, bars, lo, hi, look, pt)), run_time=0.5)
        self.play(FadeIn(slots[1], shift=RIGHT * 0.2), ghosts[1].animate.set_stroke(RED_), run_time=0.6)

        # ── s110 the gold-plated kitchen ──
        self.at("s110", 0.0)
        hax = xy_axes([0, 3500, 500], [0, 600, 100], 6.4, 3.8, "size (square feet)", "price",
                      x_labels={v: k(v) for v in (1000, 2000, 3000)}, font_size=22, y_vertical=True,
                      y_fmt=lambda v: "$0" if v == 0 else f"${v:g}k")
        hax.move_to([VX, -0.05, 0]); ax = hax.ax
        hd = house_dots(ax, r=0.1)
        bl = Line(ax.c2p(0, 50), ax.c2p(3500, 400), color=VIOLET, stroke_width=4)
        self.play(FadeIn(hax), FadeIn(hd), Create(bl), run_time=0.8)
        self.until(word_time("s110", word_index("s110", "sold")))
        ghost = hd[4].copy().set_opacity(0.3)
        self.add(ghost)
        self.play(hd[4].animate.move_to(ax.c2p(3000, 560)).set_color(RED_), run_time=0.9)
        gk = T("$560k", 24, RED_, weight=BOLD).next_to(hd[4], LEFT, buff=0.2)
        self.play(FadeIn(gk), run_time=0.4)

        # ── s111 the line swings ──
        self.at("s111", 0.0)
        big = Square(200 * (ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1]) * 0.45, stroke_color=RED_, stroke_width=3, fill_color=RED_, fill_opacity=0.2)
        big.next_to(hd[4], RIGHT, buff=0.2).shift(DOWN * 0.4)
        self.play(GrowFromPoint(big, big.get_corner(DL)), run_time=0.6)
        nl = Line(ax.c2p(400, 2), ax.c2p(3500, 560), color=RED_, stroke_width=4)
        self.until(word_time("s111", word_index("s111", "huge")))
        self.play(bl.animate.set_stroke(opacity=0.3), Create(nl), run_time=1.0)
        sl = VGroup(T("slope", 24, MUTED), T("$100", 30, VIOLET, weight=BOLD), T("→", 30, MUTED), T("$180 per sq ft", 30, RED_, weight=BOLD)).arrange(RIGHT, buff=0.2)
        sl.move_to([VX, 2.7, 0])
        self.until(word_time("s111", word_index("s111", "slope")))
        self.play(FadeIn(sl), run_time=0.6)

        # ── s112 fair price moves ──
        self.at("s112", 0.0)
        vm = DashedLine(ax.c2p(1800, 0), ax.c2p(1800, 254), color=INK2, stroke_width=3)
        p1 = Dot(ax.c2p(1800, 230), radius=0.09, color=VIOLET); p2 = Dot(ax.c2p(1800, 254), radius=0.09, color=RED_)
        fp = VGroup(T("1,800 sq ft:", 24, INK), T("$230k", 26, VIOLET, weight=BOLD), T("→", 26, MUTED), T("$254k", 26, RED_, weight=BOLD)).arrange(RIGHT, buff=0.18)
        fp.move_to([-6.7, -1.45, 0], aligned_edge=LEFT)
        self.play(Create(vm), FadeIn(p1), run_time=0.5)
        self.play(FadeIn(p2), FadeIn(fp), run_time=0.6)

        # ── s113 the billionaire ──
        self.at("s113", 0.0)
        cb = pill("from: Mean vs Median", MUTED, 24).move_to([-6.7, -2.15, 0], aligned_edge=LEFT)
        self.play(FadeIn(cb, shift=UP * 0.2), run_time=0.5)
        ck = T("check odd points first", 26, WARN, weight=BOLD).move_to([-6.7, -1.45, 0], aligned_edge=LEFT)
        self.until(word_time("s113", word_index("s113", "Check")))
        self.play(FadeOut(fp), FadeIn(ck), run_time=0.5)

        # ── s114 mistake three ──
        self.at("s114", 0.0)
        self.play(FadeOut(VGroup(hax, hd, ghost, bl, nl, big, gk, sl, vm, p1, p2, fp, cb, ck)), run_time=0.5)
        self.play(FadeIn(slots[2], shift=RIGHT * 0.2), ghosts[2].animate.set_stroke(RED_), run_time=0.6)
        c1 = card(3.7, 2.4, color=RED_); c2 = card(3.7, 2.4, color=RED_)
        cards = VGroup(c1, c2).arrange(RIGHT, buff=0.4).move_to([VX, 0.4, 0])
        i1 = VGroup(Rectangle(width=1.4, height=0.9, stroke_width=0, fill_color=RED_, fill_opacity=0.25),
                    DashedLine(LEFT * 1.2 + DOWN * 0.3, RIGHT * 0.7 + UP * 0.4, color=VIOLET, stroke_width=4)).move_to(c1.get_center() + UP * 0.35)
        i1[0].align_to(i1[1], RIGHT)
        t1 = T("far outside the data", 24, INK, weight=BOLD).move_to(c1.get_center() + DOWN * 0.7)
        i2 = VGroup(T("ice cream", 24, INK2), T("→", 30, RED_), T("sunburn", 24, INK2)).arrange(RIGHT, buff=0.15).move_to(c2.get_center() + UP * 0.35)
        x2 = cross(RED_, 0.15).move_to(i2[1])
        for m in x2: m.qa_ignore = True  # deliberate strike-through
        t2 = T("reading it as cause", 24, INK, weight=BOLD).move_to(c2.get_center() + DOWN * 0.7)
        self.until(word_time("s114", word_index("s114", "We")))
        self.play(FadeIn(VGroup(c1, i1, t1), shift=UP * 0.2), FadeIn(VGroup(c2, i2, x2, t2), shift=UP * 0.2), run_time=0.8)
        desc = T("a line describes the dots you have, nothing more", 26, AQUA, weight=BOLD).move_to([VX, -1.6, 0])
        self.until(word_time("s114", word_index("s114", "A")))
        self.play(FadeIn(desc), run_time=0.6)

        # ── s115 bonus ──
        self.at("s115", 0.0)
        self.play(FadeOut(VGroup(c1, i1, t1, c2, i2, x2, t2, desc)), run_time=0.5)
        self.play(FadeIn(slots[3], shift=RIGHT * 0.2), run_time=0.5)
        ln = Line([VX - 2.6, -1.2, 0], [VX + 2.6, 1.4, 0], color=VIOLET, stroke_width=4)
        P = np.array([VX - 0.6, 1.1, 0])
        foot_v = np.array([P[0], ln.get_start()[1] + (P[0] - ln.get_start()[0]) * 0.5, 0])
        v = Line(P, foot_v, color=ORANGE_, stroke_width=6)
        u = (ln.get_end() - ln.get_start()) / np.linalg.norm(ln.get_end() - ln.get_start())
        fp_ = ln.get_start() + np.dot(P - ln.get_start(), u) * u
        sl_ = DashedLine(P, fp_, color=MUTED, stroke_width=4)
        d = dot(INK, 0.13).move_to(P)
        ok = VGroup(check(AQUA, 0.3), T("straight up and down", 24, AQUA, weight=BOLD)).arrange(RIGHT, buff=0.2).move_to([VX - 2.7, 0.85, 0])
        no = VGroup(cross(RED_, 0.18), T("slanted", 24, RED_, weight=BOLD)).arrange(RIGHT, buff=0.2).move_to([VX + 1.8, 2.0, 0])
        self.play(Create(ln), FadeIn(d), run_time=0.6)
        self.until(word_time("s115", word_index("s115", "slanted,")) - 0.2)
        self.play(Create(sl_), FadeIn(no), run_time=0.6)
        self.until(word_time("s115", word_index("s115", "straight")))
        self.play(Create(v), FadeIn(ok), run_time=0.6)
        un = T("always in the units you predict", 26, INK).move_to([VX, -2.1, 0])
        self.until(word_time("s115", word_index("s115", "The")))
        self.play(FadeIn(un), run_time=0.5)
        self.until(SEGS["s115"]["end"] + 0.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.45)
        self.finish()
