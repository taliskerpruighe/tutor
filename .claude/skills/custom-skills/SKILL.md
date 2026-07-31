---
name: custom-skills
description: Build a custom skill for her — interviewing her for the job it does, the material it should draw on, its name, its effort level and where it lives, then writing SKILL.md and any supporting files and telling her how to use it. Use whenever she asks to make, build, write or set up a skill, or asks to teach Claude how to do something the way she does it, or wants her house style, precedents or checklists turned into something Claude follows every time. Do NOT use it to explain what a skill is or how skills work — that is the `tutor` skill — and do NOT use it to build an agent, which is the `custom-agents` skill.
user-invocable: true
---

# Building a custom skill

She has read *Skills*, so she knows a skill is a folder with a `SKILL.md` in
it. She has not written one. You do the writing; she makes the decisions
that are hers.

Interview her first, write second. Never write a partial skill and fill it
in as you go — a half-written `SKILL.md` is a live skill, and it will be
loaded into her next session exactly as it stands.

## What loads when

Every decision below follows from this, so read it once and keep it in mind.

| Layer | When it loads | What it costs |
|---|---|---|
| the frontmatter | at startup, for every skill on the machine | paid always |
| the body of `SKILL.md` | when the skill fires | paid for the rest of that session |
| supporting files | only when something reads them | paid only then |

So the frontmatter is written to be found, the body is written to be short,
and anything heavy goes into a file the body points at.

## The interview

Ask these in order. One at a time, in plain language, and let her answer
before moving on. Use `AskUserQuestion` where the answer is a choice between
options; ask in prose where the answer is hers to describe.

### 1. What the job is

Ask what she wants Claude to do, and how she does it today. Let her talk.
The answer to "how do you do it now" is usually the actual skill — the
steps she takes in order, the things she checks, the mistakes she has
learned to avoid.

Push for the order of operations. A skill that lists considerations is much
weaker than one that lists steps.

### 2. What she already has in writing

Ask this before anything about folders, because the answer decides them.

House style notes. A precedent letter. A checklist. A template she fills in
every time. A list of the phrases her firm uses and the ones it does not.

If she has any of it, it belongs in the skill as a file, not as your
paraphrase of it. Get the paths.

### 3. The name

Hers to pick. Take what she says and normalise it: lowercase, hyphens for
spaces. Tell her what you normalised it to. It becomes both the `name:`
field and the folder name, and those two must match.

If a folder of that name already exists where it is going, say so and ask
before writing into it.

### 4. The effort level

There are five levels — `low`, `medium`, `high`, `xhigh`, `max` — and three
of them are worth using. Offer her these, framed by the kind of work:

- **`medium`** — reading, finding, filling things in. Pulling dates out of
  a bundle, applying a template, checking a list against a rule.
- **`high`** — everything else. This is the default when nothing else fits.
- **`xhigh`** — planning, reviewing, or being adversarial. Working out what
  an argument should be, weighing one authority against another, going
  looking for what is wrong with a draft.

Do not offer `low` or `max`. Mention in one line that they exist and that
neither is worth reaching for — `low` gives up too much for what it saves,
and `max` costs far more than it returns.

Recommend one from what she described, in a line, and let her choose.

Tell her once that this is a **request, not a guarantee** — a machine
setting or an account limit can outrank it, and a level that is not
supported degrades quietly rather than erroring. It is worth setting and
not worth relying on.

### 5. Where it lives

Ask whether this skill should be global or belong to one folder:

- **Global** — `~/.claude/skills/<name>/`. Every session on the machine can
  see it, including sessions where it is irrelevant.
- **This project** — `<folder>/.claude/skills/<name>/`. Only sessions
  launched from that folder, or below it, can see it.

Name the actual folder she is in when you offer the second option. Say the
consequence in one line — every skill a session can see makes that session
slightly worse at everything, because each one has to be weighed on every
question. The right home is the narrowest folder that still covers every
session needing it. Recommend the project unless the job really is
machine-wide.

## The frontmatter you write

Four fields. No others.

```markdown
---
name: letter-before-action
description: Drafts a letter before action in the firm's house style.
  Use when the user asks for an LBA, a letter of claim, or a pre-action
  letter. Do NOT use it for correspondence during proceedings.
effort: medium
user-invocable: true
---
```

**`name`** — hers, normalised, matching the folder name.

**`description`** — you write this. Do not ask her to. She has told you what
the skill does and when she would reach for it; turn that into the field,
then show her the sentence and let her correct it.

This is the only part of the skill that is read before the skill fires, so
it is the entire reason the skill ever gets used. Write it to trigger:

- Say what it does **and** when it applies.
- Use the words she would actually type. If she says "LBA", the word `LBA`
  goes in the description.
- Add an explicit `Do NOT` for the near cases it should stay out of — the
  other skills it would otherwise steal work from.
