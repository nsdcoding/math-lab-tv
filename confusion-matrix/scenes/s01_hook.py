import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cm import *

rng = np.random.default_rng(11)
FRAUD_CELLS = set()
while len(FRAUD_CELLS) < 100:
    FRAUD_CELLS.add((int(rng.integers(0, 100)), int(rng.integers(0, 100))))


class S01Hook(Base):
    CHAPTER = "Two Fraud Detectors"

    def construct(self):
        # ── s001 the card team ──
        self.at("s001", 0.0)
        img = sticker("assets/analyst.png", 4.2).move_to(LEFT * 3.4 + DOWN * 0.1)
        il = T("illustration", 20, MUTED).next_to(img, DOWN, buff=0.2)
        self.play(FadeIn(img, shift=UP * 0.2), FadeIn(il), run_time=0.9, rate_func=rate_functions.ease_out_cubic)

        # ── s002 10,000 payments, 1 in 100 fraud ──
        self.at("s002", 0.0)
        cell = 0.036
        field = field_squares(100, 100, cell, skip=FRAUD_CELLS, opacity=0.55)
        fraud = field_squares(100, 100, cell, color=RED_, opacity=1.0,
                              skip={(c, r) for c in range(100) for r in range(100)} - FRAUD_CELLS)
        F = VGroup(field, fraud).move_to(RIGHT * 3.4 + UP * 0.75)
        frame = SurroundingRectangle(F, buff=0.12, corner_radius=0.08).set_stroke(GRID, 2)
        frame.qa_ignore = True
        cnt = T("10,000 payments a day", 30, INK, weight=BOLD).next_to(frame, DOWN, buff=0.25)
        self.play(FadeIn(field), Create(frame), run_time=1.2)
        self.play(FadeIn(cnt, shift=UP * 0.15), run_time=0.5)
        self.word("s002", "fraud")
        fl = T("100 of them fraud", 30, RED_, weight=BOLD).next_to(cnt, DOWN, buff=0.15)
        self.play(FadeIn(fraud), FadeIn(fl, shift=UP * 0.15), run_time=0.8)

        # ── s003 two detectors ──
        self.at("s003", 0.0)
        self.play(FadeOut(Group(img, il, field, fraud, frame, cnt, fl)), run_time=0.5)
        A = detector_box("Detector A", AQUA).move_to(LEFT * 3.6 + UP * 1.4)
        B = detector_box("Detector B", VIOLET).move_to(RIGHT * 3.6 + UP * 1.4)
        self.play(FadeIn(A, shift=RIGHT * 0.4), FadeIn(B, shift=LEFT * 0.4), run_time=0.8,
                  rate_func=rate_functions.ease_out_cubic)

        # ── s004 / s005 the two claims ──
        self.at("s004", 0.0)
        ca = pill("“we catch 90% of fraud”", AQUA, 30).next_to(A, DOWN, buff=0.4)
        self.word("s004", "catches")
        self.play(FadeIn(ca, shift=DOWN * 0.2), run_time=0.6)
        self.at("s005", 0.0)
        cb = pill("“90% of our alarms are real”", VIOLET, 30).next_to(B, DOWN, buff=0.4)
        self.word("s005", "ninety")
        self.play(FadeIn(cb, shift=DOWN * 0.2), run_time=0.6)

        # ── s006 both: 99%+ accurate ──
        self.at("s006", 0.0)
        ga = pill("99%+ accurate", WARN, 28).next_to(ca, DOWN, buff=0.3)
        gb = pill("99%+ accurate", WARN, 28).next_to(cb, DOWN, buff=0.3)
        self.word("s006", "ninety-nine")
        self.play(FadeIn(ga, shift=DOWN * 0.15), FadeIn(gb, shift=DOWN * 0.15), run_time=0.6)

        # ── s007 ninety, ninety, ninety-nine ──
        self.at("s007", 0.0)
        self.word("s007", "Ninety,")
        self.play(highlight(ca, color=AQUA), run_time=0.7)
        self.word("s007", "ninety,", nth=1)
        self.play(highlight(cb, color=VIOLET), run_time=0.7)
        self.word("s007", "ninety-nine")
        self.play(highlight(ga, gb), run_time=0.8)

        # ── s008 one of them lets more than half slip past ──
        self.at("s008", 0.0)
        self.word("s008", "different")
        self.play(VGroup(A, ca, ga).animate.set_opacity(0.3), run_time=0.5)
        gate_y = DOWN * 2.05
        gate = Line(RIGHT * 1.2 + gate_y + UP * 0.35, RIGHT * 1.2 + gate_y + DOWN * 0.35).set_stroke(VIOLET, 5)
        gate.qa_ignore = True
        self.word("s008", "half")
        reds = squares(55, 11, 0.16, RED_).move_to(LEFT * 2.0 + gate_y)
        self.qa_mute(reds)
        self.play(Create(gate), FadeIn(reds), run_time=0.5)
        self.play(reds.animate.shift(RIGHT * 6.0), run_time=1.6, rate_func=rate_functions.ease_in_out_sine)
        miss = pill("misses 55 of 100 frauds", RED_, 28).move_to(LEFT * 3.0 + DOWN * 2.05)
        self.qa_mute(reds, False)
        self.play(FadeIn(miss), run_time=0.5)

        # ── s009 a detector that does nothing: 99% too ──
        self.at("s009", 0.0)
        self.play(FadeOut(VGroup(reds, gate, miss, ca, cb)), VGroup(A, ga).animate.set_opacity(1), run_time=0.5)
        self.play(A.animate.scale(0.85).move_to(LEFT * 4.6 + UP * 1.4), B.animate.scale(0.85).move_to(UP * 1.4),
                  ga.animate.move_to(LEFT * 4.6 + UP * 0.2), gb.animate.move_to(UP * 0.2), run_time=0.7)
        Z = detector_box("Detector Zero", MUTED, w=3.8).scale(0.85).move_to(RIGHT * 4.6 + UP * 1.4)
        self.word("s009", "nothing")
        self.play(FadeIn(Z, shift=LEFT * 0.3), run_time=0.6)
        za = pill("never raises an alarm", MUTED, 26).move_to(RIGHT * 4.6 + DOWN * 1.0)
        self.word("s009", "never")
        self.play(FadeIn(za, shift=DOWN * 0.15), run_time=0.5)
        zg = pill("99% accurate", WARN, 28).move_to(RIGHT * 4.6 + UP * 0.2)
        self.word("s009", "ninety-nine")
        self.play(FadeIn(zg, shift=DOWN * 0.15), run_time=0.5)

        # ── s010 the promise from the prosecutor's fallacy ──
        self.at("s010", 0.0)
        pr = pill("from: The Prosecutor's Fallacy", INK2, 26).move_to(LEFT * 2.3 + DOWN * 1.0)
        self.play(FadeIn(pr, shift=UP * 0.2), run_time=0.6)
        self.word("s010", "solve")
        self.play(highlight(pr, color=INK2), run_time=0.8)

        # ── s011 one small table ──
        self.at("s011", 0.0)
        g = grid_at(0.9, center=np.array([0.0, -0.05, 0]), names=False, rows=("", ""), cols=("", ""),
                    row_title="", col_title="")
        self.play(FadeOut(VGroup(A, ga, B, gb, Z, za, zg, pr)), run_time=0.6)
        self.word("s011", "table")
        self.play(LaggedStart(*[Create(g.cell[k]) for k in KEYS], lag_ratio=0.2), run_time=1.2)
        tw = T("2 × 2", 40, INK2, weight=BOLD).next_to(g.cells, UP, buff=0.35)
        self.word("s011", "two")
        self.play(FadeIn(tw), run_time=0.5)
        yn = T("for any yes-or-no prediction", 30, INK2).next_to(g.cells, DOWN, buff=0.35)
        self.word("s011", "yes")
        self.play(FadeIn(yn, shift=UP * 0.15), run_time=0.5)

        # ── s012 title card ──
        self.at("s012", 0.0)
        title = the_title()
        self.play(FadeOut(VGroup(g.cells, tw, yn)), run_time=0.5)
        self.word("s012", "confusion")
        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.8, rate_func=rate_functions.ease_out_cubic)
        self.finish()
