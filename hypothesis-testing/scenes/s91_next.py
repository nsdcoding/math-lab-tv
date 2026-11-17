import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

NEXT_TOPIC = "the prosecutor's fallacy"


def puzzle(color=WARN, s=0.9):
    sq = Square(s).set_stroke(color, 5)
    k1 = Circle(s * 0.16).set_stroke(color, 5).move_to(sq.get_right())
    k2 = Circle(s * 0.16).set_stroke(color, 5).move_to(sq.get_top())
    return VGroup(sq, k1, k2)


class S91Next(Base):
    CHAPTER = "Next Time"

    def construct(self):
        lg = logo(1.1).move_to(UP * 1.1).scale(0.42).to_edge(UP, buff=0.32)   # carried over from Subscribe
        self.add(lg)
        # ── s120 a puzzle for next time ──
        self.at("s120", 0.0)
        pz = puzzle().move_to(UP * 0.4)
        self.play(Create(pz), run_time=0.7)
        self.play(Rotate(pz, PI / 8), run_time=0.4)
        self.idle(lambda: Rotate(pz, -PI / 16, rate_func=there_and_back))

        # ── s121 an expert: 1 in a million chance an innocent person matches ──
        self.at("s121", 0.0)
        self.idle()
        court = sticker("assets/courtroom.png", 2.0).move_to(LEFT * 3.6 + UP * 0.5)
        self.play(FadeOut(pz, scale=0.5), FadeIn(court, shift=RIGHT * 0.8), run_time=0.6)
        ev = VGroup(card(5.6, 1.9, WARN), T("chance an innocent person", 28, INK2, weight=BOLD), T("matches the evidence", 28, INK2, weight=BOLD),
                    TB("1 in 1,000,000", 44, WARN))
        VGroup(*ev[1:]).arrange(DOWN, buff=0.14).move_to(ev[0])
        ev.move_to(RIGHT * 3.0 + UP * 0.5)
        self.word("s121", "chance", dt=-0.3)
        self.play(FadeIn(ev[0]), FadeIn(ev[1:3], shift=UP * 0.2), run_time=0.5)
        self.word("s121", "million", dt=-0.5)
        self.play(FadeIn(ev[3], scale=1.4), ripple(ev[3].get_center(), WARN, r=0.5, scale=3), run_time=0.5)
        self.idle(lambda: pulse(ev, 1.05))

        # ── s122 so the jury thinks: 1 in a million they're innocent? real cases went this way ──
        self.at("s122", 0.0)
        self.idle()
        bt = T("“so 1 in a million they're innocent?”", 30, INK, weight=BOLD)
        bb = RoundedRectangle(corner_radius=0.3, width=bt.width + 0.7, height=1.0).set_stroke(INK2, 3).set_fill("#22221f", 1)
        bb.qa_container = True
        bub = VGroup(bb, bt).move_to(DOWN * 1.55)
        bt.move_to(bb)
        self.word("s122", "jury", dt=-0.3)
        self.play(FadeIn(bub, shift=UP * 0.3), run_time=0.5)
        qm = TB("?", 60, RED_).next_to(bb, RIGHT, buff=0.25)
        self.play(FadeIn(qm, scale=0.4), run_time=0.35)
        real = pill("this happened in real trials", RED_, 26).move_to(RIGHT * 3.0 + DOWN * 0.5)
        self.word("s122", "Real", dt=-0.3)
        self.play(FadeIn(real, shift=LEFT * 0.3), ev.animate.shift(UP * 0.5), run_time=0.5)
        self.idle(lambda: Wiggle(qm, scale_value=1.3), lambda: pulse(real, 1.08))

        # ── s123 the very same flip: next time, the prosecutor's fallacy ──
        self.at("s123", 0.0)
        self.idle()
        f1 = MathTex(r"P(\text{match}\mid\text{innocent})", font_size=56, color=WARN)
        ne = MathTex(r"\neq", font_size=72, color=RED_)
        f2 = MathTex(r"P(\text{innocent}\mid\text{match})", font_size=56, color=VIOLET)
        row = VGroup(f1, ne, f2).arrange(RIGHT, buff=0.4).move_to(UP * 0.4)
        self.play(FadeOut(Group(court, ev, bub, qm, real), shift=LEFT * 1.0), run_time=0.5)
        self.word("s123", "same", dt=-0.3)
        self.play(Write(f1), run_time=0.7)
        self.play(FadeIn(ne, scale=1.6), TransformFromCopy(f1, f2), run_time=0.8)
        nx = chip(f"next:  {NEXT_TOPIC}", AQUA, 30).next_to(lg, DOWN, buff=0.3)
        self.word("s123", "prosecutor's", dt=-0.4)
        self.play(FadeIn(nx, shift=DOWN * 0.2), run_time=0.6)
        smart = pill("why smart people fall for it", WARN, 28).move_to(DOWN * 1.4)
        self.word("s123", "smart", dt=-0.3)
        self.play(FadeIn(smart, shift=UP * 0.2), run_time=0.4)
        self.idle(lambda: Wiggle(ne, scale_value=1.3), lambda: pulse(nx, 1.08))

        # ── "I will see you in the next video." (word for word) ──
        self.at("s124", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(f1, ne, f2, smart), shift=DOWN * 0.3), run_time=0.5)
        self.play(VGroup(lg, nx).animate.move_to(UP * 0.4).scale(1.4), run_time=0.8)
        self.idle(lambda: pulse(nx, 1.08), lambda: pulse(lg, 1.06))
        self.finish()
