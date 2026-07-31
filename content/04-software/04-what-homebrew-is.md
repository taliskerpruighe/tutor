---
id: software/what-homebrew-is
title: What Homebrew is
part: Software
section: Homebrew
order: 4
summary: The package manager macOS does not come with, and the one nearly every set of instructions online quietly assumes you have
keywords: [homebrew, brew, install, opt, usr local, macos, apple silicon, terminal]
---

# What Homebrew is

*v0.2.0*

**Homebrew** is the package manager macOS does not come with. Apple
ships a finished machine, not a foundation to build one from, and
Homebrew is what most Mac users install to close the gap.

## Installing it

One command, run once, in the terminal. Homebrew's own site,
`brew.sh`, publishes it — a single `curl` piped into `bash` that
downloads and runs its installer. Paste that line in and it asks for
your password partway through — the same password you log in with —
because it needs to create a folder outside your own account. After
that it needs nothing further from you.

## Where things land

Homebrew keeps everything it installs in one place, separate from the
rest of macOS: `/opt/homebrew` on an Apple Silicon Mac, `/usr/local` on
an older Intel one. Every package it fetches, and every file that
package needs, lives under that one folder.

This matters more than it sounds. Nothing Homebrew installs touches the
parts of macOS Apple maintains, and nothing it installs conflicts with
anything else on the machine, because it is not sharing space with
anything else. Removing Homebrew — rarely done, but possible — is one
folder deleted, not a hunt through the whole disk for stray files.

It also means Homebrew knows, at all times, exactly what it put there.
Nothing on macOS itself changed to make room for it, and nothing it
installs is hidden among Apple's own files — which is what lets the
next two articles ask Homebrew direct questions about what it has done
and get a complete answer back.

## Why the internet assumes you have it

Search for how to do almost anything from a Mac terminal, and the
answer usually starts `brew install`. That is not an accident of
popularity. Homebrew is the closest thing macOS has to the package
manager every Linux distribution already has, so it is what the person
writing the instructions is standing on — the same way an instruction
written for a Linux machine assumes `apt` or `dnf` is already there.

Once it is installed, most of what this course has already shown you —
`pandoc`, `ripgrep`, `tesseract`, the whole replacements table from two
articles back — is one line away:

```
brew install ripgrep
```

That line installs a command. The next article is about a different
shape of thing Homebrew also hands you — a whole app, with a window,
installed the same way.

Press `n`.
