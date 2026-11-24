import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cm import *

NEXT_TOPIC = "How Spam Filters Work · Naive Bayes"


def teaser_visual(k):
    if k == 0:
        return TB("?", 120, WARN)
    if k == 1:
        env = envelope(INK2, 3.0)
        words = VGroup(*[pill(w, WARN, 26) for w in ("FREE", "WINNER", "URGENT")]).arrange(RIGHT, buff=0.25)
        words.next_to(env, DOWN, buff=0.35)
        right = T("right 96 times in 100", 26, AQUA, weight=BOLD).next_to(words, DOWN, buff=0.3)
        return VGroup(env, words, right)
    w = VGroup(*[pill(x, WARN, 26) for x in ("free", "winner", "urgent")]).arrange(RIGHT, buff=0.4)
    arrows = VGroup(*[Arrow(p.get_bottom(), p.get_bottom() + DOWN * 0.8, buff=0.1, color=INK2, stroke_width=4) for p in w])
    b = pill("Bayes' theorem, one word at a time", VIOLET, 28).next_to(arrows, DOWN, buff=0.15)
    return VGroup(w, arrows, b)


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
        self.play(Indicate(nx, color=AQUA, scale_factor=1.08), run_time=1.0)
        self.finish()
