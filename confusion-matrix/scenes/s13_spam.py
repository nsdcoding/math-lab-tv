import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cm import *

SPAM = dict(TP=270, FN=30, FP=10, TN=690)


class S13Spam(Base):
    CHAPTER = "Example: A Spam Filter"

    def construct(self):
        # ── s163 spam: the mistakes flip ──
        self.at("s163", 0.0)
        env = VGroup(*[envelope(BLUE_ if k % 3 else WARN, 1.2) for k in range(6)]).arrange(RIGHT, buff=0.3).move_to(UP * 0.9)
        hd = pill("example 2: a spam filter", BLUE_, 30).move_to(DOWN * 0.6)
        self.play(LaggedStart(*[FadeIn(e, shift=UP * 0.15) for e in env], lag_ratio=0.08), FadeIn(hd), run_time=0.8)
        # ── s164 1,000 emails ──
        self.at("s164", 0.0)
        g = grid_at(rows=("really spam", "really real"), cols=("spam folder", "inbox"), col_title="where the filter put it")
        self.play(FadeOut(VGroup(env, hd)), run_time=0.4)
        self.play(FadeIn(VGroup(g.cells, g.names, g.collab, g.coltitle, g.rowlab, g.rowtitle)), run_time=0.6)
        t0 = pill("300", WARN, 26).next_to(g.row0(), RIGHT, buff=0.22)
        t1 = pill("700", INK2, 26).next_to(g.row1(), RIGHT, buff=0.22)
        self.word("s164", "Three")
        self.play(FadeIn(t0), run_time=0.4)
        self.word("s164", "seven")
        self.play(FadeIn(t1), run_time=0.4)
        # ── s165 / s166 fill ──
        self.at("s165", 0.0)
        fl = T("sent to spam: 280", 26, INK2, weight=BOLD).move_to(RIGHT * (PANEL_X + 0.15) + UP * 1.3)
        self.word("s165", "sends")
        self.play(FadeIn(fl), run_time=0.4)
        self.word("s165", "seventy")
        self.play(g.set_num("TP", 270), g.light("TP"), run_time=0.5)
        self.word("s165", "Ten")
        self.play(g.set_num("FP", 10), g.light("FP"), run_time=0.5)
        self.at("s166", 0.0)
        self.word("s166", "thirty")
        self.play(g.set_num("FN", 30), g.light("FN"), run_time=0.5)
        self.word("s166", "six")
        self.play(g.set_num("TN", 690), g.light("TN"), run_time=0.5)
        # ── s167 – s169 the three numbers ──
        self.at("s167", 0.0)
        self.play(FadeOut(VGroup(fl, t0, t1)), run_time=0.3)
        fc = g.frame_of(g.col0(), VIOLET)
        p = T("precision  270/280 ≈ 96%", 24, VIOLET, weight=BOLD).move_to(RIGHT * (PANEL_X + 0.15) + UP * 1.3)
        self.play(Create(fc), FadeIn(p), run_time=0.6)
        self.at("s168", 0.0)
        fr = g.frame_of(g.row0(), ORANGE_, pad=0.17)
        r = T("recall  270/300 = 90%", 24, ORANGE_, weight=BOLD).next_to(p, DOWN, buff=0.3)
        self.play(FadeOut(fc), Create(fr), FadeIn(r), run_time=0.6)
        self.at("s169", 0.0)
        a = T("accuracy  960/1,000 = 96%", 24, WARN, weight=BOLD).next_to(r, DOWN, buff=0.3)
        self.play(FadeOut(fr), FadeIn(a), highlight(g.cell["TP"], g.cell["TN"], color=WARN), run_time=0.8)
        # ── s170 here accuracy is honest ──
        self.at("s170", 0.0)
        lz = T("lazy filter: 700/1,000 = 70%", 22, MUTED, weight=BOLD).next_to(a, DOWN, buff=0.45)
        hon = VGroup(T("spam isn't rare,", 22, AQUA, weight=BOLD), T("so accuracy can't hide", 22, AQUA, weight=BOLD)).arrange(DOWN, buff=0.08).next_to(lz, DOWN, buff=0.3)
        self.word("s170", "lazy")
        self.play(FadeIn(lz), run_time=0.5)
        self.word("s170", "hide.")
        self.play(FadeIn(hon), run_time=0.4)
        # ── s171 / s172 which mistake is worse? ──
        self.at("s171", 0.0)
        self.play(FadeOut(VGroup(p, r, a, lz, hon)), run_time=0.4)
        m1 = side_card(["spam in your inbox:", "a small annoyance"], BLUE_, 24).move_to(RIGHT * (PANEL_X + 0.15) + UP * 1.1)
        self.word("s171", "inbox")
        self.play(FadeIn(m1), highlight(g.cell["FN"], color=BLUE_), run_time=0.8)
        self.at("s172", 0.0)
        m2 = side_card(["a real email in spam:", "job offer, bill, doctor…", "maybe never read"], ORANGE_, 24).next_to(m1, DOWN, buff=0.3)
        self.word("s172", "real")
        self.play(FadeIn(m2), highlight(g.cell["FP"], color=ORANGE_), run_time=0.8)
        # ── s173 spam wants precision ──
        self.at("s173", 0.0)
        self.play(FadeOut(VGroup(m1, m2)), run_time=0.4)
        wp = side_card([T("false alarm = costly", 26, ORANGE_, weight=BOLD), T("→ want high precision", 26, VIOLET, weight=BOLD)],
                       VIOLET).move_to(RIGHT * (PANEL_X + 0.15) + UP * 0.4)
        self.word("s173", "costly")
        self.play(FadeIn(wp, shift=LEFT * 0.2), Create(fc), run_time=0.6)
        # ── s174 opposite priority from the medical test ──
        self.at("s174", 0.0)
        self.play(FadeOut(VGroup(wp, fc)), run_time=0.3)
        cmp_ = VGroup(VGroup(T("medical test", 26, RED_, weight=BOLD), T("★ recall first", 26, ORANGE_, weight=BOLD)).arrange(DOWN, buff=0.1),
                      VGroup(T("spam filter", 26, BLUE_, weight=BOLD), T("★ precision first", 26, VIOLET, weight=BOLD)).arrange(DOWN, buff=0.1)
                      ).arrange(DOWN, buff=0.45).move_to(RIGHT * (PANEL_X + 0.15) + UP * 0.4)
        self.word("s174", "opposite")
        self.play(FadeIn(cmp_), run_time=0.6)
        self.until(SEGS["s174"]["end"] + 0.1)
        self.play(FadeOut(VGroup(cmp_, grid_mobs(g))), run_time=0.5)
        self.finish()
