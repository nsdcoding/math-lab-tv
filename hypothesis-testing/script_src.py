#!/usr/bin/env python3
"""Source of truth for the narration. Run to emit script.json + script.md.

Running example (used everywhere; every number checked in verify_numbers.py):
  The coffee coin. A friend settles "who pays for coffee" with their own coin and always calls heads.
  20 flips, 15 heads (you paid 15 times, they paid 5).
  Null: the coin is fair (p_heads = 1/2). Expected 10 heads, standard deviation sqrt(5) ~ 2.24 heads.
  2^20 = 1,048,576 equally likely sequences. Ways to get >= 15 heads: 21,700  ->  p = 21700/1048576 ~ 0.0207
  "1,000 friends with fair coins": expected ~176 get exactly 10, ~15 get exactly 15, ~21 get 15 or more.
  14 heads: p = 60460/1048576 ~ 0.058 (above 0.05). So at alpha = 0.05 the line falls between 14 and 15.
  Two-sided (rigged either way): p doubles to ~0.041.
  Type I rate with "reject at >= 15": ~2.1 %.  If the coin really lands heads 70 % of the time:
  P(>= 15) ~ 0.416 -> miss ~58 %.  With 100 flips (reject at >= 59, false alarm ~4.4 %): power ~99.3 %.
  Bayes (illustration, 1 in 100 coins rigged at 70 % heads): P(rigged | >= 15 heads) ~ 17 %.
  Tiny effect: a 50.2 % coin flipped a million times -> 502,000 heads; fair-coin p ~ 0.00003 (3 in 100,000).
  20 independent tests at 0.05: chance of at least one false alarm ~ 64 %.
  5 sigma (one-sided) ~ 1 in 3.5 million.

Colour roles (one per concept, kept for the whole video):
  null / "boring explanation" / fair coin = blue      the friend's claim / alternative = orange
  observed result (15 heads)              = warn      tail area / p-value              = aqua
  significance line (alpha)               = violet    mistakes / errors                = red

Connections (from `python3 channel/channel.py refs hypothesis-testing`):
  Pays off: Bayes' teaser ("p = 0.03, '3% chance it's a fluke?' flips the question, like mistake one").
  Callbacks: bayes-examples (flipped question, 1 in 12) and standard-deviation (spread = 2.2 heads).
  Prerequisite not made: probability-distributions -> one-sentence intuition ("a picture of every outcome and
  how often it happens").  Teaser: prosecutors-fallacy.
"""
import json, pathlib, sys

SLUG = "hypothesis-testing"   # id in channel/catalog.json
TARGET_MIN = (15, 20)         # words ≈ minutes × 150 (voice ~165 wpm + pauses)
D = 0.35                      # default pause between segments
S = []
N = [0]   # auto-id counter; once voiced, insert new lines with explicit ids (e.g. s017a) so old clips stay cached


def seg(chapter, text, visual, pause=D, sid=None):
    if sid is None:
        N[0] += 1; sid = f"s{N[0]:03d}"
    S.append(dict(id=sid, chapter=chapter, text=text, visual=visual, pause_after=pause))


# ───────────── 1. HOOK ─────────────
c = "The Coffee Coin"
seg(c, "Every morning, you and a friend get coffee together. And every morning, you flip a coin to decide who pays.",
    "STICKER café: two friends at a small table, one about to flip a coin (illustration). Two coffee-cup icons slide in.")
seg(c, "It's always your friend's coin. And your friend always calls heads.",
    "A coin icon (blue rim) with 'H' face; chip 'their coin · they call heads'.")
seg(c, "After a month, you look back. Twenty flips. Heads came up fifteen times.",
    "Tally board on axes (x: flip 1–20, y: H/T): 15 orange H dots, 5 blue T dots fill in one by one; counter '15 heads / 20'.")
seg(c, "So you bought fifteen of the coffees. Your friend bought just five.",
    "Two stacks of cup icons on a count axis 0–15: 'you paid 15' (orange), 'they paid 5' (blue).", 1.0)
