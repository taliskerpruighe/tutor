---
id: agents/tabs-and-windows
title: Tabs and windows
part: Agents
section: Context
order: 2
summary: Cmd-1 through Cmd-9 jump straight to a tab, a split faces two agents at once, and a rename is how you tell three claude sessions apart
keywords: [ghostty, tab, window, split, cmd-t, cmd-n, cmd-d, rename, agent, jump]
---

# Tabs and windows

*v0.2.0*

The last article said to open three Ghostty tabs and start three
conversations, as though that were free. It is not quite. Three tabs
named nothing, holding three agents that look identical, is its own
small problem — and this article is how you avoid making it.

*Your terminal is Ghostty* already gave you `Cmd-T` for a new tab,
`Cmd-N` for a new window, and `Cmd-W` to close one. What follows
builds on those.

## Jumping straight to one

With several tabs open, clicking along the bar to find the right one
is slower than it needs to be. `Cmd-1` through `Cmd-9` jump straight
to the tab in that position — `Cmd-1` for the first, `Cmd-2` for the
second, and on down the row. Three agents running, and any one of them
is one keystroke away.

## A tab or a window

Both hold a conversation. The difference is whether you want to see
more than one at a time.

A tab hides everything else behind it — one agent on screen, the rest
waiting their turn. A window sits beside your other windows, so two
can be visible together: an agent working in one, this reader open in
the other, both in view at once. `Cmd-N` opens the new window; `Cmd-T`
opens a tab inside whichever window has focus.

Reach for a window when a job wants watching alongside something else.
Reach for a tab otherwise — it is the default for a reason, and most
of a working day is spent switching between tabs rather than arranging
windows.

## Splits — two agents, one tab

A tab can also be cut in half. `Cmd-D` splits it right; `Cmd-Shift-D`
splits it down. Either way you now have two panes in the one tab, each
running its own shell, each capable of holding its own `claude`.

```
  ┌─────────────┬─────────────┐
  │             │             │
  │  agent A    │  agent B    │
  │  drafting   │  checking   │
  │             │             │
  └─────────────┴─────────────┘
        one tab, two agents
```

That is genuinely different from two tabs. Two tabs put one agent in
front of you and hide the other. A split puts both on screen together
— the draft on the left, the citation check on the right, neither one
covering the other while you work.

## Telling them apart

None of this solves the actual problem, which is that three tabs
running plain `claude` all say the same thing on the label: `claude`.
Nothing there tells you which one is reading the bundle and which one
is still empty.

Double-click a tab and a dialog opens offering to rename it. Give it
the job, not the tool — `bundle`, `drafting`, `citations` — and the
bar stops being three identical labels and starts being a list of what
is actually happening. A tab can also be dragged along the bar to put
it next to the work it belongs with.

Do this before you have six tabs open and no memory of which is which.
It costs four seconds and the alternative is clicking through all of
them to find out.

The next article is what fills a tab up in the first place, and why
it fills faster than you would expect.

Press `n`.
