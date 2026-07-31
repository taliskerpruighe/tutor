---
id: ai/what-a-harness-consumes
title: What a harness consumes
level: Level 1
part: Agentic AI
section: Harnesses
order: 7
summary: A harness wants almost nothing from your machine, until you ask it to run many of itself at once
keywords: [cpu, ram, harness, laptop, hardware, agents, parallel, machine]
---

# What a harness consumes

*v0.2.0*

A harness is an ordinary program. It reads files, runs commands, keeps
track of a conversation, talks over the network. That needs a processor
and some memory — **CPU** and **RAM** — and not much of either. Your
Mac has plenty. So does a ten-year-old laptop.

That is the whole answer for one harness, running one conversation. It
is not the whole answer once you notice what the rest of this course is
building toward.

## One is cheap. Many is not.

Nothing stops you from opening a second terminal tab and starting a
second Claude Code session, on a second matter, while the first is
still running. Nothing stops you from opening a third. Each is a
separate ordinary program, and CPU and RAM are cheap enough that a
laptop shrugs off a handful of them.

Subagents push the same idea further, from inside a single session:
one harness handing pieces of a job to others, several loops turning at
once rather than one loop turning fast. That is a subject for later in
this course. What matters here is only the shape of the cost — it
scales with **how many agents you are running**, not with how capable
any one of them is.

Run enough of them at once — a chain working overnight, a fleet of
subagents split across a large project — and a laptop stops shrugging.
Not because any single harness got heavier. Because you are no longer
running one ordinary program. You are running twenty.

A busy afternoon of one matter, one terminal tab, costs you nothing
worth noticing. Twenty tabs, each running its own agent against its own
folder, costs you the CPU and RAM of twenty ordinary programs, all
wanting attention from the same processor at the same time. The laptop
does not fail cleanly at that point. It slows — everything running on
it slows, including whatever you were doing that had nothing to do
with any of the agents.

## The model is still the expensive part

None of this touches the model. Wherever the harness is running, the
model itself sits in a data centre, on hardware you were never going to
own — *What a model consumes* covered why. Running more agents at once
multiplies the harness's small appetite, not the model's enormous one.

So the honest shape of the problem is this: the model's appetite is
fixed and someone else already pays it. The harness's appetite is small
per copy and multiplies with every copy you run. A ten-year-old laptop
answers the first question comfortably and the second one badly.

There is an answer to the second question, and it is not a better
laptop.

Press `n`.
