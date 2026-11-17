#!/usr/bin/env python3
"""Find stretches where nothing happens on screen.

  python3 motion_check.py <scene.mp4> [...]      (scene renders, before the subtitle overlay)

Reads the video at 30 fps as 192x108 greyscale and compares each frame with the one 0.2 s earlier (what a
viewer perceives as motion). A moment "has action" when at least 0.15% of pixels changed by more than a few
grey levels (a moving label, a growing bar, a pulse, a camera move). Reports every stretch longer than MAX_STILL seconds without action, and the
scene's longest still stretch. The owner's rule: no second without something happening, so MAX_STILL = 1.0.
"""
import subprocess, sys
import numpy as np

W, H, FPS = 192, 108, 30
MAX_STILL = 1.0
PIX_DELTA = 6          # grey levels (0-255) a pixel must change by to count
ACTION = 0.0015        # share of pixels that must change for a frame to count as action
LAG = 6                # compare frames 0.2 s apart


def frames(path):
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={FPS},scale={W}:{H},format=gray", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.int16)


def still_runs(path):
    f = frames(path)
    act = (np.abs(f[LAG:] - f[:-LAG]) > PIX_DELTA).mean(axis=(1, 2)) > ACTION
    act = np.concatenate([act[:1].repeat(LAG - 1), act])
    runs, start = [], None
    for i, a in enumerate(list(act) + [True]):
        if not a and start is None:
            start = i
        elif a and start is not None:
            if (i - start) / FPS > MAX_STILL:
                runs.append((start / FPS, i / FPS))
            start = None
    return runs, len(f) / FPS, flickers(f)


def flickers(f, jump=8.0):
    """Moments where one region of the frame blinks: it jumps away from its level and comes back to the SAME level
    within a second, while most of the frame stays put (an image whose opacity overshot 1, an object drawn in the
    wrong place for a frame). Whole-screen slides and pushes are not flicker."""
    out = []
    tiles = f.reshape(len(f), 4, H // 4, 4, W // 4).mean(axis=(2, 4)).reshape(len(f), 16)
    d = np.diff(tiles, axis=0)
    moving = (np.abs(d) > 1.0).sum(axis=1)            # tiles changing at all: many = a slide/push/zoom
    for i in range(len(d)):
        big = np.abs(d[i]) > jump
        if not big.any() or big.sum() > 6 or moving[max(0, i - 3):i + 31].max() >= 9:
            continue
        for t_ in np.nonzero(big)[0]:
            pre = tiles[i, t_]
            seg = tiles[i + 2:i + 31, t_]
            if len(seg) and (np.abs(seg - pre) < 1.5).any():
                out.append(round((i + 1) / FPS, 2))
                break
    return sorted(set(out))


if __name__ == "__main__":
    bad = 0
    for p in sys.argv[1:]:
        runs, dur, fl = still_runs(p)
        longest = max([b - a for a, b in runs], default=0)
        print(f"{p.split('/')[-1]}: {dur:.1f}s, {len(runs)} still stretches > {MAX_STILL}s, longest {longest:.1f}s")
        for a, b in runs:
            print(f"    still {a:6.1f}–{b:6.1f}s  ({b - a:.1f}s)")
        if fl:
            print(f"    FLICKER at {fl[:10]} s (something blinked out and back)")
        bad += len(runs) + len(fl)
    sys.exit(1 if bad else 0)
