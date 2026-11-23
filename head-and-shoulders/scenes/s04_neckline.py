import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

VOL = {2: 4, 4: 4.5, 6: 5, 8: 5, 10: 5.5, 12: 6, 14: 6.5, 16: 5, 18: 5, 20: 5.5, 22: 6, 24: 6.5, 26: 5, 28: 4.5,
       30: 3, 32: 3, 34: 3, 36: 3.5, 38: 9}


class S04Neckline(Base):
    CHAPTER = "The Neckline"

    def construct(self):
        g = price_axes(); ax = g.ax
        P = pieces(ax)
        self.add(g, P[:4])   # same frame the previous scene ended on
        # s017: two dips at 52
        self.at("s017", 0.0)
        dd = VGroup(*[Dot(pt(ax, k), radius=0.11, color=NECK_COL) for k in ("t1", "t2")])
        labs = VGroup(*[T("$52", 26, NECK_COL, weight=BOLD).next_to(d, DOWN, buff=0.18) for d in dd])
        self.play(FadeIn(dd, scale=0.4), run_time=0.5)
        self.until(word_time("s017", word_index("s017", "both")) - 0.1)
        self.play(FadeIn(labs, shift=UP * 0.1), *[Indicate(d, color=NECK_COL, scale_factor=1.7) for d in dd], run_time=0.9)
        # s018: neckline
        self.at("s018", 0.0)
        nl = hline(ax, NECK, 6, 44, NECK_COL, width=5)
        nlab = T("neckline", 28, NECK_COL, weight=BOLD).next_to(ax.c2p(6, NECK), UP, buff=0.15).shift(RIGHT * 0.2)
        self.play(FadeOut(labs), Create(nl), run_time=1.0)
        self.play(FadeIn(nlab, shift=UP * 0.1), run_time=0.5)
        # s019: not confirmed until a close below
        self.at("s019", 0.0)
        self.play(P[3].animate.set_stroke(opacity=0.12), run_time=0.6)
        st = pill("not confirmed yet", MUTED, 26).move_to(ax.c2p(24, 32))
        self.until(word_time("s019", word_index("s019", "until")) - 0.1)
        self.play(FadeIn(st, shift=UP * 0.15), run_time=0.5)
        # s020: just a shape that might become one: ghost bounce
        self.at("s020", 0.0)
        ghost = DashedVMobject(VMobject().set_points_as_corners(
            [ax.c2p(x, y) for x, y in [(33, 61), (35, 56), (37, 53.5), (39, 58), (41, 63), (43, 67)]]),
            num_dashes=24).set_stroke(INK2, 5)
        q = T("?", 44, INK2, weight=BOLD).next_to(ax.c2p(43, 67), RIGHT, buff=0.15)
        self.play(Create(ghost), FadeIn(q), run_time=1.4)
        # s021: close below 52 → confirmed
        self.at("s021", 0.0)
        self.play(FadeOut(ghost), FadeOut(q), run_time=0.4)
        P3b = P[3].copy().set_stroke(INK, opacity=1)
        self.play(Create(P3b), run_time=1.0, rate_func=linear)
        cf = pill("confirmed: close below $52", NECK_COL, 26).move_to(st)
        self.play(Flash(pt(ax, "break"), color=NECK_COL, flash_radius=0.4), ReplacementTransform(st, cf), run_time=0.7)
        # s022: volume
        self.at("s022", 0.0)
        self.play(FadeOut(cf), run_time=0.3)
        bars = VGroup()
        for d, v in VOL.items():
            r = Rectangle(width=0.14, height=v * 0.0817 * 1.1, stroke_width=0, fill_color=VOL_COL, fill_opacity=0.85)
            r.move_to(ax.c2p(d, 20), aligned_edge=DOWN).shift(UP * 0.04)
            bars.add(r)
        vlab = T("volume · illustration", 22, VOL_COL).move_to(ax.c2p(20, 30.5))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), FadeIn(vlab), run_time=1.6)
        quiet = VGroup(*[bars[i] for i in range(14, 18)])
        self.until(word_time("s022", word_index("s022", "lighter")) - 0.2)
        self.play(quiet.animate.set_fill(SH_COL), run_time=0.6)
        self.until(word_time("s022", word_index("s022", "jumps")) - 0.2)
        self.play(bars[-1].animate.set_fill(NECK_COL), Indicate(bars[-1], color=NECK_COL, scale_factor=1.2), run_time=0.8)
        # s023: retest
        self.at("s023", 0.0)
        self.play(FadeOut(VGroup(bars, vlab)), run_time=0.4)
        rt = path_piece(ax, KEY["break"], KEY["retest"])
        self.play(Create(rt), run_time=1.2, rate_func=linear)
        rlab = pill("retest", NECK_COL, 24).next_to(ax.c2p(42, 52), UP, buff=0.35)
        ceil = T("old floor → now a ceiling", 24, NECK_COL).move_to(ax.c2p(24, 32))
        self.play(FadeIn(rlab, shift=DOWN * 0.1), Indicate(nl, color=NECK_COL), run_time=0.8)
        self.play(FadeIn(ceil), run_time=0.5)
        self.until(SEGS["s023"]["end"] + 0.1)
        self.play(FadeOut(VGroup(rlab, ceil, dd, nlab)), run_time=0.4)
        self.finish()
