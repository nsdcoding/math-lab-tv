import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

STEPS = [("Start with an uptrend", "the pattern reverses a rise", AQUA),
         ("Find three peaks", "the head is the highest", HEAD_COL),
         ("Draw the neckline", "through the two dips", NECK_COL),
         ("Wait for a close below", "no close, no pattern", INK),
         ("Measure, copy down, set a stop", "70 − 52 = 18  →  52 − 18 = 34", TGT_COL)]


class S07Recap(Base):
    CHAPTER = "Recap"

    def construct(self):
        self.at("s037", 0.0)
        ttl = TB("THE RECIPE", 44, VIOLET)
        rows = VGroup()
        for k, (h, sub, col) in enumerate(STEPS):
            ch = step_chip(k + 1, h, col, 32)
            s = T(sub, 24, INK2).next_to(ch, RIGHT, buff=0.4)
            rows.add(VGroup(ch, s))
        rows.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        box = card(rows.width + 1.0, rows.height + 0.8, INK2)
        body = VGroup(box, rows); rows.move_to(box)
        close = T("A pattern is not a prediction. It is a way to plan your risk.", 30, VIOLET, weight=BOLD)
        VGroup(ttl, body, close).arrange(DOWN, buff=0.25).move_to(UP * 0.6)
        self.play(FadeIn(ttl), FadeIn(box), run_time=0.7)
        for k, sid in enumerate(["s038", "s039", "s040", "s041", "s042"]):
            self.at(sid, 0.0)
            self.play(FadeIn(rows[k], shift=RIGHT * 0.3), run_time=0.6)
        self.at("s043", 0.0)
        self.play(FadeIn(close, shift=UP * 0.15), run_time=0.8)
        self.until(SEGS["s043"]["end"] + 0.4)
        self.play(FadeOut(VGroup(ttl, body, close)), run_time=0.5)
        self.finish()
