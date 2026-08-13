---
id: prompt/engineering
title: Prompt engineering
level: Level 2
part: Agents
section: Prompts
order: 11
summary: Three pieces, always in the same order — context, objectives, traps — and a prompt with all three rarely needs a second try.
keywords: [prompt engineering, context, objectives, traps, structure, order, chronological]
---

# Prompt engineering

*v0.2.9*

The best version from *Prompt dos and donts* had two pieces still
missing. Put all three together and you have the whole shape a serious
prompt takes: **context**, then **objectives**, then **traps**. In that
order, every time.

None of the three is optional and none is difficult on its own. What
takes practice is doing all three, every time, rather than the one
that happens to come to mind first.

## Context — why the task

Context is anything the agent needs before it starts: the history of
the matter, the goal behind the request, the reason this task exists
at all. If there is a document to read first, a prior decision to
respect, or a piece of research to do before touching anything, it
goes here.

Leave it out and the agent still produces something — but against the
wrong picture. A drafting request with no context reads the same to
the agent whether it is a first draft or the fourth revision of a
clause the other side has already rejected twice, and it cannot tell
you which one it assumed.

## Objectives — what you are asking for

This is where the instructions go, but as objectives rather than
commands — the distinction *Prompt dos and donts* drew. List them, and
list them **chronologically**: the order the agent should tackle them
in, not the order they occurred to you while typing.

```
1. Read the indemnity clause in the current
   draft.
2. Rewrite it to cap liability at the contract
   value.
3. Flag any other clause that references the
   old cap.
```

A flat list without an order forces the agent to guess at sequence,
and a guess about sequence is exactly the kind of silent wrong turn
this course keeps warning about.

## Traps — what to avoid

Traps are the things the agent must not do, stated as plainly as the
objectives are. Do not touch the definitions section. Do not rename
any party. Do not assume the client wants the aggressive version.

A trap is not a milestone to hit — it is a boundary not to cross, and
the two read differently on the page for a reason. Put objectives
first and traps last, so the agent has already understood the shape
of the task before it is told where the edges are.

Traps are also where a single sharp line does more work than a
paragraph of caution. "Do not touch the definitions section" cannot be
misread. "Be careful with the definitions section" can, and it is the
agent that decides what careful meant, after the fact.

## Why the order matters

Context before objectives, because an objective read cold means
something different from the same objective read with the history
behind it. Objectives before traps, because a boundary is easiest to
respect once you already know what you are trying to do inside it.

Get used to writing prompts in this shape and you stop needing to
think about it — the three headings arrive in order because the task
does. The next article is about what to do when all three run long
enough that typing them in the chat box stops being practical.

Press `n`.
