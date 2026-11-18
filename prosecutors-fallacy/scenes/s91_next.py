import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

NEXT_TOPIC = "the confusion matrix"


def teaser_visual(k):
    if k == 0:
        pz = VGroup(Square(1.0).set_stroke(AQUA, 4), TB("?", 56, AQUA))
        pz[1].move_to(pz[0])
        return pz
    if k == 1:
        a = result_card("model A", "catches 90% of fraud", ORANGE_, 26, 34)
        b = result_card("model B", "90% of its alarms are real", VIOLET, 26, 34)
        q = TB("=?", 48, RED_)
        return VGroup(a, q, b).arrange(RIGHT, buff=0.4)
    cells = VGroup(*[card(2.0, 1.1, c) for c in (AQUA, RED_, RED_, AQUA)]).arrange_in_grid(2, 2, buff=0.12)
    labs = VGroup(T("caught", 24, INK), T("false alarm", 24, INK), T("missed", 24, INK), T("all clear", 24, INK))
    for l_, c in zip(labs, cells):
        l_.move_to(c)
    return VGroup(cells, labs)


class S91Next(Base):
    CHAPTER = "Next Time"

    def construct(self):
        lg = logo(1.1).move_to(UP * 1.1).scale(0.42).to_edge(UP, buff=0.32)   # carried over from Subscribe
        self.add(lg)
        segs = self.ch["segs"]
        prev = None
        for k, sid in enumerate(segs[:-1]):
            self.at(sid, 0.0)
            v = teaser_visual(k).move_to(UP * 0.3)
            self.play(*([FadeOut(prev)] if prev else []), FadeIn(v, shift=UP * 0.2), run_time=0.6)
            prev = v
            if k == len(segs) - 2:
                nx = chip(f"next:  {NEXT_TOPIC}", AQUA, 30).next_to(lg, DOWN, buff=0.3)
                self.play(FadeIn(nx, shift=DOWN * 0.2), run_time=0.6)
        # ── "I will see you in the next video." (word for word) ──
        self.at(segs[-1], 0.0)
        self.play(pulse(nx, s=1.1), run_time=1.0)
        self.finish()
