# Linear Regression Explained: The Complete Beginner Guide

137 segments · 2761 words · est. 18.0 min (voice ≈165 wpm + 74 s pauses) · target 15–20 min


## The Fair Price  ·  216 words, ~79 s

- **s001** Imagine you are about to sell your house. It is eighteen hundred square feet, on a quiet street in a small town.
  - *Visual:* Line-art street draws on; one house highlights with a tag '1,800 sq ft'.
- **s002** You ask two agents what it is worth.
  - *Visual:* Two agent cards slide in (simple Manim figures, no faces needed).
- **s003** The first says two hundred sixty thousand dollars. The second says two hundred thousand.
  - *Visual:* Agent A bubble '$260k' (orange), agent B bubble '$200k' (blue); a gap bracket '$60k apart' between them.
- **s004** That is a sixty thousand dollar difference. Who do you believe? ⏸1.0s
  - *Visual:* The '$60k apart' bracket pulses warn.
- **s005** So you look at what actually sold. Five houses on your street, in the last year.
  - *Visual:* Five sale cards drop in: 1,000 sq ft $140k · 1,500 $220k · 2,000 $250k · 2,500 $280k · 3,000 $360k.
- **s006** A thousand square feet sold for one hundred forty thousand. Three thousand square feet sold for three hundred sixty thousand. The rest are in between.
  - *Visual:* Highlight the first and last cards in turn, then the middle three.
- **s007** Put them on a picture. Size along the bottom, price up the side. Every dot is one house.
  - *Visual:* Cards fly onto x/y axes (size 0–3,500 sq ft, price $0–400k, numbered ticks); five ink dots land.
- **s008** Your eye sees it straight away. Bigger houses, higher prices. The dots lean upward, almost in a line.
  - *Visual:* A soft dashed guide sweeps up through the cloud; label 'leans upward'.
- **s009** So grab a ruler and draw the line. Then read off eighteen hundred square feet.
  - *Visual:* A violet ruler line lays across the dots; a vertical marker at 1,800 sq ft.
- **s010** But hand the same ruler to three people, and you get three different lines, and three different prices. ⏸0.8s
  - *Visual:* Three ghost lines in different tilts; their readings at 1,800: $215k, $230k, $245k.
- **s011** There has to be one best line. A line we can defend, with a number that says why it wins.
  - *Visual:* Ghost lines fade; one violet line remains with a '?' score chip.
- **s012** Finding that line is called linear regression. By the end of this video, you will find it yourself, by hand, and the fair price will be two hundred thirty thousand dollars. ⏸1.0s
  - *Visual:* Title card: 'LINEAR REGRESSION' (violet) with subtitle 'the complete beginner guide'; small chip '1,800 sq ft → $230k'.

## Welcome  ·  66 words, ~24 s

- **s013** Welcome to Math Lab TV. Where math is something you can see. ⏸0.7s
  - *Visual:* Logo (violet rounded square with a green bell curve) + MATH LAB TV + tagline 'where math is something you can see'.
- **s014** Today you will learn how to score any line, by measuring how far it misses each dot.
  - *Visual:* Small logo top-right. Big ① (orange); mini scatter with orange vertical miss bars; caption 'score a line by its misses'.
- **s015** You will see the best line found, step by step, and what its slope and starting point really mean.
  - *Visual:* Big ② (violet); mini line pivots and settles, slope triangle appears; caption 'find the best line, read it'.
- **s016** And you will learn when to trust its predictions, and when a line is quietly lying to you. ⏸0.6s
  - *Visual:* Big ③ (red); mini line extends past the dots into a dashed red zone; caption 'when to trust it'.

## Why It Matters  ·  127 words, ~46 s

- **s017** Drawing a line through dots sounds like a school exercise. It is actually one of the most used tools in the world.
  - *Visual:* The scatter shrinks to the left; a counter of icons starts filling on the right.
- **s018** Whenever one number tends to move with another, people want a line between them.
  - *Visual:* Pairs appear as chips: 'size → price', 'ads → sales', 'hours studied → score', 'input size → run time'.
- **s019** Price from size. Sales from advertising. Exam scores from hours of study. How long a program runs from how much data it gets.
  - *Visual:* Each chip gets its own tiny scatter with a line, one by one.
