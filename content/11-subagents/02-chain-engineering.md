---
id: subagents/chain-engineering
title: Chain engineering
level: Level 2
part: Subagents
section: Chains
order: 2
summary: Party Trick #6 — stack agents and their skills without limit, and Claude stops doing tasks and starts taking on projects.
keywords: [party trick, chain engineering, stack, orchestrate, opus, sonnet, project, this wiki]
---

# Chain engineering

*v0.1.0*

> **Party Trick #6 from the Boss: chain engineering.** One agent spawns
> the next, each on its own model and running its own skill. Stack them
> and Claude stops doing tasks and starts taking on projects.

This is the first of the Party Tricks that is a proper superpower. The
others sharpen something you were already doing. This one changes the size
of the thing you are allowed to ask for.

## Why stacking is the whole of it

A single agent is bounded by one window. Everything it reads, drafts and
redrafts goes into the same brainspace, and *Context rot* is what happens
when you push a big job through it — the work gets worse the longer it
runs, exactly when you need it not to.

A chain has no such ceiling. Each stage gets a clean window, does one
thing well, and hands up a result. The agent above it holds the plan and
almost none of the material. Add another stage and you have not made the
existing ones any worse.

That is what "without limit" means here. Not that the machine is
infinite — that the thing which used to degrade no longer does, so the
question moves from *is this too big to ask for* to *what are the stages*.

## You are reading one

This wiki was built by a chain.

A single main agent on Opus held the outline and wrote none of it. It had
its own skills — planning, deciding, reviewing, debugging — and its job
was to work out what needed doing, in what order and by whom. Underneath
it sat several subagents on Sonnet, each armed with a separate skill: to
design the reader, to code it, to write the articles, to edit them, to
render them, to test them.

```
  outline
     │
     ▼
  main agent   opus
    plan · decide · review · debug
     ├──►  design    sonnet
     ├──►  code      sonnet
     ├──►  write     sonnet
     ├──►  edit      sonnet
     ├──►  render    sonnet
     └──►  test      sonnet
```

Look at the model column. The expensive brain is used once, for the
thinking, and every hour of actual production runs on the cheaper one —
which is *Building one*'s table doing its job at scale rather than one
agent at a time.

The article on your screen came out of the box marked **write**, was gone
over by **edit**, and reached your eyes through **render**. You are
reading the output of the thing this article describes.

## From an outline

Worth dwelling on what went in at the top: an outline. Not a specification,
not a design, not a folder of drafts. A list of what the parts were and
roughly what each should cover.

That is the shape of the ask a chain makes possible. You describe the
finished thing and the stages that get you there, and the chain does the
rest — the deciding on Opus, the producing on Sonnet, the checking on
Haiku.

Which sounds like a great deal of setting up. Most days it is none: your
default agent can already do it. That is next.

Press `n`.
