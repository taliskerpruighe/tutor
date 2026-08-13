---
id: files/how-git-works
title: How git works
level: Level 2
part: Version Control
section: Git, Github, and Jujutsu
order: 2
summary: Files are tracked or ignored, changes are staged before they are committed, and a remote can be a server or a drive as easily as GitHub
keywords: [git, repository, branch, staging area, commit, gitignore, remote, fetch, push, pull]
---

# How git works

*v0.2.9*

A **repository** — a repo — is a folder plus the entire history git has
kept of it, treated as one thing. Everything below is what happens
inside that one thing: which files it watches, how a change becomes a
permanent entry, and how that entry reaches anywhere else.

## Tracking and ignoring

Git does not watch every file in a repo by default — it watches the
ones you have told it to **track**, and leaves the rest alone. A file
git has never been told about sits in the folder, untouched by any of
this, until you add it. The opposite instruction, an **ignore** list,
tells git to never track a file even if it changes constantly — a
downloaded PDF, a folder of temporary exports, anything that is output
rather than drafting.

## Staging, then committing

Git makes you decide, separately from editing the file, which of your
changes go into the next commit. That decision is called **staging** —
its own explicit step, sitting between "I edited this" and "I have
recorded why." Skip it and the commit is empty. Stage half of what
changed and the commit holds exactly that half, with nothing telling
you the rest was left out.

Once staged, a **commit** is the note itself: the version, plus the
sentence explaining why it exists. Each commit points back to the one
before it, so the whole run of them forms a single chain — the
**history** — readable backward, in the order it actually happened.

## Branches running alongside

A **branch** is a second line of commits, split off the chain at some
point, that runs on its own without touching the line it split from.
Draft a speculative rewrite on a branch and the version everyone else is
working from does not move until you bring the branch back in — an act
called **merging**, which folds its commits into the line it split from
so the history reads as one line again.

## Fetch, push, pull: remotes elsewhere

Everything above happens on one machine. A **remote** is a copy of the
same history kept somewhere else that you can send commits to and bring
commits back from — three separate verbs for it: **push** sends yours
there, **pull** brings theirs here, and **fetch** brings theirs here
without merging them into your own work yet.

A remote does not have to be GitHub. It can be a server your firm runs,
an external drive plugged in once a week, or a colleague's own machine
— anything reachable that is willing to hold a copy.

GitHub is simply the remote most people mean by the word. What it adds,
once you point one at it, is the next article.

Press `n`.