- **s021a** Every one of those lines answers the same kind of question. If this number goes up by one step, how much does that one tend to move? ⏸0.6s
  - *Visual:* Each mini scatter gets a tiny slope triangle: 'one step → how much more?'.
- **s020** And it is the very first model in machine learning. The same idea, misses, a score, and a search for the smallest score, is how much bigger models learn. ⏸0.8s
  - *Visual:* The four mini scatters slide together into one box labelled 'machine learning, model number one'.
- **s021** So let us build it from nothing. Back to our five houses.
  - *Visual:* Mini scatters fade; the five-house scatter returns to centre.

## Measuring a Miss  ·  193 words, ~70 s

- **s022** Here is a line. Any line. We need a way to say how good it is.
  - *Visual:* A violet line at a random tilt on the five-house axes.
- **s023** The line is a price guesser. For every size, it points to a price.
  - *Visual:* A small cursor slides along the size axis; a dashed riser goes up to the line and across to a price readout.
- **s024** So for each house, we compare two prices. What the line guessed, and what the house really sold for.
  - *Visual:* At x = 1,500: a hollow violet dot on the line ('guess') and the ink dot ('sold').
- **s025** The gap between them is the miss. Statisticians call it the residual, the bit that is left over. ⏸0.8s
  - *Visual:* An orange vertical bar joins the two; defcard 'residual = sold − guessed'.
- **s026** Notice the direction. The miss is measured straight up and down. Not the shortest distance to the line.
  - *Visual:* Orange vertical bar stays; a grey perpendicular dash appears, then is crossed out in red.
- **s027** Why? Because up and down is price. We are guessing prices, so we measure our mistake in dollars.
  - *Visual:* The orange bar gets a '$' label; the perpendicular dash would be measured in a mix of feet and dollars: label 'mixes sq ft and $'.
- **s028** The size of each house is not in doubt. We know it exactly. Only the price is being guessed. ⏸0.6s
  - *Visual:* Size ticks glow ink ('known'); price axis glows orange ('guessed').
- **s029** There is a different method that uses the shortest, slanted distance, for when both numbers are uncertain. But that is a different tool, for a different job. ⏸0.6s
  - *Visual:* Small side note card: 'slanted distance → a different tool (both numbers uncertain)'.
- **s030** Now draw the miss for every house. Some dots sit above the line, and their miss is positive.
  - *Visual:* Five orange bars appear; the ones above the line get a '+' tag.
- **s031** Others are below the line, and their miss is negative.
  - *Visual:* Bars below get a '−' tag.
- **s032** A good line should have small misses. So let us add them up into one score.
  - *Visual:* A warn score box 'total miss = ?' appears top-right.

## Scoring a Line  ·  549 words, ~200 s

- **s033** Try the simplest line of all. A flat line at the average price, two hundred fifty thousand.
  - *Visual:* Flat violet line at $250k; chip 'average price = $250k'.
- **s034** In our mean versus median video, the average was the single number that best stood in for a whole group. Here it is, as a line.
  - *Visual:* Callback chip 'from: Mean vs Median'; the flat line glows.
- **s035** It ignores size completely. Every house gets the same guess. So it should score badly.
  - *Visual:* Misses drawn: −110, −30, 0, +30, +110 (in $k), orange bars.
- **s033a** Let us look at the misses for this flat line, one house at a time. The smallest house is a hundred and ten thousand below it. The biggest is a hundred and ten thousand above.
  - *Visual:* Bars light in turn with labels −110 and +110; the middle three dim.
- **s036** Add up the misses. Minus one ten, minus thirty, zero, plus thirty, plus one ten. The total is zero. ⏸1.0s
  - *Visual:* Running sum ticks in the score box: −110 → −140 → −140 → −110 → 0. Big '0'.
- **s037** Zero. A perfect score, for a line that is plainly bad.
  - *Visual:* The '0' flashes red; label 'perfect score?'.
- **s038** The pluses and minuses cancelled out. The misses above wiped out the misses below. So a plain sum is useless. ⏸1.0s
  - *Visual:* Upper bars and lower bars slide together and annihilate; red 'cancels out'.
- **s039** We need every miss to count against the line, whatever its direction. The fix is the one from our standard deviation video. Square them.
  - *Visual:* Callback chip 'from: Standard Deviation'; formula chip 'miss × miss'.