seg(c, "The first few times, it seemed like luck. Coins are random, right? But by the end of the month, you start to wonder.",
    "Calendar pages flip; the tally grows; a small thought bubble '…hmm' over the 'you' icon.")
seg(c, "So here's the question. Is that coin rigged? Or did your friend just get lucky?",
    "Split screen: left 'rigged?' (orange coin with a weight), right 'just luck?' (blue coin with a shrug). Big '?'.")
seg(c, "Take a second, and decide what you think.",
    "A slider between 'luck' and 'rigged' with a blinking cursor; small clock ticks.", 1.5)
seg(c, "Your gut probably says something is off. But a fair coin can come up heads fifteen times. It's not impossible.",
    "Coin spins; caption 'a fair coin CAN do this'.")
seg(c, "So how unusual is fifteen out of twenty, really? Unusual enough to call it rigged?",
    "A number line 0–20 heads with ticks every 5; a warn pin drops at 15; the space beyond it shimmers.")
seg(c, "There is a tool built for exactly this question. It's called hypothesis testing, and the number it gives you is called a p value.",
    "Title card: 'HYPOTHESIS TESTING' (aqua) with subtitle 'and p values, without the confusion'.", 1.0)

# ───────────── 2. WELCOME ─────────────
c = "Welcome"
seg(c, "Welcome to Math Lab TV. Where math is something you can see.",
    "Logo (violet rounded square with a green bell curve) + MATH LAB TV + tagline 'where math is something you can see'.", 0.7)
seg(c, "Today you will learn how to test a claim, by asking what boring old chance would usually do.",
    "Small logo top-right. Big ① (blue); mini bar chart of fair-coin results; caption 'test a claim against chance'.")
seg(c, "You will see exactly what a p value measures, as an area you can point at.",
    "Big ② (aqua); the mini chart's right tail fills aqua; caption 'the p value is an area'.")
seg(c, "And you will see the two ways a test can be wrong, and the traps that fool even scientists.",
    "Big ③ (red); two small warning cards 'false alarm' and 'missed it'; caption 'two ways to be wrong'.", 0.6)

# ───────────── 3. WHY IT MATTERS (pays off the Bayes teaser) ─────────────
c = "Why It Matters"
seg(c, "In our Bayes video, we left you with a puzzle.",
    "Chip 'from: Bayes' Theorem' slides in; the old teaser card reappears: 'p = 0.03'.")
seg(c, "If you missed it, you'll find it in the card at the top of this video.",
    "A YouTube-style 'i' card cue animates into the top-right corner with a thumbnail tile 'Bayes' Theorem'; an arrow points to it.", sid="s015a")
seg(c, "Scientists often report a p value, like zero point zero three, and it gets described as a three percent chance that the result is a fluke.",
    "Speech bubble beside the card: 'a 3% chance it's a fluke?' with a red question mark.")
seg(c, "We said that description flips the question. Today, we'll see what a p value really measures, and you'll see the flip with your own eyes.",
    "The bubble flips over like a card, showing two arrows pointing opposite ways.", 1.0)
seg(c, "And this matters, because p values are everywhere.",
    "Three cards slide in, empty.")
seg(c, "A new medicine is tested against a sugar pill. A website tries a new button colour. A trader checks if a strategy beats luck.",
    "Cards fill: pill vs sugar pill; two buttons A / B; a price line with a question mark.")
seg(c, "Every one of them asks the same thing as you and your friend. Is this a real effect, or just chance?",
    "All three cards tilt toward one shared question card: 'real effect, or just chance?'.", 1.0)

# ───────────── 4. THE BORING EXPLANATION ─────────────
c = "The Boring Explanation"
seg(c, "Hypothesis testing starts in a strange place. Not with what you suspect, but with the most boring explanation there is.",
    "Two boxes: an exciting orange box 'something is going on' and a plain blue box 'nothing is going on'; camera moves to the blue one.")
seg(c, "For our coin, the boring explanation is simple. The coin is fair. Heads and tails are equally likely, and fifteen heads was just luck.",
    "Blue card 'the coin is fair: heads 1/2, tails 1/2'; a fair balance beam sits level under it.")
