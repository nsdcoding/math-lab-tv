import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def four_legged(kind, color=INK2, s=1.0):
    """Simple line icons of four-legged things (illustration)."""
    sw = 4
    if kind == "table":
        top = Rectangle(width=1.2, height=0.12).set_stroke(color, sw).set_fill(color, 0.6).move_to(UP * 0.3)
        legs = VGroup(*[Line([x, 0.24, 0], [x, -0.35, 0]) for x in (-0.5, -0.25, 0.25, 0.5)]).set_stroke(color, sw)
        g = VGroup(top, legs)
    elif kind == "chair":
        seat = Rectangle(width=0.7, height=0.1).set_stroke(color, sw).set_fill(color, 0.6)
        back = Line([0.33, 0.05, 0], [0.33, 0.65, 0]).set_stroke(color, sw)
        legs = VGroup(*[Line([x, -0.05, 0], [x, -0.5, 0]) for x in (-0.3, -0.12, 0.12, 0.3)]).set_stroke(color, sw)
        g = VGroup(seat, back, legs)
    else:
        L = dict(dog=(0.9, 0.38, 0.22), cat=(0.8, 0.3, 0.2), cow=(1.25, 0.55, 0.28), horse=(1.15, 0.45, 0.25))[kind]
        bw, bh, hr = L
        body = RoundedRectangle(corner_radius=bh / 2.2, width=bw, height=bh).set_stroke(color, sw).set_fill(color, 0.25)
        head = Circle(hr).set_stroke(color, sw).set_fill(color, 0.25)
        if kind == "horse":
            head.next_to(body, UP + LEFT, buff=-0.08).shift(UP * 0.18)
        else:
            head.next_to(body, LEFT, buff=-0.08).shift(UP * 0.22)
        lx = [-bw / 2 + 0.12, -bw / 2 + 0.28, bw / 2 - 0.28, bw / 2 - 0.12]
        legh = 0.42 if kind in ("horse", "cow") else 0.3
        legs = VGroup(*[Line(body.get_bottom() + RIGHT * x + UP * 0.05, body.get_bottom() + RIGHT * x + DOWN * legh)
                        for x in lx]).set_stroke(color, sw)
        extra = VGroup()
        if kind == "dog":
            extra.add(Line(body.get_right() + UP * 0.05, body.get_right() + UR * 0.28).set_stroke(color, sw))   # tail up
            extra.add(Triangle().scale(0.09).set_stroke(color, sw).set_fill(color, 0.6).next_to(head, UP, buff=-0.05).shift(RIGHT * 0.08))
        if kind == "cat":
            extra.add(ArcBetweenPoints(body.get_right(), body.get_right() + UP * 0.45 + RIGHT * 0.15, angle=-PI / 2).set_stroke(color, sw))
            extra.add(*[Triangle().scale(0.07).set_stroke(color, sw).set_fill(color, 0.6).next_to(head, UP, buff=-0.04).shift(RIGHT * dx)
                        for dx in (-0.09, 0.09)])
        if kind == "cow":
            extra.add(*[Arc(radius=0.1, start_angle=0, angle=PI).set_stroke(color, sw).next_to(head, UP, buff=-0.02).shift(RIGHT * dx)
                        for dx in (-0.12, 0.12)])
            extra.add(*[Circle(0.08).set_stroke(width=0).set_fill(color, 0.7).move_to(body.get_center() + v)
                        for v in (LEFT * 0.2 + UP * 0.05, RIGHT * 0.25 + DOWN * 0.08)])
        if kind == "horse":
            extra.add(Line(body.get_right(), body.get_right() + DR * 0.3).set_stroke(color, sw))
            extra.add(Line(head.get_right() + DOWN * 0.05, body.get_left() + UP * 0.15 + RIGHT * 0.1).set_stroke(color, sw))
        g = VGroup(body, head, legs, extra)
    g.scale(s)
    g.kind = kind
    return g


def hmeter(frac_, color, w=4.6, label=""):
    track = RoundedRectangle(corner_radius=0.12, width=w, height=0.3).set_stroke(INK2, 2).set_fill("#22221f", 1)
    fill = RoundedRectangle(corner_radius=0.12, width=max(w * frac_, 0.24), height=0.3).set_stroke(width=0).set_fill(color, 0.95)
    fill.align_to(track, LEFT)
    for m in (track, fill):
        m.qa_ignore = True
    lab = T(label, 26, color, weight=BOLD).next_to(track, RIGHT, buff=0.25)
    g = VGroup(track, fill, lab); g.track, g.fill, g.lab = track, fill, lab
    return g