- **s040** Each orange miss becomes a square, with the miss as its side. Its area is the squared miss.
  - *Visual:* Each orange bar rotates out into an aqua square tile with equal x/y scale; tile labels show areas.
- **s041** A square is never negative, so nothing can cancel.
  - *Visual:* All tiles stack in a column; '+' signs only.
- **s042** And squaring does something else. It punishes big misses much more than small ones.
  - *Visual:* Compare: one 20 miss → tile 400; two 10 misses → tiles 100 + 100 = 200.
- **s043** One miss of twenty costs four hundred. Two misses of ten cost only two hundred together. So the best line hates being far from any one house. ⏸0.8s
  - *Visual:* The 400 tile is twice the area of the two 100 tiles side by side; label 'big misses cost more'.
- **s044** Add up all the squares. That total is our score. It is called the sum of squared errors, and smaller is better.
  - *Visual:* defcard 'score = sum of squared errors (add up every square). Smaller = better.'
- **s045** For the flat line, the score is twenty six thousand. ⏸0.8s
  - *Visual:* Score box (warn) counts up to 26,000 (units: thousand-dollar misses, squared).
- **s046** Now give the line some tilt. Here is a line through the cheapest and the most expensive house.
  - *Visual:* Violet line rotates to pass through (1,000, 140) and (3,000, 360).
- **s047** It looks great. It passes right through three of the houses.
  - *Visual:* Three dots ring aqua 'on the line'; two orange bars of 25 remain.
- **s048** Two misses of twenty five. Squared, that is six hundred twenty five each. The score is twelve fifty. ⏸0.8s
  - *Visual:* Two 625 tiles; score box drops 26,000 → 1,250.
- **s049** Much better. But is it the best? Let us go too far the other way, a line that is too steep.
  - *Visual:* Line pivots steeper about the average house; misses grow at both ends.
- **s050** Its score jumps to seven thousand two hundred fifty. Too steep is bad, too flat is bad. ⏸0.6s
  - *Visual:* Score box rises to 7,250 in red.
- **s051** So let the line search for itself. It can do two things. It can pivot, to change its tilt. And it can slide, up and down.
  - *Visual:* Two control icons: a pivot arrow around the line's centre, an up/down slide arrow.
- **s052** Watch the score as it pivots. The squares shrink, grow, and shrink again.
  - *Visual:* Line pivots slowly through slopes; aqua tiles resize live; score ticks with it.
- **s053** Now it slides. Too high is worse, too low is worse.
  - *Visual:* Line slides up and down; score ticks up both ways.
- **s052a** Think of the score as a valley. Every possible line is a spot on the ground, and the score is how high that spot is. We are looking for the lowest point. ⏸0.6s
  - *Visual:* Small inset: a bowl-shaped curve 'score vs tilt' (shape only) with a dot sliding down to the bottom as the line pivots.
- **s054** And at one spot, the score cannot get any smaller. ⏸0.6s
  - *Visual:* Line settles; the tiles stop at 100, 400, 0, 400, 100.
- **s055** The misses are minus ten, plus twenty, zero, minus twenty, and plus ten. Squared and added, the score is one thousand. ⏸1.5s
  - *Visual:* Score box lands on 1,000 and glows violet: 'the smallest possible'.
- **s056** That is it. The line with the smallest sum of squared errors is the least squares line, and finding it is linear regression. ⏸1.5s
  - *Visual:* Defcard 'least squares line = the line with the smallest score'. Scoreboard: flat 26,000 · end-to-end 1,250 · too steep 7,250 · best 1,000.
- **s057** Be honest about one thing. Squaring is a choice. If we added plain distances instead, the end to end line would actually win, fifty to sixty.
  - *Visual:* Side card: 'plain distances: end-to-end 50 · least squares 60'.
- **s058** It is the same choice as mean versus median. Squared misses behave like the mean, and plain distances like the median. Squares are the standard, because they give one clean answer with a simple formula. ⏸0.8s
  - *Visual:* Two chips: 'squares ↔ mean', 'plain distances ↔ median'; tick next to 'one clean formula'.

## The Formula  ·  387 words, ~141 s

