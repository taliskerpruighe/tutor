---
id: files/github
title: GitHub
level: Level 2
part: Version Control
section: Git, Github, and Jujutsu
order: 3
summary: GitHub hosts the remote git already knows how to talk to, and its real value to you is the working software sitting in other people's repositories
keywords: [github, remote, repository, pull request, issue, open source, legal tech, data, host]
---

# GitHub

*v0.2.9*

**GitHub** is not a version of git, and it is not where your files live
either. It is a company that hosts a remote — the copy of your history
described in *How git works* — on servers other people maintain, so
that copy exists somewhere other than your own machine.

Everything about git itself stays local: every commit, every branch,
the whole history. GitHub only becomes relevant the moment you point a
remote at it, and what it gives you in return is reach — a repository
other people can find, without any of them being anywhere near your
computer.

## The remote, plus a service on top

Pushing sends your commits to GitHub's copy. Pulling brings down commits
that are there and not yet on your machine. None of that is new — it is
the fetch, push and pull from *How git works*, aimed at one particular
remote.

What GitHub adds is everything git itself has no concept of: **issues**,
a tracked list of problems or tasks against a repository; **pull
requests**, a proposal to merge one branch into another, opened so
someone can read the change and comment before it happens; and
accounts, permissions and a record of who did what. None of it touches
the history itself — a pull request is a conversation about a merge,
and the merge it eventually produces is an ordinary commit like any
other.

## A gold mine that has nothing to do with your own code

The part worth taking seriously is not that GitHub hosts your work. It
is that GitHub hosts everyone else's — millions of repositories, almost
all of it free to take, and a working coding harness that can search
that pile for you and run what it finds.

None of the examples below are software in the sense you would
recognise as software:

- A script that redacts personal data out of a bundle of exhibits
  before disclosure, built by someone solving that exact problem for
  their own firm.
- A set of small tools for reconciling two spreadsheets of financial
  figures line by line, built for accountants rather than lawyers,
  doing precisely the comparison a matter needs.
- Templates for a cap table, a data room index, or a standard set of
  company resolutions, kept current by people who use them themselves.

Claude Code can search GitHub for something like this, read whether it
still works, and run it against your own files — which turns "nobody
has built this for me" into a search, most of the time, rather than a
project.

## What losing it does not touch

Git is the tool. GitHub is one place, among several, willing to host
what the tool produces. Losing access to GitHub does not touch a single
commit already sitting on your own machine — the history was never
there in the first place, only a copy of it.

Press `n`.
