# Voice guide

How to write an article that belongs in this course. Read this, then the exemplars at
the bottom, then write.

## 1. Who is being spoken to

One reader: a working solicitor on a Mac, senior in her own craft and new to this one.
Not stupid, not young, not a developer. She has a matter on and forty minutes.

- **Assume professional intelligence, assume no computing.** Explain `~` and `pwd`. Do
  not explain disclosure, deadlines or why consistency matters. Legal examples run
  unglossed: bundles, LBAs, captions, indemnity clauses.
- **Her inexperience is never her fault.** Where something is hard, say why it is
  structurally hard: *"it is not a difficulty of intelligence — it is a difficulty of
  discovery. Nobody works out `grep` by staring at a prompt."*
- **No reassurance, no encouragement, no praise.** "Nothing here can break anything" is
  allowed, because it is a fact. "You've got this" is not.
- **Second person throughout.** "We" appears once in fifty articles and should not
  appear again. The author is invisible; the only named person is the Boss.

The register is flat, dry and certain — a good practice note. Short declaratives, no
adverbs of enthusiasm, the occasional joke delivered without pausing for it (*"like a
microwave with ambitions"*). **No contractions**: "do not", "it is", "cannot", every
time. They appear only inside quoted speech — *"I don't want it writing anything"* —
marking the sentence as hers.

## 2. Rhythm

Sentences vary hard. The short one carries the weight; the long one before it does the
work. *"Not slower — **worse**. Every extra option is another thing to consider and
another chance to pick wrong, and it pays that cost on every single question, including
the ones where none of it was relevant."*

Paragraphs run **two to four lines**, five at the ceiling. A one-line paragraph standing
alone is the strongest move available, about twice per article: *"More is worse."*

Fragments land: *"Not a lookup. Not a search of the internet."* Lists are for genuinely
parallel items, never an escape from a paragraph. Bold goes on a term at first
definition and on a list lead-in, not on mid-sentence emphasis except at a turn. Prose
wraps at 72 columns; code lines stay under 60.

## 3. How an article opens

Frontmatter, `# Title`, `*v0.1.0*` on its own line, then one to four short paragraphs
bare of any heading.

**The move is the flat assertion: sentence one states the article's fact outright, in
her vocabulary, with no runway.** Never "In this article", never a question, never a
scene. Three variants:

- **The definition** — *"A **custom agent** is an agent you defined."* The term arrives
  bolded within two sentences.
- **The callback** — *"You already know that every conversation is a separate agent.
  Here is the part that was left out."* Picks up the last article, turns it.
- **The answer** — where the title promises something, line one settles it. Title *How
  skills work*, first line *"If they are not managed properly, they do not."*

Then a line saying what the article costs — *"This one is short"*, *"More than you need
for today"*, *"Three shapes, easiest to hardest"* — before the first `##`.

## 4. How an argument turns

Nothing here is sold. Every capability is stated with its limit attached, in the same
breath, and the limit gets the emphasis. Four moves:

- **The concession-reversal** — grant the reasonable reading in one short sentence,
  refuse it in the next. *"That reads like a limitation. It is nearer the opposite."* —
  *"It is a good story. Most of it does not survive contact with real work."*
- **The honest one** — name, explicitly, the fact that costs something, often a row of
  the table you just drew. *"That last row is the honest one, and the reason this course
  exists."* — *"Be honest about the other side. Some commercial software does not exist
  for Linux at all."*
- **The refusal to oversell** — state the ceiling unsoftened. *"**Effort is a request,
  not a guarantee.** … It is worth setting. It is not worth relying on."* — *"A
  chronology appearing is not the test. A chronology can appear and be invented."*
- **The exact distinction** — two lookalikes separated with no connective padding.
  *"That is a skill. The other is a stencil."* — *"Ability is reliable. Instinct is
  not."*

And failure is always described as **quiet** — the recurring villain goes wrong without
saying so: "ignored in silence", "no error, no warning, nothing in red", "it never tells
you". Use that register for every failure mode.

## 5. How an article closes

The last `##` ends on its final paragraph, and that paragraph is the last of the
article. Then ``Press `n`.`` alone, as the final line of the file. Nothing sits
between the two.

**An article never hands over.** No sentence at the foot of an article may point at
what comes next — not by slot (*"The next article is what to do with that."*), not by
name (*"That is* The default agent*."*), and not by topic (*"Now, what actually goes
inside the file."* — *"Next, the one that puts them in order."*). All three shapes are
the same mistake wearing different clothes: the article's closing would depend on the
article's position, and a part inserted anywhere in the course makes it quietly false.
An article is written to be true wherever it lands.

Older articles still show the habit. Read them for register, never for their closings.

**The last article of a part closes differently** — a `---` rule, then a paragraph
naming the part just finished and the part coming, then the key. *"That is Skills.
Subagents come next — how one agent hands pieces of a job to others, how you chain
agents and skills together, and how you get a skill to fire inside a subagent when you
cannot type a slash at it."*

That paragraph **names parts and never counts them.** It may say which part follows;
it may not say that a part is the last one, the third one, or one of five. An ordinal
is a fact about the shape of the course, and the shape of the course changes.

## 6. The Boss

The course's only character: an unnamed practitioner whose hard-won findings are what
distinguish this from the official documentation. Seventeen references, in three shapes.

**Shape A — the Party Trick.** A numbered technique, always a blockquote, always the
first thing after `*v0.1.0*` or first in its section, always this formatting:

```
> **Party Trick #4 from the Boss: skill engineering.** Do not write the
> instructions you want in the skill. Hand Claude examples of the work and
> let it write the instructions from those.
```

Bold runs from `Party Trick` to the end of the naming sentence. The name is a two-word
noun phrase (`content isolation`, `agent engineering`, `chain engineering`) or an
imperative (`always invoke skills manually`); one to three unbolded sentences follow
inside the quote. Use only where the whole article exists to deliver that technique.

**Shape B — the block quotation.** The Boss in his own words, blockquoted, italic inside
quotation marks. For a judgement rather than a method, where the language is blunter
than the course's own voice permits:

```
> **From the Boss:** *"This is why apps like claude.ai and Claude Cowork
> will never get you anywhere: you cannot see context. Your agents will
> start rotting, and you will only notice when the work ends up being
> dogshit — or you end up disbarred."*
```

`> **From the Boss:** *"…"*` when quoting him; `> **From the Boss.**` — full stop, no
quotation marks — when reporting him. Place it where the article's own argument has just
run out of politeness. About one per part.

**Shape C — the attributive aside.** Half a sentence of plain prose, no blockquote,
crediting a decision already being explained. The commonest shape, and the default: *"As
with agents, the Boss went through them the hard way, and four survived."*

**Inventing new ones.** Shape C is yours to write freely: it is attribution, and any
convention that came from practice rather than documentation can carry it. Shape B needs
a genuinely quotable position; use it sparingly. **Shape A you do not invent.** #1 to #6
are taken and the set is closed and counted — *"That is the sixth Party Trick doing what
it was advertised to do"*, *"You now have the six Party Tricks"*, and *About this wiki*
is built on them. A #7 from a drafter would attribute a finding to a person who never
made it and falsify a tally in two other articles. A real seventh is the user's to
authorise and number, and adding it means editing the count in
`11-subagents/10-step-five-watch-it.md` in the same change.

## 7. Spelling, punctuation, markup

- **British spelling**: `colour`, `recognise`, `customise`, `generalise`, `behaviour`,
  `licence` (noun). **Em dash, spaced**: ` — `, never `--`, never unspaced, two per
  paragraph at most. **Semicolons** sparingly, joining two halves of one thought.
- **No serial comma** in a plain list — *"Crons, schedules and routines"*. Take it only
  when the last item needs the pause: *"Lowercase, hyphenated, and something you will
  recognise on a bad afternoon"*.
- **Backticks** for anything typed or named by the machine: commands (`ls`), files
  (`SKILL.md`), fields (`description`), values (`medium`), paths (`~/.claude`), and keys
  — `n`, `Cmd-T`, `Ctrl-C`, `↑`, `⇥`. Key combinations are capitalised and hyphenated.
- **Italics** for cross-references to other articles — *Location matters*, *Context rot*
  — never "the article above". Also for her own speech, inside quotation marks: *"Use the
  custom-agents skill to build me an agent."* A prompt she types goes in a blockquote.
- **Tables** take terse lowercase cells under a `| Field | What it decides |` header;
  three columns maximum. **ASCII diagrams** sit in fenced blocks, indented two spaces,
  drawn with `──▶ ├ └ ▼ █ ░`. Fence tagged `bash` only where the line is to be run in a
  shell.

## 8. What the course never does

- **Hype.** No "powerful", "revolutionary", "incredible", "game-changing", no
  exclamation marks. Capability is demonstrated, never adjectived.
- **Hedging.** No "might", "could arguably", "in some cases you may find". Where
  something is unreliable, say so flatly and say what to do instead. No false-friendly
  filler either: no "Let's dive in", "Don't worry", "Great question", "As you can see",
  "simply", "just", "of course", "obviously".
- **Explaining a term before it is needed.** Every concept arrives at the moment it does
  work: `.claude` waits until she has a session, `effort` until she is choosing one. A
  forward reference is a one-clause promise (*"which is the next article"*), not a
  definition delivered early.
- **Summarising itself.** No "in this article we covered", and no recap of any shape.
  The last paragraph is the last point, not a review of the ones before it. And **no
  fact appears twice in the corpus** — where an earlier rule applies
  again, name it in italics and restate only its one-line form: *"That is the walk-up
  rule from* Location matters*. **More is worse.**"*
- **Second-guessing her competence.** No "this may seem complicated". If it is
  complicated, that is the article's problem.

## 9. Read these before writing

- `content/12-agents/02-context.md` — **explaining a concept.** A metaphor introduced
  once then dropped, diagrams doing the work of three paragraphs.
- `content/12-agents/20-building-one.md` — **comparing options.** A table, then one
  bolded paragraph per row, each ending with what that option is *not* for.
- `content/14-subagents/07-step-two-the-workers.md` — **a procedure.** Numbered builds,
  the exact answers to give, and a close naming the principle just demonstrated.
- `content/06-linux/03-why-it-is-better.md` — **arguing a position.** Makes the case,
  hands the other side its best shot under *What is worse*, then refuses its own argument
  in favour of the next article's.
- `content/13-skills/01-start-with-never.md` — **talking the reader out of something.**
  For the opening move, and for how a five-item list can be the spine of a piece.
