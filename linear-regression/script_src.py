#!/usr/bin/env python3
"""Source of truth for the narration. Run to emit script.json + script.md.

Running example (used everywhere; every number checked in verify_numbers.py):
  Five recent house sales on one street (a small town; illustration numbers):
    size (sq ft) 1,000  1,500  2,000  2,500  3,000
    price ($k)     140    220    250    280    360
  Average house: 2,000 sq ft, $250k.  Best line: price = $50k + $100 per sq ft
  (x in hundreds of sq ft: y = 50 + 10x). Misses: -10, +20, 0, -20, +10 -> squared 100,400,0,400,100 -> score 1,000.
  Guesses: flat line at the average 26,000 · end-to-end line 1,250 · too steep 7,250.
  Formula: dx -10,-5,0,5,10 · dy -110,-30,0,30,110 · products sum 2,500 · dx^2 sum 250 · slope 10 · intercept 50.
  1,800 sq ft -> $230k.  0 sq ft -> $50k (meaningless).  10,000 sq ft -> $1.05M (extrapolation).
  Outlier: 3,000 sq ft sells for $560k -> slope 18 ($180/sq ft), 1,800 sq ft -> $254k.
Colour roles (one per concept, kept for the whole video):
  houses (data points) = ink dots · the line / answer = violet · misses (residuals) = orange
  squared errors (tiles) = aqua · the score (running total) = warn · mistakes = red · average house = blue
Connections (from `python3 channel/channel.py refs linear-regression`):
  callbacks: mean-vs-median (flat line at the mean; an outlier drags a mean; squares vs plain distances = mean vs median),
             standard-deviation (squaring distances, the same trick). No promise to pay off, no overlaps.
  teaser: gradient-descent. Seeds planted: loss-functions, regression-metrics, multiple-regression, logistic-regression.
"""
import json, pathlib, sys

SLUG = "linear-regression"            # id in channel/catalog.json
TARGET_MIN = (15, 20)         # from the skill arguments; words ≈ minutes × 150 (voice ~165 wpm + pauses)
D = 0.35                      # default pause between segments
S = []
N = [0]   # auto-id counter; once voiced, insert new lines with explicit ids (e.g. s017a) so old clips stay cached


def seg(chapter, text, visual, pause=D, sid=None):
    if sid is None:
        N[0] += 1; sid = f"s{N[0]:03d}"
    S.append(dict(id=sid, chapter=chapter, text=text, visual=visual, pause_after=pause))


# ───────────── 1. HOOK ─────────────
c = "The Fair Price"
seg(c, "Imagine you are about to sell your house. It is eighteen hundred square feet, on a quiet street in a small town.",
    "Line-art street draws on; one house highlights with a tag '1,800 sq ft'.")
seg(c, "You ask two agents what it is worth.",
    "Two agent cards slide in (simple Manim figures, no faces needed).")
seg(c, "The first says two hundred sixty thousand dollars. The second says two hundred thousand.",
    "Agent A bubble '$260k' (orange), agent B bubble '$200k' (blue); a gap bracket '$60k apart' between them.")
seg(c, "That is a sixty thousand dollar difference. Who do you believe?",
    "The '$60k apart' bracket pulses warn.", 1.0)
seg(c, "So you look at what actually sold. Five houses on your street, in the last year.",
    "Five sale cards drop in: 1,000 sq ft $140k · 1,500 $220k · 2,000 $250k · 2,500 $280k · 3,000 $360k.")
seg(c, "A thousand square feet sold for one hundred forty thousand. Three thousand square feet sold for three hundred sixty thousand. The rest are in between.",
    "Highlight the first and last cards in turn, then the middle three.")
seg(c, "Put them on a picture. Size along the bottom, price up the side. Every dot is one house.",
    "Cards fly onto x/y axes (size 0–3,500 sq ft, price $0–400k, numbered ticks); five ink dots land.")
seg(c, "Your eye sees it straight away. Bigger houses, higher prices. The dots lean upward, almost in a line.",
    "A soft dashed guide sweeps up through the cloud; label 'leans upward'.")
