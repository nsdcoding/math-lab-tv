#!/usr/bin/env python3
"""Source of truth for the narration. Run to emit script.json + script.md.

Running example (used everywhere; every number checked in verify_numbers.py):
  A city of 8,000,000 people. A crime; a partial DNA trace at the scene. Sam (fictional) matches.
  The expert: a random INNOCENT person matches with chance 1 in 1,000,000 = P(match | innocent).
  The prosecutor's swap: "so a 1 in a million chance Sam is innocent" = P(innocent | match). Wrong.
  Count the crowd (assume: culprit is someone in the city, everyone equally likely before other evidence,
  the culprit always matches): 7,999,999 innocent people x 1/1,000,000 ~ 8 innocent matches, + 1 culprit = 9.
  P(guilty | match) = 1,000,000 / 8,999,999 ~ 1 in 9;  P(innocent | match) ~ 8 in 9 (~89 %),
  ~889,000 times bigger than 1 in a million. Each block of a million people holds ~1 innocent match.
  Base rate: village of 1,000 -> ~0.001 innocent matches -> ~999 in 1,000 guilty; country of 60 million ->
  ~60 innocent matches -> ~1 in 61.
  Callbacks: Bayes screening (P(positive | healthy) = 1 in 10 vs P(healthy | positive) = 99/108 = 11 in 12);
  coffee coin (p = 21,700/1,048,576 ~ 0.021 = P(this extreme | fair); with 1 in 100 coins rigged at 70 %
  heads, P(fair | 15+ heads) ~ 83 %).
  Real case (England, 1999): 1 in 8,543 squared = 72,982,849 ~ "1 in 73 million"; conviction overturned 2003.
  ML: face matching, 50,000 fans, false match 1 in 10,000 -> ~5 false + 1 real -> ~1 alert in 6.
  Finance: 1,000,000 honest payments + 100 frauds; catches 90; false flags 1 in 1,000 = 1,000 -> 90/1,090 ~ 1 in 12.
  CS: database of 5,000,000 profiles x 1 in a million -> ~5 innocent hits.

Colour roles (one per concept, kept for the whole video):
  innocent people / "given innocent"  = blue       the evidence / match         = warn
  guilty / the culprit                = orange     the answer we want (P(guilty | match)) = violet
  the crowd / base rate (areas)       = aqua       the swap / mistakes          = red

Connections (from `python3 channel/channel.py refs prosecutors-fallacy`):
  Pays off: hypothesis-testing teaser ("one in a million chance an innocent person would match... jury thinks
  one in a million chance innocent... the very same flip we saw today").
  Callbacks: hypothesis-testing (p-value = P(data | fair), coffee coin), bayes-examples (1 in 12 screening).
  Overlaps: none. Prerequisites not made: none.
  Teaser: confusion-matrix (precision vs recall is this same swap); catalog default was linear-regression.
"""
import json, pathlib, sys

SLUG = "prosecutors-fallacy"  # id in channel/catalog.json
TARGET_MIN = (15, 20)         # words ≈ minutes × 150 (voice ~165 wpm + pauses)
D = 0.35                      # default pause between segments
S = []
N = [0]   # auto-id counter; once voiced, insert new lines with explicit ids (e.g. s017a) so old clips stay cached


def seg(chapter, text, visual, pause=D, sid=None):
    if sid is None:
        N[0] += 1; sid = f"s{N[0]:03d}"
    S.append(dict(id=sid, chapter=chapter, text=text, visual=visual, pause_after=pause))


# ───────────── 1. HOOK ─────────────
c = "One in a Million"
seg(c, "Last time, I left you with a puzzle from a courtroom. Today, we solve it.",
    "Small chip 'from: Hypothesis Testing' slides in; a courtroom line-art frame draws on.")
seg(c, "Picture a city of eight million people. One night, a crime. At the scene, police find a tiny trace of DNA.",
    "Skyline; counter '8,000,000 people' ticks up; a magnifier over a small warn-coloured DNA icon at the scene.")
seg(c, "It's only a partial trace, so it can't point to one person. But it's still rare.",
    "The DNA icon is half-filled; label 'partial trace'.")
