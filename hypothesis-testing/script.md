# Hypothesis Testing and p Values Without the Confusion

128 segments · 2592 words · est. 17.0 min (voice ≈165 wpm + 76 s pauses) · target 15–20 min


## The Coffee Coin  ·  161 words, ~59 s

- **s001** Every morning, you and a friend get coffee together. And every morning, you flip a coin to decide who pays.
  - *Visual:* STICKER café: two friends at a small table, one about to flip a coin (illustration). Two coffee-cup icons slide in.
- **s002** It's always your friend's coin. And your friend always calls heads.
  - *Visual:* A coin icon (blue rim) with 'H' face; chip 'their coin · they call heads'.
- **s003** After a month, you look back. Twenty flips. Heads came up fifteen times.
  - *Visual:* Tally board on axes (x: flip 1–20, y: H/T): 15 orange H dots, 5 blue T dots fill in one by one; counter '15 heads / 20'.
- **s004** So you bought fifteen of the coffees. Your friend bought just five. ⏸1.0s
  - *Visual:* Two stacks of cup icons on a count axis 0–15: 'you paid 15' (orange), 'they paid 5' (blue).
- **s005** The first few times, it seemed like luck. Coins are random, right? But by the end of the month, you start to wonder.
  - *Visual:* Calendar pages flip; the tally grows; a small thought bubble '…hmm' over the 'you' icon.
- **s006** So here's the question. Is that coin rigged? Or did your friend just get lucky?
  - *Visual:* Split screen: left 'rigged?' (orange coin with a weight), right 'just luck?' (blue coin with a shrug). Big '?'.
- **s007** Take a second, and decide what you think. ⏸1.5s
  - *Visual:* A slider between 'luck' and 'rigged' with a blinking cursor; small clock ticks.
- **s008** Your gut probably says something is off. But a fair coin can come up heads fifteen times. It's not impossible.
  - *Visual:* Coin spins; caption 'a fair coin CAN do this'.
- **s009** So how unusual is fifteen out of twenty, really? Unusual enough to call it rigged?
  - *Visual:* A number line 0–20 heads with ticks every 5; a warn pin drops at 15; the space beyond it shimmers.
- **s010** There is a tool built for exactly this question. It's called hypothesis testing, and the number it gives you is called a p value. ⏸1.0s
  - *Visual:* Title card: 'HYPOTHESIS TESTING' (aqua) with subtitle 'and p values, without the confusion'.

## Welcome  ·  65 words, ~24 s

- **s011** Welcome to Math Lab TV. Where math is something you can see. ⏸0.7s
  - *Visual:* Logo (violet rounded square with a green bell curve) + MATH LAB TV + tagline 'where math is something you can see'.
- **s012** Today you will learn how to test a claim, by asking what boring old chance would usually do.
  - *Visual:* Small logo top-right. Big ① (blue); mini bar chart of fair-coin results; caption 'test a claim against chance'.
- **s013** You will see exactly what a p value measures, as an area you can point at.
  - *Visual:* Big ② (aqua); the mini chart's right tail fills aqua; caption 'the p value is an area'.
- **s014** And you will see the two ways a test can be wrong, and the traps that fool even scientists. ⏸0.6s
  - *Visual:* Big ③ (red); two small warning cards 'false alarm' and 'missed it'; caption 'two ways to be wrong'.

## Why It Matters  ·  114 words, ~41 s

- **s015** In our Bayes video, we left you with a puzzle.
  - *Visual:* Chip 'from: Bayes' Theorem' slides in; the old teaser card reappears: 'p = 0.03'.
- **s016** Scientists often report a p value, like zero point zero three, and it gets described as a three percent chance that the result is a fluke.
  - *Visual:* Speech bubble beside the card: 'a 3% chance it's a fluke?' with a red question mark.
- **s017** We said that description flips the question. Today, we'll see what a p value really measures, and you'll see the flip with your own eyes. ⏸1.0s
  - *Visual:* The bubble flips over like a card, showing two arrows pointing opposite ways.
- **s018** And this matters, because p values are everywhere.
  - *Visual:* Three cards slide in, empty.
