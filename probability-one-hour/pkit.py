"""Probability kit: reusable visuals for the one-hour probability video (dice, grid, coins, trees, charts, icons).
Layout zones (screen units, frame 14.22 x 8): header chip at y = 2.85, content between y = -2.45 and 2.4,
small persistent badges top-right. Colours: orange die / blue die, aqua = wanted, warn = total, violet = answer."""
import json
from common import *

SIM = json.loads((HERE / "sim.json").read_text())
CELL_FILL = "#2c2c29"
PANEL = "#22221f"


# ─────────────── timing-aware base ───────────────
class PBase(Base):
    def w(self, sid, word, dt=-0.1, nth=0):
        ws = [x.strip(",.;:?!'").lower() for x in SEGS[sid]["text"].split()]
        hits = [i for i, x in enumerate(ws) if x == word.lower()] or [i for i, x in enumerate(ws) if x.startswith(word.lower())]
        if len(hits) <= nth:
            print(f"WORD-MISS {type(self).__name__} {sid} {word!r} nth={nth} (hits {hits})")
            idx = hits[-1] if hits else 0
        else:
            idx = hits[nth]
        self.until(word_time(sid, idx) + dt)

    def clear(self, keep=(), rt=0.5):
        keep_ids = set()
        for k in keep:
            for m in k.get_family():
                keep_ids.add(id(m))
        out = [m for m in self.mobjects if id(m) not in keep_ids]
        if out:
            self.play(*[FadeOut(m) for m in out], run_time=rt)
            self.drop(*out)

    def show(self, *ms, rt=0.6, shift=None, scale=None):
        kw = {}
        if shift is not None: kw["shift"] = shift
        if scale is not None: kw["scale"] = scale
        self.play(*[FadeIn(m, **kw) for m in ms], run_time=rt)

    def swap(self, old, new, rt=0.5):
        self.play(FadeOut(old), FadeIn(new), run_time=rt)
        self.drop(old)


# ─────────────── text pieces ───────────────
def header(text, color=INK, size=30):
    p = pill(text, color, size)
    p.move_to(UP * 2.85)
    return p


def caption(text, color=INK2, size=30, y=-2.15):
    return T(text, size, color).move_to(UP * y)


def tex(s, color=INK, fs=64):
    return MathTex(s, color=color, font_size=fs)


def fr(a, b, color=VIOLET, fs=72):
    return MathTex(r"{" + str(a) + r"\over " + str(b) + r"}", color=color, font_size=fs)


def colfrac(a, b, ca=AQUA, cb=WARN, fs=72):
    m = MathTex(r"{" + str(a), r"\over", str(b) + r"}", font_size=fs)
    m[0].set_color(ca); m[1].set_color(INK2); m[2].set_color(cb)
    return m


def eq_row(*parts, fs=64, buff=0.25):
    """Row of MathTex / Text pieces; strings become MathTex in INK."""
    ms = [tex(p, INK, fs) if isinstance(p, str) else p for p in parts]
    return VGroup(*ms).arrange(RIGHT, buff=buff)


def boxed(mob, color=INK2, pad=0.3, fill=PANEL):
    b = RoundedRectangle(corner_radius=0.18, width=mob.width + 2 * pad, height=mob.height + 2 * pad,
                         stroke_color=color, stroke_width=2.5, fill_color=fill, fill_opacity=1)
    b.qa_container = True
    b.move_to(mob)
    g = VGroup(b, mob); g.box = b
    return g


def def_card(word, meaning, color=WARN, size=32):
    a = T(word, size, color, weight=BOLD)
    e = T("=", size, MUTED)
    m = T(meaning, size, INK)
    row = VGroup(a, e, m).arrange(RIGHT, buff=0.25)
    return boxed(row, color, pad=0.32)


def rule_card(lines, color=VIOLET, size=32, title=None):
    """lines: list of str or mobjects, stacked."""
    rows = VGroup()
    if title:
        rows.add(T(title, size - 4, color, weight=BOLD))
    for l in lines:
        rows.add(T(l, size, INK) if isinstance(l, str) else l)
    rows.arrange(DOWN, buff=0.22)
    return boxed(rows, color, pad=0.36)


def big_word(text, color=VIOLET, size=72):
    return glow(TB(text, size, color), color)


def stamp(text, color=RED_, size=30):
    p = pill(text, color, size, fill=BG)
    p.rotate(-0.12)
    return p


def badge(text, color=WARN, size=22):
    """Small persistent top-right badge."""
    p = pill(text, color, size)
    p.move_to([7.111 - 0.45 - p.width / 2, 3.35, 0])
    return p


