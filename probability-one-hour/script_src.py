#!/usr/bin/env python3
"""Source of truth for the narration. Run to emit script.json + script.md.

Running example (used everywhere; every number checked in verify_numbers.py):
  Two fair dice, one ORANGE and one BLUE, on game night.
  36 equally likely outcomes on a 6 x 6 grid (orange die = x axis, blue die = y axis).
  P(sum 7) = 6/36 = 1/6     P(sum 12) = 1/36     P(sum 8) = 5/36     sums: 1,2,3,4,5,6,5,4,3,2,1
  NOT : P(not 7) = 30/36 = 5/6
  OR  : P(orange 6 or blue 6) = 6 + 6 - 1 = 11/36;  P(sum 7 or sum 11) = 6/36 + 2/36 = 8/36 = 2/9
  AND : P(both 6) = 1/6 * 1/6 = 1/36;  coin heads and die 6 = 1/12
  AT LEAST ONE six in four rolls = 1 - (5/6)^4 = 671/1296 ~ 51.8 %  (wrong "add": 4/6 ~ 66.7 %)
               in six rolls       = 1 - (5/6)^6 = 31031/46656 ~ 66.5 % (wrong "add": 6/6 = 100 %)
  GIVEN: orange shows 6 -> P(sum 12 | orange 6) = 1/6 (vs 1/36); P(sum 7 | orange 6) = 1/6 = P(sum 7)
         sum at least 10 -> 6 outcomes, 2 doubles -> P(double | sum >= 10) = 1/3 (vs 6/36 = 1/6)
         P(orange 6 | sum 12) = 1  vs  P(sum 12 | orange 6) = 1/6
  EXPECTED: one die 3.5, two dice 7. Fair-fair stall: pay 2 tokens, win 10 tokens on a sum of 7
         -> average win 10/6 ~ 1.67 tokens per game, so you lose 1/3 token per game, about 20 tokens per 60 games.
Side examples (short, everyday, all generic): coin, 3 coins (8 outcomes, P(exactly 2 heads) = 3/8),
  weather forecast, spinner, a bag with 3 red and 2 blue marbles (both red: 3/5 * 2/4 = 3/10 without putting back,
  9/25 with putting back), a 4-option quiz guess, the "five heads in a row" streak (1/32; HHHHHH = HHHHHT = 1/64).

Colour roles (one per concept, kept for the whole video):
  orange die = orange #d95926       blue die = blue #3987e5
  outcomes we want (favourable) = aqua #199e70   the total / all outcomes = warn #fab219
  the answer (a probability)    = violet #9085e9  mistakes / traps = red #d03b3b
Connections: owner override for this video — NO callbacks to other channel videos, NO ML/DS/Finance/CS
  scenarios (generic everyday and classroom examples only). No promise to pay off.
  No next-time teaser (owner); the video ends on a subscribe line. Related videos stay in the description.
"""
import json, pathlib, sys

SLUG = "probability-one-hour"            # id in channel/catalog.json
TARGET_MIN = (50, 60)         # from the skill arguments; words ≈ minutes × 150 (voice ~165 wpm + pauses)
D = 0.45                      # default pause between segments (slower pace for a beginner hour)
S = []
N = [0]   # auto-id counter; once voiced, insert new lines with explicit ids (e.g. s017a) so old clips stay cached


def seg(chapter, text, visual, pause=D, sid=None):
    if sid is None:
        N[0] += 1; sid = f"s{N[0]:03d}"
    S.append(dict(id=sid, chapter=chapter, text=text, visual=visual, pause_after=pause))


# ───────────── 1. HOOK ─────────────
c = "Game Night"
seg(c, "It's game night. You and your friend are one move away from winning a board game.",
    "Line-art table with a game board; two player tokens near the finish square; two dice (orange, blue) sit in the middle.")
seg(c, "To win, you need to roll exactly twelve with two dice.",
    "Your token glows; a chip 'you need: 12' appears; the dice show a ghosted 6 and 6.")
seg(c, "Your friend needs exactly seven.",
    "Friend's token glows; chip 'friend needs: 7'.")
seg(c, "You each get one roll. So, who is more likely to win?",
    "Both chips side by side with a big '?' between them.", 1.2)
seg(c, "A lot of people say it's the same. Twelve is one number, seven is one number. Every number is just as likely, right?",
    "A balance beam: '12' on one pan, '7' on the other, sitting level; a grey 'gut feeling' label.")
seg(c, "Wrong. Seven comes up six times more often than twelve.",
    "The beam slams down on the 7 side; a violet tag '6 times more likely' drops in.", 1.5)
seg(c, "Six times. Same dice. Same table. Same luck.",
    "Six little '7' tokens stack on the left, one '12' token on the right, on a count axis 0–6.", 0.8)
seg(c, "If you played this race one hundred times, your friend would win about seventeen times. You'd win about three.",
    "Tally on a count axis 0–20: friend ≈ 17, you ≈ 3 (expected, out of 100 races).", sid="s007a")
seg(c, "That's what probability does. It takes something that feels like pure luck, and shows you a hidden pattern underneath.",
    "The dice dissolve into a 6 by 6 grid of squares that briefly flashes the diagonal pattern.")
seg(c, "And here's the promise. Give me one hour, and starting from absolute zero, you will finally understand probability.",
    "A clock icon sweeps from 0 to 60 minutes.", 0.6)
seg(c, "No scary formulas without pictures. No skipped steps. Just counting, and seeing.",
    "Three chips pop: 'no scary formulas' · 'no skipped steps' · 'just counting'.", 0.6)
seg(c, "Let's begin.",
    "Title card: 'PROBABILITY' (violet) with subtitle 'from absolute zero, in one hour'.", 1.0)

# ───────────── 2. WELCOME ─────────────
c = "Welcome"
seg(c, "Welcome to Math Lab TV. Where math is something you can see.",
    "Logo (violet rounded square with a green bell curve) + MATH LAB TV + tagline 'where math is something you can see'.", 0.7)
seg(c, "Today you will learn what a probability really is, and how to find one just by counting.",
    "Small logo top-right. Big ① (aqua); a mini 0-to-1 scale with a pointer; caption 'what probability is, and how to count it'.")
seg(c, "You will see the three little words that power almost every probability question. Not, or, and and.",
    "Big ② (violet); three chips NOT · OR · AND; caption 'the three magic words'.")
seg(c, "And you will learn how new information changes the odds, and how to spot the traps that fool almost everyone.",
    "Big ③ (warn); a grid shrinking to a smaller grid, then a red trap icon; caption 'new information, and the traps'.", 0.6)

# ───────────── 3. WHY IT MATTERS ─────────────
c = "Why It Matters"
seg(c, "Before we start, why should you care about probability at all?",
    "A question card 'Why care?' centered.")
seg(c, "Because you already use it, every single day, without noticing.",
    "Four empty cards slide in a row.")
seg(c, "When the weather app says seventy percent chance of rain, and you decide to take an umbrella, that's probability.",
    "Card 1: cloud with rain drops; a meter on a 0–100% axis fills to 70%.")
seg(c, "When you guess on a quiz question with four choices, and you know you have one chance in four, that's probability.",
    "Card 2: quiz sheet with A B C D; one option circled; chip '1 in 4'.")
seg(c, "When you wonder if it's worth playing a game at the school fair, that's probability.",
    "Card 3: fair stall with a spinner; a '?' over the prize.")
seg(c, "When a doctor says a medicine works for most people, or a sports commentator says a team is the favourite, they're talking in probabilities too.",
    "Two small cards: a medicine bottle 'works for most people', a trophy 'the favourite'.")
seg(c, "And when someone says, I've lost five times in a row, so I'm due for a win, that's a probability mistake. We'll fix that one later.",
    "Card 4: a speech bubble 'I'm due for a win!' gets a red trap stamp.", 0.8)
seg(c, "Probability is simply the math of not knowing for sure.",
    "The four cards shrink; a big phrase writes on: 'the math of not knowing for sure'.", 1.0)
seg(c, "Games, sports, quizzes, weather, even deciding whether to carry a jacket. They're all little bets about an uncertain future.",
    "Icons orbit the phrase: dice, ball, quiz, cloud, jacket.", sid="s022a")
seg(c, "You can't know what the next roll will be. But you can know a lot about what tends to happen. And that's surprisingly powerful.",
    "A single die tumbles with a '?' (next roll), then dissolves into a bar chart outline labelled 'what tends to happen'.")
seg(c, "So let's build it from the very first brick.",
    "One brick drops onto an empty base line.", 0.6)

# ───────────── 4. WHAT IS PROBABILITY ─────────────
c = "What Is Probability?"
seg(c, "A probability is just a number. It tells you how likely something is to happen.",
    "A horizontal number line from 0 to 1 with ticks every 0.1, title 'how likely'.")
seg(c, "And this number always lives between zero and one.",
    "The ends of the line glow: '0' and '1'.")
seg(c, "Zero means impossible. It will never happen.",
    "At 0: label 'impossible' (blue); example card: a normal die showing 'roll a 7 on one die'.")
seg(c, "Like rolling a seven on one ordinary die. A die only has the numbers one to six, so seven can never come up.",
    "A die net unfolds showing faces 1–6; '7' with a red cross.")
seg(c, "One means certain. It will always happen.",
    "At 1: label 'certain' (orange); example card 'roll a number less than 7'.")
seg(c, "Like rolling a number smaller than seven on that same die. Every face works, so it's guaranteed.",
    "All six faces get green ticks.")
seg(c, "And everything else, everything that might or might not happen, sits somewhere in between.",
    "The middle of the line shades softly.", 0.6)
seg(c, "Right in the middle, at one half, is a perfect toss-up.",
    "Pointer at 0.5, label 'toss-up'.")
seg(c, "Like flipping a coin and getting heads. Half the time yes, half the time no.",
    "A coin flips and lands heads; a two-part bar splits 1/2 | 1/2.")
seg(c, "The closer a number is to one, the more likely it is. The closer it is to zero, the less likely.",
    "Arrows along the line: toward 1 'more likely', toward 0 'less likely'.")
seg(c, "And a probability can never be negative, and never bigger than one. If you ever get an answer like one point two, or minus a half, you know something went wrong.",
    "Red zones beyond both ends of the 0–1 line: '−0.5 ✗' and '1.2 ✗'.", sid="s034a")
seg(c, "Let's place a few everyday things on this line, just by feel.",
    "Empty markers wait above the line.")
seg(c, "The sun rising tomorrow? Right up near one.",
    "A sun icon lands near 1.")
