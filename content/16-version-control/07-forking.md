---
id: vcs/forking
title: Forking
level: Level 2
part: Version Control
section: Worktrees
order: 7
summary: A forked subagent starts from the conversation you are already in rather than an empty one, which is worth it for a second opinion, not for splitting a job up
keywords: [fork, forked subagent, second opinion, parallel, github, chain, context, specialisation]
---

# Forking

*v0.2.9*

You already know the word from GitHub, where **forking** a repository
gives you your own copy of it, identical to the original at the moment
you took it, free to diverge from there onward. A **forked subagent**
works on the same principle, applied to a conversation instead of a
repository.

*What a subagent is* stated the ordinary rule: a subagent starts empty
and inherits nothing, not even the question you asked. A forked one
breaks that rule on purpose. It starts as a copy of the conversation
you are already in — everything read, everything decided, everything
corrected so far — and runs on from there as its own, separate thread.

## How it differs from an ordinary subagent

An ordinary subagent is briefed. You write out, in full, whatever it
needs to know, because it has nothing else to draw on. A forked one is
not briefed in the same sense — it already has what you have, up to the
moment of the fork, and whatever instruction you give it on top is the
only new thing it is told.

## Not for breaking a job up

Do not reach for forking to split a large task into pieces. That job
belongs to an ordinary chain, where each worker is given a narrow,
different instruction and reads only what its own piece requires — the
whole point of *Chain engineering*. A fork carries your entire
conversation with it, which is the opposite of a small, specialised
context, and costs the tokens to match.

Specialisation is the other reason to reach for an ordinary subagent
instead: a worker briefed to check citations and nothing else does that
one job better for not having a whole conversation's worth of other
concerns sitting in its window. A fork gives every continuation the
same starting point on purpose, which is precisely wrong when what you
actually wanted was several different narrow jobs done at once.

## For a second opinion, or a second attempt

Fork where you want more than one continuation of the exact same
starting point. Ask two forks to review the same draft agreement
independently, each blind to what the other one thinks, and compare
their answers afterward rather than getting one read coloured by a
second person in the room. Or fork twice on a bug neither obvious fix
has confirmed, let one fork try each fix from the identical state, and
keep whichever one actually works.

---

That is Version Control — git's history, GitHub's copy of it, jj's
smoother way of keeping it, and the worktrees and forks a harness builds
on top once several agents want a hand in the same work at once. Hooks
come next: the one part of Claude Code that does not wait to be asked,
firing on its own the moment a particular event happens.

Press `n`.
