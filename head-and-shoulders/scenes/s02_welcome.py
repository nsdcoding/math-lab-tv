import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

# FILL: the topic title card (identical to the one that ends the hook scene) and the three previews.
TITLE = ("HEAD & SHOULDERS", "explained simply, with real numbers")
PREVIEWS = [  # (number colour, caption)  -- one per "Today you will learn" sentence
    (ORANGE_, "spot the three peaks"),
    (WARN, "find the neckline"),
    (VIOLET, "measure a price target"),
]


def preview_visual(k):
    if k == 0:
        m = mini_hs(5.0, 2.2)
        dots = VGroup(*[Dot(m.get_points()[i], radius=0.1, color=c) for i, c in ((8, SH_COL), (16, HEAD_COL), (24, SH_COL))])
        return VGroup(m, dots)
    if k == 1:
        m = mini_hs(5.0, 2.2)
        y = m.get_points()[12][1]
        nl = Line([m.get_left()[0] + 0.6, y, 0], [m.get_right()[0], y, 0], color=NECK_COL, stroke_width=5)
        return VGroup(m, nl)
    row1 = VGroup(T("70", 44, HEAD_COL, weight=BOLD), T("−", 44, MUTED), T("52", 44, NECK_COL, weight=BOLD),
                  T("=", 44, MUTED), T("18", 44, TGT_COL, weight=BOLD)).arrange(RIGHT, buff=0.3)
    row2 = VGroup(T("52", 44, NECK_COL, weight=BOLD), T("−", 44, MUTED), T("18", 44, TGT_COL, weight=BOLD),
                  T("=", 44, MUTED), T("34", 44, TGT_COL, weight=BOLD)).arrange(RIGHT, buff=0.3)
    return VGroup(row1, row2).arrange(DOWN, buff=0.45)


class S02Welcome(Base):
    CHAPTER = "Welcome"

    def construct(self):
        seg_welcome, *seg_items = self.ch["segs"]          # welcome line, then the three "you will learn" lines
        title = title_card(*TITLE, size=96)
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
