#!/usr/bin/env python3
"""Check every number in the narration and on screen."""
LS, TROUGH1, HEAD, TROUGH2, RS, START = 60, 52, 70, 52, 61, 32
NECK = 52
assert TROUGH1 == TROUGH2 == NECK
assert HEAD > LS and HEAD > RS and RS < HEAD           # head highest, right shoulder a lower high
height = HEAD - NECK; assert height == 18
target = NECK - height; assert target == 34
stop = RS; risk = stop - NECK; reward = NECK - target
assert (risk, reward) == (9, 18) and reward / risk == 2
assert HEAD - TROUGH1 == 18 and RS - TROUGH2 == 9      # "+18, then +9" rallies from the dips
print("all numbers verified")