- **s019** A new medicine is tested against a sugar pill. A website tries a new button colour. A trader checks if a strategy beats luck.
  - *Visual:* Cards fill: pill vs sugar pill; two buttons A / B; a price line with a question mark.
- **s020** Every one of them asks the same thing as you and your friend. Is this a real effect, or just chance? ⏸1.0s
  - *Visual:* All three cards tilt toward one shared question card: 'real effect, or just chance?'.

## The Boring Explanation  ·  145 words, ~53 s

- **s021** Hypothesis testing starts in a strange place. Not with what you suspect, but with the most boring explanation there is.
  - *Visual:* Two boxes: an exciting orange box 'something is going on' and a plain blue box 'nothing is going on'; camera moves to the blue one.
- **s022** For our coin, the boring explanation is simple. The coin is fair. Heads and tails are equally likely, and fifteen heads was just luck.
  - *Visual:* Blue card 'the coin is fair: heads 1/2, tails 1/2'; a fair balance beam sits level under it.
- **s023** This boring explanation has a name. It's called the null hypothesis. Null just means nothing. Nothing special is going on.
  - *Visual:* Label 'NULL HYPOTHESIS' writes over the blue card; a definition card: 'null = nothing special is going on'.
- **s024** Your suspicion, that the coin favours heads, is called the alternative hypothesis.
  - *Visual:* Orange card 'ALTERNATIVE: the coin favours heads'.
- **s025** Here's the key idea. We don't try to prove the alternative directly. Instead, we pretend the boring explanation is true, and ask how surprising our result would be. ⏸1.0s
  - *Visual:* Arrow from the blue card to a thought bubble 'if the coin were fair… how surprising is 15?'.
- **s026** It's just like a courtroom. The defendant is presumed innocent. The prosecution has to show the evidence would be very hard to explain if they were innocent.
  - *Visual:* Courtroom line art: a judge's bench; 'presumed innocent' (blue) on one side, 'evidence' (warn) on the other.
- **s027** The null hypothesis is the innocent defendant. And our fifteen heads is the evidence. ⏸1.0s
  - *Visual:* Labels map over: 'innocent = fair coin' (blue), 'evidence = 15 heads' (warn).

## A Thousand Fair Coins  ·  384 words, ~140 s

- **s028** So, if the coin really is fair, what would twenty flips usually look like?
  - *Visual:* A single fair blue coin flips twenty times quickly; a counter ends at '11 heads' (illustration of one run).
- **s029** Let's find out with a thought experiment. Imagine a thousand friends, each with a perfectly fair coin, each flipping it twenty times.
  - *Visual:* A 40 × 25 grid of small blue coin dots appears on equal-scale axes: '1,000 friends, each flips a fair coin 20 times'.
- **s030** Each friend counts their heads. Then we stack them up by how many heads they got.
  - *Visual:* The dots fly from the grid into columns over an x-axis 'number of heads' 0–20 (ticks every 1, labels every 5); y-axis 'friends' 0–200, ticks every 50.
- **s031** This picture has a name. It's called a distribution. It just shows every possible result, and how often each one happens.
  - *Visual:* Definition card: 'distribution = every result + how often it happens'.
- **s032** Look at the shape. Most friends land near ten heads, the middle. About one hundred and seventy six of them get exactly ten.
  - *Visual:* The 10-heads column glows; label '≈ 176 friends' on top.
- **s033** Results further from ten get rarer and rarer, on both sides.
  - *Visual:* Arrows run down both slopes; outer bars fade to nearly zero.
- **s034** In our standard deviation video, we learned to measure spread. Here, the typical spread is about two heads either side of ten.
  - *Visual:* Chip 'from: Standard Deviation'; a bracket from 8 to 12 labelled 'typical spread ≈ 2.2 heads'.
- **s035** So, where does your friend's fifteen land? ⏸0.8s
  - *Visual:* The warn pin from the hook drops onto 15 on the x-axis.
- **s036** Way out here. More than two spreads from the middle. Only about fifteen of the thousand fair coins got exactly fifteen heads.
  - *Visual:* Camera zooms to the right tail; the 15 bar glows warn; label '≈ 15 friends'; brackets show two spreads from 10.
- **s037** But we don't just ask about exactly fifteen. We ask: how many fair coins did at least this well? Fifteen heads, or sixteen, or seventeen, all the way to twenty.
  - *Visual:* Bars 15 through 20 outline one by one, counting up.
