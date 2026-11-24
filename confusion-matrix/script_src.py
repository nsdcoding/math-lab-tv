#!/usr/bin/env python3
"""Source of truth for the narration. Run to emit script.json + script.md.

Running example (used everywhere; every number checked in verify_numbers.py):
  Detector A on 10,000 card payments, 100 fraud: TP 90 · FN 10 · FP 30 · TN 9,870.
  accuracy 99.6% · precision 90/120 = 75% · recall 90/100 = 90% · F1 = 180/220 = 9/11 ≈ 82%.
  Detector B (same model, higher cut-off): TP 45 · FN 55 · FP 5 · TN 9,895 → precision 90%, recall 45%, acc 99.4%, F1 60%.
  Detector C (low cut-off): TP 99 · FN 1 · FP 301 · TN 9,599 → recall 99%, precision ≈ 25%, acc 96.98%.
  Lazy detector (never alarms): accuracy 99%, recall 0.
  Worked practice grids (the owner asked for many examples), each labelled as its own example:
  medical test from the Bayes video (9 · 1 · 99 · 891), spam filter (270 · 30 · 10 · 690), loans (150 · 50 · 100 · 1,700).
Colour roles (one per concept, kept for the whole video):
  precision / the alarm column = violet · recall / the real-fraud row = orange · correct diagonal (TP, TN) = aqua ·
  false positive = orange tint box, false negative = blue tint box · accuracy = warn (gold) · traps = red.
Connections (from `python3 channel/channel.py refs <slug>`):
  pays off the prosecutors-fallacy teaser ("catches 90% of fraud" vs "90% of alarms are real");
  callback bayes-examples (the 1-in-12 screening test, recast as a precision calculation);
  seeds roc-curve (the cut-off dial); teaser → naive-bayes (spam filters).
"""
import json, pathlib, sys

SLUG = "confusion-matrix"            # id in channel/catalog.json
TARGET_MIN = (25, 30)         # from the skill arguments; words ≈ minutes × 150 (voice ~165 wpm + pauses)
D = 0.35                      # default pause between segments
S = []
N = [0]   # auto-id counter; once voiced, insert new lines with explicit ids (e.g. s017a) so old clips stay cached


def seg(chapter, text, visual, pause=D, sid=None):
    if sid is None:
        N[0] += 1; sid = f"s{N[0]:03d}"
    S.append(dict(id=sid, chapter=chapter, text=text, visual=visual, pause_after=pause))


# ───────────── 1. HOOK ─────────────
c = "Two Fraud Detectors"
seg(c, "Imagine you run the card team at a small bank.",
    "Illustration sticker: a person at a desk with a bank-card terminal; chip 'illustration'.")
seg(c, "Every day, ten thousand card payments go through. And about one in every hundred of them is fraud.",
    "A 100×100 dot field fills (10,000 dots); 100 of them turn red. Counter: '10,000 payments · 100 fraud'.")
seg(c, "Two companies want to sell you a fraud detector.",
    "Two sealed boxes labelled 'Detector A' and 'Detector B' slide in.")
seg(c, "The first one says: our model catches ninety percent of fraud.",
    "Detector A speech chip: 'catches 90% of fraud'.")
seg(c, "The second one says: ninety percent of our alarms are real fraud.",
    "Detector B speech chip: '90% of our alarms are real'.")
seg(c, "And both of them add: by the way, we are more than ninety-nine percent accurate.",
    "Both chips gain a gold '99%+ accurate' badge.", 0.8)
seg(c, "They sound like the same promise. Ninety, ninety, ninety-nine.",
    "The three numbers pulse in a row: 90 · 90 · 99.")
seg(c, "But they are completely different promises. One of these detectors would let more than half of the fraud walk straight past you.",
    "Detector B's box opens: 55 red dots slip past a gate. Label 'misses 55 of 100'.", 1.0)
seg(c, "And here's the strangest part. A detector that does nothing at all, that never raises a single alarm, is ninety-nine percent accurate too.",
    "A third empty box 'Detector Zero' with a gold '99% accurate' badge; inside, nothing.", 1.2)
seg(c, "At the end of our prosecutor's fallacy video, I left you with this exact puzzle. Today, we solve it.",
    "Chip 'from: The Prosecutor's Fallacy' slides in under the boxes.")
seg(c, "With one small table, two by two, that tells you the whole truth about any yes or no prediction.",
    "The dot field collapses into an empty 2×2 grid.")
seg(c, "It's called the confusion matrix.",
    "Title card: 'THE CONFUSION MATRIX' / 'accuracy · precision · recall'.", 1.0)

# ───────────── 2. WELCOME ─────────────
c = "Welcome"
seg(c, "Welcome to Math Lab TV. Where math is something you can see.",
    "Logo (violet rounded square with a green bell curve) + MATH LAB TV + tagline 'where math is something you can see'.", 0.7)
seg(c, "Today you will learn the four boxes of the confusion matrix, and how to fill them from real counts.",
    "Big ① + mini 2×2 grid filling with dots + caption 'the four outcomes'; small logo top-right.")
seg(c, "You will see why accuracy can lie, and what precision and recall tell you instead.",
    "Big ② + mini grid with one column and one row lighting up + caption 'accuracy · precision · recall'.")
seg(c, "And you will practise on four real examples, until you can read any of these tables on your own.",
    "Big ③ + four tiny grids (fraud, medical test, spam, loans) + caption 'four worked examples'.", 0.6)

