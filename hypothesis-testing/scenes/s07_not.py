import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def flip_card(n, back_text, w=3.9, h=2.3):
    """A face-down numbered card and its face (red border, the 'NOT …' statement)."""
    down = VGroup(card(w, h, RED_), TB(str(n), 80, RED_))
    down[1].move_to(down[0])
    face = VGroup(card(w, h, RED_), TB("NOT", 36, RED_), T(back_text, 30, INK, weight=BOLD))
    face[2].scale_to_fit_width(min(face[2].width, w - 0.6))
    VGroup(face[1], face[2]).arrange(DOWN, buff=0.22).move_to(face[0])
    return down, face


class S07Not(Base):
    CHAPTER = "What p Is Not"

    def construct(self):
        rng = np.random.default_rng(7)
        # ── s060 three things a p value is not: three face-down cards ──
        self.at("s060", 0.0)
        texts = ["the chance the\ncoin is fair", "how big\nthe effect is", "proof of\nnothing going on"]
        pairs = [flip_card(i + 1, tx) for i, tx in enumerate(texts)]
        downs = VGroup(*[p_[0] for p_ in pairs]).arrange(RIGHT, buff=0.45).move_to(UP * 0.4)
        for (d, f) in pairs:
            f.move_to(d)
        pv = pill("p value", AQUA, 34).move_to(UP * 2.75)
        self.play(FadeIn(pv, scale=0.6), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.6) for d in downs], lag_ratio=0.2), run_time=0.9)
        self.word("s060", "three", dt=-0.3)
        self.play(LaggedStart(*[Indicate(d[1], color=RED_, scale_factor=1.3) for d in downs], lag_ratio=0.2), run_time=0.8)
        self.idle(lambda: LaggedStart(*[pulse(d, 1.06) for d in downs], lag_ratio=0.2))

        def flip(i):
            d, f = pairs[i]
            self.qa_mute(d); self.qa_mute(f)
            w0 = d.width
            f.stretch_to_fit_width(w0).move_to(d)
            self.play(d.animate.stretch(0.02, 0), run_time=0.22)
            f.stretch(0.02, 0)
            self.remove(d); self.add(f)
            self.play(f.animate.stretch_to_fit_width(w0), run_time=0.22)
            self.qa_mute(f, False)

        # ── s061 number one: not the chance the coin is fair ──
        self.at("s061", 0.0)
        self.idle()
        self.word("s061", "one", dt=-0.2)
        flip(0)
        self.play(ripple(pairs[0][1].get_center(), RED_, r=0.6, scale=3), run_time=0.5)
        self.idle(lambda: pulse(pairs[0][1], 1.06))

        # ── s062 not "2% chance the coin is fair", not "2% chance of a fluke" ──
        self.at("s062", 0.0)
        self.idle()
        rest = VGroup(pairs[0][1], *[p_[0] for p_ in pairs[1:]])
        self.play(rest.animate.scale(0.55).move_to(UP * 2.65 + RIGHT * 2.6), FadeOut(pv), run_time=0.6)
        w1 = pill("2% chance the coin is fair", INK, 34).move_to(UP * 0.6)
        w2 = pill("2% chance it was a fluke", INK, 34).move_to(DOWN * 0.7)
        self.word("s062", "two", nth=1, dt=-0.3)
        self.play(FadeIn(w1, shift=UP * 0.3), run_time=0.5)
        no1 = pill("✗ wrong", RED_, 28).next_to(w1, RIGHT, buff=0.35)
        self.play(FadeIn(no1, scale=1.5), w1.animate.set_opacity(0.45), run_time=0.4)
        self.word("s062", "fluke", dt=-0.6)
        self.play(FadeIn(w2, shift=UP * 0.3), run_time=0.5)
        no2 = pill("✗ wrong", RED_, 28).next_to(w2, RIGHT, buff=0.35)
        self.play(FadeIn(no2, scale=1.5), w2.animate.set_opacity(0.45), run_time=0.4)
        self.idle(lambda: AnimationGroup(pulse(no1, 1.12), pulse(no2, 1.12)))

        # ── s063 the straight line: p assumes the coin is fair, then asks about the data ──
        self.at("s063", 0.0)
        self.idle()
        good = MathTex(r"P(\,\text{data}\;\mid\;\text{fair coin}\,)", font_size=64)
        good[0][2:6].set_color(WARN); good[0][7:15].set_color(BLUE_)
        good.move_to(UP * 0.5 + LEFT * 0.6)
        self.play(FadeOut(VGroup(w1, w2, no1, no2), shift=LEFT * 0.6), run_time=0.35)
        self.play(Write(good), run_time=0.7)
        self.word("s063", "assumes", dt=-0.3)
        bar_ = good[0][6]
        self.play(Indicate(bar_, color=WARN, scale_factor=1.8), run_time=0.6)
        a1 = T("assumes", 26, BLUE_, weight=BOLD).next_to(good, DOWN, buff=0.35).align_to(good[0][7], LEFT)
        a2 = T("asks about", 26, WARN, weight=BOLD).next_to(good, DOWN, buff=0.35).align_to(good[0][2], LEFT)
        self.play(FadeIn(a1, shift=UP * 0.2), run_time=0.4)
        self.word("s063", "data", dt=-0.3)
        self.play(FadeIn(a2, shift=UP * 0.2), run_time=0.4)
        ok = check(AQUA, 0.35).next_to(good, RIGHT, buff=0.4)
        self.play(Create(ok), run_time=0.4)
        self.word("s063", "coin", nth=1, dt=-0.5)
        notc = pill("never asks about the coin", RED_, 28).move_to(DOWN * 1.6)
        self.play(FadeIn(notc, shift=UP * 0.3), run_time=0.5)
        self.idle(lambda: pulse(notc, 1.1), lambda: Indicate(bar_, color=WARN, scale_factor=1.6))

        # ── s064 the same flip as Bayes ──
        self.at("s064", 0.0)
        self.idle()
        cue = card_cue("Bayes' Theorem", mini_bayes())
        self.play(FadeOut(VGroup(notc, a1, a2, ok, rest), shift=UP * 0.4), FadeIn(cue, shift=LEFT * 1.0),
                  good.animate.move_to(DOWN * 0.15 + LEFT * 1.5), run_time=0.6)
        bay1 = MathTex(r"P(\text{positive}\mid\text{sick})", font_size=52, color=INK2)
        bay2 = MathTex(r"P(\text{sick}\mid\text{positive})", font_size=52, color=INK2)
        neq1 = MathTex(r"\neq", font_size=60, color=RED_)
        brow = VGroup(bay1, neq1, bay2).arrange(RIGHT, buff=0.35).move_to(UP * 1.5)
        lab_b = T("Bayes video", 24, VIOLET, weight=BOLD).next_to(brow, LEFT, buff=0.35)
        self.word("s064", "sick", dt=-0.3)
        self.play(FadeIn(bay1, shift=RIGHT * 0.3), FadeIn(lab_b), run_time=0.5)
        self.word("s064", "positive", nth=1, dt=-0.3)
        self.play(FadeIn(neq1, scale=1.6), FadeIn(bay2, shift=LEFT * 0.3), run_time=0.5)
        bad = MathTex(r"P(\,\text{fair coin}\;\mid\;\text{data}\,)", font_size=64)
        bad[0][2:10].set_color(BLUE_); bad[0][11:15].set_color(WARN)
        neq2 = MathTex(r"\neq", font_size=72, color=RED_)
        nrow = VGroup(good.copy(), neq2, bad).arrange(RIGHT, buff=0.35).move_to(DOWN * 0.15)
        if nrow.width > 12.6:
            nrow.scale_to_fit_width(12.6)
        self.word("s064", "And", dt=-0.2)
        self.play(good.animate.move_to(nrow[0]).scale(nrow[0].height / good.height), run_time=0.5)
        self.play(FadeIn(neq2, scale=1.6), TransformFromCopy(good, bad), run_time=0.8)
        swap = CurvedArrow(good.get_bottom() + DOWN * 0.15, bad.get_bottom() + DOWN * 0.15, angle=PI / 3, color=RED_, stroke_width=4)
        swl = T("flipped", 26, RED_, weight=BOLD).next_to(swap, DOWN, buff=0.1)
        self.play(Create(swap), FadeIn(swl), run_time=0.6)
        self.idle(lambda: ShowPassingFlash(swap.copy().set_stroke(RED_, 9), time_width=0.6), lambda: pulse(cue, 1.06))

        # ── s065 number two: not how big the effect is ──
        self.at("s065", 0.0)
        self.idle()
        d2, f2 = pairs[1]
        f2.move_to(UP * 0.4).scale(1.0)
        d2.move_to(UP * 0.4)
        self.play(FadeOut(VGroup(bay1, bay2, neq1, lab_b, good, bad, neq2, swap, swl, cue), shift=LEFT * 0.8), run_time=0.5)
        if d2.width < 3: d2.scale(1 / 0.55)
        d2.move_to(UP * 0.4)
        self.play(FadeIn(d2, scale=0.6), run_time=0.4)
        self.word("s065", "two", dt=-0.2)
        flip(1)
        self.idle(lambda: pulse(f2, 1.06))

        # ── s066 a tiny p does not mean very rigged ──
        self.at("s066", 0.0)
        self.idle()
        self.play(f2.animate.scale(0.6).move_to(UP * 2.4 + LEFT * 3.6), run_time=0.5)
        ruler = VGroup(Rectangle(width=4.2, height=0.6).set_stroke(WARN, 3).set_fill("#22221f", 1),
                       *[Line(UP * 0.3, UP * (0.3 - (0.28 if k % 2 == 0 else 0.16))).set_stroke(WARN, 2).shift(LEFT * 2.1 + RIGHT * 0.42 * k)
                         for k in range(11)])
        ruler[0].qa_container = True
        for x in ruler[1:]: x.qa_ignore = True
        ruler.move_to(UP * 0.2 + RIGHT * 1.6)
        tinyp = pill("tiny p", AQUA, 32).next_to(ruler, LEFT, buff=0.6)
        q_ = TB("?", 60, WARN).next_to(ruler, RIGHT, buff=0.3)
        self.word("s066", "tiny", dt=-0.3)
        self.play(FadeIn(tinyp, shift=RIGHT * 0.3), Create(ruler[0]), run_time=0.5)
        self.play(LaggedStart(*[Create(x) for x in ruler[1:]], lag_ratio=0.08), run_time=0.6)
        self.word("s066", "rigged", dt=-0.3)
        self.play(FadeIn(q_, scale=0.5), run_time=0.35)
        later = pill("we'll see why in a moment", MUTED, 26).move_to(DOWN * 1.4 + RIGHT * 1.0)
        self.word("s066", "moment", dt=-0.6)
        self.play(FadeIn(later, shift=UP * 0.2), run_time=0.4)
        self.idle(lambda: Wiggle(q_, scale_value=1.3), lambda: pulse(ruler, 1.06))

        # ── s067 number three: a big p does not prove the boring explanation ──
        self.at("s067", 0.0)
        self.idle()
        d3, f3 = pairs[2]
        if d3.width < 3: d3.scale(1 / 0.55)
        d3.move_to(UP * 0.4); f3.move_to(UP * 0.4)
        self.play(FadeOut(VGroup(ruler, tinyp, q_, later, f2), shift=LEFT * 0.8), FadeIn(d3, scale=0.6), run_time=0.5)
        self.word("s067", "three", dt=-0.2)
        flip(2)
        self.idle(lambda: pulse(f3, 1.06))

        # ── s068 five flips, four heads: big p, but that shows nothing ──
        self.at("s068", 0.0)
        self.idle()
        self.play(f3.animate.scale(0.6).move_to(UP * 2.45 + RIGHT * 3.7), run_time=0.5)
        c5 = coin("H", BLUE_, 0.45).move_to(LEFT * 5.2 + UP * 1.5)
        tiles5 = VGroup(*[Square(0.5).set_stroke(WARN if f == "H" else MUTED, 2.5).set_fill("#22221f", 1) for f in "HHTHH"]).arrange(RIGHT, buff=0.1)
        tiles5.next_to(c5, DOWN, buff=0.35)
        for s_ in tiles5: s_.qa_container = True
        let5 = VGroup(*[T(f, 24, WARN if f == "H" else MUTED, weight=BOLD).move_to(s_) for f, s_ in zip("HHTHH", tiles5)])
        self.play(FadeIn(c5, scale=0.5), run_time=0.3)
        for k in range(5):
            self.play(flipping(c5), FadeIn(tiles5[k], scale=1.4), FadeIn(let5[k]), run_time=0.22)
        ch5 = xy_axes([0, 6, 1], [0, 400, 100], 4.2, 2.6, "heads in 5 flips", "friends (of 1,000)", font_size=20, y_vertical=True, x_labels={})
        ch5.move_to(LEFT * 0.7 + DOWN * 0.15)
        e5 = [1000 * comb(5, k) / 32 for k in range(6)]
        b5 = VGroup(*[bar(ch5.ax, k + 0.5, e5[k], BLUE_, width=0.5) for k in range(6)])
        kl = VGroup(*[T(str(k), 20, INK2).next_to(ch5.ax.c2p(k + 0.5, 0), DOWN, buff=0.14) for k in range(6)])
        ch5.xt.next_to(kl, DOWN, buff=0.15).align_to(ch5.ax.x_axis, RIGHT)
        self.play(Create(ch5.ax), FadeIn(ch5.labs), FadeIn(kl), FadeIn(ch5.xt), FadeIn(ch5.yt), run_time=0.5)
        self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b5], lag_ratio=0.1), run_time=0.6)
        self.word("s068", "large", dt=-0.4)
        self.play(*[b5[k].animate.set_fill(AQUA, 1) for k in (4, 5)], run_time=0.4)
        big_p = pill("p ≈ 0.19: large", AQUA, 28).move_to(RIGHT * 4.2 + UP * 1.0)
        self.play(FadeIn(big_p, scale=0.6), run_time=0.4)
        self.word("s068", "doesn't", dt=-0.2)
        nf = pill("does NOT show the coin is fair", RED_, 24).move_to(RIGHT * 4.2 + UP * 0.1)
        self.play(FadeIn(nf, shift=UP * 0.2), run_time=0.4)
        self.word("s068", "five", nth=1, dt=-0.3)
        few = pill("5 flips can't tell you much", INK, 24).move_to(RIGHT * 4.2 + DOWN * 0.8)
        self.play(FadeIn(few, shift=LEFT * 0.2), run_time=0.4)
        self.idle(lambda: flipping(c5), lambda: pulse(nf, 1.08))

        # ── s069 in court: not guilty ≠ innocent ──
        self.at("s069", 0.0)
        self.idle()
        gav = VGroup(RoundedRectangle(corner_radius=0.08, width=1.2, height=0.42).set_stroke(WARN, 4).set_fill(WARN, 0.9),
                     Line(ORIGIN, DOWN * 0.9).set_stroke(WARN, 6))
        gav[1].next_to(gav[0], DOWN, buff=0)
        gav.rotate(-0.5).move_to(LEFT * 3.6 + UP * 0.6)
        block_ = Rectangle(width=1.4, height=0.3).set_stroke(width=0).set_fill(WARN, 0.6).move_to(LEFT * 3.0 + DOWN * 0.45)
        block_.qa_joined = True
        stage = VGroup(c5, tiles5, let5, ch5, kl, b5, big_p, nf, few, f3)
        self.play(FadeOut(stage, shift=LEFT * 1.0), run_time=0.5)
        self.play(FadeIn(block_), FadeIn(gav, shift=DOWN * 0.3), run_time=0.4)
        self.play(Rotate(gav, 0.5, about_point=gav[1].get_end()), run_time=0.25)
        self.play(Rotate(gav, -0.5, about_point=gav[1].get_end()), ripple(block_.get_center(), WARN, r=0.3, scale=4), run_time=0.3)
        ng = pill("not guilty", BLUE_, 36).move_to(RIGHT * 2.2 + UP * 1.0)
        ni = pill("≠  proven innocent", RED_, 32).next_to(ng, DOWN, buff=0.45)
        ee = pill("= not enough evidence", WARN, 32).next_to(ni, DOWN, buff=0.45)
        self.word("s069", "guilty", dt=-0.3)
        self.play(FadeIn(ng, shift=LEFT * 0.3), run_time=0.4)
        self.word("s069", "innocent", dt=-0.4)
        self.play(FadeIn(ni, shift=LEFT * 0.3), run_time=0.4)
        self.word("s069", "enough", dt=-0.4)
        self.play(FadeIn(ee, shift=LEFT * 0.3), run_time=0.4)
        self.idle(lambda: pulse(ee, 1.1), lambda: Rotate(gav, 0.3, about_point=gav[1].get_end(), rate_func=there_and_back))
        self.until(SEGS["s069"]["end"] + 0.2)
        self.idle()
        self.play(FadeOut(VGroup(gav, block_, ng, ni, ee), shift=LEFT * 1.0), run_time=0.5)
        self.finish()
