import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

STEPS = [  # (segment, colour, heading, one line)
    ("s111", BLUE_, "State the null", "the boring explanation"),
    ("s112", VIOLET, "Choose α first", "before you look (often 0.05)"),
    ("s113", INK, "Picture chance", "the distribution if H₀ is true"),
    ("s114", AQUA, "Find the tail", "share at least as extreme"),
    ("s115", ORANGE_, "Decide, then size it", "p vs α, plus effect size"),
]


def icon(k):
    if k == 0:
        return coin("H", BLUE_, 0.26)
    if k == 1:
        return VGroup(Line(DOWN * 0.3, UP * 0.3).set_stroke(VIOLET, 6), T("α", 24, VIOLET, weight=BOLD).shift(RIGHT * 0.22 + UP * 0.12))
    xs = np.linspace(-0.4, 0.4, 30)
    cv = VMobject().set_points_smoothly([np.array([x, -0.2 + 0.42 * np.exp(-(x / 0.16) ** 2), 0]) for x in xs])
    if k == 2:
        return cv.set_stroke(INK, 4)
    if k == 3:
        tail = Polygon(*[np.array([x, -0.2 + 0.42 * np.exp(-(x / 0.16) ** 2), 0]) for x in np.linspace(0.18, 0.4, 10)],
                       np.array([0.4, -0.2, 0]), np.array([0.18, -0.2, 0])).set_stroke(width=0).set_fill(AQUA, 1)
        return VGroup(cv.set_stroke(INK2, 3), tail)
    r = VGroup(Rectangle(width=0.7, height=0.24).set_stroke(ORANGE_, 3),
               *[Line(UP * 0.12, UP * 0.02).set_stroke(ORANGE_, 2).shift(LEFT * 0.3 + RIGHT * 0.15 * i) for i in range(5)])
    return r


class S12Recipe(Base):
    CHAPTER = "Recipe"

    def construct(self):
        # ── s110 the recipe card unrolls ──
        self.at("s110", 0.0)
        frame = card(12.4, 5.3, INK2).move_to(UP * 0.35)
        ttl = TB("Hypothesis testing in 5 steps", 40, AQUA).move_to(frame.get_top() + DOWN * 0.48)
        self.play(GrowFromCenter(frame), run_time=0.6)
        self.play(Write(ttl), run_time=0.8)
        rows = VGroup()
        y0 = frame.get_top()[1] - 1.3
        for k, (sid, col, head, line) in enumerate(STEPS):
            num = VGroup(Circle(0.27).set_stroke(width=0).set_fill(col, 1), TB(str(k + 1), 30, BG))
            num[0].qa_container = True; num[1].move_to(num[0])
            ic = icon(k)
            ic.scale_to_fit_height(min(ic.height, 0.5))
            for x in ic.get_family(): x.qa_ignore = True
            h = TB(head, 34, col if col != INK else INK)
            l = T(line, 30, INK2)
            l.scale_to_fit_width(min(l.width, 5.6))
            num.move_to([frame.get_left()[0] + 0.65, y0 - k * 0.88, 0])
            ic.move_to([frame.get_left()[0] + 1.45, y0 - k * 0.88, 0])
            h.move_to([frame.get_left()[0] + 2.0, y0 - k * 0.88, 0], aligned_edge=LEFT)
            l.move_to([frame.get_left()[0] + 6.25, y0 - k * 0.88, 0], aligned_edge=LEFT)
            rows.add(VGroup(num, ic, h, l))
        self.idle(lambda: glint(ttl, AQUA, 6), lambda: pulse(ttl, 1.05))

        # ── s111–s115 one step per line: number pops, icon, heading, then the explanation ──
        for k, (sid, col, head, line) in enumerate(STEPS):
            self.at(sid, 0.0)
            self.idle()
            num, ic, h, l = rows[k]
            self.play(FadeIn(num, scale=0.4), run_time=0.3)
            self.play(FadeIn(ic, shift=RIGHT * 0.2), FadeIn(h, shift=RIGHT * 0.3), ripple(num.get_center(), col, r=0.3, scale=3), run_time=0.5)
            sid_words = SEGS[sid]["text"].split()
            self.until(word_time(sid, min(len(sid_words) - 1, 3)) )
            self.play(FadeIn(l, shift=LEFT * 0.3), run_time=0.5)
            self.idle(lambda h=h: pulse(h, 1.15), lambda r=rows[k]: pulse(r[0], r[1], s=1.35))

        # ── s116 the coffee coin, run through the recipe ──
        self.at("s116", 0.0)
        self.idle()
        strip = VGroup(*[pill(s, c, 26) for s, c in [("H₀: fair coin", BLUE_), ("15 of 20 heads", WARN), ("p ≈ 0.021", AQUA),
                                                      ("< 0.05", VIOLET), ("suspicious → flip more", ORANGE_)]])
        strip.arrange(RIGHT, buff=0.18)
        if strip.width > 13.2: strip.scale_to_fit_width(13.2)
        strip.move_to(DOWN * 2.15)
        self.play(VGroup(frame, ttl, rows).animate.scale(0.86).shift(UP * 0.25), run_time=0.5)
        for s_, w in zip(strip, ["fair", "Fifteen", "two", "Below", "suspicious"]):
            self.word("s116", w, dt=-0.25)
            self.play(FadeIn(s_, shift=UP * 0.3), run_time=0.35)
        cc = coin("H", BLUE_, 0.3).next_to(strip, UP, buff=0.15).align_to(strip, RIGHT)
        self.word("s116", "flipping", dt=-0.3)
        self.play(FadeIn(cc, scale=0.5), run_time=0.3)
        self.idle(lambda: flipping(cc), lambda: pulse(strip[-1], 1.1))

        # ── s117 the closing line ──
        self.at("s117", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(frame, ttl, rows, strip, cc), shift=UP * 0.4), run_time=0.5)
        l1 = T("A p value doesn't tell you what's true.", 44, INK, weight=BOLD)
        l2 = T("It tells you how surprised chance would be.", 44, AQUA, weight=BOLD)
        VGroup(l1, l2).arrange(DOWN, buff=0.45).move_to(UP * 0.4)
        self.play(AddTextLetterByLetter(l1), run_time=1.3)
        self.word("s117", "It", dt=-0.15)
        g2 = glow(l2.copy(), AQUA)
        self.play(AddTextLetterByLetter(l2), run_time=1.3)
        self.play(FadeIn(g2[0]), run_time=0.4)
        self.add(g2[0])
        self.idle(lambda: pulse(l2, 1.05), lambda: glint(l2, AQUA, 6))
        self.until(self.ch["t1"] - 0.55)
        self.idle()
        self.play(FadeOut(VGroup(l1, l2, g2[0])), run_time=0.5)
        self.finish()
