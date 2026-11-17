#!/usr/bin/env python3
"""Check every number used in the narration and on screen with exact arithmetic (fractions)."""
from fractions import Fraction as F
from math import comb, erfc, sqrt, lgamma, log, exp

H = F(1, 2)
def pmf(n, k, p=H): return comb(n, k) * p**k * (1 - p)**(n - k)
def tail(n, k, p=H): return sum(pmf(n, i, p) for i in range(k, n + 1))
def r(x, d): return round(float(x), d)

# 20 flips, fair coin
assert 2**20 == 1048576
assert sum(comb(20, k) for k in range(15, 21)) == 21700
p15 = tail(20, 15); assert p15 == F(21700, 1048576) and r(p15, 3) == 0.021
assert r(2 * p15, 3) == 0.041                                      # two-sided
p14 = tail(20, 14); assert r(p14, 3) == 0.058 and p14 > F(1, 20) > p15  # line falls between 14 and 15
assert round(1000 * pmf(20, 10)) == 176                            # ~176 of 1,000 get exactly 10
assert round(1000 * pmf(20, 15)) == 15                             # ~15 get exactly 15
assert round(1000 * p15) == 21                                     # ~21 get 15 or more
sd = sqrt(20 * 0.25); assert round(sd, 1) == 2.2 and (15 - 10) / sd > 2  # spread ~2.2, 15 is >2 spreads out
assert r(tail(5, 4), 3) == 0.188                                   # 5 flips, 4 heads: big p
# errors
assert r(p15, 3) == 0.021                                          # false alarm rate ~2.1%
power20 = tail(20, 15, F(7, 10)); assert round(float(power20) * 100) == 42  # caught 42%, missed 58%
assert 20 * F(7, 10) == 14                                         # 70% coin centred at 14
assert tail(100, 59) < F(1, 20) < tail(100, 58)                    # 100 flips: cut-off 59
assert float(tail(100, 59)) < 0.05
assert round(float(tail(100, 59, F(7, 10))) * 100) == 99           # caught ~99%
# Bayes (illustration): 1 in 100 coins rigged at 70%
post = F(1, 100) * power20 / (F(1, 100) * power20 + F(99, 100) * p15)
assert round(float(post) * 100) == 17 and abs(float(post) - 1 / 6) < 0.01
# tiny effect: a million flips
n, k0 = 10**6, 502000
assert sqrt(n * 0.25) == 500 and (k0 - n // 2) / 500 == 4
lp = lambda k: lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1) - n * log(2)
pm = sum(exp(lp(k)) for k in range(k0, k0 + 5000)); assert round(pm, 5) == 0.00003
assert F(502, 1000) - F(500, 1000) == F(2, 1000)                   # ~2 extra coffees per 1,000
# multiple testing
assert round((1 - 0.95**20) * 100) == 64
# thresholds
assert round(1 / (0.5 * erfc(5 / sqrt(2))) / 1e6, 1) == 3.5        # 5 sigma ~ 1 in 3.5 million
# on-screen extras: Bayes count with 10,000 coins (1 in 100 rigged at 70% heads)
rig_hits = 100 * power20; fair_hits = 9900 * p15
assert round(float(rig_hits)) == 42 and round(float(fair_hits)) == 205
assert round(float(rig_hits / (rig_hits + fair_hits)) * 100) == 17 and round(float(fair_hits / (rig_hits + fair_hits)) * 100) == 83
# 70% coin over 20 flips peaks at 14 heads (~192 of 1,000); 100 flips: fair peak ~80, 70% peak ~87 per 1,000
assert max(range(21), key=lambda k: pmf(20, k, F(7, 10))) == 14 and round(float(1000 * pmf(20, 14, F(7, 10)))) == 192
assert round(float(1000 * pmf(100, 50, H))) == 80 and round(float(1000 * pmf(100, 70, F(7, 10)))) == 87
assert 3_500_000 // 20 == 175_000                                    # physics line vs 1 in 20
assert round(float(tail(5, 4)), 2) == 0.19                          # 5 flips, 4 heads: p ≈ 0.19
# trade-off bars shown in "Two Ways to Be Wrong" (false-alarm % and miss % for each cut-off)
for c_, fa, miss in [(13, 13.2, 22.8), (14, 5.8, 39.2), (15, 2.1, 58.4), (16, 0.6, 76.2)]:
    assert round(float(tail(20, c_)) * 100, 1) == fa and round((1 - float(tail(20, c_, F(7, 10)))) * 100, 1) == miss
assert round(float(tail(100, 59)) * 100, 1) == 4.4 and round((1 - float(tail(100, 59, F(7, 10)))) * 100, 1) == 0.7
# "Tiny p" chart: p for a 50.2% coin that shows exactly 50.2% heads, by number of flips (normal approximation)
def p_at(n): return 0.5 * erfc((0.002 * sqrt(n) / 0.5) / sqrt(2))
assert [round(p_at(10 ** e), 2) for e in (2, 3, 4, 5)] == [0.48, 0.45, 0.34, 0.10] and p_at(10 ** 5.5) < 0.05 < p_at(10 ** 5)
assert round(p_at(10 ** 6), 5) == 0.00003
print("all numbers verified")
