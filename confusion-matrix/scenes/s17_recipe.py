import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cm import *

STEPS = [("Draw the grid", "truth = rows, guess = columns"),
         ("Fill the counts", "rows add up to the real totals"),
         ("Precision", "down the alarm column"),
         ("Recall", "across the real row"),
         ("Price the mistakes", "then set the cut-off")]
COLS = [INK, INK, VIOLET, ORANGE_, WARN]


class S17Recipe(Base):
    CHAPTER = "Recipe"

    def construct(self):
        self.at("s201", 0.0)
        ttl = TB("THE RECIPE", 50, AQUA).move_to(UP * 2.55 + RIGHT * 0.2)
        self.play(FadeIn(ttl, shift=DOWN * 0.15), run_time=0.5)
        rows = VGroup()
        for i, (h, e) in enumerate(STEPS):
            num = step_chip(i + 1, h, COLS[i], 30)
            ex = T(e, 26, INK2).next_to(num, RIGHT, buff=0.4)
            rows.add(VGroup(num, ex))
        rows.arrange(DOWN, buff=0.34, aligned_edge=LEFT).move_to(LEFT * 1.6 + DOWN * 0.35)
        # align explanations in one column
        x = max(r[0].get_right()[0] for r in rows) + 0.45
        for r in rows:
            r[1].move_to([x + r[1].width / 2, r[0].get_y(), 0])
        for i, sid in enumerate(("s202", "s203", "s204", "s205", "s206")):
            self.at(sid, 0.0)
            self.play(FadeIn(rows[i][0], shift=RIGHT * 0.15), run_time=0.5)
            self.play(FadeIn(rows[i][1]), run_time=0.4)
        # ── s207 try it on Detector A ──
        self.at("s207", 0.0)
        self.play(FadeOut(VGroup(*[r[1] for r in rows])), run_time=0.4)
        chips = VGroup(*[r[0] for r in rows])
        self.play(chips.animate.scale(0.85).to_edge(LEFT, buff=0.8).set_y(-0.1), run_time=0.6)
        g = mini_grid(A_COUNTS, 0.45, RIGHT * 4.6 + UP * 0.4)
        self.word("s207", "grid:")
        self.play(FadeIn(grid_mobs(g)), run_time=0.5)
        vals = [T("✓ 90 · 10 · 30 · 9,870", 24, AQUA, weight=BOLD), T("✓ rows: 100 and 9,900", 24, AQUA, weight=BOLD),
                T("3 in 4", 26, VIOLET, weight=BOLD), T("9 in 10", 26, ORANGE_, weight=BOLD), T("misses cost more → recall", 24, WARN, weight=BOLD)]
        xv = max(c.get_right()[0] for c in chips) + 0.4
        for v, c in zip(vals, chips):
            v.move_to([xv + v.width / 2, c.get_y(), 0])
        self.play(FadeIn(vals[0]), FadeIn(vals[1]), run_time=0.5)
        self.word("s207", "Precision:")
        self.play(FadeIn(vals[2]), g.light("TP", VIOLET), g.light("FP", VIOLET), run_time=0.5)
        self.word("s207", "Recall:")
        self.play(FadeIn(vals[3]), g.unlight("FP"), g.light("TP", ORANGE_), g.light("FN", ORANGE_), run_time=0.5)
        self.word("s207", "misses")
        self.play(FadeIn(vals[4]), run_time=0.5)
        # ── s208 the closing line ──
        self.at("s208", 0.0)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        cl = VGroup(T("A detector isn't good or bad on its own.", 40, INK, weight=BOLD, display=True),
                    T("It's good or bad at the mistakes you can afford.", 40, VIOLET, weight=BOLD, display=True)).arrange(DOWN, buff=0.35)
        cl.move_to(UP * 0.3)
        self.play(FadeIn(cl[0], shift=UP * 0.15), run_time=0.6)
        self.word("s208", "It's")
        self.play(FadeIn(cl[1], shift=UP * 0.15), run_time=0.6)
        self.until(SEGS["s208"]["end"] + 0.2)
        self.play(FadeOut(cl), run_time=0.5)
        self.finish()
