import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def base_chart():
    g = price_axes(); ax = g.ax
    P = pieces(ax)
    return g, ax, P


class S03Peaks(Base):
    CHAPTER = "Three Peaks"

    def construct(self):
        g, ax, P = base_chart()
        # s011: chart comes back
        self.at("s011", 0.0)
        self.play(FadeIn(g), run_time=0.6)
        self.play(Create(P[:4]), run_time=2.2, rate_func=linear)
        # s012: left shoulder
        self.at("s012", 0.0)
        ls = peak_label(ax, "ls", "left shoulder · $60", SH_COL)
        seg0 = path_piece(ax, 6, 11, SH_COL, 7)
        self.play(Create(seg0), FadeIn(ls, shift=UP * 0.15), run_time=1.0)
        ctrl = pill("buyers in control", AQUA, 24).move_to(ax.c2p(24, 30))
        self.until(word_time("s012", word_index("s012", "buyers")) - 0.2)
        self.play(FadeIn(ctrl, shift=UP * 0.15), run_time=0.5)
        # s013: head
        self.at("s013", 0.0)
        hd = peak_label(ax, "head", "head · $70", HEAD_COL)
        seg1 = path_piece(ax, 11, 17, HEAD_COL, 7)
        self.play(FadeOut(ctrl), Create(seg1), FadeIn(hd, shift=UP * 0.15), run_time=1.0)
        top = hline(ax, 70, 0, 48, HEAD_COL, dashed=True, width=2).set_opacity(0.6)
        hi = T("highest point", 24, HEAD_COL).next_to(ax.c2p(40, 70), UP, buff=0.12)
        self.until(word_time("s013", word_index("s013", "highest")) - 0.2)
        self.play(Create(top), FadeIn(hi), run_time=0.8)
        # s014: right shoulder, lower high
        self.at("s014", 0.0)
        rs = peak_label(ax, "rs", "right shoulder · $61", SH_COL)
        rs[1].next_to(rs[0], UP, buff=0.18).shift(RIGHT * 0.9)
        seg2 = path_piece(ax, 17, 22, SH_COL, 7)
        self.play(FadeOut(hi), Create(seg2), FadeIn(rs, shift=UP * 0.15), run_time=1.0)
        self.until(word_time("s014", word_index("s014", "lower")) - 0.2)
        lh = pill("lower high", RED_, 24).move_to(ax.c2p(43, 55))
        self.play(FadeIn(lh, scale=0.8), run_time=0.5)
        # s015: rallies shrink: +18 then +9 (inset in the empty lower area)
        self.at("s015", 0.0)
        box = card(5.4, 2.0, INK2).move_to(ax.c2p(24, 31))
        u = 0.08   # units per dollar in the inset
        a1 = Arrow(ORIGIN, UP * 18 * u, buff=0, color=HEAD_COL, stroke_width=7, max_tip_length_to_length_ratio=0.2)
        a2 = Arrow(ORIGIN, UP * 9 * u, buff=0, color=SH_COL, stroke_width=7, max_tip_length_to_length_ratio=0.3)
        base_y = box.get_bottom()[1] + 0.3
        a1.move_to([box.get_left()[0] + 1.0, base_y, 0], aligned_edge=DOWN)
        a2.move_to([box.get_left()[0] + 3.1, base_y, 0], aligned_edge=DOWN)
        l1 = T("+$18", 30, HEAD_COL, weight=BOLD).next_to(a1, RIGHT, buff=0.2)
        l2 = T("+$9", 30, SH_COL, weight=BOLD).next_to(a2, RIGHT, buff=0.2)
        cap = T("rally from each dip", 22, MUTED).move_to([box.get_center()[0] + 1.2, box.get_top()[1] - 0.35, 0])
        self.play(FadeIn(box), FadeIn(cap), run_time=0.5)
        self.play(GrowArrow(a1), FadeIn(l1), run_time=0.8)
        self.until(word_time("s015", word_index("s015", "buyers")) - 0.2)
        self.play(GrowArrow(a2), FadeIn(l2), run_time=0.8)
        self.play(Indicate(VGroup(a2, l2), color=RED_), run_time=1.0)
        # s016: shoulders don't need to match
        self.at("s016", 0.0)
        inset = VGroup(box, a1, a2, l1, l2, cap)
        cmp = VGroup(T("$60", 40, SH_COL, weight=BOLD), T("vs", 30, MUTED), T("$61", 40, SH_COL, weight=BOLD)).arrange(RIGHT, buff=0.35)
        ok = T("close enough", 28, AQUA, weight=BOLD)
        box2 = card(5.4, 2.0, INK2).move_to(box)
        VGroup(cmp, ok).arrange(DOWN, buff=0.3).move_to(box2)
        self.play(FadeOut(inset), FadeIn(box2), run_time=0.4)
        self.play(FadeIn(cmp, shift=UP * 0.2), Indicate(ls[0], color=SH_COL), Indicate(rs[0], color=SH_COL), run_time=0.9)
        self.play(FadeIn(ok, scale=0.8), run_time=0.5)
        self.until(SEGS["s016"]["end"] + 0.1)
        self.play(FadeOut(VGroup(box2, cmp, ok, ls, hd, rs, lh, top, seg0, seg1, seg2)), run_time=0.5)
        self.finish()