seg(c, "Rain tomorrow, when the forecast says seventy percent? Around zero point seven.",
    "A cloud lands at 0.7.")
seg(c, "Guessing a quiz question right with four choices? Zero point two five.",
    "A quiz icon lands at 0.25.")
seg(c, "Winning a big lottery? So close to zero that you can't even see the gap.",
    "A ticket icon lands at 0; a magnifier shows a tiny gap labelled 'very, very small'.", 0.8)
seg(c, "Now, there are three ways to write the same probability, and you'll see all three everywhere.",
    "Three empty slots: 'fraction' · 'decimal' · 'percent'.")
seg(c, "As a fraction, like one half.",
    "Slot 1 fills: 1/2.")
seg(c, "As a decimal, like zero point five.",
    "Slot 2 fills: 0.5.")
seg(c, "Or as a percent, like fifty percent. Percent just means out of a hundred.",
    "Slot 3 fills: 50%; a 10 by 10 grid with 50 squares shaded.")
seg(c, "They are all the same amount. One half, zero point five, fifty percent. Three outfits, one person.",
    "Equals signs link the three slots; they collapse into one violet point at 0.5 on the line.", 1.0)
seg(c, "To change a decimal into a percent, just multiply by one hundred. Zero point two five becomes twenty five percent.",
    "0.25 × 100 = 25% writes on; a 10 by 10 grid shades 25 squares.")
seg(c, "We'll mostly use fractions in this video, because fractions show you the counting.",
    "The fraction slot glows warn yellow.")
seg(c, "But what does a probability actually mean? If the chance of rain is seventy percent, will it rain or not?",
    "Cloud card returns with a '?'.", 0.8)
seg(c, "Here's the honest answer. A probability doesn't tell you what will happen next time.",
    "A single day card shows '?' (one day can't be predicted).")
seg(c, "It tells you what happens in the long run. Out of many days with a forecast like this one, about seventy out of every hundred will have rain.",
    "A calendar grid of 100 days on axes (columns 1–10, rows 1–10); 70 days turn to rain icons one row at a time.")
seg(c, "So on any one day, it might stay dry. That doesn't mean the forecast was wrong.",
    "One dry sun day pulses; label 'still fits the 70%'.")
seg(c, "Keep that idea in your pocket. Probability is about patterns over many tries, not about one single try.",
    "Chip 'patterns over many tries' slides into a small pocket icon top-right, which stays.", 1.0)
seg(c, "And where do probabilities come from? There are three main ways.",
    "Three empty cards: 'count', 'experiment', 'judgement'.")
seg(c, "One, you can count. Like a die with six equal faces. We'll do lots of this.",
    "Card 1 fills: a die and '1/6'.")
seg(c, "Two, you can experiment. Try something many times and see how often it happens. Like checking how often your bus is late over a whole term.",
    "Card 2 fills: a tally chart of late days (illustration).")
seg(c, "And three, sometimes people simply give their best judgement, like a coach saying, I think we have a sixty percent chance of winning this match.",
    "Card 3 fills: a coach with a speech bubble '60%?'.")
seg(c, "That last kind is the shakiest. In this video, we'll stick to the first two, where we can actually check our answers.",
    "Card 3 dims; cards 1 and 2 glow.", 0.8)

# ───────────── 5. COUNTING OUTCOMES ─────────────
c = "Counting Outcomes"
seg(c, "So how do we actually find a probability? For lots of everyday questions, you just count.",
    "Title strip 'Probability by counting'.")
seg(c, "Let's start with one die.",
    "A single orange die rotates in.")
seg(c, "When you roll it, there are six things that can happen. It can land on one, two, three, four, five, or six.",
    "Six die faces line up on an axis labelled 'face' with ticks 1–6.")
seg(c, "Each of these is called an outcome. An outcome is one possible result.",
    "Definition card: 'OUTCOME = one possible result'.")
seg(c, "And the list of all possible outcomes has a name too. It's called the sample space. That's just a fancy name for everything that could happen.",
    "A warn-yellow box wraps all six faces; label 'sample space = everything that could happen'.", 0.8)
seg(c, "Now, if the die is fair, each face is equally likely. No face is special. The die isn't loaded.",
    "Six equal bars on the axis, each of height 1/6 on a y axis 'probability' 0 to 0.3.")
seg(c, "So what's the chance of rolling a four?",
    "Face 4 lifts up.")
seg(c, "There is one outcome we want, the four. Out of six outcomes in total. So the chance is one out of six. One sixth.",
    "Fraction builds: '1' (aqua, outcomes we want) over '6' (warn, all outcomes) = 1/6 (violet).", 1.0)
seg(c, "That's the whole recipe. Probability equals the number of outcomes you want, divided by the total number of outcomes.",
    "Rule card: P = (outcomes you want) / (all outcomes), colour-coded aqua over warn.", 1.2)
seg(c, "The letter P is just short for probability. When you see P of something, read it as, the probability of that thing.",
    "Definition: 'P( ) = the probability of ...'; example 'P(4) = 1/6'.")
seg(c, "Let's try another one. What's the chance of rolling an even number?",
    "Faces reset; question chip 'even number?'.")
seg(c, "The even numbers are two, four and six. That's three outcomes we want.",
    "Faces 2, 4, 6 turn aqua.")
seg(c, "Three out of six. Which is the same as one half.",
    "3/6 = 1/2 builds; pointer drops at 0.5 on a mini 0–1 line.", 0.8)
seg(c, "A group of outcomes we care about, like rolling an even number, is called an event.",
    "Definition card: 'EVENT = a group of outcomes you care about'; the aqua faces get a bracket.")
seg(c, "What about rolling a number bigger than four? That's five or six. Two out of six, which is one third.",
    "Faces 5, 6 turn aqua; 2/6 = 1/3.")
seg(c, "See how simple this is? Count what you want. Count everything. Divide.",
    "Three icons: 'count what you want' → 'count everything' → 'divide'.", 1.0)
seg(c, "But there's one small rule hiding inside this recipe, and it's really important.",
    "A warn exclamation mark pulses over the rule card.")
seg(c, "The counting trick only works when every outcome is equally likely.",
    "Underline under 'equally likely' on the rule card.", 0.8)
seg(c, "Here's an example where it breaks. Imagine a spinner where the red part is three quarters of the circle, and the blue part is one quarter.",
    "A spinner circle: red 270°, blue 90°.")
seg(c, "There are two colours. But the chance of red is not one half. It's three quarters, because red takes up more space.",
    "A wrong label '1/2?' gets a red cross; the circle splits into four equal quarters, three red; '3/4' in violet.")
seg(c, "Fix it by cutting the circle into equal pieces first. Four equal quarters. Three of them are red. Now counting works again.",
    "Quarter lines draw; count 1, 2, 3 on the red quarters; 3/4.", 1.0)
seg(c, "So, always ask, are my outcomes equally likely? If they aren't, split them into pieces that are.",
    "Rule card adds a footnote: 'only if all outcomes are equally likely'.")
seg(c, "Now let's level up, and flip two coins.",
    "Two coins appear side by side, labelled 'coin 1' and 'coin 2'.")
seg(c, "What's the chance you get one head and one tail?",
    "Question chip 'one head and one tail?'.")
seg(c, "Many people think there are three outcomes. Two heads, two tails, or one of each. So the answer must be one third.",
    "Three boxes: 'HH' 'TT' 'one of each' with a grey '1/3?' label.")
seg(c, "But those three aren't equally likely. Watch.",
    "The 'one of each' box shakes.")
seg(c, "Let's draw a tree. The first coin can be heads or tails. Then for each of those, the second coin can be heads or tails.",
    "A tree diagram grows left to right: first split H / T, then each splits H / T.")
seg(c, "That gives four outcomes. Heads heads. Heads tails. Tails heads. Tails tails.",
    "Leaves label HH, HT, TH, TT.")
seg(c, "And these four are equally likely. Each one has a chance of one quarter.",
    "Each leaf gets '1/4'.")
seg(c, "Now count. One head and one tail happens two ways, heads then tails, or tails then heads.",
    "HT and TH turn aqua.")
seg(c, "Two out of four. One half. Not one third.",
    "2/4 = 1/2 in violet; the grey '1/3?' gets a red cross.", 1.2)
seg(c, "The lesson? Keep track of which coin is which. Heads tails and tails heads are different outcomes, even if they look the same at the end.",
    "Coin 1 is tinted orange, coin 2 blue; HT and TH shown side by side with their coloured coins.")
seg(c, "Let's push it one step further. Three coins.",
    "A third coin joins.")
seg(c, "Each new coin doubles the branches. Two, then four, then eight outcomes.",
    "The tree grows a third level; a counter shows 2 → 4 → 8.")
seg(c, "What's the chance of getting exactly two heads?",
    "Question chip 'exactly two heads?'.")
seg(c, "Look through the eight leaves. Heads heads tails. Heads tails heads. Tails heads heads. That's three.",
    "HHT, HTH, THH turn aqua one by one with a counter 1, 2, 3.")
seg(c, "So the answer is three out of eight.",
    "3/8 in violet; also '= 0.375'.", 1.0)
seg(c, "A tree is a wonderful tool. When you're not sure how many outcomes there are, draw the tree, and the leaves will tell you.",
    "The tree glows; tag 'draw the tree'.")

# ───────────── 5b. COUNTING BIGGER THINGS ─────────────
c = "Counting Bigger Things"
seg(c, "Trees are great, but they can get huge very quickly. So here's a shortcut for counting outcomes, without drawing every branch.",
    "A tree explodes into dozens of branches, then fades; chip 'a faster way to count'.")
seg(c, "Imagine you have three shirts and four pairs of trousers. How many different outfits can you make?",
    "Three shirts (illustration shapes) in a column on the left, four trousers in a row along the top.")
seg(c, "Put the shirts down the side and the trousers along the top, and you get a grid. Three rows, four columns.",
    "A 3 by 4 grid on axes: x 'trousers' 1–4, y 'shirt' 1–3; each cell is one outfit.")
seg(c, "Twelve squares. Twelve outfits. Three times four.",
    "Counter 3 × 4 = 12 in warn.", 1.0)
seg(c, "This is called the multiplication rule for counting. If one choice can be made in some number of ways, and a second choice in some number of ways, then together, you multiply.",
    "Rule card: 'ways for choice 1 × ways for choice 2 = total ways'.")
seg(c, "Add two pairs of shoes, and every one of those twelve outfits splits into two. Twelve times two is twenty four.",
    "The grid duplicates into two layers (shoe A, shoe B); 12 × 2 = 24.")
