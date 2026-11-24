import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cm import *


class S05Fill(Base):
    CHAPTER = "Filling the Grid"

    def construct(self):
        g = grid_at()
        self.add(g.cells, g.names, g.collab, g.coltitle, g.rowlab, g.rowtitle)

        # ── s053 Detector A ──
        self.at("s053", 0.0)
        da = pill("Detector A", AQUA, 32).move_to(RIGHT * PANEL_X + UP * 2.25)
        self.play(FadeIn(da, shift=DOWN * 0.15), run_time=0.5)
        sub = T("catches 90% of fraud", 24, AQUA).next_to(da, DOWN, buff=0.2)
        self.word("s053", "catches")
        self.play(FadeIn(sub), run_time=0.4)

        # ── s054 10,000 payments to sort ──
        self.at("s054", 0.0)
        rng = np.random.default_rng(3)
        fraud_cells = set()
        while len(fraud_cells) < 100:
            fraud_cells.add((int(rng.integers(0, 100)), int(rng.integers(0, 100))))
        fld = field_squares(100, 100, 0.028, skip=fraud_cells, opacity=0.5)
        frd = field_squares(100, 100, 0.028, color=RED_, opacity=1,
                            skip={(c, r) for c in range(100) for r in range(100)} - fraud_cells)
        F = VGroup(fld, frd).move_to(RIGHT * (PANEL_X + 0.4) + DOWN * 0.45)
        fl = T("10,000 payments", 24, INK2).next_to(F, DOWN, buff=0.2)
        self.play(FadeIn(F), FadeIn(fl), run_time=0.7)
        self.word("s054", "sort")
        flyers = VGroup(*[Square(0.09, stroke_width=0, fill_color=(RED_ if k % 4 == 0 else INK2), fill_opacity=1)
                          .move_to(F.get_center() + np.array([rng.uniform(-1.3, 1.3), rng.uniform(-1.3, 1.3), 0]))
                          for k in range(24)])
        self.qa_mute(flyers)
        dest = [g.cell[KEYS[k % 4]].get_center() + np.array([rng.uniform(-0.6, 0.6), -0.45, 0]) for k in range(24)]
        self.play(LaggedStart(*[FadeOut(f, target_position=d) for f, d in zip(flyers, dest)], lag_ratio=0.05),
                  run_time=1.6, rate_func=rate_functions.ease_in_out_sine)

        # ── s055 the 100 frauds → top row ──
        self.at("s055", 0.0)
        self.play(FadeOut(VGroup(F, fl)), run_time=0.4)
        rt0 = pill("100", ORANGE_, 26).next_to(g.row0(), RIGHT, buff=0.22)
        self.play(FadeOut(sub), run_time=0.3)
        self.word("s055", "hundred")
        self.play(FadeIn(rt0, shift=LEFT * 0.15), highlight(g.row0(), color=ORANGE_), run_time=0.9)

        def fly(n, cols, color, key, src):
            blk = squares(n, cols, 0.13, color).move_to(src)
            self.qa_mute(blk)
            self.play(FadeIn(blk), run_time=0.35)
            self.play(blk.animate.scale(0.6).move_to(g.cell[key].get_center() + DOWN * 0.2), run_time=0.7,
                      rate_func=rate_functions.ease_in_out_sine)
            return blk

        src = RIGHT * (PANEL_X + 0.4) + DOWN * 0.4
        # ── s056 90 caught ──
        self.at("s056", 0.0)
        self.word("s056", "ninety")
        b = fly(90, 10, RED_, "TP", src)
        self.play(FadeOut(b), g.set_num("TP", 90), g.light("TP"), run_time=0.45)
        # ── s057 10 missed ──
        self.at("s057", 0.0)
        b = fly(10, 5, RED_, "FN", src)
        self.play(FadeOut(b), g.set_num("FN", 10), g.light("FN"), run_time=0.45)

        # ── s058 the 9,900 fine payments → bottom row ──
        self.at("s058", 0.0)
        rt1 = pill("9,900", INK2, 26).next_to(g.row1(), RIGHT, buff=0.22)
        self.word("s058", "nine")
        self.play(FadeIn(rt1, shift=LEFT * 0.15), highlight(g.row1(), color=INK2), run_time=0.9)
        # ── s059 30 false alarms ──
        self.at("s059", 0.0)
        self.word("s059", "thirty")
        b = fly(30, 10, INK2, "FP", src)
        self.play(FadeOut(b), g.set_num("FP", 30), g.light("FP"), run_time=0.45)
        ph = VGroup(*[phone(ORANGE_, 0.42) for _ in range(10)]).arrange(RIGHT, buff=0.12)
        ph3 = VGroup(ph, ph.copy(), ph.copy()).arrange(DOWN, buff=0.15).move_to(RIGHT * (PANEL_X + 0.35) + UP * 0.5)
        pl = T("30 worried phone calls", 24, ORANGE_, weight=BOLD).next_to(ph3, DOWN, buff=0.3)
        self.word("s059", "phone")
        self.play(LaggedStart(*[FadeIn(p) for p in ph3], lag_ratio=0.2), FadeIn(pl), run_time=0.8)
        # ── s060 9,870 left alone ──
        self.at("s060", 0.0)
        self.play(FadeOut(VGroup(ph3, pl)), run_time=0.4)
        self.word("s060", "nine")
        n = ValueTracker(0)
        def cnt():
            t = TB(fmt(int(n.get_value())), 60, INK)
            t.move_to(g.num["TN"])
            return t
        g.num["TN"].become(TB("9,870", 60, INK).move_to(g.num["TN"]))
        live = always_redraw(cnt)
        self.add(live)
        self.play(n.animate.set_value(9870), g.light("TN"), run_time=1.6, rate_func=rate_functions.ease_out_cubic)
        self.remove(live)
        g.counts["TN"] = 9870
        self.add(g.num["TN"])

        # ── s061-s063 check the totals ──
        self.at("s061", 0.0)
        e1 = panel_eq([("90", AQUA), ("+", INK2), ("10", BLUE_), ("=", INK2), ("100", ORANGE_)], 1.0, dx=0.3)
        ck1 = check(AQUA, 0.28).next_to(e1, RIGHT, buff=0.25)
        self.word("s061", "Ninety")
        self.play(FadeIn(e1), run_time=0.5)
        self.word("s061", "every")
        self.play(Create(ck1), highlight(rt0, color=ORANGE_), run_time=0.8)
        self.at("s062", 0.0)
        e2 = panel_eq([("30", ORANGE_), ("+", INK2), ("9,870", AQUA), ("=", INK2), ("9,900", INK2)], 0.0, dx=0.3)
        ck2 = check(AQUA, 0.28).next_to(e2, RIGHT, buff=0.25)
        self.play(FadeIn(e2), run_time=0.5)
        self.word("s062", "every")
        self.play(Create(ck2), highlight(rt1, color=INK2), run_time=0.8)
        self.at("s063", 0.0)
        e3 = panel_eq([("all four", INK), ("=", INK2), ("10,000", INK)], -1.0, dx=0.3)
        ck3 = check(AQUA, 0.28).next_to(e3, RIGHT, buff=0.25)
        self.play(FadeIn(e3), run_time=0.5)
        self.word("s063", "exactly")
        self.play(Create(ck3), run_time=0.4)

        # ── s064 the left column = every alarm ──
        self.at("s064", 0.0)
        self.play(FadeOut(VGroup(e1, ck1, e2, ck2, e3, ck3)), run_time=0.4)
        fr = g.frame_of(g.col0(), VIOLET)
        self.word("s064", "left")
        self.play(Create(fr), run_time=0.6)
        ct = panel_eq([("90", AQUA), ("+", INK2), ("30", ORANGE_), ("=", INK2), ("120", VIOLET)], 0.6, dx=0.3)
        cl = T("every alarm A raised", 26, VIOLET).next_to(ct, DOWN, buff=0.3)
        self.word("s064", "Ninety")
        self.play(FadeIn(ct), run_time=0.5)
        self.word("s064", "every")
        self.play(FadeIn(cl), run_time=0.4)

        # ── s065 rows = truth, columns = what it did ──
        self.at("s065", 0.0)
        self.play(FadeOut(VGroup(ct, cl, fr, da, rt0, rt1)), run_time=0.4)
        r1 = side_card([T("→  the truth", 30, ORANGE_, weight=BOLD)], ORANGE_, title="ROWS", title_color=ORANGE_)
        r2 = side_card([T("↓  what it did", 30, VIOLET, weight=BOLD)], VIOLET, title="COLUMNS", title_color=VIOLET)
        VGroup(r1, r2).arrange(DOWN, buff=0.4).move_to(RIGHT * PANEL_X + UP * 0.2)
        self.word("s065", "rows")
        self.play(FadeIn(r1, shift=LEFT * 0.2), highlight(g.row0(), color=ORANGE_), run_time=0.8)
        self.word("s065", "columns")
        self.play(FadeIn(r2, shift=LEFT * 0.2), run_time=0.5)
        fc = g.frame_of(g.col0(), VIOLET)
        self.play(Create(fc), run_time=0.5)
        self.play(FadeOut(fc), run_time=0.4)
        self.word("s065", "row,")
        fr0 = g.frame_of(g.row0(), ORANGE_)
        self.play(Create(fr0), run_time=0.5)
        self.word("s065", "column.")
        self.play(ReplacementTransform(fr0, g.frame_of(g.col0(), VIOLET)), run_time=0.6)
        self.until(SEGS["s065"]["end"] + 0.1)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (g.cells, g.names, g.collab, g.coltitle, g.rowlab, g.rowtitle)
                    and m not in g.nums.submobjects and m not in list(g.num.values())],
                  *[g.unlight(k) for k in KEYS], run_time=0.5)
        self.finish()
