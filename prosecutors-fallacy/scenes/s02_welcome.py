import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

TITLE = ("The Prosecutor's Fallacy", "the statistics trap smart people fall for")
TITLE_SIZE = 74
PREVIEWS = [  # (number colour, caption)
    (VIOLET, "two different questions"),
    (AQUA, "count the crowd"),
    (ORANGE_, "catch the swap anywhere"),
]


def preview_visual(k):
    if k == 0:
        a = cond("match", "innocent", 38); b = cond("innocent", "match", 38)
        ne = TB("≠", 64, RED_)
        return VGroup(a, ne, b).arrange(RIGHT, buff=0.45)
    if k == 1:
        rng = np.random.default_rng(4)
        cells = VGroup(*[Square(0.2, stroke_width=0, fill_color=BLUE_, fill_opacity=0.75) for _ in range(30 * 10)])
        cells.arrange_in_grid(10, 30, buff=0.07)
        for i in rng.choice(300, 8, replace=False):
            cells[i].set_fill(WARN, 1)
        cells[155].set_fill(ORANGE_, 1)
        return cells
    rows = VGroup(*[VGroup(check(AQUA, 0.3), T(t, 30, INK)).arrange(RIGHT, buff=0.3)
                    for t in ("courtrooms", "medical tests", "the news")]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    return rows


class S02Welcome(Base):
    CHAPTER = "Welcome"

    def construct(self):
        seg_welcome, *seg_items = self.ch["segs"]          # welcome line, then the three "you will learn" lines
        title = title_card(*TITLE, size=TITLE_SIZE)
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