seg(c, "So if you get dressed in the dark, and grab each item at random, the chance of getting one particular outfit is one out of twenty four.",
    "One cell glows aqua; 1/24 in violet.", 1.0)
seg(c, "Here's another one. A phone lock with a four digit code. Each digit can be anything from zero to nine. That's ten choices.",
    "Four empty code slots; under each, a chip '10 choices'.")
seg(c, "First digit, ten ways. Second digit, ten ways. Third, ten. Fourth, ten.",
    "Each slot fills with '10' one by one.")
seg(c, "Ten times ten times ten times ten. Ten thousand possible codes.",
    "10 × 10 × 10 × 10 = 10,000 in warn.", 1.0)
seg(c, "So if a stranger picks up your phone and guesses once, their chance of getting it right is one in ten thousand.",
    "1/10,000 in violet; a tiny marker near 0 on the 0–1 line.")
seg(c, "And with three different guesses, it's three in ten thousand. Still tiny.",
    "3/10,000 in violet.")
seg(c, "That's why phones lock you out after a few wrong tries. They keep the number of guesses small, so the chance stays small.",
    "A padlock icon with 'too many tries' and a timer.", 1.0)
seg(c, "And this is exactly why two dice give thirty six outcomes. Six ways for the orange die, times six ways for the blue die.",
    "Two dice with '6 × 6 = 36'.")
seg(c, "Count the choices, multiply, and you know the size of your world.",
    "Chip 'multiply the choices = size of the world'.", 0.8)

# ───────────── 5c. ORDER ─────────────
c = "Putting Things in Order"
seg(c, "The multiplication rule has another trick. It can count how many ways there are to put things in order.",
    "Three book spines labelled A, B, C on a shelf.")
seg(c, "Say you have three books, A, B and C, and you put them on a shelf in a random order. How many orders are there?",
    "Question chip 'how many orders?'.")
seg(c, "For the first spot, you have three books to choose from. Once one is placed, two books are left for the second spot. And then just one book for the last spot.",
    "Three shelf slots fill with counts 3, 2, 1.")
seg(c, "Three times two times one. Six orders.",
    "3 × 2 × 1 = 6; all six orders appear in a list: ABC, ACB, BAC, BCA, CAB, CBA.", 1.0)
seg(c, "So the chance they land in alphabetical order, A then B then C, is one out of six.",
    "ABC glows aqua; 1/6 in violet.")
seg(c, "Now try ten books. Ten times nine times eight, all the way down to one. That's over three and a half million orders.",
    "10 × 9 × 8 × … × 1 = 3,628,800 in warn.")
seg(c, "The chance that ten books shuffled at random land in perfect order is about one in three and a half million. Tiny.",
    "1/3,628,800 → marker at 0 on the 0–1 line.", 1.0)
seg(c, "That's why a well shuffled deck of cards is almost certainly in an order that has never existed before. There are just too many possible orders.",
    "A deck fan; chip 'too many orders to ever repeat'.")
seg(c, "Now, a lottery. Suppose you must pick six numbers out of forty nine, and the order doesn't matter.",
    "A grid of numbered balls 1–49 (7 by 7); six get circled.")
seg(c, "If order mattered, there would be forty nine times forty eight times forty seven times forty six times forty five times forty four ways.",
    "49 × 48 × 47 × 46 × 45 × 44 writes on.")
seg(c, "But the same six numbers can be picked in any order. Six times five times four times three times two times one, which is seven hundred and twenty orders. So we divide by that.",
    "÷ (6 × 5 × 4 × 3 × 2 × 1) = ÷ 720.")
seg(c, "The result is almost fourteen million different tickets.",
    "= 13,983,816 in warn.", 1.0)
seg(c, "So the chance one ticket wins is about one in fourteen million. Remember that tiny gap near zero on our line? That's what it looks like.",
    "The 0–1 line returns; magnifier shows the ticket marker crushed against 0.", 1.0)
seg(c, "Here's a way to feel that number. If you bought one ticket every week, you'd expect to wait over a quarter of a million years for a win.",
    "A timeline arrow stretching off the screen with '≈ 269,000 years'.")
seg(c, "Counting carefully turns a vague feeling, maybe I'll win, into a clear number.",
    "Chip 'vague feeling → clear number'.", 0.8)

# ───────────── 6. TWO DICE ─────────────
c = "Two Dice"
seg(c, "Now we have enough tools to solve our game night puzzle.",
    "Game night chips return: 'you need: 12' · 'friend needs: 7'.")
seg(c, "We're rolling two dice. To keep them apart, let's make one orange and one blue.",
    "An orange die and a blue die drop in.")
seg(c, "The orange die can land six ways. And for each of those, the blue die can land six ways.",
    "Orange faces 1–6 along an x axis; blue faces 1–6 up a y axis.")
seg(c, "So let's draw a grid. Orange along the bottom, blue up the side. Every square is one outcome.",
    "A 6 by 6 grid fills between the axes; axis titles 'orange die' and 'blue die'; equal x/y scale.")
seg(c, "This square, for example, is orange three and blue five.",
    "Square (3,5) highlights; label 'orange 3, blue 5'.")
seg(c, "Six columns, six rows. Six times six is thirty six outcomes.",
    "Counter: 6 × 6 = 36 in warn yellow.", 0.8)
seg(c, "And just like with the coins, orange three blue five is different from orange five blue three. Two different squares.",
    "Squares (3,5) and (5,3) both highlight with a 'not the same' chip.")
seg(c, "With fair dice, all thirty six squares are equally likely. So now we can count.",
    "All squares flash once.")
seg(c, "Let's write the total of the two dice inside every square.",
    "Sums write into all 36 squares, row by row.", 0.8)
seg(c, "Do you see the pattern? Equal totals line up along slanted lines.",
    "Diagonals of equal sums briefly glow in turn.")
seg(c, "Now, how many squares have a total of twelve?",
    "Question chip '12?'.")
seg(c, "Only one. Orange six and blue six. The top right corner.",
    "Square (6,6) turns aqua.")
seg(c, "So the chance of rolling twelve is one out of thirty six.",
    "1/36 in violet.", 1.0)
seg(c, "And a total of seven?",
    "Question chip '7?'.")
seg(c, "Count them. One and six. Two and five. Three and four. Four and three. Five and two. Six and one.",
    "The 7-diagonal lights aqua one square at a time with a counter 1 to 6.")
seg(c, "Six squares. Six out of thirty six. Which is one sixth.",
    "6/36 = 1/6 in violet.", 1.2)
seg(c, "There it is. Seven has six ways to happen. Twelve has only one. That's why seven is six times more likely.",
    "Side by side: the long 7-diagonal and the lonely 12 corner; '6 ways' vs '1 way'.", 1.5)
seg(c, "The dice aren't magic. Seven is simply the total with the most ways to be made.",
    "Chip 'most ways to be made' sits on the 7-diagonal.")
seg(c, "Let's count the ways for every total, and build a chart.",
    "Grid shrinks to the left; an empty bar chart appears with x axis 'total' 2–12 and y axis 'number of ways' 0–6.")
seg(c, "Two can only be made one way. Three, two ways. Four, three ways. Five, four ways. Six, five ways. Seven, six ways.",
    "Each diagonal slides off the grid and stacks into its bar, from 2 up to 7.")
seg(c, "And then it comes back down. Eight, five ways. Nine, four. Ten, three. Eleven, two. And twelve, just one.",
    "Bars 8 to 12 fill in; the chart forms a triangle.")
seg(c, "A perfect little mountain, with seven at the peak.",
    "Outline of the triangle glows; peak tagged '7'.", 1.0)
seg(c, "Add up all the bars, and you get thirty six. Every square is counted exactly once.",
    "1+2+3+4+5+6+5+4+3+2+1 = 36 writes along the bottom.")
seg(c, "If we divide every bar by thirty six, each bar becomes a probability. This picture has a name. It's called a probability distribution.",
    "Y axis relabels to 'probability' with ticks 0, 1/36 … 6/36; title 'probability distribution'.", 0.8)
seg(c, "A distribution is just a map that shows how the chances are spread out over all the possible results.",
    "Definition card: 'DISTRIBUTION = how the chances are spread out'.")
seg(c, "Now you can answer lots of questions just by reading the chart. The chance of a total of eight? Five out of thirty six.",
    "Bar 8 highlights; 5/36.")
seg(c, "The chance of a total of two or twelve? Only one out of thirty six each. They're the rarest rolls in the game.",
    "Bars 2 and 12 highlight; '1/36 each'.")
seg(c, "Here's another one. What's the chance of rolling a double, both dice showing the same number? That's the diagonal from the bottom left to the top right. Six squares. One sixth.",
    "Diagonal (1,1)…(6,6) turns aqua; 6/36 = 1/6.")
seg(c, "And the chance of a total of four or less? Two has one way, three has two, four has three. Six squares again. One sixth.",
    "Bottom-left corner triangle of 6 squares aqua; 6/36 = 1/6.")
seg(c, "Many board games are designed around this exact mountain, even if the players never notice.",
    "A game board illustration fades in behind the chart (shape only).", 1.0)

# ───────────── 7. MANY TRIES ─────────────
c = "Try It Many Times"
seg(c, "But hold on. Does real life actually follow this counting? Let's test it.",
    "Theory chart from before on the left; an empty 'real rolls' chart on the right.")
seg(c, "Imagine flipping a fair coin ten times.",
    "Ten coin slots in a row.")
seg(c, "The chance of heads is one half. So should you get exactly five heads? Not necessarily.",
    "The slots flip one by one (simulation): seven heads, three tails; counter 'heads: 7 of 10'.")
seg(c, "In this run we got seven heads out of ten. That's seventy percent, not fifty.",
    "A pointer on a 0–100% axis sits at 70%; a dashed line marks 50%.")
seg(c, "Is the coin broken? No. With only ten flips, wobbles like this happen all the time.",
    "Label 'simulation · 10 flips: big wobbles'.", 0.8)
seg(c, "Now let's flip it a hundred times. Then a thousand. Then ten thousand.",
    "A line chart: x axis 'number of flips' (log scale 1 to 10,000), y axis 'share of heads' 0–100%; dashed line at 50%.")
seg(c, "Watch the share of heads. At first it jumps around wildly.",
    "The simulated line zigzags early on.")
seg(c, "But the more flips we do, the more it settles down, closer and closer to one half.",
    "The line hugs the dashed 50% line on the right side; label 'settles near 1/2'.", 1.2)