seg(c, "Weeks later, police find a man. Let's call him Sam. Sam's DNA matches the trace.",
    "STICKER: Sam, a worried man in a plain jacket (illustration). A warn 'MATCH ✓' stamp next to him.")
seg(c, "In court, an expert explains: if you picked an innocent person at random, the chance they would match is just one in a million.",
    "STICKER courtroom: an expert at the witness stand (illustration). Card: 'innocent person matches: 1 in 1,000,000'.")
seg(c, "Then the prosecutor stands up and says: so there's only a one in a million chance that Sam is innocent.",
    "Second card appears beside the first: 'Sam is innocent: 1 in 1,000,000?' with a red question mark.", 0.8)
seg(c, "The jury nods. One in a million sounds like proof.",
    "Twelve small juror icons nod in turn; a gavel icon hovers.")
seg(c, "Take a second, and decide. Do you agree with the prosecutor?",
    "Slider between 'agree' and 'disagree' with a blinking cursor; small clock ticks.", 1.5)
seg(c, "If you said yes, you're in good company. Judges, juries and even experts have made this exact mistake.",
    "Three icons (gavel, jury box, lab coat) each get a red tick 'fell for it'.")
seg(c, "By the end of this video, you'll see that Sam is much more likely innocent than guilty. And you'll be able to spot this trap anywhere.",
    "Big reveal teaser: 'innocent: about 8 in 9' blurred out with a lock icon; 'you'll see why' chip.")
seg(c, "It's called the prosecutor's fallacy.",
    "Title card: 'The Prosecutor's Fallacy' with subtitle 'the statistics trap smart people fall for'.", 1.0)

# ───────────── 2. WELCOME ─────────────
c = "Welcome"
seg(c, "Welcome to Math Lab TV. Where math is something you can see.",
    "Logo (violet rounded square with a green bell curve) + MATH LAB TV + tagline 'where math is something you can see'.", 0.7)
seg(c, "Today you will learn why the chance of the evidence, if someone is innocent, is not the chance they are innocent.",
    "Big ① + mini visual: two boxes 'P(match | innocent)' and 'P(innocent | match)' with a red ≠; caption 'two different questions'.")
seg(c, "You will see how to count the crowd, and find how many innocent people share the same evidence.",
    "Big ② + mini population square with a few warn dots; caption 'count the crowd'.")
seg(c, "And you will learn a simple recipe to catch this swap in courtrooms, medical tests, and the news.",
    "Big ③ + mini checklist icon; caption 'catch the swap anywhere'.", 0.6)

# ───────────── 3. WHY IT MATTERS: THE FLIP ─────────────
c = "Two Different Questions"
seg(c, "In our hypothesis testing video, we flipped a friend's coin twenty times, and got fifteen heads.",
    "Chip 'from: Hypothesis Testing'. Mini tally of 15 orange H and 5 blue T dots on a flip axis.")
seg(c, "We found that a fair coin would do something that extreme only about two times in a hundred.",
    "The coin's tail-area picture: bars 0–20 heads, tail ≥ 15 shaded aqua, label 'p ≈ 0.021'.")
seg(c, "And we warned: that is not the chance the coin is fair. The question had been flipped.",
    "Two cards: 'chance of this result, if the coin is fair' and 'chance the coin is fair, given this result'; red ≠ between them.", 0.8)
seg(c, "The courtroom is the very same flip. So let's write it down carefully.",
    "Coin cards slide away; the two courtroom cards from the hook slide in.")
seg(c, "Mathematicians write the chance of something with a capital P. And they use a short vertical bar, which you can read as the word given.",
    "Symbol definition card: 'P( … ) = the chance of …', '|  = given (we already know this part)'.")
seg(c, "So P of match, given innocent, means: suppose the person is innocent. How likely is a match?",
    "Box 1 (blue border): 'P(match | innocent)'. Under it: 'start with innocent people → how many match?' Value '1 in 1,000,000'.")
seg(c, "That's the number the expert gave. One in a million.",
    "Value in box 1 pulses warn: '1 in 1,000,000'.", 0.6)
seg(c, "But the jury needs a different number. P of innocent, given match. Suppose the person matches. How likely are they innocent?",
    "Box 2 (violet border): 'P(innocent | match)'. Under it: 'start with people who match → how many are innocent?' Value '?'.")
