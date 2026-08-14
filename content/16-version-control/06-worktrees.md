---
id: vcs/worktrees
title: Worktrees
level: Level 2
part: Version Control
section: Worktrees
order: 6
summary: A worktree gives one repository several working folders at once, so agents that need to touch the same project simultaneously never collide
keywords: [worktree, git worktree, subagent, isolation, frontmatter, parallel, main agent, branch]
---

# Worktrees

*v0.2.9*

A **worktree** is a second working folder attached to a repository you
already have, checked out to its own point in the history, independent
of the first folder on disk even though both draw from the same
underlying commits. Edit a file in one and the other does not see it
until something merges the two back together — exactly the collision
*Git and the harness* named as the thing a shared folder cannot prevent
on its own.

## What it is

One repository can have any number of worktrees, each a plain folder
you can `cd` into like any other, each with its own copy of the files
on disk. They are not clones — a clone duplicates the whole history a
second time; a worktree shares it, and only the files themselves are
separate. Commit inside one and the commit lands in the one shared
history, visible to every other worktree attached to the same
repository, even though none of them saw the edit while it was still
in progress.

## How it works in Claude Code

There are two doors into this.

For a main agent, start the session with its working directory set to
the worktree itself, rather than the repo's usual folder — the agent
then reads and writes files inside that folder alone, unaware anything
else exists alongside it.

For a subagent, the easier route is a line in its definition:

```
isolation: worktree
```

Set that in the frontmatter and a subagent spawned from it gets its own
worktree automatically, without you creating one by hand each time.
Spawn three of that subagent at once and three worktrees appear, one
per instance, cleared away again once each has returned its answer.

## When not to reach for it

Skip it for a pipeline where agents work in sequence — a writer, then
an editor, then a formatter, each one starting only after the last has
finished. Sequential agents never touch the same file at the same
moment, because there is no moment where two of them are both working.
A worktree solves a collision that a sequential chain was never going
to have — setting one up for a writer-then-editor-then-formatter
pipeline buys nothing beyond an extra folder to keep track of and
another merge to remember to do at the end.

## When to reach for it

Reach for it when agents genuinely need the same project open at the
same time: one drafting the opening sections of a long document while
another drafts the closing ones, each working under its own worktree,
so neither can see the other's half-finished paragraph mid-edit. What
comes out the far end is two sets of changes on the same underlying
repository, ready to be brought back together.

Press `n`.
