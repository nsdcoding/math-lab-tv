import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cm import *

TILES = [("ML", "Machine Learning", AQUA), ("DS", "Data Science", VIOLET), ("Finance", "Finance", WARN), ("CS", "Computer Science", BLUE_)]


def tile(short, long_, color, w=2.9, h=1.6):
    box = card(w, h, color)
    a = TB(short, 40, color).move_to(box.get_center() + UP * 0.2)
    b = T(long_, 20, INK2).move_to(box.get_center() + DOWN * 0.42)
    return VGroup(box, a, b)


class S15Uses(Base):
    CHAPTER = "Where You'll Use It"

    def construct(self):
        # ── s187 four tiles ──
        self.at("s187", 0.0)
        tiles = VGroup(*[tile(*t) for t in TILES]).arrange(RIGHT, buff=0.35).move_to(UP * 0.4)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.12), run_time=0.9)
        # move them into a top row of small tiles
        small = VGroup(*[tile(*t, w=2.4, h=1.1) for t in TILES]).arrange(RIGHT, buff=0.3).move_to(UP * 2.1)
        for t in small:
            t[1].scale(0.8).move_to(t[0].get_center() + UP * 0.14); t[2].scale(0.9).move_to(t[0].get_center() + DOWN * 0.3)

        def focus(i):
            return [small[j][0].animate.set_stroke(TILES[j][2] if j == i else GRID, 4 if j == i else 2.5) for j in range(4)]

        # ── s188 ML: the first thing printed ──
        self.at("s188", 0.0)
        self.play(ReplacementTransform(tiles, small), run_time=0.7)
        self.play(*focus(0), run_time=0.3)
        mb = detector_box("model", AQUA, w=2.2, h=1.1).move_to(LEFT * 3.6 + DOWN * 0.4)
        mg = mini_grid(A_COUNTS, 0.4, RIGHT * 2.2 + DOWN * 0.4)
        ar = Arrow(mb.get_right(), mg.rowlab.get_left() + LEFT * 0.1, buff=0.15, color=INK2, stroke_width=4)
        self.word("s188", "printed")
        self.play(FadeIn(mb), GrowArrow(ar), FadeIn(grid_mobs(mg)), run_time=0.8)
        qs = VGroup(pill("a cat?", INK2, 24), pill("will they cancel?", INK2, 24)).arrange(RIGHT, buff=0.3).next_to(mb, DOWN, buff=0.5)
        self.word("s188", "cat?")
        self.play(FadeIn(qs[0]), run_time=0.4)
        self.word("s188", "cancel?")
        self.play(FadeIn(qs[1]), run_time=0.4)
        # ── s188a one line of code ──
        self.at("s188a", 0.0)
        self.play(FadeOut(VGroup(mb, ar, qs, grid_mobs(mg))), run_time=0.4)
        code = T("confusion_matrix(truth, guess)", 28, AQUA)
        cb = side_card([code], AQUA).move_to(LEFT * 2.6 + DOWN * 0.3)
        out = VGroup(T("[[ 9,870    30 ]", 30, INK), T(" [    10    90 ]]", 30, INK)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        out.move_to(RIGHT * 3.6 + DOWN * 0.3)
        ar2 = Arrow(cb.get_right(), out.get_left(), buff=0.2, color=INK2, stroke_width=4)
        self.word("s188a", "line")
        self.play(FadeIn(cb), run_time=0.5)
        self.word("s188a", "grid")
        self.play(GrowArrow(ar2), FadeIn(out), run_time=0.6)
        nt = T("same four numbers (this tool puts 'no' first)", 22, MUTED).next_to(out, DOWN, buff=0.3)
        self.word("s188a", "exactly")
        self.play(FadeIn(nt), run_time=0.4)
        # ── s189 rare things: report precision and recall ──
        self.at("s189", 0.0)
        self.play(FadeOut(VGroup(cb, out, ar2, nt)), run_time=0.4)
        rep = VGroup(T("rare class? report", 30, INK, weight=BOLD), pill("precision", VIOLET, 28), pill("recall", ORANGE_, 28)).arrange(RIGHT, buff=0.3)
        rep.move_to(DOWN * 0.1)
        self.word("s189", "report")
        self.play(FadeIn(rep), run_time=0.5)
        lz = VGroup(T("not accuracy alone", 28, RED_, weight=BOLD), T("(remember the lazy 99%)", 24, MUTED)).arrange(RIGHT, buff=0.3).next_to(rep, DOWN, buff=0.45)
        self.word("s189", "never")
        self.play(FadeIn(lz), run_time=0.4)
        # ── s190 DS: explaining a model ──
        self.at("s190", 0.0)
        self.play(FadeOut(VGroup(rep, lz)), *focus(1), run_time=0.4)
        rc = side_card(["Of every 100 alarms, 75 are real.", "Of every 100 frauds, we catch 90."], VIOLET, 28,
                       title="report card", title_color=VIOLET).move_to(DOWN * 0.2)
        self.word("s190", "explain")
        self.play(FadeIn(rc[0]), FadeIn(rc[1][0]), run_time=0.5)
        self.word("s190", "Of")
        self.play(FadeIn(rc[1][1]), run_time=0.4)
        self.word("s190", "Of", nth=1)
        self.play(FadeIn(rc[1][2]), run_time=0.4)
        # ── s191 Finance ──
        self.at("s191", 0.0)
        self.play(FadeOut(rc), *focus(2), run_time=0.4)
        f1 = VGroup(payment_card(WARN, 1.1), T("fraud detection", 28, WARN, weight=BOLD)).arrange(DOWN, buff=0.25)
        f2 = VGroup(VGroup(*[Rectangle(width=0.22, height=h).set_stroke(width=0).set_fill(WARN, 0.85) for h in (0.3, 0.5, 0.75)]).arrange(RIGHT, buff=0.08, aligned_edge=DOWN),
                    T("credit risk", 28, WARN, weight=BOLD)).arrange(DOWN, buff=0.25)
        for x in f2[0]: x.qa_ignore = True
        VGroup(f1, f2).arrange(RIGHT, buff=1.5).move_to(UP * 0.1)
        self.word("s191", "fraud")
        self.play(FadeIn(f1), run_time=0.4)
        self.word("s191", "credit")
        self.play(FadeIn(f2), run_time=0.4)
        cs = T("the cut-off is set by the cost of each mistake", 26, INK2).next_to(VGroup(f1, f2), DOWN, buff=0.5)
        self.word("s191", "cut-off")
        self.play(FadeIn(cs), run_time=0.4)
        # ── s192 CS ──
        self.at("s192", 0.0)
        self.play(FadeOut(VGroup(f1, f2, cs)), *focus(3), run_time=0.4)
        items = VGroup(*[pill(t, BLUE_, 26) for t in ("spam filters", "malware scanners", "intrusion detection")]).arrange(RIGHT, buff=0.3)
        items.move_to(UP * 0.3)
        for k, w in enumerate(("spam", "malware", "intruders.")):
            self.word("s192", w)
            self.play(FadeIn(items[k], shift=UP * 0.1), run_time=0.4)
        ig = T("too many false alarms → people ignore them", 26, ORANGE_, weight=BOLD).next_to(items, DOWN, buff=0.55)
        self.word("s192", "ignore")
        self.play(FadeIn(ig), run_time=0.4)
        # ── s193 beyond ──
        self.at("s193", 0.0)
        self.play(FadeOut(VGroup(items, ig)), *focus(-1), run_time=0.4)
        more = VGroup(*[pill(t, INK2, 26) for t in ("medical tests", "airport security", "factory checks")]).arrange(RIGHT, buff=0.3).move_to(UP * 0.3)
        self.word("s193", "medical")
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in more], lag_ratio=0.3), run_time=1.2)
        two = T("any yes-or-no decision that can be wrong in two ways", 26, INK).next_to(more, DOWN, buff=0.5)
        self.word("s193", "Anywhere")
        self.play(FadeIn(two), run_time=0.5)
        self.until(SEGS["s193"]["end"] + 0.1)
        self.play(FadeOut(VGroup(more, two, small)), run_time=0.5)
        self.finish()
