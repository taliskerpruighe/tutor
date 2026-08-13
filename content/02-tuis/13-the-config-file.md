---
id: tmux/the-config-file
title: The config file
level: Level 1
part: TUIs
section: TMUX
order: 13
summary: Every persistent tweak to tmux lives in one file, read once at startup and reloaded on command rather than by restarting
keywords: [tmux, tmux.conf, config, set -g, bind, reload, source-file, mouse]
---

# The config file

*v0.2.9*

tmux reads one file at startup, `~/.tmux.conf`, and every persistent
change to how it behaves — the prefix remap from earlier in this
section included — lives there rather than being retyped by hand
each time a session starts.

A line in it is one of two shapes: `set` for an option, `bind` for a
keystroke. Both take effect only for sessions started after the
file changes, unless reloaded.

## Where it lives

`~/.tmux.conf`, in the home directory, read once when tmux itself
starts — not once per session. It is a plain text file; any editor
opens it.

## What goes in it

```
set -g mouse on
set -g base-index 1
set -g history-limit 10000
```

`-g` makes an option global, applying to every session rather than
only whichever one happens to be running when it is set — worth
using on nearly everything in this file. `mouse on` lets a click
choose a pane and a scroll wheel move through *Copy mode* without
touching the prefix. `base-index 1` numbers windows from `1` instead
of tmux's default `0`, which puts every window's number where a
finger already reaches for it on the keyboard, since `1` sits at the
near end of the number row and `0` at the far one.
`history-limit` sets how many lines of scrollback each pane keeps
for *Copy mode* — the default keeps only a couple of thousand, thin
for a long-running job.

A line starting with `#` is a comment and does nothing; use it to
leave a note beside a setting that is not self-explanatory six
months later. Order rarely matters — later lines override earlier
ones on the same option, the same as reading a script top to
bottom, so a duplicate setting near the end of the file wins.

## Reloading it

Editing the file changes nothing already running — a session open
before the edit stays on whatever it started with, indefinitely,
until told otherwise. Prefix then `:` opens tmux's own command line
at the bottom of the screen; typing `source-file ~/.tmux.conf` there
and pressing return reloads it for the whole tmux server, with no
restart and nothing lost from any pane. Because nearly everything in
this file is set with `-g`, one reload from any session reaches
every session already open, not only the one it was typed into.

A binding worth adding for exactly this purpose:

```
bind r source-file ~/.tmux.conf
```

after which prefix then `r` reloads the file in one step, rather
than typing the command out each time it changes.

Reading text already on the screen is one thing. Reaching back past
the edge of it is *Copy mode*, next.

Press `n`.
