import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *


def everyday(title, icon_mob, color):
    box = RoundedRectangle(corner_radius=0.18, width=3.0, height=2.6, stroke_color=color, stroke_width=3,
                           fill_color="#22221f", fill_opacity=1)
    box.qa_container = True
    icon_mob.move_to(box.get_center() + UP * 0.5)
    t = T(title, 26, INK, weight=BOLD).move_to(box.get_center() + DOWN * 0.35)
    stamp = T(STAMP, 20, color).move_to(box.get_center() + DOWN * 0.85)
    return VGroup(box, icon_mob, t, stamp)


def cursor():
    c = Polygon([0, 0, 0], [0, -0.62, 0], [0.16, -0.48, 0], [0.28, -0.74, 0], [0.38, -0.69, 0], [0.26, -0.44, 0],
                [0.46, -0.44, 0], color=INK, fill_color=INK, fill_opacity=1, stroke_width=2)
    c.set_stroke(BG, 3)
    c.qa_ignore = True  # the cursor deliberately sits on the button
    return c


EVERYDAY = [("the weather", lambda: ic_cloud(BLUE_, 0.8), BLUE_),
            ("the bus", lambda: ic_bus(WARN, 0.8), WARN),
            ("a quiz", lambda: ic_quiz(INK2, 0.7, 2), AQUA),
            ("a game", lambda: VGroup(die(5, ORANGE_, 0.55), die(2, BLUE_, 0.55)).arrange(RIGHT, buff=0.15), ORANGE_)]
STAMP = "what are the odds?"


class S90Subscribe(PBase):
    CHAPTER = "Subscribe"
    FADE_OUT = False  # the video ends on the logo

    def construct(self):
        seg_look, seg_sub = self.ch["segs"][:2]   # "Look around your world…", the subscribe line (word for word)
        # ── look around your world ──
        self.at(seg_look, 0.0)
        cards = VGroup(*[everyday(lab, mk(), col) for lab, mk, col in EVERYDAY]).arrange(RIGHT, buff=0.3)
        cards.move_to(UP * 0.5)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.4) for c in cards], lag_ratio=0.2), run_time=1.4)
        self.play(LaggedStart(*[Indicate(c[3], scale_factor=1.15) for c in cards], lag_ratio=0.2), run_time=1.4)
        self.play(LaggedStart(*[Wiggle(c[1]) for c in cards], lag_ratio=0.15), run_time=1.2)
        # ── subscribe (word for word) ──
        self.at(seg_sub, 0.0)
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
        # "For more mathematics, explained simply and visually, subscribe…" (owner: no next-time teaser)
        seg_more = self.ch["segs"][2]
        self.at(seg_more, 0.0)
        more = pill("more math, explained simply and visually", AQUA, 34).next_to(lg, DOWN, buff=0.6)
        self.play(FadeOut(VGroup(done, bt)), run_time=0.4)
        self.play(FadeIn(more, shift=UP * 0.2), run_time=0.6)
        self.until(SEGS[seg_more]["end"] + 0.3)
        self.play(FadeOut(more), lg.animate.move_to(UP * 0.2), run_time=0.8)
        self.finish()
