---
id: skills/building-first
title: Building your first skill
part: Skills
section: Building One
order: 9
summary: Ask the custom-skills skill and answer five questions — the important one being how hard it should think.
keywords: [custom-skills, interview, name, effort, medium, high, xhigh, description, user-invocable]
---

# Building your first skill

*v0.1.0*

Wired into this folder is a skill that writes skills for you. Open a
session here and ask for it:

```bash
cd ~/tutor && claude
```

Then say:

> *"Use the custom-skills skill to build me a skill."*

It takes over from there. It will ask you five things, in order, one at a
time.

## 1. What the job is

What you want Claude to do — and, more usefully, **how you do it today.**
Let yourself talk. The answer to "how do you do it now" almost always turns
out to be the skill.

It will push you for the *order* of operations, and it is right to. A skill
that lists things to bear in mind is a weak one. A skill that lists what
you do first, second and third is strong.

## 2. What you already have in writing

House style notes. A precedent letter. The checklist you run before
anything goes out. The template you fill in every time.

It asks this before anything about folders, because the answer decides
them — and it wants the **paths**, not a description. Your material goes
into the skill as your own files. A paraphrase of your house style is not
your house style.

## 3. The name

Yours to pick. It takes what you say and normalises it — lowercase, hyphens
for spaces — then tells you what it landed on. `letter-before-action`,
`exhibit-numbering`, `chronology`. The name and the folder must match, so it
handles both.

## 4. The effort

The one real decision, and the reason this article exists. Effort is how
hard the model thinks before it answers. The rule is about the **kind of
work**, not how important the matter is.

| Effort | Use it for | On a brief, that is |
|---|---|---|
| `medium` | reading and filling in | pulling the dates out |
| `high` | everything else | drafting the sections |
| `xhigh` | planning and being hard on it | working out the argument |

**`medium` reads, finds and fills in.** Pulling dates out of a bundle,
applying a template, checking a list against a rule. The answer is already
in the material; the job is to go and get it, and thinking longer does not
make it more correct.

**`high` does everything else.** The setting when nothing else obviously
fits, and where most of your skills will sit. If you are hesitating between
two rows, take this one.

**`xhigh` plans, reviews and goes looking for trouble.** Working out what
the argument should be. Weighing one authority against another. Reading
your own draft the way the other side will read it. Anything adversarial,
anything where the first plausible answer is the wrong one to accept.

There are five levels in all — `low`, `medium`, `high`, `xhigh`, `max`.
Two of them are not worth reaching for: `low` gives up too much for what it saves,
and `max` costs far more than it returns. It will mention both in a line
and then not offer you either.

One thing to know about all of them. **Effort is a request, not a
guarantee.** A machine setting or an account limit can outrank it, and a
level that is not supported degrades quietly rather than telling you. It
is worth setting. It is not worth relying on.

## 5. Where it lives

Global — reachable from every session on the machine — or belonging to one
folder. *Location matters* is the whole answer: the narrowest folder that
still covers every session needing it. It names the folder you are actually
in when it offers the second option, and recommends that one unless the job
really is machine-wide.

## What it does not ask you

Four fields go in the frontmatter. Two are yours — the name and the effort.
Two it handles itself: it writes the `description`, the sentence other
agents read when deciding whether this skill applies, and it sets
`user-invocable: true` without putting it to you, because that answer is
always yes.

It will show you the description it wrote. Read it. That one sentence
decides whether the skill ever fires at all.

## Then it writes it

It writes the folder — `SKILL.md`, and `references/`, `assets/` or
`scripts/` if the job needs them — copies your material in, and tells you
where the whole thing sits.

After that, you ask for it by name in any session that can see it: *"use
the letter-before-action skill"*. It will also fire on its own whenever
what you ask for matches the description, which is how it will get used
most days.

Press `n`.