- **s059** We do not have to search by sliding, though. For a straight line, there is a formula that lands on the best line directly.
  - *Visual:* Pivot and slide icons fade; a formula card frame appears.
- **s060** Step one. Find the average house. The average size is two thousand square feet, and the average price is two hundred fifty thousand.
  - *Visual:* A blue cross-hair dot at (2,000, $250k) labelled 'average house'.
- **s061** Here is a lovely fact. The best line always passes right through the average house. So now we only need its tilt. ⏸0.8s
  - *Visual:* The best line is drawn pinned through the blue dot; pin icon.
- **s062** Step two. For each house, measure how far it is from the average, both in size and in price.
  - *Visual:* Table builds: columns 'size − avg', 'price − avg'; rows −10, −5, 0, +5, +10 (hundred sq ft) and −110, −30, 0, +30, +110 ($k). Arrows on the chart from the blue dot to each house.
- **s063** To keep the numbers small, size is counted in hundreds of square feet, and price in thousands of dollars.
  - *Visual:* Unit chips on the column heads: 'hundreds of sq ft', 'thousands of $'.
- **s064** Step three. Multiply each pair together, and add them all up.
  - *Visual:* Third column 'product': 1,100 · 150 · 0 · 150 · 1,100; a Σ symbol with label 'Σ means add them all up'.
- **s065** Eleven hundred, plus one fifty, plus zero, plus one fifty, plus eleven hundred. That is two thousand five hundred.
  - *Visual:* Running total 2,500 in warn.
- **s066** When a house is bigger than average and also pricier, the product is positive. That pulls the line upward.
  - *Visual:* Rectangles drawn from the average house to each dot (equal scale) in aqua; top-right and bottom-left ones get '+'.
- **s066a** Houses that are smaller than average and also cheaper give a positive product too. Minus times minus is plus. Only a house that breaks the pattern, bigger but cheaper, would pull the line down. ⏸0.6s
  - *Visual:* Bottom-left rectangle highlights '−10 × −110 = +1,100'; a ghost 'bigger but cheaper' dot appears in the bottom-right with a '−' rectangle (illustration), then fades.
- **s067** Step four. Square each size distance, and add them up. One hundred, plus twenty five, plus zero, plus twenty five, plus one hundred. That is two hundred fifty.
  - *Visual:* Fourth column 'size² ': 100 · 25 · 0 · 25 · 100; total 250.
- **s068** That second number is just how spread out the sizes are, a close cousin of the variance.
  - *Visual:* Small chip 'spread of sizes (like variance)'.
- **s069** Step five. Divide. Two thousand five hundred over two hundred fifty is ten. That is the slope. ⏸1.0s
  - *Visual:* Fraction 2,500 / 250 = 10 (LaTeX); slope chip violet.
- **s070** Last step. Start at the average house and walk back to zero size. Two hundred fifty, minus ten times twenty, is fifty. That is the intercept. ⏸1.0s
  - *Visual:* On chart: from the blue dot the line extends left to the price axis; arithmetic '250 − 10 × 20 = 50' in Inter.
- **s071a** Check it on the picture. Start at the average house, two thousand square feet and two hundred fifty thousand. Walk back two thousand square feet, twenty steps of a hundred, and the price drops ten thousand each step. Two hundred thousand gone. Fifty is left. ⏸0.8s
  - *Visual:* From the blue dot, twenty small slope steps walk down the line to x = 0; a counter '−$10k × 20 = −$200k'; lands at $50k.
- **s071** Here is the whole recipe as symbols. Each one is just a word we already met.
  - *Visual:* Formula card: b = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)²,  a = ȳ − b x̄ (LaTeX).
- **s072** x is size and y is price. x bar and y bar, with the little line on top, are the averages. And the big sigma means add them all up.
  - *Visual:* Each symbol highlights with a plain-word label underneath: 'size', 'price', 'average size', 'average price', 'add them all up'.
- **s073** b is the slope, and a is the intercept. Ten and fifty. Exactly the line our search found. ⏸1.0s
  - *Visual:* b = 10, a = 50 fill in; the slid-and-pivoted line from before overlays exactly; tick.

## Reading the Line  ·  261 words, ~95 s

- **s074** So our line says, price equals fifty, plus ten times size, in thousands of dollars and hundreds of square feet.
  - *Visual:* Equation card: 'price = 50 + 10 × size' with unit labels.
