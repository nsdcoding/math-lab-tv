"""Confusion-matrix building blocks shared by all scenes of this video.

Colour roles (kept for the whole video):
  precision / the alarm column = VIOLET · recall / the real row = ORANGE_ · correct diagonal (TP, TN) = AQUA
  false positive = ORANGE_ tint · false negative = BLUE_ tint · accuracy = WARN (gold) · traps = RED_

Layout (default grid, scale 0.9): cells span x -4.1 … 1.1 and y -1.98 … 1.08; column labels above, row labels left.
Everything keeps clear of the chapter-label corner (x < -3.26, y > 2.98) and the subtitles (y < -2.70).
"""
from common import *

KEYS = ("TP", "FN", "FP", "TN")


def highlight(*mobs, color=WARN):
    """Still highlight, never a bounce: an underline under text, a thin ring around small things, and a rounded
    frame around anything bigger (never a brace, which can cross nearby labels). Drawn, held, faded."""
    anims = []
    for m in mobs:
        w, h = m.width, m.height
        if isinstance(m, (Text, MathTex)) or (h < 0.75 and w > 0.75):
            mk = Line(m.get_corner(DL) + DOWN * 0.1, m.get_corner(DR) + DOWN * 0.1).set_stroke(color, 5)
        elif w < 0.75 and h < 0.75:
            mk = Circle(radius=max(w, h) * 0.75 + 0.08).move_to(m).set_stroke(color, 4)
        else:
            mk = RoundedRectangle(corner_radius=0.18, width=w + 0.16, height=h + 0.16).move_to(m).set_stroke(color, 5)
        for x in mk.get_family():
            x.qa_ignore = True
        anims.append(Succession(Create(mk, run_time=0.45), Wait(0.35), FadeOut(mk, run_time=0.3)))
    return AnimationGroup(*anims)          # row-major: top row (real positive) = TP, FN; bottom row = FP, TN
NAMES = {"TP": "TRUE POSITIVE", "FN": "FALSE NEGATIVE", "FP": "FALSE POSITIVE", "TN": "TRUE NEGATIVE"}
NICK = {"TP": "caught", "FN": "missed", "FP": "false alarm", "TN": "left alone"}
COL = {"TP": AQUA, "TN": AQUA, "FP": ORANGE_, "FN": BLUE_}
CELL_FILL = "#22221f"
FRAUD_DOT = RED_          # a fraud payment
FINE_DOT = INK2           # a normal payment


def fmt(n):
    return f"{n:,}"


def tint(color, a=0.16):
    return interpolate_color(ManimColor(CELL_FILL), ManimColor(color), a)


def _lab(text, size, color, **kw):
    """Text, or an invisible placeholder for an empty label (keeps the layout maths working)."""
    if text:
        return T(text, size, color, **kw)
    t = T("x", size, color, **kw).set_opacity(0)
    t.qa_ignore = True
    return t


