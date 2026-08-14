---
id: files/jj
title: Jujutsu
level: Level 2
part: Version Control
section: Git, Github, and Jujutsu
order: 4
summary: Jujutsu reads the same history as git but removes the staging step and the state where work can go missing, saving on its own as you go
keywords: [jujutsu, jj, git, colocation, staging area, working copy, detached head, commit]
---

# Jujutsu

*v0.2.9*

**Jujutsu** — jj — does the same job as git, on the same history, and
commonly reads it straight out of the same underlying storage. Nothing
about the model from *What git is*, *How git works* and *GitHub*
changes: commits, branches and remotes all mean exactly what they meant
there. What changes is the handling — two of git's oldest sharp edges
are not present.

## How it differs from git

Git makes you stage a change, separately from editing the file, before
it can be committed — a step with its own command, easy to skip or get
half right. jj has no staging area. Whatever is sitting in the file is
what the next commit holds, always, because nothing in jj is ever
*pending* a commit. It already is one.

Git also has a state called a detached HEAD, reached by moving to a
commit that is not the tip of any branch — easy to end up in without
meaning to, and easy to lose work out of. jj has no equivalent. Every
piece of work is a real commit in the history from the moment it exists,
so there is nothing hovering that a careless move can drop.

## Colocation

jj commonly runs **colocated** with a git repository: the same folder,
the same history underneath, readable by either tool. A jj user can
hand that folder to a colleague who has never heard of jj, and nothing
about it looks unusual to them — every commit jj made is an ordinary
git commit as far as they are concerned. The Boss adopted jj on exactly
that basis: fewer steps for him, nothing to retrain in anyone he shares
a repository with.

## The working copy is already a commit

In git, "what is on disk right now" and "the next commit" are two
different things until staging joins them. In jj they are never
separate. The files you see in the folder *are* the working commit,
under whatever description it currently carries — usually none, until
you give it one.

## Saving happens on its own

jj takes a fresh snapshot of the working copy every time you run a jj
command, without being asked to. There is no moment where an edit sits
unrecorded because nobody remembered to save it — the next jj command,
whatever it is, folds the current state of every file into the commit
you are standing on.

That convenience has a cost attached: git is the tool nearly everyone
else already has installed and half-knows, and jj is a second thing to
learn on top of it, worth reaching for once git no longer feels foreign
rather than on day one.

Press `n`.