seg(c, "So grab a ruler and draw the line. Then read off eighteen hundred square feet.",
    "A violet ruler line lays across the dots; a vertical marker at 1,800 sq ft.")
seg(c, "But hand the same ruler to three people, and you get three different lines, and three different prices.",
    "Three ghost lines in different tilts; their readings at 1,800: $215k, $230k, $245k.", 0.8)
seg(c, "There has to be one best line. A line we can defend, with a number that says why it wins.",
    "Ghost lines fade; one violet line remains with a '?' score chip.")
seg(c, "Finding that line is called linear regression. By the end of this video, you will find it yourself, by hand, and the fair price will be two hundred thirty thousand dollars.",
    "Title card: 'LINEAR REGRESSION' (violet) with subtitle 'the complete beginner guide'; small chip '1,800 sq ft → $230k'.", 1.0)

# ───────────── 2. WELCOME (15–20 s) ─────────────
c = "Welcome"
seg(c, "Welcome to Math Lab TV. Where math is something you can see.",
    "Logo (violet rounded square with a green bell curve) + MATH LAB TV + tagline 'where math is something you can see'.", 0.7)
seg(c, "Today you will learn how to score any line, by measuring how far it misses each dot.",
    "Small logo top-right. Big ① (orange); mini scatter with orange vertical miss bars; caption 'score a line by its misses'.")
seg(c, "You will see the best line found, step by step, and what its slope and starting point really mean.",
    "Big ② (violet); mini line pivots and settles, slope triangle appears; caption 'find the best line, read it'.")
seg(c, "And you will learn when to trust its predictions, and when a line is quietly lying to you.",
    "Big ③ (red); mini line extends past the dots into a dashed red zone; caption 'when to trust it'.", 0.6)

# ───────────── 3. WHY IT MATTERS ─────────────
c = "Why It Matters"
seg(c, "Drawing a line through dots sounds like a school exercise. It is actually one of the most used tools in the world.",
    "The scatter shrinks to the left; a counter of icons starts filling on the right.")
seg(c, "Whenever one number tends to move with another, people want a line between them.",
    "Pairs appear as chips: 'size → price', 'ads → sales', 'hours studied → score', 'input size → run time'.")
seg(c, "Price from size. Sales from advertising. Exam scores from hours of study. How long a program runs from how much data it gets.",
    "Each chip gets its own tiny scatter with a line, one by one.")
seg(c, "And it is the very first model in machine learning. The same idea, misses, a score, and a search for the smallest score, is how much bigger models learn.",
    "The four mini scatters slide together into one box labelled 'machine learning, model number one'.", 0.8)
seg(c, "So let us build it from nothing. Back to our five houses.",
    "Mini scatters fade; the five-house scatter returns to centre.")

# ───────────── 4. MEASURING A MISS ─────────────
c = "Measuring a Miss"
seg(c, "Here is a line. Any line. We need a way to say how good it is.",
    "A violet line at a random tilt on the five-house axes.")
seg(c, "The line is a price guesser. For every size, it points to a price.",
    "A small cursor slides along the size axis; a dashed riser goes up to the line and across to a price readout.")
seg(c, "So for each house, we compare two prices. What the line guessed, and what the house really sold for.",
    "At x = 1,500: a hollow violet dot on the line ('guess') and the ink dot ('sold').")
seg(c, "The gap between them is the miss. Statisticians call it the residual, the bit that is left over.",
    "An orange vertical bar joins the two; defcard 'residual = sold − guessed'.", 0.8)
seg(c, "Notice the direction. The miss is measured straight up and down. Not the shortest distance to the line.",
    "Orange vertical bar stays; a grey perpendicular dash appears, then is crossed out in red.")
seg(c, "Why? Because up and down is price. We are guessing prices, so we measure our mistake in dollars.",
    "The orange bar gets a '$' label; the perpendicular dash would be measured in a mix of feet and dollars: label 'mixes sq ft and $'.")
seg(c, "The size of each house is not in doubt. We know it exactly. Only the price is being guessed.",
    "Size ticks glow ink ('known'); price axis glows orange ('guessed').", 0.6)