# ───────────── 3. WHY IT MATTERS ─────────────
c = "Why Accuracy Isn't Enough"
seg(c, "Let's start with that lazy detector, because it shows the whole problem.",
    "Detector Zero returns, centre stage.")
seg(c, "Its rule is simple. Whatever the payment is, say: not fraud.",
    "A rubber stamp 'NOT FRAUD' slams on payment after payment.")
seg(c, "Out of ten thousand payments, nine thousand nine hundred really are fine. So it gets all of those right.",
    "Bar on a 0–10,000 axis: 9,900 grey dots get green ticks.")
seg(c, "The one hundred frauds, it gets wrong. Every single one.",
    "The 100 red dots get red crosses.")
seg(c, "Nine thousand nine hundred right, out of ten thousand. That's ninety-nine percent accuracy.",
    "Fraction 9,900 / 10,000 = 99% builds on screen, gold.", 0.8)
seg(c, "And it caught zero fraud. Not one.",
    "Big '0 fraud caught' in red next to the 99%.", 1.2)
seg(c, "So accuracy, on its own, can't tell a useless detector from a good one.",
    "Two gauges side by side, both reading 99%; one labelled 'useless', one '?'.")
seg(c, "This happens whenever the thing you are looking for is rare.",
    "Axis 'how rare is the thing you look for' from common → rare; a 'danger zone' at the rare end.")
seg(c, "Fraud is rare. Serious diseases are rare. Faulty parts on a factory line are rare. Hackers in your network logs are rare.",
    "Four icon cards: card, heart, gear, laptop, each with 'rare' tag.")
seg(c, "And those are exactly the cases where getting it wrong costs the most.",
    "The four cards tint red.")
seg(c, "In our Bayes video, we saw a test that was ninety percent accurate, where a positive result meant only about a one in twelve chance of being sick.",
    "Chip 'from: Bayes' Theorem' + mini 1,000-dot grid with 9 vs 99 highlighted.")
seg(c, "The confusion matrix is the tool that keeps all of those numbers in one place, so nothing gets hidden.",
    "Mini Bayes grid morphs into an empty 2×2 grid.", 0.6)

# ───────────── 4. THE FOUR OUTCOMES ─────────────
c = "The Four Outcomes"
seg(c, "Every time a detector looks at a payment, two things are true.",
    "One payment card in the centre, two question tags.")
seg(c, "First, what actually happened. Was it really fraud, or not?",
    "Tag 1: 'the truth: fraud or not?'")
seg(c, "Second, what the detector said. Did it raise an alarm, or stay quiet?",
    "Tag 2: 'the guess: alarm or quiet?'")
seg(c, "Two questions, two answers each. That gives four possible outcomes. No more, no less.",
    "2 × 2 = 4 appears; tree with two branches splitting into four leaves.", 0.6)
seg(c, "Let's lay them out in a grid. The rows are the truth. The top row is real fraud. The bottom row is not fraud.",
    "2×2 grid on real axes. Row labels: 'really fraud' (top), 'really fine' (bottom). Axis title 'the truth'.")
seg(c, "The columns are what the detector said. The left column is: alarm. The right column is: quiet.",
    "Column labels: 'alarm' (left), 'quiet' (right). Axis title 'the guess'.")
seg(c, "Now let's name each box carefully, because the names trip everyone up.",
    "The four boxes pulse one by one, empty.")
seg(c, "Top left. It really was fraud, and the detector raised an alarm. A correct catch. We call it a true positive.",
    "Top-left fills aqua: 'TRUE POSITIVE (TP)' + tiny icon 'fraud → alarm ✓'.", 0.6)
seg(c, "Positive means the detector said yes, this is the thing. True means it was right.",
    "Word 'POSITIVE' glows → arrow to 'detector said yes'; 'TRUE' → 'it was right'.")
seg(c, "Bottom right. It was a normal payment, and the detector stayed quiet. Also correct. That's a true negative.",
    "Bottom-right fills aqua: 'TRUE NEGATIVE (TN)'.", 0.6)
seg(c, "Now the mistakes. Bottom left. A perfectly normal payment, but the detector raised an alarm anyway.",
    "Bottom-left box outlines in orange.")
seg(c, "A false alarm. We call it a false positive. The detector said yes, and it was wrong.",
    "Bottom-left fills orange: 'FALSE POSITIVE (FP)' + 'false alarm'.", 0.6)
seg(c, "And top right. Real fraud, and the detector said nothing. The fraud slipped through.",
    "Top-right box outlines in blue; a red dot slips through a gate.")
seg(c, "A miss. We call it a false negative. The detector said no, and it was wrong.",
    "Top-right fills blue: 'FALSE NEGATIVE (FN)' + 'a miss'.", 0.6)
seg(c, "Here's a trick to remember them. The second word is what the detector said. The first word is whether that was right.",
    "Two-part decoder card: 'FALSE | POSITIVE' → 'was it right? | what it said'.", 1.0)
seg(c, "So a false negative is: it said negative, and that was false. It said no, but the answer was yes.",
    "Decoder applied to 'FALSE NEGATIVE' step by step.")
seg(c, "Let's try it slowly with just ten payments, before we use the big numbers. Three of them are fraud.",
    "Warm-up chip; ten numbered payment cards in a row, three with a red corner (fraud).")
seg(c, "Payment one is fraud, and the detector raises an alarm. Fraud row, alarm column. A true positive.",
    "Card 1 flies into the top-left box.")
seg(c, "Payment two is a normal coffee, and the detector stays quiet. Fine row, quiet column. A true negative.",
    "Card 2 flies into the bottom-right box.")
