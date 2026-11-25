#!/usr/bin/env python3
"""YouTube package: title options, description (chapters from timings.json + related videos from the
channel tracker), tags, pinned comment, settings.
Owner override for this video: no ML / Data Science / Finance / CS sections (generic everyday examples only)."""
import math, pathlib, sys
from common import CHAPTERS, TIM, SEGS

HERE = pathlib.Path(__file__).resolve().parent
SLUG = "probability-one-hour"   # id in channel/catalog.json
OUT = HERE / "out" / "youtube"; OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(HERE.parent / "channel"))
import channel as ch  # noqa: E402

TITLES = [
    "Give Me One Hour and You'll FINALLY Understand PROBABILITY",
    "Give Me One Hour and You'll FINALLY Understand PROBABILITY (From Absolute Zero)",
    "Probability From Absolute Zero: Give Me One Hour and You'll FINALLY Get It",
]
TITLE = TITLES[0]   # recommended: the owner's title, keyword in caps

CH_TITLES = {
    "Game Night": "Game night: why 7 beats 12 six times over",
    "Welcome": "Welcome to Math Lab TV + what you'll learn",
    "Why It Matters": "Why probability matters in everyday life",
    "What Is Probability?": "What is probability? The 0-to-1 scale, fractions, decimals, percents",
    "Counting Outcomes": "Counting outcomes: sample space, events, coin trees",
    "Counting Bigger Things": "The multiplication rule: outfits and phone codes",
    "Putting Things in Order": "Orders and the lottery: 1 in 14 million",
    "Two Dice": "Two dice: the 36-square grid and the probability distribution",
    "Try It Many Times": "Law of large numbers: what happens over many tries",
    "Is This Die Fair?": "Is this die fair? Predict, then compare",
    "Quick Recap": "Halfway recap",
    "The Word NOT": "NOT: the complement rule, 1 − P(A)",
    "Odds Versus Probability": "Odds vs probability (and how to convert)",
    "The Word OR": "OR: the addition rule and the overlap",
    "The Word AND": "AND: the multiplication rule",
    "Independent or Not?": "Independent or not? Five quick examples",
    "At Least One": "At least one: flip it around",
    "A Deck of Cards": "NOT, OR, AND with a deck of cards",
    "Two Step Trees": "Two-step tree diagrams: rain and a late bus",
    "Given That": "Conditional probability: a clue shrinks the grid",
    "Expected Value": "Expected value: is a game worth playing?",
    "Measuring Instead of Counting": "Measuring instead of counting: lengths and areas",
    "More Dice, New Shapes": "More dice: how the bell curve appears",
    "Practice Round": "Practice round: 10 questions to try yourself",
    "Common Mistakes": "Common mistakes: gambler's fallacy and 4 more traps",
    "Recipe": "Your probability recipe in 8 steps",
    "Subscribe": "Look around your world + subscribe",
}

TAGS = ["probability", "probability for beginners", "probability explained", "learn probability", "basic probability",
        "probability from scratch", "conditional probability", "expected value", "law of large numbers",
        "gambler's fallacy", "dice probability", "tree diagrams", "complement rule", "addition rule",
        "multiplication rule", "odds vs probability", "probability distribution", "statistics for beginners",
        "math for beginners", "math explained", "Math Lab TV"]