seg(c, "There is a different method that uses the shortest, slanted distance, for when both numbers are uncertain. But that is a different tool, for a different job.",
    "Small side note card: 'slanted distance → a different tool (both numbers uncertain)'.", 0.6)
seg(c, "Now draw the miss for every house. Some dots sit above the line, and their miss is positive.",
    "Five orange bars appear; the ones above the line get a '+' tag.")
seg(c, "Some sit below, and their miss is negative.",
    "Bars below get a '−' tag.")
seg(c, "A good line should have small misses. So let us add them up into one score.",
    "A warn score box 'total miss = ?' appears top-right.")

# ───────────── 5. SCORING A LINE ─────────────
c = "Scoring a Line"
seg(c, "Try the simplest line of all. A flat line at the average price, two hundred fifty thousand.",
    "Flat violet line at $250k; chip 'average price = $250k'.")
seg(c, "In our mean versus median video, the average was the single number that best stood in for a whole group. Here it is, as a line.",
    "Callback chip 'from: Mean vs Median'; the flat line glows.")
seg(c, "It ignores size completely. Every house gets the same guess. So it should score badly.",
    "Misses drawn: −110, −30, 0, +30, +110 (in $k), orange bars.")
seg(c, "Add up the misses. Minus one ten, minus thirty, zero, plus thirty, plus one ten. The total is zero.",
    "Running sum ticks in the score box: −110 → −140 → −140 → −110 → 0. Big '0'.", 1.0)
seg(c, "Zero. A perfect score, for a line that is plainly bad.",
    "The '0' flashes red; label 'perfect score?'.")
seg(c, "The pluses and minuses cancelled out. Big misses above hid big misses below. So a plain sum is useless.",
    "Upper bars and lower bars slide together and annihilate; red 'cancels out'.", 1.0)
seg(c, "We need every miss to count against the line, whatever its direction. The fix is the one from our standard deviation video. Square them.",
    "Callback chip 'from: Standard Deviation'; formula chip 'miss × miss'.")
seg(c, "Each orange miss becomes a square, with the miss as its side. Its area is the squared miss.",
    "Each orange bar rotates out into an aqua square tile with equal x/y scale; tile labels show areas.")
seg(c, "A square is never negative, so nothing can cancel.",
    "All tiles stack in a column; '+' signs only.")
seg(c, "And squaring does something else. It punishes big misses much more than small ones.",
    "Compare: one 20 miss → tile 400; two 10 misses → tiles 100 + 100 = 200.")
seg(c, "One miss of twenty costs four hundred. Two misses of ten cost only two hundred together. So the best line hates being far from any one house.",
    "The 400 tile is twice the area of the two 100 tiles side by side; label 'big misses cost more'.", 0.8)
seg(c, "Add up all the squares. That total is our score. It is called the sum of squared errors, and smaller is better.",
    "defcard 'score = sum of squared errors (add up every square). Smaller = better.'")
seg(c, "For the flat line, the score is twenty six thousand.",
    "Score box (warn) counts up to 26,000 (units: thousand-dollar misses, squared).", 0.8)
seg(c, "Now give the line some tilt. Here is a line through the cheapest and the most expensive house.",
    "Violet line rotates to pass through (1,000, 140) and (3,000, 360).")
seg(c, "It looks great. It passes right through three of the houses.",
    "Three dots ring aqua 'on the line'; two orange bars of 25 remain.")
seg(c, "Two misses of twenty five. Squared, that is six hundred twenty five each. The score is twelve fifty.",
    "Two 625 tiles; score box drops 26,000 → 1,250.", 0.8)
seg(c, "Much better. But is it the best? Let us go too far the other way, a line that is too steep.",
    "Line pivots steeper about the average house; misses grow at both ends.")
seg(c, "Its score jumps to seven thousand two hundred fifty. Too steep is bad, too flat is bad.",
    "Score box rises to 7,250 in red.", 0.6)
seg(c, "So let the line search for itself. It can do two things. It can pivot, to change its tilt. And it can slide, up and down.",
    "Two control icons: a pivot arrow around the line's centre, an up/down slide arrow.")