class Grid(VGroup):
    """A 2×2 confusion matrix with row/column labels and axis titles.

    g.cell[k]  rounded box of cell k (k in KEYS)       g.num[k]   its count (Text, may be empty)
    g.name[k]  the cell's name ("TRUE POSITIVE")        g.rowlab / g.collab / g.rowtitle / g.coltitle
    """

    def __init__(self, rows=("really fraud", "really fine"), cols=("alarm", "quiet"), counts=None,
                 names=True, cw=2.9, chh=1.7, row_title="the truth", col_title="what it said",
                 num_size=60, name_size=20, label_size=28, show_lit=False):
        super().__init__()
        self.cw, self.chh = cw, chh
        self.counts = dict(counts or {})
        self.num_size, self.name_size = num_size, name_size
        self.cell, self.num, self.name = {}, {}, {}
        pos = {"TP": (0, 0), "FN": (1, 0), "FP": (0, 1), "TN": (1, 1)}
        self.cells = VGroup()
        for k in KEYS:
            c, r = pos[k]
            box = RoundedRectangle(corner_radius=0.14, width=cw - 0.1, height=chh - 0.1,
                                   stroke_color=COL[k] if show_lit else GRID, stroke_width=3,
                                   fill_color=tint(COL[k]) if show_lit else CELL_FILL, fill_opacity=1)
            box.qa_container = True
            box.move_to(np.array([(c + 0.5) * cw, -(r + 0.5) * chh, 0]))
            self.cell[k] = box
            self.cells.add(box)
        self.add(self.cells)
        self.names = VGroup()
        for k in KEYS:
            nm = T(NAMES[k], name_size, COL[k], weight=BOLD)
            nm.move_to(self.cell[k].get_top() + DOWN * (0.12 + nm.height / 2 + 0.06))
            nm.set_opacity(1 if names else 0)
            self.name[k] = nm
            self.names.add(nm)
        self.add(self.names)
        self.nums = VGroup()
        for k in KEYS:
            t = self._num_text(k, self.counts.get(k))
            self.num[k] = t
            self.nums.add(t)
        self.add(self.nums)
        # labels
        top = self.cells.get_top()[1]
        self.collab = VGroup(*[_lab(cols[i], label_size, INK, weight=BOLD).move_to(
            np.array([(i + 0.5) * cw, top + 0.42, 0])) for i in range(2)])
        self.coltitle = _lab(col_title, 24, MUTED).move_to(np.array([cw, top + 0.95, 0]))
        left = self.cells.get_left()[0]
        self.rowlab = VGroup(*[_lab(rows[i], label_size, INK, weight=BOLD) for i in range(2)])
        for i, t in enumerate(self.rowlab):
            t.move_to(np.array([left - 0.4 - t.width / 2, -(i + 0.5) * chh, 0]))
        self.rowtitle = _lab(row_title, 24, MUTED)
        self.rowtitle.move_to(np.array([self.rowlab.get_center()[0], top + 0.42, 0]))
        self.rowtitle.align_to(self.rowlab, RIGHT)
        self.add(self.collab, self.coltitle, self.rowlab, self.rowtitle)

    def _num_text(self, k, v, color=None):
        txt = "" if v is None else (v if isinstance(v, str) else fmt(v))
        sc = self.cell[k].width / (self.cw - 0.1)          # the grid may have been scaled after it was built
        t = TB(txt if txt else "0", self.num_size, color or INK).scale(sc)
        if not txt:
            t.set_opacity(0)
        box = self.cell[k]
        name_h = self.name[k].height if k in self.name else 0.3
        t.move_to(box.get_center() + DOWN * (name_h / 2 + 0.06))
        return t

    def set_num(self, k, v, color=None):
        """Animation: the count of cell k becomes v (a number or a short string)."""
        new = self._num_text(k, v, color)
        old = self.num[k]
        self.num[k] = new
        self.nums.submobjects[KEYS.index(k)] = new
        self.counts[k] = v
        return ReplacementTransform(old, new)

    # handy regions
    def col0(self):
        return VGroup(self.cell["TP"], self.cell["FP"])

    def row0(self):
        return VGroup(self.cell["TP"], self.cell["FN"])

    def row1(self):
        return VGroup(self.cell["FP"], self.cell["TN"])

    def frame_of(self, mob, color, width=6, pad=0.09):
        """A highlight frame around part of the grid (deliberately drawn round the cells: qa_ignore)."""
        pad = pad * min(1.0, self.cell["TP"].width / (self.cw - 0.1))     # keep frames tight on small grids
        r = RoundedRectangle(corner_radius=0.2, width=mob.width + 2 * pad, height=mob.height + 2 * pad,
                             stroke_color=color, stroke_width=width, fill_opacity=0).move_to(mob)
        r.qa_ignore = True   # highlight box around cells on purpose
        return r

    def light(self, k, color=None, a=0.22):
        """Animation: tint cell k with its colour (border + soft fill), never covering the number."""
        c = color or COL[k]
        return self.cell[k].animate.set_stroke(c, 4).set_fill(tint(c, a), 1)

    def unlight(self, k):
        return self.cell[k].animate.set_stroke(GRID, 3).set_fill(CELL_FILL, 1)

    def fade_cells(self, keys, op=0.22):
        """Animations fading cells (box + name + number) to op; op=1 restores."""
        out = []
        for k in keys:
            out += [self.cell[k].animate.set_opacity(op), self.name[k].animate.set_opacity(op if self.name[k].get_fill_opacity() > 0 or op == 1 else 0)]
            if self.counts.get(k) is not None:
                out.append(self.num[k].animate.set_opacity(op))
        return out


