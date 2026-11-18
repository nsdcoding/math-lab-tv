#!/usr/bin/env python3
"""YouTube package: title options, description (chapters from timings.json + related videos from the
channel tracker), tags, pinned comment, settings.  FILL every constant below; see bayes-theorem/package.py."""
import math, pathlib, sys
from common import CHAPTERS, TIM, SEGS

HERE = pathlib.Path(__file__).resolve().parent
SLUG = "prosecutors-fallacy"   # id in channel/catalog.json
OUT = HERE / "out" / "youtube"; OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(HERE.parent / "channel"))
import channel as ch  # noqa: E402

TITLES = [
    "The Prosecutor's Fallacy Explained Visually: Why 1 in a Million Isn't Proof | ML, Data Science",
    "Prosecutor's Fallacy: Why 1 in a Million Evidence Can Mean Innocent | ML, Data Science, Finance, CS",
    "The Statistics Trap Smart People Fall For: The Prosecutor's Fallacy | ML, Data Science, Finance, CS",
]
TITLE = TITLES[0]                                   # recommended
CH_TITLES = {
    "One in a Million": "A 1 in a million DNA match: is Sam guilty?",
    "Welcome": "Welcome to Math Lab TV",
    "Two Different Questions": "P(match | innocent) vs P(innocent | match): two different questions",
    "Why the Swap Matters": "Why swapping them matters (dogs and four legs)",
    "Count the Crowd": "Count the crowd: 8 million people, about 9 matches",
    "The Formula Behind It": "The counting rule (and Bayes' theorem)",
    "The Missing Piece": "The base rate: the piece the prosecutor left out",
    "When Other Evidence Counts": "How other evidence changes the answer",
    "A Real Courtroom": "A real case: 1 in 73 million",
    "The Same Swap in Medicine": "The same swap in medical testing",
    "Where You'll Use It": "Where you'll use it: ML, Data Science, Finance, CS",
    "Spot the Swap": "Quiz: spot the swap",
    "Common Mistakes": "Common mistakes (including the defense attorney's fallacy)",
    "Recipe": "The 5-step recipe to catch the swap",
    "Subscribe": "Subscribe",
    "Next Time": "Next time: the confusion matrix",
}
DOMAIN_SEGS = dict(ml="s089", ds="s092", fin="s094", cs="s097")   # first segment of each domain part
CARD_SEGS = [("s016", "Hypothesis Testing and p Values Without the Confusion"),
             ("s058", "Bayes Theorem Explained Simply, With Real Examples"),
             ("s082", "Bayes Theorem Explained Simply, With Real Examples")]   # callbacks in the narration
