import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cm import *


def base_grid(scene):
    g = grid_at(counts=A_COUNTS)
    scene.add(g.cells, g.names, g.nums, g.collab, g.coltitle, g.rowlab, g.rowtitle)
    return g


class S06Accuracy(Base):
    CHAPTER = "Accuracy"

    def construct(self):
        g = base_grid(self)
        # ── s066 accuracy ──
        self.at("s066", 0.0)
        ttl = TB("ACCURACY", 52, WARN).move_to(RIGHT * PANEL_X + UP * 2.2)
        self.word("s066", "Accuracy")
        self.play(FadeIn(ttl, shift=DOWN * 0.15), run_time=0.5)
        # ── s067 the question ──
        self.at("s067", 0.0)
        q = VGroup(T("Out of everything,", 28, INK), T("how often was it right?", 28, INK)).arrange(DOWN, buff=0.15)
        q.next_to(ttl, DOWN, buff=0.35)
        self.play(FadeIn(q), run_time=0.5)
        # ── s068 the diagonal ──
        self.at("s068", 0.0)
        self.word("s068", "diagonal")
        self.play(g.light("TP"), g.light("TN"), run_time=0.6)
        # ── s069 over everything ──
        self.at("s069", 0.0)
        fr = g.frame_of(g.cells, WARN)
        self.word("s069", "everything")
        self.play(Create(fr), run_time=0.7)
        # ── s070 the formula ──
        self.at("s070", 0.0)
        f = ratio("accuracy", "TP + TN", "total", WARN, AQUA, INK, 42).move_to(RIGHT * PANEL_X + DOWN * 0.3)
        self.play(FadeIn(f), FadeOut(fr), run_time=0.6)
        d1 = T("TP = true positives", 24, AQUA).next_to(f, DOWN, buff=0.35)
        d2 = T("TN = true negatives", 24, AQUA).next_to(d1, DOWN, buff=0.15)
        self.word("s070", "short")
        self.play(FadeIn(d1), run_time=0.4)
        self.word("s070", "short", nth=1)
        self.play(FadeIn(d2), run_time=0.4)
        # ── s071 / s072 the numbers ──
        self.at("s071", 0.0)
        self.play(FadeOut(VGroup(q, d1, d2)), f.animate.move_to(RIGHT * PANEL_X + UP * 1.0), run_time=0.5)
        e1 = panel_eq([("90", AQUA), ("+", INK2), ("9,870", AQUA), ("=", INK2), ("9,960", AQUA)], -0.4)
        self.word("s071", "ninety")
        self.play(FadeIn(e1[:3]), run_time=0.5)
        self.word("s071", "Nine", nth=1)
        self.play(FadeIn(e1[3:]), run_time=0.4)
        self.at("s072", 0.0)
        e2 = VGroup(nfrac("9,960", "10,000", INK, 44), T("=", 36, INK2), TB("99.6%", 50, WARN)).arrange(RIGHT, buff=0.22)
        e2.move_to(RIGHT * PANEL_X + DOWN * 1.7)
        self.play(FadeIn(e2[0]), run_time=0.4)
        self.word("s072", "ninety-nine")
        self.play(FadeIn(e2[1:], shift=LEFT * 0.15), run_time=0.5)

        # ── s073 versus the lazy detector ──
        self.at("s073", 0.0)
        self.play(FadeOut(VGroup(f, e1, e2)), g.unlight("TP"), g.unlight("TN"), run_time=0.5)
        nl = NumberLine(x_range=[98, 100, 0.5], length=3.3, color=INK2, include_tip=False, stroke_width=3, tick_size=0.08)
        nl.move_to(RIGHT * PANEL_X + DOWN * 0.6)
        nums = VGroup(*[T(f"{v:g}%", 20, INK2).next_to(nl.n2p(v), DOWN, buff=0.15) for v in (98, 99, 100)])
        nt = T("accuracy", 22, MUTED).next_to(nums, DOWN, buff=0.12)
        self.play(Create(nl), FadeIn(nums), FadeIn(nt), run_time=0.6)
        mz = marker(nl, 99, MUTED, "lazy 99%", height=0.7, fs=22)
        self.word("s073", "lazy")
        self.play(FadeIn(mz), run_time=0.5)
        # ── s074 only moves it 0.6 ──
        self.at("s074", 0.0)
        ma = marker(nl, 99.6, AQUA, "A 99.6%", height=1.45, fs=22)
        self.word("s074", "ninety-nine", nth=1)
        self.play(FadeIn(ma), run_time=0.5)
        gap = Line(nl.n2p(99) + DOWN * 0.0, nl.n2p(99.6)).set_stroke(WARN, 8)
        gap.qa_ignore = True   # sits on the axis line on purpose
        gl = T("this gap = 90 frauds caught", 24, WARN, weight=BOLD).next_to(nt, DOWN, buff=0.3)
        self.word("s074", "Less")
        self.play(Create(gap), FadeIn(gl), run_time=0.6)

        # ── s075 the huge bottom-right box ──
        self.at("s075", 0.0)
        self.play(FadeOut(VGroup(nl, nums, nt, mz, ma, gap, gl)), run_time=0.4)
        self.word("s075", "huge")
        self.play(g.light("TN", WARN), run_time=0.5)
        sb = stacked_bar([(90, AQUA), (10, BLUE_), (30, ORANGE_), (9870, INK2)], 3.6, 0.55).move_to(RIGHT * PANEL_X + UP * 0.2)
        sbl = T("all 10,000 payments", 22, MUTED).next_to(sb, UP, buff=0.2)
        tn = T("9,870 easy, correct", 24, INK2, weight=BOLD).next_to(sb, DOWN, buff=0.25)
        rest = T("everything else: 130", 24, ORANGE_, weight=BOLD).next_to(tn, DOWN, buff=0.15)
        self.word("s075", "Nine")
        self.play(FadeIn(sbl), GrowFromEdge(sb, LEFT), run_time=0.9)
        self.play(FadeIn(tn), run_time=0.4)
        self.word("s075", "drown")
        self.play(FadeIn(rest), run_time=0.4)
        # ── s076 rule of thumb ──
        self.at("s076", 0.0)
        self.play(FadeOut(VGroup(sb, sbl, tn, rest)), g.unlight("TN"), run_time=0.4)
        rule = side_card(["When one class is rare,", "accuracy mostly", "measures how rare it is."], WARN, 24,
                         title="RULE OF THUMB", title_color=WARN).move_to(RIGHT * PANEL_X + UP * 0.2)
        self.word("s076", "rule")
        self.play(FadeIn(rule, shift=LEFT * 0.2), run_time=0.6)
        # ── s077 fine when balanced ──
        self.at("s077", 0.0)
        self.play(FadeOut(rule), run_time=0.4)
        bb = stacked_bar([(300, ORANGE_), (700, INK2)], 3.6, 0.55).move_to(RIGHT * PANEL_X + UP * 0.6)
        bl = T("roughly balanced: 300 vs 700", 22, INK2).next_to(bb, UP, buff=0.2)
        ok = pill("accuracy is OK here", AQUA, 26).next_to(bb, DOWN, buff=0.35)
        sp = T("(the spam example, later)", 22, MUTED).next_to(ok, DOWN, buff=0.2)
        self.word("s077", "same")
        self.play(FadeIn(bl), GrowFromEdge(bb, LEFT), run_time=0.7)
        self.word("s077", "fine")
        self.play(FadeIn(ok), run_time=0.4)
        self.word("s077", "spam")
        self.play(FadeIn(sp), run_time=0.4)
        # ── s078 two questions that zoom in on the fraud ──
        self.at("s078", 0.0)
        self.play(FadeOut(VGroup(bb, bl, ok, sp, ttl)), run_time=0.4)
        fc = g.frame_of(g.col0(), VIOLET); fr_ = g.frame_of(g.row0(), ORANGE_)
        self.word("s078", "two")
        self.play(Create(fc), run_time=0.6)
        self.play(Create(fr_), run_time=0.6)
        self.until(SEGS["s078"]["end"] + 0.1)
        self.play(FadeOut(VGroup(fc, fr_)), run_time=0.4)
        self.finish()