CROWD = ["dog", "cat", "cow", "table", "horse", "chair",
         "cat", "horse", "dog", "chair", "cow", "cat",
         "table", "cow", "cat", "horse", "table", "dog",
         "chair", "cat", "cow", "table", "horse", "cat"]


class S04Swap(Base):
    CHAPTER = "Why the Swap Matters"

    def construct(self):
        # ── s026 is it a big deal? ──
        self.at("s026", 0.0)
        hd = TB("is swapping a big deal?", 52, INK).move_to(UP * 1.0)
        self.play(FadeIn(hd, shift=UP * 0.3), run_time=0.6)
        self.word("s026", "simple")
        tr = pill("try it on something simple", AQUA, 30).next_to(hd, DOWN, buff=0.5)
        self.play(FadeIn(tr, scale=0.7), run_time=0.5)

        # ── s027 P(four legs | dog): almost certain ──
        self.at("s027", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(hd, tr), shift=UP * 0.4), run_time=0.4)
        b1 = cond_box("four legs", "dog", color=ORANGE_, size=34)
        b1.move_to(UP * 2.05).set_x(-0.45 - b1.width / 2)
        self.play(FadeIn(b1, shift=UP * 0.2), run_time=0.5)
        dg = four_legged("dog", ORANGE_, 1.7).move_to(DOWN * 0.7).match_x(b1)
        self.play(FadeIn(dg, shift=RIGHT * 0.4), run_time=0.5)
        m1 = hmeter(0.97, ORANGE_, 2.1, "almost certain")
        m1.move_to(UP * 1.1).align_to(b1, LEFT)
        self.word("s027", "Almost")
        self.play(FadeIn(m1.track), GrowFromEdge(m1.fill, LEFT), FadeIn(m1.lab), run_time=0.8)
        self.idle(lambda: highlight(dg, color=ORANGE_))

        # ── s028 swap it: P(dog | four legs) ──
        self.at("s028", 0.0)
        self.idle()
        b2 = cond_box("dog", "four legs", color=VIOLET, size=34)
        b2.move_to(UP * 2.05).set_x(0.45 + b2.width / 2)
        self.word("s028", "swap")
        self.play(TransformFromCopy(b1, b2), run_time=0.8)
        self.word("s028", "four")
        crowd = VGroup(*[four_legged(k, INK2, 0.34) for k in CROWD])
        crowd.arrange_in_grid(4, 6, buff=(0.34, 0.18)).move_to(DOWN * 0.62).match_x(b2)
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in crowd], lag_ratio=0.04), run_time=1.0)

        # ── s029 cats, cows, horses, the kitchen table ──
        self.at("s029", 0.0)
        dogs = VGroup(*[c for c in crowd if c.kind == "dog"])
        self.play(*[c.animate.set_color(ORANGE_) for c in dogs], run_time=0.5)
        for w, kind in (("Cats", "cat"), ("cows", "cow"), ("horses", "horse"), ("table", "table")):
            self.word("s029", w)
            grp = VGroup(*[c for c in crowd if c.kind == kind])
            self.play(LaggedStart(*[Indicate(c, color=INK, scale_factor=1.25) for c in grp], lag_ratio=0.15), run_time=0.6)
        m2 = hmeter(3 / 24, VIOLET, 2.6, "not very likely")
        m2.move_to(UP * 1.1).align_to(b2, LEFT)
        ill = T("illustration", 22, MUTED).next_to(b2, UP, buff=0.15).align_to(b2, RIGHT)
        self.play(FadeIn(m2.track), GrowFromEdge(m2.fill, LEFT), FadeIn(m2.lab), FadeIn(ill), run_time=0.7)

        # ── s030 same words, wildly different ──
        self.at("s030", 0.0)
        cap = pill("same words, different questions", RED_, 28).move_to(DOWN * 2.35)
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.5)
        self.word("s030", "wildly")
        self.play(Indicate(m1.fill, color=ORANGE_, scale_factor=1.06), Indicate(m2.fill, color=VIOLET, scale_factor=1.3), run_time=0.8)

        # ── s031 the crowd makes the difference ──
        self.at("s031", 0.0)
        self.idle()
        self.play(FadeOut(cap), run_time=0.3)
        others = VGroup(*[c for c in crowd if c.kind != "dog"])
        self.word("s031", "crowd")
        self.play(others.animate.set_color(AQUA), run_time=0.6)
        ev = pill("everything else that fits", AQUA, 26).move_to(DOWN * 2.3).match_x(crowd)
        self.word("s031", "other")
        self.play(FadeIn(ev, shift=UP * 0.2), run_time=0.5)
        self.idle(lambda: LaggedStart(*[Indicate(c, color=AQUA, scale_factor=1.15) for c in others[:6]], lag_ratio=0.1))

        # ── s032 why smart people swap: the arrow only goes one way ──
        self.at("s032", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(b1, b2, dg, m1, crowd, m2, ill, ev)), run_time=0.5)
        gl = pill("guilty", ORANGE_, 40).move_to(LEFT * 3.2 + UP * 0.5)
        mt = pill("match", WARN, 40).move_to(RIGHT * 3.2 + UP * 0.5)
        self.play(FadeIn(gl, shift=RIGHT * 0.3), FadeIn(mt, shift=LEFT * 0.3), run_time=0.5)
        self.word("s032", "story")
        fwd = Arrow(gl.get_right() + UP * 0.25, mt.get_left() + UP * 0.25, buff=0.2, color=INK, stroke_width=6)
        fl = T("guilty → match: yes", 28, INK).next_to(fwd, UP, buff=0.2)
        self.play(GrowArrow(fwd), FadeIn(fl), run_time=0.7)
        self.word("s032", "so")
        bwd = DashedVMobject(Arrow(mt.get_left() + DOWN * 0.25, gl.get_right() + DOWN * 0.25, buff=0.2, color=RED_, stroke_width=6),
                             num_dashes=14)
        bl = T("match → guilty: not so fast", 28, RED_).next_to(bwd, DOWN, buff=0.2)
        self.play(Create(bwd), FadeIn(bl), run_time=0.8)
        self.idle(lambda: ShowPassingFlash(fwd.copy().set_stroke(WARN, 8), time_width=0.4))

        # ── s033 lots of innocent people fit the evidence too ──
        self.at("s033", 0.0)
        self.idle()
        rng = np.random.default_rng(5)
        pts = [np.array([rng.uniform(-6.2, 6.2), rng.uniform(-2.0, -0.95), 0]) for _ in range(26)]
        pts = [p for p in pts if abs(p[0]) > 0.5][:22]
        crowd2 = VGroup(*[VGroup(dot(BLUE_, 0.13), Circle(0.22).set_stroke(WARN, 3)).move_to(p) for p in pts])
        for c in crowd2:
            c[0].qa_dot = True; c[1].qa_ignore = True
        self.play(FadeOut(bl), run_time=0.3)
        fans = VGroup(*[DashedLine(mt.get_bottom(), c.get_center(), dash_length=0.08).set_stroke(RED_, 1.5, opacity=0.6)
                        for c in crowd2[::3]])
        for f in fans:
            f.qa_ignore = True
        self.word("s033", "easy")
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in crowd2], lag_ratio=0.05), run_time=1.2)
        self.play(Create(fans), run_time=0.6)
        self.word("s033", "innocent")
        lt = pill("innocent people who also match", BLUE_, 28).next_to(fl, UP, buff=0.35)
        self.play(FadeIn(lt, shift=DOWN * 0.2), run_time=0.5)
        self.idle(lambda: LaggedStart(*[Indicate(c[1], color=WARN, scale_factor=1.3) for c in crowd2[:8]], lag_ratio=0.1))

        # ── s034 Sam's crowd: a city of eight million ──
        self.at("s034", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(gl, mt, fwd, fl, bwd, fans, lt, crowd2)), run_time=0.5)
        cells = VGroup(*[Square(0.2, stroke_width=0, fill_color=BLUE_, fill_opacity=0.8) for _ in range(40 * 14)])
        cells.arrange_in_grid(14, 40, buff=0.07).move_to(DOWN * 0.3)
        lab = TB("8,000,000 people", 48, AQUA).next_to(cells, UP, buff=0.35)
        self.word("s034", "city")
        self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.002), FadeIn(lab, shift=DOWN * 0.2), run_time=1.2)
        self.word("s034", "count")
        self.play(Indicate(lab, color=AQUA, scale_factor=1.1), run_time=0.6)
        self.idle(lambda: glint(lab, AQUA))
        self.finish()
