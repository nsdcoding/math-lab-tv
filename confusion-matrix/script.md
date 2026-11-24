# The Confusion Matrix Explained: Accuracy, Precision and Recall

214 segments · 3918 words · est. 25.7 min (voice ≈165 wpm + 119 s pauses) · target 25–30 min


## Two Fraud Detectors  ·  172 words, ~63 s

- **s001** Imagine you run the card team at a small bank.
  - *Visual:* Illustration sticker: a person at a desk with a bank-card terminal; chip 'illustration'.
- **s002** Every day, ten thousand card payments go through. And about one in every hundred of them is fraud.
  - *Visual:* A 100×100 dot field fills (10,000 dots); 100 of them turn red. Counter: '10,000 payments · 100 fraud'.
- **s003** Two companies want to sell you a fraud detector.
  - *Visual:* Two sealed boxes labelled 'Detector A' and 'Detector B' slide in.
- **s004** The first one says: our model catches ninety percent of fraud.
  - *Visual:* Detector A speech chip: 'catches 90% of fraud'.
- **s005** The second one says: ninety percent of our alarms are real fraud.
  - *Visual:* Detector B speech chip: '90% of our alarms are real'.
- **s006** And both of them add: by the way, we are more than ninety-nine percent accurate. ⏸0.8s
  - *Visual:* Both chips gain a gold '99%+ accurate' badge.
- **s007** They sound like the same promise. Ninety, ninety, ninety-nine.
  - *Visual:* The three numbers pulse in a row: 90 · 90 · 99.
- **s008** But they are completely different promises. One of these detectors would let more than half of the fraud walk straight past you. ⏸1.0s
  - *Visual:* Detector B's box opens: 55 red dots slip past a gate. Label 'misses 55 of 100'.
- **s009** And here's the strangest part. A detector that does nothing at all, that never raises a single alarm, is ninety-nine percent accurate too. ⏸1.2s
  - *Visual:* A third empty box 'Detector Zero' with a gold '99% accurate' badge; inside, nothing.
- **s010** At the end of our prosecutor's fallacy video, I left you with this exact puzzle. Today, we solve it.
  - *Visual:* Chip 'from: The Prosecutor's Fallacy' slides in under the boxes.
- **s011** With one small table, two by two, that tells you the whole truth about any yes or no prediction.
  - *Visual:* The dot field collapses into an empty 2×2 grid.
- **s012** It's called the confusion matrix. ⏸1.0s
  - *Visual:* Title card: 'THE CONFUSION MATRIX' / 'accuracy · precision · recall'.

## Welcome  ·  65 words, ~24 s

- **s013** Welcome to Math Lab TV. Where math is something you can see. ⏸0.7s
  - *Visual:* Logo (violet rounded square with a green bell curve) + MATH LAB TV + tagline 'where math is something you can see'.
- **s014** Today you will learn the four boxes of the confusion matrix, and how to fill them from real counts.
  - *Visual:* Big ① + mini 2×2 grid filling with dots + caption 'the four outcomes'; small logo top-right.
- **s015** You will see why accuracy can lie, and what precision and recall tell you instead.
  - *Visual:* Big ② + mini grid with one column and one row lighting up + caption 'accuracy · precision · recall'.
- **s016** And you will practise on four real examples, until you can read any of these tables on your own. ⏸0.6s
  - *Visual:* Big ③ + four tiny grids (fraud, medical test, spam, loans) + caption 'four worked examples'.

## Why Accuracy Isn't Enough  ·  179 words, ~65 s

- **s017** Let's start with that lazy detector, because it shows the whole problem.
  - *Visual:* Detector Zero returns, centre stage.
- **s018** Its rule is simple. Whatever the payment is, say: not fraud.
  - *Visual:* A rubber stamp 'NOT FRAUD' slams on payment after payment.
- **s019** Out of ten thousand payments, nine thousand nine hundred really are fine. So it gets all of those right.
  - *Visual:* Bar on a 0–10,000 axis: 9,900 grey dots get green ticks.
- **s020** The one hundred frauds, it gets wrong. Every single one.
  - *Visual:* The 100 red dots get red crosses.
- **s021** Nine thousand nine hundred right, out of ten thousand. That's ninety-nine percent accuracy. ⏸0.8s
  - *Visual:* Fraction 9,900 / 10,000 = 99% builds on screen, gold.
- **s022** And it caught zero fraud. Not one. ⏸1.2s
  - *Visual:* Big '0 fraud caught' in red next to the 99%.
- **s023** So accuracy, on its own, can't tell a useless detector from a good one.
  - *Visual:* Two gauges side by side, both reading 99%; one labelled 'useless', one '?'.
- **s024** This happens whenever the thing you are looking for is rare.
  - *Visual:* Axis 'how rare is the thing you look for' from common → rare; a 'danger zone' at the rare end.
- **s025** Fraud is rare. Serious diseases are rare. Faulty parts on a factory line are rare. Hackers in your network logs are rare.
  - *Visual:* Four icon cards: card, heart, gear, laptop, each with 'rare' tag.
- **s026** And those are exactly the cases where getting it wrong costs the most.
  - *Visual:* The four cards tint red.