- **s075** In plain dollars, that is fifty thousand dollars, plus one hundred dollars for every square foot.
  - *Visual:* Second line under it: '$50,000 + $100 per sq ft'.
- **s076** What does the slope mean? Ten means, every extra hundred square feet adds about ten thousand dollars to the price. ⏸0.8s
  - *Visual:* Slope triangle on the line: run '+100 sq ft', rise '+$10k' (violet).
- **s077** It is a rate. Dollars per square foot. It is the single most useful number on the line.
  - *Visual:* Triangle slides along the line; same size everywhere: 'same rate everywhere'.
- **s078** And the intercept? It is where the line crosses zero size. Fifty thousand dollars, for a house with no floor at all.
  - *Visual:* Line extended dashed to x = 0; dot at $50k with '0 sq ft?' label.
- **s079** That house does not exist. The intercept is often just a starting point that makes the line fit. Do not read too much into it. ⏸0.8s
  - *Visual:* The 0 sq ft dot gets a red '?' and caption 'a starting point, not a real house'.
- **s080** Now the question we started with. Your house is eighteen hundred square feet.
  - *Visual:* Vertical marker at 1,800 sq ft.
- **s081** Fifty, plus ten times eighteen. That is fifty plus one eighty, which is two hundred thirty thousand dollars. ⏸1.5s
  - *Visual:* Riser to the line, across to the axis: '$230k' in violet. Arithmetic '50 + 10 × 18 = 230'.
- **s082** So the first agent was a bit high, and the second was too low. And now you can show why.
  - *Visual:* Agent bubbles return: $260k (above), $200k (below); the line's $230k sits between them.
- **s082a** Let us test the line on a house we already know. Twenty five hundred square feet. The line says fifty plus ten times twenty five, which is three hundred thousand.
  - *Visual:* Marker at 2,500 sq ft; line readout '$300k'.
- **s082b** It really sold for two hundred eighty thousand. So that house sold twenty thousand below the line. That is its miss, minus twenty, the same one we squared earlier. ⏸0.8s
  - *Visual:* Ink dot at $280k; orange bar −20 reappears with chip 'the same miss as before'.
- **s083** One honest note. The real houses missed the line by up to twenty thousand. So treat two hundred thirty as a centre, give or take about twenty, not a promise. ⏸0.8s
  - *Visual:* A soft violet band ±$20k around the line at 1,800; label 'give or take'.

## Prediction vs Extrapolation  ·  144 words, ~52 s

- **s084** Eighteen hundred square feet sits inside our data, between houses we have actually seen. Guessing there is called prediction, or interpolation.
  - *Visual:* Aqua shaded zone from 1,000 to 3,000 sq ft: 'inside the data'; the 1,800 marker inside it.
- **s085** Now try a mansion. Ten thousand square feet. The line says one point zero five million dollars.
  - *Visual:* Camera pans right; the line extends dashed to 10,000 sq ft; readout '$1.05M'.
- **s086** Maybe. But we have never seen a house that big on this street. We do not know if the straight line keeps going.
  - *Visual:* Beyond 3,000 the zone turns red: 'no data here'.
- **s087** Prices might level off, or jump. The line has no idea. Guessing outside your data is called extrapolation, and it is risky. ⏸0.8s
  - *Visual:* Two ghost curves leave the line beyond 3,000: one flattens, one rises; label 'illustration'.
- **s088** It goes wrong the other way too. A two hundred square foot shed, by this line, would cost seventy thousand dollars.
  - *Visual:* Pan left: marker at 200 sq ft, readout '$70k'; shed outline with red '?'.
- **s101a** There is a deeper reason too. The line only ever saw five ordinary houses on one street. It cannot know anything the data never showed it. ⏸0.6s
  - *Visual:* The five dots pulse; caption 'a model only knows its data'.
- **s089** A line is a local summary. It is only trusted where the dots are. ⏸1.0s
  - *Visual:* Camera pulls back; aqua zone glows, red zones dim; caption 'trust it where the dots are'.

## A Line Is Not a Cause  ·  161 words, ~59 s

- **s090** One more warning, and it is a big one. A line tells you that two things move together. It does not tell you why.
  - *Visual:* Two chips 'move together' (tick) vs 'causes' (crossed out in red).