seg(c, "This boring explanation has a name. It's called the null hypothesis. Null just means nothing. Nothing special is going on.",
    "Label 'NULL HYPOTHESIS' writes over the blue card; a definition card: 'null = nothing special is going on'.")
seg(c, "Your suspicion, that the coin favours heads, is called the alternative hypothesis.",
    "Orange card 'ALTERNATIVE: the coin favours heads'.")
seg(c, "Here's the key idea. We don't try to prove the alternative directly. Instead, we pretend the boring explanation is true, and ask how surprising our result would be.",
    "Arrow from the blue card to a thought bubble 'if the coin were fair… how surprising is 15?'.", 1.0)
seg(c, "It's just like a courtroom. The defendant is presumed innocent. The prosecution has to show the evidence would be very hard to explain if they were innocent.",
    "Courtroom line art: a judge's bench; 'presumed innocent' (blue) on one side, 'evidence' (warn) on the other.")
seg(c, "The null hypothesis is the innocent defendant. And our fifteen heads is the evidence.",
    "Labels map over: 'innocent = fair coin' (blue), 'evidence = 15 heads' (warn).", 1.0)

# ───────────── 5. A THOUSAND FAIR COINS (the null distribution and the tail area) ─────────────
c = "A Thousand Fair Coins"
seg(c, "So, if the coin really is fair, what would twenty flips usually look like?",
    "A single fair blue coin flips twenty times quickly; a counter ends at '11 heads' (illustration of one run).")
seg(c, "Let's find out with a thought experiment. Imagine a thousand friends, each with a perfectly fair coin, each flipping it twenty times.",
    "A 40 × 25 grid of small blue coin dots appears on equal-scale axes: '1,000 friends, each flips a fair coin 20 times'.")
seg(c, "Each friend counts their heads. Then we stack them up by how many heads they got.",
    "The dots fly from the grid into columns over an x-axis 'number of heads' 0–20 (ticks every 1, labels every 5); y-axis 'friends' 0–200, ticks every 50.")
seg(c, "This picture has a name. It's called a distribution. It just shows every possible result, and how often each one happens.",
    "Definition card: 'distribution = every result + how often it happens'.")
seg(c, "Look at the shape. Most friends land near ten heads, the middle. About one hundred and seventy six of them get exactly ten.",
    "The 10-heads column glows; label '≈ 176 friends' on top.")
seg(c, "Results further from ten get rarer and rarer, on both sides.",
    "Arrows run down both slopes; outer bars fade to nearly zero.")
seg(c, "In our standard deviation video, we learned to measure spread.",
    "Chip 'from: Standard Deviation'; the card cue appears top-right with a 'Standard Deviation' tile.")
seg(c, "That one is in the card at the top too.",
    "The card cue pulses; arrow to the top-right corner.", sid="s034a")
seg(c, "Here, the typical spread is about two heads either side of ten.",
    "A bracket from 8 to 12 labelled 'typical spread ≈ 2.2 heads'.", sid="s034b")
seg(c, "So, where does your friend's fifteen land?",
    "The warn pin from the hook drops onto 15 on the x-axis.", 0.8)
seg(c, "Way out here. More than two spreads from the middle. Only about fifteen of the thousand fair coins got exactly fifteen heads.",
    "Camera zooms to the right tail; the 15 bar glows warn; label '≈ 15 friends'; brackets show two spreads from 10.")
seg(c, "But we don't just ask about exactly fifteen. We ask: how many fair coins did at least this well? Fifteen heads, or sixteen, or seventeen, all the way to twenty.",
    "Bars 15 through 20 outline one by one, counting up.")
seg(c, "Let's fill in that tail.",
    "The tail area from 15 to 20 fills aqua, bar by bar.", 0.8)
seg(c, "About twenty one friends out of a thousand. That's roughly two in a hundred.",
    "Counter '≈ 21 of 1,000' in aqua; then '≈ 2 in 100'.", 1.0)