def grid_at(scale=0.9, center=None, **kw):
    """A Grid placed in the standard spot (cells x -4.1…1.1, y -1.98…1.08) or centred on `center` (cells' centre)."""
    g = Grid(**kw)
    g.scale(scale)
    target = center if center is not None else np.array([-1.5, -0.45, 0])
    g.shift(target - g.cells.get_center())
    return g


def formula(tex_parts, colors, size=52):
    """MathTex from parts with per-part colours."""
    m = MathTex(*tex_parts, font_size=size)
    for i, c in enumerate(colors):
        if c:
            m[i].set_color(c)
    return m


def under_labels(m, pairs, size=22, buff=0.28):
    """Plain-word labels under parts of a MathTex: pairs = [(part index, text, colour)]. Returns VGroup."""
    g = VGroup()
    for i, txt, c in pairs:
        t = T(txt, size, c).next_to(m[i], DOWN, buff=buff)
        g.add(t)
    # spread apart if two labels touch
    for _ in range(3):
        for a, b in zip(g[:-1], g[1:]):
            gap = b.get_left()[0] - a.get_right()[0]
            if gap < 0.25:
                b.shift(RIGHT * (0.25 - gap) / 2); a.shift(LEFT * (0.25 - gap) / 2)
    return g


def field_squares(cols, rows, cell, fill=0.78, color=FINE_DOT, opacity=0.85, skip=()):
    """One VMobject holding many small squares (fast to draw); `skip` = set of (c, r) left empty."""
    s = cell * fill
    m = VMobject(stroke_width=0, fill_color=color, fill_opacity=opacity)
    pts = []
    sk = set(skip)
    for r in range(rows):
        for c in range(cols):
            if (c, r) in sk:
                continue
            x, y = c * cell, -r * cell
            sq = [np.array([x, y, 0]), np.array([x + s, y, 0]), np.array([x + s, y - s, 0]), np.array([x, y - s, 0])]
            m.start_new_path(sq[0])
            m.add_points_as_corners(sq[1:] + [sq[0]])
    m.qa_ignore = True     # texture, never sits under text
    return m


def squares(n, cols, cell, color, fill=0.8, opacity=0.95):
    """n separate countable squares in rows of `cols` (top-left first)."""
    g = VGroup()
    for k in range(n):
        c, r = k % cols, k // cols
        g.add(Square(cell * fill, stroke_width=0, fill_color=color, fill_opacity=opacity).move_to(
            np.array([c * cell, -r * cell, 0])))
    return g


def payment_card(color=INK2, w=1.0, fraud=False):
    """A tiny bank-card icon (generic, no branding)."""
    b = RoundedRectangle(corner_radius=0.08 * w, width=w, height=0.63 * w).set_stroke(color, 3).set_fill("#22221f", 1)
    chip_ = RoundedRectangle(corner_radius=0.03 * w, width=0.18 * w, height=0.14 * w).set_stroke(width=0).set_fill(WARN, 1)
    chip_.move_to(b.get_corner(UL) + np.array([0.22 * w, -0.2 * w, 0]))
    stripe = Line(b.get_left() + RIGHT * 0.12 * w + DOWN * 0.12 * w, b.get_right() + LEFT * 0.4 * w + DOWN * 0.12 * w).set_stroke(MUTED, 3)
    g = VGroup(b, chip_, stripe)
    if fraud:
        corner = Triangle(fill_color=RED_, fill_opacity=1, stroke_width=0).scale(0.12 * w).rotate(-PI / 4)
        corner.move_to(b.get_corner(UR) + np.array([-0.1 * w, -0.1 * w, 0]))
        g.add(corner)
    for x in g.get_family():
        x.qa_ignore = True     # icon parts; labels are placed beside it, never on it
    return g