seg(c, "Watch the score as it pivots. The squares shrink, grow, and shrink again.",
    "Line pivots slowly through slopes; aqua tiles resize live; score ticks with it.")
seg(c, "Now it slides. Too high is worse, too low is worse.",
    "Line slides up and down; score ticks up both ways.")
seg(c, "And there is one spot where the score cannot get any smaller.",
    "Line settles; the tiles stop at 100, 400, 0, 400, 100.", 0.6)
seg(c, "The misses are minus ten, plus twenty, zero, minus twenty, and plus ten. Squared and added, the score is one thousand.",
    "Score box lands on 1,000 and glows violet: 'the smallest possible'.", 1.5)
seg(c, "That is it. The line with the smallest sum of squared errors is the least squares line, and finding it is linear regression.",
    "Defcard 'least squares line = the line with the smallest score'. Scoreboard: flat 26,000 · end-to-end 1,250 · too steep 7,250 · best 1,000.", 1.5)
seg(c, "Be honest about one thing. Squaring is a choice. If we added plain distances instead, the end to end line would actually win, fifty to sixty.",
    "Side card: 'plain distances: end-to-end 50 · least squares 60'.")
seg(c, "It is the same choice as mean versus median. Squared misses behave like the mean, and plain distances like the median. Squares are the standard, because they give one clean answer with a simple formula.",
    "Two chips: 'squares ↔ mean', 'plain distances ↔ median'; tick next to 'one clean formula'.", 0.8)

# ───────────── 6. THE FORMULA ─────────────
c = "The Formula"
seg(c, "We do not have to search by sliding, though. For a straight line, there is a formula that lands on the best line directly.",
    "Pivot and slide icons fade; a formula card frame appears.")
seg(c, "Step one. Find the average house. The average size is two thousand square feet, and the average price is two hundred fifty thousand.",
    "A blue cross-hair dot at (2,000, $250k) labelled 'average house'.")
seg(c, "Here is a lovely fact. The best line always passes right through the average house. So now we only need its tilt.",
    "The best line is drawn pinned through the blue dot; pin icon.", 0.8)
seg(c, "Step two. For each house, measure how far it is from the average, both in size and in price.",
    "Table builds: columns 'size − avg', 'price − avg'; rows −10, −5, 0, +5, +10 (hundred sq ft) and −110, −30, 0, +30, +110 ($k). Arrows on the chart from the blue dot to each house.")
seg(c, "To keep the numbers small, size is counted in hundreds of square feet, and price in thousands of dollars.",
    "Unit chips on the column heads: 'hundreds of sq ft', 'thousands of $'.")
seg(c, "Step three. Multiply each pair together, and add them all up.",
    "Third column 'product': 1,100 · 150 · 0 · 150 · 1,100; a Σ symbol with label 'Σ means add them all up'.")
seg(c, "Eleven hundred, plus one fifty, plus zero, plus one fifty, plus eleven hundred. That is two thousand five hundred.",
    "Running total 2,500 in warn.")
seg(c, "When a house is bigger than average and also pricier, the product is positive. That pulls the line upward.",
    "Rectangles drawn from the average house to each dot (equal scale) in aqua; top-right and bottom-left ones get '+'.")
seg(c, "Step four. Square each size distance, and add them up. One hundred, plus twenty five, plus zero, plus twenty five, plus one hundred. That is two hundred fifty.",
    "Fourth column 'size² ': 100 · 25 · 0 · 25 · 100; total 250.")
seg(c, "That second number is just how spread out the sizes are, a close cousin of the variance.",
    "Small chip 'spread of sizes (like variance)'.")
seg(c, "Step five. Divide. Two thousand five hundred over two hundred fifty is ten. That is the slope.",
    "Fraction 2,500 / 250 = 10 (LaTeX); slope chip violet.", 1.0)
seg(c, "Last step. Start at the average house and walk back to zero size. Two hundred fifty, minus ten times twenty, is fifty. That is the intercept.",
    "On chart: from the blue dot the line extends left to the price axis; arithmetic '250 − 10 × 20 = 50' in Inter.", 1.0)
