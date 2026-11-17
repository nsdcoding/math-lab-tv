import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def capsule(color, fill=0.9, w=1.1):
    left = RoundedRectangle(corner_radius=0.22, width=w / 2 + 0.2, height=0.44).set_stroke(color, 3).set_fill(color, fill)
    right = RoundedRectangle(corner_radius=0.22, width=w / 2 + 0.2, height=0.44).set_stroke(color, 3).set_fill("#22221f", 1)
    right.next_to(left, RIGHT, buff=-0.4)
    return VGroup(right, left)


class S03Why(Base):
    CHAPTER = "Why It Matters"

    def construct(self):
        # ── s015 the puzzle from the Bayes video ──
        self.at("s015", 0.0)
        frm = pill("from: Bayes' Theorem", VIOLET, 26).move_to(UP * 3.3 + RIGHT * 3.6)
        pc = VGroup(card(3.6, 1.6, AQUA), TB("p = 0.03", 64, AQUA)).move_to(LEFT * 2.6 + UP * 0.6)
        pc[1].move_to(pc[0])
        self.play(FadeIn(frm, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(pc, scale=0.8), run_time=0.7)

        # ── s016 'a 3% chance it's a fluke?' ──
        self.at("s016", 0.0)
        bt = T("“a 3% chance it's a fluke?”", 34, INK, weight=BOLD)
        bb = RoundedRectangle(corner_radius=0.3, width=bt.width + 0.8, height=1.2).set_stroke(INK2, 3).set_fill("#22221f", 1)
        bb.qa_container = True
        tail = Polygon(LEFT * 0.25, RIGHT * 0.25, DOWN * 0.45 + LEFT * 0.45).set_stroke(INK2, 3).set_fill("#22221f", 1)
        tail.qa_container = True
        bubble = VGroup(bb, bt).move_to(RIGHT * 1.6 + DOWN * 0.9)
        bt.move_to(bb)
        tail.next_to(bb, UP, buff=-0.05).align_to(bb, LEFT).shift(RIGHT * 0.5).rotate(PI)
        self.play(FadeIn(VGroup(tail, bubble), shift=UP * 0.2), run_time=0.6)
        self.until(word_time("s016", word_index("s016", "described")) - 0.3)
        qm = TB("?", 80, RED_).next_to(bb, RIGHT, buff=0.3)
        self.play(FadeIn(qm, scale=0.5), run_time=0.4)

        # ── s017 the description flips the question ──
        self.at("s017", 0.0)
        self.play(FadeOut(VGroup(bubble, tail), scale=0.8), FadeOut(qm), pc.animate.move_to(UP * 1.9), run_time=0.6)
        a = T("chance of this data, if it's a fluke", 32, AQUA, weight=BOLD)
        b = T("chance it's a fluke, given this data", 32, RED_, weight=BOLD)
        rows = VGroup(a, b).arrange(DOWN, buff=0.9).move_to(RIGHT * 0.4 + DOWN * 0.7)
        ar1 = Arrow(LEFT, RIGHT, color=AQUA, stroke_width=5).scale(0.5).next_to(a, LEFT, buff=0.3)
        ar2 = Arrow(RIGHT, LEFT, color=RED_, stroke_width=5).scale(0.5).next_to(b, LEFT, buff=0.3)
        neq = TB("≠", 60, INK).move_to(rows.get_center())
        self.play(FadeIn(a, shift=RIGHT * 0.3), GrowArrow(ar1), run_time=0.6)
        self.play(FadeIn(b, shift=LEFT * 0.3), GrowArrow(ar2), run_time=0.6)
        self.play(FadeIn(neq, scale=0.5), run_time=0.4)
        self.until(word_time("s017", word_index("s017", "really")) - 0.2)
        self.play(Indicate(a, color=AQUA, scale_factor=1.06), run_time=0.8)

        # ── s018 p values are everywhere: three empty cards ──
        self.at("s018", 0.0)
        cards = VGroup(*[card(4.0, 2.6) for _ in range(3)]).arrange(RIGHT, buff=0.45).move_to(UP * 0.6)
        self.play(FadeOut(VGroup(pc, a, b, ar1, ar2, neq, frm)), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cards], lag_ratio=0.2), run_time=0.9)

        # ── s019 medicine, a website button, a trader ──
        self.at("s019", 0.0)
        def cap(c, txt):
            return T(txt, 24, INK, weight=BOLD).move_to(c.get_bottom() + UP * 0.45)
        k1 = VGroup(capsule(ORANGE_), capsule(BLUE_, 0.0)).arrange(RIGHT, buff=0.4).move_to(cards[0].get_center() + UP * 0.35)
        c1 = cap(cards[0], "medicine vs sugar pill")
        bA = VGroup(RoundedRectangle(corner_radius=0.12, width=1.1, height=0.6).set_stroke(BLUE_, 3).set_fill("#22221f", 1),
                    TB("A", 30, BLUE_))
        bB = VGroup(RoundedRectangle(corner_radius=0.12, width=1.1, height=0.6).set_stroke(ORANGE_, 3).set_fill("#22221f", 1),
                    TB("B", 30, ORANGE_))
        for b_ in (bA, bB):
            b_[0].qa_container = True; b_[1].move_to(b_[0])
        k2 = VGroup(bA, bB).arrange(RIGHT, buff=0.4).move_to(cards[1].get_center() + UP * 0.35)
        c2 = cap(cards[1], "button A vs button B")
        pts = [np.array([x, 0.35 * np.sin(3.1 * x) + 0.18 * x + 0.12 * np.cos(9 * x), 0]) for x in np.linspace(-1.2, 1.2, 25)]
        k3 = VMobject().set_points_as_corners(pts).set_stroke(WARN, 4).move_to(cards[2].get_center() + UP * 0.35)
        q3 = TB("?", 40, WARN).next_to(k3, RIGHT, buff=0.1)
        c3 = cap(cards[2], "strategy vs luck")
        self.play(FadeIn(k1), FadeIn(c1), run_time=0.6)
        self.until(word_time("s019", word_index("s019", "website")) - 0.2)
        self.play(FadeIn(k2), FadeIn(c2), run_time=0.6)
        self.until(word_time("s019", word_index("s019", "trader")) - 0.2)
        self.play(Create(k3), FadeIn(q3), FadeIn(c3), run_time=0.8)

        # ── s020 the shared question ──
        self.at("s020", 0.0)
        qq = pill("real effect, or just chance?", WARN, 40).move_to(DOWN * 1.75)
        grp = VGroup(cards, k1, c1, k2, c2, k3, q3, c3)
        self.play(grp.animate.shift(UP * 0.45), run_time=0.5)
        arrows = VGroup(*[Arrow(c.get_bottom(), qq.get_top(), buff=0.12, color=MUTED, stroke_width=3,
                                max_tip_length_to_length_ratio=0.15) for c in cards])
        self.play(LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.2), FadeIn(qq, shift=UP * 0.2), run_time=0.9)
        self.play(Indicate(qq, color=WARN, scale_factor=1.06), run_time=0.8)
        self.until(SEGS["s020"]["end"] + 0.2)
        self.play(FadeOut(VGroup(grp, arrows, qq)), run_time=0.5)
        self.finish()