seg(c, "Look at the two boxes. Same words. Just swapped around the bar.",
    "Animation: 'match' and 'innocent' inside box 1 physically swap places, morphing into box 2. Red arrows show the swap.", 1.0)
seg(c, "The prosecutor took the first number, and read it out as the second. That swap is the whole fallacy.",
    "Box 1's value '1 in 1,000,000' flies into box 2; a red stamp 'THE SWAP' lands over it.", 1.2)
seg(c, "So what should the expert have said? Something like this: if Sam were innocent, a match would be very unlikely.",
    "Green ✓ card: 'If Sam were innocent, a match would be very unlikely.'", sid="s025a")
seg(c, "That sentence is true. But it does not tell you how likely Sam is to be innocent. To get that, you need one more ingredient.",
    "Under it, a violet card 'How likely is Sam innocent?' with a missing-puzzle-piece icon labelled '?'.", 0.8, sid="s025b")

c = "Why the Swap Matters"
seg(c, "Is swapping really such a big deal? Let's try it on something simple.",
    "Clean slate; two empty boxes return.")
seg(c, "What's the chance that a dog has four legs? Almost certain. Nearly every dog does.",
    "Box: 'P(four legs | dog)' with a dog silhouette; meter fills almost to 1; label 'almost certain'.")
seg(c, "Now swap it. What's the chance that something with four legs is a dog?",
    "Box: 'P(dog | four legs)'. A crowd of four-legged silhouettes appears: cats, cows, horses, chairs, tables, a few dogs.")
seg(c, "Not very likely at all. Cats have four legs. So do cows, and horses. Even your kitchen table.",
    "Dogs highlighted orange among many grey four-legged things; meter for box 2 stays low.", 1.0)
seg(c, "The two numbers share the same words, but they can be wildly different.",
    "Both meters side by side: tall vs short; caption 'same words, different questions'.")
seg(c, "The difference comes from the crowd. How many other things, besides dogs, also have four legs?",
    "The non-dog four-legged crowd glows aqua; label 'everything else that fits'.", 1.0)
seg(c, "So why do smart people swap them? Because our brains love a simple story. The evidence fits the guilty person, so the guilty person must fit the evidence.",
    "Two arrows between 'guilty' and 'match': the forward arrow solid ('guilty → match: yes'), the backward arrow dashed red ('match → guilty: not so fast').")
seg(c, "But fitting the evidence is easy when the crowd is big. Lots of innocent people can fit it too.",
    "The dashed arrow fans out to many blue dots, each with a warn ring.", 0.8)
seg(c, "In Sam's case, the crowd is a city of eight million people. So let's count it.",
    "Transition: the four-legged crowd morphs into a grid of tiny people dots labelled '8,000,000 people'.")

# ───────────── 4. BUILD + RUNNING EXAMPLE: COUNT THE CROWD ─────────────
c = "Count the Crowd"
seg(c, "Before we start, let's be honest about what we are assuming.",
    "Assumptions card slides in, empty.")
seg(c, "First, the person who did it lives somewhere in this city.",
    "Assumption ① 'the culprit is one of the 8,000,000'.")
seg(c, "Second, the real culprit's DNA always matches the trace.",
    "Assumption ② 'the culprit always matches'.")
seg(c, "And third, for now, we know nothing else about Sam. Only the match. We'll come back to that one.",
    "Assumption ③ 'no other evidence (yet)' with a small 'we'll return' tag.", 0.8)
seg(c, "Here is the whole city. Eight million people, drawn as eight big blocks of one million each.",
    "Population square on equal-scale axes: 8 blocks (4 × 2), each labelled '1,000,000'. Axis titles 'people'.")
seg(c, "One of them is the culprit. That leaves seven million, nine hundred and ninety nine thousand, nine hundred and ninety nine innocent people.",
    "One orange dot in a block; the rest of the square tints blue; counter '7,999,999 innocent'.")
seg(c, "Now the expert's number. Each innocent person matches with a chance of one in a million.",
    "Card 'P(match | innocent) = 1 in 1,000,000' docks at the top right.")
seg(c, "So in a block of one million innocent people, how many would we expect to match by pure chance?",
    "Zoom into one block; a scanning line sweeps across it.")
