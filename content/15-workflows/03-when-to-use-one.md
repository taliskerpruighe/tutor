---
id: workflows/when-to-use
title: When to use one
level: Level 2
part: Workflows
section: What They Are
order: 3
summary: One pipeline, run ten times over or ten times at once, with none of the sessions and none of the management
keywords: [workflow, pipeline, chain, context, books, chronology, session, management]
---

# When to use one

*v0.2.0*

The rule is short: reach for a workflow when there are **multiple
pipelines of the same task**. Not one job with several stages — a chain
already does that — but the identical set of stages, run again and
again on different material.

## The worked example

Say the job is to read, summarise and review ten books. Each book is
its own small chain: a reader goes through it, a summariser writes it
up, a reviewer checks the summary against the text. Nothing unusual
about any single one of those three stages.

The trouble is the number ten. Managing context might call for eight
readers working in parallel, four summarisers picking up their output,
and two reviewers behind them — a perfectly reasonable way to keep any
one agent from holding more of the material than it should. Built as a
subagent chain, that is fourteen agents for the main agent to spawn,
track and hold the results of, all inside one conversation. Fourteen is
enough to blow that agent's own context before the tenth book is done,
which is the exact failure *Context* already told you to watch for.

And even where it does not blow the budget, it is still ten separate
sessions, one per book, each opened by hand with the identical prompt
typed in again. Ten times the setup, ten chances to type the prompt
slightly differently by accident, and nobody watching to notice that
book seven ran with a different set of instructions to book one.

## What a workflow replaces that with

**A workflow is one pipeline, run ten times over — or ten at once, if
the machine can carry it — with no management required.** The script
holds the pipeline once. It does not accumulate fourteen results in a
single conversation's context, because there is no single conversation
holding them; each run of the pipeline is its own script execution,
started and finished on its own. And it does not depend on you typing
the same prompt ten times, because the prompt was written once, into
the script, and the script is what repeats it.

That is the whole test. Not *is this job complicated* — a complicated
job with one path through it is still a chain. The question is whether
you are about to run the same pipeline over and over, by hand, and
would rather hand the repeating itself to something that does not tire
of it or drift partway through book six.

Ten books is not a small run, and it will not finish while you watch
it.

Press `n`.
