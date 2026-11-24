import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def money(v):
    return "$0" if v == 0 else (f"${v:g}k" if v < 1000 else f"${v / 1000:g}M")


def wide_axes():
    g = xy_axes([0, 11000, 1000], [0, 1200, 200], 9.6, 4.6, "size (square feet)", "price",
                x_labels={v: k(v) for v in range(2000, 11001, 2000)}, font_size=24, y_vertical=True, y_fmt=money)
    g.to_edge(LEFT, buff=0.55).set_y(0.2)
    return g


class S08Extrap(Base):
    CHAPTER = "Prediction vs Extrapolation"

    def construct(self):
        axg = lesson_axes(); ax = axg.ax
        dots = house_dots(ax)
        best = price_line(ax, *BEST, 0, 3500)
        self.add(axg, best, dots)

        # ── s084 inside the data ──
        self.at("s084", 0.0)
        zone = Rectangle(width=ax.c2p(3000, 0)[0] - ax.c2p(1000, 0)[0], height=ax.c2p(0, 400)[1] - ax.c2p(0, 0)[1],
                         stroke_width=0, fill_color=AQUA, fill_opacity=0.14)
        zone.move_to(ax.c2p(2000, 200)); zone.qa_ignore = True
        self.add(zone); self.bring_to_front(best, dots)
        self.play(FadeIn(zone), run_time=0.6)
        zl = T("inside the data", 28, AQUA, weight=BOLD).move_to([2.4, 2.2, 0], aligned_edge=LEFT)
        vm = DashedLine(ax.c2p(1800, 0), ax.c2p(1800, 230), color=INK2, stroke_width=3)
        self.play(FadeIn(zl), Create(vm), run_time=0.6)
        pr = VGroup(T("prediction", 32, AQUA, weight=BOLD), T("(interpolation)", 26, MUTED)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        pr.next_to(zl, DOWN, buff=0.45).align_to(zl, LEFT)
        self.until(word_time("s084", word_index("s084", "Guessing")))
        self.play(FadeIn(pr, shift=UP * 0.2), run_time=0.6)

        # ── s085 a mansion: wide axes ──
        self.at("s085", 0.0)
        wg = wide_axes(); wax = wg.ax
        wdots = VGroup(*[dot(INK, 0.1).move_to(wax.c2p(x, y)) for x, y in HOUSES])
        wzone = Rectangle(width=wax.c2p(3000, 0)[0] - wax.c2p(1000, 0)[0], height=wax.c2p(0, 1200)[1] - wax.c2p(0, 0)[1],
                          stroke_width=0, fill_color=AQUA, fill_opacity=0.14).move_to(wax.c2p(2000, 600))
        wzone.qa_ignore = True
        wline = Line(wax.c2p(0, 50), wax.c2p(3000, 350), color=VIOLET, stroke_width=5)
        self.play(FadeOut(VGroup(zl, pr, vm)), run_time=0.4)
        self.play(ReplacementTransform(axg, wg), ReplacementTransform(dots, wdots), ReplacementTransform(zone, wzone),
                  ReplacementTransform(best, wline), run_time=1.3)
        ext = DashedLine(wax.c2p(3000, 350), wax.c2p(10000, 1050), color=VIOLET, stroke_width=5)
        self.until(word_time("s085", word_index("s085", "Ten")))
        self.play(Create(ext), run_time=1.2)
        mp = Dot(wax.c2p(10000, 1050), radius=0.13, color=VIOLET).set_stroke(INK, 2); mp.qa_dot = True
        ml = pill("10,000 sq ft → $1.05M", VIOLET, 28).move_to(wax.c2p(8600, 90))
        self.until(word_time("s085", word_index("s085", "one")))
        self.play(FadeIn(mp, scale=0.4), FadeIn(ml), run_time=0.6)

        # ── s086 no data there ──
        self.at("s086", 0.0)
        red = Rectangle(width=wax.c2p(11000, 0)[0] - wax.c2p(3300, 0)[0], height=wax.c2p(0, 1200)[1] - wax.c2p(0, 0)[1],
                        stroke_width=0, fill_color=RED_, fill_opacity=0.12).move_to(wax.c2p(7150, 600))
        red.qa_ignore = True
        self.add(red); self.bring_to_front(ext, wline, wdots, mp, ml)
        self.play(FadeIn(red), run_time=0.7)
        nd = T("no data here", 30, RED_, weight=BOLD).move_to(wax.c2p(5000, 1120))
        self.play(FadeIn(nd), run_time=0.5)

        # ── s087 level off, or jump ──
        self.at("s087", 0.0)
        flat = wax.plot(lambda x: 350 + 300 * (1 - np.exp(-(x - 3000) / 2500)), x_range=[3000, 10000], color=MUTED, stroke_width=3)
        jump = wax.plot(lambda x: 350 + 0.1 * (x - 3000) + 0.000012 * (x - 3000) ** 2, x_range=[3000, 8100], color=MUTED, stroke_width=3)
        il = T("illustration", 22, MUTED).move_to(wax.c2p(9700, 470))
        self.play(Create(flat), Create(jump), FadeIn(il), run_time=1.4)
        ex = VGroup(T("extrapolation", 30, RED_, weight=BOLD), T("guessing outside your data", 22, INK2)).arrange(DOWN, buff=0.12)
        ex.move_to(wax.c2p(5600, 265))
        self.until(word_time("s087", word_index("s087", "extrapolation,")) - 0.2)
        self.play(FadeIn(ex, scale=0.8), run_time=0.6)

        # ── s088 the other way: a shed ──
        self.at("s088", 0.0)
        self.play(FadeOut(VGroup(flat, jump, il, ex, ml, mp)), run_time=0.4)
        lz = Rectangle(width=wax.c2p(900, 0)[0] - wax.c2p(0, 0)[0], height=wax.c2p(0, 1200)[1] - wax.c2p(0, 0)[1],
                       stroke_width=0, fill_color=RED_, fill_opacity=0.12).move_to(wax.c2p(450, 600))
        lz.qa_ignore = True
        self.add(lz); self.bring_to_front(wline, wdots)
        sp = Dot(wax.c2p(200, 70), radius=0.12, color=RED_).set_stroke(INK, 2); sp.qa_dot = True
        shed = house_icon(0.7, RED_).move_to(wax.c2p(1600, 760))
        sl = VGroup(T("200 sq ft shed", 26, INK), T("→ $70k ?", 30, RED_, weight=BOLD)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        sl.next_to(shed, RIGHT, buff=0.3)
        arr = Arrow(shed.get_bottom(), sp.get_center(), buff=0.2, color=RED_, stroke_width=3, max_tip_length_to_length_ratio=0.08)
        self.until(word_time("s088", word_index("s088", "shed,")) - 0.3)
        self.play(FadeIn(lz), FadeIn(shed), FadeIn(sl), GrowArrow(arr), FadeIn(sp), run_time=0.9)

        # ── s101a a model only knows its data ──
        self.at("s101a", 0.0)
        self.play(FadeOut(VGroup(shed, sl, arr, sp)), run_time=0.4)
        self.play(LaggedStart(*[Indicate(d, color=WARN, scale_factor=1.8) for d in wdots], lag_ratio=0.2), run_time=1.4)
        kn = pill("a model only knows its data", WARN, 30).move_to(wax.c2p(7000, 250))
        self.until(word_time("s101a", word_index("s101a", "cannot")))
        self.play(FadeIn(kn, shift=UP * 0.2), run_time=0.6)

        # ── s089 trust it where the dots are ──
        self.at("s089", 0.0)
        self.play(FadeOut(kn), red.animate.set_fill(opacity=0.06), lz.animate.set_fill(opacity=0.06),
                  wzone.animate.set_fill(opacity=0.28), run_time=0.8)
        tr = pill("trust it where the dots are", AQUA, 32).move_to(wax.c2p(7000, 250))
        self.play(FadeIn(tr, scale=0.8), run_time=0.5)
        self.until(SEGS["s089"]["end"] + 0.1)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.45)
        self.finish()