seg(c, "Payment three is a normal payment, but it's a big one in another country, so the detector panics. A false positive.",
    "Card 3 flies into the bottom-left box.")
seg(c, "Payment four is fraud, but a small one, and it slips through. A false negative.",
    "Card 4 flies into the top-right box.")
seg(c, "We keep going, one payment at a time, until all ten are sorted.",
    "Cards 5–10 fly into their boxes quickly.")
seg(c, "Two true positives, one false negative, two false positives, and five true negatives. Two plus one plus two plus five is ten. Every payment has exactly one home.",
    "Counts appear: TP 2 · FN 1 · FP 2 · TN 5; total 10 ✓.", 1.0)
seg(c, "The two correct boxes sit on one diagonal. The two kinds of mistake sit on the other.",
    "Diagonal line through TP and TN glows aqua; the anti-diagonal through FP and FN glows red.", 1.0)

# ───────────── 5. FILLING THE GRID ─────────────
c = "Filling the Grid"
seg(c, "Now let's fill this grid with Detector A, the one that catches ninety percent of fraud.",
    "Grid stays; chip 'Detector A' at the top.")
seg(c, "We run it on our ten thousand payments, and sort every payment into one of the four boxes.",
    "Dots stream out of the 10,000-dot field into the four boxes.")
seg(c, "Start with the one hundred real frauds. They all belong in the top row.",
    "100 red dots move to the top row; row total '100'.")
seg(c, "Detector A raises an alarm on ninety of them. Ninety true positives.",
    "90 red dots stack in the top-left box; counter '90'.")
seg(c, "The other ten get through. Ten false negatives.",
    "10 red dots stack in the top-right box; counter '10'.", 0.6)
seg(c, "Now the nine thousand nine hundred normal payments. They belong in the bottom row.",
    "Grey dots pour into the bottom row; row total '9,900'.")
seg(c, "Detector A wrongly flags thirty of them. Thirty false positives. Thirty customers who get a worried phone call for nothing.",
    "30 grey dots stack in the bottom-left; counter '30'; tiny phone icon.")
seg(c, "And the remaining nine thousand eight hundred and seventy are correctly left alone. True negatives.",
    "Bottom-right counter rolls to '9,870'.", 0.8)
seg(c, "Let's check our work. Ninety plus ten is one hundred. That's every fraud.",
    "Top row: 90 + 10 = 100 ✓.")
seg(c, "Thirty plus nine thousand eight hundred and seventy is nine thousand nine hundred. That's every normal payment.",
    "Bottom row: 30 + 9,870 = 9,900 ✓.")
seg(c, "And all four boxes together make ten thousand. Every payment lands in exactly one box.",
    "Grand total 10,000 ✓ in the corner.", 0.6)
seg(c, "Now add up the left column. Ninety plus thirty is one hundred and twenty. That's every alarm Detector A raised.",
    "Left column total: 90 + 30 = 120, label 'all alarms'.")
seg(c, "So the rows tell you the truth. The columns tell you what the detector did. Hold on to that, because every number in this video comes from reading this grid by row, or by column.",
    "Row arrows labelled 'truth', column arrows labelled 'what it did'.", 1.0)

# ───────────── 6. ACCURACY ─────────────
c = "Accuracy"
seg(c, "Let's start with the number the salespeople love. Accuracy.",
    "Formula card title 'ACCURACY'.")
seg(c, "Accuracy asks one question: out of everything, how often was the detector right?",
    "Plain question under the title.")
seg(c, "Right means the diagonal. True positives plus true negatives.",
    "TP and TN boxes glow aqua.")
seg(c, "Then divide by everything. All four boxes.",
    "Whole grid outlined.")
seg(c, "In symbols, accuracy equals T P plus T N, over the total. T P is short for true positives. T N is short for true negatives.",
    "LaTeX: accuracy = (TP + TN) / total, with plain-word labels under TP and TN.")
seg(c, "For Detector A, that's ninety plus nine thousand eight hundred and seventy. Nine thousand nine hundred and sixty right answers.",
    "90 + 9,870 = 9,960 builds in Inter.")
seg(c, "Out of ten thousand. That's ninety-nine point six percent.",
    "9,960 / 10,000 = 99.6% in gold.", 0.8)
seg(c, "Sounds amazing. But remember the lazy detector scored ninety-nine percent by doing nothing.",
    "Gauge: lazy 99% next to Detector A 99.6%.")
seg(c, "So all of Detector A's real work, catching ninety frauds, only moves accuracy from ninety-nine to ninety-nine point six. Less than one point.",
    "Zoom on the gap between 99 and 99.6 on a 98–100 axis; label 'all the real work'.", 1.0)
seg(c, "Why? Because the bottom right box is huge. Nine thousand eight hundred and seventy easy, boring, correct answers drown out everything else.",
    "Bottom-right box swells until it squashes the other three; label 'the easy majority'.")
seg(c, "That's the rule of thumb. When one class is rare, accuracy is mostly a measure of how rare it is.",
    "Rule-of-thumb card (warn border): 'rare class → accuracy mostly measures rarity'.", 1.2)
seg(c, "Accuracy is not useless. When the two groups are roughly the same size, it's a fine first look. We'll see that in the spam example later.",
    "Small balanced grid preview (300 vs 700) with an 'OK here' tag.")
seg(c, "But for rare things, we need questions that zoom in on the fraud itself. And there are exactly two of them.",
    "Two spotlights appear over the grid: one vertical, one horizontal.", 0.6)

