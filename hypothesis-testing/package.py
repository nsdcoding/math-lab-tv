#!/usr/bin/env python3
"""YouTube package: title options, description (chapters from timings.json + related videos from the
channel tracker), tags, pinned comment, settings."""
import math, pathlib, sys
from common import CHAPTERS, TIM, SEGS

HERE = pathlib.Path(__file__).resolve().parent
SLUG = "hypothesis-testing"   # id in channel/catalog.json
OUT = HERE / "out" / "youtube"; OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(HERE.parent / "channel"))
import channel as ch  # noqa: E402

TITLES = [
    "Hypothesis Testing & p Values Explained Visually: Is This Coin Rigged? | ML, Data Science, Finance",
    "Hypothesis Testing Explained: What a p Value Really Means | ML, Data Science, Finance, CS",
    "p Values Without the Confusion: Hypothesis Testing With One Coin | ML, Data Science, Finance, CS",
]
TITLE = TITLES[0]                                   # recommended
CH_TITLES = {
    "The Coffee Coin": "The coffee coin: 15 heads in 20 flips. Rigged?",
    "Welcome": "Welcome to Math Lab TV",
    "Why It Matters": "Why p values matter (and the puzzle from the Bayes video)",
    "The Boring Explanation": "The null hypothesis: the boring explanation",
    "A Thousand Fair Coins": "What a p value measures: the tail area",
    "Drawing the Line": "Significance level (alpha): a line somebody chose",
    "What p Is Not": "Three things a p value is NOT",
    "Two Ways to Be Wrong": "Type I and type II errors (false alarms and misses)",
    "Tiny p, Tiny Effect": "A tiny p value is not a big effect",
    "Real World": "Where you'll use it: ML, Data Science, Finance, CS",
    "Common Mistakes": "Common mistakes: flipped question, p-hacking, 'no effect'",
    "Recipe": "The 5-step recipe",
    "Subscribe": "Subscribe",
    "Next Time": "Next time: the prosecutor's fallacy",
}
DOMAIN_SEGS = dict(ml="s093", ds="s091", fin="s095", cs="s097")   # first segment of each domain part
CARD_SEGS = [("s015a", "Bayes' Theorem Explained Simply"), ("s034a", "Standard Deviation and Variance"),
             ("s102", "Bayes' Theorem Explained Simply")]   # moments the narration points to the card at the top
LINES = dict(
    first2="Hypothesis testing and p values explained visually, for Machine Learning (ML), Data Science (DS), Finance and Computer Science (CS).\n"
           "See exactly what a p value measures, what a significance level is, type I and type II errors, and the traps that fool even scientists.",
    hook="Your friend's coin decides who pays for coffee, and in a month it lands heads 15 times out of 20. Is it rigged, or just luck? "
         "If the coin were fair, only about 21 of 1,000 people would get 15 or more heads: a p value of about 0.02.",
    domains=dict(ml="is model B really better than model A, or did it get a luckier test set? Shuffle tests and regression p values.",
                 ds="A/B tests: would a click gap this big appear by chance alone if the button made no difference?",
                 fin="did a backtested strategy beat the market, or was the profit luck? Test many strategies and some win by chance.",
                 cs="is new code really faster, or is the speed-up just timing noise? Run it many times and test."),
    formulas=("• p = P(data at least this extreme | H₀)\n"
              "  p = the p value · P = probability · | = given, assuming · H₀ = the null hypothesis (the boring explanation: the coin is fair)\n"
              "• Reject H₀ when p < α\n"
              "  α (alpha) = the significance level: a cut-off chosen BEFORE you look, often 0.05 (1 in 20)"),
    worked=("• 20 flips of a fair coin can land 1,048,576 ways; 21,700 of them have 15+ heads → p = 21,700 ÷ 1,048,576 ≈ 0.021\n"
            "• Two-sided (rigged either way): p ≈ 0.041 · 14 heads: p ≈ 0.058 (not significant at 0.05)\n"
            "• False alarms with 'rigged at 15+': ≈ 2.1% · a coin that lands heads 70% of the time is caught ≈ 42%, missed ≈ 58%\n"
            "• 100 flips, cut-off 59: false alarms ≈ 4.4%, the 70% coin caught ≈ 99%\n"
            "• A 50.2% coin over a million flips: 502,000 heads, p ≈ 0.00003, yet only ≈ 2 extra coffees per 1,000\n"
            "• If 1 coin in 100 is rigged, a coin with 15+ heads is still fair ≈ 83% of the time (rigged ≈ 17%)\n"
            "• 20 tests of nothing at 0.05: ≈ 64% chance at least one looks significant"),
    recipe=("1. State the null: the boring explanation\n2. Choose α first, before you look (often 0.05)\n"
            "3. Picture chance: the distribution if H₀ is true\n4. Find the tail: the share at least as extreme as your result\n"
            "5. Decide, then size it: p vs α, and always report the effect size"),
    next="The prosecutor's fallacy: a 1 in a million chance an innocent person matches the evidence is not a 1 in a million chance they're innocent.",
    pinned_extra=("• {t_two} The test here is one-sided (heads only). If you suspect the coin is off either way, count both tails: p ≈ 0.041.\n"
                  "• {t_bayes} The 1-in-100 rigged-coin town is an illustration; the real chance a coin is rigged depends on how common rigged coins are.\n"
                  "• {t_ml} Model accuracies and the regression table are illustrations, not real results.\n"
                  "• {t_tiny} The million-flip p value uses the normal approximation (exact binomial agrees: ≈ 0.00003)."),
)
TAGS = ["hypothesis testing", "p value", "p values explained", "null hypothesis", "significance level", "type 1 error",
        "type 2 error", "statistical significance", "p hacking", "machine learning", "statistics for machine learning",
        "data science", "statistics for data science", "A/B testing", "finance", "statistics for finance", "computer science",
        "ML", "DS", "CS", "statistics explained", "Math Lab TV"]


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
    extra = LINES["pinned_extra"].format(t_two=at("s047"), t_bayes=at("s101"), t_ml=at("s093"), t_tiny=at("s086"))
    pinned = ("📌 Quick summary: a p value is the chance of seeing data at least this extreme IF the boring explanation (H₀) were true. "
              "It is not the chance H₀ is true, not the size of the effect, and a big p value is not proof of nothing.\n\n"
              f"Worth adding:\n{extra}\n\nWhat's a result you've seen called 'significant' that you now want to check? 👇")
    cards = "\n".join(f"{at(sid)}  card → {title}" for sid, title in CARD_SEGS)
    settings = f"""Category: Education
Language: English · Captions: upload out/captions.srt (English)
Audience: Not made for kids
License: Standard YouTube License · Allow embedding: on
Chapters: automatic from the description timestamps (first at 0:00, all ≥ 10 s)
Thumbnails: upload thumbnail_A.png and thumbnail_B.png to "Test & compare"
End screen: link the next video in the last 20 s · Comments: on · pin pinned_comment.txt
YouTube cards (the narration says "in the card at the top" at these moments):
{cards}
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
