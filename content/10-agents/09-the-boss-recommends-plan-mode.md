---
id: perms/plan-mode
title: The boss recommends: plan mode
level: Level 2
part: Agents
section: Plans and Permissions
order: 9
summary: A mode built for code that turns out to be just as useful once several agents are the ones being coordinated
keywords: [plan mode, coding harness, subagents, chains, multi-step, dependencies, boss]
---

# The boss recommends: plan mode

*v0.2.9*

Auto mode was the last recommendation, and it is a baseline — set
once, left running underneath everything. Plan mode is not that. It
is a mode you reach for on purpose, for a particular kind of task, and
the Boss reaches for it more than the other four put together.

*The permission modes there are* already placed it on the dial as the
one that touches nothing until you approve what it proposes. This
article is why he reaches for it anyway, deliberately, more often
than the other four combined.

## What it was built for

Plan mode is one of the features that sets a coding harness apart from
a plain chat window. A codebase has files depending on other files,
and a change to one can break three more that nobody mentioned.
Reading the whole job through before touching anything, and writing
that reading down as a plan, is what a harness buys you that a
conversation alone does not.

That was the original problem it solved, and the name still carries
the assumption: a tool for software, for a reader with no code to
write. The Boss kept it anyway, because dependency is not actually a
property of code — a bundle has documents that bear on each other the
same way a codebase has files that do, and a clause drafted before its
definitions are settled is exactly the same mistake as a function
written before the thing it calls.

## Further than code

The Boss found the rest of the case by pointing the mode at ordinary
matters rather than repositories. *Out of the box* already showed the
sharpest instance of it: asked to plan something large, Claude arrives
at splitting the work across subagents on its own, without being told
a chain is even an option. The bigger the job, and the more agents or
workflows worth putting on it, the more plan mode earns its keep
before a single one of them starts — coordination proposed and shown
to you, rather than assembled behind your back.

## When to reach for it

Turn it on whenever what you are asking for is more than one step and
the steps depend on each other — research, then write from the
research; write, then test what you wrote.

> *"Read every document in the bundle, then draft a chronology from
> what you found."*

A single-step request has nothing for a plan to organise. A
multi-step one like that, seen whole before it starts, is worth the
pause every time — even where none of it touches a repository.

What plan mode writes is only as good as what you asked it to plan.
*Prompt dos and donts* is next — a request that plan mode, or anything
else, can actually work from.

Press `n`.