# ─────────────── dice and coins ───────────────
PIPS = {1: [(0, 0)], 2: [(-1, 1), (1, -1)], 3: [(-1, 1), (0, 0), (1, -1)], 4: [(-1, 1), (1, 1), (-1, -1), (1, -1)],
        5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)], 6: [(-1, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (1, -1)]}


def die(n, color=ORANGE_, s=0.9, fill=PANEL):
    sq = RoundedRectangle(corner_radius=s * 0.18, width=s, height=s, stroke_color=color, stroke_width=4,
                          fill_color=fill, fill_opacity=1)
    sq.qa_container = True
    g = VGroup(sq)
    for (x, y) in PIPS[n]:
        g.add(Dot(radius=s * 0.075, color=color).move_to(sq.get_center() + np.array([x, y, 0]) * s * 0.26))
    for d in g[1:]:
        d.qa_ignore = True
    g.n = n
    return g


def die_q(color=ORANGE_, s=0.9):
    sq = RoundedRectangle(corner_radius=s * 0.18, width=s, height=s, stroke_color=color, stroke_width=4,
                          fill_color=PANEL, fill_opacity=1)
    sq.qa_container = True
    q = TB("?", int(s * 52), color).move_to(sq)
    return VGroup(sq, q)


def coin(face="H", color=WARN, r=0.42):
    c = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=PANEL, fill_opacity=1)
    c.qa_container = True
    t = TB(face, int(r * 80), color).move_to(c)
    g = VGroup(c, t); g.face = face
    return g


def faces_row(color=ORANGE_, s=0.8, buff=0.3):
    return VGroup(*[die(k, color, s) for k in range(1, 7)]).arrange(RIGHT, buff=buff)


# ─────────────── the 6 x 6 dice grid ───────────────
class DiceGrid(VGroup):
    """Orange die along x (1–6), blue die up y (1–6). cells[(o, b)] are squares (qa_container)."""

    def __init__(self, cell=0.6, fs=24, titles=True):
        super().__init__()
        self.cell_size = cell
        self.ax = Axes(x_range=[0, 6, 1], y_range=[0, 6, 1], x_length=6 * cell, y_length=6 * cell,
                       axis_config=dict(color=INK2, stroke_width=3, include_tip=False, include_ticks=False))
        self.cells = {}
        self.sq = VGroup()
        for b in range(1, 7):
            for o in range(1, 7):
                s = Square(cell * 0.9, stroke_width=0, fill_color=CELL_FILL, fill_opacity=1)
                s.move_to(self.ax.c2p(o - 0.5, b - 0.5)); s.qa_container = True
                self.cells[(o, b)] = s; self.sq.add(s)
        self.xl = VGroup(*[T(str(k), fs, ORANGE_, weight=BOLD).next_to(self.ax.c2p(k - 0.5, 0), DOWN, buff=0.14) for k in range(1, 7)])
        self.yl = VGroup(*[T(str(k), fs, BLUE_, weight=BOLD).next_to(self.ax.c2p(0, k - 0.5), LEFT, buff=0.14) for k in range(1, 7)])
        self.add(self.ax, self.sq, self.xl, self.yl)
        self.titles = VGroup()
        if titles:
            xt = T("orange die", 22, ORANGE_).next_to(self.xl, DOWN, buff=0.12)
            yt = T("blue die", 22, BLUE_).rotate(PI / 2).next_to(self.yl, LEFT, buff=0.12)
            self.titles.add(xt, yt); self.add(self.titles)
        self.nums = VGroup()

    def c(self, o, b):
        return self.cells[(o, b)]

    def where(self, pred):
        return VGroup(*[s for (o, b), s in self.cells.items() if pred(o, b)])

    def sums(self, fs=None, color=INK):
        fs = fs or int(self.cell_size * 40)
        g = VGroup()
        for (o, b), s in self.cells.items():
            t = T(str(o + b), fs, color).move_to(s); t.ob = (o, b); t.set_z_index(3); g.add(t)
        self.nums = g
        return g

    def num(self, o, b):
        for t in self.nums:
            if t.ob == (o, b):
                return t

    def tint(self, pred, color, op=0.85):
        return [self.cells[k].animate.set_fill(color, op) for k in self.cells if pred(*k)]

    def reset(self):
        return [s.animate.set_fill(CELL_FILL, 1) for s in self.cells.values()]


