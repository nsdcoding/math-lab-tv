import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *


class S16Indep(PBase):
    CHAPTER = "Independent or Not?"

    def construct(self):
        self.at("s257")
        hd = header("independent or not?", WARN, 34)
        qq = T("does the first result change the chances of the second?", 30, INK2).move_to(UP * 2.05)
        self.play(FadeIn(hd), run_time=0.5)
        self.w("s257", "does")
        self.play(FadeIn(qq), run_time=0.6)
        items = [
            ("s258", VGroup(coin("H", WARN, 0.35), coin("T", WARN, 0.35)).arrange(RIGHT, buff=0.2), "coin today, coin tomorrow", True, "independent"),
            ("s259", VGroup(ic_card(INK2, 0.5, 0.7), ic_card(INK2, 0.5, 0.7)).arrange(RIGHT, buff=0.15), "card, keep it, card again", False, "not"),
            ("s260", VGroup(ic_cloud(BLUE_, 0.45), ic_cloud(BLUE_, 0.45)).arrange(RIGHT, buff=0.25), "rain today, rain tomorrow", False, "not"),
            ("s261", VGroup(ic_cake(ORANGE_, 0.55), ic_cake(VIOLET, 0.55)).arrange(RIGHT, buff=0.5), "your birthday, a stranger's", True, "independent"),
            ("s262", VGroup(ic_book("", INK2, 0.5, 0.7), ic_quiz(INK2, 0.6, None)).arrange(RIGHT, buff=0.3), "study tonight, pass tomorrow", False, "not"),
        ]
        rows = VGroup()
        for k, (sid, ic, txt, ind, word) in enumerate(items):
            self.at(sid)
            num = TB(str(k + 1), 34, INK2)
            t = T(txt, 30, INK)
            row = VGroup(num, ic, t).arrange(RIGHT, buff=0.4)
            row.move_to(LEFT * 1.6 + UP * (1.25 - k * 0.78))
            row.align_to(LEFT * 6.2, LEFT)
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.5)
            st = pill("INDEPENDENT" if ind else "NOT independent", AQUA if ind else WARN, 26).move_to([4.6, row.get_y(), 0])
            self.w(sid, word, nth=0)
            self.play(FadeIn(st, scale=1.3), run_time=0.35)
            rows.add(VGroup(row, st))
        # s263 rule
        self.at("s263")
        self.play(FadeOut(VGroup(rows, qq)), run_time=0.4)
        rc = rule_card(["independent → multiply the plain chances", "not independent → multiply the updated chances"], WARN, 36)
        rc.move_to(UP * 0.2)
        self.play(FadeIn(rc, scale=0.9), run_time=0.7)
        self.finish()
