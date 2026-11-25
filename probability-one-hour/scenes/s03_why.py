import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *


def ecard(icon, title, color, w=3.1, h=3.0):
    box = card(w, h, color)
    icon.move_to(box.get_center() + UP * 0.45)
    t = T(title, 26, INK, weight=BOLD).move_to(box.get_center() + DOWN * 0.9)
    if t.width > w - 0.4:
        t.scale_to_fit_width(w - 0.4)
    return VGroup(box, icon, t)


class S03Why(PBase):
    CHAPTER = "Why It Matters"

    def construct(self):
        self.at("s016")
        q = boxed(TB("Why care?", 80, WARN), WARN, pad=0.45)
        self.play(FadeIn(q, scale=0.8), run_time=0.7)
        # s017 four empty cards
        self.at("s017")
        slots = VGroup(*[card(3.1, 3.0, GRID) for _ in range(4)]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.2)
        self.play(q.animate.scale(0.55).move_to(UP * 2.85), LaggedStart(*[FadeIn(s, shift=UP * 0.3) for s in slots], lag_ratio=0.15), run_time=1.0)
        # s018 weather
        self.at("s018")
        c1 = ecard(ic_cloud(BLUE_, 1.1), "70% chance of rain", BLUE_).move_to(slots[0])
        m = VGroup(Rectangle(width=2.3, height=0.18, stroke_color=INK2, stroke_width=2, fill_opacity=0))
        mf = Rectangle(width=2.3 * 0.7, height=0.18, stroke_width=0, fill_color=BLUE_, fill_opacity=0.9)
        m.move_to(c1[0].get_center() + DOWN * 0.35); mf.align_to(m, LEFT).move_to([mf.get_center()[0], m.get_center()[1], 0])
        mf.align_to(m[0], LEFT)
        self.play(FadeOut(slots[0]), FadeIn(c1), run_time=0.6)
        self.w("s018", "seventy")
        self.play(Create(m), GrowFromEdge(mf, LEFT), run_time=0.8)
        # s019 quiz
        self.at("s019")
        c2 = ecard(ic_quiz(INK2, 1.0), "1 chance in 4", AQUA).move_to(slots[1])
        self.play(FadeOut(slots[1]), FadeIn(c2), run_time=0.6)
        self.w("s019", "one")
        self.play(Indicate(c2[2], color=AQUA), run_time=0.8)
        # s020 fair
        self.at("s020")
        sp = spinner([(0.25, ORANGE_), (0.25, BLUE_), (0.25, AQUA), (0.25, VIOLET)], r=0.62)
        c3 = ecard(sp, "worth playing?", ORANGE_).move_to(slots[2])
        self.play(FadeOut(slots[2]), FadeIn(c3), run_time=0.6)
        self.play(Rotate(sp, -TAU * 1.3, about_point=sp.get_center()), run_time=1.6, rate_func=rate_functions.ease_out_cubic)
        # s021 doctor / sports
        self.at("s021")
        ic = VGroup(ic_bottle(AQUA, 0.9), ic_trophy(WARN, 1.0)).arrange(RIGHT, buff=0.4)
        c4 = ecard(ic, "medicine · sports", VIOLET).move_to(slots[3])
        self.play(FadeOut(slots[3]), FadeIn(c4), run_time=0.6)
        self.w("s021", "sports")
        self.play(Wiggle(ic[1]), run_time=0.8)
        # s022 due for a win
        self.at("s022")
        cards = VGroup(c1, c2, c3, c4)
        self.play(FadeOut(cards), FadeOut(m), FadeOut(mf), run_time=0.5)
        self.drop(cards, m, mf)
        bub = boxed(T("I've lost 5 times in a row,\nso I'm due for a win!", 40, INK, line_spacing=1.2), INK2, pad=0.45).move_to(UP * 1.0)
        self.play(FadeIn(bub, shift=UP * 0.3), run_time=0.6)
        st = stamp("probability mistake", RED_, 36).next_to(bub, DOWN, buff=0.45)
        self.w("s022", "mistake")
        self.play(FadeIn(st, scale=1.4), run_time=0.4)
        later = T("we'll fix this one later", 28, MUTED).next_to(st, DOWN, buff=0.3)
        self.w("s022", "fix")
        self.play(FadeIn(later), run_time=0.5)
        # s023 the math of not knowing
        self.at("s023")
        self.play(FadeOut(VGroup(bub, st, later, q)), run_time=0.4)
        self.drop(bub, st, later, q)
        phrase = big_word("the math of not knowing for sure", VIOLET, 60).move_to(UP * 0.3)
        self.play(Write(phrase[1]), FadeIn(phrase[0]), run_time=1.4)
        # s022a little bets
        self.at("s022a")
        icons = [ic_cloud(BLUE_, 0.8, rain=False), ic_ball(ORANGE_, 1.0), ic_quiz(INK2, 0.8, None), die(5, ORANGE_, 0.75), ic_jacket(BLUE_, 1.0)]
        words = ["games", "sports", "quizzes", "weather", "jacket"]
        pos = [LEFT * 5 + UP * 2.1, LEFT * 2.5 + DOWN * 1.6, UP * 2.2 + RIGHT * 0.3, RIGHT * 2.8 + DOWN * 1.6, RIGHT * 5 + UP * 2.1]
        order = [3, 1, 2, 0, 4]
        for k in order:
            icons[k].move_to(pos[k])
        self.play(phrase.animate.scale(0.75), run_time=0.4)
        for k, w in zip(order, words):
            self.w("s022a", w)
            self.play(FadeIn(icons[k], scale=0.6), run_time=0.35)
        bets = T("little bets about an uncertain future", 34, WARN, weight=BOLD).next_to(phrase, DOWN, buff=0.35)
        self.w("s022a", "little")
        self.play(FadeIn(bets, shift=UP * 0.2), run_time=0.6)
        # s024 next roll vs what tends to happen
        self.at("s024")
        self.play(FadeOut(VGroup(phrase, bets, *icons)), run_time=0.4)
        self.drop(phrase, bets, *icons)
        dq = die_q(ORANGE_, 1.6).move_to(LEFT * 3.5 + UP * 0.2)
        l1 = T("next roll: ?", 32, INK2).next_to(dq, DOWN, buff=0.4)
        self.play(FadeIn(dq, scale=0.7), FadeIn(l1), run_time=0.6)
        self.play(Rotate(dq, TAU), run_time=0.8)
        ax = bar_axes(["2", "", "", "", "", "7", "", "", "", "", "12"], 6, 2, 5.2, 2.6, "total", "")
        ax.move_to(RIGHT * 3.2 + UP * 0.25)
        bb = bars(ax.ax, [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1], AQUA, width=0.36, op=0.75)
        l2 = T("what tends to happen", 32, AQUA).next_to(ax, UP, buff=0.3)
        self.w("s024", "tends")
        self.play(FadeIn(ax), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bb], lag_ratio=0.08), FadeIn(l2), run_time=1.3)
        # s025 first brick
        self.at("s025")
        self.play(FadeOut(VGroup(dq, l1, ax, bb, l2)), run_time=0.4)
        self.drop(dq, l1, ax, bb, l2)
        base = Line(LEFT * 3, RIGHT * 3, color=INK2, stroke_width=4).move_to(DOWN * 1.2)
        brick = Rectangle(width=1.6, height=0.7, stroke_color=WARN, stroke_width=4, fill_color=PANEL, fill_opacity=1).move_to(UP * 2.0)
        self.play(Create(base), run_time=0.4)
        self.play(brick.animate.next_to(base, UP, buff=0), run_time=0.6, rate_func=rate_functions.ease_in_quad)
        self.finish()