# ─────────────── probability line ───────────────
def prob_line(length=11.0, fs=24, title="how likely", step=0.1, labels=(0, 0.5, 1), percent=False):
    nl = NumberLine(x_range=[0, 1, step], length=length, color=INK2, stroke_width=4, include_tip=False, tick_size=0.1)
    labs = VGroup()
    for v in labels:
        s = f"{int(round(v * 100))}%" if percent else (f"{v:g}")
        labs.add(T(s, fs, INK2).next_to(nl.n2p(v), DOWN, buff=0.18))
    tt = T(title, 24, MUTED).next_to(labs, DOWN, buff=0.15)
    g = VGroup(nl, labs, tt); g.nl, g.labs, g.title = nl, labs, tt
    return g


def pin(nl, v, color=VIOLET, label=None, h=0.75, fs=28, label_dir=UP):
    return marker(nl, v, color, label or "", height=h, fs=fs, label_dir=label_dir)


# ─────────────── trees ───────────────
def tree(root_label, levels, x0=-5.6, dx=3.2, height=4.4, y0=0.0, size=26, colors=None, edge_labels=None):
    """levels: list of lists of branch labels per level (each node splits into all labels of the next level).
    Returns dict(nodes=[[...]], edges=[[...]], leaves=[...], paths=[[labels...]], group)."""
    colors = colors or {}
    root = pill(root_label, INK, size).move_to([x0, y0, 0]) if root_label else Dot(radius=0.08, color=INK2).move_to([x0, y0, 0])
    nodes, edges, labels = [[root]], [], []
    paths = [[]]
    n = 1
    for li, lev in enumerate(levels):
        n *= len(lev)
        gap = height / max(n, 1)
        ys = [y0 + height / 2 - gap * (k + 0.5) for k in range(n)]
        cur, ce, newp = [], [], []
        k = 0
        for pi_, par in enumerate(nodes[-1]):
            for lab in lev:
                col = colors.get(lab, INK)
                nd = pill(lab, col, size).move_to([x0 + dx * (li + 1), ys[k], 0])
                e = Line(par.get_right() + RIGHT * 0.06, nd.get_left() + LEFT * 0.06, color=INK2, stroke_width=3)
                cur.append(nd); ce.append(e); newp.append(paths[pi_] + [lab]); k += 1
        nodes.append(cur); edges.append(ce); paths = newp
    grp = VGroup(root, *[VGroup(*l) for l in nodes[1:]], *[VGroup(*e) for e in edges])
    return dict(nodes=nodes, edges=edges, leaves=nodes[-1], paths=paths, group=grp, root=root)


# ─────────────── charts ───────────────
def bar_axes(xs, y_max, y_step, x_len, y_len, x_title, y_title, fs=26, y_fmt=None):
    """Category bar axes: xs = labels (str), placed at 1..n."""
    n = len(xs)
    ax = Axes(x_range=[0, n + 1, 1], y_range=[0, y_max, y_step], x_length=x_len, y_length=y_len,
              axis_config=dict(color=INK2, stroke_width=3, include_tip=False, tick_size=0.06),
              x_axis_config=dict(include_ticks=False))
    labs = VGroup()
    for i, x in enumerate(xs):
        labs.add(T(str(x), fs, INK2).next_to(ax.c2p(i + 1, 0), DOWN, buff=0.14))
    ylabs = VGroup()
    v = 0
    while v <= y_max + 1e-9:
        s = y_fmt(v) if y_fmt else f"{v:g}"
        ylabs.add(T(s, fs, INK2).next_to(ax.c2p(0, v), LEFT, buff=0.12))
        v += y_step
    xt = T(x_title, 26, MUTED).next_to(labs, DOWN, buff=0.14)
    yt = T(y_title, 26, MUTED).rotate(PI / 2).next_to(ylabs, LEFT, buff=0.2)
    g = VGroup(ax, labs, ylabs, xt, yt); g.ax, g.labs, g.ylabs, g.xt, g.yt = ax, labs, ylabs, xt, yt
    return g


def bars(ax, vals, color=AQUA, width=0.6, op=0.9):
    return VGroup(*[bar(ax, i + 1, v, color, width=width, opacity=op) for i, v in enumerate(vals)])


def line_chart(ax, pts, color=AQUA, width=4):
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners([ax.c2p(x, y) for x, y in pts])


# ─────────────── everyday icons (line art) ───────────────
def ic_cloud(color=BLUE_, s=1.0, rain=True):
    g = VGroup(Circle(0.3 * s).shift(LEFT * 0.28 * s), Circle(0.38 * s).shift(UP * 0.12 * s), Circle(0.28 * s).shift(RIGHT * 0.32 * s))
    base = Line(LEFT * 0.55 * s + DOWN * 0.26 * s, RIGHT * 0.6 * s + DOWN * 0.26 * s)
    g = VGroup(*[Arc(radius=c.radius, start_angle=0.1, angle=PI - 0.2).move_arc_center_to(c.get_center()) for c in g], base)
    if rain:
        for x in (-0.3, 0.05, 0.4):
            g.add(Line(np.array([x, -0.42, 0]) * s, np.array([x - 0.08, -0.65, 0]) * s))
    return g.set_stroke(color, 4)


