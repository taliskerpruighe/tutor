---
id: agents/ccstatusline
title: ccstatusline
level: Level 2
part: Agents
section: Context
order: 5
summary: A third-party status line that puts the figures Context rot and Managing context asked you to watch on the line under the prompt
keywords: [ccstatusline, status line, sirmalloc, settings.json, permission mode, context, cost, session state, configuration]
---

# ccstatusline

*v0.2.9*

*Context rot* told you to watch the number. *Managing context* told you
what to do once you have. Neither told you where to look — the row
under the prompt, printed fresh on every turn, that Claude Code calls
the status line.

Claude Code already lets you build one: write a script that reads a
JSON payload off standard input and print whatever you want, or
describe it in one sentence to `/statusline` and let Claude write the
script for you. Either way you get a single line, built once, to one
specification.

## The line you write yourself

> **From the Boss:** *"The builtin status line is dogshit."*

Hand-written or generated, it comes to the same thing: a script tied
to whatever you specified — a model name here, a percentage there —
and changing your mind about a field means going back to the shell
yourself, one `jq` incantation at a time.

## ccstatusline

**ccstatusline**, by `sirmalloc`, skips the shell script entirely. Run
it directly and it opens a configuration screen:

```bash
npx -y ccstatusline@latest
```

Add widgets one at a time from inside that screen, then choose
**Install to Claude Code settings**, and it writes the `statusLine`
entry into `settings.json` for you — nothing to type into a script by
hand, nothing to remember the field names for.

The widget list runs long: context remaining, session cost, the git
branch, a running clock, several on one line in whatever order you
set. It runs long enough that reading through it is not the fast way
in. Ask an agent what is on offer before you sit down with the screen
yourself.

## Seeing at a glance what a session is doing

Three panes open, each running `claude`, each labelled identically on
the tab bar — nothing there says which one is drafting and which is
still empty. Renaming a tab fixes the label: `bundle`, `drafting`,
`citations`, and the bar stops being three identical names.

A rename tells you which matter. It says nothing about state — whether
the agent behind that label is at 20% or past the point *Context rot*
called borderline unusable, or what it has cost so far. A label set
once at the start of a session goes stale the moment the work moves
on. A status line does not: it redraws on every turn, unattended, and
the pane tells you its own condition without you clicking into it to
ask.

## The configuration that earns its place

Switch on everything ccstatusline offers and the row gets as cluttered
as a hand-written script was sparse — a full line of widgets is no
improvement on a line that told you nothing. The Boss's own setup
keeps to two fields: context remaining, the figure the last two
articles were built around, and permission mode, sitting beside it.
Cost and the rest earn their place if you want them; those two earn
it regardless.

What that second field actually is belongs to *Changing permission
modes*, the first article of the next section.

Press `n`.
