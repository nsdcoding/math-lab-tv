import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *

# FILL: the topic title card (identical to the one that ends the hook scene) and the three previews.
TITLE = ("PROBABILITY", "from absolute zero, in one hour")
PREVIEWS = [  # (number colour, caption)  -- one per "Today you will learn" sentence
    (AQUA, "what probability is, and how to count it"),
    (VIOLET, "the three magic words"),
    (WARN, "new information, and the traps"),
]


def preview_visual(k):
    if k == 0:
        pl = prob_line(7.0, fs=26, title="how likely")
        pn = pin(pl.nl, 1 / 6, VIOLET, "1/6", h=0.7)
        return VGroup(pl, pn)
    if k == 1:
        return VGroup(*[pill(w, c, 44) for w, c in (("NOT", BLUE_), ("OR", AQUA), ("AND", ORANGE_))]).arrange(RIGHT, buff=0.6)
    g = DiceGrid(0.34, fs=18, titles=False)
    for (o, b), s in g.cells.items():
        if o == 6:
            s.set_fill(WARN, 0.8)
        else:
            s.set_fill(CELL_FILL, 0.35)
    st = stamp("trap!", RED_, 34).next_to(g, RIGHT, buff=0.9)
    return VGroup(g, st)


class S02Welcome(PBase):
    CHAPTER = "Welcome"

    def construct(self):
        seg_welcome, *seg_items = self.ch["segs"]          # welcome line, then the three "you will learn" lines
        title = title_card(*TITLE)
        self.add(title)
        # ── "Welcome to Math Lab TV. Where math is something you can see." (word for word) ──
        self.at(seg_welcome, 0.0)
        lg = logo(1.15, tagline=True).move_to(UP * 0.4)
        mark, name, tag = lg[0][0], lg[0][1], lg[1]
        self.play(FadeOut(title, scale=0.85), run_time=0.5)
        self.play(DrawBorderThenFill(mark[0]), run_time=0.6)
        self.play(Create(mark[1]), FadeIn(name, shift=LEFT * 0.3), run_time=0.8)
        self.until(word_time(seg_welcome, word_index(seg_welcome, "where")) - 0.1)
        self.play(AddTextLetterByLetter(tag), run_time=1.2)
        # ── numbered preview 1, 2, 3; small logo stays top-right ──
        small = logo(0.42).to_edge(UP, buff=0.32).to_edge(RIGHT, buff=0.45)
        learn = T("TODAY YOU WILL LEARN", 24, MUTED, weight=BOLD).next_to(small, LEFT, buff=0.5)
        prev = None
        for k, sid in enumerate(seg_items[:3]):
            self.at(sid, 0.0)
            col, cap = PREVIEWS[k]
            num = TB(str(k + 1), 72, col).move_to(UP * 2.45)
            vis = preview_visual(k).move_to(UP * 0.2)
            c_ = T(cap, 34, INK).move_to(DOWN * 2.0)
            if k == 0:
                self.play(ReplacementTransform(lg[0], small), FadeOut(tag), FadeIn(learn), run_time=0.8)
            else:
                self.play(FadeOut(prev, shift=LEFT * 1.0), run_time=0.5)
            self.play(FadeIn(num, scale=0.5), FadeIn(vis), FadeIn(c_), run_time=0.9)
            prev = VGroup(num, vis, c_)
        self.until(SEGS[seg_items[-1]]["end"] + 0.1)
        self.play(FadeOut(VGroup(small, learn, prev)), run_time=0.4)
        self.finish()
