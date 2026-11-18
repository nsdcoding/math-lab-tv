import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

FLIPS = "HHTHHHTHHTHHTHHHTHHH"   # 15 heads, 5 tails (the coffee coin, illustration of the order)
assert FLIPS.count("H") == 15


def text_card(lines, color, w=None, size=30, bold_last=False):
    rows = VGroup(*[T(l, size, INK) for l in lines])
    if bold_last:
        rows[-1].become(TB(lines[-1], int(size * 1.4), color))
    rows.arrange(DOWN, buff=0.22)
    box = card(w or rows.width + 0.9, rows.height + 0.7, color)
    rows.move_to(box)
    g = VGroup(box, rows); g.box, g.rows = box, rows
    return g


class S03Questions(Base):
    CHAPTER = "Two Different Questions"

    def construct(self):
        # ── s016 the coffee coin: 15 heads of 20 ──
        self.at("s016", 0.0)
        frm = chip("from: Hypothesis Testing", AQUA, 26).to_edge(UP, buff=0.45).to_edge(RIGHT, buff=0.5)
        self.play(FadeIn(frm, shift=LEFT * 0.4), run_time=0.5)
        nl = NumberLine(x_range=[0, 21, 1], length=11.0, include_tip=False, color=INK2, stroke_width=3,
                        tick_size=0.07).move_to(DOWN * 1.0 + RIGHT * 0.6)
        nums = VGroup(*[T(str(v), 22, INK2).next_to(nl.n2p(v), DOWN, buff=0.16) for v in (1, 5, 10, 15, 20)])
        xt = T("flip number", 24, MUTED).next_to(nums, DOWN, buff=0.2).align_to(nl, RIGHT)
        yH, yT = nl.get_y() + 1.8, nl.get_y() + 0.8
        rH = T("heads", 26, ORANGE_, weight=BOLD).move_to([nl.n2p(0)[0] - 0.6, yH, 0])
        rT = T("tails", 26, BLUE_, weight=BOLD).move_to([nl.n2p(0)[0] - 0.6, yT, 0])
        dots_ = VGroup(*[dot(ORANGE_ if f == "H" else BLUE_, 0.17).move_to([nl.n2p(i + 1)[0], yH if f == "H" else yT, 0])
                         for i, f in enumerate(FLIPS)])
        self.play(Create(nl), FadeIn(nums), FadeIn(xt), FadeIn(rH), FadeIn(rT), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots_], lag_ratio=0.12), run_time=2.2)
        self.word("s016", "fifteen")
        cnt = TB("15 heads of 20", 44, ORANGE_).move_to(UP * 2.3 + RIGHT * 0.6)
        self.play(FadeIn(cnt, scale=0.6), ripple(cnt.get_center(), ORANGE_, r=0.6, scale=3), run_time=0.6)
        self.idle(lambda: pulse(cnt, s=1.1))

        # ── s017 a fair coin does that only about 2 times in 100 ──
        self.at("s017", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(nl, nums, xt, rH, rT, dots_, cnt)), run_time=0.5)
        pm = [comb(20, k) / 2 ** 20 * 100 for k in range(21)]
        g = xy_axes([0, 20, 5], [0, 20, 5], 10.5, 3.2, "heads in 20 flips (fair coin)", "chance (%)", y_vertical=True)
        g.move_to(DOWN * 0.05 + RIGHT * 0.5)
        ax = g[0]
        bars = VGroup(*[Rectangle(width=0.4, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.001))
                        .set_stroke(width=0).set_fill(AQUA if k >= 15 else BLUE_, 0.9)
                        .move_to(ax.c2p(k, 0), aligned_edge=DOWN) for k, v in enumerate(pm)])
        self.play(FadeIn(g), run_time=0.5)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), run_time=1.2)
        self.word("s017", "extreme")
        tail = VGroup(*bars[15:])
        br = Brace(tail, UP, buff=0.15, color=AQUA)
        pv = pill("15 or more heads: p ≈ 0.021", AQUA, 30)
        pv.move_to(UP * 2.45).align_to(ax, RIGHT)
        lead = Line(br.get_top(), pv.get_bottom(), buff=0.1).set_stroke(AQUA, 2.5)
        self.play(GrowFromCenter(br), Create(lead), FadeIn(pv, shift=DOWN * 0.2), Indicate(tail, color=AQUA), run_time=0.8)
        self.word("s017", "two")
        tw = pill("about 2 times in 100", WARN, 30).next_to(pv, LEFT, buff=0.4)
        self.play(FadeIn(tw, scale=0.6), run_time=0.5)
        self.idle(lambda: glint(tail[0], AQUA))

        # ── s018 that's not the chance the coin is fair ──
        self.at("s018", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(g, bars, br, pv, tw, lead)), run_time=0.5)
        k1 = text_card(["chance of 15+ heads,", "if the coin is fair", "≈ 0.021"], BLUE_, 5.4, 30, True)
        k2 = text_card(["chance the coin is fair,", "given 15+ heads", "?"], VIOLET, 5.4, 30, True)
        k1.move_to(LEFT * 3.3 + UP * 0.2); k2.move_to(RIGHT * 3.5 + UP * 0.2)
        ne = TB("≠", 80, RED_).move_to((k1.get_right() + k2.get_left()) / 2)
        self.play(FadeIn(k1, shift=RIGHT * 0.3), run_time=0.5)
        self.word("s018", "not")
        self.play(FadeIn(k2, shift=LEFT * 0.3), run_time=0.5)
        self.play(FadeIn(ne, scale=0.4), ripple(ne.get_center(), RED_), run_time=0.6)
        self.word("s018", "flipped")
        self.play(Indicate(VGroup(k1.rows[:2], k2.rows[:2]), color=RED_, scale_factor=1.05),
                  run_time=0.8)

        # ── s019 the courtroom is the same flip ──
        self.at("s019", 0.0)
        self.play(FadeOut(VGroup(k1, k2, ne), shift=UP * 0.5), FadeOut(frm), run_time=0.5)
        e1 = text_card(["an innocent person matches", "1 in 1,000,000"], BLUE_, 5.6, 28, True).move_to(LEFT * 3.3 + UP * 0.2)
        e2 = text_card(["Sam is innocent", "1 in 1,000,000 ?"], RED_, 5.0, 28, True).move_to(RIGHT * 3.5 + UP * 0.2)
        self.play(FadeIn(e1, shift=UP * 0.4), FadeIn(e2, shift=UP * 0.4), run_time=0.6)
        self.word("s019", "flip")
        self.play(Indicate(e2, color=RED_, scale_factor=1.06), run_time=0.7)
        self.word("s019", "carefully")
        pen = pill("let's write it down", INK, 28).move_to(DOWN * 2.0)
        self.play(FadeIn(pen, shift=UP * 0.2), run_time=0.4)

        # ── s020 the symbols: P( ) and the bar ──
        self.at("s020", 0.0)
        self.play(FadeOut(VGroup(e1, e2, pen)), run_time=0.5)
        hd = T("two symbols", 30, MUTED, weight=BOLD).move_to(UP * 2.3)
        d1 = defcard(r"P(\ \dots\ )", "the chance of …", INK, 34)
        d2 = defcard(r"\mid", "given  (we already know this part)", INK, 34)
        VGroup(d1, d2).arrange(DOWN, buff=0.55).move_to(UP * 0.1)
        self.play(FadeIn(hd), run_time=0.3)
        self.word("s020", "capital")
        self.play(FadeIn(d1, shift=UP * 0.3), run_time=0.6)
        self.word("s020", "bar")
        self.play(FadeIn(d2, shift=UP * 0.3), run_time=0.6)
        self.word("s020", "given")
        self.play(Indicate(d2[1][2], color=WARN, scale_factor=1.1), run_time=0.7)

        # ── s021 box 1: P(match | innocent) ──
        self.at("s021", 0.0)
        self.idle()
        b1 = cond_box("match", "innocent", value="1 in 1,000,000", color=BLUE_, size=36, w=5.6,
                      caption="innocent people →\nhow many match?")
        b1.move_to(UP * 0.15).set_x(-0.4 - b1.width / 2)
        b1.value.set_opacity(0)
        self.qa_mute(b1.value)
        self.play(FadeOut(VGroup(hd, d1, d2), shift=UP * 0.4), run_time=0.4)
        self.play(FadeIn(b1.box), FadeIn(b1.expr, shift=UP * 0.2), run_time=0.6)
        self.word("s021", "innocent")
        self.play(Indicate(b1.expr.b, color=BLUE_, scale_factor=1.2), run_time=0.6)
        self.word("s021", "match", nth=1)
        self.play(FadeIn(b1.caption, shift=UP * 0.2), Indicate(b1.expr.a, color=WARN, scale_factor=1.2), run_time=0.7)

        # ── s022 the expert's number ──
        self.at("s022", 0.0)
        self.qa_mute(b1.value, False)
        self.play(b1.value.animate.set_opacity(1), ripple(b1.value.get_center(), WARN, r=0.5, scale=3), run_time=0.7)
        exp = pill("the expert's number", BLUE_, 26).next_to(b1, UP, buff=0.3)
        self.play(FadeIn(exp, shift=DOWN * 0.2), run_time=0.4)

        # ── s023 box 2: P(innocent | match) ──
        self.at("s023", 0.0)
        b2 = cond_box("innocent", "match", value="?", color=VIOLET, size=36, w=5.6,
                      caption="people who match →\nhow many innocent?")
        b2.move_to(UP * 0.15).set_x(0.4 + b2.width / 2)
        print("box2 right", b2.get_right()[0])
        b2.value.match_y(b1.value)
        b2.caption.match_y(b1.caption)
        self.play(FadeIn(b2.box), FadeIn(b2.expr, shift=UP * 0.2), run_time=0.6)
        jn = pill("what the jury needs", VIOLET, 26).next_to(b2, UP, buff=0.3)
        self.play(FadeIn(jn, shift=DOWN * 0.2), run_time=0.4)
        self.word("s023", "Suppose")
        self.play(FadeIn(b2.caption, shift=UP * 0.2), Indicate(b2.expr.b, color=WARN, scale_factor=1.2), run_time=0.7)
        self.word("s023", "innocent", nth=1)
        self.play(FadeIn(b2.value, scale=0.5), run_time=0.5)
        self.idle(lambda: Wiggle(b2.value, scale_value=1.2, n_wiggles=4))

        # ── s024 same words, swapped around the bar ──
        self.at("s024", 0.0)
        self.idle()
        self.word("s024", "same")
        self.play(Indicate(VGroup(b1.expr.a, b2.expr.b), color=WARN, scale_factor=1.15), run_time=0.6)
        self.play(Indicate(VGroup(b1.expr.b, b2.expr.a), color=BLUE_, scale_factor=1.15), run_time=0.6)
        self.word("s024", "swapped")
        ghost = b1.expr.copy()
        self.add(ghost)
        self.qa_mute(ghost)
        self.play(FadeOut(VGroup(exp, jn)), ghost.animate.move_to(UP * 2.55), run_time=0.5)
        swap_parts(self, ghost, run_time=1.1)
        self.qa_mute(ghost)
        self.play(ghost.animate.move_to(b2.expr).set_opacity(0), run_time=0.7)
        self.remove(ghost)
        self.play(Indicate(b2.expr, color=RED_, scale_factor=1.1), run_time=0.6)

        # ── s025 the prosecutor read the first as the second ──
        self.at("s025", 0.0)
        fly = b1.value.copy()
        self.qa_mute(fly)
        self.word("s025", "read")
        self.play(FadeOut(b2.value), fly.animate.move_to(b2.value).set_color(RED_), run_time=1.0)
        self.qa_mute(fly, False)
        self.word("s025", "swap")
        stamp = pill("THE SWAP", RED_, 44).rotate(0.12).move_to(b2.get_center() + DOWN * 0.15)
        stamp.move_to(b2.caption)
        self.qa_mute(fly)
        self.play(FadeOut(b2.caption), run_time=0.2)
        self.play(FadeIn(stamp, scale=1.8), ripple(stamp.get_center(), RED_, r=0.6, scale=3), run_time=0.6)
        self.idle(lambda: pulse(stamp, s=1.1))

        # ── s025a what the expert should have said ──
        self.at("s025a", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(b1.box, b1.expr, b1.value, b1.caption, b2.box, b2.expr, fly, stamp)), run_time=0.5)
        ok = VGroup(check(AQUA, 0.5), T("If Sam were innocent, a match would be very unlikely.", 34, INK)).arrange(RIGHT, buff=0.4)
        okb = card(ok.width + 0.9, ok.height + 0.8, AQUA)
        ok.move_to(okb)
        okg = VGroup(okb, ok).move_to(UP * 1.3)
        self.play(FadeIn(okg, shift=UP * 0.3), run_time=0.6)
        self.word("s025a", "unlikely")
        tr = pill("true", AQUA, 28).next_to(okg, DOWN, buff=0.3).align_to(okg, RIGHT)
        self.play(FadeIn(tr, scale=0.6), run_time=0.4)

        # ── s025b but that's not the chance he's innocent: one more ingredient ──
        self.at("s025b", 0.0)
        q = T("How likely is Sam innocent?", 36, INK, weight=BOLD)
        qb = card(q.width + 0.9, q.height + 0.8, VIOLET); q.move_to(qb)
        qg = VGroup(qb, q).move_to(DOWN * 1.0 + LEFT * 1.6)
        self.word("s025b", "not")
        self.play(FadeIn(qg, shift=UP * 0.3), run_time=0.6)
        self.word("s025b", "ingredient")
        piece = VGroup(DashedVMobject(Square(1.2).set_stroke(VIOLET, 4), num_dashes=24), TB("?", 60, VIOLET))
        piece[1].move_to(piece[0])
        piece.next_to(qg, RIGHT, buff=0.7)
        self.play(FadeIn(piece, scale=0.5), run_time=0.6)
        self.idle(lambda: Wiggle(piece, scale_value=1.15, n_wiggles=3))
        self.until(SEGS["s025b"]["end"] + 0.2)
        self.idle()
        self.play(FadeOut(VGroup(okg, tr, qg, piece)), run_time=0.4)
        self.finish()