seg(c, "About one.",
    "A single warn dot lights up inside the block; label '≈ 1 innocent match'.", 1.0)
seg(c, "And we have eight of those blocks. So across the whole city, about eight innocent people match the trace. Just by luck.",
    "Camera pulls back; one warn dot lights in each block, counter climbs 1 → 8; label '≈ 8 innocent matches'.", 1.2)
seg(c, "You can check it yourself. Eight million, times one in a million, is eight.",
    "Arithmetic in Inter: '8,000,000 × 1/1,000,000 = 8' (warn result).", 0.8, sid="s042a")
seg(c, "Plus the one real culprit, who matches for sure.",
    "The orange culprit dot gets a warn ring; total counter '8 + 1 = 9 people match'.")
seg(c, "So if police lined up everyone in the city who matches, there would be about nine people in that line.",
    "All 9 matching dots fly out of the square into a line-up on a number axis 1–9: eight blue-filled with warn rings, one orange.", 1.0)
seg(c, "And only one of those nine is guilty.",
    "The orange figure in the line-up glows; the eight others dim slightly.", 1.0)
seg(c, "Sam is one of the people in that line. All we know is that he matched. So the chance he's the guilty one is about one in nine.",
    "Sam's sticker face appears above a random position in the line-up with a '?'; fraction card '1 guilty ÷ 9 matches ≈ 1 in 9' (violet).", 1.2)
seg(c, "Which means the chance he's innocent is about eight in nine. Around eighty nine percent.",
    "Big violet answer card: 'P(innocent | match) ≈ 8 in 9 ≈ 89%'.", 1.5)
seg(c, "Notice what we did. No fancy formula. We just imagined everyone in the city, and asked who else would match.",
    "Mini recap strip: '8,000,000 people' → '× 1 in a million' → '≈ 8 innocent + 1 culprit' → '1 in 9'.")
seg(c, "Put the two numbers next to each other.",
    "The two boxes return side by side.")
seg(c, "The chance of a match, given innocent: one in a million.",
    "Box 1: 'P(match | innocent) = 1 in 1,000,000' (blue).")
seg(c, "The chance of innocent, given a match: about eight in nine.",
    "Box 2: 'P(innocent | match) ≈ 8 in 9' (violet).")
seg(c, "The second number is almost nine hundred thousand times bigger. That's how far apart the two questions are.",
    "A bar on a log-scale axis: tiny bar for 1 in a million, tall bar for 8 in 9; arrow '≈ 889,000×'.", 1.5)

c = "The Formula Behind It"
seg(c, "What we just did is count, but you can write it as a short rule.",
    "Clean slate; heading 'the counting rule'.")
seg(c, "The chance of guilt, given a match, equals the guilty people who match, divided by everyone who matches.",
    "Formula in words: 'P(guilty | match) = guilty matches ÷ all matches'. Numerator orange, denominator warn.")
seg(c, "On top, one. On the bottom, one plus eight. One ninth.",
    "Numbers drop in: '1 ÷ (1 + 8) = 1/9' (LaTeX fraction), violet result.", 0.8)
seg(c, "In our Bayes theorem video, we wrote this same idea as a formula. Here, counting the crowd gets you to the same answer, with no formula to remember.",
    "Chip 'from: Bayes' Theorem'. Small Bayes formula appears, then the 'count the crowd' picture beside it with '=' between.")
seg(c, "And notice where the eight came from. Not from the expert's number alone. It came from the size of the crowd.",
    "The '8' in the denominator is circled aqua; arrow back to '8,000,000 people'.", 1.0)

# ───────────── BASE RATE ─────────────
c = "The Missing Piece"
seg(c, "That crowd size has a name. It's called the base rate. And it's the piece the prosecutor left out.",
    "Heading 'the base rate = how big is the crowd of possible suspects?' (aqua).")
seg(c, "Let's keep the same one in a million trace, and just change the crowd.",
    "A horizontal slider labelled 'crowd size' on a log axis: 1,000 · 1,000,000 · 8,000,000 · 60,000,000.")
seg(c, "Imagine the crime happened in a tiny village of one thousand people, and nobody else could have been there.",
    "Slider moves to 1,000; a small square of 1,000 dots (40 × 25) with one orange culprit.")