seg(c, "This is called the law of large numbers. Over many, many tries, what actually happens gets closer to the probability.",
    "Definition card: 'LAW OF LARGE NUMBERS: over many tries, results get close to the probability'.", 1.0)
seg(c, "Let's do the same with our two dice. We'll roll them thirty six times, and build a chart of the totals.",
    "Dice roll animation; the 'real rolls' bar chart (totals 2–12) starts filling.")
seg(c, "After thirty six rolls, the chart is bumpy and messy. Some totals didn't even show up.",
    "Simulation result for 36 rolls: lumpy bars, a few totals at zero.")
seg(c, "After three hundred and sixty rolls, a shape starts to appear.",
    "Bars for 360 rolls (scaled to share), a rough triangle.")
seg(c, "And after thirty six thousand rolls, look. It's our mountain. Almost exactly.",
    "Bars for 36,000 rolls; the theory triangle outline overlays and matches.", 1.5)
seg(c, "The counting we did on paper predicted what happens when you really roll the dice. That's the power of probability.",
    "Paper grid icon → arrow → real dice icon; tag 'paper predicts reality'.")
seg(c, "This also gives us a second way to find a probability. When you can't count the outcomes, you can try something many times, and see how often it happens.",
    "Two routes: 'count outcomes' and 'try many times', both pointing to the 0–1 line.")
seg(c, "You can try this yourself tonight. Flip a coin twenty times, and write down how many heads you get. Then ask a friend to do the same. Your numbers will probably be different, and that's completely normal.",
    "A notebook tally of 20 flips (illustration) next to a friend's tally; two different counts.", sid="s128a")
seg(c, "That's how a weather forecast works, in a simple sense. Out of many past days that looked like today, how many had rain?",
    "Calendar of past days with rain icons; fraction 'rainy days / similar days'.")
seg(c, "But remember the pocket idea. Many tries, not one. The law of large numbers says nothing about the next single flip.",
    "The pocket icon top-right glows: 'patterns over many tries'.", 1.0)
seg(c, "In fact, small numbers of tries can look surprisingly streaky.",
    "A row of 20 simulated coin flips appears, with a run of four heads highlighted.")
seg(c, "If you flip a coin twenty times, getting four or more heads in a row somewhere is not rare at all. It happens in nearly half of all runs.",
    "Chip '4+ heads in a row: in about 48% of 20-flip runs'.")
seg(c, "Random doesn't mean nicely mixed. Random means unpredictable. And unpredictable things are often clumpy.",
    "Two strips: a neat alternating pattern labelled 'looks random, but isn't typical' vs a clumpy strip labelled 'real randomness'.", 1.0)

# ───────────── 7a. FAIR OR NOT ─────────────
c = "Is This Die Fair?"
seg(c, "Here's a fun way to use what we just learned. Suppose a friend hands you a die, and you wonder, is it fair?",
    "A single die with a suspicious '?' tag.")
seg(c, "If it's fair, each face should come up one sixth of the time. So in sixty rolls, you'd expect each face about ten times.",
    "Bar chart axes: x 'face' 1–6, y 'times rolled' 0–25; dashed line at 10, label 'expected: 60 × 1/6 = 10'.")
seg(c, "Let's roll it sixty times. We get eight ones, eleven twos, nine threes, twelve fours, seven fives and thirteen sixes.",
    "Bars fill: 8, 11, 9, 12, 7, 13 (simulation of a fair die).")
seg(c, "Not exactly ten each. But is that suspicious? No. This kind of wobble is completely normal for a fair die, with only sixty rolls.",
    "Bars within a soft band around 10 labelled 'normal wobble'.", 1.0)
seg(c, "Now a different die. Sixty rolls, and twenty five of them are sixes.",
    "Second chart: the 6 bar shoots to 25 (red outline); others around 7.")
seg(c, "That's way more than ten. For a fair die, a result this extreme would be extremely rare. So you'd have good reason to think this die is loaded.",
    "Tag 'very unlikely for a fair die → suspicious' in warn.", 1.0)
seg(c, "Notice what we did. We used probability to predict what fair looks like, then compared it with what really happened.",
    "Two-step chip: 'predict fair' → 'compare with reality'.")
seg(c, "Small differences, we shrug off. Huge differences make us suspicious. Scientists use this same idea, with more careful math, to test whether something is really going on.",
    "A small gap vs a big gap between predicted and real bars.", 0.8)

# ───────────── 7b. HALFWAY CHECK ─────────────
c = "Quick Recap"
seg(c, "Let's take a breath, and look at how far we've come.",
    "A path with milestones; a 'you are here' pin at the middle.")
seg(c, "A probability is a number from zero to one. Zero is impossible, one is certain.",
    "Milestone 1: the 0–1 line.")
seg(c, "When outcomes are equally likely, the probability is the outcomes you want, divided by all the outcomes.",
    "Milestone 2: the counting rule card.")
seg(c, "To find all the outcomes, draw a tree or a grid, or multiply the number of choices.",
    "Milestone 3: tree, grid and '6 × 6'.")
seg(c, "With two dice, seven is the most likely total, because it has the most ways to be made.",
    "Milestone 4: the mountain chart.")
seg(c, "And over many tries, real results settle close to the probability. But a single try can still surprise you.",
    "Milestone 5: the settling line chart.", 1.0)
seg(c, "If all of that makes sense, you've already got the foundation. Everything from here is built on top of it.",
    "The pin moves forward; upcoming milestones 'NOT · OR · AND · GIVEN · EXPECTED VALUE' light up faintly.", 0.8)

# ───────────── 8. NOT ─────────────
c = "The Word NOT"
seg(c, "Now for the three little words that unlock almost every probability question. The first one is not.",
    "Three chips NOT · OR · AND; NOT lifts and glows.")
seg(c, "Something either happens, or it doesn't. There's no third option.",
    "A rectangle splits into two parts: 'happens' and 'doesn't happen'.")
seg(c, "So the chance it happens, plus the chance it doesn't, must add up to one. To everything.",
    "Bar of length 1 on a 0–1 axis: aqua 'happens' + grey 'doesn't' = 1.")
seg(c, "That means the chance something does not happen is one, minus the chance it does.",
    "Formula: P(not A) = 1 − P(A).", 1.0)
seg(c, "A here is just a name for any event. Like, rolling a seven.",
    "Definition chip: 'A = any event, e.g. rolling a 7'.")
seg(c, "Let's try it. The chance of rolling a total of seven is one sixth. So the chance of not rolling seven is one minus one sixth, which is five sixths.",
    "Two-dice grid returns; 7-diagonal aqua (6 squares); the other 30 squares turn grey; 1 − 1/6 = 5/6.")
seg(c, "And you can check it on the grid. Thirty squares are not seven. Thirty out of thirty six is five sixths. It matches.",
    "Counter on grey squares: 30; 30/36 = 5/6 in violet.", 1.0)
seg(c, "Here's why this matters. Sometimes the thing you want is hard to count, but the opposite is easy.",
    "A big messy pile labelled 'hard' next to a small neat pile labelled 'easy'.")
seg(c, "For example, what's the chance of rolling a total that is not twelve?",
    "Question chip 'not 12?'.")
seg(c, "You could count thirty five squares. Or you can just say, twelve has one square, so not twelve is one minus one over thirty six, which is thirty five over thirty six.",
    "Grid: (6,6) aqua; others grey with a fast counter to 35; 1 − 1/36 = 35/36.")
seg(c, "When counting the thing you want looks painful, flip it around. Count the opposite, and take it away from one.",
    "A flip arrow icon; tag 'count the opposite'.", 1.0)
seg(c, "This little trick becomes a superpower in a few minutes. Hold on to it.",
    "The NOT chip moves to the top-right, next to the pocket icon.")

# ───────────── 8b. ODDS ─────────────
c = "Odds Versus Probability"
seg(c, "While we're here, let's clear up a word that confuses a lot of people. Odds.",
    "Two cards: 'probability' and 'odds' side by side.")
seg(c, "People often say odds when they mean probability. But they are not quite the same thing.",
    "A '≠' between the cards.")
seg(c, "Probability compares the ways something happens to all the ways. Odds compare the ways it happens to the ways it doesn't.",
    "Probability card: 'happens ÷ everything'; odds card: 'happens : doesn't happen'.")
seg(c, "Take a total of seven on two dice. Six squares make seven. Thirty squares don't.",
    "Grid: 6 aqua squares, 30 grey squares; counters '6' and '30'.")
seg(c, "The probability is six out of thirty six. One sixth.",
    "6/36 = 1/6 in violet.")
seg(c, "But the odds are six to thirty. Which simplifies to one to five. For every one way to win, there are five ways to lose.",
    "Odds bar: 1 aqua block next to 5 grey blocks, '1 : 5'.", 1.0)
seg(c, "Notice that one to five and one sixth describe the same chance. One plus five makes six, the total.",
    "1 : 5 → 1 / (1 + 5) = 1/6.")
seg(c, "A fair coin has odds of one to one. One way to win, one way to lose. People sometimes call that evens.",
    "Coin with '1 : 1 = evens' and 1/2 underneath.")
seg(c, "To turn odds into a probability, put the first number on top, and both numbers added together on the bottom.",
    "Rule card: 'odds a : b → probability a / (a + b)'.")
seg(c, "So odds of three to one against something mean one way it happens, three ways it doesn't. One out of four. A probability of one quarter.",
    "Example: '3 : 1 against' → 1 / (1 + 3) = 1/4.", 1.0)
seg(c, "When you hear odds, just ask, is this comparing to the whole, or to the other side?",
    "Chip 'to the whole, or to the other side?'.", 0.8)

# ───────────── 9. OR ─────────────
c = "The Word OR"
seg(c, "The second word is or. What's the chance that this happens, or that happens?",
    "Chips NOT · OR · AND; OR lifts and glows.")
seg(c, "Let's start easy. On our two dice, what's the chance of rolling a total of seven, or a total of eleven?",
    "Grid returns; question chip '7 or 11?'.")
seg(c, "Seven has six squares. Eleven has two squares, five and six, and six and five.",
    "7-diagonal aqua; 11 squares (5,6),(6,5) in a second aqua shade.")
seg(c, "They don't share any squares. A roll can't be seven and eleven at the same time.",
    "A gap chip 'no shared squares'.")
seg(c, "So we just add them. Six plus two is eight squares. Eight out of thirty six.",
    "6/36 + 2/36 = 8/36 = 2/9 in violet.", 1.0)
seg(c, "When two events can't happen together, the chance of one or the other is just the two chances added up.",
    "Rule card: 'can't happen together → P(A or B) = P(A) + P(B)'.")
