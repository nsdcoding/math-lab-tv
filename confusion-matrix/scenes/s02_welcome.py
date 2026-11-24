import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cm import *

PREVIEWS = [  # (number colour, caption)  -- one per "Today you will learn" sentence
    (AQUA, "the four outcomes, filled from real counts"),
    (VIOLET, "why accuracy lies · precision and recall"),
    (ORANGE_, "four worked examples"),
]


def mini(counts=None, lit=(), col=None, row=None, s=0.62):
    g = Grid(counts=counts, names=False, rows=("", ""), cols=("", ""), row_title="", col_title="", num_size=56)
    for k in lit:
        g.cell[k].set_stroke(COL[k], 4).set_fill(tint(COL[k]), 1)
    out = VGroup(g.cells, g.nums)
    if col:
        out.add(g.frame_of(g.col0(), col))
    if row:
        out.add(g.frame_of(g.row0(), row))
    return out.scale(s)


def preview_visual(k):
    if k == 0:
        return mini(dict(TP=90, FN=10, FP=30, TN=9870), lit=KEYS, s=0.85)
    if k == 1:
        a = mini(dict(TP=90, FN=10, FP=30, TN=9870), col=VIOLET)
        b = mini(dict(TP=90, FN=10, FP=30, TN=9870), row=ORANGE_)
        la = T("precision", 26, VIOLET, weight=BOLD).next_to(a, DOWN, buff=0.2)
        lb = T("recall", 26, ORANGE_, weight=BOLD).next_to(b, DOWN, buff=0.2)
        return VGroup(VGroup(a, la), VGroup(b, lb)).arrange(RIGHT, buff=1.2)
    ex = [("fraud", dict(TP=90, FN=10, FP=30, TN=9870)), ("medical test", dict(TP=9, FN=1, FP=99, TN=891)),
          ("spam", dict(TP=270, FN=30, FP=10, TN=690)), ("loans", dict(TP=150, FN=50, FP=100, TN=1700))]
    items = VGroup()
    for name, c in ex:
        m = mini(c, lit=KEYS, s=0.4)
        items.add(VGroup(m, T(name, 24, INK2, weight=BOLD).next_to(m, DOWN, buff=0.18)))
    return items.arrange(RIGHT, buff=0.45)


class S02Welcome(Base):
    CHAPTER = "Welcome"

    def construct(self):
        seg_welcome, *seg_items = self.ch["segs"]          # welcome line, then the three "you will learn" lines
        title = the_title()
        self.add(title)
        # ── "Welcome to Math Lab TV. Where math is something you can see." (word for word) ──
        self.at(seg_welcome, 0.0)
        lg = logo(1.15, tagline=True).move_to(UP * 0.4)
        mark, name, tag = lg[0][0], lg[0][1], lg[1]
        self.play(FadeOut(title), run_time=0.5)
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
            self.play(FadeIn(num, shift=DOWN * 0.15), FadeIn(vis), FadeIn(c_), run_time=0.9)
            prev = VGroup(num, vis, c_)
        self.until(SEGS[seg_items[-1]]["end"] + 0.1)
        self.play(FadeOut(VGroup(small, learn, prev)), run_time=0.4)
        self.finish()
