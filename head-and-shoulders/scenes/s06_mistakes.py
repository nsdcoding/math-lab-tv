import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

W, H = 4.15, 4.4


def mcard(n, title):
    box = card(W, H, RED_)
    head = VGroup(TB(str(n), 40, RED_), T(title, 26, INK, weight=BOLD)).arrange(RIGHT, buff=0.25)
    head.move_to(box.get_top() + DOWN * 0.5)
    return VGroup(box, head)


class S06Mistakes(Base):
    CHAPTER = "Common Mistakes"

    def construct(self):
        # s032
        self.at("s032", 0.0)
        c1, c2, c3 = cards = VGroup(mcard(1, "too early"), mcard(2, "no uptrend"), mcard(3, "a promise?")).arrange(RIGHT, buff=0.35)
        cards.move_to(UP * 0.35)
        self.play(LaggedStart(*[FadeIn(c[0]) for c in cards], lag_ratio=0.2), run_time=0.9)
        # s033: acting before the break
        self.at("s033", 0.0)
        m1 = mini_hs(3.2, 1.3, pts=[(0, 0), (1.5, 0.45), (2.2, 0.6), (3, 0.35), (4, 1.0), (5, 0.35), (5.8, 0.62)])
        m1.move_to(c1[0].get_center() + UP * 0.05)
        y = m1.get_points()[12][1]
        n1 = Line([m1.get_left()[0] + 0.5, y, 0], [c1[0].get_right()[0] - 0.3, y, 0], color=NECK_COL, stroke_width=4)
        bounce = DashedVMobject(VMobject().set_points_as_corners(
            [m1.get_end(), [m1.get_end()[0] + 0.25, y + 0.08, 0], [m1.get_end()[0] + 0.5, y + 0.6, 0]]), num_dashes=8).set_stroke(MUTED, 4)
        cap1 = T("many turn back up", 24, INK2).move_to(c1[0].get_bottom() + UP * 0.55)
        self.play(FadeIn(c1[1]), Create(m1), run_time=0.8)
        self.play(Create(n1), run_time=0.4)
        self.until(word_time("s033", word_index("s033", "many")) - 0.2)
        self.play(Create(bounce), FadeIn(cap1), run_time=0.9)
        # s034: needs an uptrend first
        self.at("s034", 0.0)
        m2 = mini_hs(3.2, 1.6, pts=[(0, 2.2), (1.2, 1.2), (1.9, 1.4), (2.6, 0.45), (3.3, 0.6), (4, 0.3), (4.8, 0.95), (5.6, 0.3), (6.3, 0.62), (7, 0.3), (8, -0.3)])
        m2.move_to(c2[0].get_center() + UP * 0.05)
        x2 = cross(RED_, 0.45).move_to(m2)
        cap2 = T("reverses an uptrend", 24, INK2).move_to(c2[0].get_bottom() + UP * 0.55)
        self.play(FadeIn(c2[1]), Create(m2), run_time=0.9)
        self.until(word_time("s034", word_index("s034", "reversal")) - 0.2)
        self.play(Create(x2), FadeIn(cap2), run_time=0.7)
        # s035: target is a rule of thumb
        self.at("s035", 0.0)
        ctr = c3[0].get_center() + UP * 0.05
        tl = DashedLine(ctr + LEFT * 1.5, ctr + RIGHT * 1.5, color=TGT_COL, stroke_width=4)
        tt = T("target", 22, TGT_COL).next_to(tl, LEFT, buff=0.1).shift(RIGHT * 0.0)
        tt.move_to(ctr + LEFT * 1.1 + UP * 0.3)
        up = Arrow(ctr + RIGHT * 0.4 + UP * 0.1, ctr + RIGHT * 0.4 + UP * 0.85, buff=0, color=INK2, stroke_width=5)
        dn = Arrow(ctr + RIGHT * 1.1 + DOWN * 0.1, ctr + RIGHT * 1.1 + DOWN * 0.85, buff=0, color=INK2, stroke_width=5)
        stop_s = T("stops short", 20, INK2).next_to(up, LEFT, buff=0.15).shift(UP * 0.2)
        over = T("overshoots", 20, INK2).next_to(dn, LEFT, buff=0.15).shift(DOWN * 0.15)
        cap3 = T("a rule of thumb", 24, INK2).move_to(c3[0].get_bottom() + UP * 0.55)
        self.play(FadeIn(c3[1]), Create(tl), FadeIn(tt), run_time=0.8)
        self.until(word_time("s035", word_index("s035", "rule")) - 0.2)
        self.play(FadeIn(cap3), run_time=0.5)
        self.until(word_time("s035", word_index("s035", "price")) - 0.1)
        self.play(GrowArrow(up), FadeIn(stop_s), run_time=0.6)
        self.play(GrowArrow(dn), FadeIn(over), run_time=0.6)
        # s036: bonus: inverse head and shoulders
        self.at("s036", 0.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
        bonus = pill("bonus", WARN, 26).move_to(UP * 2.75)
        big = mini_hs(7.0, 2.6).move_to(UP * 0.4)
        self.play(FadeIn(bonus), Create(big), run_time=1.0)
        self.until(word_time("s036", word_index("s036", "upside")) - 0.1)
        self.play(big.animate.stretch(-1, 1), run_time=1.2)
        lab = T("inverse head and shoulders", 36, AQUA, weight=BOLD).move_to(DOWN * 1.6)
        sub = T("a possible bottom after a fall  ·  shape only", 26, MUTED).next_to(lab, DOWN, buff=0.25)
        self.play(big.animate.set_stroke(AQUA), FadeIn(lab, shift=UP * 0.15), run_time=0.8)
        self.play(FadeIn(sub), run_time=0.5)
        self.until(SEGS["s036"]["end"] + 0.3)
        self.play(FadeOut(VGroup(bonus, big, lab, sub)), run_time=0.5)
        self.finish()
