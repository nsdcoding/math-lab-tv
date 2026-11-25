import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *

TITLE = ("PROBABILITY", "from absolute zero, in one hour")


def board():
    b = RoundedRectangle(corner_radius=0.3, width=7.4, height=3.6, stroke_color=INK2, stroke_width=3,
                         fill_color=PANEL, fill_opacity=1)
    b.qa_container = True
    path = VGroup()
    pts = [(-3.0, -1.2), (-2.2, -1.2), (-1.4, -1.2), (-0.6, -1.2), (0.2, -1.2), (1.0, -1.2), (1.8, -1.2), (2.6, -1.2),
           (2.6, -0.4), (2.6, 0.4), (1.8, 0.4), (1.0, 0.4), (0.2, 0.4), (-0.6, 0.4), (-1.4, 0.4), (-1.4, 1.2), (-0.6, 1.2), (0.2, 1.2)]
    for x, y in pts:
        path.add(Square(0.62, stroke_color=MUTED, stroke_width=2, fill_opacity=0).move_to([x, y, 0]))
    fin = path[-1].copy().set_stroke(WARN, 4)
    flag = VGroup(Line(ORIGIN, UP * 0.45), Polygon(UP * 0.45, UP * 0.3 + RIGHT * 0.3, UP * 0.15)).set_stroke(WARN, 3)
    flag.move_to(fin)
    return VGroup(b, path, fin, flag), path


