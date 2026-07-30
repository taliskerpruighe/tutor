---
id: skills/frontmatter
title: The frontmatter
part: Skills
section: When To Build One
order: 3
summary: Four fields do real work in a SKILL.md — name, description, effort, and user-invocable, which is always true.
keywords: [frontmatter, name, description, effort, user-invocable, yaml, settings, ignored silently]
---

# The frontmatter

A `SKILL.md` file is built exactly like an agent definition file, and
for the same reason. Two parts, always, in this order: the
**frontmatter** between the `---` lines, and the **body** after it.

The body is free — prose, in whatever shape suits the job. The
frontmatter is not. It is YAML, the same `key: value` format as
before, and the spelling of each key has to be exact.

The documentation offers you a good many keys. As with agents, the
Boss went through them the hard way, and four survived.

```
---
name: letter-before-action
description: Drafts a letter before action in
  the firm's house style. Use when the user
  asks for an LBA, a letter of claim, or a
  pre-action letter. Do NOT use it for
  correspondence during proceedings.
effort: medium
user-invocable: true
---
```

| Field | What it decides | Your setting |
|---|---|---|
| `name` | what it is called | you choose |
| `description` | when it fires | you choose |
| `effort` | how hard it thinks | you choose |
| `user-invocable` | can you call it | always `true` |

Three you decide each time. One is the same on every skill you will
ever own.

## `name`

What you type when you want it — *"use the letter-before-action
skill"* — and what an agent uses when it reaches for it. Lowercase,
hyphens for spaces.

One rule beyond that: **it must match the folder name.** The folder is
`letter-before-action/`, so the name is `letter-before-action`. A
mismatch is a skill that will not answer to either.

## `description`

One or two sentences on what the skill does and when it applies. This
is the field that matters most, and not for the reason you would
guess.

It is the **only part of the skill read before the skill fires**. The
settings of every skill on the machine are in front of the agent from
the moment it starts; the instructions are not opened until something
decides this is the skill for the job. That decision is made on this
sentence alone.

So write it as a trigger, not a job title:

- Say what it does **and** when it applies.
- Use the words you would actually type. If you say "LBA", the word
  `LBA` belongs in the description.
- Add an explicit **`Do NOT`** for the near cases — the neighbouring
  skill it would otherwise steal work from.
- Be pushy. A skill that undersells itself is a skill that never
  fires, because the agent will decide it can manage without.

## `effort`

How hard the skill thinks when it runs. There are five levels, and the
right one depends on the work: reading and filling things in is not
the same job as working out what an argument should be.

You set it once, per skill, rather than deciding it per question —
which is the same relief `model` gives you on an agent. Which level
suits which kind of work is *Building your first skill*, where you
will be choosing one — and being recommended one — rather than reading
about it.

## `user-invocable: true`

Always. It is what lets you ask for the skill by name instead of
waiting for it to notice you. There is no reason to leave it off and
it is a nuisance to discover you did.

## The silence

The warning from *The definition file* applies here without a word
changed. **A key Claude Code does not recognise is ignored in
silence.** No error, no warning. The file loads perfectly and the
setting you invented was never read by anything.

Which is why the list is four fields and not five. Not because the
others are discouraged — because they do nothing, convincingly.

Press `n`.