- **s027** In our Bayes video, we saw a test that was ninety percent accurate, where a positive result meant only about a one in twelve chance of being sick.
  - *Visual:* Chip 'from: Bayes' Theorem' + mini 1,000-dot grid with 9 vs 99 highlighted.
- **s028** The confusion matrix is the tool that keeps all of those numbers in one place, so nothing gets hidden. ⏸0.6s
  - *Visual:* Mini Bayes grid morphs into an empty 2×2 grid.

## The Four Outcomes  ·  409 words, ~149 s

- **s029** Every time a detector looks at a payment, two things are true.
  - *Visual:* One payment card in the centre, two question tags.
- **s030** First, what actually happened. Was it really fraud, or not?
  - *Visual:* Tag 1: 'the truth: fraud or not?'
- **s031** Second, what the detector said. Did it raise an alarm, or stay quiet?
  - *Visual:* Tag 2: 'the guess: alarm or quiet?'
- **s032** Two questions, two answers each. That gives four possible outcomes. No more, no less. ⏸0.6s
  - *Visual:* 2 × 2 = 4 appears; tree with two branches splitting into four leaves.
- **s033** Let's lay them out in a grid. The rows are the truth. The top row is real fraud. The bottom row is not fraud.
  - *Visual:* 2×2 grid on real axes. Row labels: 'really fraud' (top), 'really fine' (bottom). Axis title 'the truth'.
- **s034** The columns are what the detector said. The left column is: alarm. The right column is: quiet.
  - *Visual:* Column labels: 'alarm' (left), 'quiet' (right). Axis title 'the guess'.
- **s035** Now let's name each box carefully, because the names trip everyone up.
  - *Visual:* The four boxes pulse one by one, empty.
- **s036** Top left. It really was fraud, and the detector raised an alarm. A correct catch. We call it a true positive. ⏸0.6s
  - *Visual:* Top-left fills aqua: 'TRUE POSITIVE (TP)' + tiny icon 'fraud → alarm ✓'.
- **s037** Positive means the detector said yes, this is the thing. True means it was right.
  - *Visual:* Word 'POSITIVE' glows → arrow to 'detector said yes'; 'TRUE' → 'it was right'.
- **s038** Bottom right. It was a normal payment, and the detector stayed quiet. Also correct. That's a true negative. ⏸0.6s
  - *Visual:* Bottom-right fills aqua: 'TRUE NEGATIVE (TN)'.
- **s039** Now the mistakes. Bottom left. A perfectly normal payment, but the detector raised an alarm anyway.
  - *Visual:* Bottom-left box outlines in orange.
- **s040** A false alarm. We call it a false positive. The detector said yes, and it was wrong. ⏸0.6s
  - *Visual:* Bottom-left fills orange: 'FALSE POSITIVE (FP)' + 'false alarm'.
- **s041** And top right. Real fraud, and the detector said nothing. The fraud slipped through.
  - *Visual:* Top-right box outlines in blue; a red dot slips through a gate.
- **s042** A miss. We call it a false negative. The detector said no, and it was wrong. ⏸0.6s
  - *Visual:* Top-right fills blue: 'FALSE NEGATIVE (FN)' + 'a miss'.
- **s043** Here's a trick to remember them. The second word is what the detector said. The first word is whether that was right. ⏸1.0s
  - *Visual:* Two-part decoder card: 'FALSE | POSITIVE' → 'was it right? | what it said'.
- **s044** So a false negative is: it said negative, and that was false. It said no, but the answer was yes.
  - *Visual:* Decoder applied to 'FALSE NEGATIVE' step by step.
- **s045** Let's try it slowly with just ten payments, before we use the big numbers. Three of them are fraud.
  - *Visual:* Warm-up chip; ten numbered payment cards in a row, three with a red corner (fraud).
- **s046** Payment one is fraud, and the detector raises an alarm. Fraud row, alarm column. A true positive.
  - *Visual:* Card 1 flies into the top-left box.
- **s047** Payment two is a normal coffee, and the detector stays quiet. Fine row, quiet column. A true negative.
  - *Visual:* Card 2 flies into the bottom-right box.
- **s048** Payment three is a normal payment, but it's a big one in another country, so the detector panics. A false positive.
  - *Visual:* Card 3 flies into the bottom-left box.
- **s049** Payment four is fraud, but a small one, and it slips through. A false negative.
  - *Visual:* Card 4 flies into the top-right box.
- **s050** We keep going, one payment at a time, until all ten are sorted.
  - *Visual:* Cards 5–10 fly into their boxes quickly.
- **s051** Two true positives, one false negative, two false positives, and five true negatives. Two plus one plus two plus five is ten. Every payment has exactly one home. ⏸1.0s
  - *Visual:* Counts appear: TP 2 · FN 1 · FP 2 · TN 5; total 10 ✓.
- **s052** The two correct boxes sit on one diagonal. The two kinds of mistake sit on the other. ⏸1.0s
  - *Visual:* Diagonal line through TP and TN glows aqua; the anti-diagonal through FP and FN glows red.

## Filling the Grid  ·  217 words, ~79 s

- **s053** Now let's fill this grid with Detector A, the one that catches ninety percent of fraud.
  - *Visual:* Grid stays; chip 'Detector A' at the top.
- **s054** We run it on our ten thousand payments, and sort every payment into one of the four boxes.
  - *Visual:* Dots stream out of the 10,000-dot field into the four boxes.
