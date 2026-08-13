---
id: vcs/git-and-the-harness
title: Git and the harness
level: Level 2
part: Version Control
section: Git, Github, and Jujutsu
order: 5
summary: A folder becomes a repository and a coding harness gets three things it did not have before — a history to undo into, room for several agents on one file, and drafts it can merge into one
keywords: [harness, claude code, repository, undo, parallel agents, cherry pick, merge, subagent]
---

# Git and the harness

*v0.2.9*

Claude Code is a **coding harness** — a program built to run an agent
against files on disk — and most harnesses of that kind assume a repo
underneath them, whether or not you ever mention git to them yourself.
*What git is* already named the reason: undoing an agent's edit is only
possible if something recorded what the file looked like beforehand,
and a folder that is not a repo has nothing recording that.

Turning a folder into a repository is one command, `git init`, and it
is worth understanding as a switch rather than a formality — one flip
that unlocks several things at once, not only the history you already
know about.

## Change history, on tap

The most direct unlock is the one already covered: every edit an agent
makes becomes a commit, or part of one, and every commit is a point you
can step back to. That turns "the agent rewrote the wrong clause" from
a problem you notice and cannot fix into one you notice and reverse.

## Several agents on the same file

A repo also makes it possible for more than one agent to work on the
same file at the same time without either overwriting the other. Left
to a single shared folder, two agents editing one document at once
would each silently stomp on the other's changes — whichever saved last
wins, and nothing tells either of them it happened. A repo, combined
with the right setup, gives each agent its own working copy of the file
to edit, so neither ever sees the other mid-edit.

## Several drafts, then one

The same underlying feature also lets you run the same task twice, or
three times, deliberately — one agent drafting a clause one way,
another drafting it a different way, from the same starting point — and
then take the best pieces of each and fold them into a single version.
Git's merge is what makes that folding an ordinary operation rather
than a manual cut-and-paste between three open files.

## What actually does this

None of the three above happens from `git init` alone. Each needs a
particular setup on top of the plain repository, and each earns its own
article: one where several agents share a project by each getting a
working copy of their own, and one where a single agent's conversation
is copied so more than one version of it can run in parallel.

Neither is the default. Left alone, a harness runs one agent against
one folder, the same way it always has — the repository sits underneath
it either way, but nothing reaches for these particular features until
you ask.

The next article is the first of those — working copies, several at
once, off the same repository.

Press `n`.