seg(c, "Here is the whole recipe as symbols. Each one is just a word we already met.",
    "Formula card: b = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)²,  a = ȳ − b x̄ (LaTeX).")
seg(c, "x is size and y is price. x bar and y bar, with the little line on top, are the averages. And the big sigma means add them all up.",
    "Each symbol highlights with a plain-word label underneath: 'size', 'price', 'average size', 'average price', 'add them all up'.")
seg(c, "b is the slope, and a is the intercept. Ten and fifty. Exactly the line our search found.",
    "b = 10, a = 50 fill in; the slid-and-pivoted line from before overlays exactly; tick.", 1.0)

# ───────────── 7. READING THE LINE ─────────────
c = "Reading the Line"
seg(c, "So our line says, price equals fifty, plus ten times size, in thousands of dollars and hundreds of square feet.",
    "Equation card: 'price = 50 + 10 × size' with unit labels.")
seg(c, "In plain dollars, that is fifty thousand dollars, plus one hundred dollars for every square foot.",
    "Second line under it: '$50,000 + $100 per sq ft'.")
seg(c, "What does the slope mean? Ten means, every extra hundred square feet adds about ten thousand dollars to the price.",
    "Slope triangle on the line: run '+100 sq ft', rise '+$10k' (violet).", 0.8)
seg(c, "It is a rate. Dollars per square foot. It is the single most useful number on the line.",
    "Triangle slides along the line; same size everywhere: 'same rate everywhere'.")
seg(c, "And the intercept? It is where the line crosses zero size. Fifty thousand dollars, for a house with no floor at all.",
    "Line extended dashed to x = 0; dot at $50k with '0 sq ft?' label.")
seg(c, "That house does not exist. The intercept is often just a starting point that makes the line fit. Do not read too much into it.",
    "The 0 sq ft dot gets a red '?' and caption 'a starting point, not a real house'.", 0.8)
seg(c, "Now the question we started with. Your house is eighteen hundred square feet.",
    "Vertical marker at 1,800 sq ft.")
seg(c, "Fifty, plus ten times eighteen. That is fifty plus one eighty, which is two hundred thirty thousand dollars.",
    "Riser to the line, across to the axis: '$230k' in violet. Arithmetic '50 + 10 × 18 = 230'.", 1.5)
seg(c, "So the first agent was a bit high, and the second was too low. And now you can show why.",
    "Agent bubbles return: $260k (above), $200k (below); the line's $230k sits between them.")
seg(c, "One honest note. The real houses missed the line by up to twenty thousand. So treat two hundred thirty as a centre, give or take about twenty, not a promise.",
    "A soft violet band ±$20k around the line at 1,800; label 'give or take'.", 0.8)

# ───────────── 8. PREDICTION VS EXTRAPOLATION ─────────────
c = "Prediction vs Extrapolation"
seg(c, "Eighteen hundred square feet sits inside our data, between houses we have actually seen. Guessing there is called prediction, or interpolation.",
    "Aqua shaded zone from 1,000 to 3,000 sq ft: 'inside the data'; the 1,800 marker inside it.")
seg(c, "Now try a mansion. Ten thousand square feet. The line says one point zero five million dollars.",
    "Camera pans right; the line extends dashed to 10,000 sq ft; readout '$1.05M'.")
seg(c, "Maybe. But we have never seen a house that big on this street. We do not know if the straight line keeps going.",
    "Beyond 3,000 the zone turns red: 'no data here'.")
seg(c, "Prices might level off, or jump. The line has no idea. Guessing outside your data is called extrapolation, and it is risky.",
    "Two ghost curves leave the line beyond 3,000: one flattens, one rises; label 'illustration'.", 0.8)
seg(c, "It fails the other way too. A two hundred square foot shed, by this line, would cost seventy thousand dollars.",
    "Pan left: marker at 200 sq ft, readout '$70k'; shed outline with red '?'.")
seg(c, "A line is a local summary. It is only trusted where the dots are.",
    "Camera pulls back; aqua zone glows, red zones dim; caption 'trust it where the dots are'.", 1.0)