- **s055** Start with the one hundred real frauds. They all belong in the top row.
  - *Visual:* 100 red dots move to the top row; row total '100'.
- **s056** Detector A raises an alarm on ninety of them. Ninety true positives.
  - *Visual:* 90 red dots stack in the top-left box; counter '90'.
- **s057** The other ten get through. Ten false negatives. ⏸0.6s
  - *Visual:* 10 red dots stack in the top-right box; counter '10'.
- **s058** Now the nine thousand nine hundred normal payments. They belong in the bottom row.
  - *Visual:* Grey dots pour into the bottom row; row total '9,900'.
- **s059** Detector A wrongly flags thirty of them. Thirty false positives. Thirty customers who get a worried phone call for nothing.
  - *Visual:* 30 grey dots stack in the bottom-left; counter '30'; tiny phone icon.
- **s060** And the remaining nine thousand eight hundred and seventy are correctly left alone. True negatives. ⏸0.8s
  - *Visual:* Bottom-right counter rolls to '9,870'.
- **s061** Let's check our work. Ninety plus ten is one hundred. That's every fraud.
  - *Visual:* Top row: 90 + 10 = 100 ✓.
- **s062** Thirty plus nine thousand eight hundred and seventy is nine thousand nine hundred. That's every normal payment.
  - *Visual:* Bottom row: 30 + 9,870 = 9,900 ✓.
- **s063** And all four boxes together make ten thousand. Every payment lands in exactly one box. ⏸0.6s
  - *Visual:* Grand total 10,000 ✓ in the corner.
- **s064** Now add up the left column. Ninety plus thirty is one hundred and twenty. That's every alarm Detector A raised.
  - *Visual:* Left column total: 90 + 30 = 120, label 'all alarms'.
- **s065** So the rows tell you the truth. The columns tell you what the detector did. Hold on to that, because every number in this video comes from reading this grid by row, or by column. ⏸1.0s
  - *Visual:* Row arrows labelled 'truth', column arrows labelled 'what it did'.

## Accuracy  ·  218 words, ~79 s

- **s066** Let's start with the number the salespeople love. Accuracy.
  - *Visual:* Formula card title 'ACCURACY'.
- **s067** Accuracy asks one question: out of everything, how often was the detector right?
  - *Visual:* Plain question under the title.
- **s068** Right means the diagonal. True positives plus true negatives.
  - *Visual:* TP and TN boxes glow aqua.
- **s069** Then divide by everything. All four boxes.
  - *Visual:* Whole grid outlined.
- **s070** In symbols, accuracy equals T P plus T N, over the total. T P is short for true positives. T N is short for true negatives.
  - *Visual:* LaTeX: accuracy = (TP + TN) / total, with plain-word labels under TP and TN.
- **s071** For Detector A, that's ninety plus nine thousand eight hundred and seventy. Nine thousand nine hundred and sixty right answers.
  - *Visual:* 90 + 9,870 = 9,960 builds in Inter.
- **s072** Out of ten thousand. That's ninety-nine point six percent. ⏸0.8s
  - *Visual:* 9,960 / 10,000 = 99.6% in gold.
- **s073** Sounds amazing. But remember the lazy detector scored ninety-nine percent by doing nothing.
  - *Visual:* Gauge: lazy 99% next to Detector A 99.6%.
- **s074** So all of Detector A's real work, catching ninety frauds, only moves accuracy from ninety-nine to ninety-nine point six. Less than one point. ⏸1.0s
  - *Visual:* Zoom on the gap between 99 and 99.6 on a 98–100 axis; label 'all the real work'.
- **s075** Why? Because the bottom right box is huge. Nine thousand eight hundred and seventy easy, boring, correct answers drown out everything else.
  - *Visual:* Bottom-right box swells until it squashes the other three; label 'the easy majority'.
- **s076** That's the rule of thumb. When one class is rare, accuracy is mostly a measure of how rare it is. ⏸1.2s
  - *Visual:* Rule-of-thumb card (warn border): 'rare class → accuracy mostly measures rarity'.
- **s077** Accuracy is not useless. When the two groups are roughly the same size, it's a fine first look. We'll see that in the spam example later.
  - *Visual:* Small balanced grid preview (300 vs 700) with an 'OK here' tag.
- **s078** But for rare things, we need questions that zoom in on the fraud itself. And there are exactly two of them. ⏸0.6s
  - *Visual:* Two spotlights appear over the grid: one vertical, one horizontal.

## Precision  ·  191 words, ~69 s

- **s079** The first question is about your alarms.
  - *Visual:* Bell icon over the left column.
- **s080** Picture the analyst who has to phone every flagged customer. They only ever see the alarms. They never see the quiet payments.
  - *Visual:* Everything except the left column dims.
- **s081** So their question is: when the detector raises an alarm, how often is it real?
  - *Visual:* Question card: 'When it says FRAUD, how often is it right?'
- **s082** That's precision. And it lives entirely in the left column. ⏸0.6s
  - *Visual:* Left column lights up violet; title 'PRECISION'.
- **s083** Precision equals true positives, over all the alarms. T P, over T P plus F P. F P is short for false positives, the false alarms.
  - *Visual:* LaTeX: precision = TP / (TP + FP), labels 'real catches' over 'all alarms'.