def ic_sun(color=WARN, s=1.0):
    c = Circle(0.3 * s)
    rays = VGroup(*[Line(np.array([np.cos(a), np.sin(a), 0]) * 0.42 * s, np.array([np.cos(a), np.sin(a), 0]) * 0.6 * s)
                    for a in np.linspace(0, TAU, 9)[:-1]])
    return VGroup(c, rays).set_stroke(color, 4)


def ic_quiz(color=INK2, s=1.0, circled=1):
    sheet = RoundedRectangle(corner_radius=0.06 * s, width=0.9 * s, height=1.15 * s)
    g = VGroup(sheet)
    for k, L in enumerate("ABCD"):
        y = 0.35 - k * 0.24
        g.add(Circle(0.07 * s).move_to(np.array([-0.25, y, 0]) * s))
        g.add(Line(np.array([-0.1, y, 0]) * s, np.array([0.3, y, 0]) * s))
    g.set_stroke(color, 3)
    if circled is not None:
        g[1 + 2 * circled].set_fill(AQUA, 1).set_stroke(AQUA)
    return g


def ic_ticket(color=WARN, s=1.0):
    r = RoundedRectangle(corner_radius=0.08 * s, width=1.1 * s, height=0.6 * s)
    perf = DashedLine(np.array([0.25, 0.3, 0]) * s, np.array([0.25, -0.3, 0]) * s, dash_length=0.05)
    star = Star(5, outer_radius=0.14 * s).shift(LEFT * 0.15 * s)
    return VGroup(r, perf, star).set_stroke(color, 3)


def ic_bus(color=WARN, s=1.0):
    body = RoundedRectangle(corner_radius=0.12 * s, width=1.3 * s, height=0.7 * s)
    w1 = Circle(0.11 * s).move_to(np.array([-0.35, -0.38, 0]) * s)
    w2 = Circle(0.11 * s).move_to(np.array([0.35, -0.38, 0]) * s)
    wins = VGroup(*[Rectangle(width=0.22 * s, height=0.2 * s).move_to(np.array([x, 0.12, 0]) * s) for x in (-0.4, -0.1, 0.2)])
    return VGroup(body, w1, w2, wins).set_stroke(color, 3)


def ic_lock(color=INK2, s=1.0):
    body = RoundedRectangle(corner_radius=0.08 * s, width=0.8 * s, height=0.6 * s).shift(DOWN * 0.15 * s)
    shackle = Arc(radius=0.25 * s, start_angle=0, angle=PI).shift(UP * 0.15 * s)
    kh = Circle(0.06 * s).shift(DOWN * 0.15 * s)
    return VGroup(body, shackle, kh).set_stroke(color, 4)


def ic_book(label, color=INK2, w=0.55, h=1.4):
    r = RoundedRectangle(corner_radius=0.06, width=w, height=h, stroke_color=color, stroke_width=3, fill_color=PANEL, fill_opacity=1)
    r.qa_container = True
    t = TB(label, 34, color).move_to(r)
    if t.width > w - 0.3:
        t.scale_to_fit_width(w - 0.3)
    return VGroup(r, t)


def ic_cake(color=ORANGE_, s=1.0):
    base = Rectangle(width=0.9 * s, height=0.45 * s)
    top = Rectangle(width=0.9 * s, height=0.12 * s).next_to(base, UP, buff=0)
    candle = Line(UP * 0.0, UP * 0.28 * s).next_to(top, UP, buff=0)
    flame = Ellipse(width=0.1 * s, height=0.16 * s).next_to(candle, UP, buff=0.02)
    return VGroup(base, top, candle, flame).set_stroke(color, 3)


def ic_ball(color=ORANGE_, s=1.0):
    c = Circle(0.35 * s)
    return VGroup(c, Line(UP * 0.35 * s, DOWN * 0.35 * s), Line(LEFT * 0.35 * s, RIGHT * 0.35 * s),
                  Arc(radius=0.35 * s, start_angle=-0.7, angle=1.4).shift(LEFT * 0.42 * s)).set_stroke(color, 3)


