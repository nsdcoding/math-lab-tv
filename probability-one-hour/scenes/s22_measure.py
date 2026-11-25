import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *


class S22Measure(PBase):
    CHAPTER = "Measuring Instead of Counting"

    def construct(self):
        self.at("s370")
        d = die(5, ORANGE_, 1.4).move_to(LEFT * 3.0 + UP * 0.3)
        sw = ic_clock(INK2, 1.6).move_to(RIGHT * 3.0 + UP * 0.3)
        l1 = T("countable", 30, AQUA, weight=BOLD).next_to(d, DOWN, buff=0.4)
        l2 = T("too many to list", 30, WARN, weight=BOLD).next_to(sw, DOWN, buff=0.4).set_y(l1.get_y())
        self.play(FadeIn(d), FadeIn(l1), run_time=0.6)
        self.w("s370", "some")
        self.play(FadeIn(sw), FadeIn(l2), run_time=0.6)
        # s371 bus every 10 minutes
        self.at("s371")
        self.clear()
        nl = NumberLine(x_range=[0, 10, 1], length=11, color=INK2, stroke_width=4, include_tip=False, tick_size=0.1).move_to(DOWN * 0.2)
        nums = VGroup(*[T(str(k), 26, INK2).next_to(nl.n2p(k), DOWN, buff=0.18) for k in range(11)])
        tt = T("minutes", 26, MUTED).next_to(nums, DOWN, buff=0.12)
        b1 = ic_bus(WARN, 0.9).next_to(nl.n2p(0), UP, buff=0.3); b2 = ic_bus(WARN, 0.9).next_to(nl.n2p(10), UP, buff=0.3)
        self.play(Create(nl), FadeIn(nums), FadeIn(tt), run_time=0.7)
        self.w("s371", "ten")
        self.play(FadeIn(b1), FadeIn(b2), run_time=0.5)
        self.at("s372")
        hd = header("wait less than 3 minutes?", INK, 32)
        self.play(FadeIn(hd), run_time=0.5)
        # s373 endless arrival points
        self.at("s373")
        rng = np.random.default_rng(4)
        pts = VGroup(*[Dot(nl.n2p(x) + UP * 0.25, radius=0.04, color=INK2) for x in rng.uniform(0.05, 9.95, 140)])
        self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.01), run_time=2.0)
        es = T("any split second: endless possibilities", 28, INK2).move_to(UP * 1.9)
        self.play(FadeIn(es), run_time=0.5)
        # s374 measure 7..10
        self.at("s374")
        self.play(FadeOut(VGroup(pts, es)), run_time=0.4)
        good = Line(nl.n2p(7), nl.n2p(10), color=AQUA, stroke_width=14)
        good.qa_ignore = True
        br1 = BraceBetweenPoints(nl.n2p(7) + UP * 0.4, nl.n2p(10) + UP * 0.4, UP, color=AQUA)
        g3 = T("3 minutes", 28, AQUA, weight=BOLD).next_to(br1, UP, buff=0.1)
        self.w("s374", "last")
        self.play(Create(good), run_time=0.6)
        self.play(GrowFromCenter(br1), FadeIn(g3), FadeOut(b2), run_time=0.6)
        al = T("whole wait: 10 minutes", 28, WARN, weight=BOLD).move_to(UP * 1.85 + LEFT * 2.5)
        self.w("s374", "out")
        self.play(FadeIn(al), run_time=0.4)
        # s375
        self.at("s375")
        a = MathTex(r"{3 \over 10}", font_size=72, color=VIOLET).move_to(DOWN * 2.0 + RIGHT * 4.5)
        a.move_to(UP * 1.85 + RIGHT * 2.0)
        self.play(Write(a), run_time=0.7)
        # s376 rule
        self.at("s376")
        self.clear()
        rc = MathTex(r"P", "=", r"{\text{length you want}", r"\over", r"\text{total length}}", font_size=64)
        rc[0].set_color(VIOLET); rc[2].set_color(AQUA); rc[4].set_color(WARN)
        rcb = boxed(rc, VIOLET, pad=0.4).move_to(UP * 0.3)
        self.play(FadeIn(rcb[0]), Write(rc), run_time=1.3)
        # s377–s378 dart board
        self.at("s377")
        self.clear()
        S = 3.8
        board = Square(S, stroke_color=INK2, stroke_width=4).move_to(LEFT * 2.8 + DOWN * 0.1)
        r = S * np.sqrt(0.5 / PI)
        circ = Circle(r, stroke_color=AQUA, stroke_width=4, fill_color=AQUA, fill_opacity=0.3).move_to(board)
        circ.qa_ignore = True
        il = T("illustration", 22, MUTED).next_to(board, UP, buff=0.15)
        self.play(Create(board), FadeIn(il), run_time=0.6)
        self.w("s377", "circle")
        self.play(DrawBorderThenFill(circ), run_time=0.8)
        hf = T("circle = half the area", 30, AQUA, weight=BOLD).move_to(RIGHT * 3.5 + UP * 1.0)
        self.w("s377", "half")
        self.play(FadeIn(hf), run_time=0.4)
        self.at("s378")
        rng = np.random.default_rng(8)
        c0 = board.get_center()
        darts = VGroup()
        for _ in range(60):
            p = c0 + np.array([rng.uniform(-S / 2 + 0.08, S / 2 - 0.08), rng.uniform(-S / 2 + 0.08, S / 2 - 0.08), 0])
            inside = np.linalg.norm(p - c0) < r
            darts.add(Dot(p, radius=0.05, color=VIOLET if inside else INK2))
        self.play(LaggedStart(*[FadeIn(dt, scale=2) for dt in darts], lag_ratio=0.03), run_time=1.6)
        e = MathTex(r"{\text{area you want} \over \text{total area}} = {1 \over 2}", font_size=48, color=VIOLET).next_to(hf, DOWN, buff=0.5)
        self.play(Write(e), run_time=1.0)
        # s379 same idea
        self.at("s379")
        self.clear()
        ic = VGroup(VGroup(die(3, ORANGE_, 0.9), T("counting", 28, INK2)).arrange(DOWN, buff=0.25),
                    VGroup(Line(LEFT * 0.8, RIGHT * 0.8, color=AQUA, stroke_width=10), T("lengths", 28, INK2)).arrange(DOWN, buff=0.45),
                    VGroup(Square(0.9, stroke_color=AQUA, stroke_width=4, fill_color=AQUA, fill_opacity=0.3), T("areas", 28, INK2)).arrange(DOWN, buff=0.25))
        ic.arrange(RIGHT, buff=1.4).move_to(UP * 0.9)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.2) for x in ic], lag_ratio=0.25), run_time=1.0)
        one = pill("the part you want, out of the whole", VIOLET, 36).move_to(DOWN * 1.2)
        self.w("s379", "part")
        self.play(FadeIn(one, scale=0.9), run_time=0.6)
        self.finish()
