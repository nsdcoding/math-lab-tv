import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def labelled_box(title, sub, color, w=5.6, h=2.0):
    b = card(w, h, color)
    t = TB(title, 36, color)
    s = T(sub, 26, INK)
    VGroup(t, s).arrange(DOWN, buff=0.25).move_to(b)
    return VGroup(b, t, s)


def star(color=WARN, r=0.14):
    s = Star(5, outer_radius=r, inner_radius=r * 0.45).set_stroke(width=0).set_fill(color, 1)
    s.qa_ignore = True
    return s


def key_icon(color=WARN):
    ring_ = Circle(0.28).set_stroke(color, 6)
    shaft = Line(RIGHT * 0.28, RIGHT * 1.2).set_stroke(color, 6)
    t1 = Line(RIGHT * 0.95, RIGHT * 0.95 + DOWN * 0.25).set_stroke(color, 6)
    t2 = Line(RIGHT * 1.15, RIGHT * 1.15 + DOWN * 0.25).set_stroke(color, 6)
    return VGroup(ring_, shaft, t1, t2)


def folder(label, color=WARN):
    b = RoundedRectangle(corner_radius=0.1, width=2.2, height=0.75).set_stroke(color, 3).set_fill("#22221f", 1)
    b.qa_container = True
    tab = RoundedRectangle(corner_radius=0.06, width=0.7, height=0.22).set_stroke(color, 3).set_fill("#22221f", 1)
    tab.next_to(b, UP, buff=-0.05).align_to(b, LEFT).shift(RIGHT * 0.15)
    tab.qa_joined = True
    t = T(label, 24, color, weight=BOLD).move_to(b)
    return VGroup(tab, b, t)