# ───────────── 7. PRECISION ─────────────
c = "Precision"
seg(c, "The first question is about your alarms.",
    "Bell icon over the left column.")
seg(c, "Picture the analyst who has to phone every flagged customer. They only ever see the alarms. They never see the quiet payments.",
    "Everything except the left column dims.")
seg(c, "So their question is: when the detector raises an alarm, how often is it real?",
    "Question card: 'When it says FRAUD, how often is it right?'")
seg(c, "That's precision. And it lives entirely in the left column.",
    "Left column lights up violet; title 'PRECISION'.", 0.6)
seg(c, "Precision equals true positives, over all the alarms. T P, over T P plus F P. F P is short for false positives, the false alarms.",
    "LaTeX: precision = TP / (TP + FP), labels 'real catches' over 'all alarms'.")
seg(c, "For Detector A, the left column holds ninety real frauds and thirty false alarms.",
    "Left column: 90 red dots over 30 grey dots.")
seg(c, "Ninety, out of one hundred and twenty. That's three out of every four. Seventy-five percent precision.",
    "90 / 120 = 3/4 = 75%; the 120 alarm dots rearrange into 30 rows of 4, three red one grey.", 1.0)
seg(c, "In plain words: every time Detector A rings the bell, there's a three in four chance it's real fraud, and a one in four chance it's a false alarm.",
    "Bell rings; 3 of 4 cards say 'real', 1 says 'false alarm'.")
seg(c, "Notice what precision ignores. It doesn't care about the right column at all. It doesn't know how much fraud got away.",
    "Right column greys out with a 'not counted' tag.")
seg(c, "A detector that raised one single alarm, and happened to be right, would have perfect precision. One out of one.",
    "Tiny grid: a single dot in TP, 1/1 = 100% precision, with a '?' over the 99 missed frauds.", 1.0)
seg(c, "So precision alone can be gamed by being very, very cautious.",
    "Label 'cautious = high precision' in warn.", 0.6)

# ───────────── 8. RECALL ─────────────
c = "Recall"
seg(c, "That's why we need the second question. It's about what you missed.",
    "Back to the full grid; magnifying glass on the top row.")
seg(c, "Picture the bank's fraud manager. They care about every fraud that happened, whether the detector noticed it or not.",
    "Everything except the top row dims.")
seg(c, "Their question is: out of all the real fraud, how much did we catch?",
    "Question card: 'Of all the real fraud, how much did we catch?'")
seg(c, "That's recall. And it lives entirely in the top row.",
    "Top row lights up orange; title 'RECALL'.", 0.6)
seg(c, "Recall equals true positives, over all the real positives. T P, over T P plus F N. F N is short for false negatives, the misses.",
    "LaTeX: recall = TP / (TP + FN), labels 'real catches' over 'all real fraud'.")
seg(c, "For Detector A, the top row holds ninety catches and ten misses.",
    "Top row: 90 caught | 10 missed.")
seg(c, "Ninety, out of one hundred. Ninety percent recall.",
    "90 / 100 = 90% in orange.", 1.0)
seg(c, "That's the first salesperson's claim. We catch ninety percent of fraud. That's a recall claim.",
    "Detector A's chip 'catches 90% of fraud' flies onto the top row and snaps into the word RECALL.", 1.0)
seg(c, "You'll also hear recall called sensitivity, or the true positive rate. Same number, different names.",
    "Synonym tags under RECALL: 'sensitivity', 'true positive rate'.")
seg(c, "There's also a matching number for the bottom row, called specificity. Of all the normal payments, how many did we leave alone? For Detector A, nine thousand eight hundred and seventy out of nine thousand nine hundred. Almost all of them. We'll need it when we meet the R O C curve.",
    "Bottom row lights aqua briefly: 'SPECIFICITY = TN / (TN + FP)' = 9,870/9,900 ≈ 99.7%.")
seg(c, "And recall has its own blind spot. It ignores the bottom row, so it never sees false alarms.",
    "Bottom row greys out, 'not counted'.")
seg(c, "A detector that flags every single payment as fraud catches all one hundred frauds. One hundred percent recall.",
    "Every dot jumps into the left column; recall 100/100 = 100%.")
seg(c, "And it phones all ten thousand customers. That's useless too.",
    "A wall of 10,000 phone icons; precision drops to 1%.", 1.0)
seg(c, "So here's the picture to keep. Precision reads down the alarm column. Recall reads across the fraud row. They share one box, the true positives, and look away from each other in every other direction.",
    "Same grid: left column violet, top row orange; the TP corner where they cross glows white.", 1.5)

# ───────────── 9. THE TRADE-OFF ─────────────
c = "The Trade-off"
seg(c, "Now we can finally answer the puzzle. Let's fill the grid for Detector B, the one whose alarms are ninety percent real.",
    "Second grid appears beside Detector A's; chip 'Detector B'.")
seg(c, "Detector B is much more careful. It only raises fifty alarms.",
    "Left column of B: 50 dots.")
seg(c, "Forty-five of them are real fraud. Five are false alarms. So its precision is forty-five out of fifty. Ninety percent. Its claim was true.",
    "45 red + 5 grey; 45/50 = 90% precision in violet.", 0.8)
seg(c, "But look at the top row. Forty-five caught. And fifty-five frauds missed.",
    "Top row of B: 45 | 55, the 55 in blue.")
seg(c, "Its recall is forty-five out of one hundred. Forty-five percent. It lets more than half the fraud walk straight past.",
    "45/100 = 45% recall; 55 red dots walk out through a gate.", 1.2)