seg(c, "But careful. This is where a lot of people slip.",
    "Red caution icon.")
seg(c, "What's the chance that the orange die shows six, or the blue die shows six?",
    "Question chip 'orange 6 OR blue 6?'.")
seg(c, "The orange six is a whole column. That's six squares.",
    "Column orange=6 tints orange: 6 squares.")
seg(c, "The blue six is a whole row. Also six squares.",
    "Row blue=6 tints blue: 6 squares.")
seg(c, "So, six plus six is twelve? Let's look.",
    "Grey '6 + 6 = 12?' label.")
seg(c, "The column and the row cross in one corner, double six. If we add them, we count that square twice.",
    "Square (6,6) flashes with a '×2' badge.", 0.8)
seg(c, "So we take it away once. Six plus six, minus one, is eleven.",
    "6 + 6 − 1 = 11; the '12?' gets a red cross.")
seg(c, "The answer is eleven out of thirty six.",
    "11/36 in violet; the 11 squares glow.", 1.2)
seg(c, "This is the full or rule. Add the two chances, then take away the overlap, the part where both happen, so it's not counted twice.",
    "Rule card: P(A or B) = P(A) + P(B) − P(A and B), with the overlap term in warn.", 1.0)
seg(c, "A picture helps. Draw two circles that overlap. To find the area covered by either circle, you add both circles, then remove the middle, because you counted it twice.",
    "Two overlapping circles (orange and blue); the lens in the middle glows warn with '×2', then is counted once.")
seg(c, "If the circles don't overlap at all, the middle is zero, and you're back to simply adding.",
    "The circles slide apart; overlap term becomes 0.")
seg(c, "Here's an everyday example. In a class of thirty students, twelve play football, eight play music, and five do both.",
    "A class of 30 dots on a 10 by 3 grid (illustration); 12 orange outlined, 8 blue outlined, 5 with both.")
seg(c, "How many do football or music? Twelve plus eight is twenty, minus the five who were counted twice. Fifteen students.",
    "12 + 8 − 5 = 15; 15 dots glow.")
seg(c, "So if you pick a student at random, the chance they do football or music is fifteen out of thirty. One half.",
    "15/30 = 1/2 in violet.", 1.0)
seg(c, "Whenever you hear the word or, ask yourself one question. Can both happen at once? If yes, remove the overlap.",
    "Checklist chip: 'OR → can both happen? → subtract the overlap'.")

# ───────────── 10. AND ─────────────
c = "The Word AND"
seg(c, "The third word is and. What's the chance that this happens, and that happens too?",
    "Chips NOT · OR · AND; AND lifts and glows.")
seg(c, "Back to our dice. What's the chance of double six? The orange die shows six, and the blue die shows six.",
    "Grid returns; question 'orange 6 AND blue 6?'.")
seg(c, "On the grid, that's the one square where the six column and the six row meet. One out of thirty six.",
    "Column and row tint; their crossing square glows aqua; 1/36.")
seg(c, "But here's another way to see it. The orange die has a one in six chance of six. And then, the blue die has a one in six chance of six.",
    "Two separate bars: orange 1/6, blue 1/6.")
seg(c, "Multiply them. One sixth times one sixth is one over thirty six. Same answer.",
    "1/6 × 1/6 = 1/36.", 1.0)
seg(c, "Why multiply? Picture it as area. Take a square of side one. The orange six takes one sixth of the width. The blue six takes one sixth of the height.",
    "A unit square on axes 0–1 by 0–1; a vertical strip 1/6 wide (orange) and a horizontal strip 1/6 tall (blue).")
seg(c, "Where they overlap is a little box, one sixth wide and one sixth tall. Its area is one sixth times one sixth.",
    "The tiny overlap box glows violet; 'area = 1/6 × 1/6 = 1/36'.", 1.0)
seg(c, "This works for more than two things. Three dice all showing six? One sixth, times one sixth, times one sixth. One in two hundred and sixteen.",
    "1/6 × 1/6 × 1/6 = 1/216; a tiny cube in a 6 by 6 by 6 block (illustration).")
seg(c, "So and usually means multiply. And multiplying fractions makes things smaller. Both things happening is less likely than either one alone.",
    "A shrinking arrow: 1/6 → 1/36; tag 'AND makes it smaller'.")
seg(c, "But there's a condition. This simple multiplying only works when the two events are independent.",
    "Warn chip 'only if INDEPENDENT'.", 0.8)
seg(c, "Independent means one result doesn't change the chances of the other.",
    "Definition card: 'INDEPENDENT = one result doesn't change the chances of the other'.")
seg(c, "The orange die has no idea what the blue die did. They don't talk to each other. So they're independent.",
    "The two dice with a 'no connection' dashed line and a crossed-out phone icon.")
seg(c, "A coin and a die are independent too. The chance of heads and a six is one half times one sixth. One twelfth.",
    "Tree: coin H/T then die 1–6 = 12 leaves; leaf 'H, 6' glows; 1/2 × 1/6 = 1/12.")
seg(c, "But some events do affect each other. Here's a bag with three red marbles and two blue marbles.",
    "A bag illustration with 3 red and 2 blue marbles drawn as circles.")
seg(c, "You pull out one marble, don't put it back, and then pull out another. What's the chance both are red?",
    "Hand icon takes a marble; chip 'no putting back'.")
seg(c, "First pull. Three red out of five marbles. Three fifths.",
    "Fraction 3/5; the red marbles glow.")
seg(c, "Now, if that first marble was red, the bag has changed. There are only two red left, out of four.",
    "One red marble leaves the bag; 2 red, 2 blue remain; fraction 2/4.")
seg(c, "So the second chance is two quarters. The first pull changed the second one. These events are not independent.",
    "Tag 'the first pull changed the bag' in warn.")
seg(c, "Multiply the chances along the path. Three fifths times two quarters is six over twenty, which is three tenths.",
    "Tree path: 3/5 → 2/4; 3/5 × 2/4 = 6/20 = 3/10 in violet.", 1.0)
seg(c, "If you had put the first marble back, the bag would be the same both times. Three fifths times three fifths, nine over twenty five.",
    "Alternative path: 3/5 × 3/5 = 9/25, labelled 'with putting back'.")
seg(c, "That's a bit higher, because putting the red marble back gives red a better chance the second time.",
    "Comparison on a 0–1 line: 0.30 vs 0.36.")
seg(c, "So, for and: multiply along the path. But always use the chance of the second thing, after the first one has happened.",
    "Rule card: 'AND → multiply along the path, using the updated chance'.", 1.0)

# ───────────── 10b. INDEPENDENT OR NOT ─────────────
c = "Independent or Not?"
seg(c, "Because independence matters so much, let's practise spotting it. For each pair, ask, does the first result change the chances of the second?",
    "Title strip 'Independent or not?'; four empty cards with YES / NO slots.")
seg(c, "One. Flipping a coin today, and flipping it again tomorrow. Independent. The coin doesn't remember.",
    "Card 1: two coins; stamp 'INDEPENDENT' (aqua).")
seg(c, "Two. Drawing a card from a deck, keeping it, and drawing another. Not independent. The deck has changed.",
    "Card 2: a deck missing one card; stamp 'NOT independent' (warn).")
seg(c, "Three. Rain today, and rain tomorrow. Not independent. Rainy weather tends to stick around for a few days, so rain today makes rain tomorrow more likely.",
    "Card 3: two cloud days linked by an arrow; stamp 'NOT independent'.")
seg(c, "Four. Your birthday, and the birthday of a random stranger in another country. Independent. One tells you nothing about the other.",
    "Card 4: two cake icons far apart; stamp 'INDEPENDENT'.")
seg(c, "Five. Whether you study tonight, and whether you pass tomorrow's test. Definitely not independent. Studying changes your chances. That's the whole point.",
    "Card 5: a book and a test paper with a tick; stamp 'NOT independent'.", 1.0)
seg(c, "When events are independent, multiply the plain chances. When they're not, use the updated chance for the second step.",
    "Rule card: 'independent → multiply plain chances · dependent → multiply updated chances'.", 0.8)

# ───────────── 11. AT LEAST ONE ─────────────
c = "At Least One"
seg(c, "Now let's combine not and and, to solve one of the most useful questions in all of probability.",
    "Chips NOT and AND snap together.")
seg(c, "You roll one die four times. What's the chance you get at least one six?",
    "Four die slots in a row; question 'at least one 6 in 4 rolls?'.")
seg(c, "At least one means one six, or two, or three, or four. That's a lot of cases to count.",
    "A messy list of cases: '6 _ _ _', '_ 6 _ _', '6 6 _ _' … piling up.")
seg(c, "Here's a tempting shortcut. Each roll has a one sixth chance. Four rolls, so add them up. Four sixths, about sixty seven percent.",
    "Grey '1/6 + 1/6 + 1/6 + 1/6 = 4/6 ≈ 67%?' label.")
seg(c, "But that can't be right. Watch what happens with six rolls. Six sixths is one. A hundred percent. As if six rolls guarantee a six.",
    "The sum grows to 6/6 = 100%; a red trap stamp: 'guaranteed? no!'.")
seg(c, "Anyone who's ever played a dice game knows you can roll six times and never see a six.",
    "Six simulated rolls with no six: 2, 5, 1, 3, 3, 4.", 1.0)
seg(c, "The adding was wrong because these events can all happen together, so we're counting overlaps again and again.",
    "Overlapping circles multiply into a tangle.")
seg(c, "So let's use the superpower. Flip it around. The opposite of at least one six is, no sixes at all.",
    "Flip arrow; chip 'opposite = NO sixes at all'.")
seg(c, "The chance one roll is not a six is five sixths.",
    "One die: five faces aqua, the 6 face grey; 5/6.")
seg(c, "The rolls are independent. So the chance that all four rolls are not six is five sixths, times five sixths, times five sixths, times five sixths.",
    "5/6 × 5/6 × 5/6 × 5/6 writes under the four slots.")
seg(c, "That's six hundred and twenty five out of one thousand two hundred and ninety six. About forty eight percent.",
    "= 625/1296 ≈ 48.2%; a bar on a 0–100% axis.")
seg(c, "So the chance of at least one six is one minus that. About fifty two percent.",
    "1 − 625/1296 = 671/1296 ≈ 51.8% in violet; the bar's remaining part glows.", 1.2)
seg(c, "Just over a half. Not sixty seven percent.",
    "Side by side: wrong 67% (red, struck) vs right 52% (violet).")