- **s038** Let's fill in that tail. ⏸0.8s
  - *Visual:* The tail area from 15 to 20 fills aqua, bar by bar.
- **s039** About twenty one friends out of a thousand. That's roughly two in a hundred. ⏸1.0s
  - *Visual:* Counter '≈ 21 of 1,000' in aqua; then '≈ 2 in 100'.
- **s040** And that is the p value. Zero point zero two one. ⏸1.5s
  - *Visual:* Big aqua 'p ≈ 0.021' appears beside the tail; the filled tail pulses.
- **s041** In plain words: if the coin were fair, a result this extreme or more would happen only about two times in a hundred. ⏸1.0s
  - *Visual:* Sentence card, colour-coded: 'IF the coin were fair (blue), a result THIS EXTREME OR MORE (warn) happens ≈ 2 times in 100 (aqua)'.
- **s042** We don't actually need a thousand friends. There are about a million different ways twenty flips can come out, all equally likely for a fair coin.
  - *Visual:* Card '2²⁰ = 1,048,576 possible sequences'.
- **s043** Exactly twenty one thousand seven hundred of them have fifteen heads or more. Divide, and you get the same zero point zero two one.
  - *Visual:* Formula: p = 21,700 ÷ 1,048,576 ≈ 0.021, the 0.021 in aqua.
- **s044** Let's give it symbols. People write p equals the probability of data at least this extreme, given that the null hypothesis is true.
  - *Visual:* LaTeX: p = P( data this extreme or more | H₀ ), parts colour-coded.
- **s045** The capital P means probability. H zero is the null hypothesis. And the straight line means given, or assuming.
  - *Visual:* Symbol definitions appear under each part: 'P = probability', 'H₀ = null hypothesis (fair coin)', '| = given / assuming'.
- **s046** Remember that straight line. It's going to matter a lot. ⏸1.0s
  - *Visual:* The '|' glows warn and a small chip 'assuming the coin is fair' hangs from it.
- **s047** One honest detail. We only counted the heads side, because your suspicion was about heads. If you'd suspected the coin was off in either direction, you'd count both tails, and the p value would double to about zero point zero four.
  - *Visual:* Left tail 0–5 also fills (lighter aqua) for a moment; label 'two-sided: p ≈ 0.041'; then it clears.

## Drawing the Line  ·  243 words, ~88 s

- **s048** So, two in a hundred. Is that rare enough to call the coin rigged?
  - *Visual:* The chart returns; 'p ≈ 0.021' and a question mark.
- **s049** To decide, people choose a cut off before they look at the data. It's called the significance level, and it's written with the Greek letter alpha.
  - *Visual:* A violet vertical line slides along the x-axis; label 'significance level α (alpha)'.
- **s050** The most common choice is zero point zero five. One in twenty.
  - *Visual:* Chip 'α = 0.05 = 1 in 20'.
- **s051** The rule is: if the p value is smaller than alpha, we say the result is statistically significant, and we reject the boring explanation.
  - *Visual:* Rule card: 'p < α → reject the null' with p (aqua) and α (violet).
- **s052** Our p value is zero point zero two one. That's below zero point zero five. So at this line, we'd reject the idea that the coin is fair. ⏸1.0s
  - *Visual:* Meter 0–0.10 with the violet line at 0.05 and an aqua marker at 0.021 left of it; stamp 'reject the null'.
- **s053** But here's something most people never hear. That line is not a law of nature. Somebody chose it.
  - *Visual:* The violet line wobbles; label 'a choice, not a law'.
- **s054** The statistician Ronald Fisher suggested one in twenty about a hundred years ago, as a convenient rule of thumb. It stuck.
  - *Visual:* Card 'one in twenty: a 1920s rule of thumb' (no portrait).
- **s055** Other fields draw the line in very different places. Particle physicists want something like one in three and a half million before they announce a discovery.
  - *Visual:* Line-up of thresholds on a log meter: 'common: 1 in 20', 'stricter: 1 in 200', 'particle physics: ≈ 1 in 3.5 million'.
