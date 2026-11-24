import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

STEPS = [("Plot and look", "the dots should lean along a line", INK),
         ("Measure the misses", "straight up and down, in the units you predict", ORANGE_),
         ("Square and add", "the total is the score: sum of squared errors", AQUA),
         ("Find the best line", "slope from the formula, then the intercept", VIOLET),
         ("Read and predict", "slope = a rate; predict only inside the data", WARN)]


class S12Recipe(Base):
    CHAPTER = "Recipe"

    def construct(self):
        self.at("s116", 0.0)
        title = T("THE RECIPE", 34, VIOLET, weight=BOLD).move_to(UP * 2.6)
        box = card(13.0, 3.95).move_to(UP * 0.2)
        self.play(FadeIn(title), FadeIn(box), run_time=0.6)
        rows = VGroup()
        for i, (h, d, col) in enumerate(STEPS):
            y = 1.64 - 0.72 * i
            num = step_chip(i + 1, "", col, 26)[:2].move_to([-6.0, y, 0])
            hh = T(h, 28, col, weight=BOLD).move_to([-5.55, y, 0], aligned_edge=LEFT)
            dd = T(d, 24, INK2).move_to([-1.55, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(num, hh, dd))
        for i, sid in enumerate(["s117", "s118", "s119", "s120", "s121"]):
            self.at(sid, 0.0)
            self.play(FadeIn(rows[i][:2], shift=RIGHT * 0.2), run_time=0.45)
            self.play(FadeIn(rows[i][2]), run_time=0.45)
        self.at("s122", 0.0)
        close = T("A line does not know the truth.", 28, INK, weight=BOLD)
        close2 = T("It is just the one guess that misses least.", 28, VIOLET, weight=BOLD)
        cl = VGroup(close, close2).arrange(DOWN, buff=0.12)
        self.play(VGroup(title, box, rows).animate.shift(UP * 0.25), run_time=0.4)
        cl.next_to(box, DOWN, buff=0.18)
        self.play(FadeIn(close), run_time=0.6)
        self.until(word_time("s122", word_index("s122", "It")))
        self.play(FadeIn(close2), run_time=0.6)
        self.until(SEGS["s122"]["end"] + 0.9)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.45)
        self.finish()