seg(c, "And its accuracy? Forty-five plus nine thousand eight hundred and ninety-five, out of ten thousand. Ninety-nine point four percent. Still sounds amazing.",
    "Accuracy 9,940 / 10,000 = 99.4% gold badge.", 0.8)
seg(c, "So side by side. Detector A: precision seventy-five, recall ninety. Detector B: precision ninety, recall forty-five.",
    "Comparison table on axes: two bars each for precision (violet) and recall (orange).")
seg(c, "Each salesperson quoted the number that made them look good. Neither was lying. They just answered different questions.",
    "Each chip slides onto its own bar.", 1.0)
seg(c, "In fact, this is the same swap we saw in the prosecutor's fallacy. How often does an alarm mean fraud, versus how often does fraud cause an alarm.",
    "Chip 'from: The Prosecutor's Fallacy': two arrows 'alarm → fraud?' and 'fraud → alarm?'.")
seg(c, "Now here's the key idea. A and B are often the same model, with the dial set differently.",
    "Both detectors merge into one box with a dial.")
seg(c, "Most detectors give each payment a score, say from zero to one, for how suspicious it looks. Then you pick a cut-off. Above it, alarm. Below it, quiet.",
    "Number line 0–1 with payment dots placed by score; a vertical cut-off line.")
seg(c, "Set the cut-off high, and only the most suspicious payments get flagged. Fewer false alarms, more misses. High precision, low recall. That's Detector B.",
    "Cut-off slides right; precision bar rises, recall bar falls.")
seg(c, "Set it low, and you flag lots of payments. More catches, more false alarms. High recall, low precision. That's Detector A.",
    "Cut-off slides left; recall rises, precision falls.")
seg(c, "Push it even lower, and you get a nervous Detector C. It flags four hundred payments and catches ninety-nine of the hundred frauds.",
    "Third grid 'Detector C': 99 | 1 over 301 | 9,599.")
seg(c, "Ninety-nine percent recall. But only ninety-nine of its four hundred alarms are real. Precision is about one in four.",
    "Recall 99% orange; precision 99/400 ≈ 25% violet.")
seg(c, "And its accuracy drops to about ninety-seven percent, lower than the lazy detector that catches nothing. Accuracy is pointing the wrong way.",
    "Accuracy 96.98% badge below lazy 99%; red arrow 'wrong way'.", 1.2)
seg(c, "That's the trade-off. Move the dial one way, precision goes up and recall goes down. Move it back, and they swap. You almost never get both for free.",
    "Seesaw (beam_scale) with precision on one end, recall on the other, tipping as the dial moves.", 1.0)
seg(c, "In a future video, we'll trace this whole dial on one curve, called the R O C curve. For now, just remember: the dial exists.",
    "Small teaser chip 'later: the ROC curve'.", 0.6)

# ───────────── 10. F1 SCORE ─────────────
c = "The F1 Score"
seg(c, "But sometimes you need one number. To rank ten models, or to put on a report.",
    "Ten model cards in a row, each with two bars, and a '?' for a single score.")
seg(c, "The usual compromise is called the F one score. It blends precision and recall into a single number.",
    "Title 'F1 SCORE: one number, two questions'.")
seg(c, "You might think: just average them. For Detector A, seventy-five and ninety average to eighty-two and a half.",
    "(75 + 90) / 2 = 82.5 crossed out lightly as 'plain average'.")
seg(c, "But a plain average has a problem. Remember the detector that flags everything? Recall one hundred, precision one. The average is fifty point five, which sounds half decent for a useless detector.",
    "Example: (100 + 1)/2 = 50.5 with red 'too kind'.", 0.8)
seg(c, "The F one score uses a stricter average, called the harmonic mean, that gets dragged down hard by whichever number is worse.",
    "Two bars; a weight hangs from the shorter one, pulling the F1 marker toward it.")
seg(c, "Here's the friendliest way to compute it. F one equals two T P, over two T P plus F P plus F N.",
    "LaTeX: F1 = 2TP / (2TP + FP + FN), each part labelled in plain words.")
seg(c, "In words: count the true positives twice, then compare them with all the mistakes. Both kinds of mistake count against you.",
    "TP box doubles; FP and FN boxes slide next to it on a single bar.")
seg(c, "For Detector A: two times ninety is one hundred and eighty. Plus thirty false alarms, plus ten misses, is two hundred and twenty.",
    "180 / (180 + 30 + 10) = 180 / 220.")
seg(c, "One hundred and eighty over two hundred and twenty. Nine elevenths. About eighty-two percent.",
    "180/220 = 9/11 ≈ 82% in violet.", 0.8)
seg(c, "For Detector B: two times forty-five is ninety. Plus five plus fifty-five. Ninety over one hundred and fifty. Sixty percent.",
    "90 / 150 = 60%.")
seg(c, "And the flag everything detector? Its F one is about two percent. The harmonic mean is not fooled.",
    "F1 = 200 / (200 + 9,900) ≈ 2% in red.", 1.0)
seg(c, "So by F one, Detector A wins. But be careful. F one assumes a miss and a false alarm are equally bad. And in the real world, they almost never are.",
    "F1 ranking A > B; caution card 'assumes both mistakes cost the same'.", 1.0)

# ───────────── 11. WHICH ERROR IS WORSE? ─────────────
c = "Which Error Is Worse?"
seg(c, "So the real question is not which number is highest. It's which mistake would you rather make.",
    "Two boxes, FP (orange) and FN (blue), on a balance beam.")
