#!/usr/bin/env python3
"""YouTube package: title options, description (chapters from timings.json + related videos from the
channel tracker), tags, pinned comment, settings."""
import math, pathlib, sys
from common import CHAPTERS, TIM, SEGS

HERE = pathlib.Path(__file__).resolve().parent
SLUG = "confusion-matrix"   # id in channel/catalog.json
OUT = HERE / "out" / "youtube"; OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(HERE.parent / "channel"))
import channel as ch  # noqa: E402

TITLES = ["Confusion Matrix Explained: Accuracy, Precision, Recall, F1 | ML, Data Science, Finance, CS",
          "Precision vs Recall Explained Visually: The Confusion Matrix | Machine Learning & Data Science",
          "Why 99% Accuracy Can Be Useless: The Confusion Matrix Explained | ML, DS, Finance, CS"]
TITLE = TITLES[0]
CH_TITLES = {
    "Two Fraud Detectors": "Two fraud detectors, both 99% accurate",
    "Welcome": "Welcome",
    "Why Accuracy Isn't Enough": "Why accuracy isn't enough (the lazy detector)",
    "The Four Outcomes": "The four outcomes: TP, TN, FP, FN",
    "Filling the Grid": "Filling the confusion matrix with real counts",
    "Accuracy": "Accuracy, and why it lies about rare things",
    "Precision": "Precision: a question about your alarms",
    "Recall": "Recall (sensitivity) and specificity",
    "The Trade-off": "The precision–recall trade-off and the cut-off dial",
    "The F1 Score": "The F1 score (harmonic mean)",
    "Which Error Is Worse?": "Which error is worse? Pricing the mistakes",
    "Example: A Medical Test": "Example: a medical screening test (Bayes link)",
    "Example: A Spam Filter": "Example: a spam filter",
    "Your Turn: Loan Defaults": "Your turn: loan defaults",
    "Where You'll Use It": "Where you'll use it: ML, DS, Finance, CS",
    "Common Mistakes": "Common mistakes",
    "Recipe": "The recipe",
    "Subscribe": "Subscribe",
    "Next Time": "Next time",
}
DOMAIN_SEGS = dict(ml="s188", ds="s190", fin="s191", cs="s192")
LINES = dict(
    first2="The confusion matrix explained visually: accuracy, precision, recall and the F1 score, for Machine Learning (ML), "
           "Data Science (DS), Finance and Computer Science (CS).\n"
           "Learn to read any classifier's confusion matrix, why 99% accuracy can be useless, and how to choose between "
           "precision and recall.",
    hook="Two fraud detectors check 10,000 card payments, 100 of them fraud. One says \"we catch 90% of fraud\", the other "
         "says \"90% of our alarms are real\", and both are over 99% accurate. Yet one lets 55 of the 100 frauds through, "
         "and a detector that never raises an alarm is 99% accurate too.",
    domains=dict(ml="the first thing printed after training any classifier; for rare classes report precision and recall, not accuracy alone",
                 ds="explain a model in plain words: of every 100 alarms this many are real, of every 100 cases we catch this many",
                 fin="fraud detection and credit risk; the cut-off is set by the cost of each kind of mistake",
                 cs="spam filters, malware scanners and intrusion detection, where too many false alarms get ignored"),
    formulas="• accuracy = (TP + TN) / total: how often the detector is right overall\n"
             "• precision = TP / (TP + FP): of everything it flagged, how much was real\n"
             "• recall (sensitivity) = TP / (TP + FN): of everything real, how much it caught\n"
             "• specificity = TN / (TN + FP): of everything normal, how much it left alone\n"
             "• F1 = 2TP / (2TP + FP + FN): the harmonic mean of precision and recall\n"
             "  TP = true positives (caught), TN = true negatives (correctly left alone),\n"
             "  FP = false positives (false alarms), FN = false negatives (misses)",
    worked="• Detector A (TP 90, FN 10, FP 30, TN 9,870): accuracy 99.6%, precision 75%, recall 90%, F1 = 9/11 ≈ 82%\n"
           "• Detector B (TP 45, FN 55, FP 5, TN 9,895): accuracy 99.4%, precision 90%, recall 45%, F1 60%\n"
           "• Detector C (TP 99, FN 1, FP 301, TN 9,599): recall 99%, precision ≈ 25%, accuracy 96.98%\n"
           "• Lazy detector (never alarms): accuracy 99%, recall 0\n"
           "• Medical test (9, 1, 99, 891): recall 90%, accuracy 90%, precision 9/108 = 1 in 12; in a clinic where half are sick: precision 90%\n"
           "• Spam filter (270, 30, 10, 690): precision ≈ 96%, recall 90%, accuracy 96%\n"
           "• Loans (150, 50, 100, 1,700): precision 60%, recall 75%, accuracy 92.5%, F1 = 2/3\n"
           "• Costs (illustration, a miss = $500, a false alarm = $5): A $5,150, B $27,525, C $2,005, lazy $50,000",
    recipe="1. Draw the grid: truth in the rows, the detector's answer in the columns.\n"
           "2. Fill the four counts and check the rows add up to the real totals.\n"
           "3. Precision: read down the alarm column.\n"
           "4. Recall: read across the real row.\n"
           "5. Price the mistakes, then set the cut-off. Use accuracy only when the groups are roughly balanced.",
    next="How Spam Filters Work: Naive Bayes Explained (Bayes' theorem, one word at a time)",
    pinned_extra="• (rows vs columns) Some tools, like many Python libraries, put the truth in the rows but list the negative class first, "
                 "so true positives sit in the bottom-right corner. Always read the labels first.\n"
                 "• The costs in \"Which error is worse?\" are made-up numbers to show the idea; real costs depend on the business.\n"
                 "• Precision depends on how common the thing is (see the clinic example), recall doesn't.",
)
TAGS = ["confusion matrix", "precision and recall", "precision vs recall", "accuracy precision recall", "f1 score",
        "true positive false positive", "sensitivity and specificity", "classification metrics", "imbalanced data",
        "machine learning", "statistics for machine learning", "data science", "statistics for data science", "finance",
        "statistics for finance", "computer science", "ML", "DS", "CS", "fraud detection", "statistics explained", "Math Lab TV"]


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
    pinned = f"📌 Quick summary: accuracy counts every right answer, precision asks how many alarms are real, recall asks how much of the real thing was caught. For rare things, look at the whole grid, not one number.\n\nWorth adding:\n{LINES['pinned_extra']}\n\nWhich mistake is worse in YOUR work: a false alarm or a miss? 👇"
    settings = f"""Category: Education
Language: English · Captions: upload out/captions.srt (English)
Audience: Not made for kids
License: Standard YouTube License · Allow embedding: on
Chapters: automatic from the description timestamps (first at 0:00, all ≥ 10 s)
Thumbnails: thumbnail_C.png (simple keyword + formula) as the main one; thumbnail_A.png and thumbnail_B.png for "Test & compare"
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
