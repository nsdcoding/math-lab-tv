#!/usr/bin/env python3
"""Check every number used in the narration and on screen with exact arithmetic (fractions).
Running example: five recent house sales on one street.
  size (sq ft): 1000, 1500, 2000, 2500, 3000   price ($ thousand): 140, 220, 250, 280, 360
Best line: price = 50 + 10 x (x = size in hundreds of sq ft)  i.e. $50k + $100 per sq ft."""
from fractions import Fraction as F

X = [10, 15, 20, 25, 30]          # hundreds of square feet
Y = [140, 220, 250, 280, 360]     # thousands of dollars
n = len(X)

def sse(a, b):  # line y = a + b x
    return sum((y - (a + b * x)) ** 2 for x, y in zip(X, Y))
def sae(a, b):
    return sum(abs(y - (a + b * x)) for x, y in zip(X, Y))
def res(a, b):
    return [y - (a + b * x) for x, y in zip(X, Y)]

# means: the average house
xb, yb = F(sum(X), n), F(sum(Y), n)
assert (xb, yb) == (20, 250)

# deviations and the slope formula
dx = [x - xb for x in X]; dy = [y - yb for y in Y]
assert dx == [-10, -5, 0, 5, 10] and dy == [-110, -30, 0, 30, 110]
prods = [a * b for a, b in zip(dx, dy)]
assert prods == [1100, 150, 0, 150, 1100] and sum(prods) == 2500
sq = [a * a for a in dx]
assert sq == [100, 25, 0, 25, 100] and sum(sq) == 250
b = F(sum(prods), sum(sq)); assert b == 10          # $10k per 100 sq ft = $100 per sq ft
a = yb - b * xb; assert a == 50                     # $50k

# best line: residuals and score
assert res(50, 10) == [-10, 20, 0, -20, 10]
assert sum(res(50, 10)) == 0
assert [r * r for r in res(50, 10)] == [100, 400, 0, 400, 100]
assert sse(50, 10) == 1000

# guess 1: flat line at the average price (callback: the mean)
assert res(250, 0) == [-110, -30, 0, 30, 110] and sum(res(250, 0)) == 0   # raw sum also zero -> raw sum is useless
assert sse(250, 0) == 26000
# guess 2: line through the first and last house: slope 220/20 = 11
b2 = F(360 - 140, 30 - 10); a2 = 140 - b2 * 10
assert (a2, b2) == (30, 11)
assert res(a2, b2) == [0, 25, 0, -25, 0] and sse(a2, b2) == 1250
# guess 3: too steep through the average house, slope 15 -> intercept -50
assert sse(-50, 15) == sum(r * r for r in res(-50, 15))
assert res(-50, 15) == [40, 45, 0, -45, -40] and sse(-50, 15) == 7250
# least squares really is the minimum: check a fine grid around it
best = min(((sse(F(a_, 4), F(b_, 40)), F(a_, 4), F(b_, 40))
            for a_ in range(-400, 801, 4) for b_ in range(200, 641, 4)), key=lambda t: t[0])
assert best == (1000, 50, 10), best
# pivoting about the average house and sliding: SSE is a bowl
assert sse(250 - 12 * 20, 12) == 1000 + 250 * 4 == 2000    # slope off by 2 adds 250*2^2
assert sse(60, 10) == 1000 + 5 * 100 == 1500                # slide up 10 adds 5*10^2

# absolute errors: the endpoint line scores better (50) than least squares (60)
assert sae(50, 10) == 60 and sae(a2, b2) == 50
# squaring punishes one big miss more than two small ones: 20 vs 10+10
assert 20 ** 2 == 400 and 10 ** 2 + 10 ** 2 == 200

# reading the line
assert a + b * 18 == 230            # 1,800 sq ft -> $230k
assert a + b * 19 - (a + b * 18) == 10   # +100 sq ft -> +$10k
assert a + b * 0 == 50              # 0 sq ft -> $50k (meaningless)
assert a + b * 100 == 1050          # 10,000 sq ft -> $1.05 million (extrapolation)
assert a + b * 2 == 70              # 200 sq ft shed -> $70k (extrapolation the other way)

# share of squared error removed (seed for the R-squared video)
assert 1 - F(1000, 26000) == F(25, 26)   # ~96%
assert round(float(F(25, 26)) * 100) == 96

# outlier: the 3,000 sq ft house sells for 560 instead of 360
Y2 = Y[:4] + [560]
yb2 = F(sum(Y2), n); assert yb2 == 290
b_o = F(sum((x - xb) * (y - yb2) for x, y in zip(X, Y2)), 250); assert b_o == 18
a_o = yb2 - b_o * xb; assert a_o == -70
assert a_o + b_o * 18 == 254        # 1,800 sq ft prediction moves from 230 to 254
print("all numbers verified")
