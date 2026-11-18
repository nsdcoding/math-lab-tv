import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def claim_card(n, lines, color=INK2, w=11.6):
    num = TB(f"Claim {n}", 34, WARN)
    body = VGroup(*[T(l, 30, INK) for l in lines]).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    inner = VGroup(num, body).arrange(RIGHT, buff=0.55)
    box = card(max(w, inner.width + 0.9), inner.height + 0.65, color)
    inner.move_to(box)
    g = VGroup(box, inner); g.box = box
    return g.move_to(UP * 1.55)


def stamp(text, color):
    return pill(text, color, 40).rotate(0.08)


def flame(color=RED_, s=0.3):
    return VMobject().set_points_smoothly([np.array(p) * s for p in [(0, 1.1, 0), (0.55, 0.1, 0), (0.35, -0.5, 0), (0, -0.6, 0),
                                                                        (-0.35, -0.5, 0), (-0.55, 0.1, 0), (0, 1.1, 0)]]
                                           ).set_stroke(color, 3).set_fill(color, 0.85)


def toast(color=WARN, s=0.3):
    return RoundedRectangle(corner_radius=0.25 * s, width=1.2 * s * 1.4, height=1.2 * s * 1.4).set_stroke(color, 3).set_fill("#5a3d1c", 1)


def envelope(color=INK2, fill=None):
    b = Rectangle(width=0.62, height=0.42).set_stroke(color, 3).set_fill(fill or "#22221f", 1)
    f = VMobject().set_points_as_corners([b.get_corner(UL), b.get_center() + DOWN * 0.04, b.get_corner(UR)]).set_stroke(color, 2.5)
    return VGroup(b, f)


