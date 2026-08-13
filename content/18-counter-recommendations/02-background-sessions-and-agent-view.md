---
id: counter/background-sessions
title: Background sessions and agent view
level: Level 2
part: Counter-Recommendations
order: 2
summary: What a background session and agent view actually cost, and the one setting that turns off both together
keywords: [background session, agent view, /bg, --bg, dashboard, memory, resources, settings.json, env, claude_code_disable_agent_view, headless, tmux]
---

# Background sessions and agent view

*v0.2.3*

Two features share one switch. Type `/bg` inside a session, or start
one with `--bg` on the command line, and it drops into the background
and carries on while you turn to something else — a **background
session**. Open **agent view** and every agent still running draws on
one screen at once, a dashboard that updates as each of them works.

The appeal is genuine, and it is not a small one. A session that keeps
running once you look away, and a screen that shows you what it is
doing, are exactly what *Watching* left you wanting. Neither one is
what you should reach for.

## The same job, carried at a higher weight

A background session holds a whole interactive session alive — its own
process, its own memory, its own state — to do work a headless one
carries lighter. `claude -p` runs, prints its answer and exits; nothing
is left resident once the prompt returns. A background session never
exits, because staying open is the entire point of it, and that
difference is not free. On a Mac carrying a modest amount of memory, it
is felt directly: a process left resident for the length of a working
session, for output a headless run would already have handed you,
printed and gone.

## A dashboard with its own bill

Agent view is not a window onto other processes. It is a process of
its own, with a job to do continuously — reading the state of every
agent it shows you and redrawing it, on a loop, for as long as it
stays open. It spends resources purely to render a picture of other
processes spending resources, a cost with nothing underneath it:
closing agent view changes nothing about the work it was watching,
only whether you can see it.

## More agents than a screen can hold

Set the cost aside and the thing it draws still stops helping past a
couple of agents. A dashboard of two is a status report. A dashboard
of six is a wall of moving text, none of it in the order you would
ask about it, and reading it does not tell you which one wants your
attention — it only tells you that something, somewhere on the
screen, is happening.

## One switch turns off both

The Boss turns off both features in one line, in the `env` block of
`~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_DISABLE_AGENT_VIEW": "1"
  }
}
```

Despite its name, the variable does not stop at agent view. It
disables the background session as well — `/bg` and `--bg` both — in
the same setting. One switch, not two variables to remember.

## What she already has

She already owns the same visibility, built once and free from then
on. *Piping* sends a headless run's answer straight to a file or the
next command; *Watching* puts that run in one tmux pane and a small
script reading its log in the other. Between them, that is the whole
of what a background session and agent view were offering, at no
resident cost at all.

Next is the feature that lets subagents spawn subagents of their own.

Press `n`.
