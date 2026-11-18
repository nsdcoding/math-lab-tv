#!/usr/bin/env python3
"""Check every number used in the narration and on screen with exact arithmetic (fractions).
Run it before checkpoint 1."""
from fractions import Fraction as F
from math import comb

MATCH = F(1, 1_000_000)           # chance a random innocent person matches the partial DNA trace


def p_guilty_given_match(pop):
    """Culprit is one of `pop` people, equally likely a priori; the culprit always matches."""
    innocent = pop - 1
    return F(1, 1) / (1 + innocent * MATCH)


# ── Running example: a city of eight million ──
CITY = 8_000_000
innocent_matches = (CITY - 1) * MATCH
assert innocent_matches == F(7_999_999, 1_000_000)            # 7.999999 -> "about eight"
assert round(innocent_matches) == 8
pg = p_guilty_given_match(CITY)
assert pg == F(1_000_000, 8_999_999)                          # ≈ 0.1111 -> "about one in nine"
assert abs(pg - F(1, 9)) < F(1, 10**7)
pi = 1 - pg
assert abs(pi - F(8, 9)) < F(1, 10**7)                        # ≈ 89 % innocent
assert round(float(pi) * 100) == 89
# "almost nine hundred thousand times bigger"
ratio = pi / MATCH
assert 888_000 < ratio < 889_000
# Each block of one million people holds about one innocent match
assert 1_000_000 * MATCH == 1

# ── Base rate: the same one-in-a-million in different crowds ──
VILLAGE, COUNTRY = 1_000, 60_000_000
assert (VILLAGE - 1) * MATCH == F(999, 1_000_000)             # about one in a thousand chance of any innocent match
pv = p_guilty_given_match(VILLAGE)
assert pv > F(999, 1000)                                      # "about nine hundred and ninety nine in a thousand"
assert round((COUNTRY - 1) * MATCH) == 60                     # about sixty innocent matches
pc = p_guilty_given_match(COUNTRY)
assert abs(pc - F(1, 61)) < F(1, 10**6)                       # about one in sixty one

# ── Callback: Bayes screening test (bayes-examples) ──
people, sick = 1000, 10
caught = F(9, 10) * sick
healthy = people - sick
false_pos = F(1, 10) * healthy
assert (caught, healthy, false_pos) == (9, 990, 99)
assert false_pos / (caught + false_pos) == F(11, 12)          # P(healthy | positive) = eleven in twelve
assert caught / (caught + false_pos) == F(1, 12)              # one in twelve really has it

# ── Callback: coffee coin (hypothesis-testing) ──
tail = sum(comb(20, k) for k in range(15, 21))
assert tail == 21_700 and 2**20 == 1_048_576
p_value = F(tail, 2**20)
assert round(float(p_value), 3) == 0.021                      # "about two in a hundred"
p70 = sum(comb(20, k) * F(7, 10)**k * F(3, 10)**(20 - k) for k in range(15, 21))
prior = F(1, 100)
post_rigged = prior * p70 / (prior * p70 + (1 - prior) * p_value)
assert round(float(post_rigged) * 100) == 17                  # about seventeen in a hundred rigged
assert round(float(1 - post_rigged) * 100) == 83              # so about eighty three in a hundred still fair

# ── A real case (England, 1999): one in 8,543 squared ──
assert 8543**2 == 72_982_849                                  # "about one in seventy three million"
assert round(8543**2 / 1e6) == 73

# ── Machine Learning: face matching at a stadium ──
crowd, fm = 50_000, F(1, 10_000)
false_faces = (crowd - 1) * fm
assert round(false_faces) == 5                                # about five false matches
assert abs(F(1, 1) / (1 + false_faces) - F(1, 6)) < F(1, 10**4)   # about one alert in six is the right person

# ── Data Science: A/B test, same numbers as the coin (prior 1 in 100 real effects) ── (uses coin above)

# ── Finance: card-fraud flags ──
honest, fraud = 1_000_000, 100
fraud_caught = F(9, 10) * fraud
false_flags = honest * F(1, 1000)
assert (fraud_caught, false_flags) == (90, 1000)
prec = fraud_caught / (fraud_caught + false_flags)
assert prec == F(9, 109)
assert round(1 / float(prec)) == 12                           # about one flag in twelve is real fraud

# ── Computer Science: searching a database of five million profiles ──
assert 5_000_000 * MATCH == 5                                 # about five innocent hits, even if the culprit isn't in it

print("all numbers verified")
