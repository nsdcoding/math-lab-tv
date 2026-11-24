#!/usr/bin/env python3
"""YouTube package: title options, description (chapters from timings.json + related videos from the
channel tracker), tags, pinned comment, settings.  see bayes-theorem/package.py for the pattern."""
import math, pathlib, sys
from common import CHAPTERS, TIM, SEGS

HERE = pathlib.Path(__file__).resolve().parent
SLUG = "linear-regression"   # id in channel/catalog.json
OUT = HERE / "out" / "youtube"; OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(HERE.parent / "channel"))
import channel as ch  # noqa: E402

TITLES = [
    "Linear Regression Explained: Find the Best Line by Hand | ML, Data Science, Finance, CS",
    "Linear Regression for Beginners: Least Squares, Slope and Intercept | ML, Data Science, Finance",
    "Linear Regression Explained Visually: Why We Square the Errors (ML, Data Science, Finance, CS)",
]
TITLE = TITLES[0]                                   # recommended
CH_TITLES = {
    "The Fair Price": "Two agents, two prices: what is the house really worth?",
    "Welcome": "Welcome to Math Lab TV + what you'll learn",
    "Why It Matters": "Why it matters: the first model in machine learning",
    "Measuring a Miss": "Residuals: measuring a miss straight up and down",
    "Scoring a Line": "Least squares: why we square the errors",
    "The Formula": "The slope and intercept formula, worked by hand",
    "Reading the Line": "Reading the line: slope as a rate, the intercept, a prediction",
    "Prediction vs Extrapolation": "Prediction vs extrapolation",
    "A Line Is Not a Cause": "Correlation is not causation",
    "Big Picture": "Machine learning, data science, finance & computer science",
    "Common Mistakes": "3 common mistakes (+ a bonus)",
    "Recipe": "Recipe recap: linear regression in five steps",
    "Subscribe": "Look around your world + subscribe",
    "Next Time": "Next: gradient descent",
}
DOMAIN_SEGS = dict(ml="s098", ds="s100", fin="s101", cs="s102")   # first segment of each domain part
LINES = dict(
    first2="Linear regression explained from scratch, with real uses in Machine Learning (ML), Data Science (DS), Finance and Computer Science (CS).\n"
           "Learn least squares, residuals, the sum of squared errors, slope and intercept, prediction vs extrapolation, and why correlation is not causation.",
    hook="You want to sell your 1,800 sq ft house. One agent says $260,000, another says $200,000. Five houses on your street sold last year, "
         "and a ruler line through them gives a different price for everyone who draws it. Linear regression finds the one best line, "
         "and here the fair price comes out at $230,000.",
    domains=dict(ml="linear regression is the first model you train: the score is the loss, training finds the smallest loss",
                 ds="trend lines, e.g. how much sales rise per extra $1,000 of advertising",
                 fin="a stock's beta is the slope of its moves against the market's moves",
                 cs="fit run time against input size; the slope is the cost per item (and predicting huge jobs is extrapolation)"),
    formulas="• Line: y = a + b·x   (y = price, x = size, b = slope, a = intercept)\n"
             "• Residual (miss) = actual − predicted, measured straight up and down\n"
             "• Score: sum of squared errors = Σ (miss)²   (Σ = add them all up)\n"
             "• Slope: b = Σ(x − x̄)(y − ȳ) ÷ Σ(x − x̄)²   (x̄, ȳ = the averages)\n"
             "• Intercept: a = ȳ − b·x̄   (the best line always passes through the average point)",
    worked="Five sales: 1,000 sq ft $140k · 1,500 $220k · 2,000 $250k · 2,500 $280k · 3,000 $360k\n"
           "• Average house: 2,000 sq ft, $250k\n"
           "• Size in hundreds of sq ft: Σ(x − x̄)(y − ȳ) = 2,500 · Σ(x − x̄)² = 250 → slope 10 ($100 per sq ft)\n"
           "• Intercept: 250 − 10 × 20 = 50 → price = $50,000 + $100 per sq ft\n"
           "• Misses: −10, +20, 0, −20, +10 → sum of squared errors 1,000 (in $ thousand²)\n"
           "• Other lines: flat at the average 26,000 · through the end houses 1,250 · too steep 7,250\n"
           "• 1,800 sq ft → $230k (give or take about $20k) · 10,000 sq ft → $1.05M is extrapolation\n"
           "• One outlier ($560k instead of $360k) moves the slope to $180 per sq ft and the 1,800 sq ft price to $254k\n"
           "(Illustrative house prices, not real sales.)",
    recipe="1. Plot and look: the dots should lean along a line\n"
           "2. Measure the misses: straight up and down, in the units you predict\n"
           "3. Square and add: that total is the score (sum of squared errors)\n"
           "4. Find the best line: slope from the formula, then the intercept from the average point\n"
           "5. Read and predict: the slope is a rate; predict only inside your data\n"
           "\"A line does not know the truth. It is just the one guess that misses least.\"",
    next="Gradient descent. Five houses had a formula, but a modern AI model has millions of settings and none. "
         "Next time: how it finds its smallest score by feeling which way is downhill.",
    pinned_extra="1️⃣ Squaring is a choice ({s057}). With plain distances (least absolute deviations) a different line can win, "
                 "like the median vs the mean. Least squares is the standard because it gives one clean formula.\n"
                 "2️⃣ The slanted (perpendicular) distance belongs to a different method, total least squares, used when both "
                 "numbers are measured with error ({s029}).\n"
                 "3️⃣ Beta ({s101}): a beta above 1 is a rule of thumb for 'swings more than the market', measured over a past period.",
)
TAGS = ["linear regression", "linear regression explained", "least squares", "line of best fit", "slope and intercept",
        "residuals", "sum of squared errors", "regression analysis", "correlation vs causation",
        "machine learning", "statistics for machine learning", "data science",
        "statistics for data science", "finance", "statistics for finance", "computer science", "ML", "DS", "CS",
        "statistics explained", "Math Lab TV"]