- **s084** For Detector A, the left column holds ninety real frauds and thirty false alarms.
  - *Visual:* Left column: 90 red dots over 30 grey dots.
- **s085** Ninety, out of one hundred and twenty. That's three out of every four. Seventy-five percent precision. ⏸1.0s
  - *Visual:* 90 / 120 = 3/4 = 75%; the 120 alarm dots rearrange into 30 rows of 4, three red one grey.
- **s086** In plain words: every time Detector A rings the bell, there's a three in four chance it's real fraud, and a one in four chance it's a false alarm.
  - *Visual:* Bell rings; 3 of 4 cards say 'real', 1 says 'false alarm'.
- **s087** Notice what precision ignores. It doesn't care about the right column at all. It doesn't know how much fraud got away.
  - *Visual:* Right column greys out with a 'not counted' tag.
- **s088** A detector that raised one single alarm, and happened to be right, would have perfect precision. One out of one. ⏸1.0s
  - *Visual:* Tiny grid: a single dot in TP, 1/1 = 100% precision, with a '?' over the 99 missed frauds.
- **s089** So precision alone can be gamed by being very, very cautious. ⏸0.6s
  - *Visual:* Label 'cautious = high precision' in warn.

## Recall  ·  264 words, ~96 s

- **s090** That's why we need the second question. It's about what you missed.
  - *Visual:* Back to the full grid; magnifying glass on the top row.
- **s091** Picture the bank's fraud manager. They care about every fraud that happened, whether the detector noticed it or not.
  - *Visual:* Everything except the top row dims.
- **s092** Their question is: out of all the real fraud, how much did we catch?
  - *Visual:* Question card: 'Of all the real fraud, how much did we catch?'
- **s093** That's recall. And it lives entirely in the top row. ⏸0.6s
  - *Visual:* Top row lights up orange; title 'RECALL'.
- **s094** Recall equals true positives, over all the real positives. T P, over T P plus F N. F N is short for false negatives, the misses.
  - *Visual:* LaTeX: recall = TP / (TP + FN), labels 'real catches' over 'all real fraud'.
- **s095** For Detector A, the top row holds ninety catches and ten misses.
  - *Visual:* Top row: 90 caught | 10 missed.
- **s096** Ninety, out of one hundred. Ninety percent recall. ⏸1.0s
  - *Visual:* 90 / 100 = 90% in orange.
- **s097** That's the first salesperson's claim. We catch ninety percent of fraud. That's a recall claim. ⏸1.0s
  - *Visual:* Detector A's chip 'catches 90% of fraud' flies onto the top row and snaps into the word RECALL.
- **s098** You'll also hear recall called sensitivity, or the true positive rate. Same number, different names.
  - *Visual:* Synonym tags under RECALL: 'sensitivity', 'true positive rate'.
- **s099** There's also a matching number for the bottom row, called specificity. Of all the normal payments, how many did we leave alone? For Detector A, nine thousand eight hundred and seventy out of nine thousand nine hundred. Almost all of them. We'll need it when we meet the R O C curve.
  - *Visual:* Bottom row lights aqua briefly: 'SPECIFICITY = TN / (TN + FP)' = 9,870/9,900 ≈ 99.7%.
- **s100** And recall has its own blind spot. It ignores the bottom row, so it never sees false alarms.
  - *Visual:* Bottom row greys out, 'not counted'.
- **s101** A detector that flags every single payment as fraud catches all one hundred frauds. One hundred percent recall.
  - *Visual:* Every dot jumps into the left column; recall 100/100 = 100%.
- **s102** And it phones all ten thousand customers. That's useless too. ⏸1.0s
  - *Visual:* A wall of 10,000 phone icons; precision drops to 1%.
- **s103** So here's the picture to keep. Precision reads down the alarm column. Recall reads across the fraud row. They share one box, the true positives, and look away from each other in every other direction. ⏸1.5s
  - *Visual:* Same grid: left column violet, top row orange; the TP corner where they cross glows white.

## The Trade-off  ·  381 words, ~139 s

- **s104** Now we can finally answer the puzzle. Let's fill the grid for Detector B, the one whose alarms are ninety percent real.
  - *Visual:* Second grid appears beside Detector A's; chip 'Detector B'.
- **s105** Detector B is much more careful. It only raises fifty alarms.
  - *Visual:* Left column of B: 50 dots.
- **s106** Forty-five of them are real fraud. Five are false alarms. So its precision is forty-five out of fifty. Ninety percent. Its claim was true. ⏸0.8s
  - *Visual:* 45 red + 5 grey; 45/50 = 90% precision in violet.
- **s107** But look at the top row. Forty-five caught. And fifty-five frauds missed.
  - *Visual:* Top row of B: 45 | 55, the 55 in blue.
- **s108** Its recall is forty-five out of one hundred. Forty-five percent. It lets more than half the fraud walk straight past. ⏸1.2s
  - *Visual:* 45/100 = 45% recall; 55 red dots walk out through a gate.
- **s109** And its accuracy? Forty-five plus nine thousand eight hundred and ninety-five, out of ten thousand. Ninety-nine point four percent. Still sounds amazing. ⏸0.8s
  - *Visual:* Accuracy 9,940 / 10,000 = 99.4% gold badge.
