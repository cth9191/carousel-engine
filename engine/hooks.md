# Hooks: topic signals, rubric, formula bank

Part of Carousel Engine. The evidence is a review of one AI / Claude Code creator account's own
carousel history (hook forensics, a critique of every past deck), plus third-party carousels and
published headline research. The worked examples in §4 are that account's real cover wording. The
numbers are left out; the lessons are kept in words.

To calibrate on your own account, measure each post against the median of your other carousels
posted within ±21 days (from your own post log). A post well above that median is a win; one well
below it is a loss.

**Status:** the rubric **ranks** hooks. It does **not** block shipping until a blind back-test on
your own posts shows it separates your top covers from your bottom ones.

## 1. Topic first

The hook can only be as good as the topic. Signals, in order of how much we trust them today:

1. **A launch, with a claim, verdict or build attached.**
   - **Loses:** a day-0 "X is live / is here" post with no claim. The announcement already said
     it; the carousel adds nothing.
   - **Wins:** "I built it / I tested it" posts a few days after a launch, across two launch waves.
   - **Can work on day 0:** a cover with a specific, surprising claim and real numbers, e.g.
     "Sonnet 5.5 is live (and it just beat Opus)" with the benchmark scores beside it.
   - **Rule:** a launch post needs a claim the announcement doesn't make for you (a verdict, a
     benchmark surprise, a build). "X is live" alone is the anti-pattern, not day 0 itself.
2. **Franchise topics.** A named personal system that recurs (e.g. a "JARVIS OS" the creator keeps
   upgrading) builds an audience that already knows its terms. A franchise sequel gets a slot
   whenever there's a real upgrade to show.
3. **A trending repo, only if it fixes a pain people already feel.** The pain leads; the repo
   name follows. A cover that leads with an unknown name ("FOOBAR: your task dashboard")
   gives a cold viewer nothing to anchor on.
4. **Your own YouTube demand on the same topic**, if you have a channel (hypothesis: only one
   clean case so far). When a topic is picked, log the same-topic video's 48-hour views in the
   brief. After 4 weeks, decide whether this becomes a filter.

Within one format, keep decks at least 72 hours apart. Two decks in the same format a day apart
compete for the same viewers.

## 2. Writing hooks

For each brief, write about 10 hooks across **at least 5 formulas** from §4, then score them
with §3. Show the top 3 in the brief card, star one, and give one line on why.

Every hook is a set: the **main line** (the big type), an optional **kicker** (small line or
parenthetical), and a **visual promise** (what the cover image shows). Score the set, not just
the words.

## 3. Rubric (0–2 each, max 12)

| # | Criterion | 0 | 1 | 2 |
|---|---|---|---|---|
| R1 | **Anchor:** hooks on something the viewer already knows | Leads with a name they've never heard ("FOOBAR") | A known category ("task dashboard") | A felt pain, wanted outcome or familiar reference ("JARVIS", "AI slop", "10X your project") |
| R2 | **Specific** | Abstract ("level up", "my guides") | Names a thing *or* a number | Names an artifact/result **and** one number or bound ("4-step build", "3 repos", "4 real tests") |
| R3 | **Instant visual** | Abstract art or a busy collage | Relevant but takes study | One focal image a cold viewer gets in a glance: the end state, recognizable logos, or a character doing the job |
| R4 | **Timing fit** | A bare "X is live / is here" with no claim | Neutral / evergreen | A claim, verdict, benchmark surprise or build on something people are talking about now |
| R5 | **Payable** | Promises something the deck doesn't show | Mostly paid off | The deck pays off every word one-to-one (the count matches, the outcome is shown) |
| R6 | **Glanceable** | More than 14 words in the main line, or two competing ideas | 11–14 words | ≤10 words in the main line, readable in under 2 s at 360 px wide |

**Tie-breakers:**
- Prefer the hook whose anchor is broader: two tools most of your audience already uses
  ("Claude Code + NotebookLM") over a niche pair ("<new model> + <niche tool>").
- Then prefer loss/negative framing over neutral framing. The Upworthy headline data favored
  it; for carousels this is untested.

**Automatic zeros:**
- R4 = 0 for a bare "X is live / is here / just dropped" main line that has no claim attached.
- R5 = 0 for any superlative or number the deck can't show.

## 4. Formula bank

Worked examples are real cover wording from the reviewed account unless marked third-party. Use them
as templates, not laws. The ids are stable: storyboards cite them (the worked example deck uses F10).

