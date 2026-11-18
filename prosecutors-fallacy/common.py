"""Shared style, timing and QA helpers for all scenes."""
import json, pathlib, os
import numpy as np
from math import comb
from manim import *

HERE = pathlib.Path(__file__).parent
TIM = json.loads((HERE / "timings.json").read_text())
SEGS = {s["id"]: s for s in TIM["segments"]}
ORDER = [s["id"] for s in TIM["segments"]]
CHAPTERS = []
for s in TIM["segments"]:
    if not CHAPTERS or CHAPTERS[-1]["name"] != s["chapter"]:
        CHAPTERS.append(dict(name=s["chapter"], first=s["id"], segs=[]))
    CHAPTERS[-1]["segs"].append(s["id"])
# scene windows: chapter k runs from (first start of k, or 0) to first start of k+1 (or total)
for k, c in enumerate(CHAPTERS):
    c["t0"] = 0.0 if k == 0 else SEGS[c["first"]]["start"] - 0.25
for k, c in enumerate(CHAPTERS):
    c["t1"] = CHAPTERS[k + 1]["t0"] if k + 1 < len(CHAPTERS) else TIM["total"]

# ── palette ──
BG = "#1a1a19"
BLUE_ = "#3987e5"; ORANGE_ = "#d95926"; AQUA = "#199e70"; VIOLET = "#9085e9"
WARN = "#fab219"; RED_ = "#d03b3b"; INK = "#f0efec"; INK2 = "#c3c2b7"; MUTED = "#898781"
GRID = "#3a3a37"
config.background_color = BG
config.frame_rate = 30
config.pixel_width, config.pixel_height = 1920, 1080

FONT, FONT_D = "Inter", "Inter Display"

# ── safe area (in screen units relative to camera frame, frame = 14.222 x 8) ──
# subtitles occupy the bottom 175 px; chapter label occupies top-left 520x110 px
PX = 8 / 1080
SAFE_BOTTOM = -4 + 175 * PX          # content must stay above this
EDGE = 40 * PX                         # text keeps >= 40 px from the frame border
BOX_PAD = 10 * PX                      # text keeps >= 10 px from the border of its box
LABEL_BOX = (-7.111, 4 - 110 * PX, -7.111 + 520 * PX, 4)  # x0, y0, x1, y1


def T(text, size=36, color=INK, weight=NORMAL, display=False, **kw):
    return Text(text, font=FONT_D if display else FONT, font_size=size, color=color, weight=weight, **kw)


def TB(text, size=48, color=INK, **kw):
    return T(text, size=size, color=color, weight=BOLD, display=True, **kw)


def glow(mob, color=None, layers=6, width=14, opacity=0.06):
    """Return VGroup(glow layers..., mob). Glow is built from copies of mob, so it moves,
    scales and fades with the group. Always animate the returned group, never mob alone."""
    color = color or mob.get_color()
    g = VGroup()
    for i in range(layers, 0, -1):
        c = mob.copy().set_fill(opacity=0).set_stroke(color, width=width * i / layers, opacity=opacity)
        g.add(c)
    grp = VGroup(g, mob)
    grp.is_glow_group = True
    for m in g.family_members_with_points():
        m.qa_ignore = True
    return grp


def dot(color=BLUE_, r=0.13):
    d = Dot(radius=r, color=color).set_stroke(BG, 2)
    d.qa_dot = True
    return d


def chip(text, color=INK, size=30, fill=None, pad=0.22):
    t = T(text, size=size, color=color)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 2 * pad, height=t.height + 1.5 * pad,
                           stroke_color=color, stroke_width=2, fill_color=fill or BG, fill_opacity=1)
    t.move_to(box)
    g = VGroup(box, t)
    box.qa_container = True
    return g


