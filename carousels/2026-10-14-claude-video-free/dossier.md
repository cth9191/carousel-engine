# Source dossier: Claude makes videos with code (for free)

**Date:** 2026-10-14 · **Angle (from Chase):** pilot pick from his own video; no extra angle given.

**Sources:**
- youtube · https://www.youtube.com/watch?v=rscb1DgJtNg · "Claude Now Does Video (FOR FREE) Thanks To JavaScript" · published 2026-10-06 · chapters 0:00 Claude + Javascript / 4:07 Level 1 Prompting / 7:19 Level 2 Tools + Looping / 9:56 Level 3 References / 11:43 Level 4 Skills / 13:39 Outro
  - Transcript: YouTube captions pulled with yt-dlp (kept in the author's private research folder, not included)
  - Video + frame sheets: downloaded source video and frame sheets (not included)
  - Source video description links to the skill (fixed before posting).
- repo · https://github.com/cth9191/animate · public, **691★ / 104 forks** (gh api, 2026-10-14) · created 10-04 · read from a local clone (README, `plugins/animate/skills/animate/SKILL.md`, `docs/styles.png`, `docs/storyboard.png`, `examples/history-of-ai/`)

## 1. One-line definition

*Claude Code can make a video by writing code: it draws every frame in JavaScript, then a free tool stitches the frames into an MP4.* It is not an AI video generator.

**Analogy:** a flipbook that Claude draws page by page (60 pages for every second), then binds into a movie.
(The video's own line: "Claude wrote a function. Give it a time, t, and it returns one picture.")

## 2. The pain (before)

- Today, a motion-graphics explainer, product demo or animated short means After Effects, Remotion or a paid AI video generator, plus the skill to drive them. [F1, illustrative]
- AI video generators can't give you exact text, and every revision is a reroll. [illustrative, Chase's framing: "This isn't an AI video generator."]

## 3. The outcome (after)

- One prompt (or one skill run) → an MP4 explainer, product demo or motion-graphics reel. [F2]
- Extra cost: **$0 in tools.** Playwright and FFmpeg are free and open source; it runs on the Claude plan you already pay for ("We just pay for it with usage"). Voice-over is optional (ElevenLabs or open-source TTS). [F3]
- Proof we can show: Chase's one-shot 3Blue1Brown-style explainer that explains its own pipeline (0:40–1:40); low/high/ultra showreels (Level 1); the currency→electricity reference recreation (Level 3); the skill's 7 style frames (`docs/styles.png`). [F4]

## 4. How it works (mechanism)

| Part | Plain-word definition | Shown by |
|---|---|---|
| Frame function | JavaScript code that draws one picture for a given moment `t` | the 3B1B explainer frames |
| Headless browser (Playwright) | an invisible Chrome that draws each frame, 60 per second | diagram |
| FFmpeg | free tool that stitches the frames (and sound) into an MP4 | diagram |
| Check loop | Claude pulls a contact sheet of frames, spots what's wrong, fixes the code, re-renders | contact sheet capture |

"Claude can't watch the video, but it can look at the frames, spot what's wrong, and fix the function." [F5, video ~1:20]

## 5. Setup / first step

- Easiest: hand Claude Code the repo URL (`github.com/cth9191/animate`), or install it as a plugin. It checks for and installs Playwright, FFmpeg and faster-whisper, and offers the ElevenLabs connector. [F6, video Level 4 + README]
- Requirements (README): Node 18+, Playwright with Chromium, ffmpeg on PATH; faster-whisper only for voice-over timing.
- First useful thing: ask for a **storyboard first**, approve the beats, then let it build. [F7]

## 6. Use cases (real ones)

1. A visual explainer: the one-shot 3B1B-style "how this works" video (in the video, ~0:40).
2. A motion-graphics showreel: the 15-second "show what an incredible motion designer you are" test at low/high/ultra effort (Level 1).
3. A reference-matched piece: the electricity-history video rebuilt from a currency video's composition (Level 3).
4. The skill's styles: cut paper, crosshatch ink, riso print, sketchbook, math (manim-style), pixel, isometric, or a new look matched from your references (README, `docs/styles.png`).

## 7. Value peak candidate

The verbatim on-screen prompt from Level 2 (hi-res frame at 8:56). It's titled "prompt → paste into Claude Code":

```
Make a 30-second animated explainer of how [TOPIC] works, 16:9.
Build it in JavaScript on a canvas, with a soundtrack generated in code,
and render it to an MP4 with Playwright and FFmpeg.
(optional) Here's my voice-over: voice.mp3. Time the visuals to it:
get word timestamps with Whisper and land each change on the words.
Before you call it done, use FFmpeg to pull a contact sheet,
look at it, fix what's wrong, re-render, and repeat.
```

Below it on screen: "Claude figures out the rest: renderFrame(t) · the score · frame-by-frame rendering · encoding".

Install, verbatim from the README (also on screen at 13:12):

```
/plugin marketplace add cth9191/animate
/plugin install animate@animate
```

Then: `/animate a 45-second history of the bicycle, cut paper` (README "Use" examples).

## 8. Objections / pitfalls

- **"Effort is the problem."** It usually isn't. Opus 5.5 took ~20 min on low, ~30 min on high and 8 hours on ultra code. Low and high were fine; ultra was best. It's mostly the prompt. [F8, Level 1]
- **Long renders.** A full video can take 20+ minutes, and the redo loop is where hours go. Storyboard first. [F7]
- **"Free" ≠ zero usage.** It uses your Claude plan's limits. [F3]
- The skill is a work in progress; PRs are welcome. [video, Level 4]

## 9. Chase's take

- "You don't need Remotion. You don't need After Effects. All you need is Claude Code and JavaScript." (0:00)
- "If you think your issue with these videos is an effort problem, it's probably not. It's probably just your prompts." (Level 1)
- "Simply asking for a storyboard before it creates the video is going to save you so much time." (Level 1)
- "There's no third-party AI image generator or AI video generator we need… and the quality is really high." (outro)

## 10. Demand + timing

- Published 2026-10-06; strong early views.
- Evergreen how-to with no launch day. Repo is 10 days old: 691★, 104 forks.
- Last carousel posted 10-03, on another topic. No same-format deck in the last 72 h.
- Hook on the broad outcome (videos, for free), not the craft (motion design).

## 11. Deliverable for the CTA

- Name: **the animate skill** (repo link + install line) · Exists? **yes**, public · Keyword: **ANIMATE** (new; the comment-to-DM automation needs wiring) or standing **AGENT** (generic, weaker)

## 12. Glossary

| Term | Plain definition |
|---|---|
| JavaScript | the coding language web pages run on |
| frame | one still picture; video plays 60 of them a second |
| Playwright / headless browser | a hidden copy of Chrome that Claude controls to draw the frames |
| FFmpeg | a free tool that joins frames and sound into an MP4 |
| contact sheet | one image showing many frames in a grid, so Claude can check them at a glance |
| storyboard | the key frames drawn first, so you approve the plan before the long render |
| skill | a saved set of instructions Claude Code follows step by step |

## verified-facts

| id | claim | source | checked |
|---|---|---|---|
| F1 | People use After Effects / Remotion for this today | video 0:00 ("You don't need Remotion. You don't need After Effects.") | Chase's own claim, framing |
| F2 | Claude Code + JavaScript produces MP4 explainers / demos / motion graphics | video 0:00–1:40; repo README | 2026-10-14 |
| F3 | No paid tools; uses plan usage; FFmpeg is open source | video ("totally open source", "we just pay for it with usage"); Playwright Apache-2.0, FFmpeg LGPL/GPL | 2026-10-14 |
| F4 | One-shot 3B1B-style explainer of its own pipeline | video ~0:40 ("this was a one-shot attempt") | 2026-10-14 |
| F5 | Frame = function of t; 60 frames/s; headless browser draws; FFmpeg stitches; Claude checks frames and fixes | video ~0:45–1:40 | 2026-10-14 |
| F6 | Install by handing Claude the URL or as a plugin; installs Playwright/FFmpeg/faster-whisper | video Level 4; README | 2026-10-14 |
| F7 | Storyboard-first saves render loops | video Level 1; SKILL.md non-negotiable #1 | 2026-10-14 |
| F8 | Low ~20 min, high ~30 min, ultra code 8 h; low/high fine | video Level 1 (Chase's test, Opus 5.5) | 2026-10-14 |
| F9 | 7 built-in styles + custom from references | README; SKILL.md description | 2026-10-14 |
| F10 | Repo public, 691★, 104 forks | gh api repos/cth9191/animate | 2026-10-14 (re-check on posting day) |