seg(c, "Let's put a price on each one. These are made up numbers, just to show the idea.",
    "Chip 'illustration: made-up costs'.")
seg(c, "Say a missed fraud costs the bank five hundred dollars. And a false alarm costs about five dollars, a few minutes of an analyst's time on the phone.",
    "Price tags: FN = $500, FP = $5.")
seg(c, "Detector A: ten misses times five hundred, plus thirty false alarms times five. Five thousand one hundred and fifty dollars.",
    "10 × 500 + 30 × 5 = 5,150 bar.")
seg(c, "Detector B: fifty-five misses times five hundred, plus five times five. Twenty-seven thousand five hundred and twenty-five dollars.",
    "55 × 500 + 5 × 5 = 27,525 bar, much taller.")
seg(c, "Nervous Detector C: one miss, plus three hundred and one false alarms. Only two thousand and five dollars. The cheapest of all.",
    "1 × 500 + 301 × 5 = 2,005 bar, shortest.")
seg(c, "And the lazy detector? A hundred misses. Fifty thousand dollars.",
    "100 × 500 = 50,000 bar off the top; axis rescales.", 1.0)
seg(c, "With these prices, the detector with the worst accuracy, C, is the best choice. Because misses are so expensive, you want high recall.",
    "C bar crowned; label 'high recall wins when misses are expensive'.", 1.0)
seg(c, "But change the prices. Suppose every false alarm freezes a customer's card at the checkout, and they get so annoyed that it costs two hundred dollars in lost business.",
    "FP price tag flips from $5 to $200.")
seg(c, "Now Detector C costs over sixty thousand dollars, and Detector A wins easily, at eleven thousand.",
    "Bars redraw: C = 60,700 (worst), A = 11,000 (best), B = 28,500.", 1.2)
seg(c, "Same grids. Same counts. Different answer. The confusion matrix gives you the counts. Only you can decide what each mistake costs.",
    "The four grids stay, a big hand turns the dial; caption 'the counts are math, the costs are your call'.", 1.5)

# ───────────── 12. EXAMPLE: A MEDICAL TEST ─────────────
c = "Example: A Medical Test"
seg(c, "Let's practise reading these grids on a few more examples, each with real counts.",
    "Four small grids appear: 'medical test', 'spam filter', 'loans', ticks over the first.")
seg(c, "First, an old friend. The screening test from our Bayes video.",
    "Chip 'from: Bayes' Theorem'.")
seg(c, "One thousand people. One in a hundred has the condition, so ten are sick and nine hundred and ninety are healthy.",
    "Row totals fill: sick 10, healthy 990.")
seg(c, "The test catches nine of the ten sick people. So nine true positives and one false negative.",
    "Top row: 9 | 1.")
seg(c, "And it gives a false alarm to one in ten healthy people. That's ninety-nine false positives, and eight hundred and ninety-one true negatives.",
    "Bottom row: 99 | 891.", 0.8)
seg(c, "Recall: nine out of ten. Ninety percent. The test is good at finding sick people.",
    "Top row lights orange: 9/10 = 90%.")
seg(c, "Accuracy: nine plus eight hundred and ninety-one, out of a thousand. Ninety percent again.",
    "Diagonal lights aqua: 900/1,000 = 90%.")
seg(c, "But precision. Look down the alarm column. Nine real cases, and ninety-nine false alarms. Nine out of one hundred and eight.",
    "Left column lights violet: 9 red dots, 99 grey.")
seg(c, "That's one in twelve. The exact same answer we found with Bayes' theorem.",
    "9/108 = 1/12 with chip 'same as Bayes'.", 1.2)
seg(c, "So here's the connection. Bayes' theorem was secretly a precision calculation. It asked: given an alarm, how likely is it real?",
    "Label 'P(sick | positive) = precision'; Bayes formula fades in beside the grid column.", 1.0)
seg(c, "Now watch what happens if we use the exact same test in a different crowd.",
    "The grid slides left; a second empty grid appears, chip 'same test, different crowd'.")
seg(c, "Say a specialist clinic, where people already have symptoms, and half of the thousand are sick. Five hundred sick, five hundred healthy.",
    "Row totals: 500 | 500.")
seg(c, "The test still catches nine in ten sick people. Four hundred and fifty caught, fifty missed.",
    "Top row: 450 | 50.")
seg(c, "And it still gives false alarms to one in ten healthy people. Fifty false positives, four hundred and fifty true negatives.",
    "Bottom row: 50 | 450.")
seg(c, "Recall is still ninety percent. But precision jumps from one in twelve, to four hundred and fifty out of five hundred. Ninety percent.",
    "Precision 450/500 = 90% violet vs 1/12 on the first grid.", 1.0)
seg(c, "Same test. Recall didn't move. Precision changed completely, just because the crowd changed. So precision always depends on how common the thing is. Remember that whenever someone quotes you a precision from a different setting.",
    "Two grids side by side; recall bars equal, precision bars wildly different; caption 'precision depends on how common it is'.", 1.2)
seg(c, "In medicine, recall is usually the priority for a first screening. Missing a sick person is the costly mistake.",
    "FN box glows blue 'costly'.")
seg(c, "Low precision is acceptable here, because every positive gets a second, more careful test. That's the honest way to use it.",
    "Arrow from the alarm column to a second test box, 'confirm before worrying'.", 0.6)

# ───────────── 13. EXAMPLE: A SPAM FILTER ─────────────
c = "Example: A Spam Filter"
seg(c, "Second example. A spam filter, where the mistakes flip.",
    "Envelope icons; chip 'spam filter'.")
