---
id: workflows/cost
title: What they buy and what they cost
part: Workflows
section: What They Are
order: 2
summary: A fixed script cannot forget a step, and that guarantee is paid for in agents that take longer to start and cost more to run
keywords: [workflow, consistency, quality control, cost, bloat, spawn, script, chain]
---

# What they buy and what they cost

*v0.2.0*

The upside of a workflow is one word: **consistency**. The script forces
every spawn and forces the order they happen in, so nothing gets
skipped, ever, because there is nothing left to a judgement call. A
chain can decide, mid-run, that the review stage looks unnecessary this
time. A workflow cannot decide anything — it does what it was written
to do, the same way, on the tenth run as on the first.

That is real. A step a script cannot skip is a step that genuinely
never gets skipped, which is a stronger guarantee than a step an agent
usually remembers to run.

## What that costs

Now the other side, and it is the reason this article exists rather
than the last one being enough on its own.

**Workflows are slow and expensive.** The same agent, doing the same
job, takes longer to start and stop inside a workflow than it does as
an ordinary subagent in a chain. Spinning up the scripted machinery
around each spawn adds overhead a chain simply does not carry, and that
overhead is paid on every single agent in the pipeline, not once at the
start of the run.

And a workflow almost always involves far more agents than a subagent
chain doing comparable work — that is the next article's whole subject,
but the shape of it is: where a chain might spawn three or four workers,
a workflow built to cover every case tends to spawn considerably more,
because the script has to have an agent ready for a branch it may never
take. More agents, each one slower to start than its chain equivalent,
and the two costs multiply rather than add.

| | Chain | Workflow |
|---|---|---|
| Who decides the order | the main agent, live | the script, fixed in advance |
| Can you interrupt it | yes | no |
| Agents per run | few | many |
| Start-up cost per agent | low | higher |
| What you get for it | judgement | consistency |

## The trade in one line

A chain is cheaper and adapts. A workflow is more expensive and does
not need to — because it was built to already cover what adapting would
have covered.

Which is not an argument against either. It is an argument for knowing
which job you are looking at before you reach for one, and that is
exactly what the next article settles.

Press `n`.