class S12Quiz(Base):
    CHAPTER = "Spot the Swap"

    def construct(self):
        # ── s101 four claims: swap or fair? ──
        self.at("s101", 0.0)
        hd = TB("spot the swap", 60, INK).move_to(UP * 1.2)
        tg = VGroup(pill("swap?", RED_, 36), pill("fair?", AQUA, 36)).arrange(RIGHT, buff=0.8).next_to(hd, DOWN, buff=0.6)
        self.play(FadeIn(hd, scale=0.8), run_time=0.6)
        self.word("s101", "four")
        slots = VGroup(*[card(1.0, 1.0, GRID) for _ in range(4)]).arrange(RIGHT, buff=0.3).next_to(tg, DOWN, buff=0.5)
        nums = VGroup(*[T(str(k + 1), 34, MUTED, weight=BOLD).move_to(sl) for k, sl in enumerate(slots)])
        self.play(LaggedStart(*[FadeIn(VGroup(sl, n_), shift=UP * 0.2) for sl, n_ in zip(slots, nums)], lag_ratio=0.15), run_time=0.8)
        self.word("s101", "swap", nth=0)
        self.play(FadeIn(tg[0], scale=0.6), run_time=0.4)
        self.word("s101", "fair")
        self.play(FadeIn(tg[1], scale=0.6), run_time=0.4)

        # ── s102 claim 1: smoke alarm ──
        self.at("s102", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(hd, tg, slots, nums)), run_time=0.4)
        c1 = claim_card(1, ["The alarm almost always beeps when there's a fire.", "So when it beeps, there's almost certainly a fire?"])
        self.play(FadeIn(c1, shift=DOWN * 0.3), run_time=0.6)
        th = T("decide…", 30, MUTED).move_to(DOWN * 0.6)
        self.word("s102", "So")
        self.play(FadeIn(th), run_time=0.4)
        self.idle(lambda: pulse(th, s=1.15))

        # ── s103 swap: most beeps are burnt toast ──
        self.at("s103", 0.0)
        self.idle()
        s1 = stamp("SWAP", RED_).next_to(c1, DOWN, buff=0.15).align_to(c1, RIGHT).shift(LEFT * 0.4)
        self.play(FadeOut(th), FadeIn(s1, scale=1.6), ripple(s1.get_center(), RED_, r=0.5, scale=3), run_time=0.6)
        icons = VGroup(*[(flame() if k in (3, 11) else toast()) for k in range(16)]).arrange_in_grid(2, 8, buff=(0.45, 0.3))
        icons.move_to(DOWN * 1.0 + LEFT * 1.8)
        lab = T("every beep (illustration)", 24, INK2).next_to(icons, RIGHT, buff=0.4)
        self.word("s103", "every")
        self.play(LaggedStart(*[FadeIn(i, scale=0.5) for i in icons], lag_ratio=0.05), FadeIn(lab), run_time=1.0)
        self.word("s103", "toast")
        self.play(LaggedStart(*[pulse(icons[k], s=1.25) for k in range(16) if k not in (3, 11)], lag_ratio=0.05), run_time=0.9)

        # ── s104 claim 2: tall basketball players ──
        self.at("s104", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(c1, s1, icons, lab)), run_time=0.4)
        c2 = claim_card(2, ["Nearly every professional basketball player is tall.", "So if you're tall, you're probably a pro?"])
        self.play(FadeIn(c2, shift=DOWN * 0.3), run_time=0.6)
        th = T("decide…", 30, MUTED).move_to(DOWN * 0.6)
        self.word("s104", "So")
        self.play(FadeIn(th), run_time=0.4)
        self.idle(lambda: pulse(th, s=1.15))

        # ── s105 swap: millions of tall people, a few hundred pros ──
        self.at("s105", 0.0)
        self.idle()
        s2 = stamp("SWAP", RED_).next_to(c2, DOWN, buff=0.15).align_to(c2, RIGHT).shift(LEFT * 0.4)
        self.play(FadeOut(th), FadeIn(s2, scale=1.6), ripple(s2.get_center(), RED_, r=0.5, scale=3), run_time=0.6)
        tall = VGroup(*[person(ORANGE_ if k in (17,) else INK2, 0.62, fill=0.6 if k == 17 else 0.15) for k in range(36)])
        tall.arrange_in_grid(2, 18, buff=(0.12, 0.2)).move_to(DOWN * 1.05 + LEFT * 1.3)
        tl = VGroup(T("tall people: millions", 24, INK2), T("pros: a few hundred", 24, ORANGE_, weight=BOLD)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        tl.next_to(tall, RIGHT, buff=0.35)
        il = T("illustration", 20, MUTED).next_to(tl, DOWN, buff=0.12).align_to(tl, LEFT)
        self.word("s105", "millions")
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in tall], lag_ratio=0.02), FadeIn(tl[0]), FadeIn(il), run_time=0.9)
        self.word("s105", "few")
        self.play(pulse(tall[17], s=1.4), FadeIn(tl[1]), run_time=0.6)

        # ── s106 claim 3: 1 in 9 of matches guilty ──
        self.at("s106", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(c2, s2, tall, tl, il)), run_time=0.4)
        c3 = claim_card(3, ["Out of everyone in the city who matched the trace,", "about 1 in 9 is guilty."])
        self.play(FadeIn(c3, shift=DOWN * 0.3), run_time=0.6)
        lu = lineup(9, 6, 0.6, 0.2).move_to(DOWN * 1.05)
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in lu], lag_ratio=0.06), run_time=0.7)

        # ── s107 fair: starts from the people who match ──
        self.at("s107", 0.0)
        s3 = pill("FAIR ✓", AQUA, 40).rotate(0.08).next_to(c3, DOWN, buff=0.15).align_to(c3, RIGHT).shift(LEFT * 0.4)
        self.word("s107", "fair")
        self.play(FadeIn(s3, scale=1.6), ripple(s3.get_center(), AQUA, r=0.5, scale=3), run_time=0.6)
        gm = pill("given: match", WARN, 28).next_to(lu, DOWN, buff=0.3)
        self.word("s107", "starts")
        self.play(FadeIn(gm, shift=UP * 0.2), run_time=0.4)
        self.word("s107", "jury")
        self.play(pulse(lu[6], s=1.3), run_time=0.6)

        # ── s107a claim 4: spam filter ──
        self.at("s107a", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(c3, s3, lu, gm)), run_time=0.4)
        c4 = claim_card(4, ["A spam filter catches 9 out of 10 spam emails.", "So 9 out of 10 emails it blocks are spam?"])
        self.play(FadeIn(c4, shift=DOWN * 0.3), run_time=0.6)
        th = T("decide…", 30, MUTED).move_to(DOWN * 0.6)
        self.word("s107a", "So")
        self.play(FadeIn(th), run_time=0.4)
        self.idle(lambda: pulse(th, s=1.15))

        # ── s107b swap: how many real emails does it block? ──
        self.at("s107b", 0.0)
        self.idle()
        s4 = stamp("SWAP", RED_).next_to(c4, DOWN, buff=0.15).align_to(c4, RIGHT).shift(LEFT * 0.4)
        self.play(FadeOut(th), FadeIn(s4, scale=1.6), ripple(s4.get_center(), RED_, r=0.5, scale=3), run_time=0.6)
        env = VGroup(*[envelope(BLUE_ if k in (1, 4, 6, 9, 12) else WARN) for k in range(14)]).arrange_in_grid(2, 7, buff=(0.3, 0.25))
        env.move_to(DOWN * 1.05 + LEFT * 1.6)
        el = VGroup(T("blocked emails", 24, INK2, weight=BOLD), T("spam", 24, WARN, weight=BOLD), T("real email", 24, BLUE_, weight=BOLD)
                    ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(env, RIGHT, buff=0.4)
        il = T("illustration", 20, MUTED).next_to(el, DOWN, buff=0.1).align_to(el, LEFT)
        self.word("s107b", "blocked")
        self.play(LaggedStart(*[FadeIn(e, scale=0.5) for e in env], lag_ratio=0.04), FadeIn(el), FadeIn(il), run_time=0.9)
        self.word("s107b", "real")
        self.play(LaggedStart(*[pulse(env[k], s=1.3) for k in (1, 4, 6, 9, 12)], lag_ratio=0.1), run_time=0.8)
        cr = pill("the crowd again", AQUA, 28).move_to(DOWN * 2.3)
        self.word("s107b", "crowd")
        self.play(FadeIn(cr, shift=UP * 0.2), run_time=0.4)
        self.finish()
