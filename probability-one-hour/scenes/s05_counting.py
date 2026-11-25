import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pkit import *


def coin_tree(levels, x0=-5.6, dx=3.0, height=4.6, y0=-0.05, r=0.3):
    """Coin tree with coin glyphs as nodes. Returns (group, leaves, edges, paths)."""
    root = Dot(radius=0.09, color=INK2).move_to([x0, y0, 0])
    nodes, edges, paths = [[root]], [], [[]]
    n = 1
    for li in range(levels):
        n *= 2
        gap = height / n
        ys = [y0 + height / 2 - gap * (k + 0.5) for k in range(n)]
        cur, ce, newp = [], [], []
        k = 0
        for pi_, par in enumerate(nodes[-1]):
            for f in "HT":
                col = ORANGE_ if li == 0 else (BLUE_ if li == 1 else VIOLET)
                nd = coin(f, col, r if levels < 3 else 0.2).move_to([x0 + dx * (li + 1), ys[k], 0])
                e = Line(par.get_right() + RIGHT * 0.05, nd.get_left() + LEFT * 0.05, color=INK2, stroke_width=3)
                cur.append(nd); ce.append(e); newp.append(paths[pi_] + [f]); k += 1
        nodes.append(cur); edges.append(ce); paths = newp
    return root, nodes, edges, paths