class Base(MovingCameraScene):
    """Timing-driven scene. self.at(id, dt) waits until segment `id` starts (+dt)."""
    CHAPTER = None

    def setup(self):
        super().setup()
        self.ch = next(c for c in CHAPTERS if c["name"] == self.CHAPTER)
        self.t0 = self.ch["t0"]
        self.qa_log = []
        self.camera.frame.save_state()
        self._idle, self._idle_k = [], 0

    # time on the global timeline
    def now(self):
        return self.t0 + self.renderer.time

    def at(self, sid, dt=0.0):
        self.until(SEGS[sid]["start"] + dt)

    def word(self, sid, w, dt=-0.15, nth=0):
        """Wait until the nth occurrence of word w in segment sid is spoken (+dt)."""
        ws = [x.strip(",.;:?!'").lower() for x in SEGS[sid]["text"].split()]
        idx = [i for i, x in enumerate(ws) if x == w.lower().strip(",.;:?!'")][nth]
        self.until(word_time(sid, idx) + dt)

    def idle(self, *makers):
        """Idle actors: callables that return one short Animation tied to what is on screen (a coin flip, a friend
        dropping into the chart, a glint along the key object). Every wait longer than ~0.9 s is filled with them
        in turn, so the screen never sits still. idle() with no arguments clears them."""
        self._idle, self._idle_k = list(makers), 0

    def seg_end(self, sid):
        return SEGS[sid]["end"]

    def until(self, t_global):
        w = t_global - self.now()
        while w > 0.5:
            if self._idle:
                mk = self._idle[self._idle_k % len(self._idle)]
                self._idle_k += 1
                anim = mk()
            else:      # fallback: the newest thing on screen breathes, so a wait is never a frozen frame
                f = self._focus_alive()
                if f is None:
                    break
                anim = pulse(f, s=1.1 if f.width < 6 else 1.04)
            rt = w - 0.02 if w < 1.7 else 0.85
            self.play(anim, run_time=rt)
            w = t_global - self.now()
        if w > 1 / 30:
            self.wait(w)

    def finish(self):
        self.until(self.ch["t1"])

    def qa_mute(self, mob, on=True):
        """Exclude mobjects hidden under an opaque overlay from the overlap checks (and re-include them)."""
        for m in mob.get_family():
            m.qa_ignore = on

    def drop(self, *ms):
        """Remove mobjects and every member of their families from the scene."""
        fam = []
        for m in ms:
            fam += m.get_family()
        self.remove(*fam)

    def play(self, *a, **k):
        before = list(self.mobjects)
        fam_before = {id(x) for m in before for x in m.get_family()}
        super().play(*a, **k)
        self._restore_order(before, fam_before)
        def _op(m):
            pts = [x for x in m.family_members_with_points() if isinstance(x, VMobject)]
            return max([x.get_fill_opacity() for x in pts] + [x.get_stroke_opacity() for x in pts] + [0])
        new = [m for m in self.mobjects if id(m) not in fam_before and
               (isinstance(m, ImageMobject) or (isinstance(m, VMobject) and m.width * m.height > 0.15 and _op(m) > 0.3))]
        if new:
            self._focus = max(new, key=lambda m: m.width * m.height)
        self.qa_check()

    def _focus_alive(self):
        f = getattr(self, "_focus", None)
        fam = {id(x) for m in self.mobjects for x in m.get_family()}
        if f is None or id(f) not in fam:
            f = VMobject()   # gone: fall through to the largest visible object
        _p = [x for x in f.family_members_with_points() if isinstance(x, VMobject)]
        op = max([x.get_fill_opacity() for x in _p] + [x.get_stroke_opacity() for x in _p] + [0]) \
            if not isinstance(f, ImageMobject) else 1
        if op > 0.3 and f.width * f.height >= 1.0:
            return f
        # the newest thing is gone or tiny: use the largest clearly visible object on screen
        def vis(m):
            if isinstance(m, ImageMobject):
                return 1
            pts = [x for x in m.family_members_with_points() if isinstance(x, VMobject)]
            return max([x.get_fill_opacity() for x in pts] + [x.get_stroke_opacity() for x in pts] + [0])
        cand = [m for m in self.mobjects if vis(m) > 0.3 and m.width * m.height > 0.3
                and not all(getattr(x, "qa_ignore", False) for x in m.family_members_with_points() or [m])]
        return max(cand, key=lambda m: m.width * m.height) if cand else None

    def add_mobjects_from_animations(self, animations):
        """Like Manim's, but looks inside AnimationGroups: their wrapper Group is never added, so animating
        mobjects that already sit inside a group cannot pull them out of it and redraw them on top."""
        curr = self.get_mobject_family_members()
        curr_ids = {id(x) for x in curr}
        def leaves(an):
            if isinstance(an, AnimationGroup):
                for x in an.animations:
                    yield from leaves(x)
            else:
                yield an
        for an in animations:
            for x in leaves(an):
                if x.is_introducer():
                    continue
                m = x.mobject
                if m is None or id(m) in curr_ids:
                    continue
                sub = m.get_family()[1:]
                if sub and not x.remover and not getattr(x, "replace_mobject_with_target_in_scene", False) \
                        and all(id(s_) in curr_ids for s_ in sub):
                    continue      # a temporary group around mobjects already on screen: animate them where they are
                self.add(m)
                curr_ids |= {id(s_) for s_ in m.get_family()}

    def _restore_order(self, before, fam_before):
        """Animating mobjects that already sit inside a group (LaggedStart/AnimationGroup of pulses, Indicates…)
        makes Manim split that group and re-add the pieces on top, so filled cards end up drawn over their own
        labels. Put the scene back in its original drawing order, keeping anything removed or newly added."""
        after = list(self.mobjects)
        fam_after = {id(x) for m in after for x in m.get_family()}
        out, placed = [], set()
        def put(m):
            fam = {id(x) for x in m.get_family()}
            if fam <= placed:
                return
            if fam & placed:                  # partly placed already: place the missing pieces one by one
                for s_ in m.submobjects:
                    put(s_)
                if id(m) not in placed and not m.submobjects:
                    out.append(m); placed.add(id(m))
                return
            out.append(m); placed.update(fam)
        for m in before:
            fam = m.get_family()
            if all(id(x) in fam_after for x in fam):
                put(m)                                             # whole and still on screen
            else:
                ids = {id(x) for x in fam}
                for x in after:                                   # partly removed: keep its surviving pieces
                    if id(x) in ids:
                        put(x)
        for m in after:
            if id(m) in fam_before and m not in before:
                continue                                          # a piece of an old group: already placed
            if id(m) not in fam_before and type(m) in (Group, VGroup) and any(id(s) in fam_before for s in m.submobjects):
                for s_ in m.submobjects:                          # a wrapper made by an AnimationGroup
                    if id(s_) not in fam_before:
                        put(s_)
            else:
                put(m)
        self.mobjects = out

    # ── QA: overlap checker run after every animation ──
    def _texts(self):
        out = []
        for m in self.mobjects:
            for sub in m.get_family():
                if isinstance(sub, (Text, MathTex, Tex, MarkupText)) and not getattr(sub, "qa_ignore", False):
                    op = max([x.get_fill_opacity() for x in sub.family_members_with_points()] or [0])
                    if op > 0.3 and sub.width > 0.02:
                        out.append(sub)
        # dedupe (MathTex families include SingleStringMathTex parts)
        seen, res = set(), []
        for t in out:
            if id(t) in seen: continue
            for s in t.get_family()[1:]: seen.add(id(s))
            res.append(t)
        return [t for t in res if id(t) not in seen]

    def _screen_box(self, m):
        f = self.camera.frame
        s = 8 / f.height
        c = f.get_center()
        (x0, y0, _), (x1, y1, _) = m.get_corner(DL), m.get_corner(UR)
        return ((x0 - c[0]) * s, (y0 - c[1]) * s, (x1 - c[0]) * s, (y1 - c[1]) * s)

    def qa_check(self):
        t = round(self.now(), 2)
        texts = self._texts()
        boxes = [(m, self._screen_box(m)) for m in texts]
        W, H = 7.111, 4.0
        def name(m):
            return getattr(m, "text", None) or getattr(m, "tex_string", None) or type(m).__name__
        for m, (x0, y0, x1, y1) in boxes:
            if x1 < -W or x0 > W or y1 < -H or y0 > H:
                continue  # fully off-screen
            if (x0 < -W + 0.05 or x1 > W - 0.05 or y1 > H - 0.05 or y0 < -H + 0.05) and not getattr(m, "qa_clip_ok", False):
                self.qa_log.append(dict(t=t, kind="clipped", a=name(m)))
            elif x0 < -W + EDGE or x1 > W - EDGE or y1 > H - EDGE:
                self.qa_log.append(dict(t=t, kind="near_frame_edge", a=name(m)))
            if y0 < SAFE_BOTTOM:
                self.qa_log.append(dict(t=t, kind="under_subtitles", a=name(m)))
            lx0, ly0, lx1, ly1 = LABEL_BOX
            if x0 < lx1 and y1 > ly0:
                self.qa_log.append(dict(t=t, kind="chapter_corner", a=name(m)))
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                (a, A), (b, B) = boxes[i], boxes[j]
                ox = min(A[2], B[2]) - max(A[0], B[0]); oy = min(A[3], B[3]) - max(A[1], B[1])
                if ox > -0.06 and oy > -0.06:  # boxes closer than ~8 px count as touching
                    self.qa_log.append(dict(t=t, kind="text_text", a=name(a), b=name(b)))
        # text vs solid shapes (filled, not a container/background of that text)
        shapes = []
        for m in self.mobjects:
            for sub in m.get_family():
                if (isinstance(sub, VMobject) and not isinstance(sub, (Text, MathTex, Tex, MarkupText))
                        and sub.get_fill_opacity() > 0.5 and not getattr(sub, "qa_container", False)
                        and not getattr(sub, "qa_ignore", False) and len(sub.points) > 0
                        and not any(isinstance(p, (Text, MathTex, Tex)) for p in [sub])
                        and sub.get_fill_color().to_hex().lower() != BG.lower()):
                    shapes.append(sub)
        textfam = set()
        for m in texts:
            for s in m.get_family(): textfam.add(id(s))
        textfam_all = set()
        for m in self.mobjects:
            for sub in m.get_family():
                if isinstance(sub, (Text, MathTex, Tex, MarkupText)):
                    for s2 in sub.get_family(): textfam_all.add(id(s2))
        # text crossed by strokes (lines, arrows, curves, outlines): sample points along each stroke path
        strokes = []
        for m in self.mobjects:
            for sub in m.get_family():
                if (isinstance(sub, VMobject) and not isinstance(sub, (Text, MathTex, Tex, MarkupText))
                        and len(sub.points) >= 4 and sub.get_stroke_width() > 0.5 and sub.get_stroke_opacity() > 0.3
                        and not getattr(sub, "qa_container", False) and not getattr(sub, "qa_ignore", False)
                        and id(sub) not in textfam_all and sub.get_stroke_color().to_hex().lower() != BG.lower()):
                    strokes.append(sub)
        f = self.camera.frame; sc = 8 / f.height; cc = f.get_center()
        ts_ = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
        for st in strokes:
            P = st.points[: len(st.points) // 4 * 4].reshape(-1, 4, 3)
            pts = (((1 - ts_)[None, :, None] ** 3 * P[:, None, 0] + 3 * ((1 - ts_) ** 2 * ts_)[None, :, None] * P[:, None, 1]
                    + 3 * ((1 - ts_) * ts_ ** 2)[None, :, None] * P[:, None, 2] + (ts_ ** 3)[None, :, None] * P[:, None, 3]))
            pts = (pts.reshape(-1, 3)[:, :2] - cc[:2]) * sc
            for a, A in boxes:
                m = -0.02   # a stroke within ~3 px of a label's box counts as touching it
                inside = ((pts[:, 0] > A[0] + m) & (pts[:, 0] < A[2] - m) & (pts[:, 1] > A[1] + m) & (pts[:, 1] < A[3] - m))
                if inside.any():
                    self.qa_log.append(dict(t=t, kind="text_stroke", a=name(a), b=type(st).__name__))
        # text touching the border of the box/chip/card it sits in
        conts = []
        for m in self.mobjects:
            for sub in m.get_family():
                if getattr(sub, "qa_container", False) and not getattr(sub, "qa_ignore", False) and len(sub.points) > 0 \
                        and max(sub.get_fill_opacity(), sub.get_stroke_opacity()) > 0.3:
                    conts.append(sub)
        for c_ in conts:
            C = self._screen_box(c_)
            for a, A in boxes:
                cx, cy = (A[0] + A[2]) / 2, (A[1] + A[3]) / 2
                if not (C[0] < cx < C[2] and C[1] < cy < C[3]):
                    continue
                if (A[2] - A[0]) > (C[2] - C[0]) * 0.98 and (A[3] - A[1]) > (C[3] - C[1]) * 0.98:
                    continue  # text bigger than the box: not its container
                sc_ = 8 / self.camera.frame.height
                pad = BOX_PAD * min(1.0, sc_)
                if A[0] - C[0] < pad or C[2] - A[2] < pad or A[1] - C[1] < pad * 0.6 or C[3] - A[3] < pad * 0.6:
                    self.qa_log.append(dict(t=t, kind="text_box_border", a=name(a), b=type(c_).__name__))
        # marker heads (mean triangle / median diamond) sitting on dots
        fam = [sub for m in self.mobjects for sub in m.get_family()]
        heads = [h for h in fam if getattr(h, "qa_head", False) and h.get_fill_opacity() > 0.3]
        dots_ = [d for d in fam if getattr(d, "qa_dot", False) and d.get_fill_opacity() > 0.3]
        for h in heads:
            H_ = self._screen_box(h)
            for d in dots_:
                D_ = self._screen_box(d)
                ox = min(H_[2], D_[2]) - max(H_[0], D_[0]); oy = min(H_[3], D_[3]) - max(H_[1], D_[1])
                if ox > 0.01 and oy > -0.02:
                    self.qa_log.append(dict(t=t, kind="marker_dot", a=type(h).__name__, b="Dot")); break
        # generated images (stickers) count as solid shapes
        for m in self.mobjects:
            for sub in m.get_family():
                if getattr(sub, "qa_image", False) and not getattr(sub, "qa_ignore", False):
                    I = self._screen_box(sub)
                    for a, A in boxes:
                        ox = min(A[2], I[2]) - max(A[0], I[0]); oy = min(A[3], I[3]) - max(A[1], I[1])
                        if ox > 0.04 and oy > 0.04:
                            self.qa_log.append(dict(t=t, kind="text_on_image", a=name(a), b="sticker"))
        # boxes (cards, chips, pills) overlapping other boxes, solid shapes or images without one holding the other
        solids = []
        for m in self.mobjects:
            for sub in m.get_family():
                if getattr(sub, "qa_ignore", False) or getattr(sub, "qa_joined", False):
                    continue
                if getattr(sub, "qa_image", False):
                    solids.append(sub)
                elif isinstance(sub, VMobject) and not isinstance(sub, (Text, MathTex, Tex, MarkupText)) and len(sub.points) > 0 \
                        and id(sub) not in textfam_all and sub.get_fill_opacity() > 0.5 \
                        and sub.get_fill_color().to_hex().lower() not in (BG.lower(),):
                    solids.append(sub)
        boxes_c = [c_ for c_ in conts if not getattr(c_, "qa_joined", False)]
        def inside(P, Q, tol=0.03):
            return P[0] >= Q[0] - tol and P[1] >= Q[1] - tol and P[2] <= Q[2] + tol and P[3] <= Q[3] + tol
        seen_pairs = set()
        for c_ in boxes_c:
            C = self._screen_box(c_)
            for s in solids + boxes_c:
                if s is c_ or (id(s), id(c_)) in seen_pairs: continue
                seen_pairs.add((id(c_), id(s)))
                S_ = self._screen_box(s)
                ox = min(C[2], S_[2]) - max(C[0], S_[0]); oy = min(C[3], S_[3]) - max(C[1], S_[1])
                if ox > 0.04 and oy > 0.04 and not inside(S_, C) and not inside(C, S_):
                    self.qa_log.append(dict(t=t, kind="box_overlap", a=type(c_).__name__, b=type(s).__name__))
        for a, A in boxes:
            for s in shapes:
                if id(s) in textfam: continue
                B = self._screen_box(s)
                ox = min(A[2], B[2]) - max(A[0], B[0]); oy = min(A[3], B[3]) - max(A[1], B[1])
                if ox > 0.04 and oy > 0.04:
                    self.qa_log.append(dict(t=t, kind="text_shape", a=name(a), b=type(s).__name__))

    def tear_down(self):
        super().tear_down()
        out = HERE / "build" / "qa"; out.mkdir(parents=True, exist_ok=True)
        # collapse repeats
        uniq = {}
        for e in self.qa_log:
            k = (e["kind"], e.get("a"), e.get("b"))
            uniq.setdefault(k, []).append(e["t"])
        res = [dict(kind=k[0], a=k[1], b=k[2], times=v[:6], n=len(v)) for k, v in uniq.items()]
        (out / f"{type(self).__name__}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))


def _syl(w):
    import re
    w = w.lower()
    return max(1, len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and len(w) > 3 else 0))


def word_time(sid, k):
    """Estimated global start time of the k-th word (0-based) of segment sid,
    spreading the clip's duration over syllables plus ~0.22 s per comma/full stop."""
    s = SEGS[sid]
    words = s["text"].split()
    w = []
    for x in words:
        w.append(sum(_syl(q) for q in x.strip(",.;:?!'").split("-") if q))
        if x[-1] in ",.;:?!":
            w.append(-1)
    PAUSE = 0.22
    npause = sum(1 for v in w if v < 0)
    syl = sum(v for v in w if v > 0)
    rate = (s["end"] - s["start"] - PAUSE * npause) / syl
    t, i = s["start"], 0
    for v in w:
        if v < 0:
            t += PAUSE; continue
        if i == k:
            return t
        t += v * rate; i += 1
    return s["end"]


def word_index(sid, word):
    """Index of first word starting with `word` (case-insensitive, punctuation stripped)."""
    ws = [x.strip(",.;:?!'").lower() for x in SEGS[sid]["text"].split()]
    return ws.index(word.lower().strip(",.;:?!'"))


def xy_axes(x_range, y_range, x_len, y_len, x_label, y_label, x_labels=None, font_size=22, y_vertical=False):
    """Axes with Inter tick labels and axis titles. x_labels: optional {value: text}."""
    ax = Axes(x_range=x_range, y_range=y_range, x_length=x_len, y_length=y_len,
              axis_config=dict(color=INK2, stroke_width=3, include_tip=False, tick_size=0.07),
              x_axis_config=dict(include_ticks=True), y_axis_config=dict(include_ticks=True))
    labs = VGroup()
    xs = np.arange(x_range[0], x_range[1] + 1e-9, x_range[2])
    for v in xs:
        if x_labels is not None and v not in x_labels: continue
        txt = x_labels[v] if x_labels else f"{v:g}"
        t = T(txt, font_size, INK2).next_to(ax.c2p(v, y_range[0]), DOWN, buff=0.14); t.qa_clip_ok = True
        labs.add(t)
    for v in np.arange(y_range[0], y_range[1] + 1e-9, y_range[2]):
        t = T(f"{v:g}", font_size, INK2).next_to(ax.c2p(x_range[0], v), LEFT, buff=0.14); t.qa_clip_ok = True
        labs.add(t)
    if x_label:
        xt = T(x_label, 24, MUTED).next_to(ax.x_axis, DOWN, buff=0.5).align_to(ax.x_axis, RIGHT)
    else:
        xt = VGroup()
    if y_vertical:
        ylabs = VGroup(*[l for l in labs if abs(l.get_x() - ax.c2p(x_range[0], 0)[0]) > 0.05 and l.get_x() < ax.c2p(x_range[0], 0)[0]])
        yt = T(y_label, 22, MUTED).rotate(PI / 2).next_to(ylabs if len(ylabs) else ax.y_axis, LEFT, buff=0.15)
    else:
        yt = T(y_label, 24, MUTED).next_to(ax.y_axis, UP, buff=0.18).align_to(ax.y_axis, LEFT).shift(LEFT * 0.3)
    g = VGroup(ax, labs, xt, yt)
    g.ax, g.labs, g.xt, g.yt = ax, labs, xt, yt
    return g


def marker(axis, v, color, label, height=0.75, fs=28, side=UP, label_dir=UP):
    """Triangle pointer above axis value v with dashed stem and a label."""
    tri = Triangle(color=color, fill_opacity=1, stroke_width=0).scale(0.15).rotate(PI)
    tri.move_to(axis.n2p(v) + UP * height)
    stem = DashedLine(tri.get_bottom(), axis.n2p(v), color=color, stroke_width=3)
    lab = T(label, fs, color, weight=BOLD).next_to(tri, label_dir, buff=0.12)
    tri.qa_head = True
    g = VGroup(stem, tri, lab); g.tri, g.lab = tri, lab
    return g


def diamond(axis, v, color=VIOLET, label=None, height=0.75, fs=28, label_dir=UP):
    d = Square(0.22, color=color, fill_opacity=1, stroke_width=0).rotate(PI / 4).move_to(axis.n2p(v) + UP * height)
    stem = DashedLine(d.get_bottom(), axis.n2p(v), color=color, stroke_width=3)
    d.qa_head = True
    g = VGroup(stem, d)
    if label:
        lab = T(label, fs, color, weight=BOLD).next_to(d, label_dir, buff=0.12); g.add(lab); g.lab = lab
    g.tri = d
    return g


def defcard(sym_tex, words, color=INK, fs=30, w=None):
    """A definition card: [symbol]  =  plain words."""
    s = MathTex(sym_tex, color=color, font_size=fs * 1.6)
    e = T("=", fs, MUTED)
    t = T(words, fs, INK)
    row = VGroup(s, e, t).arrange(RIGHT, buff=0.22)
    box = RoundedRectangle(corner_radius=0.14, width=(w or row.width + 0.6), height=row.height + 0.42,
                           stroke_color=color, stroke_width=2, fill_color="#22221f", fill_opacity=1)
    box.qa_container = True
    row.move_to(box)
    return VGroup(box, row)


def frac(num, den, color=INK, fs=72):
    return MathTex(r"{" + str(num) + r"\over " + str(den) + r"}", color=color, font_size=fs)


def logo_mark(size=1.0):
    """Channel mark: violet rounded square with a green bell curve (as in the Math Lab TV intro/outro)."""
    sq = RoundedRectangle(corner_radius=0.16 * size, width=size, height=size, stroke_color=VIOLET, stroke_width=5 * size,
                          fill_color=BG, fill_opacity=1)
    sq.qa_container = True
    xs = np.linspace(-0.36, 0.36, 60) * size
    curve = VMobject(stroke_color=AQUA, stroke_width=5 * size).set_points_smoothly(
        [np.array([x, -0.24 * size + 0.5 * size * np.exp(-(x / (0.14 * size)) ** 2), 0]) for x in xs])
    curve.qa_ignore = True
    return VGroup(sq, curve)


def logo(size=1.0, tagline=False):
    mark = logo_mark(size)
    name = Text("MATH LAB TV", font=FONT_D, weight=BOLD, font_size=int(78 * size), color=INK)
    g = VGroup(mark, name).arrange(RIGHT, buff=0.32 * size)
    if tagline:
        tl = T("where math is something you can see", int(34 * size), INK2)
        tl.next_to(g, DOWN, buff=0.35 * size)
        g = VGroup(g, tl)
    return g


# ───────────── Grid / crowd helpers (from the Bayes video; reuse or delete) ─────────────
# Example: 1,000 people (40 x 25), 10 have the condition (column 1, top ten rows),
# the test catches 9 of them; 99 of the 990 healthy get a false alarm.
COLS, ROWS = 40, 25
SICK = [(0, ROWS - 1 - k) for k in range(10)]          # (col, row) cells, row 0 at the bottom
MISSED = SICK[9]


def _healthy_cells():
    sick = set(SICK)
    return [(c, r) for r in range(ROWS - 1, -1, -1) for c in range(COLS) if (c, r) not in sick]


HEALTHY = _healthy_cells()
_rng = np.random.default_rng(7)
FALSE_POS = [HEALTHY[k] for k in sorted(_rng.choice(990, 99, replace=False))]  # 99 of 990 healthy (1 in 10), scattered
assert len(FALSE_POS) == 99


def crowd_axes(cell=0.19, fs=20):
    g = xy_axes([0, COLS, 5], [0, ROWS, 5], COLS * cell, ROWS * cell, "column", "row", font_size=fs)
    return g


def crowd(axg, cell=0.19, fill=0.82, color=INK2, opacity=0.9):
    """Dict-like VGroup of 1,000 squares keyed by (col, row)."""
    ax = axg.ax
    g = VGroup(); g.cell = {}
    for r in range(ROWS - 1, -1, -1):
        for c in range(COLS):
            sq = Square(cell * fill, stroke_width=0, fill_color=color, fill_opacity=opacity)
            sq.move_to(ax.c2p(c + 0.5, r + 0.5))
            g.add(sq); g.cell[(c, r)] = sq
    return g


def ring(sq, color=AQUA, width=3.5, pad=0.05):
    r = Square(sq.width + 2 * pad, stroke_color=color, stroke_width=width, fill_opacity=0).move_to(sq)
    return r


def block(n, cols, color, cell=0.19, fill=0.82):
    """n squares stacked in rows of `cols`, bottom-left first (for countable stacks)."""
    g = VGroup()
    for k in range(n):
        c, r = k % cols, k // cols
        sq = Square(cell * fill, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to(
            RIGHT * (c * cell) + UP * (r * cell))
        g.add(sq)
    return g


def meter(length=10.0, fs=22, title="chance you have it", step=10, x_max=100):
    nl = NumberLine(x_range=[0, x_max, step], length=length, color=INK2, stroke_width=3, include_tip=False, tick_size=0.09)
    nums = VGroup()
    for v in range(0, x_max + 1, step):
        t = T(f"{v}%", fs, INK2).next_to(nl.n2p(v), DOWN, buff=0.16); nums.add(t)
    tt = T(title, 24, MUTED).next_to(nums, DOWN, buff=0.2).align_to(nl, LEFT)
    g = VGroup(nl, nums, tt); g.nl, g.nums, g.title = nl, nums, tt
    return g


def person(color=INK2, h=0.6, fill=0.0):
    head = Circle(radius=h * 0.17).set_stroke(color, 3).set_fill(color, fill)
    body = RoundedRectangle(corner_radius=h * 0.16, width=h * 0.55, height=h * 0.5).set_stroke(color, 3).set_fill(color, fill)
    head.next_to(body, UP, buff=h * 0.05)
    return VGroup(body, head)


def pill(text, color=INK, size=28, pad=0.24, fill="#22221f"):
    """Text chip whose box is sized from the text width."""
    t = T(text, size, color, weight=BOLD)
    box = RoundedRectangle(corner_radius=min(0.2, (t.height + 1.4 * pad) / 2), width=t.width + 2 * pad,
                           height=t.height + 1.4 * pad, stroke_color=color, stroke_width=2.5, fill_color=fill, fill_opacity=1)
    box.qa_container = True
    t.move_to(box)
    g = VGroup(box, t); g.box, g.text = box, t
    return g


def card(w, h, color=INK2, fill="#22221f"):
    b = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=color, stroke_width=2.5,
                         fill_color=fill, fill_opacity=1)
    b.qa_container = True
    return b


def check(color=AQUA, s=0.35):
    m = VMobject(stroke_color=color, stroke_width=7).set_points_as_corners(
        [LEFT * s * 0.5 + UP * s * 0.05, DOWN * s * 0.4, RIGHT * s * 0.6 + UP * s * 0.5])
    return m


def cross(color=RED_, s=0.3):
    return VGroup(Line(UL * s, DR * s), Line(UR * s, DL * s)).set_stroke(color, 7)


def title_card(main, sub, color=VIOLET, size=104):
    """Topic title card that ends the hook and opens the welcome scene (build it identically in both
    scenes so the cut is seamless). Keep `main` short enough to fit: check .width < 12."""
    t = glow(TB(main, size, color), color)
    s_ = T(sub, 44, INK).next_to(t, DOWN, buff=0.5)
    return VGroup(t, s_).move_to(UP * 0.4)


def sticker(path, height=3.0):
    """A generated illustration (transparent PNG made by scripts/sticker.py) as a Manim image.
    The overlap checker treats it as a solid shape, so text placed on it is flagged."""
    im = ImageMobject(str(HERE / path))
    im.set_height(height)
    im.qa_image = True
    return im


def beam_scale(width=6.0, color=INK2):
    """Balance beam. Returns (group, theta tracker, left pan, right pan). Pans hang from the beam ends and stay level."""
    th = ValueTracker(0.0)
    piv = ORIGIN
    base = Polygon(piv + DOWN * 0.05, piv + DOWN * 1.0 + LEFT * 0.5, piv + DOWN * 1.0 + RIGHT * 0.5).set_stroke(color, 4)
    beam = always_redraw(lambda: Line(piv + width / 2 * np.array([-np.cos(th.get_value()), -np.sin(th.get_value()), 0]),
                                      piv + width / 2 * np.array([np.cos(th.get_value()), np.sin(th.get_value()), 0])
                                      ).shift(base.get_top() - piv).set_stroke(color, 6))
    def pan():
        plate = Arc(radius=0.9, start_angle=PI + 0.5, angle=PI - 1.0).set_stroke(color, 4)
        plate.stretch(0.35, 1)
        s1 = Line(plate.get_corner(UL), plate.get_corner(UL) + UP * 0.9 + RIGHT * 0.75).set_stroke(MUTED, 2)
        s2 = Line(plate.get_corner(UR), plate.get_corner(UR) + UP * 0.9 + LEFT * 0.75).set_stroke(MUTED, 2)
        g = VGroup(plate, s1, s2)
        g.hook = lambda: s1.get_end()
        return g
    L, R = pan(), pan()
    L.add_updater(lambda m: m.shift(beam.get_start() - m[1].get_end()))
    R.add_updater(lambda m: m.shift(beam.get_end() - m[1].get_end()))
    g = VGroup(base, beam, L, R)
    return g, th, L, R


def step_chip(n, text, color=INK, size=30):
    num = TB(str(n), int(size * 1.1), BG)
    disc = Circle(radius=size / 100, stroke_width=0, fill_color=color, fill_opacity=1)
    disc.qa_container = True
    num.move_to(disc)
    t = T(text, size, color, weight=BOLD).next_to(disc, RIGHT, buff=0.2)
    return VGroup(disc, num, t)


def stacks_axes(y_max=120, step=20, x_len=4.6, y_len=4.4, title="people who tested positive"):
    return xy_axes([0, 2, 1], [0, y_max, step], x_len, y_len, None, title, x_labels={}, font_size=22)


def stack(ax, x, n, color, per_row=5, unit=1):
    """n countable squares; each row holds per_row squares, one square = `unit` people on the y axis."""
    pitch = (ax.c2p(0, per_row * unit)[1] - ax.c2p(0, 0)[1])
    g = VGroup()
    x0 = ax.c2p(x, 0)[0] - (per_row - 1) / 2 * pitch
    for k in range(n):
        c, r = k % per_row, k // per_row
        g.add(Square(pitch * 0.82, stroke_width=0, fill_color=color, fill_opacity=0.95)
              .move_to([x0 + c * pitch, ax.c2p(0, 0)[1] + (r + 0.5) * pitch, 0]))
    return g


def bar(ax, x, v, color, width=1.2, opacity=0.9):
    r = Rectangle(width=width, height=max(1e-3, ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), stroke_width=0,
                  fill_color=color, fill_opacity=opacity)
    return r.move_to(ax.c2p(x, 0), aligned_edge=DOWN)


def domain_tile(text, color, w=2.9, h=1.5, size=40):
    box = card(w, h, color)
    t = TB(text, size, color).move_to(box)
    return VGroup(box, t)


def gauge(value, color, label, r=1.1, size=26):
    """Half-circle gauge filled to value (0–100)."""
    track = Arc(radius=r, start_angle=PI, angle=-PI).set_stroke(GRID, 16)
    fill = Arc(radius=r, start_angle=PI, angle=-PI * value / 100).set_stroke(color, 16)
    num = TB(f"{value:g}%", 44, color).move_to(track.get_center() + DOWN * 0.15 + UP * 0.1)
    num.move_to([track.get_center()[0], track.get_bottom()[1] + 0.35, 0])
    lab = T(label, size, color, weight=BOLD).next_to(track, DOWN, buff=0.3)
    g = VGroup(track, fill, num, lab); g.fill = fill
    return g


def loop_arrows(left, right, color_top=VIOLET, color_bot=WARN):
    """Two curved arrows forming a loop between mobjects `left` and `right`."""
    a1 = CurvedArrow(left.get_top() + UP * 0.15, right.get_top() + UP * 0.15, angle=-PI / 2.5, color=color_top, stroke_width=5)
    a2 = CurvedArrow(right.get_bottom() + DOWN * 0.15, left.get_bottom() + DOWN * 0.15, angle=-PI / 2.5, color=color_bot, stroke_width=5)
    return VGroup(a1, a2)


def tube(color=AQUA, h=1.6, w=0.5, fill=0.35):
    body = RoundedRectangle(corner_radius=w * 0.4, width=w, height=h).set_stroke(INK2, 4)
    liq = Rectangle(width=w * 0.8, height=h * fill).set_stroke(width=0).set_fill(color, 0.85)
    liq.move_to(body.get_bottom() + UP * (h * fill / 2 + 0.06))
    return VGroup(body, liq)


# ───────────── motion-graphics helpers ─────────────
def ripple(point, color=WARN, r=0.25, scale=5, width=5):
    """An expanding ring that fades out: marks a moment of emphasis at a point."""
    c = Circle(radius=r).set_stroke(color, width).move_to(point)
    c.qa_ignore = True
    return FadeOut(c, scale=scale)


def glint(mob, color=INK, width=6, time_width=0.35):
    """A light sweeping along a mobject's outline (or underline for text)."""
    if isinstance(mob, (Text, MathTex, Tex)) or (isinstance(mob, VGroup) and any(isinstance(x, Text) for x in mob)):
        path = Line(mob.get_corner(DL) + DOWN * 0.08, mob.get_corner(DR) + DOWN * 0.08)
    else:
        path = mob.copy().set_fill(opacity=0)
    path.set_stroke(color, width)
    for x in path.get_family(): x.qa_ignore = True
    return ShowPassingFlash(path, time_width=time_width)


def flipping(c):
    """One coin flip (squash and return)."""
    return c.animate(rate_func=there_and_back).stretch(0.06, 0)


def push(scene, old, new, direction=LEFT, run_time=0.8):
    """Slide `old` out and `new` in from the opposite side, like a camera pan between two stations."""
    d = 14.5 * direction
    new.shift(-d)
    # move each existing piece itself (animating a temporary group that wraps on-screen mobjects makes them vanish)
    # move exactly the scene's top-level pieces that belong to `old`: animating a group that is not itself in the
    # scene makes Manim add it on top, so filled cards would cover their own labels during the slide
    fam = {id(x) for x in old.get_family()}
    olds = [m for m in scene.mobjects if fam & {id(x) for x in m.get_family()}]   # incl. groups made by an earlier push
    for m in olds: scene.qa_mute(m)          # leaving the frame: not part of the layout any more
    scene.play(*[m.animate(rate_func=smooth).shift(d) for m in olds], new.animate(rate_func=smooth).shift(d), run_time=run_time)
    scene.remove(*[x for m in olds for x in m.get_family()])


def card_cue(title, mini, color=VIOLET):
    """YouTube-card cue for a referenced video: a small tile (mini picture + title) with an 'i' badge.
    Sits in the top-right corner, where the real card appears."""
    t = T(title, 24, INK, weight=BOLD)
    mini.scale_to_fit_height(0.62)
    row = VGroup(mini, t).arrange(RIGHT, buff=0.25)
    box = RoundedRectangle(corner_radius=0.16, width=row.width + 0.55, height=row.height + 0.42,
                           stroke_color=color, stroke_width=2.5, fill_color="#22221f", fill_opacity=1)
    box.qa_container = True
    row.move_to(box)
    badge = VGroup(Circle(0.21).set_stroke(INK, 2.5).set_fill(color, 1), T("i", 24, INK, weight=BOLD))
    badge[0].qa_container = True
    badge[1].move_to(badge[0])
    badge.next_to(box, LEFT, buff=0.18)
    g = VGroup(badge, box, row)
    g.move_to([7.111 - EDGE - 0.15 - g.width / 2, 4 - EDGE - 0.1 - g.height / 2, 0])
    g.box, g.badge = box, badge
    return g


def mini_bayes():
    sq = VGroup(*[Square(0.16, stroke_width=0, fill_color=(ORANGE_ if (i == 0) else BLUE_), fill_opacity=0.9)
                  for i in range(25)]).arrange_in_grid(5, 5, buff=0.04)
    return sq


def mini_sd():
    ax = Line(LEFT * 0.7, RIGHT * 0.7).set_stroke(INK2, 3)
    xs = np.linspace(-0.7, 0.7, 40)
    cur = VMobject().set_points_smoothly([np.array([x, 0.65 * np.exp(-(x / 0.28) ** 2), 0]) for x in xs]).set_stroke(AQUA, 3)
    br = DoubleArrow(LEFT * 0.28 + UP * 0.25, RIGHT * 0.28 + UP * 0.25, buff=0, stroke_width=2, tip_length=0.08, color=VIOLET)
    return VGroup(ax, cur, br)


def cup(color=WARN, s=0.42):
    body = Polygon(LEFT * 0.5 + UP * 0.45, RIGHT * 0.5 + UP * 0.45, RIGHT * 0.38 + DOWN * 0.45, LEFT * 0.38 + DOWN * 0.45)
    body.set_stroke(color, 3).set_fill(color, 0.9)
    handle = Arc(radius=0.2, start_angle=-PI / 2, angle=PI).set_stroke(color, 4).move_to(RIGHT * 0.58)
    g = VGroup(body, handle).scale(s)
    return g


def steam(cup_top, color=INK2):
    """One wisp of steam rising from a point and fading."""
    pts = [cup_top + np.array([0.06 * np.sin(k * 1.3), 0.12 * k, 0]) for k in range(6)]
    w = VMobject().set_points_smoothly(pts).set_stroke(color, 3, opacity=0.8)
    w.qa_ignore = True
    return FadeOut(w, shift=UP * 0.35)


def drop_into(ax, k, color=BLUE_, h_from=210, r=0.1):
    """A friend (dot) falling from above into column k of a distribution chart."""
    d = Dot(radius=r, color=color).move_to(ax.c2p(k, h_from))
    d.qa_ignore = True
    dist = ax.c2p(k, h_from)[1] - ax.c2p(k, 1)[1]
    return FadeOut(d, shift=DOWN * dist, rate_func=rate_functions.ease_in_quad)


def binom_k(rng):
    return int(rng.binomial(20, 0.5))


def pulse(*mobs, s=1.12):
    """Grow and settle back (safe for chips/pills: Indicate would recolour their filled box over the text).
    Several mobjects pulse together about their common centre. Never pass a temporary VGroup of mobjects that
    already belong to another group: adding it to the scene pulls them out of their group."""
    if mobs and not isinstance(mobs[-1], Mobject):
        *mobs, s = mobs
    c = VGroup(*[m.copy() for m in mobs]).get_center() if len(mobs) > 1 else mobs[0].get_center()
    return AnimationGroup(*[m.animate(rate_func=there_and_back).scale(s, about_point=c) for m in mobs])


def speedometer(title="how surprising?", left="not surprising", right="very surprising", r=1.55):
    """A real speedometer dial: coloured zones (calm → alarming), tick marks, end labels, a tapered needle on a hub.
    Returns (group, angle tracker): the needle points at angle = tracker value, PI (far left) … 0 (far right)."""
    zones = VGroup(*[Arc(radius=r, start_angle=PI - PI * a / 3, angle=-PI / 3 + 0.02).set_stroke(c, 16)
                     for a, c in enumerate([AQUA, WARN, RED_])])
    ticks = VGroup(*[Line(ORIGIN, RIGHT * (0.16 if k % 5 else 0.26)).set_stroke(INK2, 3 if k % 5 else 4)
                     .rotate(PI - PI * k / 10, about_point=ORIGIN).shift(np.array([np.cos(PI - PI * k / 10), np.sin(PI - PI * k / 10), 0]) * (r - 0.38))
                     for k in range(11)])
    for x in ticks: x.qa_ignore = True
    hub = Circle(0.13).set_stroke(BG, 3).set_fill(INK, 1)
    hub.qa_ignore = True
    ang = ValueTracker(PI * 0.97)
    def mk_needle():
        a = ang.get_value()
        d = np.array([np.cos(a), np.sin(a), 0]); n = np.array([-d[1], d[0], 0])
        c = hub.get_center()          # follows the dial wherever it is moved
        rr = zones.width / 2 - 0.25
        return Polygon(c + d * rr, c + n * 0.08, c - d * 0.22, c - n * 0.08).set_stroke(width=0).set_fill(INK, 1)
    needle = always_redraw(mk_needle)
    needle.qa_ignore = True
    lab_l = T(left, 22, AQUA, weight=BOLD).next_to(np.array([-r, 0, 0]), DOWN, buff=0.25)
    lab_r = T(right, 22, RED_, weight=BOLD).next_to(np.array([r, 0, 0]), DOWN, buff=0.25)
    ttl = T(title, 28, INK, weight=BOLD).next_to(VGroup(lab_l, lab_r), DOWN, buff=0.22)
    g = VGroup(zones, ticks, needle, hub, lab_l, lab_r, ttl)
    g.zones, g.needle, g.hub = zones, needle, hub
    return g, ang


def pmf_list(n, p, total=1000):
    """Expected count (of `total`) for each number of heads 0..n with heads-probability p."""
    return [total * comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)]