def ts(t):
    t = int(math.floor(t)); m, s = divmod(t, 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def main():
    total = TIM["total"]; mins = round(total / 60)
    rows = []
    for k, c in enumerate(CHAPTERS):
        start = 0.0 if k == 0 else c["t0"]
        end = CHAPTERS[k + 1]["t0"] if k + 1 < len(CHAPTERS) else total
        assert end - start >= 10, c["name"]
        rows.append(f"{ts(start)} {CH_TITLES[c['name']]}")
    at = lambda sid: ts(SEGS[sid]["start"])
    related = ch.desc_block(ch.load(), SLUG)
    desc = f"""Probability explained from absolute zero, for complete beginners: give me one hour and you'll finally understand probability.
Learn what a probability is, how to count outcomes, the NOT / OR / AND rules, independence, conditional probability, expected value and the traps that fool almost everyone, all with pictures.

It's game night. You need a 12 with two dice; your friend needs a 7. Most people think it's even. It isn't: 7 comes up six times more often. In this {mins}-minute lesson for people who don't think of themselves as "math people", we start from zero and count our way to the answer, then keep going.

⏱ CHAPTERS
""" + "\n".join(rows) + f"""

📐 KEY RULES
• Probability = outcomes you want ÷ all outcomes (only when every outcome is equally likely)
• NOT: P(not A) = 1 − P(A)
• OR: P(A or B) = P(A) + P(B) − P(A and B)   (the last part is the overlap; it's 0 if they can't happen together)
• AND: P(A and B) = P(A) × P(B after A)   (just P(A) × P(B) when they are independent)
• At least one: P(at least one) = 1 − P(none)
• Given: P(A | B) = outcomes in both A and B ÷ outcomes in B   ("|" means "given")
• Expected value = the average result per try over many tries
P( ) means "the probability of"; A and B are any events (groups of outcomes).

✅ WORKED ANSWERS
• Two dice: 36 equally likely outcomes · total 7: 6/36 = 1/6 · total 12: 1/36
• Not a 7: 5/6 · 7 or 11: 8/36 · orange 6 or blue 6: 11/36 · double six: 1/36
• Two coins, one head and one tail: 1/2 · three coins, exactly two heads: 3/8
• At least one 6 in four rolls: 1 − (5/6)⁴ = 671/1296 ≈ 52% (not 67%)
• Cards: king or heart 16/52 = 4/13 · two aces without putting back 1/221
• Bus late (illustration: rain 3/10, late 1/2 if rain, 1/10 if dry): 22/100; raining given late: 15/22 ≈ 68%
• Given the orange die shows 6: total 12 → 1/6, total 7 → 1/6 (unchanged: independent)
• Fair-stall game (pay 2, win 10 on a 7): expected loss ≈ 1/3 token per game
• Lottery, 6 numbers from 49: 13,983,816 possible tickets

🧭 THE RECIPE
1. List all outcomes (grid or tree; equally likely)
2. Count and divide: wanted ÷ all
3. NOT: 1 − P(A)
4. OR: add, then remove the overlap
5. AND: multiply along the path, using the updated chance
6. AT LEAST ONE: 1 − P(none)
7. GIVEN: shrink the world, then count
8. LONG RUN: probability describes patterns over many tries, not the next single try

{related + chr(10) + chr(10) if related else ''}🔔 For more mathematics, explained simply and visually, subscribe to Math Lab TV.

#probability #math #statistics
"""
    tag_str = ", ".join(TAGS)
    assert all(len(t) < 100 for t in TITLES), [len(t) for t in TITLES]
    assert len(tag_str) < 500, len(tag_str)
    s = {c["name"]: ts(0 if k == 0 else c["t0"]) for k, c in enumerate(CHAPTERS)}
    pinned = f"""📌 Quick summary: count what you want, count everything, divide. Then three words do almost all the work: NOT (1 − P), OR (add, remove the overlap) and AND (multiply along the path). A clue shrinks the world ({s['Given That']}), and probability describes the long run, not the next try ({s['Try It Many Times']}).

Worth adding:
1️⃣ The rain-and-bus numbers ({s['Two Step Trees']}) and the class examples are made up for illustration, so the counting comes out in whole numbers.
2️⃣ The coin and dice charts in "Try It Many Times" are computer simulations of fair coins and dice; your own runs will look a little different, and that's the point.
3️⃣ Lottery odds depend on the game: we used the classic "6 numbers from 49" format ({s['Putting Things in Order']}).

Which practice question tripped you up? 👇"""
    settings = f"""Category: Education
Language: English · Captions: upload out/captions.srt (English)
Audience: Not made for kids
License: Standard YouTube License · Allow embedding: on
Chapters: automatic from the description timestamps (first at 0:00, all ≥ 10 s)
Thumbnails: upload thumbnail_A.png and thumbnail_B.png to "Test & compare"
End screen: subscribe element + a related video in the last 20 s · Comments: on · pin pinned_comment.txt
Video length: {ts(total)} ({total:.1f} s)"""
    (OUT / "title.txt").write_text("\n".join(f"{'★ ' if t == TITLE else '  '}{t}  ({len(t)} chars)" for t in TITLES) + "\n")
    (OUT / "description.txt").write_text(desc)
    (OUT / "tags.txt").write_text(tag_str + "\n")
    (OUT / "pinned_comment.txt").write_text(pinned + "\n")
    (OUT / "settings.txt").write_text(settings + "\n")
    for t in TITLES: print(f"{len(t):3d}  {t}")
    print(f"tags: {len(tag_str)} chars | description: {len(desc)} chars")
    print("\n".join(rows))


if __name__ == "__main__":
    main()