- **s110** So side by side. Detector A: precision seventy-five, recall ninety. Detector B: precision ninety, recall forty-five.
  - *Visual:* Comparison table on axes: two bars each for precision (violet) and recall (orange).
- **s111** Each salesperson quoted the number that made them look good. Neither was lying. They just answered different questions. ⏸1.0s
  - *Visual:* Each chip slides onto its own bar.
- **s112** In fact, this is the same swap we saw in the prosecutor's fallacy. How often does an alarm mean fraud, versus how often does fraud cause an alarm.
  - *Visual:* Chip 'from: The Prosecutor's Fallacy': two arrows 'alarm → fraud?' and 'fraud → alarm?'.
- **s113** Now here's the key idea. A and B are often the same model, with the dial set differently.
  - *Visual:* Both detectors merge into one box with a dial.
- **s114** Most detectors give each payment a score, say from zero to one, for how suspicious it looks. Then you pick a cut-off. Above it, alarm. Below it, quiet.
  - *Visual:* Number line 0–1 with payment dots placed by score; a vertical cut-off line.
- **s115** Set the cut-off high, and only the most suspicious payments get flagged. Fewer false alarms, more misses. High precision, low recall. That's Detector B.
  - *Visual:* Cut-off slides right; precision bar rises, recall bar falls.
- **s116** Set it low, and you flag lots of payments. More catches, more false alarms. High recall, low precision. That's Detector A.
  - *Visual:* Cut-off slides left; recall rises, precision falls.
- **s117** Push it even lower, and you get a nervous Detector C. It flags four hundred payments and catches ninety-nine of the hundred frauds.
  - *Visual:* Third grid 'Detector C': 99 | 1 over 301 | 9,599.
- **s118** Ninety-nine percent recall. But only ninety-nine of its four hundred alarms are real. Precision is about one in four.
  - *Visual:* Recall 99% orange; precision 99/400 ≈ 25% violet.
- **s119** And its accuracy drops to about ninety-seven percent, lower than the lazy detector that catches nothing. Accuracy is pointing the wrong way. ⏸1.2s
  - *Visual:* Accuracy 96.98% badge below lazy 99%; red arrow 'wrong way'.
- **s120** That's the trade-off. Move the dial one way, precision goes up and recall goes down. Move it back, and they swap. You almost never get both for free. ⏸1.0s
  - *Visual:* Seesaw (beam_scale) with precision on one end, recall on the other, tipping as the dial moves.
- **s121** In a future video, we'll trace this whole dial on one curve, called the R O C curve. For now, just remember: the dial exists. ⏸0.6s
  - *Visual:* Small teaser chip 'later: the ROC curve'.

## The F1 Score  ·  256 words, ~93 s

- **s122** But sometimes you need one number. To rank ten models, or to put on a report.
  - *Visual:* Ten model cards in a row, each with two bars, and a '?' for a single score.
- **s123** The usual compromise is called the F one score. It blends precision and recall into a single number.
  - *Visual:* Title 'F1 SCORE: one number, two questions'.
- **s124** You might think: just average them. For Detector A, seventy-five and ninety average to eighty-two and a half.
  - *Visual:* (75 + 90) / 2 = 82.5 crossed out lightly as 'plain average'.
- **s125** But a plain average has a problem. Remember the detector that flags everything? Recall one hundred, precision one. The average is fifty point five, which sounds half decent for a useless detector. ⏸0.8s
  - *Visual:* Example: (100 + 1)/2 = 50.5 with red 'too kind'.
- **s126** The F one score uses a stricter average, called the harmonic mean, that gets dragged down hard by whichever number is worse.
  - *Visual:* Two bars; a weight hangs from the shorter one, pulling the F1 marker toward it.
- **s127** Here's the friendliest way to compute it. F one equals two T P, over two T P plus F P plus F N.
  - *Visual:* LaTeX: F1 = 2TP / (2TP + FP + FN), each part labelled in plain words.
- **s128** In words: count the true positives twice, then compare them with all the mistakes. Both kinds of mistake count against you.
  - *Visual:* TP box doubles; FP and FN boxes slide next to it on a single bar.
- **s129** For Detector A: two times ninety is one hundred and eighty. Plus thirty false alarms, plus ten misses, is two hundred and twenty.
  - *Visual:* 180 / (180 + 30 + 10) = 180 / 220.
- **s130** One hundred and eighty over two hundred and twenty. Nine elevenths. About eighty-two percent. ⏸0.8s
  - *Visual:* 180/220 = 9/11 ≈ 82% in violet.
- **s131** For Detector B: two times forty-five is ninety. Plus five plus fifty-five. Ninety over one hundred and fifty. Sixty percent.
  - *Visual:* 90 / 150 = 60%.
- **s132** And the flag everything detector? Its F one is about two percent. The harmonic mean is not fooled. ⏸1.0s
  - *Visual:* F1 = 200 / (200 + 9,900) ≈ 2% in red.
- **s133** So by F one, Detector A wins. But be careful. F one assumes a miss and a false alarm are equally bad. And in the real world, they almost never are. ⏸1.0s
  - *Visual:* F1 ranking A > B; caution card 'assumes both mistakes cost the same'.

## Which Error Is Worse?  ·  221 words, ~80 s

