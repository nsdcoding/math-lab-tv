#!/usr/bin/env python3
"""Source of truth for the narration. Run to emit script.json + script.md.

DEMO video (not in channel/catalog.json): how a technical-trading explainer is made with the
Math Lab TV pipeline.

Running example (illustration, a made-up stock, prices in dollars; checked in verify_numbers.py):
  uptrend from 32 → left shoulder 60 → dip 52 → head 70 → dip 52 → right shoulder 61 → breaks 52
  → pulls back to 53 → falls toward 34.
  neckline = 52 (flat), height = 70 − 52 = 18, target = 52 − 18 = 34,
  stop above right shoulder = 61, risk = 61 − 52 = 9, reward = 52 − 34 = 18, reward : risk = 2 : 1.
Colour roles:
  price line = ink, shoulders = blue, head = orange, neckline = warn, target / measured move = violet,
  stop / mistakes = red, volume bars = aqua.
"""
import json, pathlib

SLUG = "head-and-shoulders"
TARGET_MIN = (4, 5)
D = 0.35
S = []
N = [0]


def seg(chapter, text, visual, pause=D, sid=None):
    if sid is None:
        N[0] += 1; sid = f"s{N[0]:03d}"
    S.append(dict(id=sid, chapter=chapter, text=text, visual=visual, pause_after=pause))


# ───────────── 1. HOOK ─────────────
c = "A Tired Uptrend"
seg(c, "Imagine a stock that has climbed for months, from thirty two dollars all the way to sixty.",
    "Price chart on real axes (day, price $); line draws up from 32 to 60.")
seg(c, "It dips, then pushes to a new high of seventy.", "Line dips to 52, climbs to 70; '70' tag pops.")
seg(c, "But the next push only reaches sixty one. It could not even make a new high.",
    "Line dips to 52, climbs to 61; dashed line from 70 shows the gap; 'lower high' chip.")
seg(c, "Then it falls through a level it had bounced off twice before.",
    "Two bounce points at 52 pulse; the line breaks below 52.", 0.8)
seg(c, "Traders have a name for this shape. It looks like a person: two shoulders and a head.",
    "Silhouette of a head and shoulders fades in over the three peaks.", 0.6)
seg(c, "The head and shoulders pattern.", "Title card: HEAD & SHOULDERS PATTERN / explained simply, with real numbers.", 1.0)

# ───────────── 2. WELCOME ─────────────
c = "Welcome"
seg(c, "Welcome to Math Lab TV. Where math is something you can see.",
    "Logo + MATH LAB TV + tagline.", 0.7)
seg(c, "Today you will learn how to spot the three peaks.", "① mini three-peak line; 'spot the three peaks'.")
seg(c, "You will see why the neckline is the line that matters.", "② mini chart with yellow neckline; 'the neckline'.")
seg(c, "And you will measure a price target with simple subtraction.", "③ 70 − 52 = 18 → 52 − 18 = 34.", 0.6)

# ───────────── 3. THE SHAPE ─────────────
c = "Three Peaks"
seg(c, "Let's slow down and read the chart one peak at a time.", "Full chart; camera zooms to the first peak.")
seg(c, "The first peak, at sixty, is the left shoulder. Buyers are still in control.",
    "Blue marker 'left shoulder 60'.")
seg(c, "The second peak, at seventy, is the head. It is the highest point of the whole move.",
    "Orange marker 'head 70'.")
seg(c, "The third peak, at sixty one, is the right shoulder. It is lower than the head.",
    "Blue marker 'right shoulder 61'; arrow 70 → 61 labelled 'lower high'.", 0.6)
seg(c, "That lower high is the first warning. Buyers tried again, and they ran out of strength.",
    "Up-arrows shrinking: +18, then +9.", 0.8)
seg(c, "The shoulders do not need to match exactly. Real charts are never that neat.",
    "Left and right shoulder bars side by side: 60 vs 61 'close enough'.")

# ───────────── 4. THE NECKLINE ─────────────
c = "The Neckline"
seg(c, "Now look at the two dips between the peaks. Both stopped at fifty two.",
    "Two dots at the troughs, labelled 52.")
seg(c, "Join them with a line, and you have the neckline.", "Yellow neckline drawn through both dips.", 0.6)
seg(c, "Here is the key idea. Until price closes below the neckline, there is no pattern yet.",
    "Line beyond the right shoulder fades to grey; 'not confirmed' chip.")
