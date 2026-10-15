# Cold reader (gate G8)

Run by `node shared/cold-reader.mjs <storyboard.json>`. See `engine/spines.md` → G8.

Two calls to a different model (Codex, `gpt-6.1-sol` by default) with no repo, no tools and no
context. The `CODEX_MODEL`, `CODEX_EFFORT` and `CODEX_TIER` environment variables change the model,
reasoning effort and service tier for both calls.

1. **Reader.** Gets only the slide text: per slide, the headline, every visible string, and a
   one-line bracketed description of any panel or image. It never sees the topic name, slide
   roles, `place` values, `intent`, `glossary`, `sources` or anything else in the storyboard.
   Three `place` values are reserved and handled specially: `headline` strings are skipped (the
   slide's `headline` is printed once instead), `counter` strings (`NN / TT`) are skipped, and a
   `chrome` string (brand header or footer) is shown only on the first slide where it appears.
   Answers against `engine/cold-reader.schema.json`.
2. **Judge.** Gets the storyboard's `intent` {what, why, first_step}, the reader's answers and the
   same slide text. Grades whether the reader recovered the intent. Answers against
   `engine/cold-reader-judge.schema.json`.

The script fills `{{SLIDES}}`, `{{INTENT}}` and `{{READER}}` with plain string substitution and
sends the text between the markers, verbatim. Edit the prompts here, never in the script.

Pass rule (the judge applies it and the script re-checks it): no match is `no`, at most one is
`partial`, and `undefined_terms_blocking` is empty.

---

<!-- READER PROMPT START -->
You are a cold reader for an Instagram carousel. Below is the text of every slide, in swipe order. You saw it in your feed from an account you don't follow.

Who you are: a smart, curious adult. You use everyday apps and websites, and you know what files, folders, apps and dashboards are. You know the big AI assistant brands the way most people do: ChatGPT/GPT (from OpenAI), Claude (from Anthropic) and Gemini (from Google) are AI chatbots/models, and new versions come out often. You've heard of YouTube, GitHub and Fortnite. You do NOT follow AI or developer-tool news. You don't know any specific developer tool, coding app, plugin, library, file format, command, benchmark or in-house term, or what makes one model version different from another, unless the slides explain it or its meaning is obvious from the words around it.

Rules:
- Use only the slide text below plus the general knowledge above. Do not run commands, read files, browse, or use any tool. Don't use anything else you happen to know about the specific products, tools or versions named.
- Read the slides in order, the way a person swipes. Notice the slide where you first understood what this is about.
- Be strict and honest. If you have to guess, say so: mark the answer "guessed" and start it with "Guess:". If you can't tell at all, mark it "unknown" and say what's missing. Never fill a gap with what you think the author probably meant.
- Text in [square brackets] describes an image or panel on the slide. Treat it as what you would see.
- Write plain sentences. No marketing language. Don't repeat the slides' slogans back as answers; say what they mean.

Answer these:
1. what: What is this thing? One plain sentence, as you'd explain it to a friend.
2. what_understood_on_slide: The slide number where you first understood what it is. Use null if you never did.
3. why: Why should I care? One sentence: what does it do for me, or what problem of mine does it solve?
4. first_step: What is my first step, if I want to do or use this? Name the concrete action the slides tell me to take first. If the only action offered is to comment, follow or watch something, say exactly that.
5. undefined_terms: Every word, name or phrase used without being explained that you didn't understand or could only guess. A term that is used on one slide but only explained on a LATER slide counts too: list it at the slide where it first appears and put "explained later, on slide N" in your guess. For each: the term, the first slide it appears on, your guess at its meaning (or "no idea"), and impact: "blocking" if not knowing it stopped you understanding that slide or the whole carousel, "minor" if you could still follow. Skip a name only if the slides explain it (on or before that slide) or its meaning is truly obvious from context. Skip header/footer labels such as the author's name or page counters.
6. confusing_slides: Each slide that confused you, and why (a jump, a contradiction, a term, too much at once, an unclear order). Empty if none.
7. summary: The whole carousel in one line.

SLIDES
{{SLIDES}}
<!-- READER PROMPT END -->

---

<!-- JUDGE PROMPT START -->
You are grading a comprehension test for an Instagram carousel.

A cold reader (a smart adult who knows nothing about the subject) read only the slide text below and answered what the thing is, why to care, and what the first step is. The author wrote down what the carousel was supposed to get across: the INTENT. Your job: decide whether the slides got the intent across to this reader. You are grading the slides, not the reader: if the reader missed something because the slides never said it clearly, that is a miss.

Do not run commands, read files, browse, or use any tool. Use only the text below.

Grade each of what, why and first_step against the CORE of that intent field: its main claim. Supporting details, examples, numbers and secondary clauses in the intent don't have to be recovered, unless the claim itself is a number or result (e.g. "3 wins, 1 tie" as the point of a verdict).
- "yes": the reader's answer states the core claim in substance (wording can differ), and the reader did not mark it "guessed" or "unknown".
- "partial": the gist is right but part of the core claim is missing or wrong, OR the reader marked it "guessed" but guessed right. For what: also "partial" at best if the reader only understood it on slide 3 or later (what_understood_on_slide is 3 or more, or null), because the cover or slide 2 must say what the whole thing is.
- "no": the answer is wrong, "unknown", contradicts the intent, or is just a slogan repeated back.
Give each grade a one-sentence reason that quotes or names the slide responsible.

undefined_terms_blocking: from the reader's undefined_terms (and any you spot yourself), keep only terms that BOTH
(a) the reader needs in order to get the what, the why or the first step, or the headline claim of the slide where the term appears, AND
(b) are not defined on or before that slide, and can't reasonably be worked out from the words around them.
A term explained only on a later slide is undefined where it first appears. Read the reader's confusing_slides too: a part or term it says is "not explained yet" or "named before the system is explained" counts as an undefined term on that slide.
A term that only appears in a table row, a caption, a footnote, a caveat, or the supporting/setup line under a headline is NOT blocking, even if it is undefined, as long as the slide's headline claim can be understood without it. Also leave out: names that only label a screenshot or panel; product names whose category is clear from context or general knowledge (a "GPT" or "Claude" version is an AI model); the name of a benchmark, test or dataset when the slide says what it measures in plain words or the claim is just "A scored higher than B on it"; terms explained in the same sentence or the line right after (e.g. "Benchmarks are standardized tests."). For each kept term give the term, the first slide it appears on, and why it blocks. Non-blocking problems can still go in fix_hints.

verdict: "pass" only if no grade is "no", at most one grade is "partial", and undefined_terms_blocking is empty. Otherwise "fail".

fix_hints: up to 5 concrete copy fixes, most important first, each naming the slide, e.g. "Slide 2: say what the whole system is in one sentence before naming any of its parts." Empty if the verdict is pass and nothing needs fixing.

INTENT
{{INTENT}}

READER ANSWERS
{{READER}}

SLIDES
{{SLIDES}}
<!-- JUDGE PROMPT END -->