| ID | Formula | Template | Worked example | Best spine |
|---|---|---|---|---|
| F1 | Fantasy build | "THE {N}-STEP BUILD / Build Your {aspirational named system} / by the last step, it {life-scale outcome}" | "Build Your JARVIS OS / by the last step, it runs your whole day" | D |
| F2 | Known + known | "{tool everyone knows} + {tool everyone knows} / how to connect {superlative pair} (for free)" | "Claude Code + NotebookLM / how to connect two of the most powerful AI tools in the game (for free)" | A |
| F3 | New-model build | "build your {NEW MODEL} {OS/system} IN {N} STEPS" (a few days after launch) | "build your FABLE 5 OS IN 5 STEPS" | D |
| F4 | Hype + real deadline | "{MODEL} {CHARGED WORD}. / {N} use cases you must try now" + the real deadline in the chrome | "FABLE 5 INSANITY. / 5 use cases you must try now" | C |
| F5 | Count + 10X outcome | "{3/5} {GitHub Repos/Skills} That Will 10X Your {Next} Claude Code Project" + "Stop {pain}" | "3 GitHub Repos That Will 10X Your Claude Code Projects" | C |
| F6 | Enemy → identity | "DEFEAT THE {named enemy} / How to Turn {tool they use} Into a {identity} / The {N}-step workflow that kills {bad outcome}" | "DEFEAT THE AI SLOP MONSTER / How to Turn Claude Code Into a Web Design Genius" | A |
| F7 | I tested | "I tested {A} vs {B} / {N} real tests. My honest verdict." + the tests listed | "I tested GPT 6 Astra vs Claude Fable 5.1 / 4 real tests. My honest verdict." | B |
| F7b | Launch + surprising claim | "{MODEL} is live (and it just {beat X}) / on {benchmark}" + the real numbers on the cover | "Sonnet 5.5 is live (and it just beat Opus) On Terminal-Bench 4.0" | B |
| F1b | Franchise sequel | "THE V2 BUILD / Build Your {franchise} 2.0" + the N parts | "Build Your JARVIS OS 2.0" | D |
| F8 | Ranked top-N, hot vertical | "TOP {N} Claude Code {Front-End/design} Skills" | "TOP 5 Claude Code Front-End Skills" | C |
| F9 | Value twist (third-party pattern) | "{N} {things} {that replace something people pay for}" | "5 GitHub repos that replace a paid design tool" | C |
| F10 | First-person capability (third-party pattern) | "my Claude Code can {surprising capability} now / here's how I did it." | "My Claude Code makes videos now / here's the exact prompt" | A |
| F11 | Problem first, fix second | "Your AI {embarrassing failure} / I {verb} {surprising fix}" | "YOUR AI GRADES ITS OWN HOMEWORK / I Make Two AIs Attack Every Plan" | A |
| F12 | Outcome playbook (third-party pattern) | "{A} + {B} + {C} = {$ or result} IN {timeframe}" | "Claude Code + Figma + Vercel = a live site in one afternoon" | A |
| F13 | I analyzed N (third-party pattern) | "i {analyzed/read/ran/tested} {N} {things} / {payoff with M}", your own verb, N circled, a real corpus saved in the deck | "i read 120 CLAUDE.md files / here are the 9 rules they share" | C-variant (findings listicle, `engine/spines.md`) |

**Kicker add-ons that lower the risk of swiping:** "(for free)", "(exact setup inside)",
"(full stack)", "(plain-English version)".

## 5. Anti-patterns

Patterns to avoid. The examples are invented to show the shape.

| Anti-pattern | Example |
|---|---|
| Bare announcement (no claim) | "<MODEL> is out" with nothing else · "<product> is now open source" |
| Empty superlative | "the best update yet" · "a total game changer" |
| Unknown name leads | "FOOBAR: your task dashboard" · a bare command name ("/foobar") as the main line |
| Time-to-learn | "Master <tool> in a weekend" |
| Generic system | "you need an AI system" (the same idea as a named build is F1) |
| Self-diagnosis with no artifact | "Which type of <tool> user are you?" |
| Niche sub-skill for a new model | "Turn <model> into a <job title>" |
| Generic gate | "Comment <word> to get my guides": the keyword names no specific deliverable |
| Milking one model | Back-to-back hype posts on the same model with nothing new to show |

## 6. CTA keyword

- Lock it **with** the hook, never later. Two past decks had their keywords swapped after approval.
- It names this deck's deliverable ("ANIMATE" → the free animate skill). It's identical on the
  slide, in the caption and in your comment-to-DM automation (e.g. ManyChat, if you use one).
- Prefer one of your standing keywords tied to an evergreen deliverable that already exists (the
  table in `engine/templates/brief-card.md`). A new keyword means a new deliverable to build: draft
  `deliverable.md` and flag it in the brief card.
