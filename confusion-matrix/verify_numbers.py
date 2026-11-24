#!/usr/bin/env python3
"""Check every number used in the narration and on screen with exact arithmetic (fractions).
Run it before checkpoint 1: `python3 verify_numbers.py`."""
from fractions import Fraction as F


def grid(tp, fn, fp, tn):
    n = tp + fn + fp + tn
    return dict(n=n, acc=F(tp + tn, n), prec=F(tp, tp + fp) if tp + fp else None, rec=F(tp, tp + fn),
                f1=F(2 * tp, 2 * tp + fp + fn) if tp else F(0), spec=F(tn, tn + fp))


def pct(x):
    return float(x * 100)


# ── Running example: 10,000 card payments, 100 of them fraud (1 in 100) ──
N, FRAUD = 10_000, 100
assert F(FRAUD, N) == F(1, 100)

# Lazy model: never flags anything
lazy = grid(tp=0, fn=100, fp=0, tn=9_900)
assert lazy["acc"] == F(99, 100)                      # "ninety-nine percent accurate"
assert lazy["rec"] == 0                               # catches zero fraud

# Model A ("catches ninety percent of fraud"): flags 120 payments
A = grid(tp=90, fn=10, fp=30, tn=9_870)
assert A["n"] == N and 90 + 10 == FRAUD and 30 + 9_870 == 9_900
assert 90 + 30 == 120                                 # flagged
assert A["acc"] == F(9_960, 10_000) == F(249, 250)    # 99.6 %
assert pct(A["acc"]) == 99.6
assert A["rec"] == F(9, 10)                           # 90 % recall
assert A["prec"] == F(3, 4)                           # 75 % precision: three of every four alarms real
assert A["f1"] == F(9, 11)                            # ≈ 81.8 %, "about eighty-two percent"
assert round(pct(A["f1"])) == 82
assert A["f1"] == 2 * A["prec"] * A["rec"] / (A["prec"] + A["rec"])   # harmonic-mean form agrees
assert F(A["prec"] + A["rec"], 2) == F(33, 40)        # plain average would be 82.5 %
# accuracy only moved 99 → 99.6, i.e. 60 more right answers out of 10,000
assert (90 + 9_870) - 9_900 == 60

# Model B ("ninety percent of its alarms are real"): flags 50 payments
B = grid(tp=45, fn=55, fp=5, tn=9_895)
assert B["n"] == N and 45 + 55 == FRAUD and 5 + 9_895 == 9_900
assert B["prec"] == F(9, 10)                          # 90 % precision
assert B["rec"] == F(45, 100) == F(9, 20)             # 45 % recall: misses more than half
assert B["acc"] == F(9_940, 10_000)                   # 99.4 %
assert pct(B["acc"]) == 99.4
assert B["f1"] == F(90, 150) == F(3, 5)               # 60 %

# Model C (very nervous setting): flags 400 payments
C = grid(tp=99, fn=1, fp=301, tn=9_599)
assert C["n"] == N and 99 + 301 == 400
assert C["rec"] == F(99, 100)                         # 99 % recall
assert C["prec"] == F(99, 400)                        # 24.75 %, "about one in four"
assert abs(C["prec"] - F(1, 4)) < F(1, 100)
assert C["acc"] == F(9_698, 10_000)                   # 96.98 %, "about ninety-seven percent", below the lazy model
assert C["acc"] < lazy["acc"]

# Costs (illustration): a missed fraud costs 500, a false alarm (a phone call) costs 5
MISS, ALARM = 500, 5
cost = lambda g_fn, g_fp: g_fn * MISS + g_fp * ALARM
assert cost(10, 30) == 5_150                          # Model A
assert cost(55, 5) == 27_525                          # Model B
assert cost(1, 301) == 2_005                          # Model C
assert cost(100, 0) == 50_000                         # Lazy model
# break-even: the analysts' time. If a false alarm instead cost 200 (a lost customer):
LOST = 200
assert 10 * MISS + 30 * LOST == 11_000                # A
assert 55 * MISS + 5 * LOST == 28_500                 # B
assert 1 * MISS + 301 * LOST == 60_700                # C now the worst

# ── Example 2: the screening test from the Bayes video (1,000 people, 1 in 100, catches 9 of 10, false alarm 1 in 10) ──
M = grid(tp=9, fn=1, fp=99, tn=891)
assert M["n"] == 1_000 and 9 + 1 == 10 and 99 + 891 == 990
assert F(99, 990) == F(1, 10)
assert M["rec"] == F(9, 10)
assert M["prec"] == F(9, 108) == F(1, 12)             # "one in twelve", same answer as the Bayes video
assert M["acc"] == F(900, 1_000) == F(9, 10)          # 90 % accurate
assert M["spec"] == F(9, 10)

# ── Example 3: spam filter, 1,000 emails, 300 spam ──
S = grid(tp=270, fn=30, fp=10, tn=690)
assert S["n"] == 1_000 and 270 + 30 == 300 and 10 + 690 == 700
assert 270 + 10 == 280                                # sent to the spam folder
assert S["prec"] == F(270, 280) == F(27, 28)          # ≈ 96.4 %
assert round(pct(S["prec"]), 1) == 96.4
assert S["rec"] == F(9, 10)                           # 90 %
assert S["acc"] == F(960, 1_000)                      # 96 %
assert S["f1"] == F(540, 580) == F(27, 29)            # ≈ 93.1 %
lazy_spam = grid(tp=0, fn=300, fp=0, tn=700)
assert lazy_spam["acc"] == F(7, 10)                   # balanced-ish classes: lazy model only 70 %

# ── Example 4 (your turn): loan defaults, 2,000 loans, 200 default ──
L = grid(tp=150, fn=50, fp=100, tn=1_700)
assert L["n"] == 2_000 and 150 + 50 == 200 and 100 + 1_700 == 1_800
assert 150 + 100 == 250                               # flagged
assert L["prec"] == F(150, 250) == F(3, 5)            # 60 %
assert L["rec"] == F(150, 200) == F(3, 4)             # 75 %
assert L["acc"] == F(1_850, 2_000) == F(37, 40)       # 92.5 %
assert L["f1"] == F(300, 450) == F(2, 3)              # ≈ 66.7 %, "two out of three"
assert 2 * L["prec"] * L["rec"] / (L["prec"] + L["rec"]) == F(2, 3)
assert grid(0, 200, 0, 1_800)["acc"] == F(9, 10)      # lazy model: 90 %

# Warm-up: ten payments, three fraud
W = grid(tp=2, fn=1, fp=2, tn=5)
assert W["n"] == 10 and 2 + 1 == 3
# Specificity of Detector A
assert A["spec"] == F(9_870, 9_900) and round(pct(A["spec"]), 1) == 99.7
# Same medical test, clinic where half are sick
K = grid(tp=450, fn=50, fp=50, tn=450)
assert K["n"] == 1_000 and K["rec"] == M["rec"] == F(9, 10)
assert F(50, 500) == F(1, 10)
assert K["prec"] == F(9, 10)

# Flag-everything detector
everything = grid(tp=100, fn=0, fp=9_900, tn=0)
assert everything["rec"] == 1 and everything["prec"] == F(1, 100)
assert F(100 + 1, 2) == F(101, 2)                     # plain average 50.5
assert everything["f1"] == F(200, 10_100) and round(pct(everything["f1"])) == 2
# Single-alarm detector: 1/1 precision
assert grid(tp=1, fn=99, fp=0, tn=9_900)["prec"] == 1

print("all numbers verified")
