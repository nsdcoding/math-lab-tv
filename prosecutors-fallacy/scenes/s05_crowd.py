import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

GUILTY_BLOCK, GUILTY_CELL = 5, 77          # where the culprit lives (illustration)
LUCKY = [40, 101, 23, 130, 66, 88, 12, 119]  # one innocent match per block (illustration)
SAM_AT, CULPRIT_AT = 2, 6                    # positions in the line-up (illustration)


def assume_row(n, text, color=INK):
    num = TB(n, 40, AQUA)
    t = T(text, 32, color)
    return VGroup(num, t).arrange(RIGHT, buff=0.35)


class S05Crowd(Base):
    CHAPTER = "Count the Crowd"

    def construct(self):
        # ── s035–s038 assumptions ──
        self.at("s035", 0.0)
        hd = TB("what we assume", 44, INK).move_to(UP * 2.2)
        rows = VGroup(assume_row("1", "the culprit is one of the 8,000,000 people"),
                      assume_row("2", "the culprit always matches the trace"),
                      assume_row("3", "no other evidence about Sam (yet)")).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        box = card(rows.width + 1.0, rows.height + 0.9, AQUA)
        rows.move_to(box)
        VGroup(box, rows).move_to(DOWN * 0.2)
        self.play(FadeIn(hd, shift=DOWN * 0.2), Create(box), run_time=0.7)
        for sid, r in zip(("s036", "s037", "s038"), rows):
            self.at(sid, 0.0)
            self.play(FadeIn(r, shift=RIGHT * 0.3), run_time=0.5)
            self.play(Indicate(r[0], color=AQUA, scale_factor=1.3), run_time=0.5)
        self.word("s038", "back")
        tag = pill("we'll come back to this", VIOLET, 24).next_to(rows[2], RIGHT, buff=0.3)
        if tag.get_right()[0] > 6.6:
            tag.next_to(box, DOWN, buff=0.25).align_to(box, RIGHT)
        self.play(FadeIn(tag, scale=0.6), run_time=0.5)

        # ── s039 the whole city: eight blocks of one million ──
        self.at("s039", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(hd, box, rows, tag)), run_time=0.5)
        blocks = city_blocks().move_to(LEFT * 2.25 + DOWN * 0.35)
        self.word("s039", "city")
        self.play(LaggedStart(*[FadeIn(b, scale=0.9) for b in blocks], lag_ratio=0.12), run_time=1.4)
        self.word("s039", "blocks")
        labs = VGroup(T("each block = 1,000,000 people (illustration)", 24, INK2).next_to(blocks, UP, buff=0.25))
        self.play(FadeIn(labs[0], shift=DOWN * 0.2), run_time=0.6)
        px = 2.55  # right panel x (left edge)
        tot = TB("8,000,000 people", 38, AQUA).move_to(UP * 2.35).set_x(px + 2.0)
        self.play(FadeIn(tot, shift=DOWN * 0.2), run_time=0.5)

        # ── s040 one culprit; the rest innocent ──
        self.at("s040", 0.0)
        cul = blocks[GUILTY_BLOCK].cells[GUILTY_CELL]
        self.word("s040", "culprit")
        self.play(cul.animate.set_fill(ORANGE_, 1).scale(1.8), ripple(cul.get_center(), ORANGE_, r=0.2, scale=4), run_time=0.7)
        self.play(cul.animate.scale(1 / 1.8), run_time=0.3)
        self.word("s040", "innocent")
        inn = VGroup(T("innocent", 28, BLUE_, weight=BOLD), TB("7,999,999", 40, BLUE_)).arrange(DOWN, buff=0.12)
        inn.move_to(UP * 1.25).set_x(px + inn.width / 2)
        self.play(*[b.cells.animate.set_fill(BLUE_, 0.85) for b in blocks], FadeIn(inn, shift=LEFT * 0.2), run_time=0.8)
        cul.set_fill(ORANGE_, 1)

        # ── s041 the expert's number ──
        self.at("s041", 0.0)
        ex = cond_box("match", "innocent", value="1 in 1,000,000", color=BLUE_, size=24)
        ex.move_to(DOWN * 0.25).set_x(px + ex.width / 2)
        self.play(FadeIn(ex, shift=LEFT * 0.3), run_time=0.6)
        self.word("s041", "million")
        self.play(Indicate(ex.value, color=WARN, scale_factor=1.15), run_time=0.6)

        # ── s042 one block of a million: how many match by chance? ──
        self.at("s042", 0.0)
        b0 = blocks[0]
        self.play(*[b.animate.set_opacity(0.25) for b in blocks[1:]], 
                  run_time=0.5)
        cul.set_opacity(1)
        scan = Line(b0.frame.get_corner(UL), b0.frame.get_corner(DL)).set_stroke(WARN, 5)
        scan.qa_ignore = True
        self.word("s042", "block")
        self.play(Create(scan), run_time=0.3)
        self.play(scan.animate.move_to(b0.frame.get_right()), run_time=1.5, rate_func=linear)
        self.play(scan.animate.move_to(b0.frame.get_left()), run_time=1.2, rate_func=linear)

        # ── s043 about one ──
        self.at("s043", 0.0)
        hit0 = b0.cells[LUCKY[0]]
        self.play(FadeOut(scan), hit0.animate.set_fill(WARN, 1).scale(1.8), ripple(hit0.get_center(), WARN, r=0.2, scale=4), run_time=0.6)
        one = pill("≈ 1 innocent match", WARN, 26).move_to(DOWN * 1.85).set_x(px + 2.0)
        self.play(FadeIn(one, shift=UP * 0.2), hit0.animate.scale(1 / 1.8), run_time=0.5)

        # ── s044 eight blocks: about eight innocent matches ──
        self.at("s044", 0.0)
        self.play(*[b.animate.set_opacity(1) for b in blocks[1:]], run_time=0.5)
        for b in blocks:
            b.frame.set_fill(opacity=0)
        cnt = ValueTracker(1)
        cl = always_redraw(lambda: pill(f"≈ {int(round(cnt.get_value()))} innocent match{'es' if cnt.get_value() > 1.5 else ''}",
                                        WARN, 26).move_to(DOWN * 1.85).set_x(px + 2.0))
        self.remove(one); self.add(cl)
        self.word("s044", "eight", nth=0)
        hits = [hit0]
        for k in range(1, 8):
            h = blocks[k].cells[LUCKY[k]]
            hits.append(h)
            self.play(h.animate.set_fill(WARN, 1), ripple(h.get_center(), WARN, r=0.15, scale=3), cnt.animate.set_value(k + 1),
                      run_time=0.32)
        cl.clear_updaters()
        self.word("s044", "luck")
        self.play(pulse(cl, s=1.12), run_time=0.6)   # Indicate would flood the pill box with colour

        # ── s042a check it: 8,000,000 x 1/1,000,000 = 8 ──
        self.at("s042a", 0.0)
        ar = T("8,000,000 × 1 in 1,000,000 = 8", 28, INK, weight=BOLD)
        ar.next_to(blocks, UP, buff=0.25)
        self.play(FadeOut(labs), run_time=0.3)
        self.play(FadeIn(ar, shift=UP * 0.2), run_time=0.5)
        self.word("s042a", "eight", nth=1)
        self.play(ar[-1:].animate.set_color(WARN).scale(1.4), run_time=0.5)

        # ── s045 plus the culprit ──
        self.at("s045", 0.0)
        cr = Circle(0.16).set_stroke(WARN, 4).move_to(cul)
        cr.qa_ignore = True
        nine = pill("8 + 1 = 9 people match", WARN, 26).move_to(cl)
        self.play(Create(cr), ripple(cul.get_center(), ORANGE_, r=0.2, scale=4), run_time=0.6)
        self.play(FadeOut(cl), FadeIn(nine), run_time=0.5)

        # ── s046 the line-up of everyone who matches ──
        self.at("s046", 0.0)
        self.idle()
        lu = lineup(9, CULPRIT_AT, 0.85, 0.42).move_to(UP * 0.6)
        nl = NumberLine(x_range=[1, 9, 1], length=lu[-1].get_x() - lu[0].get_x(), include_tip=False, color=INK2,
                        stroke_width=3, tick_size=0.07)
        nl.move_to([lu.get_x(), lu.get_bottom()[1] - 0.45, 0])
        nn = VGroup(*[T(str(v), 22, INK2).next_to(nl.n2p(v), DOWN, buff=0.14) for v in range(1, 10)])
        xt = T("people in the city who match", 24, MUTED).next_to(nn, DOWN, buff=0.18)
        srcs = hits + [cul]
        flyers = VGroup(*[s_.copy() for s_ in srcs])
        self.add(flyers)
        self.qa_mute(flyers)
        order = [i for i in range(9) if i != CULPRIT_AT]
        targets = [lu[order[k]] for k in range(8)] + [lu[CULPRIT_AT]]
        self.play(FadeOut(VGroup(blocks, cr, ar)), FadeOut(VGroup(inn, ex, tot, nine)),
                  *[f.animate.move_to(t.get_center()) for f, t in zip(flyers, targets)], run_time=1.2)
        self.play(FadeOut(flyers), LaggedStart(*[FadeIn(p, scale=0.5) for p in lu], lag_ratio=0.06),
                  Create(nl), FadeIn(nn), FadeIn(xt), run_time=0.9)
        self.word("s046", "nine")
        self.play(LaggedStart(*[Indicate(p, color=WARN, scale_factor=1.15) for p in lu], lag_ratio=0.08), run_time=1.0)

        # ── s047 only one is guilty ──
        self.at("s047", 0.0)
        g_ = lu[CULPRIT_AT]
        others = VGroup(*[p for p in lu if not p.guilty])
        self.word("s047", "one")
        self.play(*[p[0].animate.set_opacity(0.35) for p in others], g_.animate.scale(1.2), run_time=0.6)   # dim the people only: set_opacity on the rings would fill them
        gl = pill("guilty", ORANGE_, 26).next_to(g_, UP, buff=0.25)
        self.play(FadeIn(gl, shift=DOWN * 0.2), run_time=0.4)

        # ── s048 Sam is somewhere in this line: 1 in 9 ──
        self.at("s048", 0.0)
        self.play(*[p[0].animate.set_stroke(opacity=1).set_fill(opacity=0.85) for p in others], g_.animate.scale(1 / 1.2), FadeOut(gl), run_time=0.5)
        sam = sticker("assets/sam.png", 1.25)
        sam.next_to(lu, UP, buff=0.35).set_x(lu[SAM_AT].get_x())
        sam.set_opacity(0)
        self.word("s048", "Sam")
        self.play(sam.animate(rate_func=rate_functions.ease_out_cubic).set_opacity(1), run_time=0.6)
        qm = TB("which one?", 30, INK).next_to(sam, RIGHT, buff=0.3)
        self.play(FadeIn(qm, shift=LEFT * 0.2), run_time=0.4)
        self.word("s048", "matched")
        self.play(LaggedStart(*[Indicate(p[1], color=WARN, scale_factor=1.2) for p in lu], lag_ratio=0.05), run_time=0.9)
        self.word("s048", "guilty")
        fr = VGroup(T("1 guilty", 34, ORANGE_, weight=BOLD), T("÷", 34, INK2), T("9 who match", 34, WARN, weight=BOLD),
                    T("≈ 1 in 9", 40, VIOLET, weight=BOLD)).arrange(RIGHT, buff=0.3)
        frb = card(fr.width + 0.8, fr.height + 0.6, VIOLET); fr.move_to(frb)
        frg = VGroup(frb, fr).move_to(DOWN * 2.1)
        self.play(FadeOut(xt), FadeIn(frg, shift=UP * 0.3), run_time=0.6)

        # ── s049 innocent: about 8 in 9 ≈ 89% ──
        self.at("s049", 0.0)
        self.idle()
        ans = result_card("P(innocent | match)", "≈ 8 in 9  ≈ 89%", VIOLET, 30, 60)
        ans.move_to(UP * 0.4)
        self.play(FadeOut(VGroup(lu, nl, nn, qm)), FadeOut(sam), FadeOut(frg), run_time=0.5)
        self.play(FadeIn(ans, scale=0.7), ripple(ans.get_center(), VIOLET, r=0.8, scale=3), run_time=0.8)
        lk = pill("the locked answer from the start", MUTED, 24).next_to(ans, DOWN, buff=0.35)
        self.play(FadeIn(lk, shift=UP * 0.2), run_time=0.4)
        self.idle(lambda: glint(ans.box, VIOLET))

        # ── s050 recap strip: no formula, just the crowd ──
        self.at("s050", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(ans, lk)), run_time=0.4)
        steps = [("8,000,000 people", AQUA), ("× 1 in a million", WARN), ("≈ 8 innocent + 1 culprit", WARN), ("1 in 9 guilty", VIOLET)]
        chips = VGroup(*[pill(t, c, 26) for t, c in steps]).arrange(RIGHT, buff=0.55).move_to(UP * 0.3)
        if chips.width > 13.0:
            chips.scale_to_fit_width(13.0)
        arrs = VGroup(*[Arrow(chips[k].get_right(), chips[k + 1].get_left(), buff=0.08, stroke_width=4,
                              max_tip_length_to_length_ratio=0.35, color=INK2) for k in range(3)])
        nf = pill("no fancy formula", INK, 28).next_to(chips, UP, buff=0.6)
        self.word("s050", "formula")
        self.play(FadeIn(nf, scale=0.7), run_time=0.4)
        self.word("s050", "imagined")
        for k, c in enumerate(chips):
            self.play(FadeIn(c, shift=RIGHT * 0.2), *([GrowArrow(arrs[k - 1])] if k else []), run_time=0.45)

        # ── s051–s053 the two numbers side by side ──
        self.at("s051", 0.0)
        self.play(FadeOut(VGroup(chips, arrs, nf)), run_time=0.4)
        b1 = cond_box("match", "innocent", value="1 in 1,000,000", color=BLUE_, size=36)
        b2 = cond_box("innocent", "match", value="≈ 8 in 9", color=VIOLET, size=36, vcol=VIOLET)
        b1.move_to(UP * 1.0).set_x(-0.4 - b1.width / 2)
        b2.move_to(UP * 1.0).set_x(0.4 + b2.width / 2)
        b1.value.set_opacity(0); b2.value.set_opacity(0)
        self.qa_mute(VGroup(b1.value, b2.value))
        self.play(FadeIn(b1.box), FadeIn(b1.expr), FadeIn(b2.box), FadeIn(b2.expr), run_time=0.6)
        self.at("s052", 0.0)
        self.qa_mute(b1.value, False)
        self.play(b1.value.animate.set_opacity(1), Indicate(b1.expr, color=BLUE_, scale_factor=1.05), run_time=0.7)
        self.at("s053", 0.0)
        self.qa_mute(b2.value, False)
        self.play(b2.value.animate.set_opacity(1), Indicate(b2.expr, color=VIOLET, scale_factor=1.05), run_time=0.7)

        # ── s054 almost 900,000 times bigger (log scale) ──
        self.at("s054", 0.0)
        self.idle()
        ax = Axes(x_range=[0, 2, 1], y_range=[-6, 0, 1], x_length=4.2, y_length=2.3,
                  axis_config=dict(color=INK2, stroke_width=3, include_tip=False, tick_size=0.06))
        ax.move_to(DOWN * 1.35 + RIGHT * 0.3)
        yl = {-6: "1 in a million", -3: "1 in 1,000", 0: "1"}
        ylabs = VGroup(*[T(t, 20, INK2).next_to(ax.c2p(0, v), LEFT, buff=0.14) for v, t in yl.items()])
        yt = T("chance (log scale)", 20, MUTED).next_to(ylabs, LEFT, buff=0.2).rotate(PI / 2)
        bw = 0.9
        bar1 = Rectangle(width=bw, height=0.06).set_stroke(width=0).set_fill(BLUE_, 1).move_to(ax.c2p(0.55, -6), aligned_edge=DOWN)
        h2 = ax.c2p(0, np.log10(8 / 9))[1] - ax.c2p(0, -6)[1]
        bar2 = Rectangle(width=bw, height=h2).set_stroke(width=0).set_fill(VIOLET, 1).move_to(ax.c2p(1.45, -6), aligned_edge=DOWN)
        self.play(FadeIn(ax), FadeIn(ylabs), FadeIn(yt), FadeIn(bar1), run_time=0.5)
        self.word("s054", "bigger")
        self.play(GrowFromEdge(bar2, DOWN), run_time=0.9)
        times = pill("≈ 889,000 ×", WARN, 32).next_to(bar2, RIGHT, buff=0.4)
        self.play(FadeIn(times, shift=LEFT * 0.2), ripple(times.get_center(), WARN, r=0.4, scale=3), run_time=0.6)
        self.idle(lambda: pulse(times, s=1.12))
        self.finish()