- **s134** So the real question is not which number is highest. It's which mistake would you rather make.
  - *Visual:* Two boxes, FP (orange) and FN (blue), on a balance beam.
- **s135** Let's put a price on each one. These are made up numbers, just to show the idea.
  - *Visual:* Chip 'illustration: made-up costs'.
- **s136** Say a missed fraud costs the bank five hundred dollars. And a false alarm costs about five dollars, a few minutes of an analyst's time on the phone.
  - *Visual:* Price tags: FN = $500, FP = $5.
- **s137** Detector A: ten misses times five hundred, plus thirty false alarms times five. Five thousand one hundred and fifty dollars.
  - *Visual:* 10 × 500 + 30 × 5 = 5,150 bar.
- **s138** Detector B: fifty-five misses times five hundred, plus five times five. Twenty-seven thousand five hundred and twenty-five dollars.
  - *Visual:* 55 × 500 + 5 × 5 = 27,525 bar, much taller.
- **s139** Nervous Detector C: one miss, plus three hundred and one false alarms. Only two thousand and five dollars. The cheapest of all.
  - *Visual:* 1 × 500 + 301 × 5 = 2,005 bar, shortest.
- **s140** And the lazy detector? A hundred misses. Fifty thousand dollars. ⏸1.0s
  - *Visual:* 100 × 500 = 50,000 bar off the top; axis rescales.
- **s141** With these prices, the detector with the worst accuracy, C, is the best choice. Because misses are so expensive, you want high recall. ⏸1.0s
  - *Visual:* C bar crowned; label 'high recall wins when misses are expensive'.
- **s142** But change the prices. Suppose every false alarm freezes a customer's card at the checkout, and they get so annoyed that it costs two hundred dollars in lost business.
  - *Visual:* FP price tag flips from $5 to $200.
- **s143** Now Detector C costs over sixty thousand dollars, and Detector A wins easily, at eleven thousand. ⏸1.2s
  - *Visual:* Bars redraw: C = 60,700 (worst), A = 11,000 (best), B = 28,500.
- **s144** Same grids. Same counts. Different answer. The confusion matrix gives you the counts. Only you can decide what each mistake costs. ⏸1.5s
  - *Visual:* The four grids stay, a big hand turns the dial; caption 'the counts are math, the costs are your call'.

## Example: A Medical Test  ·  342 words, ~124 s

- **s145** Let's practise reading these grids on a few more examples, each with real counts.
  - *Visual:* Four small grids appear: 'medical test', 'spam filter', 'loans', ticks over the first.
- **s146** First, an old friend. The screening test from our Bayes video.
  - *Visual:* Chip 'from: Bayes' Theorem'.
- **s147** One thousand people. One in a hundred has the condition, so ten are sick and nine hundred and ninety are healthy.
  - *Visual:* Row totals fill: sick 10, healthy 990.
- **s148** The test catches nine of the ten sick people. So nine true positives and one false negative.
  - *Visual:* Top row: 9 | 1.
- **s149** And it gives a false alarm to one in ten healthy people. That's ninety-nine false positives, and eight hundred and ninety-one true negatives. ⏸0.8s
  - *Visual:* Bottom row: 99 | 891.
- **s150** Recall: nine out of ten. Ninety percent. The test is good at finding sick people.
  - *Visual:* Top row lights orange: 9/10 = 90%.
- **s151** Accuracy: nine plus eight hundred and ninety-one, out of a thousand. Ninety percent again.
  - *Visual:* Diagonal lights aqua: 900/1,000 = 90%.
- **s152** But precision. Look down the alarm column. Nine real cases, and ninety-nine false alarms. Nine out of one hundred and eight.
  - *Visual:* Left column lights violet: 9 red dots, 99 grey.
- **s153** That's one in twelve. The exact same answer we found with Bayes' theorem. ⏸1.2s
  - *Visual:* 9/108 = 1/12 with chip 'same as Bayes'.
- **s154** So here's the connection. Bayes' theorem was secretly a precision calculation. It asked: given an alarm, how likely is it real? ⏸1.0s
  - *Visual:* Label 'P(sick | positive) = precision'; Bayes formula fades in beside the grid column.
- **s155** Now watch what happens if we use the exact same test in a different crowd.
  - *Visual:* The grid slides left; a second empty grid appears, chip 'same test, different crowd'.
- **s156** Say a specialist clinic, where people already have symptoms, and half of the thousand are sick. Five hundred sick, five hundred healthy.
  - *Visual:* Row totals: 500 | 500.
- **s157** The test still catches nine in ten sick people. Four hundred and fifty caught, fifty missed.
  - *Visual:* Top row: 450 | 50.
- **s158** And it still gives false alarms to one in ten healthy people. Fifty false positives, four hundred and fifty true negatives.
  - *Visual:* Bottom row: 50 | 450.
- **s159** Recall is still ninety percent. But precision jumps from one in twelve, to four hundred and fifty out of five hundred. Ninety percent. ⏸1.0s
  - *Visual:* Precision 450/500 = 90% violet vs 1/12 on the first grid.
- **s160** Same test. Recall didn't move. Precision changed completely, just because the crowd changed. So precision always depends on how common the thing is. Remember that whenever someone quotes you a precision from a different setting. ⏸1.2s
  - *Visual:* Two grids side by side; recall bars equal, precision bars wildly different; caption 'precision depends on how common it is'.