- **s056** And watch what the line does to our coin. Fifteen heads gives a p value of zero point zero two one. Significant.
  - *Visual:* Chart: tail from 15 filled aqua; p ≈ 0.021 left of the violet α line on the meter; tick ✓.
- **s057** Fourteen heads gives about zero point zero five eight. Not significant.
  - *Visual:* Tail from 14 fills; p ≈ 0.058 lands right of the line; label 'not significant'.
- **s058** One coin flip apart. The evidence barely changed, but the verdict flipped completely. ⏸1.5s
  - *Visual:* Side by side: '14 heads · p ≈ 0.058' vs '15 heads · p ≈ 0.021', with a tiny gap between them.
- **s059** So treat significant and not significant as a rough sign, not a magic switch. Always look at the p value itself, and at the size of the effect. ⏸1.0s
  - *Visual:* The switch icon fades; a dial 0–0.10 replaces it.

## What p Is Not  ·  217 words, ~79 s

- **s060** Now that we know what a p value is, let's be very clear about three things it is not.
  - *Visual:* Three red cards face down, numbered 1, 2, 3.
- **s061** Number one. It is not the chance that the coin is fair.
  - *Visual:* Card 1 flips: 'NOT the chance the null is true'.
- **s062** A p value of zero point zero two one does not mean a two percent chance the coin is fair, or a two percent chance it was a fluke.
  - *Visual:* '2% chance it's a fluke' appears and gets crossed out in red.
- **s063** Remember the straight line. The p value assumes the coin is fair, then asks about the data. It does not ask about the coin.
  - *Visual:* Two LaTeX lines: 'P(data | fair)' ✓ (aqua) above 'P(fair | data)' ✗ (red); arrows show they point opposite ways.
- **s064** This is the same flip we saw with Bayes. The chance a sick person tests positive is not the chance a positive person is sick. And the chance of this data from a fair coin is not the chance the coin is fair. ⏸1.5s
  - *Visual:* Chip 'from: Bayes' Theorem'; the old pair 'P(positive | sick) ≠ P(sick | positive)' slides in above the new pair.
- **s065** Number two. It is not a measure of how big the effect is.
  - *Visual:* Card 2 flips: 'NOT how big the effect is'.
- **s066** A tiny p value does not mean the coin is very rigged. We'll see why in a moment.
  - *Visual:* A small ruler icon with a question mark.
- **s067** Number three. A big p value does not prove the boring explanation.
  - *Visual:* Card 3 flips: 'NOT proof of nothing'.
- **s068** Suppose you flip a coin only five times, and get four heads. The p value is large. That doesn't show the coin is fair. It just shows five flips can't tell you much. ⏸1.0s
  - *Visual:* Mini chart for 5 flips with a wide tail; caption 'not enough data ≠ no effect'.
- **s069** In a courtroom, not guilty doesn't mean innocent. It means there wasn't enough evidence. ⏸1.0s
  - *Visual:* Gavel with 'not guilty' and a smaller line 'not proven innocent'.

## Two Ways to Be Wrong  ·  269 words, ~98 s

- **s070** Any test that makes a yes or no decision can be wrong in two different ways.
  - *Visual:* A 2 × 2 table on axes: columns 'coin really fair' (blue) / 'coin really rigged' (orange); rows 'we say rigged' / 'we say fair'.
- **s071** The first way: the coin is fair, but we call it rigged anyway. That's a false alarm. Statisticians call it a type one error.
  - *Visual:* Top-left cell turns red: 'TYPE I · false alarm'. Icon: innocent person behind bars.
- **s072** In the courtroom, that's convicting an innocent person.
  - *Visual:* Courtroom icon in the cell.
- **s073** The second way: the coin really is rigged, but we say it's fair. That's a miss. It's called a type two error.
  - *Visual:* Bottom-right cell turns red: 'TYPE II · miss'. Icon: a guilty person walking free.
- **s074** In the courtroom, that's letting a guilty person walk free. ⏸1.0s
  - *Visual:* Courtroom icon in the cell; the two correct cells turn green-grey 'correct'.
- **s075** Here's what alpha really controls. With our rule, call it rigged at fifteen heads or more, a fair coin gets falsely accused only about two times in a hundred.
  - *Visual:* Fair-coin chart (blue) with the aqua tail ≥15 labelled 'false alarm rate ≈ 2.1%'.