class S01Hook(PBase):
    CHAPTER = "Game Night"
    FADE_OUT = False  # the title card carries into the welcome scene

    def construct(self):
        # s001 game night
        self.at("s001")
        bd, path = board()
        bd.move_to(UP * 0.3)
        you = Circle(0.2, fill_color=ORANGE_, fill_opacity=1, stroke_width=0).move_to(path[-3])
        fri = Circle(0.2, fill_color=BLUE_, fill_opacity=1, stroke_width=0).move_to(path[-2])
        d1, d2 = die(3, ORANGE_, 0.7), die(5, BLUE_, 0.7)
        dice = VGroup(d1, d2).arrange(RIGHT, buff=0.3).move_to(bd[0].get_center() + DOWN * 0.4 + RIGHT * 0.2)
        self.play(FadeIn(bd[0]), Create(bd[1], lag_ratio=0.05), run_time=1.2)
        self.play(FadeIn(bd[2]), Create(bd[3]), FadeIn(you, scale=0.5), FadeIn(fri, scale=0.5), run_time=0.8)
        self.play(FadeIn(dice, shift=UP * 0.3), run_time=0.6)
        self.play(Rotate(d1, PI / 2), Rotate(d2, -PI / 2), run_time=0.6)
        game = VGroup(bd, you, fri, dice)
        # s002 you need 12
        self.at("s002")
        self.play(game.animate.scale(0.78).move_to(UP * 0.95), run_time=0.7)
        c_you = pill("you need: 12", ORANGE_, 36).move_to(LEFT * 4.6 + DOWN * 1.9)
        g66 = VGroup(die(6, ORANGE_, 0.6), die(6, BLUE_, 0.6)).arrange(RIGHT, buff=0.2).next_to(c_you, UP, buff=0.3)
        g66.set_opacity(0.45)
        self.play(Indicate(you, color=ORANGE_, scale_factor=1.6), FadeIn(c_you, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(g66), run_time=0.5)
        # s003 friend needs 7
        self.at("s003")
        c_fr = pill("friend needs: 7", BLUE_, 36).move_to(RIGHT * 4.6 + DOWN * 1.9)
        self.play(Indicate(fri, color=BLUE_, scale_factor=1.6), FadeIn(c_fr, shift=UP * 0.2), run_time=0.8)
        # s004 who is more likely
        self.at("s004")
        q = TB("?", 110, WARN).move_to(DOWN * 1.75)
        self.w("s004", "who")
        self.play(FadeIn(q, scale=0.4), run_time=0.5)
        self.play(Wiggle(q), run_time=0.8)
        # s005 the same?
        self.at("s005")
        self.play(FadeOut(VGroup(game, g66, q)), c_you.animate.move_to(LEFT * 4.85 + UP * 2.85),
                  c_fr.animate.move_to(RIGHT * 4.85 + UP * 2.85), run_time=0.7)
        self.drop(game, g66, q)
        sc, th, L, R = beam_scale(6.0)
        sc.move_to(UP * 0.6)
        lab7 = TB("7", 64, BLUE_); lab12 = TB("12", 64, ORANGE_)
        lab7.add_updater(lambda m: m.next_to(L[0], DOWN, buff=0.15))
        lab12.add_updater(lambda m: m.next_to(R[0], DOWN, buff=0.15))
        self.play(FadeIn(sc), run_time=0.6)
        self.w("s005", "twelve")
        self.play(FadeIn(lab12, shift=DOWN * 0.3), run_time=0.4)
        self.w("s005", "seven")
        self.play(FadeIn(lab7, shift=DOWN * 0.3), run_time=0.4)
        gut = T("gut feeling: same chance?", 30, MUTED).move_to(UP * 2.85)
        self.w("s005", "every")
        self.play(FadeIn(gut), run_time=0.5)
        # s006 wrong
        self.at("s006")
        self.play(th.animate.set_value(0.32), run_time=0.5, rate_func=rate_functions.ease_in_quad)
        self.play(th.animate.set_value(0.27), run_time=0.25)
        tag = pill("6 times more likely", VIOLET, 36)
        tag.move_to(UP * 2.85)
        self.w("s006", "six")
        self.play(FadeIn(tag, shift=DOWN * 0.3), FadeOut(gut), run_time=0.6)
        # s007 stacks
        self.at("s007")
        for m in (lab7, lab12):
            m.clear_updaters()
        self.play(FadeOut(VGroup(sc, lab7, lab12)), run_time=0.5)
        self.drop(sc, lab7, lab12, L, R)
        ax = bar_axes(["7", "12"], 6, 1, 5.0, 3.9, "total needed", "ways to roll it")
        ax.move_to(UP * 0.05)
        self.play(FadeIn(ax), run_time=0.5)
        st7 = VGroup(*[Square(0.58, stroke_width=0, fill_color=BLUE_, fill_opacity=0.9) for _ in range(6)])
        for k, s in enumerate(st7):
            s.move_to(ax.ax.c2p(1, k + 0.5))
        s12 = Square(0.58, stroke_width=0, fill_color=ORANGE_, fill_opacity=0.9).move_to(ax.ax.c2p(2, 0.5))
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.3) for s in st7], lag_ratio=0.25), FadeIn(s12, shift=DOWN * 0.3), run_time=1.6)
        # s007a 100 races
        self.at("s007a")
        self.play(FadeOut(VGroup(ax, st7, s12)), run_time=0.4)
        self.drop(ax, st7, s12)
        ax2 = bar_axes(["friend wins", "you win"], 20, 5, 6.0, 3.9, "out of 100 races (expected)", "races won")
        ax2.yt.shift(LEFT * 0.2)
        ax2.move_to(UP * 0.05)
        b1 = bar(ax2.ax, 1, 100 / 6, BLUE_, width=1.1); b2 = bar(ax2.ax, 2, 100 / 36, ORANGE_, width=1.1)
        self.play(FadeIn(ax2), run_time=0.4)
        self.w("s007a", "seventeen")
        n1 = TB("≈ 17", 36, BLUE_).next_to(b1, UP, buff=0.15)
        self.play(GrowFromEdge(b1, DOWN), FadeIn(n1), run_time=0.7)
        self.w("s007a", "three")
        n2 = TB("≈ 3", 36, ORANGE_).next_to(b2, UP, buff=0.15)
        self.play(GrowFromEdge(b2, DOWN), FadeIn(n2), run_time=0.6)
        # s008 hidden pattern
        self.at("s008")
        self.clear()
        g = DiceGrid(0.68, titles=False).move_to(UP * 0.05)
        self.play(FadeIn(g.ax), LaggedStart(*[FadeIn(s, scale=0.6) for s in g.sq], lag_ratio=0.02), FadeIn(g.xl), FadeIn(g.yl), run_time=1.6)
        self.w("s008", "hidden")
        for s_ in range(2, 13):
            pass
        diag = [g.where(lambda o, b, s_=s_: o + b == s_) for s_ in range(2, 13)]
        for d in diag:
            self.play(d.animate.set_fill(AQUA, 0.85), run_time=0.14)
            self.play(d.animate.set_fill(CELL_FILL, 1), run_time=0.1)
        self.play(diag[5].animate.set_fill(AQUA, 0.85), run_time=0.4)
        # s009 one hour
        self.at("s009")
        self.play(FadeOut(g), run_time=0.4); self.drop(g)
        clock = Circle(1.6, stroke_color=INK2, stroke_width=5).move_to(UP * 0.2)
        sweep = ValueTracker(0)
        wedge = always_redraw(lambda: Sector(radius=1.52, start_angle=PI / 2, angle=-TAU * sweep.get_value() + 1e-4,
                                             fill_color=VIOLET, fill_opacity=0.55, stroke_width=0).move_arc_center_to(clock.get_center()))
        hand = always_redraw(lambda: Line(clock.get_center(), clock.get_center() + 1.42 * np.array(
            [np.cos(PI / 2 - TAU * sweep.get_value()), np.sin(PI / 2 - TAU * sweep.get_value()), 0]), color=INK, stroke_width=5))
        ticks = VGroup(*[Line(clock.get_center() + 1.6 * np.array([np.cos(a), np.sin(a), 0]) * 0.88,
                              clock.get_center() + 1.6 * np.array([np.cos(a), np.sin(a), 0]), color=INK2, stroke_width=3)
                         for a in np.linspace(0, TAU, 13)[:-1]])
        lbl = T("60 minutes", 34, VIOLET, weight=BOLD).next_to(clock, DOWN, buff=0.4)
        self.play(Create(clock), FadeIn(ticks), run_time=0.6)
        self.add(wedge, hand)
        self.w("s009", "one")
        self.play(sweep.animate.set_value(1.0), FadeIn(lbl), run_time=3.0, rate_func=linear)
        # s010 three chips
        self.at("s010")
        self.play(FadeOut(VGroup(clock, ticks, lbl)), FadeOut(wedge), FadeOut(hand), run_time=0.4)
        self.drop(clock, ticks, lbl, wedge, hand)
        chips = [pill("no scary formulas", INK, 34), pill("no skipped steps", INK, 34), pill("just counting", AQUA, 34)]
        VGroup(*chips).arrange(DOWN, buff=0.45).move_to(UP * 0.2)
        for ch, w in zip(chips, ["No", "No", "Just"]):
            self.w("s010", w, nth=0 if ch is chips[0] else (1 if ch is chips[1] else 0))
            self.play(FadeIn(ch, shift=RIGHT * 0.3), run_time=0.45)
        # s011 title
        self.at("s011")
        tc = title_card(*TITLE)
        self.play(FadeOut(VGroup(*chips), c_you, c_fr, tag), run_time=0.3)
        self.play(FadeIn(tc, scale=0.9), run_time=0.7)
        self.finish()
