---
id: subagents/out-of-the-box
title: Out of the box
part: Subagents
section: Chains
order: 3
summary: Your default agent already spawns subagents — ask it to, or enter plan mode and watch it propose them itself.
keywords: [default agent, plan mode, shift+tab, plan, spawn, split the work, generic, claude]
---

# Out of the box

Nothing needs building for any of this.

The plain `claude` you launch every morning already spawns subagents. It
has the tool, it knows how to use it, and it will reach for it on a job
big enough to warrant it without being taught anything. There are two ways
to get it going, and one of them is more reliable than the other.

## 1. Ask it

The blunt way. Give it something large and tell it how you want the work
carried:

> *"Go through every document in this bundle and tell me which ones
> touch the indemnity. Split the work between subagents."*

Watch what happens underneath your prompt. A row of agents appears, each
one named `claude` — generic, all identical, all on whatever model the
session is using — and each goes off with its share. They finish at
different times, their results come back to your agent, and your agent
tells you the answer.

That is a chain. A plain one, with no design behind it, but every idea in
this part is already visible in it.

## 2. Plan mode

The better way, and the one to build a habit around.

```
shift+tab
```

Or, if you would rather type it:

```
/plan
```

Plan mode changes what happens when you ask for something. Instead of
starting straight in, Claude thinks the job through first and writes you a
plan — the stages, in order, and what each one does. Nothing is touched
until you have read it and said yes.

It is worth having on its own merits: you find out what it thinks you
asked for while that is still cheap to correct.

## What it changes here

A plan for a job of any real size almost always has subagents in it. Asked
to think a big task through properly, Claude arrives at splitting it up on
its own — so plan mode is the dependable way to get a chain, without
asking for one.

And because the plan is shown to you before anything runs, you get to read
the chain proposed. How many agents, doing what, in what order. Which is
the point at which you can say *that middle stage should be two* or *have
the checking done separately*, and have it change before a single file is
touched.

Approve it and it runs. Say no and it plans again.

Free chains, then, and a look at them first. What you cannot get this way
is control over the details — which model each stage runs on, and which of
your skills it uses. That is the next article.

Press `n`.
