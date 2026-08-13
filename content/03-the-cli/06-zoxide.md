---
id: zsh/zoxide
title: zoxide
level: Level 1
part: The CLI
section: Zsh
order: 6
summary: cd remembers nothing between commands; zoxide remembers every folder you have visited and ranks them for you
keywords: [zoxide, z, cd, frecency, jump, folder, zshrc, homebrew, shortcut]
---

# zoxide

*v0.2.9*

`cd` takes you exactly where you type, and nowhere else. **zoxide** takes
you where you meant, typing less of it than `cd` ever asked for.

It is one command, learned in a minute, and it changes how you move around
for good.

## What it remembers

zoxide watches every `cd` you run and keeps a ranked list of the folders
you actually use, weighted by how often and how recently you visited
each — a measure it calls **frecency**, frequency and recency folded into
one word. You train it by doing nothing differently: it learns from the
`cd`s you were already typing.

## z instead of cd

Once it has seen a folder once, you can jump to it with a fragment of its
name, from anywhere:

```
z okonjo
```

That lands in `~/work/okonjo` whether you are standing in your home
folder, inside another matter entirely, or three levels down in a
different one. `cd` needs the exact relative or absolute address. `z`
needs only enough of a name to be unambiguous, and ranks the possibilities
by frecency if more than one folder matches.

The two are not rivals. `cd` still does the exact, deliberate move; `z` is
for the folder you have already been in and do not want to spell out
again.

## The one honest limit

`z` cannot take you anywhere `cd` has not already been. A folder it has
never seen is not in its list, so the first visit to any new matter still
wants a real `cd`, spelled out in full or reached with the sideways move
from *Moving around*. Every visit after that first one is a jump.

More than one folder can match a fragment — `okonjo` and, say, an
`okonjo-archive` sitting next to it. `z okonjo` lands on whichever ranks
higher by frecency, which is usually the one you meant. Where it is not,
a second fragment narrows it: `z okonjo archive` matches only a path
containing both.

> As with most things that save typing, the Boss had stopped using plain
> `cd` for anything he had already visited twice, long before he had a
> name for what he was actually doing.

## Setting it up

One line installs it — `brew install zoxide`, using Homebrew, which gets
its own article later in the course — and one more line makes `z`
available every time you open a terminal:

```
eval "$(zoxide init zsh)"
```

That line goes in `~/.zshrc`, your shell's own settings file, read fresh
every time a new terminal opens. Ask Claude Code to add it for you rather
than opening the file by hand.

zoxide's line is the first thing you have put in `~/.zshrc` on purpose.
The next article is what else that file is for.

Press `n`.