seg(c, "One thousand emails. Three hundred are spam, seven hundred are real.",
    "Row totals: spam 300, real 700.")
seg(c, "The filter sends two hundred and eighty emails to the spam folder. Two hundred and seventy really are spam. Ten are real emails.",
    "Left column: 270 | 10.")
seg(c, "So thirty spam emails reach your inbox, and six hundred and ninety real emails land safely.",
    "Right column: 30 | 690.", 0.8)
seg(c, "Precision: two hundred and seventy out of two hundred and eighty. About ninety-six percent.",
    "270/280 ≈ 96.4% violet.")
seg(c, "Recall: two hundred and seventy out of three hundred. Ninety percent.",
    "270/300 = 90% orange.")
seg(c, "Accuracy: nine hundred and sixty out of a thousand. Ninety-six percent.",
    "960/1,000 = 96% gold.")
seg(c, "And notice, here accuracy is more honest. Spam isn't rare. A lazy filter that never marks anything as spam would only score seventy percent, so it can't hide.",
    "Lazy filter badge: 700/1,000 = 70%.", 1.0)
seg(c, "Now, which mistake is worse? A spam email in your inbox is a small annoyance. You delete it.",
    "FN box: 'annoying, delete it'.")
seg(c, "But a real email in the spam folder, a job offer, a bill, a message from your doctor, might never be read.",
    "FP box glows orange: three envelopes falling into a bin.")
seg(c, "So for spam, the false alarm is the costly mistake. You want high precision, even if a few more spam emails get through.",
    "Seesaw tips toward precision.", 1.2)
seg(c, "Same table, same formulas. But the opposite priority from the medical test.",
    "Medical grid and spam grid side by side: recall starred on one, precision starred on the other.", 0.6)

# ───────────── 14. YOUR TURN: LOAN DEFAULTS ─────────────
c = "Your Turn: Loan Defaults"
seg(c, "Now it's your turn. Pause whenever you like.",
    "Pause icon; chip 'your turn'.")
seg(c, "A lender has two thousand loans. Two hundred of them will default, meaning the borrower stops paying.",
    "Row totals: default 200, repay 1,800.")
seg(c, "A model flags two hundred and fifty loans as risky. One hundred and fifty of them really do default. One hundred are fine.",
    "Left column: 150 | 100.")
seg(c, "Try to fill the rest of the grid, and find the precision and the recall.",
    "Right column shows '?' and '?'; timer ring.", 3.0)
seg(c, "Here's the grid. Two hundred defaults, minus one hundred and fifty caught, leaves fifty missed.",
    "Top-right fills: 200 − 150 = 50.")
seg(c, "One thousand eight hundred good loans, minus one hundred false alarms, leaves one thousand seven hundred true negatives.",
    "Bottom-right fills: 1,800 − 100 = 1,700.", 0.6)
seg(c, "Precision: one hundred and fifty out of two hundred and fifty flagged. Sixty percent.",
    "Left column violet: 150/250 = 60%.")
seg(c, "Recall: one hundred and fifty out of two hundred defaults. Seventy-five percent.",
    "Top row orange: 150/200 = 75%.")
seg(c, "Accuracy: one hundred and fifty plus one thousand seven hundred, out of two thousand. Ninety-two and a half percent.",
    "1,850/2,000 = 92.5% gold, next to the lazy model's 90%.")
seg(c, "And the F one score: three hundred, over three hundred plus one hundred plus fifty. Three hundred over four hundred and fifty. Two thirds.",
    "F1 = 300/450 = 2/3 ≈ 67% violet.", 1.0)
seg(c, "So, in plain words. When this model says risky, it's right six times out of ten. And it spots three out of every four loans that will go bad.",
    "Two plain-word sentence cards under the grid.", 1.0)
seg(c, "If you got those, you can now read any confusion matrix you'll ever see.",
    "Green check stamp on the grid.", 0.6)

# ───────────── 15. WHERE YOU'LL USE IT ─────────────
c = "Where You'll Use It"
seg(c, "So where will you actually meet this table?",
    "Four tiles: ML, DS, Finance, CS.")
seg(c, "In machine learning, it's the first thing printed after training any classifier. Any model that answers yes or no. Is this a cat? Will this customer cancel?",
    "ML tile: a model box outputs a 2×2 grid.")
seg(c, "And when the thing you're predicting is rare, people report precision and recall, never accuracy alone. Exactly because of the lazy detector.",
    "Mini lazy-detector badge '99%' crossed out.")
seg(c, "In data science, it's how you explain a model to people who don't build models. Of every hundred alarms, this many are real. Of every hundred cases, we catch this many.",
    "DS tile: a report card with two plain sentences.")
seg(c, "In finance, it's fraud detection and credit risk, exactly the two examples we worked through. And the cut-off is set by the cost of each mistake.",
    "Finance tile: card + loan icons with the cost bars from earlier.")
seg(c, "In computer science, it's spam filters, malware scanners, and systems that watch network traffic for intruders. Too many false alarms, and people learn to ignore them.",
    "CS tile: shield + inbox; a pile of ignored alarms.")
seg(c, "And beyond those four: medical tests, airport security, factory quality checks. Anywhere a yes or no decision can be wrong in two different ways.",
    "Three more small icons fade in around the tiles.", 0.6)

# ───────────── 16. COMMON MISTAKES ─────────────
c = "Common Mistakes"
seg(c, "Let's go through the mistakes beginners make most often.",
    "Red 'common mistakes' header.")
