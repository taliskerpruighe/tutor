---
id: counter/nested-subagents
title: Subagents spawning subagents
level: Level 2
part: Counter-Recommendations
order: 3
summary: A structural fix for a feature the Boss says to switch off entirely, with the bug that made him say it
keywords: [subagent, nested subagents, agent, tools, chain, spawn, cost, scope, bug, custom agent]
---

# Subagents spawning subagents

*v0.2.3*

A subagent can spawn subagents of its own. Each of those can spawn
subagents of its own, and so can theirs — five levels deep, by design.
One agent, then its workers, then their workers, then their workers'
workers, then a fifth layer under that.

The Boss says do not use it. There is no switch to flip for this one —
the fix sits in the agent files themselves, not in a setting.

## Build workers that cannot delegate

You met the `tools` list already, in *The definition file* and *The
fields that matter*: the set of things an agent is allowed to do, and
`Agent` is the entry that lets one agent call another.

Build a dedicated custom agent — one that is only ever called as a
subagent, never addressed directly — and leave `Agent` off that list.

```
tools: Read, Glob, Grep
```

An agent with that list can read, search and report. It cannot spawn
anything, because the one tool that would let it is missing.

## Nobody is watching five levels down

*Watching* established the limit on what a headless run shows you: only
what surfaces, and a wrong answer at the top tells you something went
wrong without telling you where. A chain five levels deep is that
problem multiplied by five. Nothing about level three, four or five
reaches you at all — not a name, not a token count, not a minute spent.

An agent you never authorised can spend an afternoon on work you never
scoped, on a model you did not choose, and the report that reaches you
at the top reads like any other report. Cost and scope run away
precisely where nobody is looking, because nobody can be.

## A bug with no name

There is also a plain defect, not a design trade-off. When a subagent
spawns a second subagent, and that second one finishes, the first
subagent is sometimes told the wrong job is done — the result handed
back names the other one. Nothing announces the mix-up. No error, no
warning, nothing in red. What climbs back up to your main agent reads
exactly like the run where it did not happen.

> **From the Boss:** *"I don't nest agents I can't see. You lose the
> thread on cost and scope the moment you go past one layer down, and
> you don't find out until the invoice or the output tells you — and by
> then it's already happened."*

Press `n`.
