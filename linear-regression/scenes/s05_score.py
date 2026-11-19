import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

PX_ = PANEL_X


def sse(a, b):
    return sum((y - (a + b * x)) ** 2 for x, y in HOUSES)


class S05Score(Base):
    CHAPTER = "Scoring a Line"

    def score_box(self, value, color=WARN, title="score"):
        t = T(title, 26, MUTED)
        v = TB(value, 52, color)
        g = VGroup(t, v).arrange(DOWN, buff=0.12)
        box = card(max(3.6, g.width + 0.8), g.height + 0.5, color=color)
        box.move_to(g)
        grp = VGroup(box, g).move_to(RIGHT * PX_ + UP * 2.2)
        grp.val = v
        return grp

    def set_score(self, sb, value, color=WARN, rt=0.5):
        nv = TB(value, 52, color).move_to(sb.val)
        self.play(Transform(sb.val, nv), sb[0].animate.set_stroke(color), run_time=rt)

    def tiles(self, ax, a, b, color=AQUA, y=-0.1, labels=True):
        """One square per house, side = |miss| (same scale for all five; 0.85 x the chart's price scale)."""
        u = 0.85 * (ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1])
        R = [abs(yv - (a + b * xv)) for xv, yv in HOUSES]
        sq, labs, slots = VGroup(), VGroup(), VGroup()
        for r in R:
            s = max(r * u, 0.02)
            sq.add(Square(s, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.35 if r > 0 else 0))
            lab = T(f"{r * r:,.0f}", 20, INK2)
            labs.add(lab)
            slots.add(Rectangle(width=max(s, lab.width if labels else 0.25), height=0.01).set_opacity(0))
        slots.arrange(RIGHT, buff=0.3).move_to(RIGHT * PX_).set_y(y)
        for s_, sl, lab in zip(sq, slots, labs):
            s_.move_to(sl.get_center()).align_to(sl, DOWN)
            lab.next_to(s_, DOWN, buff=0.14).set_x(sl.get_x())
        return VGroup(sq, labs if labels else VGroup())

    def construct(self):
        axg = lesson_axes(); ax = axg.ax
        dots = house_dots(ax)
        # ── final state of the previous scene, faded away ──
        A0, B0 = 170, 0.04
        old_ln = price_line(ax, A0, B0, 0, 3500)
        old_bars = VGroup(*[miss_bar(ax, x, y, A0, B0) for x, y in HOUSES])
        old_tags = VGroup()
        for (x, y), b in zip(HOUSES, old_bars):
            r = y - (A0 + B0 * x)
            old_tags.add(T(f"{'+' if r > 0 else '−'}{abs(r):.0f}", 24, ORANGE_ if r > 0 else BLUE_, weight=BOLD)
                         .next_to(b, LEFT if r > 0 else RIGHT, buff=0.14))
        old_tags[2].set_opacity(0)  # zero miss had no tag
        unit = T("misses in $ thousand", 24, MUTED).move_to(RIGHT * PANEL_X).align_to(UP * 2.3, UP)
        sc0 = pill("total miss  =  ?", WARN, 34).move_to(RIGHT * PANEL_X + UP * 0.6)
        self.add(axg, old_ln, old_bars, dots, old_tags, unit, sc0)

        # ── s033 flat line at the average price ──
        self.at("s033", 0.0)
        self.play(FadeOut(VGroup(old_ln, old_bars, old_tags, unit, sc0)), run_time=0.5)
        flat = price_line(ax, 250, 0, 0, 3500)
        self.until(word_time("s033", word_index("s033", "flat")))
        self.play(Create(flat), run_time=0.8)
        avg = pill("average price = $250k", VIOLET, 28).move_to(RIGHT * PX_ + UP * 2.3)
        self.play(FadeIn(avg, shift=LEFT * 0.2), run_time=0.5)

        # ── s034 callback: mean vs median ──
        self.at("s034", 0.0)
        cb = pill("from: Mean vs Median", MUTED, 24).next_to(avg, DOWN, buff=0.3)
        self.play(FadeIn(cb, shift=UP * 0.2), run_time=0.5)
        self.until(word_time("s034", word_index("s034", "Here")))
        g = glow(flat.copy(), VIOLET, width=22, opacity=0.1)
        self.play(FadeIn(g), run_time=0.6)
        self.play(FadeOut(g), run_time=0.6)

        # ── s035 every house gets the same guess: the misses ──
        self.at("s035", 0.0)
        A, B = 250, 0
        bars = VGroup(*[miss_bar(ax, x, y, A, B) for x, y in HOUSES])
        R = [y - A for x, y in HOUSES]
        tags = VGroup()
        for b, r in zip(bars, R):
            t = T(("+" if r > 0 else ("−" if r < 0 else "")) + f"{abs(r)}", 24, ORANGE_ if r > 0 else (BLUE_ if r < 0 else MUTED), weight=BOLD)
            t.next_to(b, RIGHT if r < 0 else LEFT, buff=0.14) if r != 0 else t.next_to(b, DOWN, buff=0.25)
            tags.add(t)
        self.add(bars); self.bring_to_front(dots)
        self.until(word_time("s035", word_index("s035", "same")))
        self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.15), run_time=1.0)
        self.play(FadeIn(tags, lag_ratio=0.15), run_time=0.8)

        # ── s033a one house at a time ──
        self.at("s033a", 0.0)
        self.until(word_time("s033a", word_index("s033a", "smallest")))
        self.play(Indicate(bars[0], color=BLUE_, scale_factor=1.15), tags[0].animate.scale(1.3), run_time=0.8)
        self.until(word_time("s033a", word_index("s033a", "biggest")))
        self.play(Indicate(bars[4], color=ORANGE_, scale_factor=1.15), tags[4].animate.scale(1.3), run_time=0.8)
        self.play(tags[0].animate.scale(1 / 1.3), tags[4].animate.scale(1 / 1.3), run_time=0.4)

        # ── s036 add the raw misses: zero ──
        self.at("s036", 0.0)
        self.play(FadeOut(VGroup(avg, cb)), run_time=0.4)
        sb = self.score_box("?", title="sum of the misses")
        self.play(FadeIn(sb, shift=LEFT * 0.2), run_time=0.5)
        running = ["−110", "−140", "−140", "−110", "0"]
        words = ["Minus", "minus", "zero,", "plus", "plus"]
        idx = [word_index("s036", "Minus"), None, None, None, None]
        ws = [x.strip(",.").lower() for x in SEGS["s036"]["text"].split()]
        pos, start = [], 0
        for w in ["minus", "minus", "zero", "plus", "plus"]:
            j = ws.index(w, start); pos.append(j); start = j + 1
        for k, (j, val) in enumerate(zip(pos, running)):
            self.until(word_time("s036", j))
            self.play(Indicate(tags[k], scale_factor=1.3), Transform(sb.val, TB(val, 52, WARN).move_to(sb.val)), run_time=0.45)

        # ── s037 zero: a perfect score? ──
        self.at("s037", 0.0)
        self.set_score(sb, "0", RED_)
        pf = T("a perfect score?", 30, RED_, weight=BOLD).next_to(sb, DOWN, buff=0.3)
        self.play(FadeIn(pf), sb.animate.scale(1.08), rate_func=there_and_back, run_time=0.7)

        # ── s038 they cancel out ──
        self.at("s038", 0.0)
        up = VGroup(bars[3], bars[4]); dn = VGroup(bars[0], bars[1])
        self.play(Indicate(up, color=ORANGE_), Indicate(dn, color=BLUE_), run_time=0.9)
        canc = T("+ and − cancel out", 30, RED_, weight=BOLD).next_to(pf, DOWN, buff=0.35)
        self.until(word_time("s038", word_index("s038", "wiped")))
        self.play(FadeIn(canc, shift=UP * 0.2), run_time=0.5)
        useless = T("plain sum: useless", 30, MUTED).next_to(canc, DOWN, buff=0.3)
        self.until(word_time("s038", word_index("s038", "So")))
        self.play(FadeIn(useless), run_time=0.5)

        # ── s039 square them (callback: standard deviation) ──
        self.at("s039", 0.0)
        self.play(FadeOut(VGroup(sb, pf, canc, useless)), run_time=0.4)
        cb2 = pill("from: Standard Deviation", MUTED, 24).move_to(RIGHT * PX_ + UP * 2.4)
        self.until(word_time("s039", word_index("s039", "The")))
        self.play(FadeIn(cb2, shift=DOWN * 0.2), run_time=0.5)
        mm = pill("miss  ×  miss", AQUA, 36).next_to(cb2, DOWN, buff=0.4)
        self.until(word_time("s039", word_index("s039", "Square")))
        self.play(FadeIn(mm, scale=0.7), run_time=0.5)

        # ── s040 each miss becomes a square ──
        self.at("s040", 0.0)
        tl = self.tiles(ax, A, B, y=-1.7)
        self.play(FadeOut(VGroup(cb2, mm)), run_time=0.3)
        self.play(LaggedStart(*[ReplacementTransform(b.copy(), s_) for b, s_ in zip(bars, tl[0])], lag_ratio=0.2), run_time=1.8)
        self.until(word_time("s040", word_index("s040", "area")))
        self.play(FadeIn(tl[1], lag_ratio=0.15), run_time=0.8)
        ar = T("area = squared miss", 28, AQUA, weight=BOLD).move_to(RIGHT * PX_ + UP * 2.4)
        self.play(FadeIn(ar), run_time=0.4)

        # ── s041 never negative ──
        self.at("s041", 0.0)
        nn = VGroup(T("never negative,", 26, INK), T("so nothing cancels", 26, INK)).arrange(DOWN, buff=0.12).next_to(ar, DOWN, buff=0.3)
        self.play(FadeIn(nn, shift=UP * 0.1), run_time=0.5)
        self.play(*[Indicate(s_, color=AQUA, scale_factor=1.08) for s_ in tl[0][::2]], run_time=0.8)

        # ── s042 / s043 big misses cost more ──
        self.at("s042", 0.0)
        self.play(FadeOut(VGroup(ar, nn)), tl.animate.set_opacity(0.15), run_time=0.5)
        U = 0.055
        big = Square(20 * U, stroke_color=AQUA, stroke_width=3, fill_color=AQUA, fill_opacity=0.35)
        sm1 = Square(10 * U, stroke_color=AQUA, stroke_width=3, fill_color=AQUA, fill_opacity=0.35)
        sm2 = sm1.copy()
        right = VGroup(sm1, sm2).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
        VGroup(big, right).arrange(DOWN, buff=0.75, aligned_edge=LEFT).move_to(RIGHT * (PX_ - 1.6) + UP * 1.05)
        bl = T("one miss of 20", 24, INK2).next_to(big, RIGHT, buff=0.4).align_to(big, UP)
        sl = T("two misses of 10", 24, INK2).next_to(right, RIGHT, buff=0.4).align_to(right, UP).align_to(bl, LEFT)
        self.qa_mute(tl)
        self.until(word_time("s042", word_index("s042", "punishes")))
        self.play(FadeIn(bl), GrowFromEdge(big, DOWN), run_time=0.6)
        self.play(FadeIn(sl), GrowFromEdge(sm1, DOWN), GrowFromEdge(sm2, DOWN), run_time=0.6)
        self.at("s043", 0.0)
        c1 = T("400", 30, WARN, weight=BOLD).next_to(bl, DOWN, buff=0.18).align_to(bl, LEFT)
        c2 = T("100 + 100 = 200", 28, WARN, weight=BOLD).next_to(sl, DOWN, buff=0.18).align_to(sl, LEFT)
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.5)
        self.until(word_time("s043", word_index("s043", "Two")))
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)
        bm = pill("big misses cost more", AQUA, 28).move_to(RIGHT * PX_ + DOWN * 1.6)
        self.until(word_time("s043", word_index("s043", "So")))
        self.play(FadeIn(bm, shift=UP * 0.2), run_time=0.5)

        # ── s044 the score: sum of squared errors ──
        self.at("s044", 0.0)
        self.play(FadeOut(VGroup(big, sm1, sm2, bl, sl, c1, c2, bm)), tl.animate.set_opacity(1), run_time=0.5)
        self.qa_mute(tl, False)
        for s_ in tl[0]:
            s_.set_fill(opacity=0.35 if s_.width > 0.05 else 0)
        sb = self.score_box("?", title="sum of squared errors")
        self.play(FadeIn(sb, shift=LEFT * 0.2), run_time=0.5)
        sm = T("smaller = better", 26, INK).next_to(sb, DOWN, buff=0.25)
        self.until(word_time("s044", word_index("s044", "smaller")))
        self.play(FadeIn(sm), run_time=0.4)

        # ── s045 flat line: 26,000 ──
        self.at("s045", 0.0)
        self.set_score(sb, "26,000")
        self.play(sb.animate.scale(1.08), rate_func=there_and_back, run_time=0.6)
        board = VGroup()

        def board_row(name, val, color):
            r = VGroup(T(name, 24, INK2), T(val, 24, color, weight=BOLD)).arrange(RIGHT, buff=0.3)
            return r
        # ── s046 a line through the cheapest and dearest house ──
        self.at("s046", 0.0)
        A2, B2 = 30, 0.11
        end = price_line(ax, A2, B2, 0, 3500)
        bars2 = VGroup(*[miss_bar(ax, x, y, A2, B2) for x, y in HOUSES])
        tl2 = self.tiles(ax, A2, B2, y=-1.7)
        self.play(FadeOut(tags), FadeOut(sm), run_time=0.3)
        self.until(word_time("s046", word_index("s046", "Here")))
        self.play(Transform(flat, end), Transform(bars, bars2), Transform(tl, tl2), run_time=1.4)
        self.set_score(sb, "?", rt=0.3)

        # ── s047 three houses right on it ──
        self.at("s047", 0.0)
        rings = VGroup(*[Circle(radius=0.22, color=AQUA, stroke_width=4).move_to(dots[i]) for i in (0, 2, 4)])
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.2), run_time=0.9)

        # ── s048 two misses of 25 → 1,250 ──
        self.at("s048", 0.0)
        self.play(FadeOut(rings), *[Indicate(tl[0][i], color=AQUA) for i in (1, 3)], run_time=0.8)
        self.until(word_time("s048", word_index("s048", "score")))
        self.set_score(sb, "1,250")

        # ── s049 too steep ──
        self.at("s049", 0.0)
        self.until(word_time("s049", word_index("s049", "Let")))
        A3, B3 = -50, 0.15
        steep = price_line(ax, A3, B3, 0, 3500)
        self.play(Transform(flat, steep), Transform(bars, VGroup(*[miss_bar(ax, x, y, A3, B3) for x, y in HOUSES])),
                  Transform(tl, self.tiles(ax, A3, B3, y=-1.7)), run_time=1.4)

        # ── s050 7,250 ──
        self.at("s050", 0.0)
        self.set_score(sb, "7,250", RED_)
        tf = T("too steep or too flat: worse", 26, INK).next_to(sb, DOWN, buff=0.25)
        self.until(word_time("s050", word_index("s050", "Too")))
        self.play(FadeIn(tf), run_time=0.5)

        # ── s051 pivot and slide ──
        self.at("s051", 0.0)
        self.play(FadeOut(tf), FadeOut(tl), run_time=0.4)
        piv = VGroup(Arc(radius=0.45, start_angle=PI / 6, angle=4 * PI / 3, color=VIOLET, stroke_width=5).add_tip(tip_length=0.18),
                     T("pivot", 28, VIOLET, weight=BOLD))
        piv[1].next_to(piv[0], DOWN, buff=0.2)
        sld = VGroup(DoubleArrow(UP * 0.55, DOWN * 0.55, color=VIOLET, stroke_width=5, buff=0, tip_length=0.18),
                     T("slide", 28, VIOLET, weight=BOLD))
        sld[1].next_to(sld[0], DOWN, buff=0.2)
        ctl = VGroup(piv, sld).arrange(RIGHT, buff=1.2, aligned_edge=DOWN).move_to(RIGHT * PX_ + DOWN * 0.35)
        self.until(word_time("s051", word_index("s051", "pivot,")))
        self.play(FadeIn(piv, scale=0.7), run_time=0.5)
        self.until(word_time("s051", word_index("s051", "slide,")))
        self.play(FadeIn(sld, scale=0.7), run_time=0.5)

        # ── s052 live pivot about the average house ──
        self.at("s052", 0.0)
        bt = ValueTracker(0.15); da = ValueTracker(0.0)

        def ab():
            b = bt.get_value(); return 250 - b * 2000 + da.get_value(), b
        live_ln = always_redraw(lambda: price_line(ax, *ab(), 0, 3500))
        live_bars = always_redraw(lambda: VGroup(*[miss_bar(ax, x, y, *ab()) for x, y in HOUSES]))
        live_tl = always_redraw(lambda: self.tiles(ax, *ab(), y=-2.45, labels=False))
        live_val = always_redraw(lambda: TB(f"{sse(*ab()):,.0f}", 52, WARN).move_to(sb.val))
        self.remove(flat, bars, sb.val)
        self.add(live_ln, live_bars, live_tl, live_val); self.bring_to_front(dots)
        sb[0].set_stroke(WARN)
        self.play(FadeOut(sld), run_time=0.3)
        self.play(Rotate(piv[0], -PI / 2), bt.animate.set_value(0.04), run_time=2.0, rate_func=smooth)
        self.play(bt.animate.set_value(0.13), run_time=1.6, rate_func=smooth)
        self.play(bt.animate.set_value(0.10), run_time=1.0, rate_func=smooth)

        # ── s053 slide ──
        self.at("s053", 0.0)
        self.play(FadeOut(piv), FadeIn(sld), run_time=0.3)
        self.play(da.animate.set_value(40), run_time=0.9, rate_func=smooth)
        self.play(da.animate.set_value(-40), run_time=1.2, rate_func=smooth)
        self.play(da.animate.set_value(15), run_time=0.7, rate_func=smooth)

        # ── s052a the valley ──
        self.at("s052a", 0.0)
        self.play(FadeOut(sld), run_time=0.3)
        vax = Axes(x_range=[0.04, 0.16, 0.02], y_range=[0, 10000, 2000], x_length=3.6, y_length=1.9,
                   axis_config=dict(color=INK2, stroke_width=2.5, include_tip=False, tick_size=0.04))
        vax.move_to(RIGHT * PX_ + DOWN * 0.15)
        curve = vax.plot(lambda b: sse(250 - b * 2000, b), x_range=[0.04, 0.16], color=WARN, stroke_width=4)
        vx = T("tilt", 22, MUTED).next_to(vax.x_axis, DOWN, buff=0.12).align_to(vax.x_axis, RIGHT)
        vy = T("score", 22, MUTED).next_to(vax.y_axis, UP, buff=0.1).align_to(vax.y_axis, LEFT)
        ill = T("shape only", 20, MUTED).next_to(vax, LEFT, buff=0.15).align_to(vax, UP)
        vdot = always_redraw(lambda: Dot(vax.c2p(bt.get_value(), sse(250 - bt.get_value() * 2000, bt.get_value())), radius=0.09, color=VIOLET))
        self.play(da.animate.set_value(0), Create(vax), FadeIn(vx), FadeIn(vy), FadeIn(ill), run_time=0.8)
        self.play(Create(curve), FadeIn(vdot), run_time=0.8)
        self.until(word_time("s052a", word_index("s052a", "lowest")))
        self.play(bt.animate.set_value(0.15), run_time=0.6)
        self.play(bt.animate.set_value(0.10), run_time=1.2, rate_func=smooth)

        # ── s054 the bottom ──
        self.at("s054", 0.0)
        bot = Dot(vax.c2p(0.10, 1000), radius=0.13, color=VIOLET)
        self.play(Flash(bot, color=VIOLET, line_length=0.2), run_time=0.7)

        # ── s055 the best misses: 1,000 ──
        self.at("s055", 0.0)
        for m in (live_ln, live_bars, live_tl, live_val, vdot):
            m.clear_updaters()
        best_ln = price_line(ax, *BEST, 0, 3500)
        self.remove(live_ln); self.add(best_ln); self.bring_to_front(dots)
        self.play(FadeOut(VGroup(vax, curve, vx, vy, ill, vdot)), FadeOut(live_tl), run_time=0.4)
        tl3 = self.tiles(ax, *BEST, y=-1.6)
        R3 = [y - (BEST[0] + BEST[1] * x) for x, y in HOUSES]
        tags3 = VGroup()
        for b, r in zip(live_bars, R3):
            t = T(("+" if r > 0 else ("−" if r < 0 else "")) + f"{abs(r):.0f}", 24, ORANGE_ if r > 0 else (BLUE_ if r < 0 else MUTED), weight=BOLD)
            t.next_to(b, LEFT if r > 0 else RIGHT, buff=0.14) if r != 0 else t.next_to(dots[2], DOWN, buff=0.25)
            tags3.add(t)
        self.play(FadeIn(tags3, lag_ratio=0.2), run_time=1.2)
        self.until(word_time("s055", word_index("s055", "Squared")))
        self.play(LaggedStart(*[ReplacementTransform(b.copy(), s_) for b, s_ in zip(live_bars, tl3[0])], lag_ratio=0.15),
                  FadeIn(tl3[1]), run_time=1.2)
        self.remove(live_val); sb.val.become(TB("1,000", 52, WARN).move_to(sb.val)); self.add(sb.val)
        self.until(word_time("s055", word_index("s055", "one")))
        self.set_score(sb, "1,000", VIOLET)
        sg = glow(sb[0].copy().set_fill(opacity=0), VIOLET, width=20, opacity=0.08)
        sp = T("the smallest possible", 26, VIOLET).next_to(sb, DOWN, buff=0.25)
        self.play(FadeIn(sg), FadeIn(sp), run_time=0.6)

        # ── s056 least squares; scoreboard ──
        self.at("s056", 0.0)
        self.play(FadeOut(VGroup(tl3, sp, sg)), run_time=0.4)
        rows = VGroup(board_row("flat line", "26,000", INK2), board_row("end to end", "1,250", INK2),
                      board_row("too steep", "7,250", RED_), board_row("least squares", "1,000", VIOLET))
        for i, r in enumerate(rows):
            y = 0.35 - 0.48 * i
            r[0].move_to([PX_ - 1.6, y, 0], aligned_edge=LEFT)
            r[1].move_to([PX_ + 1.6, y, 0], aligned_edge=RIGHT)
        self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in rows], lag_ratio=0.2), run_time=1.2)
        self.until(word_time("s056", word_index("s056", "least")))
        hl = SurroundingRectangle(rows[3], color=VIOLET, buff=0.12, corner_radius=0.1)
        hl.qa_ignore = True  # deliberate highlight box
        lsl = T("least squares line", 30, VIOLET, weight=BOLD).next_to(rows, DOWN, buff=0.45)
        self.play(Create(hl), FadeIn(lsl), run_time=0.6)

        # ── s057 squaring is a choice ──
        self.at("s057", 0.0)
        self.play(FadeOut(VGroup(rows, hl, lsl, tags3)), run_time=0.4)
        ch = T("squaring is a choice", 30, WARN, weight=BOLD).move_to(RIGHT * PX_ + UP * 0.6)
        self.play(FadeIn(ch), run_time=0.4)
        pd = T("plain distances:", 26, INK2)
        r1 = VGroup(T("end to end", 26, INK), T("50", 26, AQUA, weight=BOLD)).arrange(RIGHT, buff=0.4)
        r2 = VGroup(T("least squares", 26, INK), T("60", 26, INK2, weight=BOLD)).arrange(RIGHT, buff=0.4)
        alt = VGroup(pd, r1, r2).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        r1[1].align_to(r2[1], RIGHT)
        ab_ = card(alt.width + 0.6, alt.height + 0.5, color=MUTED).move_to(alt)
        altc = VGroup(ab_, alt).next_to(ch, DOWN, buff=0.35)
        self.until(word_time("s057", word_index("s057", "If")))
        self.play(FadeIn(altc, shift=UP * 0.2), run_time=0.6)
        self.until(word_time("s057", word_index("s057", "end")))
        endl = DashedLine(ax.c2p(0, 30), ax.c2p(3500, 30 + 0.11 * 3500 if 30 + 0.11 * 3500 <= 400 else 400), color=AQUA, stroke_width=3)
        endl = price_line(ax, 30, 0.11, 0, 3500, color=AQUA, width=3)
        self.play(Create(endl), run_time=0.8)

        # ── s058 same choice as mean vs median ──
        self.at("s058", 0.0)
        self.play(FadeOut(VGroup(altc, ch, endl)), run_time=0.4)
        m1 = pill("squared misses  ↔  mean", VIOLET, 26)
        m2 = pill("plain distances  ↔  median", AQUA, 26)
        mm2 = VGroup(m1, m2).arrange(DOWN, buff=0.35).move_to(RIGHT * PX_ + UP * 0.3)
        self.until(word_time("s058", word_index("s058", "Squared")))
        self.play(FadeIn(m1, shift=LEFT * 0.2), run_time=0.5)
        self.until(word_time("s058", word_index("s058", "plain")))
        self.play(FadeIn(m2, shift=LEFT * 0.2), run_time=0.5)
        ok = VGroup(check(AQUA, 0.3), T("one clean formula", 28, INK)).arrange(RIGHT, buff=0.25).next_to(mm2, DOWN, buff=0.45)
        self.until(word_time("s058", word_index("s058", "Squares")))
        self.play(FadeIn(ok), run_time=0.5)
        self.until(SEGS["s058"]["end"] - 0.1)
        self.play(FadeOut(VGroup(mm2, ok, sb)), run_time=0.45)
        self.finish()
