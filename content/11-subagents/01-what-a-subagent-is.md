---
id: subagents/what-it-is
title: What a subagent is
part: Subagents
section: Chains
order: 1
summary: Your main agent can open conversations underneath your own, hand out instructions, and take the finished work back.
keywords: [subagent, main agent, spawn, context, fresh, inherits nothing, return, delegate]
---

# What a subagent is

*v0.1.0*

Everything in this course so far has been about a **main agent**. That is
Claude Code's name for the agent you are having the conversation with —
the one that answers when you type, whether it is the default agent or one
you built yourself.

A main agent can do something you have not seen yet. It can **spawn
subagents**.

## A conversation underneath yours

Spawning a subagent means starting a whole new conversation *underneath*
the one you are in. Your main agent opens it, hands that agent its
instructions, lets it work, and takes the finished work product back.

```
  you  ──►  main agent
              ├──►  subagent
              ├──►  subagent
              └──►  subagent
```

You never leave your own conversation. You are talking to the main agent
before, during and after — the subagents are its doing, not yours. Their
conversations are not yours to join: you did not open them, and you cannot
type into them. What you see at your prompt is your agent going off for a
while and coming back with something.

## Each one starts empty

*Context* said every agent has its own window and begins fresh. A subagent
is an agent, so that holds in full. It inherits **nothing** — not your
conversation, not the files your main agent has read, not the correction
you made ten minutes ago, not even the question you asked in the first
place.

Which gives you the rule that governs the whole of this part. **Whatever a
subagent needs, it must be told** — in the instructions it is spawned
with, written out in full. There is nothing else for it to draw on, and it
cannot come back and ask.

## What comes back is one return

The other half of the same coin. A subagent does not chat. It does the
work and returns **one thing**: its final answer, handed up to the agent
that spawned it, in one piece, at the end.

There is no back and forth with it. No follow-up question halfway through,
no *"actually, make it shorter"*. If what comes back is wrong, the remedy
is not an argument with that subagent — it is a better instruction and
another spawn.

That reads like a limitation. It is nearer the opposite. Because a
subagent's whole life is one instruction in and one result out, several
can run at once without getting tangled in each other, and all the
reading and false starts that go into their work fill up their windows
instead of yours.

One agent, one job, one answer back. That is the piece. What you can build
out of it is the next article.

Press `n`.
