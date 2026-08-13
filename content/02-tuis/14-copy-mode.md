---
id: tmux/copy-mode
title: Copy mode
level: Level 1
part: TUIs
section: TMUX
order: 14
summary: Scrollback tmux keeps for itself, and the only way text inside a pane gets out of it
keywords: [tmux, copy mode, scrollback, selection, paste buffer, mouse, search]
---

# Copy mode

*v0.2.9*

Scrollback in an ordinary terminal is the terminal's own doing —
Ghostty keeps it, and a pane inside tmux does not show it the same
way. tmux keeps its own scrollback instead, set by `history-limit`
in *The config file*, and none of it is visible on the ordinary
screen at all.

Copy mode is how you reach that scrollback, and it is also the only
way text inside a pane gets out of it. A handful of keys cover the
whole of it.

## Entering it

Prefix then `[` enters copy mode. The screen looks unchanged except
for a position indicator in the corner; every key that would
normally reach the pane now moves you through it instead, rather
than being typed into whatever the pane is running.

## Moving and searching

Arrow keys and `Page Up`/`Page Down` move the same way they would
anywhere else. `Ctrl-r` searches backward through the buffer for a
string typed after it — the fastest way back to a line of output
that scrolled past minutes ago, rather than paging up by hand.
Pressing it again repeats the same search further back, the same
way a shell history search does.

## Selecting and copying

`Ctrl-Space` marks the start of a selection; moving from there
extends it, the same shape as marking a point and stretching it in
any text editor. `Alt-w` copies the selection into tmux's own paste
buffer and drops back out of copy mode automatically. With
`mouse on` from *The config file*, dragging across text does the
same selecting and copying in one motion, with no keys at all.

## Pasting it back

Prefix then `]` pastes the most recent buffer into whichever pane
has focus, at the cursor position — the other half of the pair, and
the reason copying it in the first place was worth doing. tmux keeps
a short stack of buffers, not just the last one, but `prefix ]`
only ever reaches for the top of it; anything further back needs
`tmux choose-buffer` to find by hand.

## The other set of keys

`set -g mode-keys vi` in *The config file* swaps every key above for
its vi equivalent: `h j k l` to move, `v` to start a selection, `y`
to copy. Neither set is more correct than the other. Use whichever
one your fingers already know from somewhere else. `q` exits copy
mode at any point in either set, and leaves the pane exactly as it
was, buffer or no buffer.

None of this appears anywhere on screen once you are back out of it.
The one thing that is always on screen, and always telling you
something, is next.

Press `n`.
