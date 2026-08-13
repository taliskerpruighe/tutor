---
id: zsh/ripgrep
title: ripgrep
level: Level 1
part: The CLI
section: Zsh
order: 10
summary: The same search as grep, defaulting to recursive, skipping what a .gitignore already excludes, fast enough not to notice
keywords: [ripgrep, rg, grep, gitignore, fast, search, recursive, default, homebrew]
---

# ripgrep

*v0.2.9*

**ripgrep** is grep rewritten for how you actually search a folder: for
everything underneath it, skipping the files nobody wants searched, fast
enough that the wait disappears. The command is `rg`.

The defaults are the entire pitch. Nothing here is a new idea — *grep*
already searches contents, line by line, and `rg` is not a different way
of thinking about that. It is the same tool with better instincts about
what you actually meant to search.

## What it does without being asked

`grep` searches one file unless told `-r`. `rg` searches the current
folder and everything under it, unasked:

```
rg "without prejudice"
```

That alone replaces `grep -r "without prejudice" .`. `rg` also skips
anything a `.gitignore` already excludes, skips binary files it cannot
usefully search, and colours the match in the output — three things
`grep` either cannot do or needs a flag for individually.

Speed is the other half of the pitch. `rg` searches several files at
once rather than one after another, using a matching engine built for
the job rather than adapted from decades-old tooling — the difference
you notice the first time you search a folder with years of documents in
it, and the prompt is already back before you have looked away from the
screen.

## Narrowing by file type

```
rg --type md "without prejudice"
```

`--type` restricts the search to one kind of file — markdown here,
`--type pdf` for another — without you writing the file extension into
the pattern yourself or excluding it by hand. `rg --type-list` prints
everything it already knows how to recognise, which is most of what you
will ever open.

## Same flags, less typing

Most of what *grep* taught still applies: `-i` for case, `-l` for
filenames only, `-n` for line numbers, all unchanged. What is gone is the
`-r` you needed every single time, because recursive is no longer a
special case worth naming.

## Getting it

One more Homebrew install, the same way zoxide arrived a few articles
back:

```
brew install ripgrep
```

`grep` still ships with every Mac, and still deserves knowing — the
difference here is speed and defaults, not correctness, and there will be
a machine somewhere without `rg` on it.

> The Boss keeps both on principle: `rg` for everyday searching, `grep`
> for the rare script that has to run somewhere `rg` was never installed.
> Knowing the older tool is what makes the newer one optional rather than
> load-bearing.

Searching contents is now fast. The next article turns the same idea —
filter a list down as you type — into something you steer with your own
hands.

Press `n`.
