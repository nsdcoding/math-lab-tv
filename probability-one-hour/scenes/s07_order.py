import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *


class S07Order(PBase):
    CHAPTER = "Putting Things in Order"

    def construct(self):
        self.at("s111")
        hd = header("how many orders?", INK, 32)
        shelf = Line(LEFT * 3, RIGHT * 3, color=INK2, stroke_width=5).move_to(DOWN * 0.6)
        books = VGroup(ic_book("A", ORANGE_), ic_book("B", BLUE_), ic_book("C", AQUA)).arrange(RIGHT, buff=0.25)
        books.next_to(shelf, UP, buff=0.02)
        self.play(FadeIn(hd), Create(shelf), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.4) for b in books], lag_ratio=0.2), run_time=0.9)
        # s112 shuffle
        self.at("s112")
        self.w("s112", "random")
        self.play(books[0].animate.move_to(books[2].get_center()), books[2].animate.move_to(books[0].get_center()), run_time=0.6)
        self.play(books[0].animate.move_to(books[1].get_center()), books[1].animate.move_to(books[0].get_center()), run_time=0.6)
        # s113 3,2,1 slots
        self.at("s113")
        self.play(FadeOut(VGroup(books, shelf)), run_time=0.4)
        slots = VGroup(*[RoundedRectangle(corner_radius=0.12, width=1.6, height=1.8, stroke_color=INK2, stroke_width=3,
                                          fill_color=PANEL, fill_opacity=1) for _ in range(3)]).arrange(RIGHT, buff=0.6).move_to(UP * 0.6)
        for s in slots: s.qa_container = True
        lbl = VGroup(*[T(t, 24, MUTED).next_to(s, DOWN, buff=0.2) for t, s in zip(("1st spot", "2nd spot", "3rd spot"), slots)])
        self.play(FadeIn(slots), FadeIn(lbl), run_time=0.5)
        ns = VGroup(*[TB(str(n), 70, WARN).move_to(s) for n, s in zip((3, 2, 1), slots)])
        for k, w in enumerate(("three", "two", "one")):
            self.w("s113", w)
            self.play(FadeIn(ns[k], scale=0.5), run_time=0.4)
        # s114 6 orders
        self.at("s114")
        e = TB("3 × 2 × 1 = 6", 56, WARN).move_to(DOWN * 1.7)
        self.play(Write(e), run_time=0.8)
        # s115 list + ABC
        self.at("s115")
        self.play(FadeOut(VGroup(slots, lbl, ns)), e.animate.scale(0.7).move_to(UP * 1.9), run_time=0.5)
        orders = ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]
        lst = VGroup(*[pill(o, INK2, 36) for o in orders]).arrange(RIGHT, buff=0.35).move_to(UP * 0.5)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.2) for x in lst], lag_ratio=0.1), run_time=0.8)
        f = MathTex(r"P(\text{A, B, C in order}) = {1 \over 6}", font_size=60, color=VIOLET).move_to(DOWN * 1.2)
        self.w("s115", "alphabetical")
        self.play(lst[0][0].animate.set_stroke(AQUA, 4), lst[0][1].animate.set_color(AQUA), run_time=0.5)
        self.w("s115", "one")
        self.play(Write(f), run_time=0.8)
        # s116 ten books
        self.at("s116")
        self.play(FadeOut(VGroup(lst, f, e)), run_time=0.4)
        cols = [ORANGE_, BLUE_, AQUA, VIOLET, WARN, RED_, INK2, ORANGE_, BLUE_, AQUA]
        tb = VGroup(*[ic_book(str(k + 1), cols[k], 0.6, 1.3) for k in range(10)]).arrange(RIGHT, buff=0.12).move_to(UP * 0.9)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in tb], lag_ratio=0.06), run_time=1.0)
        e10 = TB("10 × 9 × 8 × … × 1", 52, WARN).move_to(DOWN * 0.7)
        self.w("s116", "ten", nth=1)
        self.play(Write(e10), run_time=0.9)
        r10 = TB("= 3,628,800", 56, WARN).next_to(e10, DOWN, buff=0.3)
        self.w("s116", "three")
        self.play(FadeIn(r10, shift=UP * 0.2), run_time=0.6)
        # s117 tiny chance
        self.at("s117")
        self.play(FadeOut(VGroup(tb, e10)), r10.animate.move_to(UP * 1.6), run_time=0.5)
        pl = prob_line(10.0, fs=26, title="how likely").move_to(DOWN * 0.8)
        pn = pin(pl.nl, 0.0, VIOLET, "1 in 3.6 million", h=0.75, fs=28)
        pn.lab.shift(RIGHT * 1.3)
        self.play(FadeIn(pl), run_time=0.5)
        self.play(FadeIn(pn, shift=DOWN * 0.2), run_time=0.6)
        # s118 deck
        self.at("s118")
        self.play(FadeOut(VGroup(r10, pl, pn)), run_time=0.4)
        fan = VGroup(*[ic_card(INK2, 1.0, 1.4) for _ in range(9)])
        for k, c in enumerate(fan):
            c.rotate((k - 4) * 0.12, about_point=ORIGIN + DOWN * 2.5).shift(RIGHT * (k - 4) * 0.35)
        fan.move_to(UP * 0.6)
        self.play(LaggedStart(*[FadeIn(c) for c in fan], lag_ratio=0.08), run_time=0.9)
        tm = pill("too many orders to ever repeat", WARN, 34).move_to(DOWN * 1.6)
        self.w("s118", "never")
        self.play(FadeIn(tm, shift=UP * 0.2), run_time=0.6)
        # s119 lottery balls
        self.at("s119")
        self.play(FadeOut(VGroup(fan, tm)), run_time=0.4)
        hd2 = header("a lottery: pick 6 numbers from 49", INK, 32)
        self.play(FadeOut(hd), FadeIn(hd2), run_time=0.5); hd = hd2
        balls = VGroup()
        for k in range(49):
            r_, c_ = k // 7, k % 7
            b = Circle(0.24, stroke_color=INK2, stroke_width=2, fill_color=PANEL, fill_opacity=1)
            b.qa_container = True
            t = T(str(k + 1), 18, INK2).move_to(b)
            balls.add(VGroup(b, t).move_to(LEFT * 3.6 + RIGHT * c_ * 0.6 + UP * (1.8 - r_ * 0.6)))
        self.play(FadeIn(balls, lag_ratio=0.01), run_time=1.0)
        pick = [3, 11, 17, 26, 38, 44]
        self.w("s119", "six")
        self.play(*[balls[k][0].animate.set_stroke(AQUA, 4) for k in pick], *[balls[k][1].animate.set_color(AQUA) for k in pick], run_time=0.7)
        nm = T("order doesn't matter", 30, WARN, weight=BOLD).move_to(RIGHT * 3.5 + UP * 1.6)
        self.w("s119", "order")
        self.play(FadeIn(nm), run_time=0.5)
        # s120 ordered count
        self.at("s120")
        e1 = MathTex(r"49 \times 48 \times 47", r"\times 46 \times 45 \times 44", font_size=48, color=INK).move_to(RIGHT * 3.4 + UP * 0.6)
        e1.arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(RIGHT * 3.4 + UP * 0.5)
        self.play(Write(e1[0]), run_time=1.5)
        self.w("s120", "forty", nth=3)
        self.play(Write(e1[1]), run_time=1.6)
        # s121 divide by 720
        self.at("s121")
        e2 = MathTex(r"\div (6 \times 5 \times 4 \times 3 \times 2 \times 1)", font_size=40, color=INK2).next_to(e1, DOWN, buff=0.35)
        self.w("s121", "six")
        self.play(Write(e2), run_time=1.6)
        e3 = MathTex(r"= \div\, 720", font_size=48, color=INK2).next_to(e2, DOWN, buff=0.25)
        self.w("s121", "seven")
        self.play(FadeIn(e3), run_time=0.5)
        # s122 result
        self.at("s122")
        res = TB("= 13,983,816 tickets", 46, WARN).next_to(e3, DOWN, buff=0.35)
        self.play(FadeIn(res, shift=UP * 0.2), run_time=0.6)
        # s123 line
        self.at("s123")
        self.play(FadeOut(VGroup(balls, nm, e1, e2, e3)), res.animate.move_to(UP * 1.7), run_time=0.5)
        pl = prob_line(10.0, fs=26, title="how likely").move_to(DOWN * 0.8)
        pn = pin(pl.nl, 0.0, RED_, "1 in 14 million", h=0.75, fs=28)
        pn.lab.shift(RIGHT * 1.3)
        self.play(FadeIn(pl), run_time=0.5)
        self.w("s123", "remember")
        self.play(FadeIn(pn, shift=DOWN * 0.2), run_time=0.6)
        self.play(Indicate(pn.tri, color=RED_, scale_factor=2), run_time=0.8)
        # s124 a quarter of a million years
        self.at("s124")
        self.play(FadeOut(VGroup(pl, pn, res)), run_time=0.4)
        tl = Arrow(LEFT * 6.2, RIGHT * 6.6, color=WARN, stroke_width=6, buff=0).move_to(DOWN * 0.2)
        tks = VGroup(*[Line(UP * 0.15, DOWN * 0.15, color=WARN).move_to(tl.get_start() + RIGHT * (0.4 + k * 0.6)) for k in range(20)])
        tt = T("1 ticket a week…", 32, INK2).next_to(tl, UP, buff=0.5).align_to(tl, LEFT).shift(RIGHT * 0.3)
        yrs = TB("≈ 269,000 years", 60, WARN).next_to(tl, DOWN, buff=0.6)
        self.play(GrowArrow(tl), FadeIn(tt), run_time=1.0)
        self.play(FadeIn(tks, lag_ratio=0.05), run_time=0.8)
        self.w("s124", "quarter")
        self.play(FadeIn(yrs, scale=0.8), run_time=0.6)
        # s125
        self.at("s125")
        self.play(FadeOut(VGroup(tl, tks, tt, yrs)), run_time=0.4)
        a = pill("maybe I'll win?", MUTED, 40); b = pill("1 in 14 million", VIOLET, 40)
        row = VGroup(a, b).arrange(RIGHT, buff=1.6).move_to(UP * 0.2)
        ar = Arrow(a.get_right(), b.get_left(), color=INK2, buff=0.15)
        self.play(FadeIn(a), run_time=0.4)
        self.w("s125", "clear")
        self.play(GrowArrow(ar), FadeIn(b, shift=LEFT * 0.2), run_time=0.7)
        self.finish()
