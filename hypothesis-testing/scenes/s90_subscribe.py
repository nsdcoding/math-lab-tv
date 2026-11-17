import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def everyday(title, icon_mob, color):
    box = RoundedRectangle(corner_radius=0.18, width=3.15, height=2.6, stroke_color=color, stroke_width=3,
                           fill_color="#22221f", fill_opacity=1)
    box.qa_container = True
    icon_mob.move_to(box.get_center() + UP * 0.5)
    t = T(title, 24, INK, weight=BOLD).move_to(box.get_center() + DOWN * 0.35)
    stamp = T(STAMP, 20, color).move_to(box.get_center() + DOWN * 0.85)
    return VGroup(box, icon_mob, t, stamp)


def cursor():
    c = Polygon([0, 0, 0], [0, -0.62, 0], [0.16, -0.48, 0], [0.28, -0.74, 0], [0.38, -0.69, 0], [0.26, -0.44, 0],
                [0.46, -0.44, 0], color=INK, fill_color=INK, fill_opacity=1, stroke_width=2)
    c.set_stroke(BG, 3)
    c.qa_ignore = True  # the cursor deliberately sits on the button
    return c


def trophy():
    c = Polygon(LEFT * 0.35 + UP * 0.3, RIGHT * 0.35 + UP * 0.3, RIGHT * 0.2 + DOWN * 0.15, LEFT * 0.2 + DOWN * 0.15).set_stroke(WARN, 4)
    hl = Arc(radius=0.14, start_angle=PI / 2, angle=PI).set_stroke(WARN, 4).next_to(c, LEFT, buff=-0.08).shift(UP * 0.1)
    hr = Arc(radius=0.14, start_angle=-PI / 2, angle=PI).set_stroke(WARN, 4).next_to(c, RIGHT, buff=-0.08).shift(UP * 0.1)
    st = Line(c.get_bottom(), c.get_bottom() + DOWN * 0.2).set_stroke(WARN, 4)
    base = Line(LEFT * 0.22, RIGHT * 0.22).set_stroke(WARN, 5).next_to(st, DOWN, buff=0)
    return VGroup(c, hl, hr, st, base)


def slot():
    b = RoundedRectangle(corner_radius=0.08, width=0.95, height=0.6).set_stroke(RED_, 4)
    w = VGroup(*[Square(0.22).set_stroke(RED_, 2) for _ in range(3)]).arrange(RIGHT, buff=0.06).move_to(b)
    lev = VGroup(Line(b.get_right(), b.get_right() + RIGHT * 0.15 + UP * 0.3).set_stroke(RED_, 3), Dot(radius=0.05, color=RED_))
    lev[1].move_to(lev[0].get_end())
    return VGroup(b, w, lev)


def stock():
    pts = [LEFT * 0.45 + DOWN * 0.25, LEFT * 0.2 + DOWN * 0.05, LEFT * 0.05 + DOWN * 0.15, RIGHT * 0.2 + UP * 0.1, RIGHT * 0.45 + UP * 0.3]
    ln = VMobject().set_points_as_corners(pts).set_stroke(AQUA, 4)
    tip = Triangle().scale(0.08).set_stroke(width=0).set_fill(AQUA, 1).rotate(-PI / 5).move_to(pts[-1])
    return VGroup(ln, tip)


def shirt():
    s = Polygon(LEFT * 0.2 + UP * 0.3, LEFT * 0.45 + UP * 0.12, LEFT * 0.32 + DOWN * 0.05, LEFT * 0.22 + UP * 0.02,
                LEFT * 0.22 + DOWN * 0.32, RIGHT * 0.22 + DOWN * 0.32, RIGHT * 0.22 + UP * 0.02, RIGHT * 0.32 + DOWN * 0.05,
                RIGHT * 0.45 + UP * 0.12, RIGHT * 0.2 + UP * 0.3).set_stroke(VIOLET, 4)
    return s


EVERYDAY = [("winning streak", trophy, WARN), ("slot machine", slot, RED_),
            ("stock that doubled", stock, AQUA), ("lucky shirt", shirt, VIOLET)]
STAMP = "real, or chance?"


class S90Subscribe(Base):
    CHAPTER = "Subscribe"

    def construct(self):
        seg_look, seg_sub = self.ch["segs"][:2]   # "Look around your world…", the subscribe line (word for word)
        # ── look around your world ──
        self.at(seg_look, 0.0)
        cards = VGroup(*[everyday(lab, mk(), col) for lab, mk, col in EVERYDAY]).arrange(RIGHT, buff=0.2)
        cards.move_to(UP * 0.5)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.4) for c in cards], lag_ratio=0.2), run_time=1.4)
        self.play(LaggedStart(*[Indicate(c[3], scale_factor=1.15) for c in cards], lag_ratio=0.2), run_time=1.4)
        self.play(LaggedStart(*[Wiggle(c[1]) for c in cards], lag_ratio=0.15), run_time=1.2)
        self.idle(lambda: LaggedStart(*[Wiggle(c[1], scale_value=1.3) for c in cards], lag_ratio=0.15))
        # ── subscribe (word for word) ──
        self.at(seg_sub, 0.0)
        self.idle()
        lg = logo(1.1).move_to(UP * 1.1)
        self.play(FadeOut(cards, shift=UP * 0.4), run_time=0.5)
        self.play(FadeIn(lg, scale=0.9), run_time=0.7)
        btn_box = RoundedRectangle(corner_radius=0.32, width=3.6, height=0.8, stroke_width=0, fill_color=RED_, fill_opacity=1)
        btn_box.qa_container = True
        btn_t = T("SUBSCRIBE", 32, INK, weight=BOLD)
        btn = VGroup(btn_box, btn_t).next_to(lg, DOWN, buff=0.6)
        btn_t.move_to(btn_box)
        self.play(GrowFromCenter(btn), run_time=0.5)
        cur = cursor().move_to(btn.get_center() + RIGHT * 2.6 + DOWN * 1.2, aligned_edge=UL)
        self.add(cur)
        self.until(word_time(seg_sub, word_index(seg_sub, "subscribe")) - 0.4)
        self.play(cur.animate.move_to(btn.get_center() + RIGHT * 0.25 + DOWN * 0.05, aligned_edge=UL), run_time=0.7,
                  rate_func=rate_functions.ease_out_cubic)
        self.play(btn.animate.scale(0.92), cur.animate.scale(0.9), run_time=0.12)
        done_box = btn_box.copy().set_fill("#6b6b66", 1).scale(1 / 0.92)
        done_t = T("SUBSCRIBED  ✓", 30, INK, weight=BOLD).move_to(done_box)
        done = VGroup(done_box, done_t).move_to(btn)
        done_box.qa_container = True
        self.play(ReplacementTransform(btn, done), cur.animate.scale(1 / 0.9), run_time=0.3)
        self.play(cur.animate.shift(RIGHT * 1.6 + DOWN * 1.0).set_opacity(0), run_time=0.6)
        self.remove(cur)
        bt = T("so we can keep building together", 32, INK2).next_to(done, DOWN, buff=0.45)
        self.until(word_time(seg_sub, word_index(seg_sub, "so")) - 0.2)
        self.play(FadeIn(bt, shift=UP * 0.2), run_time=0.6)
        self.idle(lambda: pulse(done, 1.08), lambda: pulse(lg, 1.05))
        self.until(SEGS[seg_sub]["end"] + 0.25)
        self.idle()
        self.play(FadeOut(VGroup(done, bt)), lg.animate.scale(0.42).to_edge(UP, buff=0.32), run_time=0.6)
        self.finish()
