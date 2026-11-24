# Math Lab TV: how videos are made in this repo

Math Lab TV is a YouTube channel of math explainers for people who are NOT good at math.
Claude makes every video end to end: script → voice-over → Manim video → YouTube package.

**This repository is the whole Math Lab TV channel** (`nsdcoding/math-lab-tv`, home branch `main`). The owner's
other channels live in other repositories (e.g. `nsdcoding/videos`); nothing from them (files, `gen.py`,
`motion-video-style`, styles, voices) is used here, and Math Lab TV work is never committed there.

**To make a video, type `/math-lab-video`.** The skill recommends the next topic from what has been made, you
pick it and give the duration, and it does the rest (full prompt in its SKILL.md).

## Start here: the channel tracker (`channel/`)

| file | what it is |
|---|---|
| `channel/catalog.json` | **source of truth**: all 96 planned videos in 9 series, their status, what each must cover, the planned visual, and how the videos connect (`builds_on`, `related`, `overlaps`), plus production details of every finished video |
| `channel/README.md` | the tracker as a page (generated: `python3 channel/channel.py render`; never edit by hand) |
| `channel/youtube-links.txt` | the owner pastes `slug = URL` here after uploading; a line there = published |
| `.claude/skills/math-lab-video/SKILL.md` | the owner's standing production prompt (structure, checklists, checkpoints, style). Follow it for every video |
| `channel/lesson-lab/<slug>/` | older draft scripts from the Lesson Lab app (reference only) |
| `channel/channel.py` | `status`, `show`, `refs`, `next`, `set`, `link`, `desc-block`, `render` |

## Workflow for every new video

1. **Recommend the topic**: `python3 channel/channel.py recommend 3`, the owner picks; then
   ask for the duration.
2. **Read its connections**: `python3 channel/channel.py refs <slug>` and `show <slug>`.
   - `callbacks`: finished videos to reference on screen and in the narration
     (e.g. "In our mean versus median video, we saw…"). Use 1–3 natural callbacks, never a list.
   - `promised_by`: a video whose ending teased this one. Open by paying off that promise.
   - `overlaps`: a related video made from a different angle. Use a **different running example**
     (check that video's `production.running_example`) and refer to it rather than repeating it.
   - `prerequisites_not_made`: give a 1–2 sentence intuition instead of assuming it.
   - `tease_next`: default topic for the NEXT TIME teaser. Confirm it at checkpoint 1.
   - The topic's own `covers` and `visual` in the catalog are the beats and picture the owner planned.
3. Run `.claude/skills/math-lab-video/scripts/new_video.py --slug <slug> --minutes <lo-hi>` (creates
   `<slug>/` from the template, writes BRIEF.md, sets the topic in-production), then follow the
   skill's SKILL.md exactly (both ⏸ checkpoints). `bayes-theorem/` is the newest complete example.
4. **Description**: `package.py` must include `channel.desc_block(...)` (see `bayes-theorem/package.py`):
   links to connected videos that are live, and the next video.
5. **When the final video is done**, fill the topic's `production` record in `catalog.json`
   (folder, branch, length, video, package, youtube_title, running_example, hook, callbacks,
   teaser_next), run `set <slug> produced`, then `render`, and commit.
6. **When the owner says a video is uploaded and sends its YouTube link** (in chat, any wording), do all of this
   without being asked again:
   - `python3 channel/channel.py link <slug> <url>`: writes `channel/youtube-links.txt`, marks it published,
     re-renders `channel/README.md`, and re-runs **every** video's `package.py` (`refresh`), so every
     description's 📺 Related videos / 🎓 More from Math Lab TV block carries every live link.
   - If any `package.py` fails (e.g. manim missing in a fresh container), install per the skill's setup.md and
     run `python3 channel/channel.py refresh`.
   - Commit and push, then tell the owner which already-live videos got a new description, with the text
     ready to paste into YouTube Studio.
   - Videos finished on other session branches must be merged into the working branch first (see "Keep one
     tracker" below), or their links and descriptions are missed.

**Keep one tracker.** Each session starts from `main`. If a finished video is missing from the tracker, look
for it on other `claude/*` branches (`git ls-tree -d --name-only origin/<branch>`) and merge those branches in.
Ask the owner to merge the working branch into `main` (pull request) after each video so the next session
starts up to date.

## Owner preferences (keep these)

- **Images: Manim/SVG first.** Gemini 2.5 Flash Image ("Nano Banana") is allowed only through the skill's
  `scripts/sticker.py`, only where Manim is not enough (relatable people, real-world objects, recurring
  characters), and only for images listed in the visual plan the owner approves at checkpoint 1. Never for
  numbers, charts, formulas or text, and never outside that workflow without asking.
- Voice: Google Cloud TTS `en-US-Chirp3-HD-Zubenelgenubi`. Credentials: `GCP_SA_KEY_B64`.
- Text must never touch frame edges or box borders; the overlap checker in `common.py` enforces it.
- Thumbnails: keyword headline (e.g. "BAYES' THEOREM / EXPLAINED VISUALLY"), the key formula, a real
  diagram from the running example, where viewers will use it (ML, DS, Finance, CS), and an
  "Explained in X minutes" badge; bottom-right corner clear; readable at 320×180.
- Commit and push milestones to the session's working branch; open a pull request into `main` when the
  owner asks. Never commit Math Lab TV work to another channel's repository.
