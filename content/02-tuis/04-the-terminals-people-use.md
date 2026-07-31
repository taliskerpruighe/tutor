---
id: tuis/terminals-people-use
title: The terminals people use
part: TUIs
section: Terminals
order: 4
summary: The terminal on your Mac is not the only one, and the ones people actually reach for differ on five things
keywords: [terminal, iterm2, wezterm, alacritty, kitty, ghostty, config, gpu]
---

# The terminals people use

*v0.2.0*

The first article in this part named the axes terminals differ on
without naming a single one, beyond the one Apple ships. Here are the
others, and where each sits on those axes.

**iTerm2** is the old guard. It predates most of what follows by a
decade, and it shows: a huge settings window, split panes, search,
profiles for different jobs. It is not quick to draw — it does its
drawing on the ordinary processor rather than the graphics chip — and
that is the trade its long feature list was built on.

**WezTerm** is written by one person, in Rust, and configured in Lua — a
real programming language, not a settings file, which buys logic
("dark theme after sunset") at the cost of a language to learn first. It
draws through the graphics chip and runs identically on a Mac, on Linux,
and on Windows.

**Alacritty** does one thing: draw text as fast as a screen can be
refreshed. No tabs of its own, no splits of its own — plain text config,
minimal defaults, and the assumption that anything else you want, tmux
will supply.

**kitty** draws through the graphics chip too, and adds one feature the
others mostly do not: it can put an actual picture on the screen,
inline, mid-scroll, using a protocol it invented and other terminals have
since copied.

**Ghostty** is next.

## Where they actually differ

| Terminal | Fast to draw | Config |
|---|---|---|
| iTerm2 | on the processor | a settings window |
| WezTerm | on the graphics chip | Lua |
| Alacritty | on the graphics chip | plain text |
| kitty | on the graphics chip | plain text |
| Ghostty | on the graphics chip | plain text |

Draw speed used to separate them cleanly; it barely does now, because
every recent terminal learned the same trick and moved its drawing onto
the graphics chip. What still separates them is everything else in that
table, plus two things it does not show: whether a picture can appear on
screen at all, and whether tabs and split panes come built in or have to
be borrowed from something else running inside the terminal.

Tabs and splits split the same way. iTerm2, kitty and Ghostty all draw
their own tabs and their own splits, so a new pane is one keystroke away
in any of them. Alacritty draws neither — reach for tmux, three articles
from now, if you want either inside it. WezTerm sits in between: tabs and
splits of its own, configured in the same Lua file as everything else.

None of this is a decision you need to make. It has already been made.

Press `n`.
