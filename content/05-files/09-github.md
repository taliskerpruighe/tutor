---
id: files/github
title: GitHub
level: Level 1
part: Files
section: Version Control
order: 9
summary: A host for the history git already keeps, and everything a host adds once other people can reach it
keywords: [github, remote, git, pull request, issue, repository, host, collaboration]
---

# GitHub

*v0.2.0*

**GitHub** is not a version of git. It is a company that hosts the
remote — the copy of your history described in *How git works* — on
its own servers, so that copy exists somewhere other than your machine.

Git runs entirely on the computer in front of you: every commit, every
branch, the whole history, all local. GitHub is the opposite of local.
It is where a **repository** — the folder and its whole history,
together — can live on a server, reachable by anyone you let in, without
any of them being anywhere near your machine.

## What pushing to it actually does

Pushing sends your commits to that server copy. Pulling brings down
whatever commits are there that you do not have yet. Two people working
on the same repository, both pushing and pulling against the same
GitHub copy, each end up with the other's history on their own machine
— which is the mechanism that makes shared drafting possible without
either of you ever opening the other's laptop.

## What a host adds on top

Git itself has no concept of any of the following. They exist because
GitHub sits a service on top of the plain history:

- **Issues** — a tracked list of problems or tasks against the
  repository, each with its own discussion, so "fix the schedule
  numbering" is a recorded thing rather than a message someone might
  have seen.
- **Pull requests** — a proposal to merge one branch into another,
  opened before the merge happens, so someone else can read the change
  and comment on it first.
- **Other people** — accounts, permissions, and a record of who did
  what and when, none of which a lone folder on a lone machine has any
  way of expressing.

None of it touches the history itself. A pull request is a conversation
*about* a merge, layered over the git model from two articles back; the
merge it eventually produces is an ordinary commit, exactly the kind
*How git works* already described.

## The distinction that matters

Git is the tool. GitHub is one place, among several, willing to host
what the tool produces. Losing access to GitHub does not touch a single
commit sitting on your own machine — the history was never there in the
first place, only a copy of it.

---

That is Version Control, and Files with it — a language is text, an
editor is how you touch it, and git is how every version of it is kept
and shared. Linux comes next: the operating system all of this was
built on, running underneath more of your work than you have noticed.

Press `n`.