def bell(color=VIOLET, s=0.5):
    body = VMobject().set_points_smoothly([np.array(p) * s for p in
                                           [(-0.5, -0.35, 0), (-0.38, 0.1, 0), (-0.25, 0.42, 0), (0, 0.52, 0), (0.25, 0.42, 0),
                                            (0.38, 0.1, 0), (0.5, -0.35, 0)]])
    body.add_line_to(np.array([-0.5, -0.35, 0]) * s)
    body.set_stroke(color, 3).set_fill(color, 0.85)
    clap = Circle(0.09 * s * 1.6).set_stroke(width=0).set_fill(color, 1).move_to(np.array([0, -0.47, 0]) * s)
    g = VGroup(body, clap)
    for x in g: x.qa_ignore = True
    return g


def phone(color=INK2, s=0.5):
    b = RoundedRectangle(corner_radius=0.08 * s, width=0.55 * s, height=1.0 * s).set_stroke(color, 3).set_fill("#22221f", 1)
    sp = Line(b.get_top() + DOWN * 0.1 * s + LEFT * 0.1 * s, b.get_top() + DOWN * 0.1 * s + RIGHT * 0.1 * s).set_stroke(color, 3)
    g = VGroup(b, sp)
    for x in g: x.qa_ignore = True
    return g


def envelope(color=INK2, s=1.0):
    b = Rectangle(width=0.62 * s, height=0.42 * s).set_stroke(color, 3).set_fill("#22221f", 1)
    f = VMobject().set_points_as_corners([b.get_corner(UL), b.get_center() + DOWN * 0.04 * s, b.get_corner(UR)]).set_stroke(color, 2.5)
    g = VGroup(b, f)
    for x in g: x.qa_ignore = True
    return g


def detector_box(label, color=INK2, w=3.2, h=1.6):
    """A closed 'detector' box with its name on the front."""
    b = card(w, h, color)
    t = TB(label, 34, color).move_to(b)
    g = VGroup(b, t); g.box, g.text = b, t
    return g


def bars_axes(n_groups, labels, y_max=100, step=25, x_len=5.2, y_len=3.6, title="percent", fs=22):
    """Axes for small grouped bar charts: x has n_groups slots labelled with `labels`."""
    g = xy_axes([0, n_groups, 1], [0, y_max, step], x_len, y_len, None, title,
                x_labels={}, font_size=fs)
    labs = VGroup()
    for i, l in enumerate(labels):
        t = T(l, 24, INK, weight=BOLD).next_to(g.ax.c2p(i + 0.5, 0), DOWN, buff=0.2)
        labs.add(t)
    g.add(labs); g.slot_labels = labs
    return g


def vbar(ax, x, v, color, width=0.45, opacity=0.9):
    r = Rectangle(width=width, height=max(1e-3, ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), stroke_width=0,
                  fill_color=color, fill_opacity=opacity)
    return r.move_to(ax.c2p(x, 0), aligned_edge=DOWN)


def value_label(bar_, text, color, size=24):
    return T(text, size, color, weight=BOLD).next_to(bar_, UP, buff=0.12)


