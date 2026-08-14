---
id: tmux/the-prefix-key
title: The prefix key
level: Level 1
part: TUIs
section: TMUX
order: 9
summary: A chord, not a single key, decides whether a keystroke reaches tmux or the program running inside it
keywords: [tmux, prefix, chord, keybinding, ctrl-b, ctrl-a, remap, tmux.conf]
---

# The prefix key

*v0.2.9*

Every tmux command starts with the same two keystrokes, and the first
one does nothing on its own.

This is short, and it has to come first, because nothing else in this
section makes sense without it.

## Why a chord at all

A pane inside tmux is usually running something that wants every
keystroke for itself — a shell, an editor, an agent reading from
standard input. If a single key such as `n` meant "next window" to
tmux, nothing running inside a pane could ever type the letter `n`.
tmux solves this by never listening to a bare key. It listens for a
**prefix**: press one key, release it, then press a second. Only the
pair together is a tmux command. Everything not preceded by the
prefix passes straight through to the pane, untouched.

## The default, and how it is written

The default prefix is `Ctrl-b`. A tmux command such as "open a new
window" is written throughout this section as prefix, then `c` — two
separate presses, not one held chord.

## Why people change it

`Ctrl-b` sits an awkward stretch from the home row. The older
program tmux borrowed the idea from, `screen`, used `Ctrl-a`
instead — a key that also happens to be "start of line" in a shell,
which is exactly the collision remapping creates. Most people who
remap tmux move it to `Ctrl-a` anyway, and accept losing that shell
shortcut, because they type the prefix dozens of times an hour and
type "start of line" rarely by comparison.

## Changing it

The remap lives in the config file, three lines:

```
unbind C-b
set -g prefix C-a
bind C-a send-prefix
```

The first line frees `Ctrl-b` back to whatever it did before tmux
claimed it. The second tells tmux which key to treat as the prefix
from now on. The third is easy to skip and breaks things if you do:
without it, `Ctrl-a` becomes the prefix but is never itself passed
through to a nested tmux or a program expecting it. Where that line
lives, and what else belongs beside it, is *The config file*.

## Sending the prefix key itself

SSH into a machine that is already running its own tmux, from
inside your own tmux, and the outer session is the one attached to
your actual terminal — it sees the prefix first, every time, and the
inner one never gets a chance at it. Pressing the prefix twice is
the way past that: the outer session treats the first press as the
prefix as usual and, because `send-prefix` is bound to it by
default, forwards the second press through as a single literal
prefix keystroke, which is what the inner session then sees. It is a
narrow case, and the only way past it without remapping one of the
two.

Press `n`.