- **s075a** Notice that it's two in a hundred, not five. Twenty flips can only give whole numbers of heads, so the line can't sit exactly at one in twenty. It lands on the nearest safe step.
  - *Visual:* Staircase of tail areas: ≥14 → 5.8% (above the α line), ≥15 → 2.1% (below); arrow 'nearest safe step'.
- **s076** But what about misses? Suppose the coin really is rigged, and lands heads seventy percent of the time.
  - *Visual:* A second distribution (orange) for a 70%-heads coin slides in above the blue one, centred at 14 (illustration: a 70% coin).
- **s077** Then fifteen heads or more happens only about forty two percent of the time. So more than half the time, our test would miss it. ⏸1.5s
  - *Visual:* The orange bars from 15 up fill (≈ 42% 'caught'); bars below 15 hatch red '≈ 58% missed'.
- **s078** Twenty flips just isn't much evidence. Both pictures overlap a lot.
  - *Visual:* Camera pulls back to show the two distributions overlapping heavily.
- **s079** Now flip a hundred times instead. The two pictures pull apart. With a cut off at fifty nine heads, a fair coin is still falsely accused under five times in a hundred.
  - *Visual:* Both distributions redraw for 100 flips (x-axis 30–90, ticks every 10): blue centred at 50, orange at 70; violet line at 59.
- **s080** And the rigged coin gets caught about ninety nine times in a hundred. ⏸1.5s
  - *Visual:* The orange area right of 59 fills: 'caught ≈ 99%'.
- **s081** That's the trade off. A stricter line means fewer false alarms but more misses. And the main way to cut both at once is more data. ⏸1.0s
  - *Visual:* A seesaw: 'false alarms' vs 'misses'; a block labelled 'more data' lifts both sides down.

## Tiny p, Tiny Effect  ·  213 words, ~77 s

- **s082** Now let's come back to that second thing a p value is not. A measure of size.
  - *Visual:* Card 2 from 'What p Is Not' returns: 'NOT how big the effect is'.
- **s083** Imagine a different coin. It's almost fair. It lands heads fifty point two percent of the time. Just a hair more than half.
  - *Visual:* A coin with a microscopic weight; a bar '50.2% heads' next to '50% fair', nearly the same length.
- **s084** Over twenty flips, you'd never notice. But suppose a machine flips it a million times, and gets five hundred and two thousand heads.
  - *Visual:* A counter spins to '1,000,000 flips · 502,000 heads'.
- **s085** For a fair coin, the spread over a million flips is about five hundred heads. Two thousand extra heads is four spreads from the middle.
  - *Visual:* Fair-coin bell (blue) for a million flips, x-axis 498,000–502,000 ticks every 1,000; brackets of 500 each; warn pin at 502,000.
- **s086** The p value is about zero point zero zero zero zero three. Three in a hundred thousand. Incredibly significant. ⏸1.0s
  - *Visual:* Tiny aqua tail; 'p ≈ 0.00003' in big aqua; stamp 'highly significant'.
- **s087** But does it matter? If this coin decided your coffee, you'd pay for about two extra coffees in every thousand. ⏸1.5s
  - *Visual:* Your share of 1,000 coffees: 502 (this coin) vs 500 (a fair coin), almost identical; caption '≈ 2 extra coffees per 1,000 flips'.
- **s087a** And it works the other way too. A big effect can hide behind a big p value, when there's only a little data. That was our seventy percent coin, missed more than half the time in twenty flips. ⏸1.0s
  - *Visual:* The 20-flip overlap picture returns small, beside the million-flip picture: 'big effect, little data' vs 'tiny effect, huge data'.
- **s088** So the p value tells you whether an effect is probably there. It does not tell you whether it's big enough to care about.
  - *Visual:* Two dials: 'is it there?' (aqua, p value) and 'how big is it?' (orange, effect size).
- **s089** With enough data, almost any tiny difference becomes significant. That's why good reports show both the p value and the size of the effect. ⏸1.0s
  - *Visual:* Checklist card: '✓ p value  ✓ effect size'.

## Real World  ·  243 words, ~88 s