# ───────────── Prosecutor's Fallacy helpers ─────────────
# Colour roles: innocent = BLUE_, match/evidence = WARN, guilty = ORANGE_, answer = VIOLET, crowd = AQUA, swap = RED_
WORD_COL = {"match": WARN, "innocent": BLUE_, "guilty": ORANGE_, "positive": WARN, "healthy": BLUE_,
            "fair": BLUE_, "this extreme": WARN, "fraud": ORANGE_, "flagged": WARN, "four legs": WARN, "dog": ORANGE_}


def cond(a, b, size=40):
    """'P(a | b)' as separate Inter pieces: g.P, g.a, g.bar, g.b, g.close. Colours from WORD_COL."""
    P = T("P(", size, INK, weight=BOLD)
    A = T(a, size, WORD_COL.get(a, INK), weight=BOLD)
    bar = T("|", size, INK2, weight=BOLD)
    B = T(b, size, WORD_COL.get(b, INK), weight=BOLD)
    cl = T(")", size, INK, weight=BOLD)
    g = VGroup(P, A, bar, B, cl).arrange(RIGHT, buff=0.14)
    bar.set_x((A.get_right()[0] + B.get_left()[0]) / 2)   # Text pads '|' unevenly: centre it between the words
    g.P, g.a, g.bar, g.b, g.close = P, A, bar, B, cl
    return g


