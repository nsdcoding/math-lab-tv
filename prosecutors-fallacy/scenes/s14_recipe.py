import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

STEPS = [("Find the given", "what does the number assume is true?", "innocent"),
         ("Flip it", "is that the question you care about?", "innocent | match?"),
         ("Find the crowd", "the base rate: how many could match?", "8,000,000"),
         ("Count the matches", "crowd × false-match rate, + the real ones", "8 + 1"),
         ("Divide", "real matches ÷ all matches; add other evidence", "1 in 9")]


class S14Recipe(Base):
    CHAPTER = "Recipe"

    def construct(self):
        self.at("s115", 0.0)
        title = TB("catch the swap", 48, VIOLET)
        rows = VGroup()
        for k, (h, e, _) in enumerate(STEPS):
            n = TB(str(k + 1), 40, AQUA)
            hh = T(h, 32, INK, weight=BOLD)
            ee = T(e, 26, INK2)
            rows.add(VGroup(n, hh, ee))
        # two columns: number + heading | explanation (explanations left-aligned in one column)
        hw = max(r[1].width for r in rows)
        for i, r in enumerate(rows):
            y = -i * 0.78
            r[0].move_to([0, y, 0])
            r[1].next_to(r[0], RIGHT, buff=0.35)
            r[2].move_to([0, y, 0]).set_x(r[0].get_right()[0] + 0.35 + hw + 0.7 + r[2].width / 2)
        body = VGroup(title, rows).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        box = card(body.width + 1.0, body.height + 0.8, VIOLET)
        body.move_to(box)
        rc = VGroup(box, body).move_to(UP * 0.3)
        if rc.width > 13.2:
            rc.scale_to_fit_width(13.2)
        for r in rows:
            r.set_opacity(0)
        self.qa_mute(rows)
        self.play(Create(box), FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
        for sid, r in zip(("s116", "s117", "s118", "s119", "s120"), rows):
            self.at(sid, 0.0)
            self.qa_mute(r, False)
            r.shift(RIGHT * 0.3)
            self.play(r.animate.set_opacity(1).shift(LEFT * 0.3), run_time=0.5)
            self.play(pulse(r[0], s=1.25), run_time=0.4)

        # ── s120a try it on Sam: ticks + values ──
        self.at("s120a", 0.0)
        self.idle()
        vals = VGroup()
        for k, (r, (_, _, v)) in enumerate(zip(rows, STEPS)):
            t = T("Sam:  " + v, 28, VIOLET if k == 4 else WARN, weight=BOLD)
            t.move_to(r[2], aligned_edge=LEFT)
            vals.add(t)
        sam = sticker("assets/sam.png", 1.2).next_to(title, RIGHT, buff=0.6)
        sam.set_opacity(0)
        tt = T("try it on Sam", 30, INK2, weight=BOLD).next_to(sam, RIGHT, buff=0.3)
        self.play(sam.animate(rate_func=rate_functions.ease_out_cubic).set_opacity(1), FadeIn(tt), run_time=0.5)
        words = ["given", "Flip", "crowd", "matches", "Divide"]
        for t, w, r in zip(vals, words, rows):
            self.word("s120a", w)
            self.play(FadeOut(r[2], shift=UP * 0.15), FadeIn(t, shift=UP * 0.15), r[0].animate.set_color(VIOLET), run_time=0.45)
            r.remove(r[2])   # keep the faded explanation out of the card group (a later move would re-add it)

        # ── s121 closing line ──
        self.at("s121", 0.0)
        self.idle()
        cl = T("A rare match is not a rare chance of innocence.", 36, VIOLET, weight=BOLD)
        cl.next_to(rc, DOWN, buff=0.3).set_x(0)
        if cl.get_bottom()[1] < -2.55:
            self.play(Group(rc, vals, sam, tt).animate.shift(UP * (-2.55 - cl.get_bottom()[1])), run_time=0.4)
            cl.next_to(rc, DOWN, buff=0.3).set_x(0)
        self.play(FadeIn(cl, shift=UP * 0.2), run_time=0.7)
        self.play(ripple(cl.get_center(), VIOLET, r=0.8, scale=3), run_time=0.6)
        self.idle(lambda: glint(cl, VIOLET))
        self.finish()