LINES = dict(
    first2="The prosecutor's fallacy explained visually, for Machine Learning (ML), Data Science (DS), Finance and Computer Science (CS).\n"
           "See why P(evidence | innocent) is not P(innocent | evidence), how to count the crowd, and why the base rate is the missing piece.",
    hook="In a city of 8 million people, Sam's DNA matches a partial trace from a crime scene. An expert says an innocent person "
         "would match only 1 time in a million, and the prosecutor says that means a 1 in a million chance Sam is innocent. "
         "Count the crowd, and about 8 innocent people match too: Sam is innocent about 8 times in 9.",
    domains=dict(ml="a face-matching camera with 1 false match in 10,000, scanning 50,000 fans: about 5 false alerts + 1 real, so an alert is right only about 1 time in 6.",
                 ds="a p value is P(results this extreme | nothing going on), not P(nothing going on | results). Same coin, p ≈ 0.021, can still be fair ≈ 83% of the time.",
                 fin="a fraud model that wrongly flags 1 honest payment in 1,000: per million honest payments and 100 frauds, 90 ÷ 1,090 ≈ 1 flag in 12 is real fraud.",
                 cs="search 5 million DNA profiles for a 1 in a million match and expect about 5 innocent hits, even if the culprit isn't in the database."),
    formulas=("• P(A | B) = the chance of A, given B (the bar | means 'given': we already know B)\n"
              "• P(match | innocent) = 1 in 1,000,000 is NOT P(innocent | match)\n"
              "• P(guilty | match) = guilty people who match ÷ everyone who matches\n"
              "  = 1 ÷ (1 + 8) = 1/9 in the city example (Bayes' theorem, done by counting)"),
    worked=("• City of 8,000,000: 7,999,999 innocent × 1 in a million ≈ 8 innocent matches, + 1 culprit = 9\n"
            "• P(guilty | match) ≈ 1 in 9 · P(innocent | match) ≈ 8 in 9 ≈ 89% (about 889,000× bigger than 1 in a million)\n"
            "• Same trace, different crowd: village of 1,000 → ≈ 999 in 1,000 guilty · country of 60 million → ≈ 1 in 61\n"
            "• Before the match Sam was 1 in 8,000,000; after it, 1 in 9: strong evidence, not proof\n"
            "• Medical test (from the Bayes video): P(positive | healthy) = 1 in 10, but P(healthy | positive) = 99 ÷ 108 = 11 in 12\n"
            "• Real case: 1 in 8,543 squared ≈ 1 in 73 million (two errors: treating the deaths as unrelated, and the swap)"),
    recipe=("1. Find the given: what does the number assume is true?\n2. Flip it: is that the question you actually care about?\n"
            "3. Find the crowd: the base rate, how many could match?\n4. Count the matches: crowd × false-match rate, + the real ones\n"
            "5. Divide: real matches ÷ all matches, then combine any other evidence honestly"),
    next="The confusion matrix: 'catches 90% of fraud' and '90% of alarms are real' are two different claims. One simple table makes the swap impossible to miss.",
    pinned_extra=("• {t_case} The real case is Sally Clark (England, convicted 1999, conviction overturned 2003). The Royal Statistical Society "
                  "publicly criticised the 1 in 73 million figure in 2001.\n"
                  "• The names 'prosecutor's fallacy' and 'defense attorney's fallacy' come from Thompson & Schumann (1987), "
                  "'Interpretation of statistical evidence in criminal trials', Law and Human Behavior.\n"
                  "• {t_crowd} The city example assumes the culprit is one of the 8 million, everyone was equally likely before any "
                  "evidence, and nothing else is known. Real cases always have more evidence, which shrinks the crowd ({t_ev}).\n"
                  "• 1 in a million is a typical figure for a partial DNA profile; full profiles are usually far rarer, and close "
                  "relatives match much more often than strangers.\n"
                  "• The grids, stadium, fraud and database numbers are illustrations of the counting idea, not real data."),
)
TAGS = ["prosecutor's fallacy", "prosecutors fallacy", "conditional probability", "base rate fallacy", "base rate",
        "Bayes theorem", "statistics in court", "DNA evidence statistics", "false positives", "machine learning",
        "statistics for machine learning", "data science", "statistics for data science", "finance", "statistics for finance",
        "computer science", "ML", "DS", "CS", "statistics explained", "probability explained", "Math Lab TV"]

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
    extra = LINES["pinned_extra"].format(t_case=at("s074"), t_crowd=at("s035"), t_ev=at("s069"))
    pinned = ("📌 Quick summary: 'a 1 in a million chance an innocent person would match' is P(match | innocent). "
              "The jury needs P(innocent | match), and to get it you must count the crowd: in a city of 8 million, "
              "about 8 innocent people match too, so a match alone means guilty only about 1 time in 9.\n\n"
              f"Worth adding:\n{extra}\n\nWhere have you seen a '1 in a million' that hid a swap? 👇")
    cards = "\n".join(f"{at(sid)}  card → {title}" for sid, title in CARD_SEGS)
    settings = f"""Category: Education
Language: English · Captions: upload out/captions.srt (English)
Audience: Not made for kids
License: Standard YouTube License · Allow embedding: on
Chapters: automatic from the description timestamps (first at 0:00, all ≥ 10 s)
Thumbnails: upload thumbnail_A.png and thumbnail_B.png to "Test & compare"
End screen: link the next video in the last 20 s · Comments: on · pin pinned_comment.txt
YouTube cards (callbacks in the narration):
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
