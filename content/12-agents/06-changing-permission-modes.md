---
id: perms/changing-modes
title: Changing permission modes
level: Level 2
part: Agents
section: Plans and Permissions
order: 6
summary: Shift-Tab moves a running session between how closely it checks with you before acting, and a setting moves the one it opens in
keywords: [permission mode, shift-tab, mode indicator, default settings, ccstatusline, session state]
---

# Changing permission modes

*v0.2.9*

Every interactive session names a mode at the bottom of the screen,
before you have any reason to know what it means. That is the
session's **permission mode** — how often it stops and asks before
running a command or touching a file, rather than doing the thing and
telling you afterwards.

*ccstatusline* named it in passing, on the row it recommends showing
alongside the context figure. This article is the one it promised:
what each mode actually is comes in *The permission modes there
are*; this one is how you move a session between them once it is
already running.

A session at the strict end of that scale asks before it deletes a
file, before it runs anything on the command line, before it touches
somewhere outside the folder you started it in. A session at the loose
end asks about none of it. Everything in between is a mode, and this
is how you land on one deliberately rather than by accident.

## One key, mid-session

Press `Shift-Tab` and the session steps to the next mode, immediately,
with no confirmation asked and no second press needed. Nothing else
changes — the transcript, the folder, the files it can already see are
exactly as they were a moment ago. Only the answer to *how carefully
does this check with me* moves.

That makes it cheap to try. Step into a stricter mode for the one
change you want watched closely — deleting something, touching a file
outside the matter — and step back out again once it is done. The
mode is a dial you turn as you go, not a decision you live with for
the rest of the session.

## Nothing else moves

Stepping the dial does not touch anything the session already knows.
The rules it loaded on the way in, the skills on its path, its own
memory of what you asked five minutes ago — none of that resets with
the mode. Only the checking-in habit changes; everything the session
has learned about the job stays exactly where it was.

## Watching it happen

The name at the bottom is the tell, and it changes the instant you
press the key, with nothing else on screen disturbed. Set up
`ccstatusline` the way the Boss recommends and the same figure sits on
its own line under the prompt, redrawn on every turn rather than
waiting for you to look down and check.

## A default worth setting

`Shift-Tab` only ever touches the session in front of you. It says
nothing about the next one, which opens back at whatever your settings
call the default. You do not have to accept that.

> *"Set my default permission mode in my global settings."*

Ask an agent to do it in those words and every session you launch
after that starts already where you meant it to, rather than back at
whatever Claude Code ships with.

Press `n`.
