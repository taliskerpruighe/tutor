---
id: agents/building
title: Building one
part: Agents
section: Custom Agents
order: 11
summary: Ask the custom-agents skill and answer four questions — including which model does which kind of work.
keywords: [custom-agents, skill, build, opus, sonnet, haiku, model choice, tutor]
---

# Building one

*v0.1.0*

Wired into this folder is a skill that writes agent definitions for you.
Open a session here and ask for it:

```bash
cd ~/tutor && claude
```

Then say:

> *"Use the custom-agents skill to build me an agent."*

It takes over from there. It will ask you four things.

## 1. What to call it

Yours to pick. Lowercase, hyphenated, and something you will recognise on
a bad afternoon: `bundler`, `case-reader`, `cite-checker`.

## 2. What it is for

Say it in plain terms — what the agent does, and when you would reach for
it. *"Goes through a disclosure bundle and tells me which documents
matter. I don't want it writing anything."*

That answer becomes the `description`, and the "I don't want it writing
anything" part becomes the `tools` set. Say what it must not do as well as
what it must; both halves land somewhere in the file.

## 3. Which model

The one real decision. The rule is about the **kind of work**, not how
important the matter is.

| Model | Use it to | On a brief, that is |
|---|---|---|
| Opus | analyse and decide | understanding the law and the facts, and planning the writing |
| Sonnet | do the work | drafting the sections |
| Haiku | search and check | bluebook, citations to the record |

Read the third column as one job split three ways.

**Opus analyses and decides.** Give it the authorities and the facts and
have it work out what the argument is and how the brief should be
structured. This is the expensive thinking, and it is where the expensive
model earns it.

**Sonnet does the work.** Handed that plan, it writes the sections. Best
of all when it also has a skill telling it what good looks like — which is
the next part of this course.

**Haiku searches and checks.** Is this citation in the right format. Does
this reference to the record point at the right page. Quick, mechanical,
match-and-report. Nothing beyond that: it is not the one to ask whether an
authority is on point.

Opus and Sonnet also hold more context than Haiku — the table in
*Context* has the numbers — which is another reason the checking job is
the one that goes to the small model.

## 4. Where it lives

It will ask whether the agent should be global — reachable from anywhere —
or belong to one folder. *Location matters* is the whole answer: the
narrowest folder that still covers every session needing it.

If you are unsure, choose the folder. Moving an agent up later is one
file move. Discovering six months on that everything is global is a
clear-out.

## Then it writes it

The skill writes the file, sets the three fields that are always the same,
tells you where it put it, and gives you the line to run:

```bash
claude --agent bundler
```

Open a new tab, run that, and you are talking to something you built.

---

That is Agents. Skills are next — how you teach one of these to do a job
properly, instead of explaining it again every morning.

Press `n`.