seg(c, "Now the chance that even one innocent villager matches is about one in a thousand.",
    "Scan line sweeps; no warn dot lights; label 'innocent matches ≈ 0.001'.")
seg(c, "So if someone in the village matches, they are almost certainly the culprit. About nine hundred and ninety nine times in a thousand.",
    "Line-up axis: just one orange figure; violet card 'P(guilty | match) ≈ 999 in 1,000'.", 1.0)
seg(c, "Back in our city of eight million, the same match gave about one in nine.",
    "Slider moves to 8,000,000; line-up of 9; card '≈ 1 in 9'.")
seg(c, "And if anyone in a whole country of sixty million could have done it, about sixty innocent people would match. The chance of guilt drops to about one in sixty one.",
    "Slider to 60,000,000; line-up axis grows to 61 tiny figures (60 blue with warn rings, 1 orange); card '≈ 1 in 61'.", 1.2)
seg(c, "The evidence never changed. Only the crowd did. And the answer swung from almost certain, to almost certainly not.",
    "Three result cards in a row: '999 in 1,000', '1 in 9', '1 in 61', with the unchanged '1 in a million' chip above all three.", 1.5)
seg(c, "Same trace. Same expert. Same one in a million. Three completely different answers.",
    "The three result cards pulse in turn under the fixed '1 in a million' chip.", 1.0, sid="s066a")
seg(c, "That's why the expert's number, on its own, can never tell you the chance of guilt. You always need the crowd as well.",
    "Equation in words: 'evidence + crowd → answer'; the crowd part glows aqua.")

c = "When Other Evidence Counts"
seg(c, "Now, remember our third assumption. We knew nothing about Sam except the match.",
    "Assumption ③ card returns: 'no other evidence (yet)'.")
seg(c, "In a real case, there's usually more. Maybe Sam was seen near the scene that night.",
    "A second evidence chip 'seen near the scene' slides in next to the DNA chip.")
seg(c, "Other evidence works by shrinking the crowd. Instead of eight million possible people, maybe only a few hundred were nearby.",
    "The 8-block square shrinks to a small cluster of a few hundred dots labelled 'people nearby (illustration)'.")
seg(c, "In a smaller crowd, far fewer innocent people match by luck, and the match becomes much stronger evidence.",
    "Inside the small cluster: almost certainly no innocent warn dots; only the orange culprit matches; violet meter rises toward 'very likely'.", 1.0)
seg(c, "So the match isn't useless. It's one piece, and it has to be combined with everything else, honestly.",
    "Puzzle pieces 'DNA match' + 'seen nearby' + 'other facts' click together.", 0.8)

seg(c, "In fact, here's how much the match moved things. Before it, Sam was just one of eight million people. One in eight million.",
    "Meter on a log axis: 'before the match: 1 in 8,000,000' (orange, tiny).", sid="s073a")
seg(c, "After it, he's one in nine. His chance of guilt jumped almost nine hundred thousand times.",
    "Meter jumps to '1 in 9'; arrow '≈ 889,000× higher'.", 1.0, sid="s073b")
seg(c, "Strong evidence. Just not, on its own, proof.",
    "Label 'strong ≠ proof'.", 0.8, sid="s073c")
# ───────────── A REAL CASE ─────────────
c = "A Real Courtroom"
seg(c, "This isn't just a classroom puzzle. In England, in nineteen ninety nine, a mother was convicted after two of her babies died suddenly.",
    "Plain card 'A real case · England · 1999' (no names, no photos). A calendar icon.")
seg(c, "A medical expert told the jury that, for a family like hers, the chance of one sudden infant death was about one in eight thousand five hundred.",
    "Card: 'one sudden infant death: about 1 in 8,543' (blue).")
seg(c, "He then multiplied that number by itself, and said the chance of two such deaths was about one in seventy three million.",
    "'1 in 8,543 × 1 in 8,543 ≈ 1 in 73,000,000' builds up; red underline on the ×.")
seg(c, "That number had two problems. First, multiplying assumes the two deaths were unrelated. But families can share genes and homes, so a second death is more likely after a first.",
    "Red tag 1 'treated as unrelated (they may not be)': two linked baby-cradle icons with a shared-home outline.")
