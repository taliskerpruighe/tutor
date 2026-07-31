---
id: wiki/this-version
title: This version
level: Level 1
part: This Wiki
order: 2
summary: What this version of the course covers, what it leaves out on purpose, and what a later one adds
keywords: [version, roadmap, agents, skills, subagents, workflows, hooks, plugins, headless, crons, changelog]
---

# This version

*v0.2.0*

This is version **0.2.0**, and it covers the whole path from opening a
terminal for the first time to running an agent that works unattended,
with nobody watching it.

That is a longer road than it sounds, and it runs in two halves. The
first is everything Claude Code sits on top of: the terminal, the
shell, the software your Mac already had and the software it did not,
plain files against proprietary ones, Linux underneath all of it, and
then what a model and a harness actually are before Claude Code is
named as one particular example of both. None of that is Claude Code
yet. It is what makes the rest of this course legible once Claude Code
arrives.

The second half is the part you came for. **Agents**, which do the
work; **skills**, which teach an agent something once and keep it
taught; **subagents**, which chain agents together into something
bigger than a conversation. Then **workflows**, the scripted version of
a chain; **hooks** and **plugins**, which wire all of it into the rest
of your machine and share it with other projects; and **headless
sessions**, which run any of the above with no chat window open at all.

## What it deliberately leaves out

Everything above happens because you are sitting there, asking for it.
This version stops short of work that starts itself — crons, schedules,
routines that fire on their own while you are in a meeting or asleep.
That is a real capability and a real later version, not a gap left by
accident.

## Why the order matters

Each part assumes the one before it. Software before Linux, because
the Linux case leans on packages already having been explained. Agents
before Skills, because a skill is something you hand to an agent, not
a thing on its own. Skip ahead and a later article will use a word it
never defined for you — press `n` and you will not have that problem.

This version is also organised into more parts than the last one was,
fifteen against a handful. That is not the same course cut into
smaller pieces for its own sake. Some of what used to sit inside one
broad part — the terminal, the shell, what a model actually is —
turned out to need its own room once it was written out properly
rather than assumed.

## Returning after an update

If you have read this course before and are back for a new version,
you do not need to reread all of it. The next article is the delta.

Press `n`.
