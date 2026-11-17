import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def weight(color=ORANGE_):
    w = Polygon(LEFT * 0.22 + DOWN * 0.18, RIGHT * 0.22 + DOWN * 0.18, RIGHT * 0.14 + UP * 0.14, LEFT * 0.14 + UP * 0.14)
    w.set_stroke(color, 3).set_fill(color, 0.9)
    h = Arc(radius=0.1, start_angle=0, angle=PI).set_stroke(color, 3).next_to(w, UP, buff=0)
    return VGroup(w, h)


class S01Hook(Base):
    CHAPTER = "The Coffee Coin"

    def construct(self):
        # ── s001 the café ──
        self.at("s001", 0.0)
        cafe = sticker("assets/cafe.png", 4.8).move_to(UP * 0.4)
        self.play(FadeIn(cafe, shift=UP * 0.3), run_time=1.0)
        who = pill("who pays? flip a coin", WARN, 30).move_to(RIGHT * 4.3 + UP * 3.3)
        self.until(word_time("s001", word_index("s001", "flip")) - 0.2)
        self.play(FadeIn(who, shift=DOWN * 0.2), run_time=0.6)

        # ── s002 their coin, they call heads ──
        self.at("s002", 0.0)
        c = coin("H", BLUE_, 0.95).move_to(RIGHT * 3.7 + UP * 1.1)
        self.play(FadeOut(who), cafe.animate.scale(0.75).move_to(LEFT * 3.0 + UP * 0.3), run_time=0.8)
        self.play(FadeIn(c, scale=0.5), run_time=0.5)
        self.play(c.animate(rate_func=there_and_back).stretch(0.08, 0), run_time=0.5)
        chips = VGroup(pill("their coin", INK, 30),
                       pill("they always call heads", INK, 30)).arrange(DOWN, buff=0.3).next_to(c, DOWN, buff=0.45)
        self.play(FadeIn(chips[0], shift=UP * 0.2), run_time=0.4)
        self.until(word_time("s002", word_index("s002", "calls")) - 0.2)
        self.play(FadeIn(chips[1], shift=UP * 0.2), run_time=0.4)

        # ── s003 the month of flips: tally board on a 'flip number' axis ──
        self.at("s003", 0.0)
        nl = NumberLine(x_range=[0, 21, 1], length=11.55, include_tip=False, color=INK2, stroke_width=3,
                        tick_size=0.07).move_to(DOWN * 0.9 + RIGHT * 0.7)
        nums = VGroup(*[T(str(v), 22, INK2).next_to(nl.n2p(v), DOWN, buff=0.16) for v in (1, 5, 10, 15, 20)])
        xt = T("flip number", 24, MUTED).next_to(nums, DOWN, buff=0.2).align_to(nl, RIGHT)
        yH, yT = nl.get_y() + 1.75, nl.get_y() + 0.75
        rowH = T("heads", 26, WARN, weight=BOLD).move_to([nl.n2p(0)[0] - 0.55, yH, 0])
        rowT = T("tails", 26, MUTED, weight=BOLD).move_to([nl.n2p(0)[0] - 0.55, yT, 0])
        guides = VGroup(*[DashedLine(nl.n2p(0.5) + UP * (y - nl.get_y()), nl.n2p(20.5) + UP * (y - nl.get_y()),
                                     color=GRID, stroke_width=2) for y in (yH, yT)])
        for g_ in guides: g_.qa_ignore = True   # faint row guides behind the dots
        dots_ = VGroup(*[dot(WARN if f == "H" else MUTED, 0.17).move_to([nl.n2p(i + 1)[0], yH if f == "H" else yT, 0])
                         for i, f in enumerate(FLIPS)])
        self.play(FadeOut(Group(cafe, c, chips), shift=UP * 0.3), run_time=0.5)
        self.play(Create(nl), FadeIn(nums), FadeIn(xt), FadeIn(rowH), FadeIn(rowT), Create(guides), run_time=0.8)
        cnt = ValueTracker(0)
        counter = always_redraw(lambda: T(f"{int(round(cnt.get_value()))} heads of 20", 40, WARN, weight=BOLD)
                                .move_to(UP * 2.75 + RIGHT * 3.0))
        self.add(counter)
        heads_idx = [i for i, f in enumerate(FLIPS) if f == "H"]
        anims = []
        for i, d in enumerate(dots_):
            anims.append(FadeIn(d, scale=0.3))
        self.play(LaggedStart(*anims, lag_ratio=0.5), cnt.animate.set_value(15), run_time=3.2, rate_func=linear)
        counter.clear_updaters()

        # ── s004 coffees paid for ──
        self.at("s004", 0.0)
        sa = stacks_axes(y_max=15, step=5, x_len=4.6, y_len=3.6, title="coffees paid for")
        sa.move_to(RIGHT * 3.4 + UP * 0.15)
        ax = sa.ax
        you = stack(ax, 0.5, 15, WARN, per_row=3)
        fr_ = stack(ax, 1.5, 5, INK2, per_row=3)
        lab_you = T("you: 15", 28, WARN, weight=BOLD).next_to(ax.c2p(0.5, 0), DOWN, buff=0.25)
        lab_fr = T("your friend: 5", 28, INK2, weight=BOLD).next_to(ax.c2p(1.5, 0), DOWN, buff=0.25)
        board = VGroup(nl, nums, xt, rowH, rowT, guides, dots_)
        self.play(board.animate.scale(0.5).move_to(LEFT * 3.25 + UP * 0.5), counter.animate.scale(0.7).move_to(LEFT * 3.0 + UP * 2.1),
                  run_time=0.8)
        self.play(Create(ax), FadeIn(sa.labs), FadeIn(sa.yt), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.2) for s in you], lag_ratio=0.12), FadeIn(lab_you), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.2) for s in fr_], lag_ratio=0.12), FadeIn(lab_fr), run_time=0.7)

        # ── s005 you start to wonder ──
        self.at("s005", 0.2)
        bub = VGroup(Ellipse(width=2.2, height=1.0), Circle(0.12), Circle(0.07)).set_stroke(INK2, 3).set_fill("#22221f", 1)
        bub[0].qa_container = True
        bub[1].next_to(bub[0], DOWN + RIGHT * 0.2, buff=0.05); bub[2].next_to(bub[1], DOWN + RIGHT * 0.3, buff=0.05)
        hmm = T("…hmm", 30, INK).move_to(bub[0])
        bubble = VGroup(bub, hmm).move_to(LEFT * 3.4 + DOWN * 1.35)
        self.play(FadeIn(bub, scale=0.6), run_time=0.5)
        self.until(word_time("s005", word_index("s005", "wonder")) - 0.4)
        self.play(Write(hmm), run_time=0.6)
        self.play(Indicate(you, color=WARN, scale_factor=1.04), run_time=0.8)

        # ── s006 rigged, or just luck? ──
        self.at("s006", 0.0)
        cl = coin("H", ORANGE_, 1.0).move_to(LEFT * 3.6 + UP * 0.7)
        wt = weight().next_to(cl, RIGHT, buff=0.15).shift(DOWN * 0.5)
        cr = coin("H", BLUE_, 1.0).move_to(RIGHT * 3.6 + UP * 0.7)
        tl = T("rigged?", 40, ORANGE_, weight=BOLD).next_to(cl, DOWN, buff=0.45)
        tr = T("just luck?", 40, BLUE_, weight=BOLD).next_to(cr, DOWN, buff=0.45)
        qm = glow(TB("?", 130, WARN), WARN).move_to(UP * 0.5)
        self.play(FadeOut(VGroup(board, counter, sa, you, fr_, lab_you, lab_fr, bubble)), run_time=0.5)
        self.until(word_time("s006", word_index("s006", "rigged")) - 0.3)
        self.play(FadeIn(cl, shift=RIGHT * 0.4), FadeIn(wt, shift=DOWN * 0.3), FadeIn(tl), run_time=0.6)
        self.until(word_time("s006", word_index("s006", "lucky")) - 0.5)
        self.play(FadeIn(cr, shift=LEFT * 0.4), FadeIn(tr), run_time=0.6)
        self.play(FadeIn(qm, scale=0.5), run_time=0.5)

        # ── s007 decide: a slider between luck and rigged ──
        self.at("s007", 0.0)
        sl = NumberLine(x_range=[0, 1, 0.25], length=8.0, include_tip=False, color=INK2, stroke_width=4,
                        tick_size=0.08).move_to(DOWN * 1.85)
        l1 = T("just luck", 28, BLUE_, weight=BOLD).next_to(sl.n2p(0), DOWN, buff=0.3)
        l2 = T("rigged", 28, ORANGE_, weight=BOLD).next_to(sl.n2p(1), DOWN, buff=0.3)
        cur = Line(UP * 0.3, DOWN * 0.3, color=WARN, stroke_width=6).move_to(sl.n2p(0.5))
        self.play(qm.animate.scale(0.55).move_to(UP * 0.7), FadeIn(sl), FadeIn(l1), FadeIn(l2), run_time=0.6)
        self.add(cur)
        for _ in range(2):
            self.play(cur.animate.set_opacity(0.1), run_time=0.35)
            self.play(cur.animate.set_opacity(1), run_time=0.35)

        # ── s008 a fair coin CAN do this ──
        self.at("s008", 0.0)
        self.play(FadeOut(VGroup(cl, wt, tl, qm, sl, l1, l2, cur)), cr.animate.move_to(UP * 0.9).scale(1.2),
                  FadeOut(tr), run_time=0.8)
        for _ in range(3):
            self.play(cr.animate(rate_func=there_and_back).stretch(0.06, 0), run_time=0.45)
        self.until(word_time("s008", word_index("s008", "fair")) - 0.2)
        can = T("a fair coin CAN do this", 40, INK, weight=BOLD).next_to(cr, DOWN, buff=0.6)
        self.play(FadeIn(can, shift=UP * 0.2), run_time=0.5)
        self.until(word_time("s008", word_index("s008", "impossible")) - 0.4)
        np_ = T("15 heads of 20: unusual, not impossible", 30, MUTED).next_to(can, DOWN, buff=0.3)
        self.play(FadeIn(np_), run_time=0.5)

        # ── s009 how unusual? a heads number line with a pin at 15 ──
        self.at("s009", 0.0)
        hl = NumberLine(x_range=[0, 20, 1], length=11.0, include_tip=False, color=INK2, stroke_width=3,
                        tick_size=0.08).move_to(DOWN * 0.8)
        hn = VGroup(*[T(str(v), 24, INK2).next_to(hl.n2p(v), DOWN, buff=0.16) for v in range(0, 21, 5)])
        ht = T("heads in 20 flips", 24, MUTED).next_to(hn, DOWN, buff=0.2).align_to(hl, RIGHT)
        self.play(FadeOut(VGroup(cr, can, np_)), Create(hl), FadeIn(hn), FadeIn(ht), run_time=0.8)
        pin = marker(hl, 15, WARN, "15", height=1.3, fs=36)
        self.play(FadeIn(pin, shift=DOWN * 1.0), run_time=0.6, rate_func=rate_functions.ease_out_bounce)
        zone = Rectangle(width=hl.n2p(20)[0] - hl.n2p(15)[0], height=1.0, stroke_width=0, fill_color=AQUA, fill_opacity=0.12)
        zone.move_to(hl.n2p(17.5) + UP * 0.5)
        q = T("unusual enough to call it rigged?", 34, INK, weight=BOLD).move_to(UP * 2.3)
        self.until(word_time("s009", word_index("s009", "Unusual")) - 0.2)
        self.play(FadeIn(zone), FadeIn(q, shift=DOWN * 0.2), run_time=0.6)
        self.play(zone.animate.set_fill(opacity=0.28), rate_func=there_and_back, run_time=1.2)

        # ── s010 title card ──
        self.at("s010", 0.0)
        title = ht_title()
        self.until(word_time("s010", word_index("s010", "hypothesis")) - 0.3)
        self.play(FadeOut(VGroup(hl, hn, ht, pin, zone, q)), run_time=0.5)
        self.play(FadeIn(title[0], scale=0.85), run_time=0.8)
        self.until(word_time("s010", word_index("s010", "p")) - 0.3)
        self.play(Write(title[1]), run_time=1.0)
        self.finish()