seg(c, "And with six rolls, it's about sixty seven percent. Likely, but nowhere near certain.",
    "Line chart: x axis 'number of rolls' 1–12, y axis 'chance of at least one 6' 0–100%; points rising and bending; 6 rolls at 66.5%.")
seg(c, "Look at this curve. Every extra roll helps, but it never quite reaches one hundred percent.",
    "The curve flattens toward the top dashed 100% line.", 1.0)
seg(c, "This trick works everywhere. The chance of at least one success, equals one, minus the chance of no success at all.",
    "Rule card: P(at least one) = 1 − P(none).", 1.0)
seg(c, "For example, if you guess on three quiz questions, each with four choices, what's the chance you get at least one right?",
    "Three quiz cards A B C D.")
seg(c, "The chance of getting one wrong is three quarters. All three wrong is three quarters cubed, twenty seven over sixty four.",
    "3/4 × 3/4 × 3/4 = 27/64.")
seg(c, "So at least one right is thirty seven out of sixty four. A bit more than half.",
    "1 − 27/64 = 37/64 ≈ 58% in violet.", 1.0)
seg(c, "Whenever you see the words at least one, your brain should shout, flip it around.",
    "A big 'AT LEAST ONE → FLIP IT' banner.")

# ───────────── 11a. CARDS ─────────────
c = "A Deck of Cards"
seg(c, "Let's practise our three words, not, or, and, on something new. A normal deck of playing cards.",
    "A fan of card outlines (no real branding), title 'a standard deck'.")
seg(c, "A deck has fifty two cards. There are four suits, hearts, diamonds, clubs and spades. And each suit has thirteen cards, from ace up to king.",
    "A 13 by 4 grid on axes: x 'rank' A, 2 … 10, J, Q, K; y 'suit' ♥ ♦ ♣ ♠. 4 × 13 = 52 in warn.")
seg(c, "Shuffle well, and every card is equally likely to be on top. So our counting recipe works.",
    "All 52 cells flash once; chip 'equally likely'.")
seg(c, "What's the chance the top card is a heart? Thirteen hearts out of fifty two cards. That's one quarter.",
    "Heart row aqua; 13/52 = 1/4 in violet.", 1.0)
seg(c, "What's the chance it's a king? Four kings out of fifty two. One thirteenth.",
    "King column aqua; 4/52 = 1/13.")
seg(c, "Now, the chance it's a king or a heart?",
    "Question chip 'king OR heart?'.")
seg(c, "Thirteen hearts, plus four kings. But one card is both, the king of hearts. Don't count it twice.",
    "Row and column tint; the crossing cell flashes '×2'.")
seg(c, "Thirteen plus four, minus one, is sixteen. Sixteen out of fifty two, which simplifies to four thirteenths.",
    "13 + 4 − 1 = 16; 16/52 = 4/13 in violet.", 1.0)
seg(c, "And the chance it's not a heart? One minus one quarter. Three quarters.",
    "Other three rows grey-glow; 1 − 1/4 = 3/4.")
seg(c, "Now for and. You draw two cards, without putting the first one back. What's the chance both are aces?",
    "Two card slots; chip 'no putting back'.")
seg(c, "First card. Four aces out of fifty two.",
    "4/52 under slot 1.")
seg(c, "If that was an ace, there are now three aces left, out of fifty one cards.",
    "One ace leaves; 3/51 under slot 2.")
seg(c, "Multiply along the path. Four over fifty two, times three over fifty one. That's one out of two hundred and twenty one.",
    "4/52 × 3/51 = 12/2652 = 1/221 in violet.", 1.0)
seg(c, "Not even half a percent. Two aces in a row really is rare.",
    "Marker near 0 on a 0–100% axis: ≈ 0.45%.")
seg(c, "Same three words, a completely different game. That's the beauty of it. Once you know the tools, they work everywhere.",
    "NOT · OR · AND chips glow together.", 0.8)

# ───────────── 11b. TWO-STEP TREES ─────────────
c = "Two Step Trees"
seg(c, "Real life is often a chain of events, where the second step depends on the first. A tree diagram handles that beautifully.",
    "A two-level tree outline draws on.")
seg(c, "Here's a story. On a typical school day in your town, there's a three in ten chance of rain.",
    "Weather chip 'rain: 3/10'; first split of the tree: 'rain' 3/10, 'dry' 7/10.")
seg(c, "When it rains, the school bus is late half the time. When it's dry, the bus is late only one time in ten.",
    "Second level: rain → 'late' 1/2, 'on time' 1/2; dry → 'late' 1/10, 'on time' 9/10.")
seg(c, "These numbers are made up for this example, but the method works for any numbers.",
    "Small label 'illustration: made-up numbers'.")
seg(c, "Question. On a random school day, what's the chance the bus is late?",
    "Question chip 'bus late?'.")
seg(c, "Let's imagine one hundred school days, and walk them through the tree.",
    "A 10 by 10 grid of day squares on axes, columns 1–10, rows 1–10.")
seg(c, "Three in ten days are rainy. That's thirty rainy days.",
    "30 squares tint blue-grey 'rain'.")
seg(c, "On half of those, the bus is late. Fifteen days.",
    "15 of the rainy squares get an aqua 'late' mark.")
seg(c, "Seventy days are dry. On one in ten of them, the bus is late. Seven days.",
    "7 of the 70 dry squares get an aqua 'late' mark.")
seg(c, "So the bus is late on fifteen plus seven days. Twenty two days out of one hundred.",
    "15 + 7 = 22; 22/100 in violet.", 1.0)
seg(c, "With the tree, you can do this without imagining days. Multiply along each path to a late bus, then add the paths together.",
    "Paths highlight: 3/10 × 1/2 = 15/100 and 7/10 × 1/10 = 7/100; sum 22/100.")
seg(c, "Multiply along a path, because both steps have to happen. That's and. Add across paths, because either path works. That's or.",
    "The words AND (along) and OR (across) label the tree.", 1.2)
seg(c, "And a quick check. All four paths together, late and on time, rainy and dry, must add up to one hundred days. Fifteen, plus fifteen, plus seven, plus sixty three. One hundred. Good.",
    "All four leaves: 15 + 15 + 7 + 63 = 100.", sid="s297a")
seg(c, "So the tree is just and and or, working together.",
    "Chip 'tree = AND along, OR across'.")
seg(c, "Now a sneaky question, which will lead us into our next big idea. The bus was late today. What's the chance it was raining?",
    "Question chip 'bus was late → was it raining?'.", 1.0)
seg(c, "Look at the hundred days again. The bus was late on twenty two of them. That's our world now.",
    "Only the 22 late squares stay bright; the rest fade.")
seg(c, "Fifteen of those twenty two were rainy days.",
    "The 15 rainy-late squares glow.")
seg(c, "So the chance it was raining, given the bus was late, is fifteen out of twenty two. About sixty eight percent.",
    "15/22 ≈ 68% in violet.", 1.2)
seg(c, "Before you knew anything, rain had a thirty percent chance. Knowing the bus was late made rain much more likely.",
    "Before/after: 30% → 68%.")
seg(c, "That idea, how a clue changes a probability, is what we'll look at next.",
    "Arrow pointing to a chip 'next: GIVEN THAT'.", 0.8)

# ───────────── 12. GIVEN THAT ─────────────
c = "Given That"
seg(c, "So far, we've rolled the dice without knowing anything. But what if someone gives you a clue?",
    "Two-dice grid returns, all squares neutral; a clue envelope floats in.")
seg(c, "This is called conditional probability. It's the chance of something, given that you already know something else.",
    "Definition card: 'CONDITIONAL PROBABILITY = the chance of A, given that B is true'.")
seg(c, "Here's the key idea, and it's beautiful. A clue shrinks the grid.",
    "The grid shrinks to a smaller highlighted region with a 'clue' label.", 1.0)
seg(c, "Your friend rolls both dice, hides them, and peeks at the orange one. They tell you, the orange die is a six.",
    "A cup covers the dice; a speech bubble 'the orange die is a 6!'.")
seg(c, "What's the chance the total is twelve?",
    "Question chip 'total 12, given orange is 6?'.")
seg(c, "Before the clue, it was one in thirty six. But now, every square where orange isn't six is impossible. Cross them out.",
    "Columns 1–5 grey out and fade; only the orange=6 column stays.")
seg(c, "We're left with just one column. Six squares. That's our new world.",
    "The orange=6 column glows warn as the new total: 6.")
seg(c, "And in this new world, a total of twelve is one square out of six. One sixth.",
    "(6,6) aqua; 1/6 in violet.", 1.2)
seg(c, "The clue made twelve six times more likely. New information changed the probability.",
    "Before/after: 1/36 → 1/6, with an arrow labelled 'clue'.")
seg(c, "We write this with a straight line. P of twelve, line, orange six. And we read that line as, given.",
    "Notation: P(12 | orange 6) = 1/6; the bar '|' glows with label 'given'.", 1.0)
seg(c, "So the recipe is the same as always. Count the outcomes you want, but only inside the shrunken world. Then divide by the size of that shrunken world.",
    "Rule card: P(A | B) = (outcomes in both A and B) / (outcomes in B).")
seg(c, "Now here's a surprising one. With the same clue, the orange die is a six, what's the chance the total is seven?",
    "Grid resets to the orange=6 column; question 'total 7, given orange is 6?'.")
seg(c, "In the six column, only one square makes seven, orange six and blue one. One out of six.",
    "Square (6,1) aqua; 1/6.")
seg(c, "But the chance of seven without any clue was also one sixth.",
    "Earlier result '7: 1/6' slides in beside it.")
seg(c, "The clue changed nothing! Knowing the orange die doesn't help you guess whether the total is seven.",
    "Equals sign between the two 1/6 values glows.", 1.2)
seg(c, "Why? Because whatever the orange die shows, there's always exactly one blue number that makes seven. So the clue gives no advantage.",
    "Each column, in turn, lights its single 7-square: one per column.")
seg(c, "And this is the real meaning of independent. Two events are independent when knowing one doesn't change the chance of the other.",
    "Definition card returns: 'INDEPENDENT: the clue doesn't change the chance'.", 1.0)
seg(c, "Let's try a trickier clue. Your friend says, the total is at least ten. What's the chance they rolled a double, two dice showing the same number?",
    "Grid resets; speech bubble 'total is at least 10'; question 'double?'.")
seg(c, "First, shrink the world. Which squares have a total of ten, eleven or twelve?",
    "Squares with sums 10, 11, 12 stay bright; others fade.")
seg(c, "Four and six. Five and five. Six and four. Five and six. Six and five. Six and six. Six squares.",
    "The six squares count up 1–6 in warn.")
