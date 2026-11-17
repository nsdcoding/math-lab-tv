import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def capsule(color, fill=0.9, w=1.1):
    left = RoundedRectangle(corner_radius=0.22, width=w / 2 + 0.2, height=0.44).set_stroke(color, 3).set_fill(color, fill)
    right = RoundedRectangle(corner_radius=0.22, width=w / 2 + 0.2, height=0.44).set_stroke(color, 3).set_fill("#22221f", 1)
    right.next_to(left, RIGHT, buff=-0.4)
    for x in (left, right): x.qa_joined = True
    return VGroup(right, left)


def paper():
    b = RoundedRectangle(corner_radius=0.08, width=1.5, height=1.9).set_stroke(INK2, 3).set_fill("#22221f", 1)
    b.qa_container = True
    lines = VGroup(*[Line(LEFT * 0.5, RIGHT * (0.5 if k % 3 else 0.2)).set_stroke(MUTED, 3) for k in range(6)]).arrange(DOWN, buff=0.17)
    lines.move_to(b)
    return VGroup(b, lines)


class S03Why(Base):
    CHAPTER = "Why It Matters"

    def construct(self):
        rng = np.random.default_rng(5)
        # ── s015 the puzzle from the Bayes video: its card tile flies to the top-right corner ──
        self.at("s015", 0.0)
        cue = card_cue("Bayes' Theorem", mini_bayes())
        cue_big = cue.copy().scale(1.8).move_to(UP * 0.6)
        self.play(FadeIn(cue_big, scale=0.6), run_time=0.6)
        self.play(LaggedStart(*[pulse(sq, 1.5) for sq in cue_big[2][0]], lag_ratio=0.03), run_time=0.9)
        self.word("s015", "puzzle", dt=-0.3)
        pz = TB("?", 90, WARN).next_to(cue_big, DOWN, buff=0.35)
        self.play(FadeIn(pz, scale=0.4), ripple(pz.get_center(), WARN, r=0.4, scale=3), run_time=0.6)

        # ── s015a find it in the card at the top ──
        self.at("s015a", 0.0)
        self.play(ReplacementTransform(cue_big, cue), FadeOut(pz), run_time=0.8)
        arr = Arrow(UP * 1.2 + RIGHT * 2.2, cue.get_bottom() + DOWN * 0.1 + LEFT * 0.4, color=VIOLET, stroke_width=5, buff=0.1)
        lab = T("watch it: card at the top", 30, VIOLET, weight=BOLD).next_to(arr.get_start(), DOWN, buff=0.2)
        self.play(GrowArrow(arr), FadeIn(lab, shift=UP * 0.2), run_time=0.6)
        self.idle(lambda: pulse(cue, 1.06), lambda: glint(cue.box, VIOLET, 6))

        # ── s016 scientists report p = 0.03 … described as '3% chance it's a fluke' ──
        self.at("s016", 0.0)
        self.idle()
        pap = paper().move_to(LEFT * 4.6 + UP * 0.3)
        self.play(FadeOut(VGroup(arr, lab)), FadeIn(pap, shift=UP * 0.4), cue.animate.set_opacity(0.0), run_time=0.6)
        self.remove(cue)
        self.play(pap.animate.scale(1.25), LaggedStart(*[Create(l) for l in pap[1]], lag_ratio=0.25), run_time=1.2)
        self.idle(lambda: pulse(pap, 1.12), lambda: LaggedStart(*[pulse(l, 1.3) for l in pap[1]], lag_ratio=0.1))
        pc = VGroup(card(3.6, 1.6, AQUA), TB("p = 0.03", 64, AQUA)).move_to(LEFT * 0.9 + UP * 0.9)
        pc[1].move_to(pc[0])
        self.word("s016", "zero", dt=-0.3)
        self.play(TransformFromCopy(pap[1][2], pc[0]), FadeIn(pc[1], scale=0.6), run_time=0.7)
        self.play(ripple(pc.get_center(), AQUA, r=0.6, scale=3), run_time=0.5)
        bt = T("“a 3% chance it's a fluke”", 34, INK, weight=BOLD)
        bb = RoundedRectangle(corner_radius=0.3, width=bt.width + 0.8, height=1.1).set_stroke(INK2, 3).set_fill("#22221f", 1)
        bb.qa_container = True
        bubble = VGroup(bb, bt).move_to(RIGHT * 2.6 + DOWN * 1.2)
        bt.move_to(bb)
        self.word("s016", "described", dt=-0.3)
        self.play(FadeIn(bubble, shift=UP * 0.3), run_time=0.5)
        self.idle(lambda: pulse(bubble, 1.1), lambda: pulse(pc, 1.12))
        self.word("s016", "three", nth=1, dt=-0.2)
        self.play(Indicate(bt, color=WARN, scale_factor=1.08), run_time=0.6)
        qm = TB("?", 80, RED_).next_to(bb, UP, buff=0.2).align_to(bb, RIGHT)
        self.word("s016", "fluke", dt=-0.2)
        self.play(FadeIn(qm, scale=0.4), run_time=0.4)
        self.idle(lambda: AnimationGroup(Wiggle(qm, scale_value=1.4), pulse(bubble, 1.08)), lambda: pulse(pc, 1.12))

        # ── s017 the description flips the question ──
        self.at("s017", 0.0)
        self.word("s017", "flips", dt=-0.3)
        self.idle()
        self.qa_mute(bubble)   # squashing like a card flip
        self.play(bubble.animate.stretch(0.02, 0), FadeOut(qm), run_time=0.35)
        self.remove(bubble)
        a = T("chance of this data, if it's a fluke", 32, AQUA, weight=BOLD)
        b = T("chance it's a fluke, given this data", 32, RED_, weight=BOLD)
        rows = VGroup(a, b).arrange(DOWN, buff=0.9).move_to(RIGHT * 1.0 + DOWN * 1.0)
        ar1 = Arrow(LEFT, RIGHT, color=AQUA, stroke_width=5).scale(0.5).next_to(a, LEFT, buff=0.3)
        ar2 = Arrow(RIGHT, LEFT, color=RED_, stroke_width=5).scale(0.5).next_to(b, LEFT, buff=0.3)
        neq = TB("≠", 56, INK).move_to(rows.get_center())
        self.play(FadeOut(pap, shift=LEFT), pc.animate.move_to(UP * 2.1 + LEFT * 0.4), run_time=0.5)
        self.play(FadeIn(a, shift=RIGHT * 0.4), GrowArrow(ar1), run_time=0.45)
        b.save_state(); b.become(a.copy().set_color(RED_)); b.move_to(rows[1])
        self.play(Restore(b), GrowArrow(ar2), run_time=0.6)     # the same words, swapped round
        self.play(FadeIn(neq, scale=0.4), run_time=0.35)
        self.word("s017", "Today", dt=-0.2)
        self.play(Indicate(a, color=AQUA, scale_factor=1.06), b.animate.set_opacity(0.45), ar2.animate.set_opacity(0.45), run_time=0.7)
        self.idle(lambda: pulse(a, 1.1), lambda: pulse(pc, 1.14))
        eye = VGroup(Ellipse(width=1.6, height=0.8).set_stroke(INK, 5), Circle(0.24).set_stroke(width=0).set_fill(AQUA, 1))
        eye.move_to(RIGHT * 4.6 + UP * 2.1)
        self.word("s017", "eyes", dt=-0.6)
        self.play(FadeIn(eye, scale=0.5), run_time=0.4)
        self.idle(lambda: AnimationGroup(eye[1].animate(rate_func=there_and_back).shift(RIGHT * 0.45), pulse(a, 1.08)),
                  lambda: AnimationGroup(ShowPassingFlash(ar1.copy().set_stroke(AQUA, 10), time_width=0.6), pulse(pc, 1.1)))

        # ── s018 p values are everywhere: tags pop up all over the screen ──
        self.at("s018", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(pc, a, b, ar1, ar2, neq, eye), shift=UP * 0.4), run_time=0.45)
        vals = ["p = 0.04", "p = 0.01", "p = 0.20", "p = 0.003", "p = 0.07", "p = 0.049", "p = 0.12", "p = 0.002", "p = 0.03"]
        spots = [(-4.4, 1.9), (0.2, 2.4), (4.6, 1.8), (-2.2, 0.5), (2.4, 0.4), (-4.9, -0.9), (5.0, -0.8), (-1.0, -1.7), (1.9, -1.8)]
        tags = VGroup(*[pill(v, AQUA, 28).move_to([x, y, 0]) for v, (x, y) in zip(vals, spots)])
        self.play(LaggedStart(*[FadeIn(tg, scale=0.3) for tg in tags[:4]], lag_ratio=0.3), run_time=1.1)
        self.word("s018", "everywhere", dt=-0.5)
        self.play(LaggedStart(*[FadeIn(tg, scale=0.3) for tg in tags[4:]], lag_ratio=0.15), run_time=0.9)
        self.idle(lambda: LaggedStart(*[pulse(tg, 1.1) for tg in tags], lag_ratio=0.08))

        # ── s019 medicine, a website button, a trader ──
        self.at("s019", 0.0)
        self.idle()
        cards = VGroup(*[card(4.0, 2.6) for _ in range(3)]).arrange(RIGHT, buff=0.45).move_to(UP * 0.6)
        self.play(LaggedStart(*[FadeOut(tg, scale=0.3) for tg in tags], lag_ratio=0.05), run_time=0.5)
        def cap(c, txt):
            return T(txt, 24, INK, weight=BOLD).move_to(c.get_bottom() + UP * 0.45)
        k1 = VGroup(capsule(ORANGE_), capsule(BLUE_, 0.0)).arrange(RIGHT, buff=0.4).move_to(cards[0].get_center() + UP * 0.35)
        c1 = cap(cards[0], "medicine vs sugar pill")
        bA = VGroup(RoundedRectangle(corner_radius=0.12, width=1.1, height=0.6).set_stroke(BLUE_, 3).set_fill("#22221f", 1), TB("A", 30, BLUE_))
        bB = VGroup(RoundedRectangle(corner_radius=0.12, width=1.1, height=0.6).set_stroke(ORANGE_, 3).set_fill("#22221f", 1), TB("B", 30, ORANGE_))
        for b_ in (bA, bB):
            b_[0].qa_container = True; b_[1].move_to(b_[0])
        k2 = VGroup(bA, bB).arrange(RIGHT, buff=0.4).move_to(cards[1].get_center() + UP * 0.35)
        c2 = cap(cards[1], "button A vs button B")
        pts = [np.array([x, 0.35 * np.sin(3.1 * x) + 0.18 * x + 0.12 * np.cos(9 * x), 0]) for x in np.linspace(-1.2, 1.2, 25)]
        k3 = VMobject().set_points_as_corners(pts).set_stroke(WARN, 6).move_to(cards[2].get_center() + UP * 0.35)
        q3 = TB("?", 40, WARN).next_to(k3, RIGHT, buff=0.1)
        c3 = cap(cards[2], "strategy vs luck")
        self.play(FadeIn(cards[0], shift=UP * 0.4), FadeIn(k1, shift=UP * 0.2), FadeIn(c1), run_time=0.5)
        self.play(Wiggle(k1, scale_value=1.15), run_time=0.7)
        self.idle(lambda: Wiggle(k1, scale_value=1.25), lambda: pulse(cards[0], 1.06))
        self.word("s019", "website", dt=-0.2)
        self.idle()
        self.play(FadeIn(cards[1], shift=UP * 0.4), FadeIn(k2, shift=UP * 0.2), FadeIn(c2), run_time=0.5)
        cur = Polygon([0, 0, 0], [0, -0.42, 0], [0.11, -0.33, 0], [0.19, -0.5, 0], [0.26, -0.47, 0], [0.18, -0.3, 0], [0.31, -0.3, 0])
        cur.set_fill(INK, 1).set_stroke(BG, 2).move_to(bA.get_center() + DOWN * 0.15 + RIGHT * 0.1)
        cur.qa_ignore = True
        self.play(FadeIn(cur), pulse(bA, 0.9), run_time=0.4)
        self.play(cur.animate.move_to(bB.get_center() + DOWN * 0.15 + RIGHT * 0.1), run_time=0.4)
        self.play(pulse(bB, 0.9), run_time=0.3)
        self.word("s019", "trader", dt=-0.2)
        self.idle()
        self.play(FadeIn(cards[2], shift=UP * 0.4), FadeIn(c3), FadeOut(cur), run_time=0.4)
        self.play(Create(k3), pulse(c3, 1.15), run_time=0.8)
        tip = Dot(radius=0.09, color=WARN).move_to(k3.get_end())
        self.play(FadeIn(q3, scale=0.5), FadeIn(tip), run_time=0.35)
        self.idle(lambda: AnimationGroup(MoveAlongPath(tip, k3), ShowPassingFlash(k3.copy().set_stroke(INK, 9), time_width=0.5)),
                  lambda: LaggedStart(*[pulse(cd, kk, s=1.1) for cd, kk in ((cards[0], k1), (cards[1], k2), (cards[2], k3))], lag_ratio=0.25))
        self._idle.reverse()

        # ── s020 the shared question ──
        self.at("s020", 0.0)
        self.idle()
        qq = pill("real effect, or just chance?", WARN, 40).move_to(DOWN * 1.75)
        grp = VGroup(cards, k1, c1, k2, c2, k3, q3, c3, tip)
        self.play(grp.animate.shift(UP * 0.45), run_time=0.5)
        arrows = VGroup(*[Arrow(c.get_bottom(), qq.get_top(), buff=0.22, color=MUTED, stroke_width=3,
                                max_tip_length_to_length_ratio=0.15) for c in cards])
        self.play(LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.2), run_time=0.7)
        self.idle(lambda: LaggedStart(*[pulse(cd, s=1.1) for cd in cards], lag_ratio=0.25))
        self.word("s020", "real", dt=-0.3)
        self.idle()
        self.play(FadeIn(qq, scale=0.6), ripple(qq.get_center(), WARN, r=0.6, scale=4), run_time=0.6)
        self.idle(lambda: pulse(qq, 1.14), lambda: LaggedStart(*[ShowPassingFlash(a_.copy().set_stroke(WARN, 10), time_width=0.6)
                                                                   for a_ in arrows], lag_ratio=0.15))
        self.until(SEGS["s020"]["end"] + 0.2)
        self.idle()
        self.play(FadeOut(VGroup(grp, arrows, qq), shift=LEFT * 1.0), run_time=0.5)
        self.finish()
