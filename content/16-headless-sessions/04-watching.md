---
id: headless/watching
title: Watching
level: Level 2
part: Headless Sessions
section: Running Without a Chat
order: 4
summary: A headless session prints once and stops talking, which is not the same as nothing happening in between
keywords: [watching, tmux, panes, headless, subagent, chain, tail, log, monitor, split]
---

# Watching

*v0.2.0*

A headless session prints once and stops talking. That is not the same
as nothing happening in between. A chain running underneath it can
spawn half a dozen agents, one after another, and you will not see a
single one of them start — only the final answer, once the last agent
in the line has finished and handed it up.

Most of the time that is the whole point. On a chain still being tested,
it is a problem: a wrong answer tells you something went wrong and
nothing about where.

## Ask for the watcher

Do not write the watching script yourself. Redirect the run's own output
to a file, so there is something for a second script to read —

```bash
claude -p "Run the disclosure chain" > run.log &
```

— and then, in an ordinary chat, ask for the rest:

> *"Write me a shell script that watches `run.log` and prints a line
> every time a new agent name appears in it."*

That is the same habit *Moving around* used for an alias: say what you
want watched and in what shape, and let Claude write the watching. A
script built this way can be as particular as the job needs — flag a
model you did not expect, count agents as they finish, time how long
each one took — without you writing a line of it.

## Two panes, one screen

*What it is for*, back in *TUIs*, named this and left it for here: a
tmux window split into **panes**, one process in each, both alive on
the same screen. This is the case it was named for — the run in one
pane, the watcher reading its log in the other.

```bash
tmux new -s disclosure-run
```

Inside it, split the window — the prefix, released, then the key:

```
Ctrl-B  %
```

splits it vertically, side by side. Start the headless chain in one
half, the watcher in the other, and both run in front of you at once —
the run's own scroll of output on one side, your watcher calling out
each agent as it appears on the other.

```
Ctrl-B  d
```

detaches, and both keep running exactly as *Sessions that survive*
described. Reattach later and the two panes are exactly where you left
them, one still narrating the other.

---

That closes Headless Sessions. Counter-Recommendations comes next —
the last part, four features Claude Code ships that the Boss says to
leave switched off: agents it dispatches on its own initiative, a
background view that hides as much as it shows, subagents spawning
further subagents until nobody can say what ran, and agent teams,
switched off anyway because experimental means nobody promised the
shape holds from one version to the next.

Press `n`.