- **s161** In medicine, recall is usually the priority for a first screening. Missing a sick person is the costly mistake.
  - *Visual:* FN box glows blue 'costly'.
- **s162** Low precision is acceptable here, because every positive gets a second, more careful test. That's the honest way to use it. ⏸0.6s
  - *Visual:* Arrow from the alarm column to a second test box, 'confirm before worrying'.

## Example: A Spam Filter  ·  198 words, ~72 s

- **s163** Second example. A spam filter, where the mistakes flip.
  - *Visual:* Envelope icons; chip 'spam filter'.
- **s164** One thousand emails. Three hundred are spam, seven hundred are real.
  - *Visual:* Row totals: spam 300, real 700.
- **s165** The filter sends two hundred and eighty emails to the spam folder. Two hundred and seventy really are spam. Ten are real emails.
  - *Visual:* Left column: 270 | 10.
- **s166** So thirty spam emails reach your inbox, and six hundred and ninety real emails land safely. ⏸0.8s
  - *Visual:* Right column: 30 | 690.
- **s167** Precision: two hundred and seventy out of two hundred and eighty. About ninety-six percent.
  - *Visual:* 270/280 ≈ 96.4% violet.
- **s168** Recall: two hundred and seventy out of three hundred. Ninety percent.
  - *Visual:* 270/300 = 90% orange.
- **s169** Accuracy: nine hundred and sixty out of a thousand. Ninety-six percent.
  - *Visual:* 960/1,000 = 96% gold.
- **s170** And notice, here accuracy is more honest. Spam isn't rare. A lazy filter that never marks anything as spam would only score seventy percent, so it can't hide. ⏸1.0s
  - *Visual:* Lazy filter badge: 700/1,000 = 70%.
- **s171** Now, which mistake is worse? A spam email in your inbox is a small annoyance. You delete it.
  - *Visual:* FN box: 'annoying, delete it'.
- **s172** But a real email in the spam folder, a job offer, a bill, a message from your doctor, might never be read.
  - *Visual:* FP box glows orange: three envelopes falling into a bin.
- **s173** So for spam, the false alarm is the costly mistake. You want high precision, even if a few more spam emails get through. ⏸1.2s
  - *Visual:* Seesaw tips toward precision.
- **s174** Same table, same formulas. But the opposite priority from the medical test. ⏸0.6s
  - *Visual:* Medical grid and spam grid side by side: recall starred on one, precision starred on the other.

## Your Turn: Loan Defaults  ·  208 words, ~76 s

- **s175** Now it's your turn. Pause whenever you like.
  - *Visual:* Pause icon; chip 'your turn'.
- **s176** A lender has two thousand loans. Two hundred of them will default, meaning the borrower stops paying.
  - *Visual:* Row totals: default 200, repay 1,800.
- **s177** A model flags two hundred and fifty loans as risky. One hundred and fifty of them really do default. One hundred are fine.
  - *Visual:* Left column: 150 | 100.
- **s178** Try to fill the rest of the grid, and find the precision and the recall. ⏸3.0s
  - *Visual:* Right column shows '?' and '?'; timer ring.
- **s179** Here's the grid. Two hundred defaults, minus one hundred and fifty caught, leaves fifty missed.
  - *Visual:* Top-right fills: 200 − 150 = 50.
- **s180** One thousand eight hundred good loans, minus one hundred false alarms, leaves one thousand seven hundred true negatives. ⏸0.6s
  - *Visual:* Bottom-right fills: 1,800 − 100 = 1,700.
- **s181** Precision: one hundred and fifty out of two hundred and fifty flagged. Sixty percent.
  - *Visual:* Left column violet: 150/250 = 60%.
- **s182** Recall: one hundred and fifty out of two hundred defaults. Seventy-five percent.
  - *Visual:* Top row orange: 150/200 = 75%.
- **s183** Accuracy: one hundred and fifty plus one thousand seven hundred, out of two thousand. Ninety-two and a half percent.
  - *Visual:* 1,850/2,000 = 92.5% gold, next to the lazy model's 90%.
- **s184** And the F one score: three hundred, over three hundred plus one hundred plus fifty. Three hundred over four hundred and fifty. Two thirds. ⏸1.0s
  - *Visual:* F1 = 300/450 = 2/3 ≈ 67% violet.
- **s185** So, in plain words. When this model says risky, it's right six times out of ten. And it spots three out of every four loans that will go bad. ⏸1.0s
  - *Visual:* Two plain-word sentence cards under the grid.
- **s186** If you got those, you can now read any confusion matrix you'll ever see. ⏸0.6s
  - *Visual:* Green check stamp on the grid.

## Where You'll Use It  ·  164 words, ~60 s

- **s187** So where will you actually meet this table?
  - *Visual:* Four tiles: ML, DS, Finance, CS.
- **s188** In machine learning, it's the first thing printed after training any classifier. Any model that answers yes or no. Is this a cat? Will this customer cancel?
  - *Visual:* ML tile: a model box outputs a 2×2 grid.
- **s189** And when the thing you're predicting is rare, people report precision and recall, never accuracy alone. Exactly because of the lazy detector.
  - *Visual:* Mini lazy-detector badge '99%' crossed out.