- **s090** So where will you actually meet this?
  - *Visual:* Four tiles: Machine Learning, Data Science, Finance, Computer Science.
- **s091** In data science, the classic one is an A B test. Half the visitors see the old button, half see the new one.
  - *Visual:* Data Science tile expands: two buttons A and B, each with a visitor counter.
- **s092** The null hypothesis is that the button makes no difference. If the new one gets more clicks, the p value asks: how often would a gap this big appear by chance alone?
  - *Visual:* Blue 'no difference' card; a small null distribution of 'gap between A and B' with the observed gap in its tail (illustration).
- **s093** In machine learning, you compare two models on the same test set. One scores a little higher. Is it really better, or did it just get a luckier set of examples?
  - *Visual:* Machine Learning tile: two model cards 'accuracy 91.2%' vs '91.6%'; a coin-flip icon between them.
- **s094** A hypothesis test, or a simple shuffle test, tells you whether that gap is bigger than chance usually makes.
  - *Visual:* Labels shuffle between the two models several times; a little distribution of shuffled gaps builds.
- **s094a** And when you fit a linear regression, every input gets its own p value. It asks: if this input truly had no effect, how surprising would the slope we found be?
  - *Visual:* Mini regression table (illustration): rows 'size', 'age', 'colour' with slope and p columns; the p column glows aqua.
- **s095** In finance, a trader backtests a strategy and it beats the market. But markets are noisy. The null hypothesis is that the strategy has no real edge, and the profit was luck.
  - *Visual:* Finance tile: a jagged price line with a profit arrow; blue card 'no real edge'.
- **s096** And try enough strategies, and some will look brilliant by pure luck. We'll come back to that in a moment.
  - *Visual:* Twenty little price lines; one glows gold; a red question mark beside it.
- **s097** In computer science, engineers test whether new code is really faster. Timing a program is noisy, just like a coin. So they run it many times, and test whether the speed up is more than noise. ⏸1.0s
  - *Visual:* CS tile: two run-time strips 'old code' vs 'new code' with scattered timing dots; a bracket 'speed-up or noise?'.
- **s098** Different worlds, same question as your coffee. Real effect, or just chance? ⏸1.0s
  - *Visual:* All four tiles shrink around the coffee coin in the centre.

## Common Mistakes  ·  264 words, ~96 s

- **s099** Let's finish with the most common mistakes, because they trip up beginners and experts alike.
  - *Visual:* Three red mistake cards slide in, face down.
- **s100** Mistake one: reading the p value as the chance the boring explanation is true.
  - *Visual:* Card 1 flips: 'p = chance the coin is fair?' (red).
- **s101** Here's how far apart those two numbers can be. Suppose that in your town, only one coin in a hundred is rigged, and a rigged one lands heads seventy percent of the time.
  - *Visual:* Illustration: a grid of 100 coins on equal-scale axes, 1 orange (rigged) and 99 blue (fair); chip 'illustration'.
- **s102** Then, just like in our Bayes theorem video, count. Among all the coins that would give fifteen heads or more, about eighty three percent are still fair coins. Only about seventeen percent are rigged.
  - *Visual:* Bayes-style split: of the coins that reach ≥15 heads, the blue block (fair) is far larger than the orange block (rigged); labels '≈ 83% fair' (blue) and '≈ 17% rigged' (orange).
- **s103** The p value was two percent. But the chance the coin is rigged is only about one in six. Same evidence, very different numbers. ⏸1.5s
  - *Visual:* Side by side: 'p ≈ 0.021' (aqua) vs 'chance rigged ≈ 17%' (violet), with '≠' between them.
- **s104** Mistake two: running lots of tests, and only reporting the one that worked.
  - *Visual:* Card 2 flips: 'testing many things, reporting one' (red).
- **s105** If you test twenty things that have no real effect, each at one in twenty, the chance that at least one looks significant is about sixty four percent.
  - *Visual:* Twenty fair-coin mini charts in a 5 × 4 grid; one by chance lands in its tail and glows; counter 'chance of ≥ 1 false alarm ≈ 64%'.
- **s105a** This has a name. It's called p hacking: trying analysis after analysis until something crosses the line.
  - *Visual:* Chip 'p-hacking' stamps on in red over the grid of twenty charts.