def cond_box(a, b, value=None, color=INK2, size=40, w=None, caption=None, vcol=None):
    """A rounded box holding P(a | b) and, below it, an optional value and caption."""
    e = cond(a, b, size)
    rows = [e]
    v = None
    if value is not None:
        v = TB(value, int(size * 1.1), vcol or color); rows.append(v)
    cp = None
    if caption:
        cp = T(caption, int(size * 0.62), INK2); rows.append(cp)
    inner = VGroup(*rows).arrange(DOWN, buff=0.3)
    box = card(max(w or 0, inner.width + 0.8), inner.height + 0.7, color)
    inner.move_to(box)
    g = VGroup(box, inner)
    g.box, g.expr, g.value, g.caption = box, e, v, cp
    return g


def swap_parts(scene, e, run_time=1.2):
    """Animate the two words of a cond() expression trading places over and under the bar; returns new expr."""
    pa, pb = e.a.get_center(), e.b.get_center()
    wa, wb = e.a.width, e.b.width
    # final layout: P( b | a )
    left = e.P.get_right()[0] + 0.14
    nb = left + wb / 2
    bar_x = left + wb + 0.14 + e.bar.width / 2
    na = bar_x + e.bar.width / 2 + 0.14 + wa / 2
    cl_x = na + wa / 2 + 0.14 + e.close.width / 2
    y = e.a.get_y()
    pa_arc = ArcBetweenPoints(pa, np.array([na, y, 0]), angle=-PI * 0.7)
    pb_arc = ArcBetweenPoints(pb, np.array([nb, y, 0]), angle=-PI * 0.7)
    scene.qa_mute(e)
    scene.play(MoveAlongPath(e.a, pa_arc), MoveAlongPath(e.b, pb_arc),
               e.bar.animate.set_x(bar_x), e.close.animate.set_x(cl_x), run_time=run_time)
    scene.qa_mute(e, False)
    e.a, e.b = e.b, e.a
    e.submobjects = [e.P, e.a, e.bar, e.b, e.close]
    return e


