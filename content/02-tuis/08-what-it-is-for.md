---
id: tuis/tmux-use-cases
title: What it is for
part: TUIs
section: TMUX
order: 8
summary: Insurance for a long job, a session you can hand to someone else, and several processes on one screen
keywords: [tmux, session, panes, layout, sharing, laptop, workflow]
---

# What it is for

*v0.2.0*

A session that survives its window sounds like a convenience. It is
closer to insurance, and the last article's idiom earns its keep in
four ordinary situations rather than one clever one.

## Insurance for a long job

A job that takes an hour does not stop needing to run because you shut
your laptop. Started inside an ordinary Ghostty tab, closing the lid
kills it halfway through. Started inside a tmux session, closing the lid
does nothing to it — the session is not inside the window, so the window
closing is not an event it experiences. Open the lid later, look back
in, and the job has either finished or is still going exactly where you
left it.

## Handing a session to someone else

Because a tmux session is a separate thing from the window looking at
it, more than one window can look at the same session at once — on the
same machine, or on a different one entirely, if both can reach it. That
turns a terminal into something two people can watch together: you drive,
someone else watches over your shoulder from their own machine, both of
you looking at the identical scrolling text in real time. Nothing about
a Ghostty tab can do this. A tab is a window onto a process only the
person sitting at that window can see.

## Several processes, one screen

A tmux window can be split into **panes** — the terminal equivalent of
the splits *The terminals people use* mentioned some terminals doing on
their own. Where Ghostty's splits belong to Ghostty, tmux's belong to
the session itself, which means they survive the same way the session
does: a job running in one pane and a script watching it in the other,
both still there after you reattach.

## Keeping many of them straight

None of this matters if you cannot tell your sessions apart. tmux lets
you **name** one when you start it, so a session for one matter and a
session for another read as what they are in a list, rather than as
three identical, anonymous entries you would otherwise have to guess
between. A dozen anonymous sessions are a dozen guesses; a dozen named
ones are a dozen labels, and the difference is entirely the naming.

---

That is TUIs — the window, the terminal underneath it, and the session
that outlives both. *The CLI* is next: the line you actually type into,
what writes it, and what runs when you press return.

Press `n`.
