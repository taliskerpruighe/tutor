---
id: tmux/windows-and-panes
title: Windows and panes
level: Level 1
part: TUIs
section: TMUX
order: 11
summary: A window takes the whole screen and a pane shares it, both living and dying with the session underneath them
keywords: [tmux, window, pane, split, kill-pane, layout, zoom]
---

# Windows and panes

*v0.2.9*

A session can hold more than one screen at a time, and tmux gives
you two ways to divide it: windows, which take the whole pane area
one at a time, and panes, which share it. Two objects, one habit
each.

Both live inside the session from *Sessions*, and both vanish with
it — closing every pane and window at once is exactly what killing a
session does.

## Windows

A window is a full screen within the session, numbered from `0`.
Prefix then `c` opens a new one; prefix then `n` or `p` steps to the
next or previous; prefix then a number jumps straight to that
window. Every open window's number is listed along the bottom of the
screen — reading that list is *The status bar*.

## Panes

A pane is the split *What it is for* already introduced, and a
window can hold several of them at once, side by side or stacked.
Prefix then `%` splits the current pane into two side by side;
prefix then `"` splits it into two, one above the other. Each split
works on whichever pane has focus, so splitting twice in a row from
the same pane produces three panes, not four. There is no fixed
limit on how many a window can hold, only how small each one gets
before the split stops being useful to read.

## Moving between panes

Prefix then an arrow key moves focus one pane in that direction.
Prefix then `o` cycles through every pane in the window in order,
which is faster than aiming an arrow key when there are more than
two.

## Filling the screen with one

Prefix then `z` zooms the focused pane to fill the whole window
temporarily, hiding the others without closing them. Pressing
prefix then `z` again restores the layout exactly as it was — the
fastest way to read a wide table in a narrow pane without rearranging
anything on either side of it.

## Closing one

Typing `exit`, or the shell's own exit keystroke, ends whatever is
running in the focused pane, and the pane closes with it; the last
pane in a window closes the window the same way. Prefix then `x`
does the same thing without waiting for the program inside to finish
on its own, and asks first.

Closing the last pane in the last window ends the session along with
it, the same as *Sessions*' own `kill-session` — there is nothing
left for tmux to hold open.

A pane you cannot see is still running.

Press `n`.
