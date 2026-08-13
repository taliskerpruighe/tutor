---
id: tmux/detaching-and-reattaching
title: Detaching and reattaching
level: Level 1
part: TUIs
section: TMUX
order: 12
summary: Leaving a session on purpose and finding it again are each one command, and neither one is closing the window
keywords: [tmux, detach, attach, tmux attach, reattach, session, sharing]
---

# Detaching and reattaching

*v0.2.9*

Closing the window a session is attached to is not how you leave it
on purpose. Prefix then `d` is. One keystroke out, one command back.

The difference matters because *What tmux is* established that
closing the window never kills the session underneath it — so the
two routes end up in the same place regardless. But prefix then `d`
returns you cleanly to the ordinary shell prompt outside tmux, in
the same window, rather than closing anything, and that is the
version worth building a habit around.

## Detaching

Prefix then `d` drops you out of the session and back to whatever
shell started it. Nothing inside the session stops. Every pane,
every window, everything running in them, carries on exactly as it
was, unattended. The window you were sitting in does not close — it
simply stops looking at tmux and goes back to being an ordinary
shell, free to run something else entirely or to close outright with
no consequence for the session it just left.

## Detaching without doing anything

A dropped SSH connection detaches a session automatically, with no
prefix and no warning — the server underneath keeps the session
running exactly as if `d` had been pressed on purpose. Reconnect and
the same command below finds it exactly where the connection left
it, work included. A closed laptop lid mid-job behaves the same way:
the local network drops, the remote session detaches, and nothing
running inside it notices.

## Reattaching

```
tmux attach
```

or its short form `tmux a`, reattaches to the most recently detached
session — the natural next command after opening a fresh window with
nothing else running in it.

## Naming which one

With more than one session open, `tmux attach` on its own is
ambiguous, and tmux picks one for you rather than asking. Name it
instead:

```
tmux attach -t matter-4471
```

`tmux ls`, from *Sessions*, is how you find the name to put there.
Run either form of `attach` with no session anywhere on the machine
and tmux says so plainly — `no server running` — rather than
starting one for you. Attaching and creating are two different
commands on purpose.

## Reattaching without detaching the other end

Attaching to a session already attached somewhere else does not
detach that other window — both now show the same screen, resized to
fit whichever one is smaller, which is the sharing *What it is for*
described. Add `-d` to the command and the earlier window is
detached automatically, leaving exactly one.

The session survives the window. It does not survive editing it by
hand while blind — the config file is next, and what belongs in it.

Press `n`.
