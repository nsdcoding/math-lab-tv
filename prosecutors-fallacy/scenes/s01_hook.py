import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

TITLE = ("The Prosecutor's Fallacy", "the statistics trap smart people fall for")
TITLE_SIZE = 74


def evidence_card(text, color, w=6.0, size=30, value=None, vsize=46):
    t = T(text, size, INK)
    rows = [t]
    if value:
        rows.append(TB(value, vsize, color))
    inner = VGroup(*rows).arrange(DOWN, buff=0.25)
    box = card(max(w, inner.width + 0.9), inner.height + 0.65, color)
    inner.move_to(box)
    g = VGroup(box, inner); g.box, g.inner = box, inner
    return g


class S01Hook(Base):
    CHAPTER = "One in a Million"

    def construct(self):
        # ── s001 the puzzle from last time ──
        self.at("s001", 0.0)
        court = sticker("assets/courtroom.png", 3.4).move_to(UP * 0.5)
        court.set_opacity(0)
        self.play(court.animate(rate_func=rate_functions.ease_out_cubic).set_opacity(1), run_time=0.9)
        frm = chip("from: Hypothesis Testing", AQUA, 26).to_edge(UP, buff=0.45).to_edge(RIGHT, buff=0.5)
        self.word("s001", "puzzle")
        self.play(FadeIn(frm, shift=LEFT * 0.4), run_time=0.5)
        q = TB("?", 90, WARN).next_to(court, DOWN, buff=0.25)
        self.play(FadeIn(q, scale=0.4), ripple(q.get_center(), WARN), run_time=0.6)
        self.word("s001", "solve")
        self.play(q.animate.rotate(TAU).set_color(VIOLET), run_time=0.8)
        self.idle(lambda: pulse(q, s=1.15))

        # ── s002 a city of eight million; a crime; a trace of DNA ──
        self.at("s002", 0.0)
        self.idle()
        city = skyline(12.6, INK2).move_to(DOWN * 1.15)
        self.play(FadeOut(court), FadeOut(q), FadeOut(frm), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.6) for b in city], lag_ratio=0.04), run_time=1.0)
        cnt = ValueTracker(0)
        counter = always_redraw(lambda: TB(f"{int(cnt.get_value()):,} people", 52, AQUA).move_to(UP * 2.55))
        self.add(counter)
        self.play(cnt.animate.set_value(8_000_000), run_time=1.4, rate_func=rate_functions.ease_out_cubic)
        counter.clear_updaters()
        self.word("s002", "crime")
        spot = city[9].get_top() + UP * 0.05
        flash = Star(5, outer_radius=0.32, color=RED_).set_fill(RED_, 1).move_to(spot + UP * 0.3)
        self.play(FadeIn(flash, scale=0.3), ripple(flash.get_center(), RED_, r=0.3, scale=4), run_time=0.6)
        self.word("s002", "DNA")
        d = dna(1.6, WARN).move_to(RIGHT * 4.2 + UP * 0.9)
        mag = VGroup(Circle(0.95).set_stroke(INK, 5), Line(DR * 0.67, DR * 1.25).set_stroke(INK, 8)).move_to(d.get_center() + DR * 0.15)
        mag[0].qa_ignore = True
        self.play(counter.animate.scale(0.7).move_to(LEFT * 3.8 + UP * 2.55), Create(d), FadeIn(mag, scale=0.6), run_time=0.9)
        self.idle(lambda: Rotate(d, PI, axis=UP, run_time=0.85))

        # ── s003 partial, but still rare ──
        self.at("s003", 0.0)
        self.play(*[r.animate.set_stroke(opacity=0.15) for r in d.rungs[len(d.rungs) // 2:]],
                  d[0].animate.set_stroke(opacity=0.55), run_time=0.7)
        part = pill("partial trace", WARN, 28).next_to(mag, DOWN, buff=0.3)
        self.play(FadeIn(part, shift=UP * 0.2), run_time=0.5)
        self.word("s003", "rare")
        rare = pill("but rare", VIOLET, 30).next_to(part, LEFT, buff=0.4)
        self.play(FadeIn(rare, scale=0.6), ripple(rare.get_center(), VIOLET), run_time=0.6)

        # ── s004 Sam matches ──
        self.at("s004", 0.0)
        self.idle()
        trace = VGroup(d, mag)
        self.play(FadeOut(city), FadeOut(flash), FadeOut(part), FadeOut(rare), FadeOut(counter),
                  trace.animate.scale(0.8).move_to(RIGHT * 3.6 + UP * 0.5), run_time=0.7)
        self.word("s004", "Sam")
        sam = sticker("assets/sam.png", 4.2).move_to(LEFT * 3.4 + UP * 0.3)
        sam.set_opacity(0)
        self.play(sam.animate(rate_func=rate_functions.ease_out_cubic).set_opacity(1), run_time=0.7)
        nm = pill("Sam", INK, 30).next_to(sam, DOWN, buff=0.2)
        self.play(FadeIn(nm, shift=UP * 0.2), run_time=0.4)
        self.word("s004", "matches")
        link = DashedLine(sam.get_right() + RIGHT * 0.2, trace.get_left() + LEFT * 0.2, color=WARN, stroke_width=4)
        stamp = pill("MATCH ✓", WARN, 40).move_to(link.get_center() + UP * 0.9)
        self.play(Create(link), FadeIn(stamp, scale=1.6), run_time=0.6)
        self.play(ripple(stamp.get_center(), WARN, r=0.5, scale=3), run_time=0.6)
        self.idle(lambda: pulse(stamp, s=1.12))

        # ── s005 the expert: an innocent person matches 1 in a million ──
        self.at("s005", 0.0)
        self.idle()
        self.play(FadeOut(link), FadeOut(stamp), FadeOut(trace),
                  Group(sam, nm).animate.scale(0.6).move_to(LEFT * 5.6 + DOWN * 0.6), run_time=0.6)
        court = sticker("assets/courtroom.png", 2.5).move_to(RIGHT * 0.9 + UP * 1.65)
        court.set_opacity(0)
        self.play(court.animate(rate_func=rate_functions.ease_out_cubic).set_opacity(1), run_time=0.6)
        self.word("s005", "innocent")
        c1 = evidence_card("an innocent person matches", BLUE_, 5.0, 26, "1 in 1,000,000", 40)
        c1.move_to(DOWN * 1.45).set_x(-4.45 + c1.width / 2)
        self.play(FadeIn(c1, shift=UP * 0.3), run_time=0.6)
        self.word("s005", "million")
        self.play(Indicate(c1.inner[1], color=WARN, scale_factor=1.15), run_time=0.7)
        self.idle(lambda: glint(c1.box, BLUE_))

        # ── s006 the prosecutor: so 1 in a million Sam is innocent ──
        self.at("s006", 0.0)
        self.idle()
        self.word("s006", "prosecutor")
        self.play(court.animate.shift(LEFT * 0.0).scale(1.05), run_time=0.4)
        self.word("s006", "only")
        c2 = evidence_card("Sam is innocent", RED_, 4.0, 26, "1 in 1,000,000", 40)
        c2.next_to(c1, RIGHT, buff=0.45)
        print("cards span", c1.get_left()[0], c2.get_right()[0])
        self.play(TransformFromCopy(c1, c2), run_time=0.9)
        qm = TB("?", 64, RED_).next_to(c2, UP, buff=0.15).align_to(c2, RIGHT).shift(LEFT * 0.2)
        self.play(FadeIn(qm, scale=0.4), ripple(qm.get_center(), RED_), run_time=0.6)
        self.idle(lambda: Wiggle(qm, scale_value=1.2, n_wiggles=4))

        # ── s007 the jury nods ──
        self.at("s007", 0.0)
        self.idle()
        jur = VGroup(*[juror(INK2, 0.8) for _ in range(12)]).arrange(RIGHT, buff=0.26).move_to(RIGHT * 1.0 + UP * 1.5)
        box = card(jur.width + 0.5, 1.3, MUTED).move_to(jur.get_bottom() + UP * 0.15)
        box.set_fill(opacity=0)
        self.play(FadeOut(court), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(j, shift=DOWN * 0.3) for j in jur], lag_ratio=0.06), Create(box), run_time=0.8)
        self.word("s007", "nods")
        self.play(LaggedStart(*[j[1].animate(rate_func=there_and_back).shift(DOWN * 0.12) for j in jur], lag_ratio=0.12),
                  run_time=1.2)
        self.word("s007", "proof")
        pr = pill("sounds like proof", INK, 30).next_to(jur, UP, buff=0.3)
        self.play(FadeIn(pr, scale=0.7), run_time=0.5)

        # ── s008 your turn: agree or disagree? ──
        self.at("s008", 0.0)
        self.play(FadeOut(VGroup(jur, box, pr)), run_time=0.4)
        line = Line(LEFT * 3.2, RIGHT * 3.2).set_stroke(INK2, 6).move_to(RIGHT * 0.9 + UP * 1.9)
        la = T("agree", 30, INK2, weight=BOLD).next_to(line, LEFT, buff=0.35)
        ld = T("disagree", 30, INK2, weight=BOLD).next_to(line, RIGHT, buff=0.35)
        knob = Circle(0.24).set_stroke(INK, 3).set_fill(VIOLET, 1).move_to(line.get_center())
        knob.qa_dot = True
        self.play(Create(line), FadeIn(la), FadeIn(ld), FadeIn(knob, scale=0.4), run_time=0.6)
        your = pill("your call", VIOLET, 28).next_to(line, UP, buff=0.4)
        self.play(FadeIn(your, shift=DOWN * 0.2), run_time=0.4)
        k = [0]
        def sway():
            k[0] += 1
            return knob.animate(rate_func=smooth).set_x(line.get_center()[0] + (2.3 if k[0] % 2 else -2.3))
        self.idle(sway)

        # ── s009 good company: judges, juries, experts ──
        self.at("s009", 0.0)
        self.idle()
        self.play(FadeOut(VGroup(line, la, ld, knob, your)), run_time=0.4)
        icons = [gavel(INK2, 1.6), VGroup(*[juror(INK2, 0.7) for _ in range(3)]).arrange(RIGHT, buff=0.15), labcoat(INK, 1.7)]
        names = ["judges", "juries", "experts"]
        cols = VGroup()
        for ic, nm_ in zip(icons, names):
            lab = T(nm_, 30, INK, weight=BOLD)
            cols.add(VGroup(ic, lab).arrange(DOWN, buff=0.3))
        cols.arrange(RIGHT, buff=1.4).move_to(RIGHT * 0.9 + UP * 1.75)
        for i, w in enumerate(["Judges", "juries", "experts"]):
            self.word("s009", w)
            self.play(FadeIn(cols[i], shift=UP * 0.3), run_time=0.45)
        self.word("s009", "mistake")
        tags = VGroup(*[pill("fell for it", RED_, 22).next_to(c_, UP, buff=0.2) for c_ in cols])
        self.play(LaggedStart(*[FadeIn(t_, scale=1.5) for t_ in tags], lag_ratio=0.2), run_time=0.8)

        # ── s010 the reveal, locked ──
        self.at("s010", 0.0)
        self.play(FadeOut(VGroup(cols, tags)), FadeOut(VGroup(c1, c2, qm)), run_time=0.5)
        rv = evidence_card("Sam is innocent", VIOLET, 6.0, 40, "about 8 in 9", 60).move_to(RIGHT * 0.9 + UP * 0.6)
        cover = RoundedRectangle(corner_radius=0.12, width=rv.inner[1].width + 0.5, height=rv.inner[1].height + 0.16).set_stroke(MUTED, 2).set_fill("#2b2b28", 1)
        cover.move_to(rv.inner[1])
        lk = lock_icon(INK2, 0.55).move_to(cover)
        rv.inner[1].set_opacity(0)      # the answer stays hidden under the lock until the lesson
        self.qa_mute(rv.inner[1])
        self.play(FadeIn(rv, shift=UP * 0.3), FadeIn(cover), FadeIn(lk), run_time=0.7)
        self.word("s010", "innocent")
        self.play(Indicate(rv.inner[0], color=VIOLET, scale_factor=1.1), run_time=0.7)
        self.idle(lambda: Wiggle(lk, scale_value=1.15, n_wiggles=3))
        self.word("s010", "spot")
        yw = pill("you'll see why", AQUA, 30).next_to(rv, DOWN, buff=0.45)
        self.play(FadeIn(yw, shift=UP * 0.2), run_time=0.5)

        # ── s011 title card ──
        self.at("s011", 0.0)
        self.idle()
        title = title_card(*TITLE, size=TITLE_SIZE)
        self.play(FadeOut(VGroup(rv, cover, lk, yw)), Group(sam, nm).animate.set_opacity(0), run_time=0.5)
        self.remove(sam, nm)
        self.play(FadeIn(title[0], scale=0.85), run_time=0.7)
        self.play(FadeIn(title[1], shift=UP * 0.2), run_time=0.5)
        self.finish()