seg(c, "Second, the swap. One in seventy three million was presented as if it were the chance she was innocent.",
    "Two boxes again: 'P(two deaths | innocent)' vs 'P(innocent | two deaths)'; red 'THE SWAP' stamp.", 1.0)
seg(c, "But a double murder of babies is also extremely rare. The real question is which rare explanation is more likely. Comparing them points the other way.",
    "Balance beam: left pan 'two natural deaths (rare)', right pan 'two murders (even rarer)'; the beam tips toward natural deaths. Label 'shape only'.", 1.0)
seg(c, "Statisticians spoke out, and in two thousand and three, her conviction was overturned.",
    "Card 'conviction overturned · 2003'; a scale-of-justice icon levels out.", 1.5)

# ───────────── SAME SWAP IN MEDICINE ─────────────
c = "The Same Swap in Medicine"
seg(c, "The very same swap happens in doctors' offices, every day.",
    "Clinic icon; the two boxes reappear with new words.")
seg(c, "Back in our Bayes theorem video, a test gave a false alarm to one in ten healthy people.",
    "Chip 'from: Bayes' Theorem'. Box 1: 'P(positive | healthy) = 1 in 10' (blue).")
seg(c, "That's the chance of a positive, given healthy. Swap it, and ask: given a positive, how likely are you healthy?",
    "Box 2: 'P(healthy | positive) = ?' (violet); swap arrows.")
seg(c, "Out of a thousand people, ninety nine healthy people got false alarms, and only nine people who were really sick tested positive.",
    "Recap of that video's picture: 1,000-dot grid; 99 blue dots with warn rings, 9 orange dots with warn rings.")
seg(c, "So eleven out of twelve of the positives were healthy. A world away from one in ten.",
    "Fraction card 'P(healthy | positive) = 99 ÷ 108 = 11 in 12' (violet) next to '1 in 10'.", 1.2)
seg(c, "It's the courtroom again. A rare false alarm, inside a big healthy crowd, still adds up to lots of false alarms.",
    "Side by side: city line-up (8 innocent + 1) and clinic line-up (99 healthy + 9); caption 'big innocent crowd → many false matches'.", 1.0)

# ───────────── REAL WORLD ─────────────
c = "Where You'll Use It"
seg(c, "That's why a single positive result is usually followed by a second, different test. A second test shrinks the crowd, just like extra evidence in court.",
    "Clinic line-up of 108 goes through a second test filter; the crowd shrinks; label 'second test = smaller crowd (illustration)'.", 0.8)
seg(c, "So if you ever get a scary test result, ask the flipped question. Out of everyone who tests positive, how many really have it?",
    "Question card (violet): 'Out of everyone who tests positive, how many really have it?'", 1.0, sid="s084a")
seg(c, "Once you can see this swap, you'll find it everywhere, especially in the world of data.",
    "Four tiles: Machine Learning, Data Science, Finance, Computer Science.")
seg(c, "In machine learning, take a face recognition camera at a stadium, looking for one wanted person among fifty thousand fans.",
    "ML tile expands: stadium crowd of dots (illustration), one orange 'wanted' dot. Chip 'false match: 1 in 10,000'.")
seg(c, "It only wrongly matches one face in ten thousand. Sounds great. But fifty thousand fans means about five false matches, plus the one real person.",
    "Scan across the crowd: about five warn rings on blue dots, one on the orange dot; counter '≈ 5 + 1 = 6 alerts'.")
seg(c, "So when the alarm goes off, it's the right person only about one time in six.",
    "Violet card 'P(right person | alert) ≈ 1 in 6'.", 1.0)
seg(c, "In data science, it's the p value from our coin video. A p value is the chance of results this extreme, given that nothing is going on.",
    "DS tile: the coin tail-area picture, label 'p = P(this extreme | nothing going on) ≈ 0.021'.")
seg(c, "It is not the chance that nothing is going on. If only one coin in a hundred were rigged, that coin would still be fair about eighty three times in a hundred.",
    "Box 'P(fair | 15+ heads) ≈ 83 in 100 (if 1 coin in 100 is rigged · illustration)' (violet) beside '0.021'.", 1.0)
