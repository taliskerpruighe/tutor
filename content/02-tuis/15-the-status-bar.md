---
id: tmux/the-status-bar
title: The status bar
level: Level 1
part: TUIs
section: TMUX
order: 15
summary: The one line on screen tmux never lets go blank, and what it is telling you by default
keywords: [tmux, status bar, status-left, status-right, session name, window list, customise]
---

# The status bar

*v0.2.9*

A line along the bottom of every tmux screen is never blank and
never optional. It is tmux telling you, continuously, which session
this is and what else is open in it.

Nothing on it needs a keystroke to appear. Half of it is worth
reading; the other half you may as well ignore.

## Reading it, by default

The left edge names the session — the string set with `-s` in
*Sessions*, or the plain number tmux gave it if nothing was set. The
middle lists every window by number and the name of whatever is
running in it, with the current one marked and drawn in a different
colour. The right edge, by default, carries the date and time.

## The symbols after the number

A window's number in that list carries a marker of its own: `*` for
the one you are looking at, `-` for whichever one you were looking
at immediately before it, `Z` for one currently zoomed by the trick
in *Windows and panes*. None of it needs decoding at the moment you
see it — the current window is already the brightest thing on the
line — but the `-` is what tells you, at a glance, which window
prefix then `l` will return you to.

## Why the window list matters more than the clock

Everything on the right is decoration copied from whatever the
machine already tells you elsewhere. The window list in the middle
is the part earning its keep every time you look at it — the answer
to "what else did I open in this session, and where did I leave it",
without running a command to ask. It is also the only part of the
bar that changes on its own, growing by one entry every time prefix
then `c` opens a window and shrinking by one every time a pane you
close was the last one in it.

## Customising it

```
set -g status-left "#S "
set -g status-right "%H:%M"
set -g status-style "bg=colour235,fg=white"
```

`status-left` and `status-right` are format strings: `#S` expands to
the session name, `%H:%M` to the current time, and either can be
shortened, reordered, or dropped to nothing. `status-style` sets the
bar's background and text colour together, as one comma-separated
value — worth changing only if the default is genuinely hard to
read, since a status bar that looks different from every other
machine you sit down at is one more thing to relearn.

---

That is TUIs. A terminal is a window, Ghostty is the one already set
up, and tmux is what keeps a session alive underneath either. The
CLI is next: the program waiting inside every one of those windows
before you have typed anything into it.

Press `n`.
