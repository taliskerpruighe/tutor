---
id: files/how-git-works
title: How git works
part: Files
section: Version Control
order: 7
summary: Commits chain into history, branches split off it, and a remote is the same history living somewhere else
keywords: [git, commit, history, branch, merge, remote, github, model]
---

# How git works

*v0.2.0*

Three ideas carry the whole of git. Not the commands — those are covered
where a skill needs one. The model underneath them, which is what makes
the commands make sense once you meet them.

## Commits chain into history

Each commit points back to the one before it, so the whole thing forms
a chain:

```
  commit 1 ──▶ commit 2 ──▶ commit 3 ──▶ commit 4
  first draft   added        fixed       indemnity
                schedule     dates       clause added
```

That chain is the **history**. Walk it backward and you are reading the
document's whole life, one note at a time, in the order it actually
happened rather than the order the filenames suggest.

## A branch is a second line running alongside

A **branch** is a separate line of commits that splits off the chain at
some point and runs on its own, without touching the line it split from.
Draft a speculative rewrite of a clause on a branch, and the version
everyone else is working from does not move until you decide to bring
the branch back in.

```
                       ┌─▶ commit 3a ──▶ commit 3b  (branch)
  commit 1 ──▶ commit 2┤
                       └─▶ commit 3  ──▶ commit 4   (main)
```

Bringing a branch back in is called **merging** — folding its commits
into the line it split from, so the history reads as one line again.
Two branches can touch the same paragraph in incompatible ways, and git
will say so rather than guess; sorting that out by hand is the one part
of this model with no shortcut.

## A remote is the same history, elsewhere

Everything so far lives on one machine. A **remote** is a copy of that
same history kept somewhere else — another machine, or a server neither
of you owns — that you can push commits to and pull commits from.

That is the piece that turns a private log into something shared. Two
people can each hold the full history on their own machine, both push
their commits to the same remote, and both end up with a complete
record of what the other one did and why. It is also what protects the
log itself: lose the folder on your own machine and the remote still
has every commit in it.

## What none of this needed

No mouse. Every one of these — a commit, a branch, a merge, a push to a
remote — is a single typed command, which is exactly why this belongs
in a course about a terminal rather than a course about an application.
A chain of commits is not read by clicking through folders named `v1`,
`v2` and `v2-final` — it is read straight, in order, by the tool that
built it.

Git itself asks you to remember a fair number of those commands and
their flags in the right order. The next article is a different tool
built on the exact same history, engineered to remove that particular
cost.

Press `n`.
