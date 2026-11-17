import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def weight(color=ORANGE_):
    w = Polygon(LEFT * 0.22 + DOWN * 0.18, RIGHT * 0.22 + DOWN * 0.18, RIGHT * 0.14 + UP * 0.14, LEFT * 0.14 + UP * 0.14)
    w.set_stroke(color, 3).set_fill(color, 0.9)
    h = Arc(radius=0.1, start_angle=0, angle=PI).set_stroke(color, 3).next_to(w, UP, buff=0)
    return VGroup(w, h)


def calendar():
    box = card(3.0, 2.7, INK2)
    top = Rectangle(width=3.0, height=0.45).set_stroke(width=0).set_fill(RED_, 1).align_to(box, UP)
    top.qa_joined = True
    days = VGroup(*[Square(0.3).set_stroke(MUTED, 1.5) for _ in range(30)]).arrange_in_grid(5, 6, buff=0.1)
    days.next_to(top, DOWN, buff=0.17)
    return VGroup(box, top, days)


class S01Hook(Base):
    CHAPTER = "The Coffee Coin"

    def construct(self):
        rng = np.random.default_rng(11)
        # ── s001 the café, every morning ──
        self.at("s001", 0.0)
        cafe = sticker("assets/cafe.png", 4.6).move_to(UP * 0.35 + DOWN * 3)
        cafe.set_opacity(0)
        self.play(cafe.animate.shift(UP * 3).set_opacity(1), run_time=0.9, rate_func=rate_functions.ease_out_back)
        cupL = cafe.get_center() + np.array([-0.42, 0.2, 0]); cupR = cafe.get_center() + np.array([0.48, 0.2, 0])
        self.idle(lambda: steam(cupL + rng.uniform(-0.1, 0.1) * RIGHT), lambda: steam(cupR + rng.uniform(-0.1, 0.1) * RIGHT))
        sun = VGroup(Circle(0.32).set_stroke(WARN, 4).set_fill(WARN, 0.9),
                     *[Line(UP * 0.45, UP * 0.62).rotate(a, about_point=ORIGIN).set_stroke(WARN, 4) for a in np.arange(0, TAU, TAU / 8)])
        sun.move_to(LEFT * 5.0 + UP * 1.6)
        self.word("s001", "coffee")
        self.play(FadeIn(sun, shift=UP * 0.6), run_time=0.6)
        self.word("s001", "every", nth=1)
        self.play(Rotate(sun[1:], PI / 2, about_point=sun[0].get_center()), run_time=0.7)
        self.word("s001", "flip")
        c0 = coin("H", BLUE_, 0.3).move_to(cafe.get_center() + np.array([-0.95, 2.75, 0]))
        self.play(FadeIn(c0, shift=UP * 0.5), run_time=0.35)
        self.play(c0.animate.shift(UP * 0.3), flipping(c0), run_time=0.45)
        self.play(c0.animate.shift(DOWN * 0.3), flipping(c0), run_time=0.45)
        who = pill("who pays?", WARN, 32).move_to(RIGHT * 4.6 + UP * 1.4)
        self.word("s001", "who")
        self.play(FadeIn(who, shift=LEFT * 0.4), FadeOut(sun), ripple(who.get_center(), WARN), run_time=0.6)

        # ── s002 their coin; they always call heads ──
        self.at("s002", 0.0)
        self.idle()
        c = coin("H", BLUE_, 0.95).move_to(RIGHT * 9 + UP * 1.0)
        self.play(FadeOut(who), FadeOut(c0), cafe.animate.scale(0.75).move_to(LEFT * 3.4 + UP * 0.2), run_time=0.6)
        self.add(c)
        c0_ = c.copy(); start, end = c.get_center(), RIGHT * 3.4 + UP * 1.0
        self.play(UpdateFromAlphaFunc(c, lambda m, a: m.become(c0_.copy().rotate(2 * TAU * (1 - a)).move_to(start + (end - start) * a))),
                  run_time=0.9, rate_func=smooth)   # the coin rolls in
        ch1 = pill("their coin", INK, 30).next_to(c, DOWN, buff=0.45)
        self.play(FadeIn(ch1, shift=UP * 0.2), run_time=0.4)
        self.idle(lambda: flipping(c))
        self.word("s002", "calls")
        bub = pill("“heads!”", ORANGE_, 34).next_to(ch1, DOWN, buff=0.35)
        self.play(FadeIn(bub, scale=0.6), flipping(c), run_time=0.5)
        self.play(Indicate(c[2], color=ORANGE_, scale_factor=1.3), run_time=0.6)

        # ── s003 a month of flips: calendar, then the tally board ──
        self.at("s003", 0.0)
        self.idle()
        cal = calendar().move_to(RIGHT * 3.4 + UP * 0.6)
        self.play(FadeOut(VGroup(ch1, bub)), FadeOut(c, shift=RIGHT), FadeIn(cal, shift=LEFT * 0.5), run_time=0.5)
        self.play(LaggedStart(*[d.animate.set_fill(WARN, 0.85) for d in cal[2]], lag_ratio=0.08), run_time=1.0)
        nl = NumberLine(x_range=[0, 21, 1], length=11.55, include_tip=False, color=INK2, stroke_width=3,
                        tick_size=0.07).move_to(DOWN * 0.9 + RIGHT * 0.7)
        nums = VGroup(*[T(str(v), 22, INK2).next_to(nl.n2p(v), DOWN, buff=0.16) for v in (1, 5, 10, 15, 20)])
        xt = T("flip number", 24, MUTED).next_to(nums, DOWN, buff=0.2).align_to(nl, RIGHT)
        yH, yT = nl.get_y() + 1.75, nl.get_y() + 0.75
        rowH = T("heads", 26, WARN, weight=BOLD).move_to([nl.n2p(0)[0] - 0.55, yH, 0])
        rowT = T("tails", 26, MUTED, weight=BOLD).move_to([nl.n2p(0)[0] - 0.55, yT, 0])
        guides = VGroup(*[DashedLine(nl.n2p(0.5) + UP * (y - nl.get_y()), nl.n2p(20.5) + UP * (y - nl.get_y()),
                                     color=GRID, stroke_width=2) for y in (yH, yT)])
        for g_ in guides: g_.qa_ignore = True   # faint row guides behind the dots
        dots_ = VGroup(*[dot(WARN if f == "H" else MUTED, 0.17).move_to([nl.n2p(i + 1)[0], yH if f == "H" else yT, 0])
                         for i, f in enumerate(FLIPS)])
        self.word("s003", "Twenty")
        self.play(FadeOut(Group(cafe, cal), shift=UP * 0.4),
                  Create(nl), FadeIn(nums), FadeIn(xt), FadeIn(rowH), FadeIn(rowT), Create(guides), run_time=0.6)
        cnt = ValueTracker(0)
        counter = always_redraw(lambda: T(f"{int(round(cnt.get_value()))} heads of 20", 40, WARN, weight=BOLD)
                                .move_to(UP * 2.75 + RIGHT * 3.0))
        self.add(counter)
        steps = []
        h = 0
        for i, d in enumerate(dots_):
            h += FLIPS[i] == "H"
            steps.append(h)
        # one flip at a time, the counter ticking with each head
        for i, d in enumerate(dots_):
            self.play(FadeIn(d, scale=2.2), cnt.animate.set_value(steps[i]), run_time=0.15)
        counter.clear_updaters()
        self.word("s003", "fifteen")
        self.play(Indicate(counter, color=WARN, scale_factor=1.15), ripple(counter.get_center(), WARN, r=0.6, scale=3),
                  run_time=0.7)

        # ── s004 coffees bought ──
        self.at("s004", 0.0)
        sa = stacks_axes(y_max=15, step=5, x_len=4.6, y_len=3.6, title="coffees bought")
        sa.move_to(RIGHT * 3.4 + UP * 0.15)
        ax = sa.ax
        pitch = ax.c2p(0, 3)[1] - ax.c2p(0, 0)[1]
        def cups(x, n, color):
            g = VGroup()
            x0 = ax.c2p(x, 0)[0] - pitch
            for k in range(n):
                cc = cup(color, 0.5).move_to([x0 + (k % 3) * pitch, ax.c2p(0, 0)[1] + (k // 3 + 0.5) * pitch, 0])
                g.add(cc)
            return g
        you = cups(0.5, 15, WARN); fr_ = cups(1.5, 5, INK2)
        lab_you = T("you: 15", 28, WARN, weight=BOLD).next_to(ax.c2p(0.5, 0), DOWN, buff=0.25)
        lab_fr = T("your friend: 5", 28, INK2, weight=BOLD).next_to(ax.c2p(1.5, 0), DOWN, buff=0.25)
        board = VGroup(nl, nums, xt, rowH, rowT, guides, dots_)
        self.play(board.animate.scale(0.5).move_to(LEFT * 3.25 + UP * 0.5), counter.animate.scale(0.7).move_to(LEFT * 3.0 + UP * 2.1),
                  Create(ax), FadeIn(sa.labs), FadeIn(sa.yt), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.6) for s in you], lag_ratio=0.15), FadeIn(lab_you), run_time=1.3)
        self.word("s004", "friend")
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.6) for s in fr_], lag_ratio=0.2), FadeIn(lab_fr), run_time=0.8)
        self.play(ripple(lab_you.get_center(), WARN, r=0.4, scale=3), run_time=0.5)

        # ── s005 it seemed like luck… then you wonder ──
        self.at("s005", 0.0)
        luck = VGroup(*[check(AQUA, 0.22).next_to(dots_[i], UP, buff=0.08) for i in range(3)])
        self.play(LaggedStart(*[Create(l) for l in luck], lag_ratio=0.3), *[ripple(dots_[i].get_center(), AQUA, r=0.12, scale=4) for i in range(3)],
                  run_time=0.8)
        fl = iter(range(20))
        self.idle(lambda: Indicate(you, color=WARN, scale_factor=1.08), lambda: Indicate(fr_, color=INK, scale_factor=1.1))
        self.word("s005", "random")
        self.play(Wiggle(dots_, scale_value=1.15, rotation_angle=0.02 * TAU), run_time=0.8)
        self.word("s005", "end")
        hi = VGroup(*[ring(Square(0.17).move_to(d), WARN, 3, 0.04) for i, d in enumerate(dots_) if FLIPS[i] == "H"])
        for r in hi: r.qa_ignore = True
        self.play(FadeOut(luck), LaggedStart(*[Create(r) for r in hi], lag_ratio=0.08),
                  LaggedStart(*[Indicate(d, color=WARN, scale_factor=1.6) for i, d in enumerate(dots_) if FLIPS[i] == "H"], lag_ratio=0.1),
                  run_time=1.2)
        bub = VGroup(Ellipse(width=2.2, height=1.0), Circle(0.12), Circle(0.07)).set_stroke(INK2, 3).set_fill("#22221f", 1)
        bub[0].qa_container = True
        for b_ in bub[1:]: b_.qa_joined = True
        bub[1].next_to(bub[0], DOWN + RIGHT * 0.2, buff=0.05); bub[2].next_to(bub[1], DOWN + RIGHT * 0.3, buff=0.05)
        hmm = T("…hmm", 30, INK).move_to(bub[0])
        bubble = VGroup(bub, hmm).move_to(LEFT * 3.4 + DOWN * 1.35)
        hmm.move_to(bub[0])
        self.idle(lambda: Indicate(you, color=WARN, scale_factor=1.03))
        self.word("s005", "wonder", dt=-0.4)
        self.play(FadeIn(bub, scale=0.6), FadeOut(hi), run_time=0.4)
        self.play(Write(hmm), run_time=0.5)
        self.idle(lambda: Wiggle(you, scale_value=1.04, rotation_angle=0.02 * TAU))

        # ── s006 rigged, or just luck? ──
        self.at("s006", 0.0)
        self.idle()
        div = Line(UP * 2.9, DOWN * 2.3, color=GRID, stroke_width=3)
        cl = coin("H", ORANGE_, 1.0).move_to(LEFT * 3.6 + UP * 0.7)
        wt = weight().next_to(cl, RIGHT, buff=0.15).shift(DOWN * 0.5)
        cr = coin("H", BLUE_, 1.0).move_to(RIGHT * 3.6 + UP * 0.7)
        tl = T("rigged?", 40, ORANGE_, weight=BOLD).next_to(cl, DOWN, buff=0.45)
        tr = T("just luck?", 40, BLUE_, weight=BOLD).next_to(cr, DOWN, buff=0.45)
        qm = glow(TB("?", 130, WARN), WARN).move_to(UP * 0.5)
        self.play(FadeOut(VGroup(board, counter, sa, you, fr_, lab_you, lab_fr, bubble), shift=LEFT * 0.6),
                  GrowFromCenter(div), run_time=0.6)
        self.idle(lambda: glint(div, WARN, 6))
        self.word("s006", "rigged", dt=-0.3)
        self.play(FadeIn(cl, shift=RIGHT * 0.4), FadeIn(tl), run_time=0.5)
        self.play(FadeIn(wt, shift=DOWN * 0.8), cl.animate.rotate(-0.15), run_time=0.5, rate_func=rate_functions.ease_out_bounce)
        self.word("s006", "lucky", dt=-0.5)
        self.play(FadeIn(cr, shift=LEFT * 0.4), FadeIn(tr), run_time=0.5)
        self.play(flipping(cr), run_time=0.4)
        self.play(FadeOut(div), FadeIn(qm, scale=0.5), run_time=0.5)

        # ── s007 decide: the slider wavers ──
        self.at("s007", 0.0)
        sl = NumberLine(x_range=[0, 1, 0.25], length=8.0, include_tip=False, color=INK2, stroke_width=4,
                        tick_size=0.08).move_to(DOWN * 1.85)
        l1 = T("just luck", 28, BLUE_, weight=BOLD).next_to(sl.n2p(0), DOWN, buff=0.3)
        l2 = T("rigged", 28, ORANGE_, weight=BOLD).next_to(sl.n2p(1), DOWN, buff=0.3)
        knob = Circle(0.16).set_stroke(BG, 3).set_fill(WARN, 1).move_to(sl.n2p(0.5))
        clock = VGroup(Circle(0.38).set_stroke(INK2, 3), Line(ORIGIN, UP * 0.28).set_stroke(WARN, 4))
        clock.move_to(UP * 2.5)
        hand = clock[1]
        self.play(qm.animate.scale(0.5).move_to(UP * 0.9), FadeIn(sl), FadeIn(l1), FadeIn(l2), FadeIn(knob, scale=0.5),
                  FadeIn(clock), run_time=0.6)
        pos = iter([0.3, 0.72, 0.45, 0.62, 0.5, 0.68, 0.4])
        self.idle(lambda: AnimationGroup(knob.animate.move_to(sl.n2p(next(pos, 0.55))),
                                         Rotate(hand, -TAU / 6, about_point=clock[0].get_center())))

        # ── s008 your gut… but a fair coin can do this ──
        self.at("s008", 0.0)
        self.idle()
        self.word("s008", "gut", dt=-0.2)
        off = pill("something's off", ORANGE_, 28).next_to(sl.n2p(0.85), UP, buff=0.35)
        self.play(knob.animate.move_to(sl.n2p(0.85)), FadeOut(VGroup(tl, tr)), FadeIn(off, shift=UP * 0.2), run_time=0.6)
        self.idle(lambda: AnimationGroup(knob.animate(rate_func=there_and_back).shift(LEFT * 0.7), pulse(off, 1.12)))
        self.word("s008", "But", dt=-0.2)
        self.play(FadeOut(VGroup(cl, wt, qm, sl, l1, l2, knob, off, clock)), cr.animate.move_to(LEFT * 4.2 + UP * 1.2).scale(0.7), run_time=0.6)
        self.idle()
        strip = VGroup(*[Square(0.42).set_stroke(WARN if f == "H" else MUTED, 2.5).set_fill("#22221f", 1) for f in FLIPS])
        strip.arrange(RIGHT, buff=0.08).move_to(DOWN * 0.35)
        lets = VGroup(*[T(f, 22, WARN if f == "H" else MUTED, weight=BOLD).move_to(s) for f, s in zip(FLIPS, strip)])
        for s in strip: s.qa_container = True
        can = T("a fair coin CAN do this", 40, INK, weight=BOLD).move_to(UP * 1.2 + RIGHT * 1.4)
        self.play(FadeIn(can, shift=LEFT * 0.3), run_time=0.5)
        for k in range(20):
            self.play(flipping(cr), FadeIn(strip[k], scale=1.4), FadeIn(lets[k]), run_time=0.17)
        self.word("s008", "impossible", dt=-0.5)
        stamp = pill("unusual, not impossible", AQUA, 32).rotate(4 * DEGREES).move_to(DOWN * 1.65)
        self.play(FadeIn(stamp, scale=1.6), run_time=0.35, rate_func=rate_functions.ease_out_back)
        self.play(ripple(stamp.get_center(), AQUA, r=0.5, scale=4), run_time=0.6)

        # ── s009 how unusual? a heads number line ──
        self.at("s009", 0.0)
        hl = NumberLine(x_range=[0, 20, 1], length=11.0, include_tip=False, color=INK2, stroke_width=3,
                        tick_size=0.08).move_to(DOWN * 0.8)
        hn = VGroup(*[T(str(v), 24, INK2).next_to(hl.n2p(v), DOWN, buff=0.16) for v in range(0, 21, 5)])
        ht = T("heads in 20 flips", 24, MUTED).next_to(hn, DOWN, buff=0.2).align_to(hl, RIGHT)
        self.play(FadeOut(VGroup(cr, can, stamp, lets, strip), shift=UP * 0.5), Create(hl), FadeIn(hn), FadeIn(ht), run_time=0.7)
        pin = marker(hl, 0, WARN, "15", height=1.3, fs=36)
        self.add(pin)
        self.play(pin.animate.shift(hl.n2p(15) - hl.n2p(0)), run_time=1.0, rate_func=smooth)
        self.play(ripple(hl.n2p(15), WARN, r=0.2, scale=5), run_time=0.5)
        zone = Rectangle(width=hl.n2p(20)[0] - hl.n2p(15)[0], height=1.0, stroke_width=0, fill_color=AQUA, fill_opacity=0.12)
        zone.move_to(hl.n2p(17.5) + UP * 0.5)
        zone.qa_ignore = True
        q = VGroup(*[T(w, 36, INK, weight=BOLD) for w in "unusual enough to call it rigged?".split()]).arrange(RIGHT, buff=0.2)
        q.move_to(UP * 2.3)
        self.word("s009", "Unusual", dt=-0.2)
        self.play(FadeIn(zone), run_time=0.3)
        for k, wd in enumerate(q):
            self.play(FadeIn(wd, shift=UP * 0.15), run_time=0.18)
        self.idle(lambda: zone.animate(rate_func=there_and_back).set_fill(opacity=0.32))

        # ── s010 the tool: a magnifier sweeps in, the title grows out of its lens ──
        self.at("s010", 0.0)
        self.idle()
        lens = VGroup(Circle(0.55).set_stroke(INK, 5), Line(ORIGIN, DR * 0.55).set_stroke(INK, 7))
        lens[1].shift(lens[0].point_at_angle(-PI / 4) - lens[1].get_start())
        for x in lens: x.qa_ignore = True   # the magnifier deliberately passes over the 15 label
        lens.move_to(LEFT * 6 + UP * 0.6).set_stroke(opacity=0)
        self.add(lens)
        self.play(lens.animate.move_to(hl.n2p(15) + UP * 0.9 + RIGHT * 0.3).set_stroke(opacity=1), run_time=0.9)
        self.play(lens.animate.shift(RIGHT * 1.6), run_time=0.8, rate_func=there_and_back)
        self.idle(lambda: lens.animate(rate_func=there_and_back).shift(RIGHT * 1.2 + UP * 0.2))
        title = ht_title()
        self.word("s010", "hypothesis", dt=-0.35)
        self.play(FadeOut(VGroup(hl, hn, ht, pin, zone, q)), lens.animate.scale(6).set_stroke(opacity=0), FadeIn(title[0], scale=0.3),
                  run_time=0.8)
        self.idle(lambda: glint(title[0][1], AQUA, 8))
        self.word("s010", "p", dt=-0.3)
        self.play(Write(title[1]), run_time=1.0)
        self.finish()