def ts(t):
    t = int(math.floor(t)); m, s = divmod(t, 60)
    return f"{m}:{s:02d}"


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
    d = LINES["domains"]
    desc = f"""{LINES['first2']}

{LINES['hook']} A {mins}-minute explainer for people who don't think of themselves as "math people".

⏱ CHAPTERS
""" + "\n".join(rows) + f"""

🌍 WHERE YOU'LL USE IT
• Machine Learning / ML ({at(DOMAIN_SEGS['ml'])}): {d['ml']}
• Data Science / DS ({at(DOMAIN_SEGS['ds'])}): {d['ds']}
• Finance ({at(DOMAIN_SEGS['fin'])}): {d['fin']}
• Computer Science / CS ({at(DOMAIN_SEGS['cs'])}): {d['cs']}

📐 KEY FORMULAS
{LINES['formulas']}

✅ WORKED EXAMPLE
{LINES['worked']}

🧭 THE RECIPE
{LINES['recipe']}

{related + chr(10) + chr(10) if related else ''}▶ NEXT VIDEO: {LINES['next']}

#machinelearning #datascience #statistics
"""
    tag_str = ", ".join(TAGS)
    assert all(len(t) < 100 for t in TITLES), [len(t) for t in TITLES]
    assert len(tag_str) < 500, len(tag_str)
    extra = LINES["pinned_extra"].format(**{k: at(k) for k in ("s057", "s029", "s101")})
    pinned = (f"📌 Quick summary: linear regression finds the line with the smallest sum of squared errors. For our five houses "
              f"that is $50,000 + $100 per sq ft, so 1,800 sq ft → about $230k ({at('s081')}). Trust it only inside your data "
              f"({at('s084')}), and remember a line shows that things move together, not why ({at('s090')}).\n\n"
              f"Worth adding:\n{extra}\n\nWhat two numbers in your life seem to climb together? A line, a curve, or a coincidence? 👇")
    settings = f"""Category: Education
Language: English · Captions: upload out/captions.srt (English)
Audience: Not made for kids
License: Standard YouTube License · Allow embedding: on
Chapters: automatic from the description timestamps (first at 0:00, all ≥ 10 s)
Thumbnails: upload thumbnail_A.png and thumbnail_B.png to "Test & compare"
End screen: link the next video in the last 20 s · Comments: on · pin pinned_comment.txt
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