seg(c, "Mistake one: trusting accuracy when the class is rare. Always ask how rare it is, and compare with the lazy model that always says no.",
    "Card ①: lazy 99% vs model 99.6%; arrow 'compare with the baseline'.", 0.8)
seg(c, "Mistake two: mixing up precision and recall. Here's the fix. Precision starts from the alarms. Recall starts from the real cases.",
    "Card ②: grid with 'start from the alarms' on the column, 'start from the real cases' on the row.")
seg(c, "Ask yourself: am I dividing by everything the model flagged, or by everything that was really there?",
    "Two denominators: 'all flagged' (violet) vs 'all really there' (orange).", 0.8)
seg(c, "Mistake three: assuming every table is laid out the same way. Some tools put the truth in the rows, some in the columns. Some put the positive class first, some last.",
    "Card ③: our grid, then the same grid transposed and flipped; labels highlighted.")
seg(c, "So before you read any number, read the labels. Find the alarm column and the real fraud row first.",
    "Finger traces the axis labels.", 0.8)
seg(c, "And a bonus mistake: judging a model by one number. Any single score, even F one, hides which mistake the model makes. Look at the whole grid.",
    "Bonus card: F1 82% with a curtain pulled back to reveal the full grid.", 1.0)

# ───────────── 17. RECIPE ─────────────
c = "Recipe"
seg(c, "Here's the whole method as a recipe.",
    "Recipe card, numbered 1–5.")
seg(c, "Step one: draw the grid. Truth in the rows, the detector's answer in the columns. Label them.",
    "① Draw the grid · truth = rows, guess = columns.")
seg(c, "Step two: fill the four boxes with counts, and check that the rows add up to the real totals.",
    "② Fill the counts · rows add up to the truth.")
seg(c, "Step three: for precision, read down the alarm column. Of everything flagged, how much was real?",
    "③ Precision · down the alarm column.")
seg(c, "Step four: for recall, read across the real row. Of everything real, how much did we catch?",
    "④ Recall · across the real row.")
seg(c, "Step five: decide which mistake costs more, and choose your cut-off to match. Use accuracy only when the groups are roughly balanced.",
    "⑤ Price the mistakes · then set the dial.", 0.8)
seg(c, "Try it on Detector A. The grid: ninety, ten, thirty, nine thousand eight hundred and seventy. Precision: three in four. Recall: nine in ten. And if misses cost more, pick the detector with the higher recall.",
    "The recipe steps tick off one by one beside Detector A's grid.", 1.0)
seg(c, "Because a detector is not good or bad on its own. It's good or bad at the mistakes you can afford.",
    "Closing line in large Inter Display, violet.", 1.5)

# ───────────── 18. SUBSCRIBE ─────────────
c = "Subscribe"
seg(c, "Look around your world, and notice how many things quietly answer yes or no for you. Your inbox, your bank card, your phone's face unlock. Each one is making both kinds of mistake.",
    "Four everyday cards (inbox, bank card, phone unlock, airport gate), each stamped with a tiny 2×2 grid.", 0.6)
seg(c, "If this lesson made things clear for you, please subscribe to Math Lab TV, so we can keep building together.",
    "Logo + red SUBSCRIBE button; a cursor clicks it; it turns grey 'SUBSCRIBED ✓'; 'so we can keep building together' appears.", 0.8)

# ───────────── 19. NEXT TIME ─────────────
c = "Next Time"
seg(c, "But here's a puzzle for next time.", "Small logo top-centre; puzzle icon.")
seg(c, "Our spam filter was right ninety-six times out of a hundred. But how does it decide, in the first place, that an email full of words like free, winner, and urgent is probably spam?",
    "Email card with 'FREE', 'WINNER', 'URGENT' highlighted; a '?' over a dial reading 'spam score'.")
seg(c, "It turns out it's Bayes' theorem again, applied one word at a time. Next time, we'll build a spam filter from scratch, and see how it works.",
    "'next: How Spam Filters Work · Naive Bayes' chip under the logo.")
seg(c, "I will see you in the next video.", "Logo + next chip hold.", 2.0)

if __name__ == "__main__":
    import re
    out = pathlib.Path(__file__).parent
    bad = [s["id"] for s in S if re.search(r"[0-9%$]", s["text"])]
    if bad:
        print("WARNING digits/symbols in narration (write numbers as words):", bad)
    (out / "script.json").write_text(json.dumps(S, indent=2, ensure_ascii=False))
    words = sum(len(s["text"].split()) for s in S)
    pauses = sum(s["pause_after"] for s in S)
    est = words / 165 + pauses / 60
    md = [f"# The Confusion Matrix Explained: Accuracy, Precision and Recall\n",
          f"{len(S)} segments · {words} words · est. {est:.1f} min (voice ≈165 wpm + {pauses:.0f} s pauses) · target {TARGET_MIN[0]}–{TARGET_MIN[1]} min\n"]
    cur, cw = None, {}
    for s in S:
        cw[s["chapter"]] = cw.get(s["chapter"], 0) + len(s["text"].split())
    for s in S:
        if s["chapter"] != cur:
            cur = s["chapter"]; md.append(f"\n## {cur}  ·  {cw[cur]} words, ~{cw[cur] / 165 * 60:.0f} s\n")
        p = f" ⏸{s['pause_after']}s" if s["pause_after"] > D else ""
        md.append(f"- **{s['id']}** {s['text']}{p}\n  - *Visual:* {s['visual']}")
    (out / "script.md").write_text("\n".join(md) + "\n")
    print(md[1])
