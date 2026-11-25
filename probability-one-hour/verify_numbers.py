#!/usr/bin/env python3
"""Check every number used in the narration and on screen with exact arithmetic (fractions).
Simulations use fixed seeds; their results are written to sim.json so the scenes show exactly these numbers."""
from fractions import Fraction as F
from itertools import product
from math import comb, factorial, prod
import json, pathlib, random

D = list(product(range(1, 7), repeat=2))           # (orange, blue)
def P(pred, space=D, given=lambda o: True):
    w = [o for o in space if given(o)]
    return F(sum(1 for o in w if pred(o)), len(w))
tot = lambda o: o[0] + o[1]

# hook / two dice
assert len(D) == 36
assert P(lambda o: tot(o) == 7) == F(6, 36) == F(1, 6)
assert P(lambda o: tot(o) == 12) == F(1, 36)
assert P(lambda o: tot(o) == 7) / P(lambda o: tot(o) == 12) == 6
ways = [sum(1 for o in D if tot(o) == s) for s in range(2, 13)]
assert ways == [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1] and sum(ways) == 36
assert P(lambda o: tot(o) == 8) == F(5, 36)
assert P(lambda o: o[0] == o[1]) == F(1, 6)
assert P(lambda o: tot(o) <= 4) == F(6, 36) == F(1, 6)
# what is probability / counting
assert F(25, 100) == F(1, 4)
assert F(3, 6) == F(1, 2) and F(2, 6) == F(1, 3)
coins2 = list(product("HT", repeat=2)); assert F(sum(1 for c in coins2 if c.count("H") == 1), 4) == F(1, 2)
coins3 = list(product("HT", repeat=3)); assert len(coins3) == 8
assert F(sum(1 for c in coins3 if c.count("H") == 2), 8) == F(3, 8) and float(F(3, 8)) == 0.375
# counting bigger things
assert 3 * 4 == 12 and 12 * 2 == 24
assert 10 ** 4 == 10000
# order
assert factorial(3) == 6 and factorial(10) == 3628800
assert prod(range(44, 50)) // factorial(6) == comb(49, 6) == 13983816 and factorial(6) == 720
assert 250000 < comb(49, 6) / 52 < 270000          # "over a quarter of a million years" (≈ 268,919)
# NOT
assert 1 - F(1, 6) == F(5, 6) == F(30, 36)
assert 1 - F(1, 36) == F(35, 36)
# odds
assert F(6, 6 + 30) == F(1, 6) and F(6, 30) == F(1, 5)
assert F(1, 1 + 3) == F(1, 4)
# OR
assert P(lambda o: tot(o) in (7, 11)) == F(8, 36) == F(2, 9)
assert P(lambda o: o[0] == 6 or o[1] == 6) == F(11, 36)
assert 12 + 8 - 5 == 15 and F(15, 30) == F(1, 2)
# AND
assert P(lambda o: o == (6, 6)) == F(1, 6) * F(1, 6) == F(1, 36)
assert F(1, 2) * F(1, 6) == F(1, 12)
assert F(3, 5) * F(2, 4) == F(6, 20) == F(3, 10)
assert F(3, 5) * F(3, 5) == F(9, 25) and float(F(9, 25)) == 0.36
assert F(1, 6) ** 3 == F(1, 216)
# at least one
assert F(5, 6) ** 4 == F(625, 1296) and round(float(F(625, 1296)) * 100, 1) == 48.2
assert 1 - F(5, 6) ** 4 == F(671, 1296) and round(float(F(671, 1296)) * 100, 1) == 51.8
assert round(float(F(4, 6)) * 100) == 67
assert round(float(1 - F(5, 6) ** 6) * 100, 1) == 66.5
assert F(3, 4) ** 3 == F(27, 64) and 1 - F(27, 64) == F(37, 64) and round(float(F(37, 64)) * 100) == 58
# cards
deck = list(product(range(1, 14), "HDCS"))
Pc = lambda pred: F(sum(1 for c in deck if pred(c)), 52)
assert Pc(lambda c: c[1] == "H") == F(1, 4) and Pc(lambda c: c[0] == 13) == F(1, 13)
assert Pc(lambda c: c[1] == "H" or c[0] == 13) == F(16, 52) == F(4, 13)
assert F(4, 52) * F(3, 51) == F(1, 221) and round(float(F(1, 221)) * 100, 2) == 0.45
# two-step trees (illustrative numbers)
late = F(3, 10) * F(1, 2) + F(7, 10) * F(1, 10)
assert late == F(22, 100)
assert (F(3, 10) * F(1, 2)) / late == F(15, 22) and round(float(F(15, 22)) * 100) == 68
# given that
assert P(lambda o: tot(o) == 12, given=lambda o: o[0] == 6) == F(1, 6)
assert P(lambda o: tot(o) == 7, given=lambda o: o[0] == 6) == F(1, 6) == P(lambda o: tot(o) == 7)
assert all(P(lambda o: tot(o) == 7, given=lambda o, k=k: o[0] == k) == F(1, 6) for k in range(1, 7))
assert sum(1 for o in D if tot(o) >= 10) == 6
assert P(lambda o: o[0] == o[1], given=lambda o: tot(o) >= 10) == F(1, 3)
assert P(lambda o: o[0] == 6, given=lambda o: tot(o) == 12) == 1
assert F(8, 12) == F(2, 3)
# expected value
assert F(sum(range(1, 7)), 6) == F(7, 2) and F(7, 2) * 2 == 7
ev = 10 * F(1, 6)
assert round(float(ev), 2) == 1.67 and ev - 2 == F(-1, 3) and 60 * (ev - 2) == -20
assert 50 * F(1, 100) == F(1, 2) and F(1, 2) - 1 == F(-1, 2)
# measuring
assert F(3, 10) == F(3, 10)
# more dice
D3 = list(product(range(1, 7), repeat=3)); assert len(D3) == 216
w3 = {s: sum(1 for o in D3 if sum(o) == s) for s in range(3, 19)}
assert w3[10] == w3[11] == 27 and max(w3.values()) == 27
# practice round
assert F(4, 10) == F(2, 5)
assert P(lambda o: tot(o) == 10) == F(3, 36) == F(1, 12) and 1 - F(1, 12) == F(11, 12)
assert 1 - F(1, 8) == F(7, 8)
assert P(lambda o: o[0] % 2 == 0 and o[1] % 2 == 0) == F(9, 36) == F(1, 4)
assert P(lambda o: o[0] == o[1], given=lambda o: tot(o) == 4) == F(1, 3)
assert F(1 + 2 + 3 + 6, 4) == 3
# mistakes
assert F(1, 2) ** 5 == F(1, 32) and F(1, 2) ** 6 == F(1, 64)
assert 30_000_000 * F(1, 1_000_000) == 30   # "tens of millions" × one-in-a-million → dozens