seg(c, "It is only a shape that might become one.", "Ghost path that bounces off 52 and goes back up.", 0.6)
seg(c, "When the price closes below fifty two, the pattern is confirmed.",
    "Line closes below 52; 'confirmed' chip turns yellow.", 0.8)
seg(c, "Volume often tells the same story. Trading is lighter on the right shoulder, then jumps on the break.",
    "Aqua volume bars under the chart: smaller at right shoulder, tall bar at the break.")
seg(c, "And sometimes the price comes back up to touch the neckline from below, before it falls away.",
    "Pullback to 53 marked 'retest'; old floor now acts as a ceiling.", 0.6)

# ───────────── 5. THE PRICE TARGET ─────────────
c = "The Price Target"
seg(c, "So how far might it fall? There is a simple rule of thumb.",
    "Chart; violet ruler appears.")
seg(c, "Measure the height of the head above the neckline.", "Vertical violet bracket from 52 to 70.")
seg(c, "Seventy minus fifty two is eighteen dollars.", "70 − 52 = 18 written beside the bracket.", 0.6)
seg(c, "Now copy that same eighteen down from the neckline.", "Bracket slides down below 52.")
seg(c, "Fifty two minus eighteen is thirty four. That is the price target.",
    "52 − 18 = 34; violet dashed target line at 34.", 1.0)
seg(c, "Traders also decide where they would be wrong. A common choice is just above the right shoulder, at sixty one.",
    "Red stop line at 61.")
seg(c, "Selling at the break, at fifty two, risks nine dollars to aim for eighteen.",
    "Red bar 9 (risk) vs violet bar 18 (reward).")
seg(c, "That is two dollars of possible reward for every dollar of risk.", "'2 : 1' badge.", 1.0)

# ───────────── 6. COMMON MISTAKES ─────────────
c = "Common Mistakes"
seg(c, "Three mistakes trip up beginners.", "Three cards appear.")
seg(c, "Mistake one: acting before the neckline breaks. Many right shoulders simply turn back up.",
    "Card 1, red: ghost path bounces off the neckline.")
seg(c, "Mistake two: finding the shape anywhere. It is a reversal pattern, so it needs an uptrend before it to reverse.",
    "Card 2: same shape inside a downtrend, crossed out.")
seg(c, "Mistake three: treating the target as a promise. It is a rule of thumb. Price can stop short, or overshoot.",
    "Card 3: target line with arrows above and below it.", 0.8)
seg(c, "And a bonus: flip the chart upside down, and you get the inverse head and shoulders, a possible bottom after a fall.",
    "Chart flips vertically; label 'inverse head and shoulders'.", 0.8)

# ───────────── 7. RECIPE ─────────────
c = "Recap"
seg(c, "Here is the whole recipe.", "Numbered card appears.")
seg(c, "One. Start with an uptrend.", "Step 1 lights up.")
seg(c, "Two. Find three peaks, with the head the highest.", "Step 2.")
seg(c, "Three. Draw the neckline through the two dips.", "Step 3.")
seg(c, "Four. Wait for a close below it.", "Step 4.")
seg(c, "Five. Measure the head, copy it down, and set where you would be wrong.", "Step 5.", 0.8)
seg(c, "A pattern is not a prediction. It is a way to plan your risk.", "Closing line in violet.", 1.2)

# ───────────── 8. SUBSCRIBE ─────────────
c = "Subscribe"
seg(c, "Look around your world, and notice how often a rally runs out of steam before it turns.",
    "Four cards: stock chart, house prices, a sports streak, a viral trend; stamp 'lower high?'.", 0.6)
seg(c, "If this lesson made things clear for you, please subscribe to Math Lab TV, so we can keep building together.",
    "Logo + SUBSCRIBE button clicked.", 0.8)

# ───────────── 9. NEXT TIME ─────────────
c = "Next Time"
seg(c, "But here's a puzzle for next time.", "Small logo top-centre; puzzle icon.")
seg(c, "What if the price makes only two peaks, at the same height? That is the double top.",
    "Mini chart with two equal peaks; 'next: double top' chip.")
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
    md = [f"# Head and Shoulders Pattern (demo)\n",
          f"{len(S)} segments · {words} words · est. {est:.1f} min · target {TARGET_MIN[0]}–{TARGET_MIN[1]} min\n"]
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