seg(c, "Now, which of these are doubles? Five and five, and six and six. That's two.",
    "(5,5) and (6,6) turn aqua.")
seg(c, "Two out of six. One third.",
    "2/6 = 1/3 in violet.", 1.0)
seg(c, "Without the clue, doubles happen six times out of thirty six, one sixth. With the clue, it doubles to one third.",
    "Before/after: 1/6 → 1/3.")
seg(c, "Now for the most important warning in this whole chapter. The order of a given statement matters.",
    "Red caution icon; two cards slide in.")
seg(c, "The chance of a total of twelve, given the orange die is six, is one sixth. We just saw it.",
    "Card 1: P(12 | orange 6) = 1/6 with its shrunken column.")
seg(c, "But the chance the orange die is six, given the total is twelve, is one. It's certain! The only way to make twelve is double six.",
    "Card 2: P(orange 6 | 12) = 1 with its one-square world.")
seg(c, "Same two things. Swapped around. Completely different answers.",
    "A swap arrow between the cards with '≠'.", 1.2)
seg(c, "Here's an everyday version. Most professional basketball players are tall. But most tall people are not professional basketball players.",
    "Two cards: 'given a pro player → very likely tall' vs 'given tall → very unlikely a pro player'.")
seg(c, "Here's one more everyday example. In a class, twelve of the thirty students wear glasses, and eight of those twelve are girls.",
    "A 10 by 3 dot class (illustration); 12 dots get glasses rings; 8 of them violet-tinted 'girls'.")
seg(c, "Pick a student who wears glasses. What's the chance it's a girl? The clue puts you in the glasses world, twelve students. Eight of them are girls. Eight twelfths, two thirds.",
    "Only the 12 glasses dots stay bright; 8/12 = 2/3 in violet.", 1.0)
seg(c, "Cards work the same way. If you're told the top card is a picture card, a jack, a queen or a king, what's the chance it's a king? The world shrinks to twelve picture cards. Four of them are kings. Four twelfths, one third.",
    "Card grid: only the J, Q, K columns stay (12 cells); K column aqua; 4/12 = 1/3.", sid="s333a")
seg(c, "Always ask, which world did the clue put me in? That world goes on the bottom of your fraction.",
    "The fraction bottom glows warn: 'the world the clue puts you in'.", 1.0)

# ───────────── 13. EXPECTED VALUE ─────────────
c = "Expected Value"
seg(c, "Let's go back to the fair. A stall has a game. You pay two tokens to roll two dice. If the total is seven, you win ten tokens.",
    "Fair stall illustration; chips 'cost: 2 tokens' · 'roll 7: win 10 tokens'.")
seg(c, "Should you play? To answer that, we need one more idea. Expected value.",
    "Title strip 'expected value'.")
seg(c, "Expected value is the average result you'd get per game, if you played many, many times.",
    "Definition card: 'EXPECTED VALUE = the average per game, over many games'.")
seg(c, "Let's start with something simple. What's the average number you roll on one die?",
    "One die; faces 1–6 on an axis.")
seg(c, "Each face comes up one sixth of the time. So add up one, two, three, four, five, and six, and divide by six.",
    "(1+2+3+4+5+6) / 6 writes on.")
seg(c, "That's twenty one divided by six. Three and a half.",
    "= 21/6 = 3.5 in violet; a marker at 3.5 on the face axis.", 1.0)
seg(c, "Notice something funny. You can never actually roll three and a half. The expected value doesn't have to be a possible result. It's a long run average.",
    "A balance beam with weights on 1–6 balances exactly at 3.5; tag 'balance point'.")
seg(c, "For two dice, the average total is three and a half plus three and a half. Seven. Right at the peak of our mountain.",
    "Mountain bar chart returns; balance triangle under 7; '3.5 + 3.5 = 7'.", 1.0)
seg(c, "Now the fair game. Each game, you win ten tokens one sixth of the time, because seven has a one sixth chance.",
    "Tree: 'roll 7' (1/6) → +10 tokens; 'not 7' (5/6) → 0 tokens.")
seg(c, "So on average, you win ten times one sixth. That's about one point six seven tokens per game.",
    "10 × 1/6 ≈ 1.67 tokens.")
seg(c, "But you pay two tokens every single time.",
    "Chip 'pay 2 every game' in red.")
seg(c, "So on average, you lose about one third of a token per game.",
    "1.67 − 2 ≈ −0.33 per game in violet.", 1.0)
seg(c, "Play once, and you might win ten tokens and feel brilliant. But play sixty games, and you'd expect to be down about twenty tokens.",
    "A line chart: x axis 'games played' 0–60, y axis 'tokens won or lost'; a simulated wiggly line drifting down; a dashed 'expected' line from 0 to −20.")
seg(c, "That's the quiet secret of almost every game at a fair. The expected value is a little bit in the stall's favour.",
    "The stall tag 'expected value favours the stall' in warn.", 1.0)
seg(c, "For the game to be fair, the expected win should equal the cost. Here, that would mean a price of ten sixths, about one point six seven tokens.",
    "Fair price: 10/6 ≈ 1.67 tokens; a level beam.")
seg(c, "Let's try one more. Your class sells one hundred raffle tickets, at one token each. There's one prize, worth fifty tokens.",
    "100 ticket squares on a 10 by 10 grid; one gold; chips 'ticket: 1 token' · 'prize: 50 tokens'.")
seg(c, "If you buy one ticket, your chance of winning is one in a hundred. So your expected win is fifty times one hundredth. Half a token.",
    "50 × 1/100 = 0.5 token.")
seg(c, "You paid one token, and you expect half a token back. So on average, you lose half a token per ticket.",
    "0.5 − 1 = −0.5 in violet.")
seg(c, "But that's fine for a raffle! The extra money goes to the class trip. Expected value doesn't tell you what to do. It tells you what it costs, on average.",
    "A school bus icon labelled 'class trip' collects the extra tokens.", 1.0)
seg(c, "Expected value is how you decide, using probability, whether something is worth it in the long run.",
    "Chip 'is it worth it in the long run?'.")
seg(c, "But remember, it's about the long run. A single game can go either way.",
    "Pocket icon glows again.", 1.0)

# ───────────── 13a. MEASURING ─────────────
c = "Measuring Instead of Counting"
seg(c, "So far, we've always counted outcomes. But some things can't be counted, because there are too many possibilities to list.",
    "A die (countable) next to a stopwatch (not countable) with '?'.")
seg(c, "Imagine a bus that comes exactly every ten minutes. You walk to the stop at a random moment, without checking the timetable.",
    "A timeline axis 'minutes' 0–10 between two bus icons.")
seg(c, "What's the chance you wait less than three minutes?",
    "Question chip 'wait less than 3 minutes?'.")
seg(c, "You could arrive at any moment in those ten minutes. Not just whole minutes, but any split second. There are endless possibilities.",
    "Dots sprinkle densely along the timeline.")
seg(c, "So instead of counting, we measure. The good arrival times are the last three minutes before the bus comes. That's a stretch three minutes long, out of ten.",
    "The segment from 7 to 10 on the axis turns aqua, labelled '3 minutes'; the whole axis labelled '10 minutes' in warn.")
seg(c, "Three out of ten. A probability of three tenths.",
    "3/10 in violet.", 1.0)
seg(c, "It's the same recipe, just with lengths instead of counts. The length you want, divided by the total length.",
    "Rule card: P = length you want / total length.")
seg(c, "And it works with areas too. Throw a dart at a square board, landing at a random spot. The board has a circle drawn on it that fills half the area.",
    "A square board on axes with equal scale; a circle shape covering half the area (illustration).")
seg(c, "Then the chance of landing inside the circle is one half. Area you want, divided by total area.",
    "Random dart dots: about half inside; 'area you want / total area = 1/2'.", 1.0)
seg(c, "Counting, measuring lengths, measuring areas. It's all the same idea. The part you want, out of the whole.",
    "Three icons merge into one card: 'the part you want, out of the whole'.", 0.8)

# ───────────── 13c. MORE DICE ─────────────
c = "More Dice, New Shapes"
seg(c, "Let's go back to our dice mountain, and ask one more question. What happens if we roll more dice?",
    "The two-dice triangle chart returns, totals 2–12.")
seg(c, "With one die, every total from one to six is equally likely. The chart is flat, like a table.",
    "Chart morphs to one die: six equal bars on axes 'total' 1–6, 'probability'.")
seg(c, "With two dice, it becomes a triangle. A pointy mountain, peaking at seven.",
    "Chart morphs to the triangle.")
seg(c, "With three dice, there are six times six times six, two hundred and sixteen outcomes. And the chart starts to look rounder, with the peak at ten and eleven.",
    "Chart morphs to three dice: totals 3–18, counts out of 216, peak at 10 and 11 (27 each).")
seg(c, "Roll more and more dice, and the shape keeps getting smoother and rounder. A soft hill with a peak in the middle and gentle tails at the edges.",
    "Charts for 5 and 10 dice (scaled), each smoother; label 'shape only' for the scaled ones.")
seg(c, "That shape has a famous name. The bell curve. And it appears again and again in nature, from people's heights to measurement errors.",
    "A smooth bell outline traces over the last chart; tag 'the bell curve'.", 1.2)
seg(c, "Why? Because when lots of small random things add together, extreme results need everything to go the same way, which is rare. Middle results can happen in many more ways.",
    "Ten dice: all sixes (one way) vs a middle total (many ways) shown as a tiny vs a big pile.")
seg(c, "It's the exact same reason seven beats twelve. Just with more dice.",
    "A small inset: 7 vs 12 from game night.", 0.8)

# ───────────── 13b. PRACTICE ROUND ─────────────
c = "Practice Round"
seg(c, "Time for a quick practice round. I'll ask a question, you pause the video if you like, and try it yourself. Then we'll check together.",
    "Title strip 'Practice round'; a pause icon.")
seg(c, "Question one. A jar has four green sweets and six yellow sweets. You pick one without looking. What's the chance it's green?",
    "Jar with 4 green and 6 yellow circles; 'Q1' tag; a 3-second countdown ring.", 3.0)
seg(c, "Count what you want, four green. Count everything, ten sweets. Four tenths, which is two fifths.",
    "4/10 = 2/5 in violet.", 1.0)
seg(c, "Question two. With two dice, what's the chance of a total of ten?",
    "Two-dice grid returns; 'Q2' tag; countdown ring.", 3.0)
seg(c, "Ten can be made by four and six, five and five, and six and four. Three squares. Three out of thirty six, which is one twelfth.",
    "Squares (4,6),(5,5),(6,4) aqua; 3/36 = 1/12.", 1.0)