# streak claim: in 20 fair flips, a run of 4+ heads somewhere happens in "about half" of runs
def p_no_run(n, k):   # P(no run of k heads in n flips), exact DP over the current run length
    st = {0: F(1)}
    for _ in range(n):
        nx = {}
        for r, p in st.items():
            nx[0] = nx.get(0, 0) + p / 2
            if r + 1 < k:
                nx[r + 1] = nx.get(r + 1, 0) + p / 2
        st = nx
    return sum(st.values())
streak = 1 - p_no_run(20, 4)
print(f"P(4+ heads in a row within 20 flips) = {float(streak):.3f}")
assert 0.45 < streak < 0.50   # narration: "close to half of all runs"

# fair-die check (bars as shown)
fair = [8, 11, 9, 12, 7, 13]; assert sum(fair) == 60
from math import comb as C
tail = sum(F(C(60, k)) * F(1, 6) ** k * F(5, 6) ** (60 - k) for k in range(25, 61))
print(f"P(25+ sixes in 60 fair rolls) = {float(tail):.2e}")
assert tail < F(1, 10000)

# ── simulations (fixed seeds) for the on-screen charts ──
sim = {}
rng = random.Random(7)
while True:   # first 10-flip run with exactly 7 heads, for the "wobble" beat
    flips = [rng.random() < 0.5 for _ in range(10)]
    if sum(flips) == 7:
        break
sim["ten_flips"] = ["H" if f else "T" for f in flips]
rng = random.Random(11); h = 0; curve = []
for n in range(1, 10001):
    h += rng.random() < 0.5
    curve.append(h / n)
sim["heads_share"] = {str(n): curve[n - 1] for n in [1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 50, 75, 100, 150, 200, 300, 500, 750, 1000, 2000, 3000, 5000, 7500, 10000]}
for n, seed in [(36, 3), (360, 5), (36000, 9)]:
    rng = random.Random(seed); cnt = {s: 0 for s in range(2, 13)}
    for _ in range(n):
        cnt[rng.randint(1, 6) + rng.randint(1, 6)] += 1
    sim[f"sums_{n}"] = cnt
sim["no_six_in_six"] = [2, 5, 1, 3, 3, 4]
rng = random.Random(21); flips20 = None
for _ in range(1000):
    f = "".join(rng.choice("HT") for _ in range(20))
    if "HHHH" in f and "HHHHH" not in f:
        flips20 = f; break
sim["twenty_flips"] = flips20
rng = random.Random(3); tokens = [0]
for _ in range(60):
    tokens.append(tokens[-1] + (10 if rng.randint(1, 6) + rng.randint(1, 6) == 7 else 0) - 2)
sim["stall_tokens"] = tokens
assert tokens[-1] == -20   # this seed lands on the expected value, so the chart reads cleanly
pathlib.Path(__file__).with_name("sim.json").write_text(json.dumps(sim, indent=1))
print("ten flips:", "".join(sim["ten_flips"]), "| 36 rolls zeros:", [s for s, c in sim["sums_36"].items() if c == 0],
      "| 20 flips:", flips20, "| stall after 60:", tokens[-1])
print("all numbers verified")