- **s190** In data science, it's how you explain a model to people who don't build models. Of every hundred alarms, this many are real. Of every hundred cases, we catch this many.
  - *Visual:* DS tile: a report card with two plain sentences.
- **s191** In finance, it's fraud detection and credit risk, exactly the two examples we worked through. And the cut-off is set by the cost of each mistake.
  - *Visual:* Finance tile: card + loan icons with the cost bars from earlier.
- **s192** In computer science, it's spam filters, malware scanners, and systems that watch network traffic for intruders. Too many false alarms, and people learn to ignore them.
  - *Visual:* CS tile: shield + inbox; a pile of ignored alarms.
- **s193** And beyond those four: medical tests, airport security, factory quality checks. Anywhere a yes or no decision can be wrong in two different ways. ⏸0.6s
  - *Visual:* Three more small icons fade in around the tiles.

## Common Mistakes  ·  149 words, ~54 s

- **s194** Let's go through the mistakes beginners make most often.
  - *Visual:* Red 'common mistakes' header.
- **s195** Mistake one: trusting accuracy when the class is rare. Always ask how rare it is, and compare with the lazy model that always says no. ⏸0.8s
  - *Visual:* Card ①: lazy 99% vs model 99.6%; arrow 'compare with the baseline'.
- **s196** Mistake two: mixing up precision and recall. Here's the fix. Precision starts from the alarms. Recall starts from the real cases.
  - *Visual:* Card ②: grid with 'start from the alarms' on the column, 'start from the real cases' on the row.
- **s197** Ask yourself: am I dividing by everything the model flagged, or by everything that was really there? ⏸0.8s
  - *Visual:* Two denominators: 'all flagged' (violet) vs 'all really there' (orange).
- **s198** Mistake three: assuming every table is laid out the same way. Some tools put the truth in the rows, some in the columns. Some put the positive class first, some last.
  - *Visual:* Card ③: our grid, then the same grid transposed and flipped; labels highlighted.
- **s199** So before you read any number, read the labels. Find the alarm column and the real fraud row first. ⏸0.8s
  - *Visual:* Finger traces the axis labels.
- **s200** And a bonus mistake: judging a model by one number. Any single score, even F one, hides which mistake the model makes. Look at the whole grid. ⏸1.0s
  - *Visual:* Bonus card: F1 82% with a curtain pulled back to reveal the full grid.

## Recipe  ·  155 words, ~56 s

- **s201** Here's the whole method as a recipe.
  - *Visual:* Recipe card, numbered 1–5.
- **s202** Step one: draw the grid. Truth in the rows, the detector's answer in the columns. Label them.
  - *Visual:* ① Draw the grid · truth = rows, guess = columns.
- **s203** Step two: fill the four boxes with counts, and check that the rows add up to the real totals.
  - *Visual:* ② Fill the counts · rows add up to the truth.
- **s204** Step three: for precision, read down the alarm column. Of everything flagged, how much was real?
  - *Visual:* ③ Precision · down the alarm column.
- **s205** Step four: for recall, read across the real row. Of everything real, how much did we catch?
  - *Visual:* ④ Recall · across the real row.
- **s206** Step five: decide which mistake costs more, and choose your cut-off to match. Use accuracy only when the groups are roughly balanced. ⏸0.8s
  - *Visual:* ⑤ Price the mistakes · then set the dial.
- **s207** Try it on Detector A. The grid: ninety, ten, thirty, nine thousand eight hundred and seventy. Precision: three in four. Recall: nine in ten. And if misses cost more, pick the detector with the higher recall. ⏸1.0s
  - *Visual:* The recipe steps tick off one by one beside Detector A's grid.
- **s208** Because a detector is not good or bad on its own. It's good or bad at the mistakes you can afford. ⏸1.5s
  - *Visual:* Closing line in large Inter Display, violet.

## Subscribe  ·  53 words, ~19 s

- **s209** Look around your world, and notice how many things quietly answer yes or no for you. Your inbox, your bank card, your phone's face unlock. Each one is making both kinds of mistake. ⏸0.6s
  - *Visual:* Four everyday cards (inbox, bank card, phone unlock, airport gate), each stamped with a tiny 2×2 grid.
- **s210** If this lesson made things clear for you, please subscribe to Math Lab TV, so we can keep building together. ⏸0.8s
  - *Visual:* Logo + red SUBSCRIBE button; a cursor clicks it; it turns grey 'SUBSCRIBED ✓'; 'so we can keep building together' appears.

## Next Time  ·  76 words, ~28 s

- **s211** But here's a puzzle for next time.
  - *Visual:* Small logo top-centre; puzzle icon.
- **s212** Our spam filter was right ninety-six times out of a hundred. But how does it decide, in the first place, that an email full of words like free, winner, and urgent is probably spam?
  - *Visual:* Email card with 'FREE', 'WINNER', 'URGENT' highlighted; a '?' over a dial reading 'spam score'.
- **s213** It turns out it's Bayes' theorem again, applied one word at a time. Next time, we'll build a spam filter from scratch, and see how it works.
  - *Visual:* 'next: How Spam Filters Work · Naive Bayes' chip under the logo.
- **s214** I will see you in the next video. ⏸2.0s
  - *Visual:* Logo + next chip hold.
