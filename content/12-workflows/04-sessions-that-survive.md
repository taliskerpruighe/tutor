---
id: workflows/sessions-that-survive
title: Sessions that survive
part: Workflows
section: What They Are
order: 4
summary: Start the workflow inside a named tmux session, detach, and it keeps running with the lid shut
keywords: [tmux, session, detach, reattach, workflow, naming, persistence, lid]
---

# Sessions that survive

*v0.2.0*

*What tmux is* and *What it is for*, back in *TUIs*, told you that a
tmux session runs independently of the window looking at it, and that a
long job is the case it earns its keep on. Ten books, running as a
workflow, is that case arriving for real.

This article is the second half of that idiom — the persistence, not
the panes — aimed squarely at running a workflow inside it.

## Why a Ghostty tab will not do

A Ghostty tab and the process inside it are one object. Start the
workflow in an ordinary tab and the run lives exactly as long as that
tab does — close it, or shut the lid without thinking, and the ten
books stop wherever they had got to. A tmux session breaks that link.
The workflow runs inside the session, not inside the window, so the
window can close without the run noticing.

## Starting one

```bash
tmux new -s ten-books
```

`new` starts a fresh session; `-s ten-books` names it. You are now
inside it, looking at an ordinary shell, in every way that matters to
you. Start the workflow here, the same way you would from any tab.

## Detaching

Leaving does not mean closing anything. The default tmux prefix is
`Ctrl-B`, held and released before the next key rather than held
through it. To detach:

```
Ctrl-B  d
```

The window goes back to an ordinary prompt. The session, and the
workflow inside it, keeps running exactly as it was — shut the lid now
and nothing about the run changes.

## Listing and reattaching

From anywhere, including a fresh Ghostty tab opened later:

```bash
tmux ls
```

lists every session still alive, by name. Reattach to the one you want:

```bash
tmux attach -t ten-books
```

and you are looking at precisely where the workflow had got to, output
scrolling exactly as it would have if you had never left.

## Naming is not decoration

`tmux ls` with one anonymous session is fine. `tmux ls` with four spike
workflows and two overnight ones, all named `0`, `1`, `2` and `3`, is
four guesses before you find the one you want. Name a session after the
workflow it is running — `ten-books`, `bundle-review`, `disclosure-run`
— and ten of them still read as what they are.

Panes — several processes sharing one screen, one watching the other —
are a later instalment, at *Headless Sessions*, where a workflow that
runs unattended is worth a script sitting beside it keeping watch.

For now, the mechanics above are the whole of it. Next, how you get a
workflow written in the first place.

Press `n`.
