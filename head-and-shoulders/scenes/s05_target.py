import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def bracket(ax, x, y0, y1, color, w=0.14):
    a, b = ax.c2p(x, y0), ax.c2p(x, y1)
    return VGroup(Line(a, b), Line(a + LEFT * w, a + RIGHT * w), Line(b + LEFT * w, b + RIGHT * w)).set_stroke(color, 6)


def eq(*parts, size=34):
    return VGroup(*[T(t, size, c, weight=BOLD if c not in (MUTED,) else NORMAL) for t, c in parts]).arrange(RIGHT, buff=0.22)


class S05Target(Base):
    CHAPTER = "The Price Target"

    def construct(self):
        g = price_axes(); ax = g.ax
        P = pieces(ax)
        nl = hline(ax, NECK, 6, 44, NECK_COL, width=5)
        rt = path_piece(ax, KEY["break"], KEY["retest"])
        self.add(g, P[:4], rt, nl)
        box = card(5.6, 2.0, INK2).move_to(ax.c2p(24, 33))
        # s024: how far might it fall?
        self.at("s024", 0.0)
        q = T("how far might it fall?", 30, TGT_COL, weight=BOLD).move_to(box)
        self.play(FadeIn(box), FadeIn(q, shift=UP * 0.15), run_time=0.7)
        # s025: measure the head above the neckline
        self.at("s025", 0.0)
        guide = hline(ax, HEAD, 24.6, 46, HEAD_COL, dashed=True, width=3)
        br = bracket(ax, 45, NECK, HEAD, TGT_COL)
        self.play(Create(guide), run_time=0.6)
        self.play(GrowFromEdge(br, DOWN), run_time=0.8)
        # s026: 70 − 52 = 18
        self.at("s026", 0.0)
        e1 = eq(("height", MUTED), ("70", HEAD_COL), ("−", MUTED), ("52", NECK_COL), ("=", MUTED), ("18", TGT_COL))
        e1.move_to(box.get_center() + UP * 0.42)
        tag = T("$18", 28, TGT_COL, weight=BOLD).next_to(br, LEFT, buff=0.2)
        self.play(FadeOut(q), FadeIn(e1, shift=UP * 0.15), FadeIn(tag), run_time=0.8)
        # s027: copy it down
        self.at("s027", 0.0)
        br2 = br.copy()
        self.add(br2)
        self.play(br2.animate.move_to(bracket(ax, 45, TARGET, NECK, TGT_COL)), FadeOut(tag), run_time=1.4)
        # s028: 52 − 18 = 34 → target line, price follows
        self.at("s028", 0.0)
        e2 = eq(("target", MUTED), ("52", NECK_COL), ("−", MUTED), ("18", TGT_COL), ("=", MUTED), ("34", TGT_COL))
        e2.move_to(box.get_center() + DOWN * 0.42)
        tl = hline(ax, TARGET, 38, 48, TGT_COL, dashed=True, width=4)
        tlab = T("target $34", 28, TGT_COL, weight=BOLD).next_to(ax.c2p(42.5, TARGET), DOWN, buff=0.15)
        self.play(FadeIn(e2, shift=UP * 0.15), run_time=0.7)
        self.until(word_time("s028", word_index("s028", "that")) - 0.2)
        self.play(FadeOut(box), FadeOut(VGroup(e1, e2)), Create(tl), FadeIn(tlab), run_time=0.8)
        rest = path_piece(ax, KEY["retest"], KEY["end"])
        self.play(FadeOut(VGroup(br, br2, guide)), Create(rest), run_time=1.6, rate_func=linear)
        # s029: stop above the right shoulder
        self.at("s029", 0.0)
        sl = hline(ax, RS, 33.5, 48, STOP_COL, dashed=True, width=4)
        slab = T("stop $61", 28, STOP_COL, weight=BOLD).next_to(ax.c2p(35.5, RS), UP, buff=0.15)
        wrong = T("where you'd be wrong", 22, STOP_COL).next_to(slab, UP, buff=0.12).align_to(slab, LEFT)
        self.until(word_time("s029", word_index("s029", "common")) - 0.2)
        self.play(Create(sl), FadeIn(slab), run_time=0.8)
        self.play(FadeIn(wrong), Indicate(pt_dot := Dot(pt(ax, "rs"), radius=0.1, color=SH_COL)), run_time=0.8)
        # s030: risk 9 vs reward 18
        self.at("s030", 0.0)
        rk = bracket(ax, 47, NECK, RS, STOP_COL)
        rw = bracket(ax, 47, TARGET, NECK, TGT_COL)
        box2 = card(5.6, 2.0, INK2).move_to(ax.c2p(24, 33))
        r1 = eq(("risk", MUTED), ("61", STOP_COL), ("−", MUTED), ("52", NECK_COL), ("=", MUTED), ("$9", STOP_COL), size=30)
        r2 = eq(("reward", MUTED), ("52", NECK_COL), ("−", MUTED), ("34", TGT_COL), ("=", MUTED), ("$18", TGT_COL), size=30)
        VGroup(r1, r2).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(box2)
        self.play(FadeOut(pt_dot), GrowFromEdge(rk, DOWN), FadeIn(box2), FadeIn(r1), run_time=0.8)
        self.until(word_time("s030", word_index("s030", "aim")) - 0.1)
        self.play(GrowFromEdge(rw, UP), FadeIn(r2), run_time=0.8)
        # s031: 2 : 1
        self.at("s031", 0.0)
        badge = pill("2 : 1  reward to risk", TGT_COL, 34)
        badge.move_to(box2)
        self.play(FadeOut(VGroup(r1, r2)), ReplacementTransform(box2, badge.box), FadeIn(badge.text), run_time=0.7)
        self.play(Indicate(badge, color=TGT_COL, scale_factor=1.08), run_time=0.9)
        self.until(SEGS["s031"]["end"] + 0.3)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.finish()
