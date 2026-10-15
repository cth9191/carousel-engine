# Story spines + text gates

Part of Carousel Engine. The rules come from an audit of one creator account's past carousels; the
examples below keep the lesson and drop the deck names and numbers.

A **spine** is the fixed story path for a format. Each slide has a **role**, and the role decides
three things: what the slide has to do, what evidence it needs, and how many words it gets.
Claude writes `storyboard.json` (schema: `engine/storyboard.schema.json`) by filling the
spine's roles. All gates below run on that text, before any image exists.

These are defaults we're testing, not laws. The sample sizes behind them are small. Log any
deviation and the reason for it in `storyboard.json` → `deviations[]`.

## Picking the spine

| The deck is about… | Spine | Signature |
|---|---|---|
| A new tool, repo, feature, skill or workflow, explained so someone can use it | **A. Explainer** | What → Why → How → value peak → use → CTA |
| Two models or tools tested against each other, or a launch put to a real test | **B. Head-to-head** | "I tested" → on paper → tests → verdict |
| N repos / skills / plugins / prompts | **C. Listicle** | count hook → one item per slide |
| A named personal system built in N steps (JARVIS OS, Claude OS) | **D. System build** | named system → N steps → the outcome |

If a topic fits two spines, use the one whose cover hook ranks higher (`engine/hooks.md`).

**Length:** 10 slides or fewer by default (you can raise it). No data says longer decks hurt.
Within one format, never post two decks within 72 hours of each other. The shipped worked example
(`carousels/2026-10-14-claude-video-free`) doesn't count toward this rule.

## Universal role rules

- **Cover:** one hook (ranked top-3 on the rubric), one focal image a cold viewer gets at a
  glance, and an optional preview of the deck's shape ("4 parts", "3 steps", "4 real tests").
  No "comment X" on the cover.
- **Headlines:** 7 words or fewer, with one accent phrase.
- **Body budget:** about 45 words, plus one proof artifact and one caption or table.
  Structured rows (tables, numbered rows, prompt cards) may go up to ~100 words when each row
  is short. Never stack sticky + narration card + table + footer bar on one slide.
- **Proof vs illustration:** PROVE means a real capture, a verified number or a real run.
  EXPLAIN means a diagram or mock, clearly illustrative. A mock is never shown as proof.
- **Chrome:** every slide gets a counter `NN / TT` matching the real total, plus the style
  card's header/footer. In `storyboard.json` these strings take the reserved places `counter` and
  `chrome`, and every line of the headline takes `headline`; the cold reader and the brief card
  handle those three specially. Any other `place` is free-form.
- **CTA:** exactly one action on the slide: `Comment KEYWORD`, followed by what they get. The
  YouTube link, "save" and "follow" go in the caption.

## A. Explainer (8–10 slides)

| # | Role | Job | Must contain | Evidence |
|---|---|---|---|---|
| 1 | `cover` | Stop a cold scroller | Hook + focal image | the end state, recognizable logos, or a character doing the job |
| 2 | `what` | Define it for someone who has never heard of it | A concrete pain → "the fix is X" + one sentence: *X is a ___ that ___*. Optional: a plain-word strip previewing the steps. **No component names.** | one simple visual of the thing |
| 3 | `why` | The "But": why this matters to *me* | Old way vs new way; one countable pain; why-now if it's news. Never framed against another product ("the web app can't…") | PROVE: real screenshot or number |
| 4 | `model` | Teach the vocabulary before the steps | One diagram, 4 or fewer named parts, each defined in ≤8 words | EXPLAIN: diagram |
| 5–6 | `how` | One mechanism or step per slide | What happens, shown; callouts on the panel. Slide 5 or 6 carries a re-hook line ("this is the part that makes it click") | PROVE: real panel |
| 7 | `peak` | The save slide | A copy-paste prompt, command or config, verbatim and short enough to read | the real text |
| 8 | `use` | The send slide | 2–3 concrete uses with real output, or the numbers | PROVE |
| 9 | `start` | Lower the barrier | Install + first command, or a start plan / pitfalls | real command |
| 10 | `cta` | One action | `Comment KEYWORD` + the named deliverable | — |

For small topics, merge `model`+`how` or `use`+`start`. Never drop `what` or `why`.

## B. Head-to-head / launch test (8–10 slides)

| # | Role | Must contain |
|---|---|---|
| 1 | `cover` | "I tested A vs B" + the N tests listed + a promise of a verdict |
| 2 | `paper` | What the benchmarks/specs say, with each benchmark defined in plain words; label who measured it |
| 3 | `context` | Cost / speed / access: the practical difference |
| 4…N+3 | `test` | One real test per slide: the task, side-by-side output, a per-test winner, and one line on *why* it won |
| N+4 | `verdict` | Scoreboard ("3 wins, 1 tie") + who should use which |
| last | `cta` | Comment KEYWORD for the full test files/prompts |

The verdict must come from real runs. On day 0, run the launch variant: the cover leads with
a specific, surprising claim backed by real numbers (e.g. "Sonnet 5.5 is live (and it just beat
Opus)" with the benchmark scores on the cover). A bare "X is live" with no claim is the
anti-pattern.

## C. Listicle (7–10 slides)