- **s091** Here, it feels obvious that more space makes a house cost more. But the line did not prove it. We knew it from common sense.
  - *Visual:* Five-house scatter with the line; a 'common sense' tag, not 'the line says'.
- **s092** Lines can link things that have nothing to do with each other. Ice cream sales and sunburns rise and fall together, with a lovely straight line between them.
  - *Visual:* New schematic scatter labelled 'illustration': ice cream sales vs sunburn cases, with a line.
- **s093** Ice cream does not cause sunburn. Hot sunny days cause both. ⏸0.8s
  - *Visual:* A sun icon above both axes with arrows to each: 'hidden cause'.
- **s094** The same thing can hide in house prices. Bigger houses are often newer, or in better neighbourhoods. Some of the hundred dollars per square foot may really belong to those.
  - *Visual:* Back to houses: 'newer?' and 'better area?' chips with arrows into price.
- **s095** Separating those effects needs more than one input, and that is a later video on multiple regression. ⏸0.6s
  - *Visual:* Chip 'later: multiple regression'.
- **s096** So read the slope as, houses that are bigger tend to cost this much more. Not, adding a room will raise the price by exactly this. ⏸1.0s
  - *Visual:* Two speech cards: green tick 'bigger houses tend to cost more' · red cross 'adding a room adds exactly $10k'.

## Big Picture  ·  202 words, ~73 s

- **s097** Now let us see where this exact idea shows up in the real world.
  - *Visual:* Four domain tiles: ML, DS, Finance, CS.
- **s098** In machine learning, a linear regression is the first model you train. The five houses are the training data, and the line is the model.
  - *Visual:* ML tile opens: dots labelled 'training data', line labelled 'model'.
- **s099** The sum of squared errors is called a loss. Training means finding the settings with the smallest loss, exactly like our line pivoting and sliding.
  - *Visual:* Score box relabelled 'loss'; the pivot-and-slide replay in miniature.
- **s100** In data science, it is the trend line. How much do sales rise for each extra thousand dollars of advertising? The slope answers it.
  - *Visual:* DS tile: schematic scatter 'ad spend → sales', slope triangle 'sales per $1k ads'; label 'illustration'.
- **s101** In finance, analysts plot a stock's daily moves against the whole market's moves. The slope of that line has a name, beta. A beta above one means the stock swings more than the market.
  - *Visual:* Finance tile: schematic scatter 'market move % → stock move %', line slope labelled 'beta'; label 'illustration'.
- **s102** In computer science, engineers time a program on bigger and bigger inputs and fit a line. The slope is the cost per item, and it tells them how long a huge job will take.
  - *Visual:* CS tile: scatter 'input size → run time', slope 'time per item'; red warning zone far right 'extrapolation'.
- **s103** But notice that last one is an extrapolation. Engineers check it, for the same reason we did with the mansion. ⏸0.8s
  - *Visual:* Callback arrow to the mansion zone.
- **s104** Measuring how good a line is deserves its own video. For now, notice that our line cut the score from twenty six thousand to one thousand. ⏸0.8s
  - *Visual:* Bar 26,000 vs bar 1,000; chip 'later: R squared, MSE and RMSE'.

## Common Mistakes  ·  245 words, ~89 s

- **s105** Here are the mistakes beginners make most often.
  - *Visual:* Red header 'common mistakes'; three empty numbered slots.
- **s106** Mistake one. Forcing a straight line onto a curve.
  - *Visual:* Slot 1 fills: '1  a line on a curve'.
- **s107** The formula will always give you a line, even when the dots bend. It never warns you. So always look at the picture first.
  - *Visual:* Schematic curved cloud (label 'shape only'); a straight fit misses the middle; misses form an arch pattern.
- **s115a** Picture a scatter that rises steeply and then flattens out, like test scores against hours of study. A straight line cuts through the bend, too low in the middle and too high at both ends. ⏸0.6s
  - *Visual:* Schematic hours-of-study scatter rising then flattening (label 'shape only'); straight line overlays; middle region tagged 'line too low', ends 'line too high'.