# ───────────── 9. A LINE IS NOT A CAUSE ─────────────
c = "A Line Is Not a Cause"
seg(c, "One more warning, and it is a big one. A line tells you that two things move together. It does not tell you why.",
    "Two chips 'move together' (tick) vs 'causes' (crossed out in red).")
seg(c, "Here, it feels obvious that more space makes a house cost more. But the line did not prove it. We knew it from common sense.",
    "Five-house scatter with the line; a 'common sense' tag, not 'the line says'.")
seg(c, "Lines can link things that have nothing to do with each other. Ice cream sales and sunburns rise and fall together, with a lovely straight line between them.",
    "New schematic scatter labelled 'illustration': ice cream sales vs sunburn cases, with a line.")
seg(c, "Ice cream does not cause sunburn. Hot sunny days cause both.",
    "A sun icon above both axes with arrows to each: 'hidden cause'.", 0.8)
seg(c, "The same thing can hide in house prices. Bigger houses are often newer, or in better neighbourhoods. Some of the hundred dollars per square foot may really belong to those.",
    "Back to houses: 'newer?' and 'better area?' chips with arrows into price.")
seg(c, "Separating those effects needs more than one input, and that is a later video on multiple regression.",
    "Chip 'later: multiple regression'.", 0.6)
seg(c, "So read the slope as, houses that are bigger tend to cost this much more. Not, adding a room will raise the price by exactly this.",
    "Two speech cards: green tick 'bigger houses tend to cost more' · red cross 'adding a room adds exactly $10k'.", 1.0)

# ───────────── 10. BIG PICTURE ─────────────
c = "Big Picture"
seg(c, "Now let us see where this exact idea shows up in the real world.",
    "Four domain tiles: ML, DS, Finance, CS.")
seg(c, "In machine learning, a linear regression is the first model you train. The five houses are the training data, and the line is the model.",
    "ML tile opens: dots labelled 'training data', line labelled 'model'.")
seg(c, "The sum of squared errors is called a loss. Training means finding the settings with the smallest loss, exactly like our line pivoting and sliding.",
    "Score box relabelled 'loss'; the pivot-and-slide replay in miniature.")
seg(c, "In data science, it is the trend line. How much do sales rise for each extra thousand dollars of advertising? The slope answers it.",
    "DS tile: schematic scatter 'ad spend → sales', slope triangle 'sales per $1k ads'; label 'illustration'.")
seg(c, "In finance, analysts plot a stock's daily moves against the whole market's moves. The slope of that line has a name, beta. A beta above one means the stock swings more than the market.",
    "Finance tile: schematic scatter 'market move % → stock move %', line slope labelled 'beta'; label 'illustration'.")
seg(c, "In computer science, engineers time a program on bigger and bigger inputs and fit a line. The slope is the cost per item, and it tells them how long a huge job will take.",
    "CS tile: scatter 'input size → run time', slope 'time per item'; red warning zone far right 'extrapolation'.")
seg(c, "But notice that last one is an extrapolation. Engineers check it, for the same reason we did with the mansion.",
    "Callback arrow to the mansion zone.", 0.8)
seg(c, "And that score we built, how much of the squared error the line removes, deserves its own video. Our line cut it from twenty six thousand to one thousand.",
    "Bar 26,000 vs bar 1,000; chip 'later: R squared, MSE and RMSE'.", 0.8)

# ───────────── 11. COMMON MISTAKES ─────────────
c = "Common Mistakes"
seg(c, "Here are the mistakes beginners make most often.",
    "Red header 'common mistakes'; three empty numbered slots.")
seg(c, "Mistake one. Forcing a straight line onto a curve.",
    "Slot 1 fills: '1  a line on a curve'.")
seg(c, "The formula will always give you a line, even when the dots bend. It never warns you. So always look at the picture first.",
    "Schematic curved cloud (label 'shape only'); a straight fit misses the middle; misses form an arch pattern.")
seg(c, "If the misses are all positive in the middle and negative at the ends, the line is the wrong shape.",
    "Misses coloured by sign show a + middle, − ends pattern; label 'pattern in the misses = wrong shape'.", 0.8)