seg(c, "And that is the p value. Zero point zero two one.",
    "Big aqua 'p ≈ 0.021' appears beside the tail; the filled tail pulses.", 1.5)
seg(c, "In plain words: if the coin were fair, a result this extreme or more would happen only about two times in a hundred.",
    "Sentence card, colour-coded: 'IF the coin were fair (blue), a result THIS EXTREME OR MORE (warn) happens ≈ 2 times in 100 (aqua)'.", 1.0)
seg(c, "We don't actually need a thousand friends. There are about a million different ways twenty flips can come out, all equally likely for a fair coin.",
    "Card '2²⁰ = 1,048,576 possible sequences'.")
seg(c, "Exactly twenty one thousand seven hundred of them have fifteen heads or more. Divide, and you get the same zero point zero two one.",
    "Formula: p = 21,700 ÷ 1,048,576 ≈ 0.021, the 0.021 in aqua.")
seg(c, "Let's give it symbols. People write p equals the probability of data at least this extreme, given that the null hypothesis is true.",
    "LaTeX: p = P( data this extreme or more | H₀ ), parts colour-coded.")
seg(c, "The capital P means probability. H zero is the null hypothesis. And the straight line means given, or assuming.",
    "Symbol definitions appear under each part: 'P = probability', 'H₀ = null hypothesis (fair coin)', '| = given / assuming'.")
seg(c, "Remember that straight line. It's going to matter a lot.",
    "The '|' glows warn and a small chip 'assuming the coin is fair' hangs from it.", 1.0)
seg(c, "One honest detail. We only counted the heads side, because your suspicion was about heads. If you'd suspected the coin was off in either direction, you'd count both tails, and the p value would double to about zero point zero four.",
    "Left tail 0–5 also fills (lighter aqua) for a moment; label 'two-sided: p ≈ 0.041'; then it clears.")

# ───────────── 6. DRAWING THE LINE (significance level) ─────────────
c = "Drawing the Line"
seg(c, "So, two in a hundred. Is that rare enough to call the coin rigged?",
    "The chart returns; 'p ≈ 0.021' and a question mark.")
seg(c, "To decide, people choose a cut off before they look at the data. It's called the significance level, and it's written with the Greek letter alpha.",
    "A violet vertical line slides along the x-axis; label 'significance level α (alpha)'.")
seg(c, "The most common choice is zero point zero five. One in twenty.",
    "Chip 'α = 0.05 = 1 in 20'.")
seg(c, "The rule is: if the p value is smaller than alpha, we say the result is statistically significant, and we reject the boring explanation.",
    "Rule card: 'p < α → reject the null' with p (aqua) and α (violet).")
seg(c, "Our p value is zero point zero two one. That's below zero point zero five. So at this line, we'd reject the idea that the coin is fair.",
    "Meter 0–0.10 with the violet line at 0.05 and an aqua marker at 0.021 left of it; stamp 'reject the null'.", 1.0)
seg(c, "But here's something most people never hear. That line is not a law of nature. Somebody chose it.",
    "The violet line wobbles; label 'a choice, not a law'.")
seg(c, "The statistician Ronald Fisher suggested one in twenty about a hundred years ago, as a convenient rule of thumb. It stuck.",
    "Card 'one in twenty: a 1920s rule of thumb' (no portrait).")
seg(c, "Other fields draw the line in very different places. Particle physicists want something like one in three and a half million before they announce a discovery.",
    "Line-up of thresholds on a log meter: 'common: 1 in 20', 'stricter: 1 in 200', 'particle physics: ≈ 1 in 3.5 million'.")
seg(c, "And watch what the line does to our coin. Fifteen heads gives a p value of zero point zero two one. Significant.",
    "Chart: tail from 15 filled aqua; p ≈ 0.021 left of the violet α line on the meter; tick ✓.")
seg(c, "Fourteen heads gives about zero point zero five eight. Not significant.",
    "Tail from 14 fills; p ≈ 0.058 lands right of the line; label 'not significant'.")
