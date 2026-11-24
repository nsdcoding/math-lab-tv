import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def agent(label, color):
    box = card(3.6, 2.6)
    p = person(color, 1.0).move_to(box.get_center() + UP * 0.35)
    t = T(label, 28, INK2).move_to(box.get_bottom() + UP * 0.45)
    return VGroup(box, p, t)


def sale_card(sz, pr):
    h = house_icon(0.8)
    t1 = T(f"{k(sz)} sq ft", 26, INK2).next_to(h, DOWN, buff=0.25)
    t2 = T(f"${pr}k", 34, INK, weight=BOLD).next_to(t1, DOWN, buff=0.16)
    inner = VGroup(h, t1, t2)
    box = card(2.35, inner.height + 0.7).move_to(inner)
    return VGroup(box, h, t1, t2)


class S01Hook(Base):
    CHAPTER = "The Fair Price"

    def construct(self):
        fr = self.camera.frame
        # ── s001 the street, your house ──
        ground = Line(LEFT * 6.3, RIGHT * 6.3, color=GRID, stroke_width=3).move_to(DOWN * 1.1)
        sizes = [0.95, 1.15, 1.0, 1.3, 0.9, 1.1]
        street = VGroup(*[house_icon(w) for w in sizes]).arrange(RIGHT, buff=0.7, aligned_edge=DOWN)
        street.next_to(ground, UP, buff=0).shift(UP * 0.01)
        mine = street[3]
        self.at("s001", 0.0)
        self.play(Create(ground), LaggedStart(*[Create(h) for h in street], lag_ratio=0.15), run_time=2.0)
        self.until(word_time("s001", word_index("s001", "eighteen")) - 0.1)
        self.play(mine.animate.set_stroke(VIOLET, 5), run_time=0.5)
        tag = pill("1,800 sq ft", VIOLET, 32).next_to(mine, UP, buff=0.45)
        self.play(FadeIn(tag, shift=DOWN * 0.2), run_time=0.5)
        you = T("your house", 26, VIOLET).next_to(ground, DOWN, buff=0.25).align_to(mine, LEFT).shift(LEFT * 0.1)
        self.play(FadeIn(you), run_time=0.4)

        # ── s002 two agents ──
        self.at("s002", 0.0)
        mini = VGroup(street, ground, tag, you)
        a1 = agent("agent A", ORANGE_).move_to(LEFT * 3.9 + DOWN * 0.2)
        a2 = agent("agent B", BLUE_).move_to(RIGHT * 3.9 + DOWN * 0.2)
        self.play(FadeOut(mini, shift=UP * 0.4), run_time=0.6)
        self.play(FadeIn(a1, shift=RIGHT * 0.5), FadeIn(a2, shift=LEFT * 0.5), run_time=0.7)

        # ── s003 $260k vs $200k ──
        self.at("s003", 0.2)
        b1 = pill("$260k", ORANGE_, 46).next_to(a1, RIGHT, buff=0.45).shift(UP * 0.55)
        b2 = pill("$200k", BLUE_, 46).next_to(a2, LEFT, buff=0.45).shift(DOWN * 0.55)
        self.play(FadeIn(b1, scale=0.6), run_time=0.5)
        self.until(word_time("s003", word_index("s003", "second")))
        self.play(FadeIn(b2, scale=0.6), run_time=0.5)

        # ── s004 $60k apart ──
        self.at("s004", 0.0)
        gl = pill("$60k apart", WARN, 34).move_to(UP * 2.0)
        gap = VGroup()
        self.play(FadeIn(gl, shift=DOWN * 0.2), run_time=0.7)
        for _ in range(2):
            self.play(gl.animate.scale(1.12), rate_func=there_and_back, run_time=0.6)
        q = T("Who do you believe?", 40, INK, weight=BOLD).move_to(DOWN * 2.2)
        self.play(FadeIn(q), run_time=0.4)

        # ── s005 five sale cards ──
        self.at("s005", 0.0)
        cards = VGroup(*[sale_card(x, y) for x, y in HOUSES]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.15)
        head = T("sold on your street, last year", 30, MUTED).next_to(cards, UP, buff=0.4)
        self.play(FadeOut(VGroup(a1, a2, b1, b2, gap, gl, q)), run_time=0.5)
        self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=DOWN * 0.8) for c in cards], lag_ratio=0.15), run_time=1.5)

        # ── s006 highlight first, last, then the middle ──
        self.at("s006", 0.0)
        self.play(cards[0][0].animate.set_stroke(WARN, 4), run_time=0.4)
        self.until(word_time("s006", word_index("s006", "Three")))
        self.play(cards[0][0].animate.set_stroke(INK2, 2.5), cards[4][0].animate.set_stroke(WARN, 4), run_time=0.4)
        self.until(word_time("s006", word_index("s006", "rest")))
        self.play(cards[4][0].animate.set_stroke(INK2, 2.5), *[c[0].animate.set_stroke(WARN, 4) for c in cards[1:4]], run_time=0.4)
        self.play(*[c[0].animate.set_stroke(INK2, 2.5) for c in cards[1:4]], run_time=0.4)

        # ── s007 onto axes ──
        self.at("s007", 0.0)
        axg = house_axes().move_to(LEFT * 1.0 + UP * 0.3)
        ax = axg.ax
        dots = house_dots(ax)
        self.play(FadeOut(head), cards.animate.scale(0.45).to_edge(UP, buff=0.25).shift(RIGHT * 2.2), run_time=0.6)
        self.play(Create(ax), FadeIn(axg.labs), FadeIn(axg.xt), FadeIn(axg.yt), run_time=0.9)
        self.until(word_time("s007", word_index("s007", "Every")))
        self.play(LaggedStart(*[ReplacementTransform(c, d) for c, d in zip(cards, dots)], lag_ratio=0.15), run_time=1.6)
        one = T("one house", 24, INK2).next_to(dots[2], UP, buff=0.5).shift(LEFT * 0.6)
        ar = Arrow(one.get_bottom(), dots[2].get_center() + UL * 0.1, buff=0.12, color=INK2, stroke_width=3,
                   max_tip_length_to_length_ratio=0.2)
        self.play(FadeIn(one), GrowArrow(ar), run_time=0.5)

        # ── s008 leans upward ──
        self.at("s008", 0.0)
        self.play(FadeOut(VGroup(one, ar)), run_time=0.3)
        guide = DashedLine(ax.c2p(800, 110), ax.c2p(3300, 400), color=MUTED, stroke_width=3, dash_length=0.12)
        self.until(word_time("s008", word_index("s008", "Bigger")))
        self.play(Create(guide), run_time=1.0)
        lean = T("leans upward", 28, MUTED).next_to(ax.c2p(1300, 330), UP, buff=0)
        self.play(FadeIn(lean), run_time=0.4)
        self.play(LaggedStart(*[Indicate(d, color=WARN, scale_factor=1.6) for d in dots], lag_ratio=0.2), run_time=1.6)

        # ── s009 the ruler ──
        self.at("s009", 0.0)
        ruler = price_line(ax, 40, 0.105, 300, 3400)
        self.play(FadeOut(VGroup(guide, lean)), Create(ruler), run_time=1.0)
        self.until(word_time("s009", word_index("s009", "eighteen")))
        vm = DashedLine(ax.c2p(1800, 0), ax.c2p(1800, 395), color=INK2, stroke_width=3)
        vl = T("1,800 sq ft", 24, INK2).next_to(ax.c2p(1800, 395), RIGHT, buff=0.12)
        self.play(Create(vm), FadeIn(vl), run_time=0.6)

        # ── s010 three people, three lines ──
        self.at("s010", 0.0)
        G = [(35, 0.10, BLUE_), (50, 0.10, AQUA), (110, 0.075, ORANGE_)]
        ghosts = VGroup(*[price_line(ax, a, b, 300, 3400, color=c, width=4) for a, b, c in G])
        reads = VGroup()
        for (a, b, c) in G:
            reads.add(T(f"${a + b * 1800:.0f}k", 30, c, weight=BOLD))
        reads.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 5.0 + DOWN * 0.3)
        rt = T("at 1,800 sq ft", 24, MUTED).next_to(reads, UP, buff=0.35)
        pins = VGroup(*[Dot(ax.c2p(1800, a + b * 1800), radius=0.08, color=c) for a, b, c in G])
        self.play(FadeOut(ruler), run_time=0.3)
        self.play(LaggedStart(*[Create(g) for g in ghosts], lag_ratio=0.35), run_time=1.6)
        self.play(FadeIn(rt), LaggedStart(*[AnimationGroup(FadeIn(p, scale=0.5), FadeIn(r, shift=LEFT * 0.2))
                                         for p, r in zip(pins, reads)], lag_ratio=0.3), run_time=1.4)

        # ── s011 one best line, with a score ──
        self.at("s011", 0.0)
        best = price_line(ax, *BEST, 300, 3400)
        self.play(FadeOut(VGroup(ghosts, pins, reads, rt)), Create(best), run_time=1.0)
        score = pill("score: ?", WARN, 32).move_to(RIGHT * 5.0 + UP * 0.6)
        self.until(word_time("s011", word_index("s011", "number")))
        self.play(FadeIn(score, shift=LEFT * 0.3), run_time=0.5)
        self.play(score.animate.scale(1.15), rate_func=there_and_back, run_time=0.8)

        # ── s012 title card ──
        self.at("s012", 0.0)
        title = hook_title()
        self.play(FadeOut(VGroup(axg, dots, best, vm, vl, score), scale=0.9), run_time=0.7)
        self.play(FadeIn(title[0][0], scale=0.85), run_time=0.8)
        self.play(Write(title[0][1]), run_time=0.9)
        self.until(word_time("s012", word_index("s012", "fair")))
        self.play(FadeIn(title[1], shift=UP * 0.2), run_time=0.6)
        self.finish()
