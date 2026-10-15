# Brief card (touch 1 of 2)

Stage 3 of the /carousel skill. This is the single message the user approves before any image
exists. Claude sends it in chat. Alongside it, Claude shows the style tile(s) inline (with
SendUserFile where the client has it): the `--only` crop from `node shared/build-gallery.mjs` or the
full style gallery in `engine/styles/`.

`node shared/brief-card.mjs <storyboard.json> --style <REC> --alt <ALT>` writes everything down to
Deviations. Claude appends `### Timing` and `### Needs from you` by hand: the script doesn't write
them, and rerunning it overwrites the file.

The user can reply in any of these forms:
- `go`: approves the starred hook, the storyboard as written, and the recommended style.
- `hook 2, S03`: swaps the hook and/or the style.
- Copy edits, quoting the slide number.

A story rewrite after rendering sends the deck back here. It never triggers another round of images.

---

## Format

**{topic}** · spine {A/B/C/D} · {N} slides · keyword **{KEYWORD}** → {deliverable} ({exists / needs building})

### Hooks

Ranked by the `engine/hooks.md` rubric.

| | Main line · kicker | Visual promise | Formula | Score |
|---|---|---|---|---|
| ★1 | "{…}" · "{…}" | {…} | F{n} | {x}/12 |
| 2 | … | … | … | … |
| 3 | … | … | … | … |

Why ★1: {one line}

### Storyboard

Written for ★1. The fourth column holds every string on the slide except the reserved `headline`,
`counter` and `chrome` places.

| # | Role | Headline | Everything else on the slide (verbatim) | Evidence |
|---|---|---|---|---|
| 1 | cover | {…} | {…} | {focal image} |
| 2 | what | {…} | {…} | {…} |
| … | | | | |

**Spine test** (headlines alone): "{h1} — so {h2} — but {h3} — then {h4} …"

### Gates

G1 ✓ · G2 ✓ · G3 ✓ · G4 ✓ · G5 ✓ · G6 ✓ · G7 ✓/⚠ · G8 ✓
(Any ⚠ or ✗ gets one line on what failed and what was changed.)

**Cold reader** (a different model with no context, reading only the slide text):

| | Intended | Reader recovered | Grade |
|---|---|---|---|
| What | {intent.what} | {…} | {yes / partial / no} |
| Why | {intent.why} | {…} | {…} |
| First step | {intent.first_step} | {…} | {…} |

Blocking terms: {none / list} · Verdict: **{PASS / FAIL}**

### Style

**Recommended: {S0n Name}**: {uses / median / best, from your own post log if you keep one} · fits {format} · last used {date}
Alternative: {S0m Name}: {one line}

### Caption

```
{caption, with the keyword and a pointer to the source video when there is one}
```

### Deviations (logged)

- {only when `storyboard.json` → `deviations[]` has entries}

### Timing

{launch day N / evergreen} · same-format deck in the last 72 h: {no} · same-topic video's 48-hour views: {if you have that data}

### Needs from you

- {only what's genuinely missing: a capture you must take, a deliverable and its comment-keyword automation to confirm, a fact only you know}

---

## Standing CTA keywords

Your standing keywords, one row each: a keyword and the real, evergreen deliverable it sends, already
wired into your comment-to-DM automation (e.g. ManyChat, if you use one). A row pairs the keyword
with what the commenter gets, e.g. ANIMATE → a GitHub repo with a free skill, used on how-to
explainers for that skill. Fill the table in once and keep it current. If the table is empty (or the
keyword isn't in it), the keyword is new: draft `deliverable.md` in the deck folder and flag it
under Needs from you.

| Keyword | Deliverable | Exists? | Fits |
|---|---|---|---|