seg(c, "One coin flip apart. The evidence barely changed, but the verdict flipped completely.",
    "Side by side: '14 heads · p ≈ 0.058' vs '15 heads · p ≈ 0.021', with a tiny gap between them.", 1.5)
seg(c, "So treat significant and not significant as a rough sign, not a magic switch. Always look at the p value itself, and at the size of the effect.",
    "The switch icon fades; a dial 0–0.10 replaces it.", 1.0)

# ───────────── 7. WHAT A P VALUE IS NOT ─────────────
c = "What p Is Not"
seg(c, "Now that we know what a p value is, let's be very clear about three things it is not.",
    "Three red cards face down, numbered 1, 2, 3.")
seg(c, "Number one. It is not the chance that the coin is fair.",
    "Card 1 flips: 'NOT the chance the null is true'.")
seg(c, "A p value of zero point zero two one does not mean a two percent chance the coin is fair, or a two percent chance it was a fluke.",
    "'2% chance it's a fluke' appears and gets crossed out in red.")
seg(c, "Remember the straight line. The p value assumes the coin is fair, then asks about the data. It does not ask about the coin.",
    "Two LaTeX lines: 'P(data | fair)' ✓ (aqua) above 'P(fair | data)' ✗ (red); arrows show they point opposite ways.")
seg(c, "This is the same flip we saw with Bayes. The chance a sick person tests positive is not the chance a positive person is sick. And the chance of this data from a fair coin is not the chance the coin is fair.",
    "Chip 'from: Bayes' Theorem'; the old pair 'P(positive | sick) ≠ P(sick | positive)' slides in above the new pair.", 1.5)
seg(c, "Number two. It is not a measure of how big the effect is.",
    "Card 2 flips: 'NOT how big the effect is'.")
seg(c, "A tiny p value does not mean the coin is very rigged. We'll see why in a moment.",
    "A small ruler icon with a question mark.")
seg(c, "Number three. A big p value does not prove the boring explanation.",
    "Card 3 flips: 'NOT proof of nothing'.")
seg(c, "Suppose you flip a coin only five times, and get four heads. The p value is large. That doesn't show the coin is fair. It just shows five flips can't tell you much.",
    "Mini chart for 5 flips with a wide tail; caption 'not enough data ≠ no effect'.", 1.0)
seg(c, "In a courtroom, not guilty doesn't mean innocent. It means there wasn't enough evidence.",
    "Gavel with 'not guilty' and a smaller line 'not proven innocent'.", 1.0)

# ───────────── 8. TWO WAYS TO BE WRONG (type I and type II errors) ─────────────
c = "Two Ways to Be Wrong"
seg(c, "Any test that makes a yes or no decision can be wrong in two different ways.",
    "A 2 × 2 table on axes: columns 'coin really fair' (blue) / 'coin really rigged' (orange); rows 'we say rigged' / 'we say fair'.")
seg(c, "The first way: the coin is fair, but we call it rigged anyway. That's a false alarm. Statisticians call it a type one error.",
    "Top-left cell turns red: 'TYPE I · false alarm'. Icon: innocent person behind bars.")
seg(c, "In the courtroom, that's convicting an innocent person.",
    "Courtroom icon in the cell.")
seg(c, "The second way: the coin really is rigged, but we say it's fair. That's a miss. It's called a type two error.",
    "Bottom-right cell turns red: 'TYPE II · miss'. Icon: a guilty person walking free.")
seg(c, "In the courtroom, that's letting a guilty person walk free.",
    "Courtroom icon in the cell; the two correct cells turn green-grey 'correct'.", 1.0)
seg(c, "Here's what alpha really controls. With our rule, call it rigged at fifteen heads or more, a fair coin gets falsely accused only about two times in a hundred.",
    "Fair-coin chart (blue) with the aqua tail ≥15 labelled 'false alarm rate ≈ 2.1%'.")
seg(c, "Notice that it's two in a hundred, not five. Twenty flips can only give whole numbers of heads, so the line can't sit exactly at one in twenty. It lands on the nearest safe step.",
    "Staircase of tail areas: ≥14 → 5.8% (above the α line), ≥15 → 2.1% (below); arrow 'nearest safe step'.", sid="s075a")