seg(c, "Mistake two. Forgetting how much one odd point can pull the line.",
    "Slot 2 fills: '2  one point pulls the line'.")
seg(c, "Say the three thousand square foot house had a gold-plated kitchen and sold for five hundred sixty thousand instead.",
    "Back to the five houses; the 3,000 sq ft dot rises to $560k in red.")
seg(c, "Because misses are squared, that one house has huge pull. The slope jumps from one hundred to one hundred eighty dollars per square foot.",
    "Line swings steeper; slope chip $100 → $180 per sq ft; the big red square tile beside the outlier.")
seg(c, "And your fair price moves from two hundred thirty thousand to two hundred fifty four.",
    "At 1,800 sq ft: $230k ghost → $254k red.")
seg(c, "It is the same reason one billionaire drags up an average income. Check odd points before you trust the slope.",
    "Callback chip 'from: Mean vs Median'.", 0.8)
seg(c, "Mistake three. Trusting the line far outside the data, or reading it as cause. We just saw both. A line describes the dots you have, and nothing more.",
    "Slot 3 fills: '3  outside the data, or as cause'; mini mansion zone and ice cream icon.", 0.8)
seg(c, "And a bonus one. Measuring the misses slanted, instead of straight up and down. The miss is always in the units of what you are predicting.",
    "Bonus slot: 'measure misses vertically'; vertical orange bar vs crossed-out perpendicular.", 0.8)

# ───────────── 12. RECIPE ─────────────
c = "Recipe"
seg(c, "Let us put the whole method on one card.",
    "Recipe card frame, numbered steps appear one by one.")
seg(c, "One. Plot the dots, and check they look like a line.",
    "Step 1 bold 'Plot and look' + 'check the dots lean along a line'.")
seg(c, "Two. Measure each miss straight up and down, in the units you predict.",
    "Step 2 'Measure the misses' + 'vertical, in the units you predict'.")
seg(c, "Three. Square the misses and add them. That is the score.",
    "Step 3 'Square and add' + 'the sum of squared errors'.")
seg(c, "Four. Find the line with the smallest score. Slope from the formula, then the intercept from the average point.",
    "Step 4 'Find the best line' + 'slope = Σ(x−x̄)(y−ȳ) / Σ(x−x̄)², then intercept'.")
seg(c, "Five. Read the slope as a rate, and predict only where you have data.",
    "Step 5 'Read and predict' + 'slope = rate · stay inside the data'.", 0.8)
seg(c, "A line does not know the truth. It is just the one guess that misses least.",
    "Closing line in violet under the card.", 1.5)

# ───────────── 13. SUBSCRIBE (~12 s) ─────────────
c = "Subscribe"
seg(c, "Look around your world, and notice how often one number seems to climb with another, and ask whether it is a line, a curve, or just a coincidence.",
    "Four everyday cards: taxi fare vs distance, phone bill vs data, plant height vs weeks, rent vs size; stamped 'line, curve, or coincidence?'.", 0.6)
seg(c, "If this lesson made things clear for you, please subscribe to Math Lab TV, so we can keep building together.",
    "Logo + red SUBSCRIBE button; a cursor clicks it; it turns grey 'SUBSCRIBED ✓'; 'so we can keep building together' appears.", 0.8)

# ───────────── 14. NEXT TIME ─────────────
c = "Next Time"
seg(c, "But here's a puzzle for next time.", "Small logo top-centre; puzzle icon.")
seg(c, "With five houses and one straight line, we had a formula. But a modern AI model has millions of settings, and no formula at all.",
    "Our pivot-and-slide icon multiplies into a wall of thousands of tiny dials; 'next: gradient descent' chip under the logo.")
seg(c, "So how does it find its smallest score? It does what our line did. It feels which way is downhill, and takes a small step. That is gradient descent.",
    "A bowl-shaped score surface (illustration); a ball rolls down in small steps to the bottom.", 0.8)
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
    md = [f"# Linear Regression Explained: The Complete Beginner Guide\n",
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
