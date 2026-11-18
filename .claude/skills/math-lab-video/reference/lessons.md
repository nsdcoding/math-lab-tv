# Lessons from earlier videos (read before building)

## Script
- Real voice speed is ~165 wpm: 2,450 words + 84 s of pauses came out at 15:12. Plan `minutes × 150` words.
- Ambiguous spoken words get mis-heard: "ninety sick" → "ninety-six", "the sick side" → "six side",
  a sentence-final number can be swallowed ("…, eight." → say "about eight percent."). Reword, re-voice.
- "Bayes" at the end of a sentence was heard as "bass"; respelling it "Bays" for the voice fixed it.
- Keep the welcome to 15–20 s: short preview sentences and 0.6–0.7 s pauses.
- Teasers become promises: record `teaser_next` so the next video pays it off.

## Audio
- Linear loudnorm can't reach −14 LUFS when peaks are high; an oversampled limiter at 0.35 (≈1% of samples)
  before loudnorm fixes it. AAC encoding adds ~0.3 dB of peak: master to −2.0 dBTP.
- To change only the audio of a finished video, remux: `ffmpeg -i video.mp4 -i voiceover.wav -map 0:v -map 1:a
  -c:v copy -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest out.mp4`.

## Manim layout
- Frame is 14.22 × 8 units; subtitles cover y < −2.70; chapter label covers x < −3.26 and y > 2.98.
- Keep a fixed right-panel column (e.g. x ≥ 0.9–1.7) next to a left graph; left-align panel text to it.
- Axis titles above the y-axis collide with headers: use `y_vertical=True` or move the chart down.
- Labels next to curves: put them in empty regions under the curve with a thin leader line, or use a legend.
- When zooming into a grid, fade the axis labels (they become huge) and restore them after.
- Moving objects in flight across labels trigger the checker: `qa_mute` them for the flight.
- A Transform target placed while an updater runs lands in the wrong spot: clear updaters, transform, re-add.
- Rotating loop arrows sweep through labels: use ShowPassingFlash along the arrow instead.
- Recipe cards with many rows: a two-column layout (bold heading | one-line explanation) keeps text large.
- Build `title_card()` identically at the end of the hook and the start of the welcome scene (seamless cut).

## Thumbnails
- The owner wants: keyword headline + "EXPLAINED VISUALLY", the formula, a real diagram from the running
  example, where you'll use it (ML, DS, Finance, CS) with icons and one-line takeaways, the length badge.
- Never generate images without the owner's approval at checkpoint 1.

## Repo / GitHub
- Math Lab TV has its own repository, `nsdcoding/math-lab-tv` (home branch `main`). The owner's other channels
  live in other repositories; nothing from them is used here.
- Links to files must include the branch (`https://github.com/nsdcoding/math-lab-tv/blob/<branch>/<path>`).
- Files under 100 MB can be committed (a 15-min 1080p MP4 is ~60 MB).

## Motion and flicker (Hypothesis Testing)
- Never fade with an overshooting rate function (`ease_out_back`): opacity goes above 1 and an image blinks out
  for a few frames. Use `ease_out_cubic` for fades; overshoot is fine for pure motion (a needle, a scale).
- Animating mobjects that already sit inside a group with LaggedStart/AnimationGroup made Manim re-add them on
  top of everything (cards drew over their own labels). `Base` now skips AnimationGroup wrappers and restores the
  drawing order after every play.
- Idle actors must move enough to see: a 1.06 pulse over a second is invisible. motion_check compares frames 0.2 s
  apart; aim for pulses of 1.1+ and falls of a few units.
- Gauges: use `speedometer()` (zones, ticks, end labels, needle on a hub), not a bare arc and line.
- Images (stickers) placed partly off-frame are drawn in the wrong place for a frame or two. Never slide an
  image in from off-screen: FadeIn(img, shift=...) from just inside the frame.

## Prosecutor's Fallacy
- `Indicate(...)` on a pill, chip or card floods its filled box with the highlight colour for a few frames. Use
  `pulse()` on anything with a filled box; keep `Indicate` for bare text and dots.
- `group.animate.set_opacity(x)` also sets the fill of outline-only circles (rings) in the group; restoring to 1
  turns them into solid discs. Dim only the parts you mean (e.g. `p[0].animate.set_opacity(0.35)`).
- When inserting script lines after voicing, check the new segment's `chapter` in script.json: a line placed
  after a chapter's `c = ...` assignment silently joins the next chapter.
- A recipe card too wide for a side column: swap each explanation for the worked value in place instead.
