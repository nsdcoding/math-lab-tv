import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cm import *


class S14Loans(Base):
    CHAPTER = "Your Turn: Loan Defaults"

    def construct(self):
        # ── s175 your turn ──
        self.at("s175", 0.0)
        pz = VGroup(VGroup(Rectangle(width=0.18, height=0.7), Rectangle(width=0.18, height=0.7)).arrange(RIGHT, buff=0.2)
                    .set_stroke(width=0).set_fill(WARN, 1), T("your turn", 40, WARN, weight=BOLD)).arrange(RIGHT, buff=0.4)
        pz.move_to(UP * 0.4)
        self.play(FadeIn(pz), run_time=0.5)
        # ── s176 2,000 loans, 200 default ──
        self.at("s176", 0.0)
        g = grid_at(rows=("will default", "will repay"), cols=("flagged risky", "not flagged"), col_title="what the model said")
        self.play(FadeOut(pz), run_time=0.3)
        self.play(FadeIn(VGroup(g.cells, g.names, g.collab, g.coltitle, g.rowlab, g.rowtitle)), run_time=0.6)
        t0 = pill("200", ORANGE_, 26).next_to(g.row0(), RIGHT, buff=0.22)
        t1 = pill("1,800", INK2, 26).next_to(g.row1(), RIGHT, buff=0.22)
        hd = T("2,000 loans", 28, INK2, weight=BOLD).move_to(RIGHT * (PANEL_X + 0.4) + UP * 1.6)
        self.play(FadeIn(hd), run_time=0.3)
        self.word("s176", "default,")
        self.play(FadeIn(t0), FadeIn(t1), run_time=0.5)
        # ── s177 250 flagged: 150 default, 100 fine ──
        self.at("s177", 0.0)
        fl = T("flagged: 250", 28, VIOLET, weight=BOLD).next_to(hd, DOWN, buff=0.3)
        self.word("s177", "flags")
        self.play(FadeIn(fl), run_time=0.4)
        self.word("s177", "One")
        self.play(g.set_num("TP", 150), g.light("TP"), run_time=0.5)
        self.word("s177", "One", nth=1)
        self.play(g.set_num("FP", 100), g.light("FP"), run_time=0.5)
        # ── s178 try it ──
        self.at("s178", 0.0)
        self.play(g.set_num("FN", "?", MUTED), g.set_num("TN", "?", MUTED), run_time=0.5)
        tk = VGroup(T("fill the ? boxes", 26, WARN, weight=BOLD), T("precision = ?", 26, VIOLET, weight=BOLD),
                    T("recall = ?", 26, ORANGE_, weight=BOLD)).arrange(DOWN, buff=0.18).next_to(fl, DOWN, buff=0.45)
        self.play(FadeIn(tk), run_time=0.5)
        timer = Arc(radius=0.4, start_angle=PI / 2, angle=-TAU).set_stroke(WARN, 6).next_to(tk, DOWN, buff=0.35)
        timer.qa_ignore = True
        self.play(Create(timer), run_time=SEGS["s179"]["start"] - self.now() - 0.3, rate_func=linear)
        # ── s179 / s180 the answers ──
        self.at("s179", 0.0)
        self.play(FadeOut(VGroup(tk, timer)), run_time=0.3)
        e1 = panel_eq([("200", ORANGE_), ("−", INK2), ("150", AQUA), ("=", INK2), ("50", BLUE_)], -0.1, dx=0.2, size=28)
        self.word("s179", "minus")
        self.play(FadeIn(e1), run_time=0.5)
        self.word("s179", "fifty", nth=1)
        self.play(g.set_num("FN", 50), g.light("FN"), run_time=0.5)
        self.at("s180", 0.0)
        e2 = panel_eq([("1,800", INK2), ("−", INK2), ("100", ORANGE_), ("=", INK2), ("1,700", AQUA)], -0.9, dx=0.2, size=28)
        self.word("s180", "minus")
        self.play(FadeIn(e2), run_time=0.5)
        self.word("s180", "seven")
        self.play(g.set_num("TN", 1700), g.light("TN"), run_time=0.5)
        # ── s181 – s184 the scores ──
        self.at("s181", 0.0)
        self.play(FadeOut(VGroup(e1, e2, hd, fl, t0, t1)), run_time=0.3)
        fc = g.frame_of(g.col0(), VIOLET)
        rows = [T("precision  150/250 = 60%", 24, VIOLET, weight=BOLD), T("recall  150/200 = 75%", 24, ORANGE_, weight=BOLD),
                T("accuracy  =  92.5%", 24, WARN, weight=BOLD), T("lazy model: 90%", 22, MUTED),
                T("F1  300/450 = 2/3 ≈ 67%", 24, VIOLET, weight=BOLD)]
        VGroup(*rows).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(RIGHT * (PANEL_X + 0.15) + UP * 0.6)
        self.play(Create(fc), FadeIn(rows[0]), run_time=0.6)
        self.at("s182", 0.0)
        fr = g.frame_of(g.row0(), ORANGE_, pad=0.17)
        self.play(FadeOut(fc), Create(fr), FadeIn(rows[1]), run_time=0.6)
        self.at("s183", 0.0)
        self.play(FadeOut(fr), FadeIn(rows[2]), run_time=0.5)
        self.word("s183", "Ninety-two")
        self.play(FadeIn(rows[3]), run_time=0.4)
        self.at("s184", 0.0)
        self.word("s184", "three")
        self.play(FadeIn(rows[4]), run_time=0.5)
        # ── s185 in plain words ──
        self.at("s185", 0.0)
        self.play(FadeOut(VGroup(*rows)), run_time=0.4)
        w1 = side_card(["When it says risky,", "it's right 6 times in 10."], VIOLET, 24).move_to(RIGHT * (PANEL_X + 0.4) + UP * 0.9)
        w2 = side_card(["It spots 3 of every 4", "loans that go bad."], ORANGE_, 24).next_to(w1, DOWN, buff=0.3)
        self.word("s185", "risky,")
        self.play(FadeIn(w1), run_time=0.5)
        self.word("s185", "spots")
        self.play(FadeIn(w2), run_time=0.5)
        # ── s186 you can read any confusion matrix ──
        self.at("s186", 0.0)
        ok = VGroup(check(AQUA, 0.4), T("you can read any confusion matrix", 26, AQUA, weight=BOLD)).arrange(RIGHT, buff=0.25)
        ok.move_to(DOWN * 2.35 + LEFT * 0.4)
        self.play(FadeIn(ok), run_time=0.5)
        self.until(SEGS["s186"]["end"] + 0.1)
        self.play(FadeOut(VGroup(w1, w2, ok, grid_mobs(g))), run_time=0.5)
        self.finish()