seg(c, "But what about misses? Suppose the coin really is rigged, and lands heads seventy percent of the time.",
    "A second distribution (orange) for a 70%-heads coin slides in above the blue one, centred at 14 (illustration: a 70% coin).")
seg(c, "Then fifteen heads or more happens only about forty two percent of the time. So more than half the time, our test would miss it.",
    "The orange bars from 15 up fill (≈ 42% 'caught'); bars below 15 hatch red '≈ 58% missed'.", 1.5)
seg(c, "Twenty flips just isn't much evidence. Both pictures overlap a lot.",
    "Camera pulls back to show the two distributions overlapping heavily.")
seg(c, "Now flip a hundred times instead. The two pictures pull apart. With a cut off at fifty nine heads, a fair coin is still falsely accused under five times in a hundred.",
    "Both distributions redraw for 100 flips (x-axis 30–90, ticks every 10): blue centred at 50, orange at 70; violet line at 59.")
seg(c, "And the rigged coin gets caught about ninety nine times in a hundred.",
    "The orange area right of 59 fills: 'caught ≈ 99%'.", 1.5)
seg(c, "That's the trade off. A stricter line means fewer false alarms but more misses. And the main way to cut both at once is more data.",
    "A seesaw: 'false alarms' vs 'misses'; a block labelled 'more data' lifts both sides down.", 1.0)

# ───────────── 9. TINY P, TINY EFFECT ─────────────
c = "Tiny p, Tiny Effect"
seg(c, "Now let's come back to that second thing a p value is not. A measure of size.",
    "Card 2 from 'What p Is Not' returns: 'NOT how big the effect is'.")
seg(c, "Imagine a different coin. It's almost fair. It lands heads fifty point two percent of the time. Just a hair more than half.",
    "A coin with a microscopic weight; a bar '50.2% heads' next to '50% fair', nearly the same length.")
seg(c, "Over twenty flips, you'd never notice. But suppose a machine flips it a million times, and gets five hundred and two thousand heads.",
    "A counter spins to '1,000,000 flips · 502,000 heads'.")
seg(c, "For a fair coin, the spread over a million flips is about five hundred heads. Two thousand extra heads is four spreads from the middle.",
    "Fair-coin bell (blue) for a million flips, x-axis 498,000–502,000 ticks every 1,000; brackets of 500 each; warn pin at 502,000.")
seg(c, "The p value is about zero point zero zero zero zero three. Three in a hundred thousand. Incredibly significant.",
    "Tiny aqua tail; 'p ≈ 0.00003' in big aqua; stamp 'highly significant'.", 1.0)
seg(c, "But does it matter? If this coin decided your coffee, you'd pay for about two extra coffees in every thousand.",
    "Your share of 1,000 coffees: 502 (this coin) vs 500 (a fair coin), almost identical; caption '≈ 2 extra coffees per 1,000 flips'.", 1.5)
seg(c, "And it works the other way too. A big effect can hide behind a big p value, when there's only a little data. That was our seventy percent coin, missed more than half the time in twenty flips.",
    "The 20-flip overlap picture returns small, beside the million-flip picture: 'big effect, little data' vs 'tiny effect, huge data'.", 1.0, sid="s087a")
seg(c, "So the p value tells you whether an effect is probably there. It does not tell you whether it's big enough to care about.",
    "Two dials: 'is it there?' (aqua, p value) and 'how big is it?' (orange, effect size).")
seg(c, "With enough data, almost any tiny difference becomes significant. That's why good reports show both the p value and the size of the effect.",
    "Checklist card: '✓ p value  ✓ effect size'.", 1.0)

# ───────────── 10. REAL WORLD ─────────────
c = "Real World"
seg(c, "So where will you actually meet this?",
    "Four tiles: Machine Learning, Data Science, Finance, Computer Science.")
seg(c, "In data science, the classic one is an A B test. Half the visitors see the old button, half see the new one.",
    "Data Science tile expands: two buttons A and B, each with a visitor counter.")