class S05Counting(PBase):
    CHAPTER = "Counting Outcomes"

    def construct(self):
        self.at("s058")
        hd = header("probability by counting", AQUA, 32)
        self.play(FadeIn(hd), run_time=0.6)
        # s059–s060 one die, six outcomes
        self.at("s059")
        d = die(4, ORANGE_, 1.4).move_to(UP * 0.3)
        self.play(FadeIn(d, scale=0.5), run_time=0.5)
        self.play(Rotate(d, PI), run_time=0.6)
        self.at("s060")
        ax = NumberLine(x_range=[0.5, 6.5, 1], length=10.2, color=INK2, stroke_width=3, include_tip=False, include_ticks=False)
        ax.move_to(DOWN * 0.9)
        faces = VGroup(*[die(k, ORANGE_, 1.05).move_to(ax.n2p(k) + UP * 0.85) for k in range(1, 7)])
        nums = VGroup(*[T(str(k), 30, INK2).next_to(ax.n2p(k), DOWN, buff=0.2) for k in range(1, 7)])
        at = T("face", 26, MUTED).next_to(nums, DOWN, buff=0.15)
        self.play(FadeOut(d), Create(ax), FadeIn(at), run_time=0.5)
        self.w("s060", "one")
        for k in range(6):
            if k > 0:
                self.w("s060", ["one", "two", "three", "four", "five", "six"][k])
            self.play(FadeIn(faces[k], shift=UP * 0.3), FadeIn(nums[k]), run_time=0.3)
        # s061 outcome
        self.at("s061")
        dc = def_card("OUTCOME", "one possible result", AQUA, 34).move_to(UP * 1.95)
        self.play(FadeIn(dc, shift=DOWN * 0.2), Indicate(faces[2], color=AQUA), run_time=0.8)
        # s062 sample space
        self.at("s062")
        box = SurroundingRectangle(faces, color=WARN, buff=0.22, corner_radius=0.15, stroke_width=4)
        dc2 = def_card("SAMPLE SPACE", "everything that could happen", WARN, 34).move_to(UP * 1.95)
        self.w("s062", "sample")
        self.play(Create(box), ReplacementTransform(dc, dc2), run_time=0.9)
        # s063 equally likely bars
        self.at("s063")
        self.play(FadeOut(VGroup(box, dc2, faces, nums, at, ax)), run_time=0.4)
        bx = bar_axes([str(k) for k in range(1, 7)], 0.3, 0.1, 8.0, 3.6, "face", "probability", y_fmt=lambda v: f"{v:.1f}")
        bx.move_to(DOWN * 0.15)
        bb = bars(bx.ax, [1 / 6] * 6, ORANGE_, width=0.8)
        lab = T("each = 1/6", 30, ORANGE_, weight=BOLD).next_to(bb, UP, buff=0.2)
        self.play(FadeIn(bx), run_time=0.4)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bb], lag_ratio=0.12), run_time=1.0)
        self.w("s063", "special")
        self.play(FadeIn(lab), run_time=0.5)
        # s064–s065 chance of a four
        self.at("s064")
        self.play(FadeOut(VGroup(bx, bb, lab)), run_time=0.4)
        faces = VGroup(*[die(k, ORANGE_, 1.0) for k in range(1, 7)]).arrange(RIGHT, buff=0.35).move_to(UP * 0.9)
        q = header("chance of rolling a 4?", INK, 32)
        self.play(FadeOut(hd), FadeIn(q), FadeIn(faces), run_time=0.6)
        hd = q
        self.play(faces[3].animate.shift(UP * 0.3), run_time=0.4)
        self.at("s065")
        f = colfrac(1, 6, fs=96).move_to(DOWN * 1.2)
        l_w = T("outcomes we want", 28, AQUA).next_to(f[0], RIGHT, buff=0.6)
        l_t = T("all outcomes", 28, WARN).next_to(f[2], RIGHT, buff=0.6)
        self.play(faces[3][0].animate.set_stroke(AQUA, 6), run_time=0.3)
        self.play(Write(f[0]), FadeIn(l_w), run_time=0.5)
        self.w("s065", "six")
        self.play(Write(f[1]), Write(f[2]), FadeIn(l_t), run_time=0.6)
        self.w("s065", "sixth")
        self.play(f.animate.set_color(VIOLET), run_time=0.5)
        # s066 the recipe
        self.at("s066")
        self.play(FadeOut(VGroup(faces, f, l_w, l_t)), run_time=0.4)
        rc = MathTex(r"P", r"=", r"{\text{outcomes you want}", r"\over", r"\text{all outcomes}}", font_size=72)
        rc[2].set_color(AQUA); rc[4].set_color(WARN); rc[0].set_color(VIOLET)
        rcard = boxed(rc, VIOLET, pad=0.45).move_to(UP * 0.2)
        self.play(FadeIn(rcard[0]), Write(rc), run_time=1.4)
        # s067 P means probability
        self.at("s067")
        self.play(rcard.animate.scale(0.7).move_to(UP * 1.6), run_time=0.5)
        dp = def_card("P( … )", "the probability of …", VIOLET, 34).move_to(DOWN * 0.05)
        ex = MathTex(r"P(4) = {1 \over 6}", font_size=64, color=VIOLET).next_to(dp, DOWN, buff=0.35)
        self.play(FadeIn(dp, shift=UP * 0.2), run_time=0.6)
        self.w("s067", "probability", nth=1)
        self.play(Write(ex), run_time=0.8)
        # s068–s070 even
        self.at("s068")
        self.play(FadeOut(VGroup(dp, ex)), run_time=0.4)
        faces = VGroup(*[die(k, ORANGE_, 0.95) for k in range(1, 7)]).arrange(RIGHT, buff=0.35).move_to(UP * 0.4)
        q = header("chance of an even number?", INK, 32)
        self.play(FadeOut(hd), FadeIn(q), FadeIn(faces), run_time=0.6)
        hd = q
        self.at("s069")
        for k, w in ((1, "two"), (3, "four"), (5, "six")):
            self.w("s069", w)
            self.play(faces[k][0].animate.set_fill(AQUA, 0.35).set_stroke(AQUA, 6), run_time=0.3)
        self.at("s070")
        f = MathTex(r"{3 \over 6}", "=", r"{1 \over 2}", font_size=72, color=VIOLET).move_to(DOWN * 1.5)
        self.play(Write(f[0]), run_time=0.5)
        self.w("s070", "half")
        self.play(Write(f[1:]), run_time=0.6)
        # s071 event
        self.at("s071")
        br = Brace(VGroup(faces[1], faces[5]), DOWN, color=AQUA, buff=0.15)
        self.play(FadeOut(f), run_time=0.3)
        ev = def_card("EVENT", "a group of outcomes you care about", AQUA, 32).move_to(DOWN * 1.8)
        self.play(GrowFromCenter(br), FadeIn(ev, shift=UP * 0.2), run_time=0.8)
        # s072 bigger than four
        self.at("s072")
        self.play(FadeOut(VGroup(br, ev)), *[faces[k][0].animate.set_fill(PANEL, 1).set_stroke(ORANGE_, 4) for k in (1, 3, 5)], run_time=0.4)
        q = header("bigger than 4?", INK, 32)
        self.play(FadeOut(hd), FadeIn(q), run_time=0.4); hd = q
        self.w("s072", "five")
        self.play(*[faces[k][0].animate.set_fill(AQUA, 0.35).set_stroke(AQUA, 6) for k in (4, 5)], run_time=0.4)
        f = MathTex(r"{2 \over 6}", "=", r"{1 \over 3}", font_size=72, color=VIOLET).move_to(DOWN * 1.5)
        self.w("s072", "two")
        self.play(Write(f), run_time=0.8)
        # s073 count / count / divide
        self.at("s073")
        self.play(FadeOut(VGroup(faces, f)), run_time=0.4)
        steps = VGroup(pill("count what you want", AQUA, 34), pill("count everything", WARN, 34), pill("divide", VIOLET, 34)).arrange(RIGHT, buff=0.9)
        steps.scale_to_fit_width(12.4).move_to(DOWN * 1.0)
        arr = VGroup(*[Arrow(steps[i].get_right(), steps[i + 1].get_left(), color=INK2, buff=0.12, stroke_width=4) for i in range(2)])
        for k, w in enumerate(("count", "count", "divide")):
            self.w("s073", w, nth=1 if k == 1 else 0)
            self.play(FadeIn(steps[k], shift=RIGHT * 0.2), *([GrowArrow(arr[k - 1])] if k else []), run_time=0.4)
        # s074–s075 the hidden rule
        self.at("s074")
        ex_ = TB("!", 90, WARN).next_to(rcard, RIGHT, buff=0.4)
        self.play(FadeOut(VGroup(steps, arr)), FadeIn(ex_, scale=0.4), run_time=0.5)
        self.play(Wiggle(ex_), run_time=0.8)
        self.at("s075")
        el = T("only if every outcome is equally likely", 36, WARN, weight=BOLD).next_to(rcard, DOWN, buff=0.45)
        ul = Underline(el, color=WARN, buff=0.08)
        self.play(FadeIn(el, shift=UP * 0.2), run_time=0.6)
        self.play(Create(ul), run_time=0.5)
        # s076–s079 spinner
        self.at("s076")
        self.play(FadeOut(VGroup(rcard, ex_, el, ul)), run_time=0.4)
        q = header("a spinner: red or blue?", INK, 32)
        self.play(FadeOut(hd), FadeIn(q), run_time=0.4); hd = q
        sp = spinner([(0.75, RED_), (0.25, BLUE_)], r=1.7).move_to(LEFT * 3.3 + DOWN * 0.15)
        self.play(FadeIn(sp, scale=0.8), run_time=0.7)
        lr = T("red: 3/4 of the circle", 30, RED_, weight=BOLD).move_to(RIGHT * 2.8 + UP * 1.0)
        lb = T("blue: 1/4 of the circle", 30, BLUE_, weight=BOLD).next_to(lr, DOWN, buff=0.3).align_to(lr, LEFT)
        self.w("s076", "red")
        self.play(FadeIn(lr), run_time=0.4)
        self.w("s076", "blue")
        self.play(FadeIn(lb), run_time=0.4)
        self.at("s077")
        wrong = MathTex(r"P(\text{red}) = {1 \over 2}\,?", font_size=60, color=MUTED).move_to(RIGHT * 2.8 + DOWN * 0.9)
        self.play(Write(wrong), run_time=0.7)
        xx = cross(RED_, 0.5).move_to(wrong); [setattr(m, "qa_ignore", True) for m in xx]
        self.w("s077", "not")
        self.play(Create(xx), run_time=0.4)
        right = MathTex(r"P(\text{red}) = {3 \over 4}", font_size=60, color=VIOLET).move_to(wrong)
        self.w("s077", "three")
        self.play(FadeOut(VGroup(wrong, xx)), Write(right), run_time=0.7)
        self.at("s078")
        cuts = VGroup(*[Line(sp[0].get_arc_center(), sp[0].get_arc_center() + 1.7 * np.array([np.cos(a), np.sin(a), 0]), color=BG, stroke_width=6)
                        for a in (PI / 2, 0, -PI / 2, PI)])
        self.w("s078", "cutting")
        self.play(Create(cuts), run_time=0.8)
        nums = VGroup(*[TB(str(i + 1), 44, INK).move_to(sp[0].get_arc_center() + 0.95 * np.array([np.cos(a), np.sin(a), 0]))
                        for i, a in enumerate((PI / 4, -PI / 4, -3 * PI / 4))])
        self.w("s078", "three")
        self.play(LaggedStart(*[FadeIn(n, scale=0.5) for n in nums], lag_ratio=0.35), run_time=1.0)
        self.at("s079")
        tip = boxed(T("not equally likely?\nsplit into pieces that are", 32, WARN, line_spacing=1.2), WARN, pad=0.35).move_to(RIGHT * 2.8 + DOWN * 0.9)
        self.play(FadeOut(VGroup(right, lr, lb)), FadeIn(tip), run_time=0.6)
        # s080–s089 two coins
        self.at("s080")
        self.clear()
        c1, c2 = coin("H", ORANGE_, 0.7), coin("T", BLUE_, 0.7)
        cc = VGroup(c1, c2).arrange(RIGHT, buff=1.4).move_to(UP * 0.4)
        tl = VGroup(T("coin 1", 28, ORANGE_).next_to(c1, DOWN, buff=0.3), T("coin 2", 28, BLUE_).next_to(c2, DOWN, buff=0.3))
        self.play(FadeIn(cc, scale=0.6), FadeIn(tl), run_time=0.7)
        self.at("s081")
        hd = header("chance of one head and one tail?", INK, 32)
        self.play(FadeIn(hd), run_time=0.5)
        self.at("s082")
        self.play(FadeOut(VGroup(cc, tl)), run_time=0.3)
        three = VGroup(pill("H H", INK2, 40), pill("T T", INK2, 40), pill("one of each", INK2, 40)).arrange(RIGHT, buff=0.7).move_to(UP * 0.5)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in three], lag_ratio=0.3), run_time=1.0)
        g13 = MathTex(r"{1 \over 3}\,?", font_size=72, color=MUTED).next_to(three, DOWN, buff=0.6)
        self.w("s082", "third")
        self.play(Write(g13), run_time=0.5)
        self.at("s083")
        self.play(Wiggle(three[2]), run_time=1.0)
        # tree
        self.at("s084")
        self.play(FadeOut(VGroup(three, g13)), run_time=0.4)
        root, nodes, edges, paths = coin_tree(2, x0=-5.6, dx=2.7, height=4.0, y0=0.15, r=0.36)
        l1 = T("coin 1", 26, ORANGE_).move_to([-2.9, -2.3, 0]); l2 = T("coin 2", 26, BLUE_).move_to([-0.2, -2.3, 0])
        self.play(FadeIn(root), run_time=0.2)
        self.w("s084", "first")
        self.play(*[Create(e) for e in edges[0]], *[FadeIn(n) for n in nodes[1]], FadeIn(l1), run_time=0.8)
        self.w("s084", "then")
        self.play(*[Create(e) for e in edges[1]], *[FadeIn(n) for n in nodes[2]], FadeIn(l2), run_time=0.9)
        self.at("s085")
        leaf_t = VGroup()
        for k, (lf, pth) in enumerate(zip(nodes[2], paths)):
            leaf_t.add(TB(" ".join(pth), 36, INK).next_to(lf, RIGHT, buff=0.5))
        for k in range(4):
            self.w("s085", ["heads", "heads", "tails", "tails"][k], nth=[0, 1, 1, 2][k] if k else 0)
            self.play(FadeIn(leaf_t[k], shift=LEFT * 0.2), run_time=0.35)
        self.at("s086")
        qs = VGroup(*[MathTex(r"\tfrac{1}{4}", font_size=48, color=WARN).next_to(t, RIGHT, buff=0.6) for t in leaf_t])
        self.play(LaggedStart(*[FadeIn(x) for x in qs], lag_ratio=0.15), run_time=0.8)
        self.at("s087")
        hl = VGroup(*[SurroundingRectangle(leaf_t[k], color=AQUA, buff=0.12, corner_radius=0.1) for k in (1, 2)])
        for m in hl: m.qa_ignore = True  # highlight box around the label (deliberate)
        self.w("s087", "two")
        self.play(*[leaf_t[k].animate.set_color(AQUA) for k in (1, 2)], Create(hl), run_time=0.7)
        self.at("s088")
        ans = MathTex(r"{2 \over 4} = {1 \over 2}", font_size=72, color=VIOLET).move_to(RIGHT * 5.2 + UP * 0.9)
        n13 = MathTex(r"{1 \over 3}", font_size=60, color=MUTED).next_to(ans, DOWN, buff=0.6)
        xx = cross(RED_, 0.4).move_to(n13); [setattr(m, "qa_ignore", True) for m in xx]
        self.play(Write(ans), run_time=0.7)
        self.w("s088", "not")
        self.play(FadeIn(n13), Create(xx), run_time=0.5)
        self.at("s089")
        self.play(FadeOut(VGroup(n13, xx)), run_time=0.3)
        keep = T("coin 1 ≠ coin 2", 32, WARN, weight=BOLD).next_to(ans, DOWN, buff=0.6).set_x(5.2)
        self.play(FadeIn(keep), Indicate(leaf_t[1], color=AQUA), Indicate(leaf_t[2], color=AQUA), run_time=1.0)
        # three coins
        self.at("s090")
        self.play(FadeOut(VGroup(*edges[0], *edges[1], root, *nodes[1], *nodes[2], leaf_t, qs, hl, l1, l2, ans, keep)), run_time=0.4)
        q = header("three coins", INK, 32)
        self.play(FadeOut(hd), FadeIn(q), run_time=0.4); hd = q
        self.at("s091")
        root, nodes, edges, paths = coin_tree(3, x0=-6.0, dx=2.2, height=4.7, y0=-0.1)
        cnt = TB("2", 60, WARN).move_to(RIGHT * 5.4 + UP * 1.6)
        self.add(root)
        self.play(*[Create(e) for e in edges[0]], *[FadeIn(n) for n in nodes[1]], FadeIn(cnt), run_time=0.6)
        self.w("s091", "four")
        self.play(*[Create(e) for e in edges[1]], *[FadeIn(n) for n in nodes[2]], Transform(cnt, TB("4", 60, WARN).move_to(cnt)), run_time=0.6)
        self.w("s091", "eight")
        self.play(*[Create(e) for e in edges[2]], *[FadeIn(n) for n in nodes[3]], Transform(cnt, TB("8", 60, WARN).move_to(cnt)), run_time=0.6)
        self.at("s092")
        q = header("exactly two heads?", INK, 32)
        self.play(FadeOut(hd), FadeIn(q), run_time=0.4); hd = q
        lt = VGroup(*[T("".join(pth), 26, INK, weight=BOLD).next_to(lf, RIGHT, buff=0.3) for lf, pth in zip(nodes[3], paths)])
        self.play(FadeIn(lt, lag_ratio=0.05), run_time=0.6)
        self.at("s093")
        two = [k for k, pth in enumerate(paths) if pth.count("H") == 2]
        ctr = TB("0", 60, AQUA).move_to(RIGHT * 5.4 + DOWN * 0.3)
        self.play(FadeIn(ctr), run_time=0.3)
        for i, k in enumerate(two):
            self.w("s093", ["heads", "heads", "tails"][i], nth=[0, 2, 1][i])
            self.play(lt[k].animate.set_color(AQUA), Transform(ctr, TB(str(i + 1), 60, AQUA).move_to(ctr)), run_time=0.4)
        self.at("s094")
        ans = MathTex(r"{3 \over 8}", font_size=84, color=VIOLET).move_to(RIGHT * 5.4 + DOWN * 0.3)
        self.play(ReplacementTransform(ctr, ans), run_time=0.6)
        dec = T("= 0.375", 30, VIOLET).next_to(ans, DOWN, buff=0.3)
        self.play(FadeIn(dec), run_time=0.4)
        self.at("s095")
        tag = pill("draw the tree", WARN, 34).move_to(RIGHT * 5.0 + UP * 1.6)
        self.play(FadeOut(cnt), FadeIn(tag, scale=0.8), run_time=0.5)
        self.play(*[e.animate.set_color(WARN) for lev in edges for e in lev], run_time=0.8)
        self.play(*[e.animate.set_color(INK2) for lev in edges for e in lev], run_time=0.6)
        self.finish()