def dna(h=1.5, color=WARN, w=0.55, partial=False):
    """Double-helix icon: two sine strands and rungs. partial=True dims the top half (a partial trace)."""
    ys = np.linspace(-h / 2, h / 2, 50)
    s1 = VMobject().set_points_smoothly([np.array([w / 2 * np.sin(y / h * 2 * TAU), y, 0]) for y in ys]).set_stroke(color, 5)
    s2 = VMobject().set_points_smoothly([np.array([-w / 2 * np.sin(y / h * 2 * TAU), y, 0]) for y in ys]).set_stroke(color, 5)
    rungs = VGroup()
    for y in np.linspace(-h / 2 + 0.08, h / 2 - 0.08, 9):
        x = w / 2 * np.sin(y / h * 2 * TAU)
        if abs(x) > 0.04:
            rungs.add(Line([-x, y, 0], [x, y, 0]).set_stroke(color, 3, opacity=0.8))
    g = VGroup(s1, s2, rungs)
    g.rungs = rungs
    return g


def skyline(width=12.0, color=INK2, seed=3, h_max=2.2):
    rng = np.random.default_rng(seed)
    g = VGroup(); x = -width / 2
    while x < width / 2 - 0.3:
        bw = rng.uniform(0.45, 0.9); bh = rng.uniform(0.6, h_max)
        b = Rectangle(width=bw, height=bh).set_stroke(color, 2.5).set_fill("#22221f", 1)
        b.move_to([x + bw / 2, bh / 2, 0])
        wins = VGroup()
        for wy in np.arange(0.25, bh - 0.15, 0.32):
            for wx in np.arange(-bw / 2 + 0.15, bw / 2 - 0.1, 0.22):
                if rng.random() < 0.45:
                    wins.add(Square(0.08).set_stroke(width=0).set_fill(WARN, 0.6).move_to([x + bw / 2 + wx + 0.04, wy, 0]))
        g.add(VGroup(b, wins)); x += bw + 0.05
    for m in g.family_members_with_points():
        m.qa_ignore = True
    return g