def ic_jacket(color=BLUE_, s=1.0):
    pts = [(-0.2, 0.45), (0.2, 0.45), (0.5, 0.25), (0.55, -0.45), (-0.55, -0.45), (-0.5, 0.25)]
    body = Polygon(*[np.array([x, y, 0]) * s for x, y in pts])
    zip_ = Line(np.array([0, 0.45, 0]) * s, np.array([0, -0.45, 0]) * s)
    return VGroup(body, zip_).set_stroke(color, 3)


def ic_bottle(color=AQUA, s=1.0):
    b = RoundedRectangle(corner_radius=0.08 * s, width=0.55 * s, height=0.8 * s)
    cap = Rectangle(width=0.4 * s, height=0.18 * s).next_to(b, UP, buff=0.02)
    cr = VGroup(Line(LEFT * 0.12 * s, RIGHT * 0.12 * s), Line(DOWN * 0.12 * s, UP * 0.12 * s)).move_to(b)
    return VGroup(b, cap, cr).set_stroke(color, 3)


def ic_trophy(color=WARN, s=1.0):
    cup = Arc(radius=0.35 * s, start_angle=PI, angle=PI).shift(UP * 0.2 * s)
    rim = Line(LEFT * 0.35 * s, RIGHT * 0.35 * s).shift(UP * 0.2 * s)
    stem = Line(DOWN * 0.15 * s, DOWN * 0.35 * s)
    base = Line(LEFT * 0.25 * s, RIGHT * 0.25 * s).shift(DOWN * 0.38 * s)
    return VGroup(cup, rim, stem, base).set_stroke(color, 3)


def ic_clock(color=INK2, s=1.0):
    c = Circle(0.45 * s)
    h = Line(ORIGIN, UP * 0.3 * s)
    m = Line(ORIGIN, RIGHT * 0.22 * s)
    return VGroup(c, h, m).set_stroke(color, 4)


def ic_bag(color=INK2, s=1.0):
    body = RoundedRectangle(corner_radius=0.3 * s, width=1.6 * s, height=1.5 * s)
    neck = Line(LEFT * 0.45 * s, RIGHT * 0.45 * s).next_to(body, UP, buff=-0.05)
    tie = VGroup(Line(LEFT * 0.15 * s, LEFT * 0.35 * s + UP * 0.2 * s), Line(RIGHT * 0.15 * s, RIGHT * 0.35 * s + UP * 0.2 * s)).next_to(neck, UP, buff=0)
    return VGroup(body, neck, tie).set_stroke(color, 4)


def marble(color, r=0.17):
    m = Circle(r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.95)
    return m


def ic_person(color=INK2, h=0.6):
    return person(color, h)


def ic_calendar(color=INK2, s=1.0):
    r = RoundedRectangle(corner_radius=0.06 * s, width=1.0 * s, height=0.9 * s)
    top = Line(LEFT * 0.5 * s, RIGHT * 0.5 * s).shift(UP * 0.22 * s)
    return VGroup(r, top).set_stroke(color, 3)


def ic_phone(color=INK2, s=1.0):
    r = RoundedRectangle(corner_radius=0.1 * s, width=0.6 * s, height=1.05 * s)
    b = Circle(0.05 * s).shift(DOWN * 0.4 * s)
    return VGroup(r, b).set_stroke(color, 3)


def ic_card(color=INK2, w=0.6, h=0.85, label=None, lc=None):
    r = RoundedRectangle(corner_radius=0.07, width=w, height=h, stroke_color=color, stroke_width=3, fill_color=PANEL, fill_opacity=1)
    r.qa_container = True
    g = VGroup(r)
    if label:
        g.add(T(label, int(h * 34), lc or color, weight=BOLD).move_to(r))
    return g


def spinner(parts, r=1.3, start=PI / 2):
    """parts: list of (fraction, colour). Returns VGroup of sectors + outline."""
    g = VGroup()
    a = start
    for f, col in parts:
        sec = Sector(radius=r, start_angle=a, angle=-TAU * f, fill_color=col, fill_opacity=0.75, stroke_color=BG, stroke_width=3)
        sec.qa_container = True
        g.add(sec); a -= TAU * f
    g.add(Circle(r, stroke_color=INK2, stroke_width=3))
    return g


def unit_grid(n_cols, n_rows, cell=0.3, fill=CELL_FILL):
    g = VGroup()
    for r in range(n_rows):
        for c in range(n_cols):
            s = Square(cell * 0.86, stroke_width=0, fill_color=fill, fill_opacity=1).move_to(RIGHT * c * cell + DOWN * r * cell)
            s.rc = (r, c); g.add(s)
    return g.center()


def arrow(a, b, color=INK2, sw=4):
    return Arrow(a, b, color=color, stroke_width=sw, buff=0.15, max_tip_length_to_length_ratio=0.15)
