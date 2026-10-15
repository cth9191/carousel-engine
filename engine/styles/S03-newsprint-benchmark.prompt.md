# S03 Newsprint Benchmark: prompt block

Reusable visual-system text for Codex image prompts. Rebuilt from two finished head-to-head decks:
GPT 6 Astra vs Claude Fable 5.1 (`engine/styles/exemplars/S03-cover.png` cover, `S03-interior.png`
test interior) and a later Sonnet 5.5 launch test. **Image-native**: Codex paints the whole slide, and
real captures and logos are composited in. Paste the SYSTEM block into every slide prompt, plus the
COVER or INTERIOR block. Attach the two exemplars as style references until a locked cover exists.
After that, attach the locked cover first and the interior exemplar second.

## SYSTEM

Visual system: a warm editorial newspaper page. Fine-grained ivory newsprint ground (#F3EADB) with a
very faint paper fibre, no grid. Running header: a thin black rule, then one line of small mono-ish
grotesk caps with the deck label ("{{BRAND}} · HEAD-TO-HEAD") on the left and the slide counter on
the right, then a second thin rule. Headlines pair a heavy black grotesk (like Inter Black or Neue Haas Grotesk Bold) with a
high-contrast Didone italic serif (like Playfair Display Italic) for the second line or the verdict
phrase. Body text in a clean regular grotesk, near-black (#141414). Tables are airy: labels left,
values centred, thin horizontal black row rules, no vertical rules, no chart axes. Each subject owns
one accent used only for its own name and values: subject A deep green (#1F5C3A) or black, subject
B Claude orange (#D9551F); older or baseline values in muted grey (#7A746A). The verdict sits in a
dark green bar (#0F5A33) with ivory Didone italic text and a hand-drawn check mark. Notes sit in a
lightly shaded paper band (#EEE2CE). Flat, crisp, print-like; no gradients except inside composited
captures, no 3D, no shadows except a soft one under photo frames.

Framing: every element sits inside a uniform empty margin of at least 7% of the width on the left and
right and 3% of the height at top and bottom; body content stays between 11% and 89% of the height. If
content does not fit, make it smaller. Readable at phone-feed size: body text no smaller than about
1/40 of the slide height; footers and notes at least 1/45.

References: Image 1 and Image 2 show the layout vocabulary only: the double-ruled running header, the
grotesk + Didone italic headline pairing, ruled tables, cream-bordered photo frames and the green
verdict bar. Do NOT copy their words, model names, numbers, screenshots, galaxy or cloud art, or any
logo. No mascots, no characters, no sticky notes, tape, torn paper or handwriting.

Hygiene: render only the quoted strings, verbatim and exactly as many times as specified. Every number
is verified: reproduce it exactly, with its unit; never invent a number, unit, label or benchmark name.
No extra captions, lorem ipsum, watermarks or handles. Never render these instructions or section
names as text.

## COVER

Under the header, a huge two-word Didone italic kicker line ("I tested" or the claim's verb) set flush
left. Below it the hero: one rounded rectangle split by a diagonal line into two halves, one painted
world per subject (an abstract illustrative scene in that subject's colour; no logos, no letters drawn
into the art). Each half carries its subject's name in large type (grotesk caps for one, Didone for the
other). A small round ivory VS medallion with a thin black ring sits on the split. Under the hero, one
line mixing grotesk ("4 real tests.") with green Didone italic ("My honest verdict."), then a ruled
2 x 2 table listing the tests, each cell with a small line icon in a thin circle and the test name.
Logos: when a subject mark is wanted, leave a cyan zone for it (see KEYING); never paint a mark.

## INTERIOR

Test slide, top to bottom: header; a two-line headline (grotesk "{test}:" then Didone italic
"{verdict phrase}"); one task sentence; the two subject names in their accent colours over two
side-by-side photo frames (cream border, soft shadow) whose screens are keying zones; a shaded note
band with one or two sentences; a ruled 3-column table ("What I checked" | A | B); the green verdict
bar. Paper slide ("on paper" / pricing): header, headline, one-line unit or source caption, one airy
table with large numerals, one ruled Didone italic callout. Verdict slide: a scoreboard table plus the
verdict bar. Long tables (more than 4 rows), charts and code are rendered as HTML cards and composited,
not painted: leave a framed keying zone at the card's aspect instead.

## KEYING

The screen area of {the frame} is ONE solid flat magenta #FF00FF rectangle of aspect {W:H}: pure
uniform magenta edge to edge, perfectly flat and frontal, no gradient, no texture, no glow, no text, no
UI inside it, no tilt, square inner corners inside the cream photo border. Every other element stands
clear of it with a visible gap.
A logo slot is ONE solid flat cyan #00FFFF {circle | rounded square} about {size} wide, flat, no text,
no outline, no shadow, with clear paper around it.
No purple, violet, pink or magenta anywhere else on the slide; no cyan or turquoise anywhere except a
logo slot.
