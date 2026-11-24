import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

A, B_ = 170, 0.04          # "any line": guesses 210, 230, 250, 270, 290; misses -70, -10, 0, +10, +70
HX, HY = 1000, 140         # the house we zoom in on: guessed 210, sold 140, miss -70


def panel(*mobs, top=2.0, buff=0.35):
    g = VGroup(*mobs).arrange(DOWN, buff=buff, aligned_edge=LEFT)
    g.move_to(RIGHT * PANEL_X).align_to(UP * top, UP)
    return g


class S04Miss(Base):
    CHAPTER = "Measuring a Miss"

    def construct(self):
        axg = lesson_axes(); ax = axg.ax
        dots = house_dots(ax)
        self.add(axg, dots)

        # ── s022 any line ──
        self.at("s022", 0.0)
        ln = price_line(ax, A, B_, 0, 3500)
        self.play(Create(ln), run_time=1.0)
        anyl = pill("any line", VIOLET, 30)
        q = T("how good is it?", 30, INK)
        p1 = panel(anyl, q, top=2.3)
        self.play(FadeIn(anyl, shift=LEFT * 0.2), run_time=0.4)
        self.until(word_time("s022", word_index("s022", "We")))
        self.play(FadeIn(q), run_time=0.4)

        # ── s023 a price guesser ──
        self.at("s023", 0.0)
        xv = ValueTracker(500)
        riser = always_redraw(lambda: DashedLine(ax.c2p(xv.get_value(), 0), ax.c2p(xv.get_value(), A + B_ * xv.get_value()),
                                                 color=INK2, stroke_width=3))
        across = always_redraw(lambda: DashedLine(ax.c2p(xv.get_value(), A + B_ * xv.get_value()), ax.c2p(0, A + B_ * xv.get_value()),
                                                  color=VIOLET, stroke_width=3))
        cur = always_redraw(lambda: Triangle(color=INK, fill_opacity=1, stroke_width=0).scale(0.11).move_to(ax.c2p(xv.get_value(), 0) + DOWN * 0.02))
        for m in (riser, across, cur):
            self.qa_mute(m)
        guess = T("size in  →  price out", 30, VIOLET, weight=BOLD)
        panel(guess, top=0.6)
        self.play(FadeOut(q), FadeIn(riser), FadeIn(across), FadeIn(cur), FadeIn(guess), run_time=0.5)
        self.play(xv.animate.set_value(3200), run_time=2.4, rate_func=smooth)
        self.play(xv.animate.set_value(HX), run_time=1.0, rate_func=smooth)

        # ── s024 guessed vs sold at 1,500 ──
        self.at("s024", 0.0)
        for m in (riser, across, cur):
            m.clear_updaters()
        self.play(FadeOut(VGroup(riser, across, cur, guess)), run_time=0.3)
        gdot = Circle(radius=0.12, color=VIOLET, stroke_width=4).set_fill(BG, 1).move_to(ax.c2p(HX, A + B_ * HX))
        gdot.qa_dot = True
        self.play(FadeIn(gdot, scale=0.4), run_time=0.4)
        gl = T("guessed  $210k", 30, VIOLET, weight=BOLD)
        sl = T("sold  $140k", 30, INK, weight=BOLD)
        p2 = panel(gl, sl, top=1.2)
        self.until(word_time("s024", word_index("s024", "What")))
        self.play(FadeIn(gl, shift=LEFT * 0.2), Indicate(gdot, color=VIOLET), run_time=0.7)
        self.until(word_time("s024", word_index("s024", "really")))
        self.play(FadeIn(sl, shift=LEFT * 0.2), Indicate(dots[0], color=WARN, scale_factor=1.6), run_time=0.7)

        # ── s025 the miss, the residual ──
        self.at("s025", 0.0)
        bar = miss_bar(ax, HX, HY, A, B_)
        self.add(bar); self.bring_to_front(gdot, dots[0])
        self.play(Create(bar), run_time=0.6)
        ml = T("−$70k", 28, ORANGE_, weight=BOLD).next_to(bar, RIGHT, buff=0.18)
        self.play(FadeIn(ml), run_time=0.3)
        self.until(word_time("s025", word_index("s025", "Statisticians")))
        d1 = T("the miss  =  residual", 30, ORANGE_, weight=BOLD)
        d2 = T("sold − guessed", 28, INK)
        d3 = T("140 − 210 = −70", 28, INK2)
        box_txt = VGroup(d1, d2, d3).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        dbox = card(box_txt.width + 0.6, box_txt.height + 0.55, color=ORANGE_)
        dbox.move_to(box_txt)
        dc = VGroup(dbox, box_txt)
        dc.move_to(RIGHT * PANEL_X + DOWN * 1.15)
        self.play(FadeIn(dc, shift=UP * 0.2), run_time=0.6)
        self.until(word_time("s025", word_index("s025", "left")))
        self.play(Indicate(d1, color=ORANGE_, scale_factor=1.1), run_time=0.7)

        # ── s026 straight up and down, not the shortest distance ──
        self.at("s026", 0.0)
        self.play(FadeOut(VGroup(gl, sl, dc, anyl)), run_time=0.4)
        P = np.array(ax.c2p(HX, HY)); L0 = np.array(ax.c2p(0, A)); L1 = np.array(ax.c2p(3500, A + B_ * 3500))
        u = (L1 - L0) / np.linalg.norm(L1 - L0)
        foot = L0 + np.dot(P - L0, u) * u
        perp = DashedLine(P, foot, color=MUTED, stroke_width=4, dash_length=0.06)
        # zoom in on the house so the two distances are easy to see
        fr = self.camera.frame
        zc = ax.c2p(HX + 150, 175)
        self.play(fr.animate.scale(0.5).move_to(zc), FadeOut(axg.xt), FadeOut(axg.yt), FadeOut(axg.labs), run_time=1.0)
        self.until(word_time("s026", word_index("s026", "straight")))
        self.play(Indicate(bar, color=ORANGE_, scale_factor=1.15), run_time=0.7)
        self.until(word_time("s026", word_index("s026", "Not")))
        self.play(Create(perp), run_time=0.5)
        px = cross(RED_, 0.09).move_to(perp.get_center() + UR * 0.05)
        self.play(Create(px), run_time=0.4)

        # ── s027 because up and down is price ──
        self.at("s027", 0.0)
        dl = T("measured in $", 16, ORANGE_, weight=BOLD).next_to(ml, DOWN, buff=0.08).align_to(ml, LEFT)
        self.until(word_time("s027", word_index("s027", "price.")))
        self.play(FadeIn(dl), Indicate(ml, color=ORANGE_), run_time=0.6)
        mx = T("mixes sq ft and $", 16, MUTED).next_to(foot, UL, buff=0.1)
        self.until(word_time("s027", word_index("s027", "We")))
        self.play(FadeIn(mx), run_time=0.5)

        # ── s028 size is known, price is guessed ──
        self.at("s028", 0.0)
        self.play(fr.animate.restore(), FadeOut(VGroup(mx, dl)), FadeIn(axg.xt), FadeIn(axg.yt), FadeIn(axg.labs), run_time=1.0)
        xlabs = VGroup(*[l for l in axg.labs if l.get_y() < ax.c2p(0, 0)[1] - 0.05])
        ylabs = VGroup(*[l for l in axg.labs if l not in xlabs])
        kn = pill("size: known exactly", INK, 28)
        gu = pill("price: guessed", ORANGE_, 28)
        panel(kn, gu, top=1.6, buff=0.3)
        self.play(xlabs.animate.set_color(INK), FadeIn(kn, shift=LEFT * 0.2), run_time=0.6)
        self.until(word_time("s028", word_index("s028", "Only")))
        self.play(ylabs.animate.set_color(ORANGE_), FadeIn(gu, shift=LEFT * 0.2), run_time=0.6)

        # ── s029 the slanted distance is a different tool ──
        self.at("s029", 0.0)
        n1 = T("slanted distance", 26, MUTED, weight=BOLD)
        n2 = T("a different tool,", 26, INK2)
        n3 = T("for when both numbers", 26, INK2)
        n4 = T("are uncertain", 26, INK2)
        nt = VGroup(n1, n2, n3, n4).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        nb = card(nt.width + 0.6, nt.height + 0.55, color=MUTED); nb.move_to(nt)
        note = VGroup(nb, nt).move_to(RIGHT * PANEL_X + DOWN * 1.35)
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.6)
        self.until(word_time("s029", word_index("s029", "different")) + 0.6)
        self.play(Indicate(n2, color=INK), run_time=0.7)

        # ── s030 every miss; above = positive ──
        self.at("s030", 0.0)
        self.play(FadeOut(VGroup(note, kn, gu, perp, px, ml, gdot)), xlabs.animate.set_color(INK2), ylabs.animate.set_color(INK2), run_time=0.5)
        bars = VGroup(*[miss_bar(ax, x, y, A, B_) for x, y in HOUSES])
        self.remove(bar); self.add(bars); self.bring_to_front(dots)
        self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.15), run_time=1.2)
        R = [y - (A + B_ * x) for x, y in HOUSES]
        tags = VGroup()
        for (x, y), r, b in zip(HOUSES, R, bars):
            t = T(f"{'+' if r > 0 else '−'}{abs(r):.0f}", 24, ORANGE_ if r > 0 else BLUE_, weight=BOLD)
            t.next_to(b, LEFT if r > 0 else RIGHT, buff=0.14)
            tags.add(t)
        unit = T("misses in $ thousand", 24, MUTED)
        panel(unit, top=2.3)
        self.until(word_time("s030", word_index("s030", "above")))
        self.play(FadeIn(unit), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t, r in zip(tags, R) if r > 0], lag_ratio=0.2), run_time=1.0)

        # ── s031 below = negative ──
        self.at("s031", 0.0)
        self.play(*[FadeIn(t, scale=1.4) for t, r in zip(tags, R) if r < 0], run_time=0.6)
        self.play(*[Indicate(b, color=BLUE_, scale_factor=1.1) for b, r in zip(bars, R) if r < 0], run_time=0.7)

        # ── s032 add them up into one score ──
        self.at("s032", 0.0)
        sc = pill("total miss  =  ?", WARN, 34).move_to(RIGHT * PANEL_X + UP * 0.6)
        self.until(word_time("s032", word_index("s032", "So")))
        self.play(FadeIn(sc, shift=LEFT * 0.3), run_time=0.6)
        self.play(sc.animate.scale(1.12), rate_func=there_and_back, run_time=0.8)
        self.finish()
