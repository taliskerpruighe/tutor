---
id: subagents/step-three
title: Step three — the door
level: Level 2
part: Subagents
section: Build a Chain
order: 8
summary: One more skill, and this one does no work — it spawns the four you already built.
keywords: [exercise, door, custom-skills, spawn, slash opener, subagent, prompt, bundle]
---

# Step three — the door

*v0.1.0*

One more `/custom-skills`, and this one is different in kind. The four
workers each do a job. This one does none. It is the **door** from *The
door*: you type its name, and its steps are subagent spawns that do the
work between them.

Same session, same folder:

```
/custom-skills build me a skill
```

## What to tell it

The interview will ask what the job is first. This is the answer, and it
is worth giving nearly word for word — the order in it is the skill:

> Take the folder I name. Spawn one `bundle-reader` subagent per
> document in it, all at once, each one's prompt opening with
> `/bundle-read` and the document path. Collect what they return. Then
> spawn one `bundle-consolidator` subagent, its prompt opening with
> `/bundle-consolidate`, with the question and every returned list
> pasted in. Give me back what it returns.

The rest of the interview is short. Nothing in writing. Name it
`bundle`. Effort **medium** — the door reads a folder listing and hands
work on; the thinking happens in the workers. This project.

## What it will write

Ask it to show you a spawn prompt when it is finished. You should see
something shaped like this:

```
/bundle-read

document: ~/tutor/bundle/letter-hartley.md
```

Two things about that.

**The first line is a slash command, alone.** That is what fires the
skill inside the subagent, and firing it that way is what carries the
skill's `effort` into the subagent. A prompt that instead says *"use the
bundle-read skill"* in prose runs at whatever effort the session
inherited, and the request you set in step two is lost — no error, no
warning, work that comes back done the ordinary way.

**Everything else it needs is written out underneath.** A subagent is an
independent session. It inherits nothing from yours: not the folder you
named, not the documents, not what the other subagents found. It cannot
ask you a question halfway through. What is in its prompt is what it
has.

One skill per spawn, too. A subagent invocation runs exactly one skill —
a stage needing a second one is a second spawn. That is why reading and
consolidating are two agents rather than one clever agent doing both.

## What you have now

Five things in `~/tutor/bundle/.claude/`: two agents, two worker skills, and a
door that knows the order they go in. Nothing has run yet.

Press `n`.
