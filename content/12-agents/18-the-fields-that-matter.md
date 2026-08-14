---
id: agents/fields
title: The fields that matter
level: Level 2
part: Agents
section: Custom Agents
order: 18
summary: Party Trick #3 — six frontmatter fields do real work, and the rest is decoration.
keywords: [name, description, model, background, memory, tools, party trick, agent engineering, subagent]
---

# The fields that matter

*v0.1.0*

> **Party Trick #3 from the Boss: agent engineering.** Six fields. Set
> those, ignore the rest, and every agent you write behaves.

Here they are in full, in a working definition:

```
---
name: bundler
description: Reads a disclosure bundle and
  reports what is relevant. Use for review,
  never for drafting.
model: haiku
tools: Read, Glob, Grep, Agent
background: true
memory: user
---
```

| Field | What it decides | Your setting |
|---|---|---|
| `name` | what you call it | you choose |
| `description` | when another agent picks it | you choose |
| `model` | which brain runs it | you choose |
| `tools` | what it can do | a set, never all |
| `background` | can it be sent off | always `true` |
| `memory` | does it learn | always `user` |

Three you decide each time. Three are the same on every agent you will
ever write.

## `name`

What you type after `--agent`, and what another agent uses to call this
one. Keep it lowercase and hyphenated, and make it match the filename.

## `description`

One or two sentences on what this agent is for. You will rarely read it —
**other agents** do. When one of your agents needs a job done and looks
around for something to hand it to, this is what it reads to decide.

So write it as a trigger, not a job title. *"Reads a disclosure bundle and
reports what is relevant. Use for review, never for drafting."* Say what
it is for, and say what it is not for; both halves get used.

## `model`

Which model this agent runs on. Set it and it is settled — no more
switching mid-session because the work got harder, and no more forgetting
to switch back when it got easier again.

Leave it out and the agent runs on whatever the session was already using,
which is exactly the thing you were trying to stop doing.

## `tools`

The list of things this agent is allowed to do. Read files. Write files.
Run commands. Search the web.

Leave it out and the agent gets **everything**, which is the default agent
again with extra steps. Give it a set instead — the smallest one that
covers the job.

```
  reads and reports    Read, Glob, Grep, Agent
  writes documents     + Write, Edit
  runs things          + Bash
```

An agent that cannot write cannot overwrite your draft by mistake. That is
not a hypothetical benefit; it is most of why the field exists.

Note `Agent` on every line. That is the tool that lets one agent call
another, and you want it on everything you write — an agent without it can
only do its own work, never delegate a piece of it.

## `background: true`

Always. It makes the agent available to be sent off on a job by another
agent — working in the background while the conversation carries on in
front of you.

There is no cost to setting it and it is a nuisance to discover you did
not. Set it on everything.

## `memory: user`

Always. This is the one that breaks the rule you learned in *What an agent
is* — that every agent starts fresh, knowing nothing of any other session.

With `memory: user`, this agent keeps notes across its own sessions. The
bundler you use on Monday remembers what it worked out on Friday. The
context still empties every time; what persists is what it chose to write
down.

## You do not have to remember any of this

Six fields, three of them fixed. It is not much — and you are not going to
type it by hand anyway.

There is a skill for it.

Press `n`.