seg(c, "In finance, a bank's fraud model flags card payments. It wrongly flags just one honest payment in a thousand.",
    "Finance tile: card-payment icons stream past; chip 'false flag: 1 in 1,000'.")
seg(c, "But for every million honest payments, there are maybe a hundred frauds. The model catches ninety of those, and also flags a thousand honest ones.",
    "Two stacks on a count axis 0–1,000: 'real fraud caught: 90' (orange), 'honest but flagged: 1,000' (blue with warn ring).")
seg(c, "So only about one flag in twelve is really fraud. The rest are customers whose cards just got blocked.",
    "Violet card 'P(fraud | flagged) = 90 ÷ 1,090 ≈ 1 in 12'.", 1.0)
seg(c, "And in computer science, it's what happens when you search a huge database.",
    "CS tile: a database cylinder icon with rows of profile records.")
seg(c, "Search five million DNA profiles for a one in a million match, and you'd expect about five innocent hits, even if the real culprit isn't in there at all.",
    "Search bar animates through rows; five warn hits pop out, all blue; label 'culprit not in database'.")
seg(c, "The bigger the search, the more coincidences you're guaranteed to find.",
    "Line on axes x: profiles searched (millions, 0–5), y: expected innocent hits (0–5); straight line rising.", 1.0)

seg(c, "Four different fields, one same trap. A rare false match, multiplied by a big crowd, gives you lots of false matches.",
    "The four tiles return in a row, each with its line-up: '1 in 6', '83 in 100 fair', '1 in 12', '5 innocent hits'; caption 'rare × big crowd = many'.", 1.0)

# ───────────── QUIZ ─────────────
c = "Spot the Swap"
seg(c, "Let's practise. I'll read four claims. For each one, decide: is it a swap, or is it fair?",
    "Heading 'spot the swap'; four blank claim cards; a 'swap?' / 'fair?' toggle under each.")
seg(c, "Claim one. A smoke alarm almost always beeps when there's a fire. So when it beeps, there's almost certainly a fire.",
    "Card ①: smoke-alarm icon + flame; text 'beeps | fire: almost always → fire | beeps: almost certain?'.", 1.5)
seg(c, "That's a swap. Think of every single time the alarm beeps. Most of those times, someone just burnt the toast.",
    "Card ① stamped red 'SWAP'; a crowd of beep icons, most next to toast icons, a few next to flames. Label 'illustration'.", 0.8)
seg(c, "Claim two. Nearly every professional basketball player is tall. So if you're tall, you're probably a professional basketball player.",
    "Card ②: basketball icon + height bar; text 'tall | pro player → pro player | tall?'.", 1.5)
seg(c, "Swap again. There are millions of tall people, and only a few hundred of them play professionally.",
    "Card ② stamped red 'SWAP'; a big crowd of tall figures with a tiny orange group 'pros'. Label 'illustration'.", 0.8)
seg(c, "Claim three. Out of everyone in the city who matched the trace, about one in nine is guilty.",
    "Card ③: the 9-person line-up; text 'guilty | match ≈ 1 in 9'.", 1.5)
seg(c, "That one is fair. It starts from the people who match, and asks how many are guilty. That's exactly the question the jury needs.",
    "Card ③ stamped green 'FAIR ✓'; the 'given match' part glows.", 1.0)

seg(c, "Claim four. A spam filter catches nine out of ten spam emails. So nine out of ten emails it blocks are spam.",
    "Card ④: envelope icon + filter; text 'blocked | spam: 9 in 10 → spam | blocked: 9 in 10?'.", 1.5, sid="s107a")
seg(c, "Swap. To know how many blocked emails are spam, you'd need to know how many real emails it blocks too. That's the crowd again.",
    "Card ④ stamped red 'SWAP'; a stack of blocked envelopes, some marked 'real email' in blue. Label 'illustration'.", 0.8, sid="s107b")
# ───────────── COMMON MISTAKES ─────────────
c = "Common Mistakes"
seg(c, "Let's name the mistakes, so you can catch them.",
    "Heading 'common mistakes' (red).")
seg(c, "Mistake one: the swap itself. Reading the chance of the evidence, given innocence, as the chance of innocence, given the evidence.",
    "Red card ①: 'P(match | innocent) ≠ P(innocent | match)' with the swap arrows.")
