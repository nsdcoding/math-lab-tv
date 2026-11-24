import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cm import *


def head(n, text, color=RED_):
    return VGroup(TB(f"Mistake {n}", 34, color), T(text, 30, INK, weight=BOLD)).arrange(RIGHT, buff=0.35).move_to(UP * 2.3)


class S16Mistakes(Base):
    CHAPTER = "Common Mistakes"

    def construct(self):
        # ── s194 header ──
        self.at("s194", 0.0)
        hd = TB("COMMON MISTAKES", 60, RED_).move_to(UP * 0.3)
        self.play(FadeIn(hd, shift=DOWN * 0.15), run_time=0.5)
        # ── s195 mistake one ──
        self.at("s195", 0.0)
        h1 = head(1, "trusting accuracy on a rare class")
        self.play(FadeOut(hd), FadeIn(h1), run_time=0.5)
        tip = VGroup(T("ask: how rare is it?", 30, INK2), T("compare with the lazy model", 30, INK2)).arrange(DOWN, buff=0.2).move_to(UP * 0.6)
        self.word("s195", "Always")
        self.play(FadeIn(tip[0]), run_time=0.4)
        self.word("s195", "compare")
        self.play(FadeIn(tip[1]), run_time=0.4)
        # ── s195a the baseline sliver ──
        self.at("s195a", 0.0)
        self.play(FadeOut(tip), run_time=0.3)
        nl = NumberLine(x_range=[98, 100, 0.5], length=9.0, color=INK2, include_tip=False, stroke_width=3, tick_size=0.08).move_to(DOWN * 0.6)
        nums = VGroup(*[T(f"{v:g}%", 22, INK2).next_to(nl.n2p(v), DOWN, buff=0.15) for v in (98, 98.5, 99, 99.5, 100)])
        nt = T("accuracy", 22, MUTED).next_to(nums, DOWN, buff=0.12)
        self.play(Create(nl), FadeIn(nums), FadeIn(nt), run_time=0.6)
        mz = marker(nl, 99, MUTED, "lazy 99%", height=0.8, fs=24)
        self.word("s195a", "ninety-nine")
        self.play(FadeIn(mz), run_time=0.5)
        ma = marker(nl, 99.6, AQUA, "Detector A 99.6%", height=1.65, fs=24)
        self.word("s195a", "ninety-nine", nth=1)
        self.play(FadeIn(ma), run_time=0.5)
        gap = Line(nl.n2p(99), nl.n2p(99.6)).set_stroke(WARN, 9)
        gap.qa_ignore = True
        gl = T("that sliver = 90 frauds caught", 26, WARN, weight=BOLD).move_to(LEFT * 3.6 + UP * 0.9)
        self.word("s195a", "sliver.")
        self.play(Create(gap), run_time=0.6)
        self.word("s195a", "ninety", nth=0)
        self.play(FadeIn(gl), run_time=0.4)
        # ── s196 mistake two ──
        self.at("s196", 0.0)
        h2 = head(2, "mixing up precision and recall")
        self.play(FadeOut(VGroup(nl, nums, nt, mz, ma, gap, gl)), ReplacementTransform(h1, h2), run_time=0.6)
        g = grid_at(0.75, np.array([-2.1, -0.55, 0]), counts=A_COUNTS, names=False, row_title="", col_title="", label_size=34, num_size=66)
        self.play(FadeIn(grid_mobs(g)), run_time=0.5)
        fc = g.frame_of(g.col0(), VIOLET)
        fx1 = T("precision starts from the alarms", 26, VIOLET, weight=BOLD).move_to(RIGHT * 3.9 + UP * 0.9)
        self.word("s196", "Precision")
        self.play(Create(fc), FadeIn(fx1), run_time=0.6)
        fr = g.frame_of(g.row0(), ORANGE_, pad=0.17)
        fx2 = T("recall starts from the real cases", 26, ORANGE_, weight=BOLD).next_to(fx1, DOWN, buff=0.35)
        self.word("s196", "Recall")
        self.play(Create(fr), FadeIn(fx2), run_time=0.6)
        # ── s197 which denominator? ──
        self.at("s197", 0.0)
        d1 = T("÷ everything it flagged?", 26, VIOLET).next_to(fx2, DOWN, buff=0.55)
        d2 = T("÷ everything really there?", 26, ORANGE_).next_to(d1, DOWN, buff=0.2)
        self.word("s197", "flagged,")
        self.play(FadeIn(d1), run_time=0.4)
        self.word("s197", "really")
        self.play(FadeIn(d2), run_time=0.4)
        # ── s197a the bottom numbers: 120 and 100 ──
        self.at("s197a", 0.0)
        self.play(FadeOut(VGroup(fx1, fx2, d1, d2)), run_time=0.3)
        c120 = pill("column total 120", VIOLET, 26).move_to(RIGHT * 3.9 + UP * 0.6)
        r100 = pill("row total 100", ORANGE_, 26).next_to(c120, DOWN, buff=0.35)
        self.word("s197a", "column,")
        self.play(FadeIn(c120), run_time=0.4)
        self.word("s197a", "row,")
        self.play(FadeIn(r100), run_time=0.4)
        # ── s198 mistake three: layouts differ ──
        self.at("s198", 0.0)
        h3 = head(3, "assuming every table looks the same")
        self.play(FadeOut(VGroup(c120, r100, fc, fr)), ReplacementTransform(h2, h3), run_time=0.6)
        g2 = grid_at(0.6, np.array([3.6, -0.55, 0]), counts=dict(TP=9870, FN=30, FP=10, TN=90), names=False,
                     rows=("fine", "fraud"), cols=("quiet", "alarm"), row_title="", col_title="", label_size=40, num_size=70)
        ot = T("another tool's layout", 24, MUTED).move_to(np.array([3.6, 1.35, 0]))
        self.word("s198", "rows,")
        self.play(FadeIn(grid_mobs(g2)), FadeIn(ot), run_time=0.7)
        self.word("s198", "first,")
        self.play(highlight(g2.rowlab, color=WARN), run_time=0.8)
        # ── s199 read the labels ──
        self.at("s199", 0.0)
        self.word("s199", "labels.")
        self.play(highlight(g.collab, g2.collab, color=WARN), run_time=0.8)
        self.word("s199", "alarm")
        self.play(Create(g2.frame_of(VGroup(g2.cell["FN"], g2.cell["TN"]), VIOLET)), run_time=0.6)
        # ── s199a find TP first ──
        self.at("s199a", 0.0)
        self.word("s199a", "true")
        self.play(g.light("TP"), g2.light("TN"), run_time=0.6)
        tp = T("TP is here (90)", 24, AQUA, weight=BOLD).next_to(g2.cells, DOWN, buff=0.3)
        self.play(FadeIn(tp), run_time=0.4)
        # ── s200 bonus: one number ──
        self.at("s200", 0.0)
        hb = VGroup(TB("Bonus", 34, WARN), T("judging a model by one number", 30, INK, weight=BOLD)).arrange(RIGHT, buff=0.35).move_to(UP * 2.3)
        self.play(FadeOut(VGroup(grid_mobs(g2), ot, tp, *[m for m in self.mobjects if isinstance(m, RoundedRectangle) and getattr(m, "qa_ignore", False)])),
                  ReplacementTransform(h3, hb), g.unlight("TP"), run_time=0.6)
        sc = pill("F1 = 82%", VIOLET, 34).move_to(RIGHT * 3.6 + UP * 0.4)
        self.word("s200", "single")
        self.play(FadeIn(sc), run_time=0.4)
        hide = T("hides which mistake it makes", 26, INK2).next_to(sc, DOWN, buff=0.3)
        self.word("s200", "hides")
        self.play(FadeIn(hide), run_time=0.4)
        lk = T("look at the whole grid", 28, AQUA, weight=BOLD).next_to(hide, DOWN, buff=0.4)
        self.word("s200", "whole")
        self.play(FadeIn(lk), Create(g.frame_of(g.cells, AQUA)), run_time=0.6)
        self.until(SEGS["s200"]["end"] + 0.1)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        self.finish()