def side_card(lines, color=INK2, size=30, w=None, title=None, title_color=None, align=LEFT):
    """A card with optional bold title and lines of text, sized from its text."""
    rows = []
    if title:
        rows.append(TB(title, int(size * 1.15), title_color or color))
    for l in lines:
        rows.append(l if isinstance(l, Mobject) else T(l, size, INK))
    inner = VGroup(*rows).arrange(DOWN, buff=0.2, aligned_edge=align)
    box = card(max(w or 0, inner.width + 0.7), inner.height + 0.6, color)
    inner.move_to(box)
    g = VGroup(box, inner); g.box, g.inner = box, inner
    return g


def ratio(label, num, den, lcol=INK, ncol=INK, dcol=INK, size=46):
    """'label =' in Inter next to a LaTeX fraction num/den (both plain-text parts)."""
    lab = T(f"{label} =", size * 0.72, lcol, weight=BOLD)
    fr = MathTex(r"{\text{" + num + r"}", r"\over", r"\text{" + den + r"}}", font_size=size)
    fr[0].set_color(ncol); fr[2].set_color(dcol); fr[1].set_color(INK2)
    g = VGroup(lab, fr).arrange(RIGHT, buff=0.25)
    g.lab, g.fr = lab, fr
    return g


def nfrac(a, b, color=INK, size=60):
    return MathTex(r"{\text{" + a + r"}", r"\over", r"\text{" + b + r"}}", font_size=size, color=color)


def seq(*parts, size=40, buff=0.22):
    """A row of (text, colour) parts in Inter bold, e.g. seq(("90", AQUA), ("+", INK2), ...)."""
    return VGroup(*[T(t, size, c, weight=BOLD) for t, c in parts]).arrange(RIGHT, buff=buff)


TITLE = ("CONFUSION MATRIX", "accuracy · precision · recall")


def the_title():
    """Identical title card at the end of the hook and the start of the welcome (seamless cut)."""
    return title_card(*TITLE, size=88)

PANEL_X = 4.4           # centre of the right-hand panel next to the default grid (cells end at x = 1.1)
A_COUNTS = dict(TP=90, FN=10, FP=30, TN=9870)
B_COUNTS = dict(TP=45, FN=55, FP=5, TN=9895)
C_COUNTS = dict(TP=99, FN=1, FP=301, TN=9599)


def panel_eq(parts, y, size=30, dx=0.0):
    """An equation row in the right panel: parts = [(text, colour)], centred on PANEL_X (+dx) at height y."""
    return seq(*parts, size=size).move_to(RIGHT * (PANEL_X + dx) + UP * y)


def stacked_bar(parts, length=3.8, h=0.5):
    """Horizontal bar split into parts [(value, colour)], scaled to `length` in total."""
    tot = sum(v for v, _ in parts)
    g = VGroup()
    x = 0
    for v, c in parts:
        w = max(0.012, length * v / tot)
        r = Rectangle(width=w, height=h).set_stroke(width=0).set_fill(c, 0.9).move_to(RIGHT * (x + w / 2))
        g.add(r); x += w
    return g


def mini_grid(counts, s=0.45, center=ORIGIN, rows=("fraud", "fine"), cols=("alarm", "quiet"), lit=True):
    """A small labelled grid for side panels (no cell names; labels enlarged so they stay readable)."""
    g = Grid(counts=counts, names=False, rows=rows, cols=cols, row_title="", col_title="", num_size=58, label_size=44,
             show_lit=lit)
    g.scale(s)
    g.shift(center - g.cells.get_center())
    return g


def show_grid(scene, g, with_nums=True):
    scene.add(g.cells, g.collab, g.coltitle, g.rowlab, g.rowtitle)
    if any(n.get_fill_opacity() > 0 for n in g.names):
        scene.add(g.names)
    if with_nums:
        scene.add(*[g.num[k] for k in KEYS if g.counts.get(k) is not None])


def grid_mobs(g):
    return VGroup(g.cells, g.names, g.collab, g.coltitle, g.rowlab, g.rowtitle,
                  *[g.num[k] for k in KEYS if g.counts.get(k) is not None])
