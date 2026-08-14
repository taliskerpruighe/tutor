---
id: workflows/making-it-thinner
title: Making it thinner
level: Level 2
part: Workflows
section: Building One
order: 6
summary: What Claude hands back first is oversized on purpose — push back on the count, the models, and whether an LLM was ever needed
keywords: [workflow, thinner, cost, model, downgrade, script, push back, haiku, sonnet]
---

# Making it thinner

*v0.2.0*

Do not trust what comes back from *How to build a workflow*'s ask. Left
to itself, Claude will sell you ten times the agents you actually need,
every one of them running on the most expensive model available. Not
out of any dishonesty — it is answering the brief you gave it, which
was to build something that works, and a generous pipeline is one way
to be sure of that.

Working is not the same question as lean. Ask for a workflow, read what
comes back, and then push on it.

## Start with the count

How many agents does this actually spawn, and does each one earn its
place. A pipeline built to be safe against every edge case often has a
reader for a format you will never hand it, or a review stage
duplicating a check the stage before it already did. Ask directly:

> *"How can this be built with fewer agents?"*

## Then the models

Every agent in the draft is worth a second look at what it is running
on. *Building one*'s table still holds: analysing and deciding wants
the expensive model, doing the work wants the middle one, searching and
checking wants the cheap one. A workflow drafted in one pass tends to
put everything on the same model regardless, because that is the safe
default, and safe defaults are expensive when they are repeated across
fourteen agents rather than one.

> *"Which of these can drop to a cheaper model without losing
> anything?"*

## The best question of all

Not every stage in a workflow needs an agent at all. Sorting files by
extension, counting how many documents came in, checking a filename
against a pattern — none of that needs a model to think about it, and a
line of the script can do it directly, with no spawn, no cost, and no
chance of getting it wrong the way a language model occasionally does
on something mechanical.

> *"Which of these steps needs no LLM at all, and can just be part of
> the script?"*

That last question is the one worth asking every time, because it is
the one most likely to have an answer nobody thought to look for on the
first draft.

---

That is Workflows — a chain with a script standing where the main agent
was, run once and trusted to repeat itself exactly, at a cost worth
checking before you let it run unattended. Version Control is next: git,
GitHub and Jujutsu, and the worktrees that let several agents hold the
same project open at once without colliding.

Press `n`.
