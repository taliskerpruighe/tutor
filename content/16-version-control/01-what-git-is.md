---
id: files/what-git-is
title: What git is
level: Level 2
part: Version Control
section: Git, Github, and Jujutsu
order: 1
summary: Git is not only for code, and the Boss treats it as the one indispensable safeguard against an agent's own trigger-happy edits
keywords: [git, version control, commit, history, linus torvalds, linux, google drive, ai agents, insurance]
---

# What git is

*v0.2.9*

You have already met **git** in passing — *Packages* put its one-line
form on record: git keeps every version of every file, with a note on
why each one changed. This part is what stands behind that line, at the
depth a Level 2 reader can use.

Git was written by Linus Torvalds, the same person who wrote Linux, to
manage the source code of Linux itself. That parentage is why almost
everyone who has heard of git assumes it is a coding tool. It is not —
it is a version-control tool that coding happened to need first.

## Not only for code

Nothing about git reads the meaning of a file. It reads lines of plain
text and notes which ones moved, which is exactly as true of a
memorandum, a spreadsheet exported to CSV, or a set of drafting notes as
it is of a script. Combine it with a coding harness — Claude Code, doing
the actual editing — and the pairing works on any field that produces
drafts worth keeping a history of, not only software.

That combination is the whole reason this part exists at Level 2 rather
than staying where it started. A programmer reaches for git because the
code demands it. You reach for it because an agent is now the one
holding the pen, and everything from here follows from that one
difference.

## What a sync folder does not do

A cloud drive keeps the current state of a file and a short recent
history it prunes on its own schedule. Open the version from three
weeks ago and it may no longer be there. Git keeps the whole
sequence, indefinitely, under your own control rather than a service's
— every draft from the day the matter opened, still reachable by name
rather than by luck.

> **From the Boss:** *"If nothing else, use it for this: it is the one
> thing standing between you and an agent's trigger-happy edits. Every
> version an agent touches is a version you can get back to. Without
> it, you are trusting the model to be right the first time, every
> time."*

That is not a risk to be managed once and forgotten. Every session in
this course runs an agent that edits files directly, and every one of
those edits is reversible only if something recorded what the file
looked like beforehand. Git is that something.

## What it is not

Git does not sit in the folder watching you type, the way a cloud drive
does. It records only the moments you tell it to, and it is not a
backup service either — destroy the folder with nothing else holding a
copy and the log goes with it, which is the gap a remote closes.

Press `n`.
