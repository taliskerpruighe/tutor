---
id: tuis/what-tmux-is
title: What tmux is
level: Level 1
part: TUIs
section: TMUX
order: 7
summary: A program that keeps a terminal session running even after the window looking at it is gone
keywords: [tmux, session, multiplexer, terminal, detach, screen, ghostty]
---

# What tmux is

*v0.2.0*

**tmux** is a program that holds a terminal session open independently
of whatever window is looking at it. You can close the window. The
session keeps running.

That sentence is doing more work than it looks like, so slow down on it.

## What a Ghostty tab actually is

A Ghostty tab is a window onto a process — a shell, running Claude Code,
running whatever — and the process lives inside that window. Close the
tab and the process it was showing you is killed along with it. This is
true of every terminal in *The terminals people use*, not only Ghostty.
The tab and the thing it shows are one object, and closing one closes
the other.

A tmux session breaks that link. tmux runs as its own separate program,
detached entirely from any window, holding whatever is inside the
session — a shell, an agent, a long job — genuinely alive on the
machine whether or not anything is looking at it. A Ghostty tab
attached to a tmux session is a viewer, not a container. Close the
window and the session does not notice. Open a fresh one and point it at
the same session, and you are looking at exactly where you left off.

## The name

tmux is short for *terminal multiplexer*. A multiplexer, in the general
sense, is anything that takes several signals and carries them down one
channel — and that is exactly the trade tmux makes. One tmux session can
hold several windows and several panes within them, all carried through
whichever single Ghostty tab happens to be attached at the time. The
multiplexing is what makes several processes fit behind one viewer, and
it is also what survives when that viewer is closed and reopened.

## Why an old idiom is still the answer

This is not a new trick. A program called `screen` did the same job
starting in 1987 — long before graphical desktops were the default way
anyone worked, back when a session outliving its window was not a
convenience but the only sane way to leave a long job running overnight
on a machine you did not own. tmux inherited that idiom rather than
inventing a new one, and nothing since has replaced it, because the
problem it solves has not gone away. A job that takes an hour still does
not care whether you are watching it, and a laptop lid still closes.

Press `n`.