class S04Boring(Base):
    CHAPTER = "The Boring Explanation"

    def construct(self):
        fr = self.camera.frame
        rng = np.random.default_rng(4)
        # ── s021 a strange place to start: not the exciting idea, the boring one ──
        self.at("s021", 0.0)
        flag = VGroup(Line(DOWN * 0.8, UP * 0.6).set_stroke(INK2, 4),
                      Polygon(UP * 0.6, UP * 0.6 + RIGHT * 0.7 + DOWN * 0.18, UP * 0.24).set_stroke(width=0).set_fill(AQUA, 1))
        start = VGroup(flag, T("start here", 28, AQUA, weight=BOLD).next_to(flag, DOWN, buff=0.15)).move_to(UP * 0.6)
        self.play(FadeIn(flag, shift=DOWN * 0.6), FadeIn(start[1]), run_time=0.6)
        self.play(Wiggle(flag), run_time=0.7)
        ex = labelled_box("something is going on", "what you suspect", ORANGE_).move_to(LEFT * 3.3 + UP * 0.6)
        bo = labelled_box("nothing is going on", "the boring explanation", BLUE_).move_to(RIGHT * 3.3 + UP * 0.6)
        self.word("s021", "Not", dt=-0.3)
        self.play(FadeOut(start, scale=0.5), FadeIn(ex, shift=RIGHT * 0.4), run_time=0.5)
        stars = VGroup(*[star(WARN).move_to(ex[0].get_corner(c) + v) for c, v in
                         ((UL, RIGHT * 0.5 + UP * 0.32), (UR, LEFT * 0.6 + UP * 0.32), (DR, LEFT * 0.4 + DOWN * 0.32), (DL, RIGHT * 0.7 + DOWN * 0.32))])
        self.play(LaggedStart(*[FadeIn(s_, scale=0.2) for s_ in stars], lag_ratio=0.2), run_time=0.5)
        x = pill("not here", RED_, 28).next_to(ex, DOWN, buff=0.3)
        self.word("s021", "suspect", dt=-0.1)
        self.play(FadeIn(x, scale=1.5), ex.animate.set_opacity(0.25), FadeOut(stars), run_time=0.5)
        self.word("s021", "boring", dt=-0.3)
        self.play(FadeIn(bo, shift=LEFT * 0.4), run_time=0.5)
        zz = VGroup(*[T("z", 26 + 6 * k, BLUE_, weight=BOLD) for k in range(3)])
        for k, z in enumerate(zz):
            z.move_to(bo[0].get_corner(UR) + LEFT * 0.5 + UP * (0.38 + 0.38 * k) + RIGHT * 0.32 * k)
        self.play(LaggedStart(*[FadeIn(z, shift=UP * 0.2) for z in zz], lag_ratio=0.3), fr.animate.scale(0.85).move_to(RIGHT * 1.4 + UP * 0.6),
                  run_time=0.9)
        self.idle(lambda: LaggedStart(*[z.animate(rate_func=there_and_back).shift(UP * 0.18) for z in zz], lag_ratio=0.2),
                  lambda: pulse(bo, 1.12))

        # ── s022 the coin is fair: a level balance, heads ½ and tails ½ ──
        self.at("s022", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(ex, zz)), FadeOut(x), fr.animate.restore(), bo.animate.move_to(UP * 2.3), run_time=0.7)
        bs, th, L, R = beam_scale(4.6, INK2)
        bs.move_to(DOWN * 0.6 + LEFT * 2.6)
        hc = coin("H", BLUE_, 0.32); tc = coin("T", BLUE_, 0.32)
        self.word("s022", "fair", dt=-0.3)
        self.play(FadeIn(bs), run_time=0.5)
        hc.add_updater(lambda m: m.move_to(L[0].get_center() + UP * 0.38))
        tc.add_updater(lambda m: m.move_to(R[0].get_center() + UP * 0.38))
        self.play(FadeIn(hc, shift=DOWN * 0.5), th.animate.set_value(0.15), run_time=0.45)
        self.play(FadeIn(tc, shift=DOWN * 0.5), th.animate.set_value(0.0), run_time=0.45)
        half = VGroup(T("heads ½", 30, BLUE_, weight=BOLD), T("tails ½", 30, BLUE_, weight=BOLD))
        self.word("s022", "equally", dt=-0.2)
        half[0].next_to(L[0], DOWN, buff=0.35); half[1].next_to(R[0], DOWN, buff=0.35)
        self.play(FadeIn(half, shift=UP * 0.2), run_time=0.5)
        self.idle(lambda: th.animate(rate_func=there_and_back).set_value(0.08), lambda: th.animate(rate_func=there_and_back).set_value(-0.08))
        self.word("s022", "fifteen", dt=-0.3)
        row = VGroup(*[dot(WARN, 0.13) for _ in range(15)]).arrange_in_grid(3, 5, buff=0.16).move_to(RIGHT * 3.4 + DOWN * 0.2)
        luck = pill("just luck", BLUE_, 30).next_to(row, DOWN, buff=0.4)
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in row], lag_ratio=0.05), run_time=0.8)
        self.play(FadeIn(luck, scale=1.5), run_time=0.4, rate_func=rate_functions.ease_out_cubic)

        # ── s023 its name: the null hypothesis — null means nothing ──
        self.at("s023", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(bs, half, row, luck)), FadeOut(hc), FadeOut(tc), run_time=0.4)
        self.remove(*bs)
        hc.clear_updaters(); tc.clear_updaters()
        self.play(bo.animate.move_to(UP * 0.9), run_time=0.4)
        nh = TB("NULL HYPOTHESIS", 50, BLUE_).next_to(bo, UP, buff=0.35)
        self.word("s023", "called", dt=-0.1)
        self.play(FadeIn(nh, scale=1.6), run_time=0.4, rate_func=rate_functions.ease_out_cubic)
        self.play(ripple(nh.get_center(), BLUE_, r=0.8, scale=3), run_time=0.5)
        nul = T("null", 44, BLUE_, weight=BOLD).move_to(DOWN * 1.2 + LEFT * 1.4)
        eq = T("=", 44, MUTED).next_to(nul, RIGHT, buff=0.35)
        noth = T("nothing", 44, INK, weight=BOLD).next_to(eq, RIGHT, buff=0.35)
        zero = VGroup(Circle(0.32).set_stroke(INK, 5), Line(DL * 0.42, UR * 0.42).set_stroke(INK, 5)).next_to(noth, RIGHT, buff=0.45)
        self.word("s023", "Null", nth=1, dt=-0.2)
        self.play(TransformFromCopy(nh[:4], nul), run_time=0.6)
        self.play(FadeIn(eq), FadeIn(noth, shift=LEFT * 0.3), run_time=0.4)
        self.play(Create(zero), run_time=0.5)
        d0 = defcard(r"H_0", "nothing special is going on", BLUE_, fs=30).move_to(DOWN * 1.2)
        self.word("s023", "special", dt=-0.4)
        self.play(FadeOut(VGroup(nul, eq, noth, zero), shift=UP * 0.2), FadeIn(d0, shift=UP * 0.2), run_time=0.5)
        self.idle(lambda: pulse(d0, 1.12), lambda: pulse(bo, 1.1))

        # ── s024 the alternative: the coin favours heads ──
        self.at("s024", 0.0)
        self.idle()
        d1 = defcard(r"H_1", "alternative: the coin favours heads", ORANGE_, fs=30).next_to(d0, DOWN, buff=0.3)
        tilt = coin("H", ORANGE_, 0.42).next_to(d1, RIGHT, buff=0.4)
        self.play(FadeIn(d1, shift=LEFT * 1.0), run_time=0.5)
        self.word("s024", "heads", dt=-0.3)
        self.play(FadeIn(tilt, scale=0.5), run_time=0.4)
        self.idle(lambda: tilt.animate(rate_func=there_and_back).rotate(-0.6), lambda: pulse(d1, 1.12))

        # ── s025 the key idea: don't prove H1 — pretend H0, ask how surprising ──
        self.at("s025", 0.0)
        self.idle()
        k = key_icon().move_to(UP * 2.8 + RIGHT * 4.6)
        self.play(FadeOut(nh, shift=UP * 0.3), FadeIn(k, shift=LEFT * 0.6), run_time=0.5)
        self.play(Rotate(k, -PI / 8, about_point=k[0].get_center()), run_time=0.5)
        self.word("s025", "prove", dt=-0.2)
        self.play(VGroup(bo, d0, d1).animate.shift(UP * 0.95), FadeOut(tilt), run_time=0.35)
        xx = pill("not proved directly", RED_, 26).next_to(d1, DOWN, buff=0.22)
        self.play(FadeIn(xx, scale=1.5), d1.animate.set_opacity(0.35), run_time=0.5)
        self.word("s025", "pretend", dt=-0.3)
        stamp = pill("SUPPOSE IT'S TRUE", BLUE_, 30).rotate(4 * DEGREES).next_to(d0, DOWN, buff=0.35)
        self.play(FadeOut(VGroup(d1, xx)), FadeOut(k), run_time=0.3)
        self.play(FadeIn(stamp, scale=1.8), run_time=0.4, rate_func=rate_functions.ease_out_cubic)
        self.play(ripple(stamp.get_center(), BLUE_, r=0.5, scale=3), run_time=0.5)
        self.word("s025", "surprising", dt=-0.4)
        self.play(FadeOut(d0), stamp.animate.next_to(bo, DOWN, buff=0.3), run_time=0.3)
        gz, ang = speedometer()
        gz.move_to(DOWN * 1.25)
        self.play(VGroup(bo, stamp).animate.shift(UP * 0.5), run_time=0.3)
        self.play(FadeIn(gz, shift=UP * 0.3), run_time=0.4)
        self.play(ang.animate(rate_func=rate_functions.ease_out_back).set_value(PI * 0.12), run_time=1.0)
        self.idle(lambda: ang.animate(rate_func=there_and_back).set_value(PI * 0.3), lambda: pulse(stamp, 1.12))

        # ── s026 a courtroom ──
        self.at("s026", 0.0)
        self.idle()
        court = sticker("assets/courtroom.png", 2.4).move_to(UP * 1.25)
        gz.needle.clear_updaters()
        # images drawn partly off-frame glitch in Manim: slide in from just inside the frame while fading in
        self.play(FadeOut(VGroup(bo, stamp, gz), shift=LEFT * 3), FadeIn(court, shift=LEFT * 2.5), run_time=0.8)
        inn = pill("presumed innocent", BLUE_, 30).move_to(LEFT * 3.4 + DOWN * 0.9)
        self.word("s026", "presumed", dt=-0.2)
        self.play(FadeIn(inn, shift=UP * 0.3), ripple(court.get_right() + LEFT * 0.4 + UP * 0.2, BLUE_, r=0.3, scale=4), run_time=0.6)
        fs_ = VGroup(*[folder(f"evidence {c}") for c in "ABC"]).arrange(DOWN, buff=0.3).move_to(RIGHT * 4.3 + DOWN * 0.6)
        fs_.shift(UP * 0.25)
        self.word("s026", "prosecution", dt=-0.2)
        self.play(LaggedStart(*[FadeIn(f, shift=LEFT * 0.8) for f in fs_], lag_ratio=0.35), run_time=1.1)
        self.word("s026", "hard", dt=-0.2)
        self.play(LaggedStart(*[pulse(f, 1.1) for f in fs_], lag_ratio=0.2), Wiggle(inn), run_time=0.9)
        self.idle(lambda: pulse(inn, 1.14), lambda: LaggedStart(*[pulse(f, 1.14) for f in fs_], lag_ratio=0.2))

        # ── s027 mapping: innocent = H0 (fair coin), evidence = 15 heads ──
        self.at("s027", 0.0)
        self.idle()
        m1 = pill("= H₀: the fair coin", BLUE_, 28).next_to(inn, DOWN, buff=0.3)
        fc = coin("H", BLUE_, 0.3).next_to(m1, LEFT, buff=0.25)
        self.play(FadeIn(m1, shift=DOWN * 0.2), FadeIn(fc, scale=0.5), run_time=0.5)
        self.play(flipping(fc), run_time=0.4)
        ev = pill("= our 15 heads", WARN, 28).move_to(fs_.get_center())
        strip15 = VGroup(*[dot(WARN, 0.09) for _ in range(15)]).arrange(RIGHT, buff=0.06).next_to(ev, DOWN, buff=0.3)
        self.word("s027", "fifteen", dt=-0.4)
        self.play(ReplacementTransform(fs_, ev), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in strip15], lag_ratio=0.05), run_time=0.6)
        self.idle(lambda: pulse(ev, 1.14), lambda: pulse(m1, 1.12))
        self.until(SEGS["s027"]["end"] + 0.3)
        self.idle()
        self.play(FadeOut(Group(court, inn, m1, fc, ev, strip15), shift=LEFT * 1.5), run_time=0.5)
        self.finish()