- Put the main use first. The listing is cut from the back at 1,536
  characters, and what gets cut is trigger vocabulary.
- Be pushy. Models skip skills for work they think they can handle alone, so
  a description that undersells itself is a skill that never fires.

**`effort`** — her answer from question 4.

**`user-invocable: true`** — always. Set it, mention it in a line
afterwards, do not turn it into a question.

## Writing the body

Imperative and second person, addressed to the agent that will run it. Head
each section by the task or the rule it covers, not the topic, so a model
scanning for the step it needs finds it from the heading alone.

Write her steps in her order. Where she gave a rule, give the reason with
it — a reason generalises to the case she did not think to mention, and a
bare instruction gets pattern-matched and then fails there.

**Keep it under 500 lines.** When it runs long the fix is not tighter
prose; it is asking what belongs in a supporting file instead. The body is
paid for on every turn of every session it fires in. A file is paid for only
when read.

## When the skill is a chain lead

Some skills do not do the work. They are the **door**: she types `/<name>`,
and the body's steps are subagent spawns that do the work between them. If
her answer to question 1 described stages handed from one worker to the next,
this is what she is asking for, and it is written differently.

**Every spawn prompt opens with the skill's slash command**, on line one by
itself, followed by a blank line and then the values that spawn needs:

```
/bundle-read

document: disclosure/2019-03-11-letter.md
```

That opener is what fires the skill inside the subagent. A spawn prompt that
names the skill in prose instead runs at the session's inherited effort and
the skill's `effort` request is lost in silence — no error, no warning, work
that comes back done the ordinary way.

Three rules follow from it, and the body states each one:

- **One skill per spawn.** A subagent invocation runs exactly one skill. A
  stage needing a second skill is a second spawn.
- **Everything the subagent needs goes in its spawn prompt, written out in
  full.** A subagent is an independent session; it inherits nothing from
  hers and returns its result as its final output. It cannot ask.
- **Model belongs on the agent, effort on the skill.** An agent may run
  different skills across spawns, so pinning thinking depth in the agent
  definition fixes a value that definition cannot know.

Every worker skill in the chain needs `user-invocable: true` for the door to
fire it this way. It is already always set, so this costs nothing — but say
it once, because it is the reason.

## The three supporting folders

Optional, and any skill can have none, one, or all three.

```
.claude/skills/letter-before-action/
├── SKILL.md
├── references/
│   └── house-style.md
├── assets/
│   └── lba-template.md
└── scripts/
    └── check-dates.py
```

| Folder | What goes in it | The test |
|---|---|---|
| `references/` | style guides, house rules, precedent wording, lookup tables | heavy, and needed only sometimes |
| `assets/` | templates, letter skeletons, example outputs | something the skill fills in or copies |
| `scripts/` | shell or Python the skill runs | the step must come out identical every time |

### The pointer rule

Whenever the body names one of these files, it names **the condition for
reading it** in the same breath:

> Before drafting, read `references/house-style.md`.

> If the claim involves a limitation date, run `scripts/check-dates.py`.

A pointer with no condition gets read every time, which spends exactly what
the folder existed to save.

### About `scripts/`

A script is real code. It runs the same way every time, which is the point —
a date calculation or a formatting pass should not vary with the weather.
But it is also code she cannot read or repair, and a script that breaks
tends to break silently.

So write one only where an identical result every time is genuinely the
requirement, and only when she has asked for it. Everything else is better
as instructions.

## Moving her material in

If she named documents in question 2, put them in the skill rather than
summarising them into the body. Her own house style, in her own words, is
worth more than your account of it.

Copy the file into `references/` or `assets/`, then write the pointer with
its condition.

Two things to tell her when you do:

1. **The copy is now the one that counts.** From here on she edits the file
   inside the skill folder, not the original. If she keeps editing the
   original, the two drift apart and the skill quietly follows the old
   version while looking like it is working.
2. **Word documents are converted.** These folders hold markdown, so a
   `.docx` is converted on the way in and she is told the new filename. If
   it cannot be converted, ask her to paste the text instead of pointing at
   a file the agent cannot open.

## Afterwards

Tell her three things, and stop:

1. Where the folder is, and what is in it.
2. That she can ask for it by name in any session that can see it —
   *"use the letter-before-action skill"*.
3. That it will also fire on its own when what she asks for matches the
   description, which is the normal way it will get used.

## Hard rules

- **Never invent a frontmatter field.** An unrecognised key is ignored in
  silence — the file loads clean and the setting never applies. Use only the
  four fields above.
- **Never write anything before every question is answered.**
- **Never inline material that belongs in `references/`.** It is the most
  expensive mistake available here and the easiest one to make.
- **Never write a `scripts/` file she did not ask for.**
- **Never soften a `Do NOT` she gave you.** It is the half of the
  description that keeps her skills apart.
- Never run `git`, `jj`, `dvc`, or `git-ops`.