seg(c, "Listen for it in the words. One in a million chance an innocent person would match, is not the same as one in a million chance he's innocent.",
    "Two speech bubbles: left green ✓ 'an innocent person would match: 1 in a million', right red ✗ 'he is innocent: 1 in a million'.", 1.0)
seg(c, "Mistake two: forgetting the crowd. A rare match means very different things in a village and in a whole country.",
    "Red card ②: mini slider with '999 in 1,000' ↔ '1 in 61'.")
seg(c, "Mistake three goes the other way. Some defense lawyers say: there are nine matches, so the chance he did it is only one in nine. The evidence is worthless.",
    "Red card ③: speech bubble 'only 1 in 9 → worthless!' with a red ✗.")
seg(c, "That's a fallacy too. The match took eight million people down to nine. That's powerful evidence. It just isn't proof on its own.",
    "Funnel: '8,000,000' at the top narrows to '9' at the bottom; label 'powerful, not proof'.", 1.0)
seg(c, "And a bonus mistake, from the real case: multiplying chances together when the events are connected. That can make a coincidence look far rarer than it is.",
    "Red bonus card: '1/8,543 × 1/8,543' with a red 'connected?' tag.", 0.8)

# ───────────── RECIPE ─────────────
c = "Recipe"
seg(c, "Here's a recipe to catch the swap in any claim you're shown.",
    "Recipe card frame draws on: 'catch the swap'.")
seg(c, "Step one: find the given. Ask what the number assumes is already true.",
    "① **Find the given** — what does the number assume is true?")
seg(c, "Step two: flip it. Write down the question you actually care about, and check it's not the one you were given.",
    "② **Flip it** — is that the question you actually care about?")
seg(c, "Step three: find the crowd. How many people, or tests, or payments, could have produced this evidence?",
    "③ **Find the crowd** — the base rate: how many could match?")
seg(c, "Step four: count the matches. Expected false matches, plus the real ones.",
    "④ **Count the matches** — crowd × false-match rate, + the real ones.")
seg(c, "And step five: divide. The real matches, out of all the matches. Then add in any other evidence.",
    "⑤ **Divide** — real matches ÷ all matches; then combine other evidence.", 1.0)
seg(c, "Try it on Sam. The given: innocent. Flip it: is Sam innocent, given the match? The crowd: eight million. The matches: about eight, plus one. Divide: one in nine.",
    "The five recipe steps tick green one by one, each with Sam's number beside it: 'innocent' · 'innocent | match?' · '8,000,000' · '8 + 1' · '1 in 9'.", 1.0, sid="s120a")
seg(c, "Because a rare match is not the same as a rare chance of innocence.",
    "Closing line under the card: 'a rare match is not a rare chance of innocence' (violet).", 1.5)

# ───────────── SUBSCRIBE ─────────────
c = "Subscribe"
seg(c, "Look around your world, and notice how often a rare coincidence gets treated as proof.",
    "Four everyday cards: a news headline 'one in a million!', a medical test result, a security alarm, a fraud text message; each stamped 'given what?'.", 0.6)
seg(c, "If this lesson made things clear for you, please subscribe to Math Lab TV, so we can keep building together.",
    "Logo + red SUBSCRIBE button; a cursor clicks it; it turns grey 'SUBSCRIBED ✓'; 'so we can keep building together' appears.", 0.8)

# ───────────── NEXT TIME ─────────────
c = "Next Time"
seg(c, "But here's a puzzle for next time.",
    "Small logo top-centre; a puzzle-piece icon draws on.")
seg(c, "A model says it catches ninety percent of fraud. Another says ninety percent of its alarms are real. Are they bragging about the same thing?",
    "Two model cards: 'catches 90% of fraud' and '90% of alarms are real'; a big '=?' between them.")
seg(c, "They're not. It's the same swap we saw today, wearing a lab coat. Next time, we'll lay it all out in one simple table, called the confusion matrix.",
    "The two cards slot into a 2 × 2 grid outline; chip 'next: the confusion matrix' under the logo.")
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
    md = [f"# The Prosecutor's Fallacy: The Statistics Trap Smart People Fall For\n",
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
        print(f"  {k:28s} {v:4d} words ~{v / 165 * 60:5.0f} s")