def juror(color=INK2, h=0.55):
    return person(color, h, fill=0.25)


def lock_icon(color=INK2, s=0.5):
    body = RoundedRectangle(corner_radius=0.06 * s / 0.5, width=0.7 * s, height=0.55 * s).set_stroke(color, 4).set_fill(color, 0.9)
    shackle = Arc(radius=0.23 * s, start_angle=0, angle=PI).set_stroke(color, 5).next_to(body, UP, buff=0)
    return VGroup(body, shackle)


def gavel(color=INK2, s=1.0):
    head = RoundedRectangle(corner_radius=0.06, width=0.7, height=0.3).set_stroke(color, 3).set_fill(color, 0.85)
    handle = Line(ORIGIN, DOWN * 0.75 + RIGHT * 0.35).set_stroke(color, 6).next_to(head, DOWN, buff=0).shift(RIGHT * 0.15)
    return VGroup(head, handle).rotate(-0.3).scale(s)


def labcoat(color=INK, s=1.0):
    p = person(color, 0.9 * s, fill=0.0)
    lap = VGroup(Line(p[0].get_top() + LEFT * 0.08 * s, p[0].get_center()),
                 Line(p[0].get_top() + RIGHT * 0.08 * s, p[0].get_center())).set_stroke(color, 3)
    return VGroup(p, lap)
