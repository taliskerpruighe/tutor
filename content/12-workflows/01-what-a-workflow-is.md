---
id: workflows/what-it-is
title: What a workflow is
part: Workflows
section: What They Are
order: 1
summary: The same idea as a chain with the driving seat taken out — a script calls every agent instead of one you can talk to
keywords: [workflow, chain, script, pipeline, orchestration, prompt, claude directory, subagent]
---

# What a workflow is

*v0.2.0*

You already know a **chain**: one agent spawning others, each on its own
model, each running its own skill, while the main agent above them holds
the plan and talks to you. A **workflow** is the same idea with the main
agent taken out and a script put in its place.

This is short. It is one distinction, drawn carefully, because everything
in the rest of this part follows from it.

## Who is doing the calling

In a chain, a main agent decides who to spawn next, reads what comes
back, and adjusts — spawn another reader if a document turned up late,
skip the review stage if nothing changed. It is doing that deciding
because you are talking to it, and it can answer you while it works.

In a workflow, a script does the calling. It spawns every agent in the
pipeline, in the order it was written to spawn them, and hands each one
the prompt it was written to hand it. Nothing decides on the fly. The
order was fixed before the run started, by whoever wrote the script, and
the run follows it exactly.

## You are not in the room

That has a consequence worth stating on its own.

**You cannot interact with any agent in the pipeline.** Not the first
one, not the last. The script gives every agent its instructions, and
you are not party to that exchange — there is no prompt of yours for any
of them to read, and nothing they produce arrives in front of you until
the whole pipeline has finished.

A chain still has you at the top of it, one layer removed from the
workers but reachable the whole time. A workflow removes that layer
too. What you get back is the finished thing, or nothing, and the run in
between is not a conversation.

## Where it lives

A workflow is not a separate kind of object living somewhere else on the
machine. It sits in `.claude`, alongside the agents and skills from the
last two parts, and it can see everything a session in that folder can
see — the same custom agents, the same skills, called by name the same
way an agent would call them.

That matters for how one gets built, which is *How to build a
workflow*, several articles from here. For now, the shape is enough: a
chain you talk to while it runs, and a workflow you do not.

The next article is what that trade actually buys you, and what it
costs.

Press `n`.