- **s106** That's how a lucky trading strategy, or a surprising headline, can come from pure noise. If you test many things, you need a stricter line. ⏸1.0s
  - *Visual:* The glowing chart is stamped 'lucky, not real'; the violet line moves further right.
- **s107** Mistake three: treating not significant as proof there's no effect.
  - *Visual:* Card 3 flips: 'not significant = no effect?' (red).
- **s108** Remember the seventy percent coin. With twenty flips, we missed it more than half the time. Not significant often just means not enough data. ⏸1.0s
  - *Visual:* The overlapping 20-flip pictures return; the '≈ 58% missed' area highlights.
- **s109** And a bonus mistake: choosing the line after you've seen the data. If you move alpha until your result is significant, the p value stops meaning anything. ⏸1.0s
  - *Visual:* The violet line slides right to sneak past a p value; a red 'no!' stamp. Caption 'choose α before you look'.

## Recipe  ·  154 words, ~56 s

- **s110** Let's turn all of that into a recipe you can use for any claim.
  - *Visual:* Recipe card frame unrolls: 'Hypothesis testing in five steps'.
- **s111** Step one: state the boring explanation. That's the null hypothesis. Nothing special is going on.
  - *Visual:* Item 1 (blue): 'State the null' + 'the boring explanation'.
- **s112** Step two: choose your line, before you look. Alpha, usually one in twenty.
  - *Visual:* Item 2 (violet): 'Choose α first' + 'usually 0.05'.
- **s113** Step three: picture what chance alone would do. Draw the distribution, assuming the null is true.
  - *Visual:* Item 3: 'Picture chance' + 'the distribution if the null is true'.
- **s114** Step four: find the tail. The p value is the share of that picture at least as extreme as your result.
  - *Visual:* Item 4 (aqua): 'Find the tail area' + 'p = share at least this extreme'.
- **s115** Step five: decide, and then ask how big. Compare p to alpha, and always report the size of the effect too. ⏸1.5s
  - *Visual:* Item 5 (orange): 'Decide, then size it' + 'p vs α, plus effect size'.
- **s116** For the coffee coin: fair coin as the null. Fifteen heads out of twenty. A p value of about two in a hundred. Below one in twenty, so we'd call it suspicious, and keep flipping to be sure. ⏸1.0s
  - *Visual:* Summary strip: 'H₀ fair · 15 of 20 heads · p ≈ 0.021 < 0.05 → suspicious, collect more data'.
- **s117** A p value doesn't tell you what's true. It tells you how surprised chance would be. ⏸2.0s
  - *Visual:* Closing line types on in aqua, centred.

## Subscribe  ·  36 words, ~13 s

- **s118** Look around your world, and notice how often a lucky streak gets mistaken for a pattern. ⏸0.6s
  - *Visual:* Four everyday cards: a sports winning streak, a 'hot' slot machine, a stock that doubled, a lucky shirt; each stamped 'real, or chance?'.
- **s119** If this lesson made things clear for you, please subscribe to Math Lab TV, so we can keep building together. ⏸0.8s
  - *Visual:* Logo + red SUBSCRIBE button; a cursor clicks it; it turns grey 'SUBSCRIBED ✓'; 'so we can keep building together' appears.

## Next Time  ·  84 words, ~31 s

- **s120** But here's a puzzle for next time.
  - *Visual:* Small logo top-centre; a puzzle-piece icon draws on.
- **s121** In a courtroom, an expert says there's only a one in a million chance that an innocent person would match the evidence.
  - *Visual:* Courtroom line art; a card 'chance an innocent person matches: 1 in 1,000,000'.
- **s122** So the jury thinks there's a one in a million chance the defendant is innocent. Real cases have gone exactly this way.
  - *Visual:* Speech bubble 'so 1 in a million they're innocent?' with a red question mark.
- **s123** It's the very same flip we saw today. Next time, we'll see why it's called the prosecutor's fallacy, and why smart people fall for it.
  - *Visual:* The 'P(data | innocent)' vs 'P(innocent | data)' pair flips; chip 'next: the prosecutor's fallacy' under the logo.
- **s124** I will see you in the next video. ⏸2.0s
  - *Visual:* Logo + next chip hold.