| # | Role | Must contain |
|---|---|---|
| 1 | `cover` | Count + outcome ("…That Will 10X Your Claude Code Projects") + one verified star figure or month stamp |
| 2 | `why` (optional) | Why this list matters, or how it's sorted; one concrete stake |
| 3… | `item` | Name, what it does in one sentence a cold viewer understands, what it replaces or solves, real proof (README/UI/stars verified on posting day), one concrete use |
| n−1 | `combo` (optional) | How I'd combine 2 of these |
| last | `cta` | Comment KEYWORD for the full list with links |

Every item slide is its own mini what-and-why. A slide of names alone fails (a past listicle
showed about 70 repo names with no descriptions).

## D. System build (8–10 slides)

| # | Role | Required? | Must contain |
|---|---|---|---|
| 1 | `cover` | yes | Named system + "N-step build" + the outcome ("by the last step, it runs your whole day") + the N parts as icons |
| 2 | `what` | optional | What this system is, in one sentence, plus the prize |
| 3 | `why` | optional | Old way / new way, real screenshot |
| 4 | `parts` | optional | The N parts with a body-role analogy (brain / memory / voice / face) |
| … | `step` | yes, N of them | One step per slide: what you build, the real panel, the prompt or command |
| n−1 | `day` | optional | A real day with the system running: the payoff |
| last | `cta` | yes | Comment KEYWORD for the exact setup |

The cover's N counts **step slides only**. A build "in 5 steps" can run 8 slides: cover, prize, 5
steps, CTA.

## Text gates

Run all gates in order and record each result in `storyboard.json` → `gates`. Any FAIL means
rewriting the text. After 2 failed rewrites, stop and show the failure in the brief card.

| # | Gate | Fails when… |
|---|---|---|
| G1 | **Cover contract** | The hook names no outcome/artifact; a count on the cover ≠ the number of slides that pay it off; a superlative the deck doesn't prove ("the biggest upgrade of the year", "the biggest upgrade since <X>"); a bare "X is live / is here" with no claim attached; a number the deck never shows (a cover promising 100 items that shows 40) |
| G2 | **Slide 2 defines the whole thing** | Slide 2 introduces a sub-component (a model name, voice engine, tier, internal tool) before defining the whole; or a sub-component appears before slide 4 (a deck that opens on the name of its internal router) |
| G3 | **Glossary** | Any term a cold viewer wouldn't know is used before it's defined; more than one new term on a slide; any new term on `verdict`/`cta`. Keep the term list in `storyboard.json` → `glossary` |
| G4 | **Budget** | A headline over 7 words; body text over the role's budget; more than one proof artifact + one caption/table |
| G5 | **Spine test** | Read only the headlines, joined by "so / but / then / and": it doesn't read as one story; a headline repeats the cover; step numbering drifts (a "4-step" cover over 3 steps + "STEP 0") |
| G6 | **Re-sequence** | The slide order follows the source's timeline or section order instead of the viewer's questions; a source tangent got its own slide (a shortcut the video mentions in passing becomes "STEP 1") |
| G7 | **CTA match** | The keyword doesn't name this deck's deliverable; it differs between slide, caption and your comment-to-DM automation; the deliverable doesn't exist yet and isn't drafted |
| G8 | **Cold reader** | `node shared/cold-reader.mjs` (a context-free model) can't recover `intent.what`/`why`/`first_step`, or flags an undefined term |

G1–G7 are Claude's self-check. G8 is independent: a different model with no context
(validated on 3 past decks before release: it passed the one the audit had rated clear and failed
the two the audit had rated confusing).

**What the gates protect: comprehension, not reach.** A deck can fail G8 and still find its
audience when the topic carries it. A failing gate triggers a rewrite (max 2) and then gets
reported in the brief card. You can override it, for example on a franchise sequel whose
audience already knows the terms. Write `intent.why` as one claim; the judge grades every
clause as core.

## Source → spine (input flow)

A video runs setup → build → reveal. A carousel leads with the reveal. Map the **dossier**
(`engine/templates/dossier.md`) onto the roles; never map the source's timeline.

| Source | Feeds |
|---|---|
| Your YouTube video | transcript → `what`/`why`/`how`; frames at chosen timestamps → proof panels (scrub the webcam bubble); your on-camera take → `verdict` or `peak`; demos → `use` |
| GitHub repo | README's one-line definition → `what`; install → `start`; verified stars/demo → proof; examples → `use` |
| Docs / announcement | definition + examples → `what`, `use`; verified numbers → `why`/`paper`. Ignore the announcement's section order |
| "Go research it" | web search (plus any research skills you have) → the same dossier (slower path) |

## Failure modes these gates catch

| Failure | Example | Gate |
|---|---|---|
| Jargon before definition | A slide 2 that explains how an internal classifier sorts requests into "Tier 1, 2 or 3" before saying what the system is | G2, G3 |
| Missing what/why | A system-build deck that opens on "STEP 1" | spine A/D roles |
| Why framed against another product | "The <other product> can't run your skills." | spine A `why` |
| Fragment slides | 70 repo names, no descriptions | spine C `item` |
| Stacked blocks | Headline + sticky + panel + narration + table + footer on every slide | G4 |
| Drifting numbers | A "4-step" cover → 3 steps + STEP 0; one deck saying 3-step in one place and 4-step in another | G1, G5 |
| Source order copied | Slides that follow the transcript's timestamps; a launch deck that follows the press release | G6 |
| Cover promise unpaid | A cover promising 100 items that shows 40; a "10x" never shown | G1 |
| CTA mismatch | Slide "Watch the full video" vs caption "Comment GUIDE" | G7 |
