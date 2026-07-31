---
id: hooks/what-it-is
title: What a hook is
level: Level 2
part: Hooks
section: What They Are
order: 1
summary: A script that fires by itself on a trigger, which is the only part of Claude Code that is not a request
keywords: [hook, trigger, script, settings, automation, force, visibility, chains, workflows]
---

# What a hook is

*v0.2.0*

A **hook** is a script that fires on its own, the moment a particular
event happens in a session — not because you asked, and not because
Claude decided to. It sits in `settings.json`, attached to a moment
rather than a question, waiting.

That is a short definition covering a large change. Everything else in
this course is a request.

## Not a request

A rule in `CLAUDE.md` is a strong one, read before the session starts,
but Claude can still misjudge it, or drop it three corrections into a
long conversation. A skill is stronger again, but it only fires if
Claude decides to invoke it — and *Start with never* already told you
that decision is not guaranteed. A custom agent, built exactly for the
job, can still skip a step under the pressure of a long chain.

A hook does not have that problem, because it does not go through
Claude's judgement at all. It is the only mechanism in Claude Code that
can force behaviour rather than request it — blocking a tool call
outright before it runs, or putting text in front of Claude that it has
no chance to skip past. Nothing about a rule, a skill or an agent's own
instructions can do either of those things.

A hook is small on its own. A `PreToolUse` hook that refuses to let
`Bash` run against an uncommitted file is a handful of lines. What
changes is not the size of the script — it is that a script, once
attached to a trigger, is no longer something Claude can talk itself
out of running.

## The framing worth keeping

The useful question is not "what can a hook do" — it is "where have I
lost sight of what is happening." As your chains and workflows grow,
that is most of the time. A subagent chain hands work between three or
four agents that never show you their working. A workflow runs the same
pipeline as a script, without even the illusion of a conversation to
watch.

You know a workflow finished. You do not automatically know it followed
the rule you gave it, checked the file it should have checked, or ran
the review you were relying on somewhere in the middle. Nobody tells
you, in silence, that a step was skipped — it simply was, and the
report at the end reads exactly like the one where nothing was.

A hook is how you get that back. Not by asking harder, and not by
reading the transcript more carefully afterwards — by placing a script
at the exact moment you want checked, so the check happens whether or
not anyone was watching. A hook that fires on `PostToolUse` does not
care whether you read its output. It ran anyway.

## What it is not

A hook is not a smarter instruction, and it is not Claude being asked
more firmly. It runs outside the conversation entirely — an ordinary
script, the kind you could run from a terminal by hand, except that
something else runs it for you, at a moment you chose in advance rather
than one you happened to be watching for.

That moment has a name, and there are eight of them.

Press `n`.
