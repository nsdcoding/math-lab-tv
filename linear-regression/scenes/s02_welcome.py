import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

PREVIEWS = [  # (number colour, caption)  -- one per "Today you will learn" sentence
    (ORANGE_, "score a line by its misses"),
    (VIOLET, "find the best line, and read it"),
    (RED_, "when to trust it"),
]


def _mini():
    ax = Axes(x_range=[0, 3500, 500], y_range=[0, 400, 100], x_length=4.6, y_length=2.7,
              axis_config=dict(color=INK2, stroke_width=3, include_tip=False, tick_size=0.05))
    return ax


def preview_visual(k):
    """A small visual (about 9 x 3 units) from the running example for preview k."""
    ax = _mini()
    dots = house_dots(ax, r=0.09)
    if k == 0:
        ln = price_line(ax, 120, 0.06, 0, 3500, width=4)
        bars = VGroup(*[miss_bar(ax, x, y, 120, 0.06, width=5) for x, y in HOUSES])
        return VGroup(ax, ln, bars, dots)
    if k == 1:
        ln = price_line(ax, *BEST, 0, 3500, width=4)
        tri = VGroup(Line(ax.c2p(2200, 270), ax.c2p(3000, 270)), Line(ax.c2p(3000, 270), ax.c2p(3000, 350))).set_stroke(VIOLET, 3)
        return VGroup(ax, ln, tri, dots)
    ax2 = Axes(x_range=[0, 6000, 1000], y_range=[0, 700, 100], x_length=6.4, y_length=2.7,
               axis_config=dict(color=INK2, stroke_width=3, include_tip=False, tick_size=0.05))
    dots = VGroup(*[dot(INK, 0.09).move_to(ax2.c2p(x, y)) for x, y in HOUSES])
    zone = Rectangle(width=ax2.c2p(6000, 0)[0] - ax2.c2p(3300, 0)[0], height=2.7, stroke_width=0,
                     fill_color=RED_, fill_opacity=0.15).move_to(ax2.c2p(4650, 350))
    ln = Line(ax2.c2p(0, 50), ax2.c2p(3000, 350), color=VIOLET, stroke_width=4)
    ext = DashedLine(ax2.c2p(3000, 350), ax2.c2p(6000, 650), color=RED_, stroke_width=4)
    return VGroup(ax2, zone, ln, ext, dots)


class S02Welcome(Base):
    CHAPTER = "Welcome"

    def construct(self):
        seg_welcome, *seg_items = self.ch["segs"]          # welcome line, then the three "you will learn" lines
        title = hook_title()
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
            vis = preview_visual(k).scale(1.35).move_to(UP * 0.2)
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
