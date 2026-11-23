import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


class S01Hook(Base):
    CHAPTER = "A Tired Uptrend"

    def construct(self):
        g = price_axes(); ax = g.ax
        P = pieces(ax)
        ill = T("illustration · made-up stock", 22, MUTED).move_to(ax.c2p(40, 24))
        # s001: climb from 32 to 60
        self.at("s001", 0.0)
        self.play(FadeIn(g), FadeIn(ill), run_time=0.8)
        self.play(Create(P[0]), run_time=3.2, rate_func=linear)
        t60 = peak_label(ax, "ls", "$60", SH_COL)
        self.play(FadeIn(t60, shift=UP * 0.15), run_time=0.4)
        # s002: dip, new high 70
        self.at("s002", 0.1)
        self.play(Create(P[1]), run_time=1.8, rate_func=linear)
        t70 = peak_label(ax, "head", "$70", HEAD_COL)
        self.play(FadeIn(t70, shift=UP * 0.15), Flash(pt(ax, "head"), color=HEAD_COL), run_time=0.5)
        # s003: right shoulder only 61, lower high
        self.at("s003", 0.0)
        self.play(Create(P[2]), run_time=1.8, rate_func=linear)
        t61 = peak_label(ax, "rs", "$61", SH_COL)
        guide = hline(ax, 70, 24.6, 37.5, HEAD_COL, dashed=True, width=3)
        g61 = hline(ax, 61, 35.2, 37.5, SH_COL, dashed=True, width=3)
        gap = Arrow(ax.c2p(37, 69.6), ax.c2p(37, 61.4), buff=0, color=RED_, stroke_width=5,
                    max_tip_length_to_length_ratio=0.3)
        lh = pill("lower high", RED_, 26).next_to(ax.c2p(37.6, 65.5), RIGHT, buff=0.15)
        self.play(FadeIn(t61, shift=UP * 0.15), Create(guide), Create(g61), run_time=0.6)
        self.play(GrowArrow(gap), FadeIn(lh), run_time=0.7)
        # s004: two bounces at 52, then the break
        self.at("s004", 0.0)
        bd = VGroup(*[Dot(pt(ax, k), radius=0.11, color=NECK_COL) for k in ("t1", "t2")])
        self.play(FadeIn(bd, scale=0.4), run_time=0.4)
        self.play(*[Indicate(d, color=NECK_COL, scale_factor=1.8) for d in bd], run_time=0.8)
        self.play(Create(P[3]), run_time=1.3, rate_func=linear)
        self.play(Flash(pt(ax, "break"), color=RED_, flash_radius=0.4), run_time=0.5)
        # s005: the silhouette
        self.at("s005", 0.0)
        self.play(FadeOut(VGroup(guide, g61, gap, lh)), run_time=0.4)
        outline = [(8, 47), (11, 57), (14, 63.5), (17, 60), (20.5, 61), (21, 65), (22, 71), (24, 74), (26, 71),
                   (27, 65), (27.5, 61), (31, 61), (33, 64.5), (36, 59), (38.5, 49)]
        sil = VMobject(stroke_color=VIOLET, stroke_width=6).set_points_smoothly([ax.c2p(x, y) for x, y in outline])
        sil.qa_ignore = True   # decorative outline drawn around the peak labels
        self.play(FadeOut(VGroup(t60, t70, t61)), Create(sil), run_time=2.0)
        names = VGroup(T("shoulder", 26, SH_COL, weight=BOLD).move_to(ax.c2p(13, 68)),
                       T("head", 26, HEAD_COL, weight=BOLD).move_to(ax.c2p(24, 78)),
                       T("shoulder", 26, SH_COL, weight=BOLD).move_to(ax.c2p(34.5, 69)))
        self.play(LaggedStart(*[FadeIn(n, shift=DOWN * 0.15) for n in names], lag_ratio=0.35), run_time=1.4)
        # s006: title card
        self.at("s006", 0.0)
        title = title_card("HEAD & SHOULDERS", "explained simply, with real numbers", size=96)
        self.play(FadeOut(VGroup(g, P[:4], bd, sil, names, ill)), run_time=0.5)
        self.play(FadeIn(title, scale=0.9), run_time=0.7)
        self.finish()