- **s108** If the misses are all positive in the middle and negative at the ends, the line is the wrong shape. ⏸0.8s
  - *Visual:* Misses coloured by sign show a + middle, − ends pattern; label 'pattern in the misses = wrong shape'.
- **s109** Mistake two. Forgetting how much one odd point can pull the line.
  - *Visual:* Slot 2 fills: '2  one point pulls the line'.
- **s110** Say the three thousand square foot house had a gold-plated kitchen and sold for five hundred sixty thousand instead.
  - *Visual:* Back to the five houses; the 3,000 sq ft dot rises to $560k in red.
- **s111** Because every miss gets squared, that one house has a huge effect on the line. The slope jumps from one hundred to one hundred eighty dollars per square foot.
  - *Visual:* Line swings steeper; slope chip $100 → $180 per sq ft; the big red square tile beside the outlier.
- **s112** And your fair price moves from two hundred thirty thousand to two hundred fifty four.
  - *Visual:* At 1,800 sq ft: $230k ghost → $254k red.
- **s113** It is the same reason one billionaire drags up an average income. Check odd points before you trust the slope. ⏸0.8s
  - *Visual:* Callback chip 'from: Mean vs Median'.
- **s114** Mistake three. Trusting the line far outside the data, or reading it as cause. We just saw both. A line describes the dots you have, and nothing more. ⏸0.8s
  - *Visual:* Slot 3 fills: '3  outside the data, or as cause'; mini mansion zone and ice cream icon.
- **s115** And a bonus one. Measuring the misses slanted, instead of straight up and down. The miss is always in the units of what you are predicting. ⏸0.8s
  - *Visual:* Bonus slot: 'measure misses vertically'; vertical orange bar vs crossed-out perpendicular.

## Recipe  ·  93 words, ~34 s

- **s116** Let us put the whole method on one card.
  - *Visual:* Recipe card frame, numbered steps appear one by one.
- **s117** One. Plot the dots, and check they look like a line.
  - *Visual:* Step 1 bold 'Plot and look' + 'check the dots lean along a line'.
- **s118** Two. Measure each miss straight up and down, in the units you predict.
  - *Visual:* Step 2 'Measure the misses' + 'vertical, in the units you predict'.
- **s119** Three. Square the misses and add them. That is the score.
  - *Visual:* Step 3 'Square and add' + 'the sum of squared errors'.
- **s120** Four. Find the line with the smallest score. Slope from the formula, then the intercept from the average point.
  - *Visual:* Step 4 'Find the best line' + 'slope = Σ(x−x̄)(y−ȳ) / Σ(x−x̄)², then intercept'.
- **s121** Five. Read the slope as a rate, and predict only where you have data. ⏸0.8s
  - *Visual:* Step 5 'Read and predict' + 'slope = rate · stay inside the data'.
- **s122** A line does not know the truth. It is just the one guess that misses least. ⏸1.5s
  - *Visual:* Closing line in violet under the card.

## Subscribe  ·  48 words, ~17 s

- **s123** Look around your world, and notice how often one number seems to climb with another, and ask whether it is a line, a curve, or just a coincidence. ⏸0.6s
  - *Visual:* Four everyday cards: taxi fare vs distance, phone bill vs data, plant height vs weeks, rent vs size; stamped 'line, curve, or coincidence?'.
- **s124** If this lesson made things clear for you, please subscribe to Math Lab TV, so we can keep building together. ⏸0.8s
  - *Visual:* Logo + red SUBSCRIBE button; a cursor clicks it; it turns grey 'SUBSCRIBED ✓'; 'so we can keep building together' appears.

## Next Time  ·  69 words, ~25 s

- **s125** But here's a puzzle for next time.
  - *Visual:* Small logo top-centre; puzzle icon.
- **s126** With five houses and one straight line, we had a formula. But a modern AI model has millions of settings, and no formula at all.
  - *Visual:* Our pivot-and-slide icon multiplies into a wall of thousands of tiny dials; 'next: gradient descent' chip under the logo.
- **s127** So how does it find its smallest score? It does what our line did. It feels which way is downhill, and takes a small step. That is gradient descent. ⏸0.8s
  - *Visual:* A bowl-shaped score surface (illustration); a ball rolls down in small steps to the bottom.
- **s128** I will see you in the next video. ⏸2.0s
  - *Visual:* Logo + next chip hold.
