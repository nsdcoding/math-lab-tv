import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def cradle(color=INK2, s=1.0):
    basket = Arc(radius=0.45, start_angle=PI, angle=PI).set_stroke(color, 4)
    rim = Line(LEFT * 0.45, RIGHT * 0.45).set_stroke(color, 4)
    rock = Arc(radius=0.6, start_angle=-PI * 0.8, angle=PI * 0.6).set_stroke(color, 3).shift(UP * 0.05)
    return VGroup(basket, rim, rock).scale(s)


def house(color=INK2, w=3.4, h=1.7):
    body = Rectangle(width=w, height=h).set_stroke(color, 3)
    roof = Polygon(body.get_corner(UL) + LEFT * 0.2, body.get_corner(UR) + RIGHT * 0.2, body.get_top() + UP * 0.8).set_stroke(color, 3)
    for m in (body, roof):
        m.qa_ignore = True
    return VGroup(body, roof)


class S09RealCase(Base):
    CHAPTER = "A Real Courtroom"

    def construct(self):
        # ── s074 a real case, England, 1999 ──
        self.at("s074", 0.0)
        t1 = TB("A real case", 52, INK)
        t2 = T("England · 1999", 34, INK2)
        inner = VGroup(t1, t2).arrange(DOWN, buff=0.3)
        bx = card(inner.width + 1.4, inner.height + 0.9, INK2); inner.move_to(bx)
        rc = VGroup(bx, inner).move_to(UP * 0.8)
        self.play(FadeIn(rc, shift=UP * 0.3), run_time=0.7)
        self.word("s074", "convicted")
        nt = T("no names or photos: the details are in the pinned comment", 24, MUTED).next_to(rc, DOWN, buff=0.45)
        self.play(FadeIn(nt), run_time=0.5)
        self.word("s074", "babies")
        cr = VGroup(cradle(INK2), cradle(INK2)).arrange(RIGHT, buff=0.6).next_to(nt, DOWN, buff=0.4)
        self.play(FadeIn(cr, shift=UP * 0.2), run_time=0.6)

        # ── s075 one sudden infant death: about 1 in 8,543 ──
        self.at("s075", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(nt, cr)), rc.animate.scale(0.6).to_edge(UP, buff=0.4).to_edge(RIGHT, buff=0.5), run_time=0.6)
        one = result_card("one sudden infant death, for a family like hers", "about 1 in 8,543", BLUE_, 28, 52).move_to(UP * 0.4)
        self.word("s075", "expert")
        self.play(FadeIn(one, shift=UP * 0.3), run_time=0.6)
        self.word("s075", "eight")
        self.play(pulse(one.value, s=1.12), run_time=0.6)

        # ── s076 multiplied by itself: about 1 in 73 million ──
        self.at("s076", 0.0)
        self.play(one.animate.scale(0.7).move_to(UP * 1.4), run_time=0.5)
        eq = VGroup(T("1 in 8,543", 40, BLUE_, weight=BOLD), T("×", 44, RED_, weight=BOLD), T("1 in 8,543", 40, BLUE_, weight=BOLD),
                    T("≈", 44, INK2), T("1 in 73,000,000", 44, WARN, weight=BOLD)).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.5)
        self.word("s076", "multiplied")
        self.play(FadeIn(eq[0]), FadeIn(eq[1], scale=0.5), FadeIn(eq[2]), run_time=0.7)
        ul = Line(eq[1].get_corner(DL) + DOWN * 0.15 + LEFT * 0.1, eq[1].get_corner(DR) + DOWN * 0.15 + RIGHT * 0.1).set_stroke(RED_, 5)
        self.play(Create(ul), run_time=0.3)
        self.word("s076", "seventy")
        self.play(FadeIn(eq[3]), FadeIn(eq[4], scale=0.6), ripple(eq[4].get_center(), WARN, r=0.6, scale=3), run_time=0.7)

        # ── s077 problem one: the deaths may not be unrelated ──
        self.at("s077", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(one, ul)), eq.animate.scale(0.75).move_to(UP * 1.8), run_time=0.5)
        p1 = pill("problem 1: treated as unrelated", RED_, 32).move_to(UP * 0.75)
        self.word("s077", "First")
        self.play(FadeIn(p1, shift=UP * 0.2), run_time=0.5)
        hs = house(INK2).move_to(DOWN * 1.1 + LEFT * 2.6)
        crs = VGroup(cradle(INK2, 0.8), cradle(INK2, 0.8)).arrange(RIGHT, buff=0.6).move_to(hs[0])
        self.word("s077", "families")
        self.play(Create(hs), FadeIn(crs), run_time=0.7)
        lk = DashedLine(crs[0].get_right(), crs[1].get_left(), color=WARN, stroke_width=4)
        tags = VGroup(T("shared genes", 28, WARN, weight=BOLD), T("shared home", 28, WARN, weight=BOLD)).arrange(DOWN, buff=0.25)
        tags.next_to(hs, RIGHT, buff=0.8)
        self.word("s077", "genes")
        self.play(Create(lk), FadeIn(tags[0], shift=LEFT * 0.2), run_time=0.5)
        self.word("s077", "homes")
        self.play(FadeIn(tags[1], shift=LEFT * 0.2), run_time=0.4)
        mr = T("→ a second death is more\n   likely after a first", 28, INK).next_to(tags, DOWN, buff=0.35).align_to(tags, LEFT)
        if mr.get_right()[0] > 6.6:
            mr.scale_to_fit_width(6.6 - mr.get_left()[0])
        self.word("s077", "second")
        self.play(FadeIn(mr, shift=UP * 0.2), run_time=0.5)

        # ── s078 problem two: the swap ──
        self.at("s078", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(p1, hs, crs, lk, tags, mr)), run_time=0.5)
        b1 = cond_box("two deaths", "innocent", value="1 in 73 million?", color=BLUE_, size=34)
        b2 = cond_box("innocent", "two deaths", value="?", color=VIOLET, size=34)
        b1.move_to(DOWN * 0.3).set_x(-0.4 - b1.width / 2); b2.move_to(DOWN * 0.3).set_x(0.4 + b2.width / 2)
        b2.value.match_y(b1.value)
        self.word("s078", "swap")
        self.play(FadeIn(b1, shift=UP * 0.2), FadeIn(b2, shift=UP * 0.2), run_time=0.6)
        self.word("s078", "presented")
        fly = b1.value.copy(); self.qa_mute(fly)
        self.play(FadeOut(b2.value), fly.animate.move_to(b2.value).set_color(RED_).scale(0.85), run_time=0.9)
        stamp = pill("THE SWAP", RED_, 40).rotate(0.1).next_to(b2, DOWN, buff=0.3)
        self.play(FadeIn(stamp, scale=1.6), ripple(stamp.get_center(), RED_, r=0.5, scale=3), run_time=0.6)

        # ── s079 compare two rare explanations (balance beam, shape only) ──
        self.at("s079", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(b1, b2, fly, stamp, eq)), run_time=0.5)
        bs, th, L, R = beam_scale(6.4, INK2)
        bs.move_to(DOWN * 0.15)
        self.add(bs)
        self.play(FadeIn(bs), run_time=0.5)
        ln = VGroup(T("two natural deaths", 28, BLUE_, weight=BOLD), T("rare", 24, INK2)).arrange(DOWN, buff=0.12)
        rn = VGroup(T("two murders of babies", 28, RED_, weight=BOLD), T("even rarer", 24, INK2)).arrange(DOWN, buff=0.12)
        ln.add_updater(lambda m: m.next_to(L, DOWN, buff=0.2))
        rn.add_updater(lambda m: m.next_to(R, DOWN, buff=0.2))
        self.word("s079", "murder")
        self.play(FadeIn(rn), run_time=0.5)
        self.word("s079", "which")
        self.play(FadeIn(ln), run_time=0.5)
        so = T("shape only", 22, MUTED).next_to(bs, UP, buff=1.2)
        self.word("s079", "points")
        self.play(th.animate.set_value(-0.22), FadeIn(so), run_time=1.2)
        more = pill("more likely", BLUE_, 26)
        more.add_updater(lambda m: m.next_to(ln, DOWN, buff=0.2))
        self.play(FadeIn(more, scale=0.6), run_time=0.4)

        # ── s080 overturned in 2003 ──
        self.at("s080", 0.0)
        self.idle()
        for m in (ln, rn, more):
            m.clear_updaters()
        self.play(FadeOut(VGroup(bs, ln, rn, more, so)), run_time=0.5)
        sp = pill("statisticians spoke out", AQUA, 32).move_to(UP * 0.9)
        ov = result_card("2003", "conviction overturned", AQUA, 32, 48).next_to(sp, DOWN, buff=0.5)
        self.word("s080", "Statisticians")
        self.play(FadeIn(sp, shift=UP * 0.2), run_time=0.5)
        self.word("s080", "overturned")
        self.play(FadeIn(ov, scale=0.8), run_time=0.6)
        self.idle(lambda: pulse(ov, s=1.05))
        self.finish()
