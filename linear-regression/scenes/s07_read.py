import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


class S07Read(Base):
    CHAPTER = "Reading the Line"

    def construct(self):
        fr = self.camera.frame
        axg = lesson_axes(); ax = axg.ax
        dots = house_dots(ax)
        best = price_line(ax, *BEST, 0, 3500)

        # ── s074 the equation ──
        self.at("s074", 0.0)
        eq = VGroup(T("price", 40, INK, weight=BOLD), T("=", 40, MUTED), T("50", 40, VIOLET, weight=BOLD),
                    T("+", 40, MUTED), T("10", 40, VIOLET, weight=BOLD), T("×  size", 40, INK, weight=BOLD)).arrange(RIGHT, buff=0.25)
        eq.move_to(UP * 1.2)
        un = T("price in $ thousands  ·  size in hundreds of sq ft", 26, MUTED).next_to(eq, DOWN, buff=0.35)
        self.play(FadeIn(eq, shift=UP * 0.2), run_time=0.8)
        self.until(word_time("s074", word_index("s074", "thousands")))
        self.play(FadeIn(un), run_time=0.5)

        # ── s075 in plain dollars ──
        self.at("s075", 0.0)
        pd = VGroup(T("$50,000", 44, VIOLET, weight=BOLD), T("+", 44, MUTED), T("$100 per sq ft", 44, VIOLET, weight=BOLD)).arrange(RIGHT, buff=0.3)
        pd.next_to(un, DOWN, buff=0.6)
        self.play(FadeIn(pd[0]), run_time=0.5)
        self.until(word_time("s075", word_index("s075", "plus")))
        self.play(FadeIn(pd[1:]), run_time=0.6)

        # ── s076 the slope: +100 sq ft → +$10k (zoomed) ──
        self.at("s076", 0.0)
        self.play(FadeOut(VGroup(eq, un, pd)), run_time=0.4)
        self.play(FadeIn(axg), FadeIn(dots), Create(best), run_time=0.8)
        x0 = 1750
        run_l = Line(ax.c2p(x0, 50 + 0.1 * x0), ax.c2p(x0 + 100, 50 + 0.1 * x0), color=WARN, stroke_width=3)
        rise_l = Line(ax.c2p(x0 + 100, 50 + 0.1 * x0), ax.c2p(x0 + 100, 50 + 0.1 * (x0 + 100)), color=VIOLET, stroke_width=3)
        rl = T("+100 sq ft", 9, WARN, weight=BOLD).next_to(run_l, DOWN, buff=0.04)
        ri = T("+$10k", 9, VIOLET, weight=BOLD).next_to(rise_l, RIGHT, buff=0.04)
        self.until(word_time("s076", word_index("s076", "every")))
        self.play(FadeOut(VGroup(axg.labs, axg.xt, axg.yt)), fr.animate.scale(0.13).move_to(run_l.get_center() + UP * 0.05), run_time=1.3)
        self.play(Create(run_l), FadeIn(rl), run_time=0.6)
        self.play(Create(rise_l), FadeIn(ri), run_time=0.6)

        # ── s077 a rate, same everywhere ──
        self.at("s077", 0.0)
        self.play(fr.animate.restore(), FadeOut(VGroup(run_l, rise_l, rl, ri)), FadeIn(VGroup(axg.labs, axg.xt, axg.yt)), run_time=1.0)
        tris = VGroup()
        for x in (1000, 2500):
            y = 50 + 0.1 * x
            tris.add(VGroup(Line(ax.c2p(x, y), ax.c2p(x + 500, y), color=WARN, stroke_width=3),
                            Line(ax.c2p(x + 500, y), ax.c2p(x + 500, y + 50), color=VIOLET, stroke_width=3)))
        rate = VGroup(T("a rate:", 30, INK2), T("$100 per sq ft", 34, VIOLET, weight=BOLD),
                      T("same everywhere on the line", 24, INK)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        rate.move_to([2.3, 1.6, 0], aligned_edge=LEFT)
        self.play(Create(tris[0]), FadeIn(rate[:2]), run_time=0.7)
        self.play(TransformFromCopy(tris[0], tris[1]), FadeIn(rate[2]), run_time=0.9)
        mu = pill("the most useful number", WARN, 24).move_to([2.3, -0.2, 0], aligned_edge=LEFT)
        self.until(word_time("s077", word_index("s077", "single")))
        self.play(FadeIn(mu, shift=UP * 0.2), run_time=0.5)

        # ── s078 the intercept ──
        self.at("s078", 0.0)
        self.play(FadeOut(VGroup(tris, rate, mu)), run_time=0.4)
        seg_ = Line(ax.c2p(0, 50), ax.c2p(1000, 150), color=VIOLET, stroke_width=5)
        dash = DashedLine(ax.c2p(0, 50), ax.c2p(1000, 150), color=VIOLET, stroke_width=5)
        icp = Dot(ax.c2p(0, 50), radius=0.14, color=VIOLET).set_stroke(INK, 2); icp.qa_dot = True
        self.until(word_time("s078", word_index("s078", "crosses")))
        self.play(Flash(icp, color=VIOLET, line_length=0.2), FadeIn(icp, scale=0.4), run_time=0.7)
        il = VGroup(T("0 sq ft", 28, INK), T("→  $50k ?", 28, VIOLET, weight=BOLD)).arrange(RIGHT, buff=0.2)
        il.move_to([2.3, 0.9, 0], aligned_edge=LEFT)
        self.play(FadeIn(il), run_time=0.5)

        # ── s079 that house does not exist ──
        self.at("s079", 0.0)
        no = T("not a real house", 30, RED_, weight=BOLD).next_to(il, DOWN, buff=0.35).align_to(il, LEFT)
        st = T("just a starting point", 28, INK).next_to(no, DOWN, buff=0.2).align_to(il, LEFT)
        qm = T("?", 40, RED_, weight=BOLD).next_to(icp, UR, buff=0.12)
        self.play(FadeIn(no), FadeIn(qm), run_time=0.5)
        self.until(word_time("s079", word_index("s079", "starting")))
        self.play(FadeIn(st), run_time=0.5)

        # ── s080 your house: 1,800 sq ft ──
        self.at("s080", 0.0)
        self.play(FadeOut(VGroup(il, no, st, qm, icp)), run_time=0.4)
        vm = DashedLine(ax.c2p(1800, 0), ax.c2p(1800, 230), color=INK2, stroke_width=3)
        vl = T("your house: 1,800 sq ft", 28, INK).move_to([2.3, 2.3, 0], aligned_edge=LEFT)
        self.play(Create(vm), FadeIn(vl), run_time=0.7)

        # ── s081 50 + 10 × 18 = 230 ──
        self.at("s081", 0.0)
        ar = T("50 + 10 × 18 = 230", 36, INK, weight=BOLD).move_to([2.3, 1.4, 0], aligned_edge=LEFT)
        self.play(Write(ar), run_time=1.4)
        hz = DashedLine(ax.c2p(1800, 230), ax.c2p(0, 230), color=VIOLET, stroke_width=3)
        pin = Dot(ax.c2p(1800, 230), radius=0.13, color=VIOLET).set_stroke(INK, 2); pin.qa_dot = True
        ans = pill("$230k", VIOLET, 44).move_to([2.3, 0.4, 0], aligned_edge=LEFT)
        self.until(word_time("s081", word_index("s081", "two")))
        self.play(FadeIn(pin, scale=0.4), Create(hz), run_time=0.7)
        self.play(FadeIn(ans, scale=0.7), run_time=0.5)
        self.play(ans.animate.scale(1.1), rate_func=there_and_back, run_time=0.6)

        # ── s082 the agents ──
        self.at("s082", 0.0)
        aA = Dot(ax.c2p(1800, 260), radius=0.1, color=ORANGE_); bB = Dot(ax.c2p(1800, 200), radius=0.1, color=BLUE_)
        aA.qa_dot = bB.qa_dot = True
        la = T("A $260k", 22, ORANGE_, weight=BOLD).next_to(aA, LEFT, buff=0.15)
        lb = T("B $200k", 22, BLUE_, weight=BOLD).next_to(bB, RIGHT, buff=0.15)
        self.play(FadeIn(aA), FadeIn(la), run_time=0.5)
        self.until(word_time("s082", word_index("s082", "second")))
        self.play(FadeIn(bB), FadeIn(lb), run_time=0.5)
        why = T("now you can show why", 28, INK).next_to(ans, DOWN, buff=0.4).align_to(ans, LEFT)
        self.until(word_time("s082", word_index("s082", "now")))
        self.play(FadeIn(why), run_time=0.5)

        # ── s082a test on 2,500 sq ft ──
        self.at("s082a", 0.0)
        self.play(FadeOut(VGroup(aA, bB, la, lb, why, vm, hz, pin, ar, ans, vl)), run_time=0.5)
        vm2 = DashedLine(ax.c2p(2500, 0), ax.c2p(2500, 300), color=INK2, stroke_width=3)
        g2 = Circle(radius=0.12, color=VIOLET, stroke_width=4).set_fill(BG, 1).move_to(ax.c2p(2500, 300)); g2.qa_dot = True
        t1 = T("2,500 sq ft", 28, INK).move_to([2.3, 2.3, 0], aligned_edge=LEFT)
        t2 = T("50 + 10 × 25 = 300", 32, VIOLET, weight=BOLD).next_to(t1, DOWN, buff=0.3).align_to(t1, LEFT)
        self.play(Create(vm2), FadeIn(t1), run_time=0.6)
        self.until(word_time("s082a", word_index("s082a", "fifty")))
        self.play(Write(t2), FadeIn(g2, scale=0.4), run_time=1.0)

        # ── s082b sold for 280: miss −20 ──
        self.at("s082b", 0.0)
        t3 = T("sold for $280k", 30, INK, weight=BOLD).next_to(t2, DOWN, buff=0.3).align_to(t1, LEFT)
        self.play(FadeIn(t3), Indicate(dots[3], color=WARN, scale_factor=1.6), run_time=0.7)
        bar = miss_bar(ax, 2500, 280, *BEST)
        self.add(bar); self.bring_to_front(g2, dots)
        ml = T("−20", 26, BLUE_, weight=BOLD).next_to(bar, RIGHT, buff=0.15)
        self.until(word_time("s082b", word_index("s082b", "twenty")))
        self.play(Create(bar), FadeIn(ml), run_time=0.6)
        same = pill("the same miss as before", ORANGE_, 24).next_to(t3, DOWN, buff=0.4).align_to(t1, LEFT)
        self.until(word_time("s082b", word_index("s082b", "same")))
        self.play(FadeIn(same, shift=UP * 0.2), run_time=0.5)

        # ── s083 give or take ──
        self.at("s083", 0.0)
        self.play(FadeOut(VGroup(vm2, g2, t1, t2, t3, bar, ml, same)), run_time=0.5)
        band = Polygon(ax.c2p(0, 70), ax.c2p(3500, 420 if False else 420), ax.c2p(3500, 380), ax.c2p(0, 30),
                       stroke_width=0, fill_color=VIOLET, fill_opacity=0.18)
        band = Polygon(ax.c2p(0, 70), ax.c2p(3300, 400), ax.c2p(3500, 400), ax.c2p(3500, 380), ax.c2p(0, 30),
                       stroke_width=0, fill_color=VIOLET, fill_opacity=0.18)
        band.qa_ignore = True  # translucent band, text never sits on it
        self.add(band); self.bring_to_front(best, dots)
        self.until(word_time("s083", word_index("s083", "up")))
        self.play(FadeIn(band), run_time=0.8)
        gt = VGroup(T("$230k", 40, VIOLET, weight=BOLD), T("give or take about $20k", 28, INK),
                    T("a centre, not a promise", 26, MUTED)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        gt.move_to([2.3, 1.3, 0], aligned_edge=LEFT)
        vm3 = DashedLine(ax.c2p(1800, 0), ax.c2p(1800, 250), color=INK2, stroke_width=3)
        self.until(word_time("s083", word_index("s083", "treat")))
        self.play(Create(vm3), FadeIn(gt), run_time=0.8)
        self.until(SEGS["s083"]["end"] - 0.1)
        self.play(FadeOut(VGroup(band, gt, vm3)), run_time=0.45)
        self.finish()
