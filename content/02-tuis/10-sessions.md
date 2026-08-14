---
id: tmux/sessions
title: Sessions
level: Level 1
part: TUIs
section: TMUX
order: 10
summary: Every tmux command works on a session, and an unnamed one is a number you will forget by the third matter
keywords: [tmux, session, tmux new, tmux ls, tmux kill-session, naming, matter]
---

# Sessions

*v0.2.9*

A session is the object every tmux command in this section
ultimately targets — started, named, listed, ended. Four commands
cover it end to end.

`tmux new` on its own is fine for a job that will not outlive the
next few minutes — a quick check, a one-off script. It stops being
fine the moment you would need to describe it to find it again, and
tmux does not try: left unnamed, a session is called a plain number,
`0`, then `1` if a second one starts, and matter work rarely stays
at one.

## Starting one, named

```
tmux new -s matter-4471
```

`-s` sets the name at creation, so the session reads as what it is
in every list from here on, rather than as a number you have to
remember alongside it. Against a name already in use, `tmux new -s`
refuses outright, with `duplicate session: matter-4471` and nothing
started — the same protection `tmux ls` gives you, arriving a step
earlier: check first, or let the error do the checking for you.

## Renaming one already running

From inside a running session, prefix then `$` prompts for a new
name and applies it immediately — useful for the session tmux
started for you with a number, before you had decided what it was
for. The rename does not touch anything running inside it; every
window and pane carries on exactly as it was, under a name that now
actually says what it is for. It also does not need remembering by
anyone else attached to the same session — the new name shows up on
their screen the moment it is set, same as it does on yours.

## Listing what is open

```
tmux ls
```

prints every session currently held open on the machine, one per
line, whoever started it and whether you are looking at it right
now:

```
matter-4471: 2 windows (created Mon 09:14)
0: 1 windows (created Mon 11:02)
```

named and un-, with its window count and whether anything is
currently attached to it. Run this before starting a new one, so a
matter already in progress is found and reattached to, rather than
started twice under two different names.

## Killing one

```
tmux kill-session -t matter-4471
```

ends the session and everything running inside it — every window,
every pane, gone at once. There is no confirmation prompt and no
undo; check `tmux ls` first if there is any doubt which name is
which. `tmux kill-server` goes further still, ending every session
on the machine in one command, named and un-, and is worth knowing
about mainly so it is never typed by accident.

Detaching leaves a session alive, everything inside it untouched.
Killing it does not.

Press `n`.
