import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

PX = -2.9   # main panel left edge; the list of mistakes sits left of it


def bubble(text, color, ok):
    t = T(text, 28, INK)
    mark = check(AQUA, 0.4) if ok else cross(RED_, 0.22)
    row = VGroup(mark, t).arrange(RIGHT, buff=0.3)
    b = RoundedRectangle(corner_radius=0.3, width=row.width + 0.8, height=row.height + 0.6).set_stroke(color, 3).set_fill("#22221f", 1)
    b.qa_container = True
    row.move_to(b)
    return VGroup(b, row)


def main_card(n, title):
    num = TB(n, 40, RED_)
    t = T(title, 30, INK, weight=BOLD)
    row = VGroup(num, t).arrange(RIGHT, buff=0.35)
    b = card(row.width + 0.8, row.height + 0.55, RED_); row.move_to(b)
    g = VGroup(b, row)
    return g.move_to(UP * 1.6).set_x(PX + g.width / 2)


class S13Mistakes(Base):
    CHAPTER = "Common Mistakes"

    def construct(self):
        self.at("s108", 0.0)
        hd = TB("common mistakes", 56, RED_).move_to(UP * 0.4)
        self.play(FadeIn(hd, scale=0.8), run_time=0.6)
        self.word("s108", "catch")
        self.play(pulse(hd, s=1.08), run_time=0.6)
        lst = VGroup()

        def to_list(title):
            ch_ = pill(title, RED_, 20)
            if len(lst):
                ch_.next_to(lst[-1], DOWN, buff=0.15).align_to(lst[0], LEFT)
            else:
                ch_.move_to(UP * 2.35).set_x(-6.6 + ch_.width / 2)
            lst.add(ch_)
            return ch_

        # ── mistake 1: the swap ──
        self.at("s109", 0.0)
        self.idle()
        self.play(FadeOut(hd), run_time=0.3)
        m1 = main_card("1", "the swap itself")
        self.play(FadeIn(m1, shift=DOWN * 0.2), run_time=0.5)
        a = cond("match", "innocent", 30); ne = TB("≠", 48, RED_); b = cond("innocent", "match", 30)
        eq = VGroup(a, ne, b).arrange(RIGHT, buff=0.3).move_to(UP * 0.1)
        eq.set_x(min(PX + 4.6, 6.4 - eq.width / 2))
        self.word("s109", "Reading")
        self.play(FadeIn(a, shift=RIGHT * 0.2), run_time=0.5)
        self.word("s109", "as")
        self.play(FadeIn(ne, scale=0.5), FadeIn(b, shift=LEFT * 0.2), run_time=0.6)

        # s110 listen for it in the words
        self.at("s110", 0.0)
        good = bubble("“an innocent person would match: 1 in a million”", AQUA, True)
        bad = bubble("“he is innocent: 1 in a million”", RED_, False)
        VGroup(good, bad).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(eq, DOWN, buff=0.45).set_x(PX + 4.6)
        for bb in (good, bad):
            if bb.get_right()[0] > 6.6:
                bb.shift(LEFT * (bb.get_right()[0] - 6.6))
        self.word("s110", "One")
        self.play(FadeIn(good, shift=UP * 0.2), run_time=0.5)
        self.word("s110", "not")
        self.play(FadeIn(bad, shift=UP * 0.2), run_time=0.5)

        # ── mistake 2: forgetting the crowd ──
        self.at("s111", 0.0)
        self.idle()
        c1 = to_list("1 · the swap")
        self.play(ReplacementTransform(m1, c1), FadeOut(VGroup(eq, good, bad)), run_time=0.6)
        m2 = main_card("2", "forgetting the crowd")
        self.play(FadeIn(m2, shift=DOWN * 0.2), run_time=0.5)
        v = result_card("village · 1,000", "999 in 1,000", VIOLET, 24, 40, 3.6)
        k = result_card("country · 60,000,000", "1 in 61", VIOLET, 24, 40, 3.6)
        sl = DoubleArrow(LEFT * 0.8, RIGHT * 0.8, color=INK2, stroke_width=4, buff=0)
        row = VGroup(v, sl, k).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.75).set_x(PX + 4.6)
        same = pill("same 1-in-a-million match", WARN, 24).next_to(row, UP, buff=0.3)
        self.word("s111", "village")
        self.play(FadeIn(v, shift=UP * 0.2), FadeIn(same), run_time=0.5)
        self.word("s111", "country")
        self.play(GrowFromCenter(sl), FadeIn(k, shift=UP * 0.2), run_time=0.5)

        # ── mistake 3: the defense's version ──
        self.at("s112", 0.0)
        self.idle()
        c2 = to_list("2 · forgetting the crowd")
        self.play(ReplacementTransform(m2, c2), FadeOut(VGroup(v, k, sl, same)), run_time=0.6)
        m3 = main_card("3", "the other way: “worthless”")
        self.play(FadeIn(m3, shift=DOWN * 0.2), run_time=0.5)
        bb = bubble("“only 1 in 9, so the evidence is worthless!”", RED_, False).move_to(UP * 0.1).set_x(PX + 4.6)
        if bb.get_right()[0] > 6.6:
            bb.shift(LEFT * (bb.get_right()[0] - 6.6))
        self.word("s112", "lawyers")
        self.play(FadeIn(bb, shift=UP * 0.2), run_time=0.5)
        self.word("s112", "worthless")
        self.play(pulse(bb, s=1.06), run_time=0.5)

        # s113 a funnel: 8,000,000 down to 9
        self.at("s113", 0.0)
        top = pill("8,000,000 people", AQUA, 24); bot = pill("9 who match", WARN, 24)
        fun = Polygon(LEFT * 1.6, RIGHT * 1.6, RIGHT * 0.4 + DOWN * 0.6, LEFT * 0.4 + DOWN * 0.6).set_stroke(INK2, 3)
        fg = VGroup(top, fun, bot).arrange(DOWN, buff=0.1).next_to(bb, DOWN, buff=0.25).set_x(PX + 2.0)
        pw = pill("powerful evidence, not proof", VIOLET, 24).next_to(fun, RIGHT, buff=0.4)
        self.word("s113", "eight")
        self.play(FadeIn(top), Create(fun), run_time=0.5)
        self.word("s113", "nine")
        self.play(FadeIn(bot, shift=DOWN * 0.3), run_time=0.4)
        self.word("s113", "powerful")
        self.play(FadeIn(pw, shift=LEFT * 0.2), run_time=0.5)

        # ── bonus: multiplying connected chances ──
        self.at("s114", 0.0)
        self.idle()
        c3 = to_list("3 · “worthless”")
        self.play(ReplacementTransform(m3, c3), FadeOut(VGroup(bb, fg, pw)), run_time=0.6)
        m4 = main_card("+", "bonus: multiplying connected chances")
        self.play(FadeIn(m4, shift=DOWN * 0.2), run_time=0.5)
        mul = VGroup(T("1 in 8,543", 40, BLUE_, weight=BOLD), T("×", 44, RED_, weight=BOLD), T("1 in 8,543", 40, BLUE_, weight=BOLD)
                     ).arrange(RIGHT, buff=0.3).move_to(UP * 0.0).set_x(PX + 4.6)
        cn = pill("connected?", RED_, 30).next_to(mul, DOWN, buff=0.4)
        self.word("s114", "multiplying")
        self.play(FadeIn(mul, shift=UP * 0.2), run_time=0.5)
        self.word("s114", "connected")
        self.play(FadeIn(cn, scale=0.6), ripple(cn.get_center(), RED_, r=0.5, scale=3), run_time=0.6)
        rr = T("a coincidence can look far rarer than it is", 28, INK2).next_to(cn, DOWN, buff=0.35)
        self.word("s114", "rarer")
        self.play(FadeIn(rr, shift=UP * 0.2), run_time=0.5)
        self.finish()
