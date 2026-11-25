import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *

RX = 3.7


class S24Practice(PBase):
    CHAPTER = "Practice Round"

    def countdown(self, sid):
        """Ring that empties during the thinking pause after question segment sid."""
        t0 = self.now()
        nxt = ORDER[ORDER.index(sid) + 1]
        dur = max(1.0, SEGS[nxt]["start"] - t0 - 0.15)
        ring = Arc(radius=0.45, start_angle=PI / 2, angle=-TAU, stroke_color=WARN, stroke_width=8).move_to(RIGHT * 6.0 + UP * 2.85)
        ring.qa_ignore = True
        self.add(ring)
        self.play(Uncreate(ring), run_time=dur, rate_func=linear)

    def q(self, n, text):
        tag = pill(f"Q{n}", WARN, 34).move_to(LEFT * 3.2 + UP * 2.85)
        tag.move_to(UP * 2.85 + LEFT * 2.6)
        qt = T(text, 30, INK).move_to(UP * 2.05)
        if qt.width > 12.4: qt.scale_to_fit_width(12.4)
        return VGroup(tag, qt)

    def construct(self):
        self.at("s388")
        hd = header("practice round", WARN, 36)
        pz = VGroup(Rectangle(width=0.25, height=0.9, fill_color=INK, fill_opacity=1, stroke_width=0),
                    Rectangle(width=0.25, height=0.9, fill_color=INK, fill_opacity=1, stroke_width=0)).arrange(RIGHT, buff=0.25).move_to(UP * 0.3)
        tip = T("pause the video, try it, then check", 32, INK2).next_to(pz, DOWN, buff=0.5)
        self.play(FadeIn(hd), FadeIn(pz, scale=0.6), FadeIn(tip), run_time=0.8)

        # Q1 sweets
        self.at("s389")
        self.clear()
        qq = self.q(1, "4 green + 6 yellow sweets: chance of green?")
        jar = RoundedRectangle(corner_radius=0.3, width=3.0, height=2.6, stroke_color=INK2, stroke_width=4).move_to(LEFT * 3.4 + DOWN * 0.5)
        sw = VGroup(*[marble(c, 0.2) for c in [AQUA] * 4 + [WARN] * 6]).arrange_in_grid(2, 5, buff=0.15).move_to(jar)
        self.play(FadeIn(qq), Create(jar), FadeIn(sw, lag_ratio=0.05), run_time=0.9)
        self.until(SEGS["s389"]["end"]); self.countdown("s389")
        self.at("s390")
        a = MathTex(r"{4 \over 10} = {2 \over 5}", font_size=72, color=VIOLET).move_to(RIGHT * RX + DOWN * 0.5)
        self.play(*[Indicate(m, color=AQUA) for m in sw[:4]], run_time=0.6)
        self.w("s390", "four", nth=1)
        self.play(Write(a), run_time=0.8)

        # Q2–Q3 total of ten
        self.at("s391")
        self.clear()
        qq = self.q(2, "two dice: chance of a total of 10?")
        g = DiceGrid(0.56, fs=24).move_to(LEFT * 3.2 + DOWN * 0.55)
        sums = g.sums()
        self.play(FadeIn(qq), FadeIn(g), FadeIn(sums), run_time=0.8)
        self.until(SEGS["s391"]["end"]); self.countdown("s391")
        self.at("s392")
        self.play(*g.tint(lambda a, b: a + b == 10, AQUA, 0.9), run_time=0.6)
        a = MathTex(r"{3 \over 36} = {1 \over 12}", font_size=66, color=VIOLET).move_to(RIGHT * RX + DOWN * 0.5)
        self.w("s392", "three", nth=0)
        self.play(Write(a), run_time=0.8)
        self.at("s393")
        q3 = self.q(3, "and the chance of NOT a total of 10?")
        self.play(FadeOut(qq), FadeIn(q3), a.animate.scale(0.7).move_to(RIGHT * RX + UP * 0.9), run_time=0.6)
        qq = q3
        self.until(SEGS["s393"]["end"]); self.countdown("s393")
        self.at("s394")
        self.play(*g.tint(lambda a, b: a + b != 10, BLUE_, 0.35), run_time=0.5)
        a3 = MathTex(r"1 - {1 \over 12} = {11 \over 12}", font_size=60, color=VIOLET).move_to(RIGHT * RX + DOWN * 0.8)
        self.play(Write(a3), run_time=0.9)

        # Q4 three coins at least one head
        self.at("s395")
        self.clear()
        qq = self.q(4, "three coins: chance of at least one head?")
        cs = VGroup(*[coin("?", WARN, 0.5) for _ in range(3)]).arrange(RIGHT, buff=0.4).move_to(LEFT * 3.4 + DOWN * 0.3)
        self.play(FadeIn(qq), FadeIn(cs), run_time=0.7)
        self.until(SEGS["s395"]["end"]); self.countdown("s395")
        self.at("s396")
        tt = VGroup(*[coin("T", BLUE_, 0.5) for _ in range(3)]).arrange(RIGHT, buff=0.4).move_to(cs)
        nh = T("opposite: no heads = TTT = 1/8", 30, BLUE_, weight=BOLD).next_to(tt, DOWN, buff=0.45)
        self.w("s396", "tails")
        self.play(Transform(cs, tt), FadeIn(nh), run_time=0.7)
        a = MathTex(r"1 - {1 \over 8} = {7 \over 8}", font_size=66, color=VIOLET).move_to(RIGHT * RX + DOWN * 0.3)
        self.w("s396", "seven")
        self.play(Write(a), run_time=0.8)

        # Q5 both even
        self.at("s397")
        self.clear()
        qq = self.q(5, "two dice: chance both show an even number?")
        g = DiceGrid(0.56, fs=24).move_to(LEFT * 3.2 + DOWN * 0.55)
        self.play(FadeIn(qq), FadeIn(g), run_time=0.7)
        self.until(SEGS["s397"]["end"]); self.countdown("s397")
        self.at("s398")
        a = MathTex(r"{1 \over 2} \times {1 \over 2} = {1 \over 4}", font_size=60, color=VIOLET).move_to(RIGHT * RX + UP * 0.4)
        self.w("s398", "one", nth=1)
        self.play(Write(a), run_time=1.0)
        self.w("s398", "grid")
        self.play(*g.tint(lambda a, b: a % 2 == 0 and b % 2 == 0, AQUA, 0.9), run_time=0.6)
        a2 = MathTex(r"= {9 \over 36}", font_size=60, color=AQUA).next_to(a, DOWN, buff=0.35)
        self.play(Write(a2), run_time=0.6)

        # Q6 total is 4, double?
        self.at("s399")
        self.play(FadeOut(VGroup(qq, a, a2)), *g.reset(), run_time=0.4)
        qq = self.q(6, "the total is 4: chance it was a double?")
        sums = g.sums(fs=22)
        self.play(FadeIn(qq), FadeIn(sums), run_time=0.6)
        self.until(SEGS["s399"]["end"]); self.countdown("s399")
        self.at("s400")
        dim = VGroup(*[g.cells[k] for k in g.cells if sum(k) != 4], *[t for t in sums if sum(t.ob) != 4])
        self.w("s400", "shrink")
        self.play(dim.animate.set_opacity(0.12), run_time=0.7)
        self.qa_mute(dim)
        self.play(*g.tint(lambda a, b: a + b == 4, WARN, 0.5), run_time=0.4)
        self.w("s400", "only")
        self.play(g.c(2, 2).animate.set_fill(AQUA, 0.95), run_time=0.4)
        a = MathTex(r"{1 \over 3}", font_size=80, color=VIOLET).move_to(RIGHT * RX + DOWN * 0.3)
        self.w("s400", "third")
        self.play(Write(a), run_time=0.6)

        # Q7 spinner expected value
        self.at("s401")
        self.clear()
        qq = self.q(7, "spinner with 1, 2, 3 and 6 points: expected points per spin?")
        sp = spinner([(0.25, ORANGE_), (0.25, BLUE_), (0.25, AQUA), (0.25, VIOLET)], r=1.5).move_to(LEFT * 3.4 + DOWN * 0.4)
        nums = VGroup(*[TB(str(v), 44, BG).move_to(sp[0].get_arc_center() + 0.8 * np.array([np.cos(a_), np.sin(a_), 0]))
                        for v, a_ in zip((1, 2, 3, 6), (PI / 4, -PI / 4, -3 * PI / 4, 3 * PI / 4))])
        self.play(FadeIn(qq), FadeIn(sp), FadeIn(nums), run_time=0.7)
        self.until(SEGS["s401"]["end"]); self.countdown("s401")
        self.at("s402")
        a = MathTex(r"{1 + 2 + 3 + 6 \over 4} = {12 \over 4} = 3", font_size=60, color=VIOLET).move_to(RIGHT * 3.2 + DOWN * 0.4)
        self.play(Write(a), run_time=1.2)

        # Q8 red or queen
        self.at("s398a")
        self.clear()
        qq = self.q(8, "one card: chance it's red OR a queen?")
        dg = deck_grid(0.5).move_to(DOWN * 0.15)
        self.play(FadeIn(qq), FadeIn(dg), run_time=0.7)
        self.until(SEGS["s398a"]["end"]); self.countdown("s398a")
        self.at("s398b")
        self.w("s398b", "red")
        self.play(dg.where(lambda r, s: s < 2).animate.set_fill(RED_, 0.6), run_time=0.5)
        self.w("s398b", "queens")
        self.play(dg.where(lambda r, s: r == 11 and s >= 2).animate.set_fill(BLUE_, 0.6), run_time=0.5)
        self.w("s398b", "two", nth=0)
        self.play(*[dg.cells[(11, s)].animate.set_fill(WARN, 0.95) for s in (0, 1)], run_time=0.5)
        a = MathTex(r"26 + 4 - 2 = 28 \;\rightarrow\; {28 \over 52} = {7 \over 13}", font_size=50, color=VIOLET).move_to(DOWN * 2.05)
        self.w("s398b", "twenty", nth=1)
        self.play(Write(a), run_time=1.3)

        # Q9 at least one six in three rolls
        self.at("s398c")
        self.clear()
        qq = self.q(9, "three rolls: chance of at least one 6?")
        sl = VGroup(*[die_q(ORANGE_, 1.0) for _ in range(3)]).arrange(RIGHT, buff=0.5).move_to(LEFT * 3.4 + DOWN * 0.3)
        self.play(FadeIn(qq), FadeIn(sl), run_time=0.6)
        self.until(SEGS["s398c"]["end"]); self.countdown("s398c")
        self.at("s398d")
        e1 = MathTex(r"\left({5 \over 6}\right)^3 = {125 \over 216}", font_size=54, color=BLUE_).move_to(RIGHT * 3.2 + UP * 0.5)
        e2 = MathTex(r"1 - {125 \over 216} = {91 \over 216} \approx 42\%", font_size=54, color=VIOLET).next_to(e1, DOWN, buff=0.4)
        if e2.width > 7.0: e2.scale_to_fit_width(7.0)
        e2.set_x(3.2)
        self.play(Write(e1), run_time=1.0)
        self.w("s398d", "ninety")
        self.play(Write(e2), run_time=1.2)

        # Q10 spinner twice
        self.at("s398e")
        self.clear()
        qq = self.q(10, "a spinner is 3/4 red. Two spins: both red?")
        sp = spinner([(0.75, RED_), (0.25, BLUE_)], r=1.4).move_to(LEFT * 3.4 + DOWN * 0.4)
        self.play(FadeIn(qq), FadeIn(sp), run_time=0.6)
        self.until(SEGS["s398e"]["end"]); self.countdown("s398e")
        self.at("s398f")
        a = MathTex(r"{3 \over 4} \times {3 \over 4} = {9 \over 16} \approx 56\%", font_size=60, color=VIOLET).move_to(RIGHT * 3.0 + DOWN * 0.4)
        self.w("s398f", "three")
        self.play(Write(a), run_time=1.2)

        # s403 score card
        self.at("s403")
        self.clear()
        sc = VGroup(TB("10 questions", 48, WARN), VGroup(*[check(AQUA, 0.3) for _ in range(10)]).arrange(RIGHT, buff=0.25)).arrange(DOWN, buff=0.5)
        scb = boxed(sc, WARN, pad=0.5).move_to(UP * 0.3)
        self.play(FadeIn(scb[0]), FadeIn(sc[0]), run_time=0.5)
        self.play(LaggedStart(*[Create(c) for c in sc[1]], lag_ratio=0.12), run_time=1.4)
        self.finish()
