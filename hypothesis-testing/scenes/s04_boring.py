import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def labelled_box(title, sub, color, w=6.1, h=2.0):
    b = card(w, h, color)
    t = TB(title, 38, color)
    s = T(sub, 28, INK)
    VGroup(t, s).arrange(DOWN, buff=0.25).move_to(b)
    return VGroup(b, t, s)


class S04Boring(Base):
    CHAPTER = "The Boring Explanation"

    def construct(self):
        fr = self.camera.frame
        # ── s021 exciting vs boring ──
        self.at("s021", 0.0)
        ex = labelled_box("something is going on", "the exciting idea", ORANGE_).move_to(LEFT * 3.2 + UP * 0.6)
        bo = labelled_box("nothing is going on", "the boring explanation", BLUE_).move_to(RIGHT * 3.2 + UP * 0.6)
        self.play(FadeIn(ex, shift=RIGHT * 0.3), run_time=0.6)
        self.until(word_time("s021", word_index("s021", "boring")) - 0.3)
        self.play(FadeIn(bo, shift=LEFT * 0.3), run_time=0.6)
        self.play(ex.animate.set_opacity(0.25), Indicate(bo, color=BLUE_, scale_factor=1.05), run_time=0.9)

        # ── s022 the coin is fair ──
        self.at("s022", 0.0)
        self.play(FadeOut(ex), bo.animate.move_to(UP * 1.9), run_time=0.7)
        fair = VGroup(T("the coin is fair", 36, BLUE_, weight=BOLD),
                      T("heads ½ · tails ½", 32, INK)).arrange(DOWN, buff=0.22)
        fair.next_to(bo, DOWN, buff=0.35)
        self.play(FadeIn(fair, shift=UP * 0.2), run_time=0.6)
        bs, th, L, R = beam_scale(4.4, INK2)
        bs.next_to(fair, DOWN, buff=0.25)
        hc = coin("H", BLUE_, 0.32); tc = coin("T", BLUE_, 0.32)
        self.add(bs)
        self.play(FadeIn(bs), run_time=0.6)
        hc.add_updater(lambda m: m.move_to(L[0].get_center() + UP * 0.38))
        tc.add_updater(lambda m: m.move_to(R[0].get_center() + UP * 0.38))
        self.play(FadeIn(hc), FadeIn(tc), run_time=0.5)
        self.play(th.animate.set_value(0.12), run_time=0.5)
        self.play(th.animate.set_value(-0.08), run_time=0.5)
        self.play(th.animate.set_value(0.0), run_time=0.5)
        self.until(word_time("s022", word_index("s022", "luck")) - 0.3)
        luck = T("15 heads = just luck", 28, MUTED).move_to([4.8, bs.get_y() + 0.9, 0])
        self.play(FadeIn(luck), run_time=0.5)

        # ── s023 its name: the null hypothesis ──
        self.at("s023", 0.0)
        nh = TB("NULL HYPOTHESIS", 44, BLUE_)
        nh.next_to(bo, UP, buff=0.25)
        self.play(FadeOut(VGroup(bs, hc, tc, luck, fair)), run_time=0.4)
        self.remove(*bs, hc, tc)
        self.play(bo.animate.shift(DOWN * 0.6), run_time=0.4)
        nh.next_to(bo, UP, buff=0.3)
        self.play(Write(nh), run_time=0.8)
        d0 = defcard(r"H_0", "null hypothesis: nothing special is going on", BLUE_, fs=30).next_to(bo, DOWN, buff=0.5)
        self.until(word_time("s023", word_index("s023", "Null")) - 0.2)
        self.play(FadeIn(d0, shift=UP * 0.2), run_time=0.6)

        # ── s024 the alternative ──
        self.at("s024", 0.0)
        d1 = defcard(r"H_1", "alternative: the coin favours heads", ORANGE_, fs=30).next_to(d0, DOWN, buff=0.3)
        self.play(FadeIn(d1, shift=UP * 0.2), run_time=0.6)

        # ── s025 pretend the boring explanation is true, ask how surprising ──
        self.at("s025", 0.0)
        self.play(FadeOut(VGroup(nh, d1, d0)), bo.animate.scale(0.8).move_to(LEFT * 3.6 + UP * 0.6), run_time=0.7)
        no = T("we don't prove H₁ directly", 28, MUTED).next_to(bo, DOWN, buff=0.4)
        self.play(FadeIn(no), run_time=0.5)
        self.until(word_time("s025", word_index("s025", "pretend")) - 0.3)
        bt = VGroup(T("if the coin were fair…", 32, BLUE_, weight=BOLD),
                    T("how surprising is 15 heads?", 32, WARN, weight=BOLD)).arrange(DOWN, buff=0.25)
        bub = RoundedRectangle(corner_radius=0.5, width=bt.width + 0.9, height=bt.height + 0.8).set_stroke(INK2, 3)
        bub.set_fill("#22221f", 1); bub.qa_container = True
        th_ = VGroup(bub, bt).move_to(RIGHT * 3.5 + UP * 0.6)
        bt.move_to(bub)
        arr = Arrow(bo.get_right(), bub.get_left(), buff=0.2, color=BLUE_, stroke_width=4)
        self.play(GrowArrow(arr), FadeIn(bub), FadeIn(bt[0]), run_time=0.8)
        self.until(word_time("s025", word_index("s025", "surprising")) - 0.3)
        self.play(FadeIn(bt[1], shift=UP * 0.15), run_time=0.5)

        # ── s026 a courtroom ──
        self.at("s026", 0.0)
        court = sticker("assets/courtroom.png", 2.4).move_to(UP * 1.25)
        self.play(FadeOut(VGroup(bo, no, arr, th_)), run_time=0.5)
        self.play(FadeIn(court, shift=UP * 0.2), run_time=0.7)
        inn = pill("presumed innocent", BLUE_, 30).move_to(LEFT * 3.2 + DOWN * 0.9)
        ev = pill("evidence", WARN, 30).move_to(RIGHT * 3.2 + DOWN * 0.9)
        self.until(word_time("s026", word_index("s026", "presumed")) - 0.2)
        self.play(FadeIn(inn, shift=UP * 0.2), run_time=0.5)
        self.until(word_time("s026", word_index("s026", "evidence")) - 0.2)
        self.play(FadeIn(ev, shift=UP * 0.2), run_time=0.5)

        # ── s027 mapping ──
        self.at("s027", 0.0)
        m1 = T("= the null hypothesis (fair coin)", 28, BLUE_).next_to(inn, DOWN, buff=0.3)
        m2 = T("= our 15 heads", 28, WARN).next_to(ev, DOWN, buff=0.3)
        self.play(FadeIn(m1, shift=DOWN * 0.15), run_time=0.5)
        self.until(word_time("s027", word_index("s027", "fifteen")) - 0.4)
        self.play(FadeIn(m2, shift=DOWN * 0.15), run_time=0.5)
        self.until(SEGS["s027"]["end"] + 0.3)
        self.play(FadeOut(Group(court, inn, ev, m1, m2)), run_time=0.5)
        self.finish()