seg(c, "Question three. So what's the chance of not getting a total of ten?",
    "'Q3' tag; countdown ring.", 3.0)
seg(c, "Flip it around. One minus one twelfth. Eleven twelfths.",
    "1 − 1/12 = 11/12 in violet.", 1.0)
seg(c, "Question four. You flip three coins. What's the chance of at least one head?",
    "Three coins; 'Q4' tag; countdown ring.", 3.0)
seg(c, "At least one means flip it around. The opposite is no heads at all, which is tails tails tails. One out of eight. So at least one head is seven eighths.",
    "Tree with 8 leaves; TTT grey; 1 − 1/8 = 7/8.", 1.0)
seg(c, "Question five. With two dice, what's the chance that both dice show an even number?",
    "Grid; 'Q5' tag; countdown ring.", 3.0)
seg(c, "Each die is even half the time, and the dice are independent. One half times one half is one quarter. On the grid, that's nine squares out of thirty six.",
    "Even-even squares (9) turn aqua; 1/2 × 1/2 = 1/4 = 9/36.", 1.0)
seg(c, "Question six. Your friend says the total of two dice is four. What's the chance it was a double?",
    "'Q6' tag; speech bubble 'total is 4'; countdown ring.", 3.0)
seg(c, "Shrink the world. A total of four comes from one and three, two and two, and three and one. Three squares. Only two and two is a double. One third.",
    "Squares (1,3),(2,2),(3,1) bright; (2,2) aqua; 1/3.", 1.0)
seg(c, "Question seven. A spinner has four equal parts showing one, two, three and six points. What's the expected number of points per spin?",
    "Spinner with four equal sectors 1, 2, 3, 6; 'Q7' tag; countdown ring.", 3.0)
seg(c, "Add them up, twelve, and divide by four. Three points per spin, on average.",
    "(1 + 2 + 3 + 6) / 4 = 3 in violet; balance beam balancing at 3.", 1.0)
seg(c, "Question eight. You draw one card from a well shuffled deck. What's the chance it's a red card, or a queen?",
    "Card grid; 'Q8' tag; countdown ring.", 3.0, sid="s398a")
seg(c, "Red cards are hearts and diamonds, twenty six of them. Queens, four. But two queens are red, so don't count them twice. Twenty six plus four minus two is twenty eight. Twenty eight out of fifty two, which is seven thirteenths.",
    "26 + 4 − 2 = 28; 28/52 = 7/13 in violet.", 1.0, sid="s398b")
seg(c, "Question nine. You roll one die three times. What's the chance of at least one six?",
    "Three die slots; 'Q9' tag; countdown ring.", 3.0, sid="s398c")
seg(c, "Flip it around. No sixes at all is five sixths, three times. One hundred and twenty five out of two hundred and sixteen. So at least one six is ninety one out of two hundred and sixteen. About forty two percent.",
    "1 − (5/6)³ = 1 − 125/216 = 91/216 ≈ 42% in violet.", 1.0, sid="s398d")
seg(c, "Question ten. A spinner is three quarters red. You spin it twice. What's the chance both spins land on red?",
    "Spinner 3/4 red; 'Q10' tag; countdown ring.", 3.0, sid="s398e")
seg(c, "The spins are independent, so multiply. Three quarters times three quarters is nine sixteenths. A little more than half.",
    "3/4 × 3/4 = 9/16 ≈ 56% in violet.", 1.0, sid="s398f")
seg(c, "How did you do? If you got even half of those ten, you're already thinking like a probability person.",
    "A score card '10 questions' with ticks.", 0.8)

# ───────────── 14. COMMON MISTAKES ─────────────
c = "Common Mistakes"
seg(c, "You now know more probability than most people. So let's protect you from the traps that catch almost everyone.",
    "Title strip 'the traps'; four empty red-bordered cards.")
seg(c, "Trap number one. I'm due for a win.",
    "Card 1: 'I'm due!' (red).")
seg(c, "A coin lands heads five times in a row. Surely tails is coming now, right?",
    "Five heads in a row on a strip; a sixth coin spins with '?'.")
seg(c, "No. The coin has no memory. The chance of tails on the next flip is still one half.",
    "The sixth coin: 1/2 heads, 1/2 tails; a 'no memory' brain icon crossed out.", 1.0)
seg(c, "Each flip is independent. The past doesn't push the future back into balance.",
    "Chip 'independent: the past doesn't push'.")
seg(c, "But wait, doesn't the law of large numbers say things even out? It does, but not by correcting. Over a huge number of flips, five extra heads just get diluted, like a drop of ink in an ocean.",
    "Line chart of share of heads: an early bump fades as flips grow; tag 'diluted, not corrected'.")
seg(c, "In fact, the sequence heads, heads, heads, heads, heads, tails, is exactly as likely as six heads in a row. One in sixty four each.",
    "Two strips HHHHHT and HHHHHH, each tagged 1/64.", 1.0)
seg(c, "This mistake has a name. The gambler's fallacy.",
    "Name tag 'the gambler's fallacy' on card 1.")
seg(c, "And here's a sneaky cousin of this trap. Judging from too few tries. A new player scores three shots out of three, and everyone says they never miss.",
    "Three basketball shots, all in; a speech bubble 'never misses!'.")
seg(c, "But three tries is a tiny sample. Remember the coin that gave seven heads out of ten. Small samples wobble. Wait for many tries before you trust a pattern.",
    "The 10-flip wobble from earlier returns briefly; chip 'small samples wobble'.", 1.0)
seg(c, "Trap number two. There are two outcomes, so it's fifty fifty.",
    "Card 2: 'two outcomes → 50/50?' (red).")
seg(c, "Will I win the lottery? Either I win, or I don't. Two outcomes. So fifty fifty?",
    "A ticket with 'win' / 'lose' and a grey '1/2?' label.")
seg(c, "Of course not. Two possible results doesn't mean two equally likely results. Remember the spinner.",
    "The spinner from earlier returns, 3/4 red, 1/4 blue.")
seg(c, "Before you count, always check that your outcomes are equally likely.",
    "Rule footnote glows: 'only if equally likely'.", 1.0)
seg(c, "Trap number three. Adding when you shouldn't.",
    "Card 3: 'adding chances blindly' (red).")
seg(c, "We saw it already. Four rolls at one sixth each is not four sixths, because the events overlap. If they can happen together, adding counts too much.",
    "The 4/6 vs 671/1296 comparison returns.")
seg(c, "A quick sanity check helps here. If your answer is more than one, or more than one hundred percent, something has gone wrong.",
    "A gauge 0–1 with a red zone beyond 1; tag 'never above 1'.", 1.0)
seg(c, "Trap number four. Flipping the given.",
    "Card 4: 'flipping the given' (red).")
seg(c, "The chance of A given B is not the same as the chance of B given A. Tall given basketball player is very different from basketball player given tall.",
    "The two basketball cards with '≠'.")
seg(c, "Whenever you hear a statement with given, if, or among, pause and ask, which group am I really looking at?",
    "Chip 'which group am I in?'.", 1.0)
seg(c, "And one bonus trap. Thinking that unlikely means impossible.",
    "Bonus card: 'unlikely = impossible?' (red).")
seg(c, "A one in a million event is very rare for you. But in a country of tens of millions of people, you'd expect it to happen to dozens of them.",
    "A grid of many tiny dots (illustration), a scattered few glowing; tag 'rare for one, common for many'.")
seg(c, "So when you hear about an amazing coincidence, remember, with enough people and enough chances, surprising things are expected.",
    "Chip 'enough chances → surprises are normal'.", 1.0)

# ───────────── 15. RECIPE ─────────────
c = "Recipe"
seg(c, "Let's put everything together. Here's your probability recipe.",
    "Recipe card title 'Your probability recipe'.")
seg(c, "Step one. List everything that could happen. Use a grid or a tree, and make sure every outcome is equally likely.",
    "① List all outcomes — 'grid or tree; equally likely'.")
seg(c, "Step two. Count the outcomes you want, and divide by all the outcomes.",
    "② Count and divide — 'wanted ÷ all'.")
seg(c, "Step three. For not, take it away from one.",
    "③ NOT — '1 − P(A)'.")
seg(c, "Step four. For or, add, and remove the overlap.",
    "④ OR — 'add, then remove the overlap'.")
seg(c, "Step five. For and, multiply along the path, using the updated chance.",
    "⑤ AND — 'multiply along the path'.")
seg(c, "Step six. For at least one, flip it around. One, minus the chance of none.",
    "⑥ AT LEAST ONE — '1 − P(none)'.")
seg(c, "Step seven. For a given, shrink the world first, then count.",
    "⑦ GIVEN — 'shrink the world, then count'.")
seg(c, "And step eight. Remember, probability describes the long run. Not the next single try.",
    "⑧ LONG RUN — 'patterns over many tries'.", 1.0)
seg(c, "Let's run the recipe one last time, on our game night question. Two dice, so six times six, thirty six equally likely outcomes.",
    "Mini grid 6 × 6 next to step ①.")
seg(c, "Twelve has one way, seven has six ways. Count and divide. One over thirty six, against six over thirty six.",
    "1/36 vs 6/36 beside step ②.")
seg(c, "And over many game nights, your friend will win this race about six times as often as you. Unless you change the rules.",
    "Step ⑧ glows; tally of many game nights 6 : 1.", 1.0)
seg(c, "You can't control the dice. But now, you can understand them.",
    "The recipe card dims; the two dice roll once more and land on 7.", 1.5)

# ───────────── 16. SUBSCRIBE (final chapter; owner: no next-time teaser) ─────────────
c = "Subscribe"
seg(c, "Look around your world, and notice how often you're quietly guessing the odds. The weather, the bus, a quiz, a game.",
    "Four everyday cards: cloud, bus stop, quiz sheet, dice; each stamped with a small '?'.", 0.6)
seg(c, "If this lesson made things clear for you, please subscribe to Math Lab TV, so we can keep building together.",
    "Logo + red SUBSCRIBE button; a cursor clicks it; it turns grey 'SUBSCRIBED ✓'; 'so we can keep building together' appears.", 0.8)
seg(c, "For more mathematics, explained simply and visually, subscribe, and I will see you in the next video.",
    "Logo holds; chip 'more math, explained simply and visually'; slow fade to the logo.", 2.0)

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
    md = [f"# Give Me One Hour and You'll FINALLY Understand PROBABILITY\n",
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
        print(f"  {k:22s} {v:5d} words ~{v/165:5.1f} min")