seg(c, "The null hypothesis is that the button makes no difference. If the new one gets more clicks, the p value asks: how often would a gap this big appear by chance alone?",
    "Blue 'no difference' card; a small null distribution of 'gap between A and B' with the observed gap in its tail (illustration).")
seg(c, "In machine learning, you compare two models on the same test set. One scores a little higher. Is it really better, or did it just get a luckier set of examples?",
    "Machine Learning tile: two model cards 'accuracy 91.2%' vs '91.6%'; a coin-flip icon between them.")
seg(c, "A hypothesis test, or a simple shuffle test, tells you whether that gap is bigger than chance usually makes.",
    "Labels shuffle between the two models several times; a little distribution of shuffled gaps builds.")
seg(c, "And when you fit a linear regression, every input gets its own p value. It asks: if this input truly had no effect, how surprising would the slope we found be?",
    "Mini regression table (illustration): rows 'size', 'age', 'colour' with slope and p columns; the p column glows aqua.", sid="s094a")
seg(c, "In finance, a trader backtests a strategy and it beats the market. But markets are noisy. The null hypothesis is that the strategy has no real edge, and the profit was luck.",
    "Finance tile: a jagged price line with a profit arrow; blue card 'no real edge'.")
seg(c, "And try enough strategies, and some will look brilliant by pure luck. We'll come back to that in a moment.",
    "Twenty little price lines; one glows gold; a red question mark beside it.")
seg(c, "In computer science, engineers test whether new code is really faster. Timing a program is noisy, just like a coin. So they run it many times, and test whether the speed up is more than noise.",
    "CS tile: two run-time strips 'old code' vs 'new code' with scattered timing dots; a bracket 'speed-up or noise?'.", 1.0)
seg(c, "Different worlds, same question as your coffee. Real effect, or just chance?",
    "All four tiles shrink around the coffee coin in the centre.", 1.0)

# ───────────── 11. COMMON MISTAKES ─────────────
c = "Common Mistakes"
seg(c, "Let's finish with the most common mistakes, because they trip up beginners and experts alike.",
    "Three red mistake cards slide in, face down.")
seg(c, "Mistake one: reading the p value as the chance the boring explanation is true.",
    "Card 1 flips: 'p = chance the coin is fair?' (red).")
seg(c, "Here's how far apart those two numbers can be. Suppose that in your town, only one coin in a hundred is rigged, and a rigged one lands heads seventy percent of the time.",
    "Illustration: a grid of 100 coins on equal-scale axes, 1 orange (rigged) and 99 blue (fair); chip 'illustration'.")
seg(c, "Then, just like in our Bayes theorem video, which is linked in the card above, we count. Among all the coins that would give fifteen heads or more, about eighty three percent are still fair coins. Only about seventeen percent are rigged.",
    "Bayes-style split: of the coins that reach ≥15 heads, the blue block (fair) is far larger than the orange block (rigged); labels '≈ 83% fair' (blue) and '≈ 17% rigged' (orange).")
seg(c, "The p value was two percent. But the chance the coin is rigged is only about one in six. Same evidence, very different numbers.",
    "Side by side: 'p ≈ 0.021' (aqua) vs 'chance rigged ≈ 17%' (violet), with '≠' between them.", 1.5)
seg(c, "Mistake two: running lots of tests, and only reporting the one that worked.",
    "Card 2 flips: 'testing many things, reporting one' (red).")
seg(c, "If you test twenty things that have no real effect, each at one in twenty, the chance that at least one looks significant is about sixty four percent.",
    "Twenty fair-coin mini charts in a 5 × 4 grid; one by chance lands in its tail and glows; counter 'chance of ≥ 1 false alarm ≈ 64%'.")
seg(c, "This has a name. It's called p hacking: trying analysis after analysis until something crosses the line.",
    "Chip 'p-hacking' stamps on in red over the grid of twenty charts.", sid="s105a")
seg(c, "That's how a lucky trading strategy, or a surprising headline, can come from pure noise. If you test many things, you need a stricter line.",
    "The glowing chart is stamped 'lucky, not real'; the violet line moves further right.", 1.0)
seg(c, "Mistake three: treating not significant as proof there's no effect.",
    "Card 3 flips: 'not significant = no effect?' (red).")
seg(c, "Remember the seventy percent coin. With twenty flips, we missed it more than half the time. Not significant often just means not enough data.",
    "The overlapping 20-flip pictures return; the '≈ 58% missed' area highlights.", 1.0)
seg(c, "And a bonus mistake: choosing the line after you've seen the data. If you move alpha until your result is significant, the p value stops meaning anything.",
    "The violet line slides right to sneak past a p value; a red 'no!' stamp. Caption 'choose α before you look'.", 1.0)

# ───────────── 12. RECIPE ─────────────
c = "Recipe"
seg(c, "Let's turn all of that into a recipe you can use for any claim.",
    "Recipe card frame unrolls: 'Hypothesis testing in five steps'.")
seg(c, "Step one: state the boring explanation. That's the null hypothesis. Nothing special is going on.",
    "Item 1 (blue): 'State the null' + 'the boring explanation'.")
seg(c, "Step two: choose your line, before you look. Alpha, usually one in twenty.",
    "Item 2 (violet): 'Choose α first' + 'usually 0.05'.")
seg(c, "Step three: picture what chance alone would do. Draw the distribution, assuming the null is true.",
    "Item 3: 'Picture chance' + 'the distribution if the null is true'.")
seg(c, "Step four: find the tail. The p value is the share of that picture at least as extreme as your result.",
    "Item 4 (aqua): 'Find the tail area' + 'p = share at least this extreme'.")
seg(c, "Step five: decide, and then ask how big. Compare p to alpha, and always report the size of the effect too.",
    "Item 5 (orange): 'Decide, then size it' + 'p vs α, plus effect size'.", 1.5)
seg(c, "For the coffee coin: fair coin as the null. Fifteen heads out of twenty. A p value of about two in a hundred. Below one in twenty, so we'd call it suspicious, and keep flipping to be sure.",
    "Summary strip: 'H₀ fair · 15 of 20 heads · p ≈ 0.021 < 0.05 → suspicious, collect more data'.", 1.0)
seg(c, "A p value doesn't tell you what's true. It tells you how surprised chance would be.",
    "Closing line types on in aqua, centred.", 2.0)

# ───────────── 13. SUBSCRIBE ─────────────
c = "Subscribe"
seg(c, "Look around your world, and notice how often a lucky streak gets mistaken for a pattern.",
    "Four everyday cards: a sports winning streak, a 'hot' slot machine, a stock that doubled, a lucky shirt; each stamped 'real, or chance?'.", 0.6)
seg(c, "If this lesson made things clear for you, please subscribe to Math Lab TV, so we can keep building together.",
    "Logo + red SUBSCRIBE button; a cursor clicks it; it turns grey 'SUBSCRIBED ✓'; 'so we can keep building together' appears.", 0.8)

# ───────────── 14. NEXT TIME ─────────────
c = "Next Time"
seg(c, "But here's a puzzle for next time.",
    "Small logo top-centre; a puzzle-piece icon draws on.")
seg(c, "In a courtroom, an expert says there's only a one in a million chance that an innocent person would match the evidence.",
    "Courtroom line art; a card 'chance an innocent person matches: 1 in 1,000,000'.")
seg(c, "So the jury thinks there's a one in a million chance the defendant is innocent. Real cases have gone exactly this way.",
    "Speech bubble 'so 1 in a million they're innocent?' with a red question mark.")
seg(c, "It's the very same flip we saw today. Next time, we'll see why it's called the prosecutor's fallacy, and why smart people fall for it.",
    "The 'P(data | innocent)' vs 'P(innocent | data)' pair flips; chip 'next: the prosecutor's fallacy' under the logo.")
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
    md = [f"# Hypothesis Testing and p Values Without the Confusion\n",
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
    for k, v in cw.items():
        print(f"  {k:24s} {v:4d} words ~{v / 165 * 60:5.0f} s")
