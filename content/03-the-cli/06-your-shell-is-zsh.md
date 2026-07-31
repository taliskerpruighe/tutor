---
id: shell/your-shell-zsh
title: Your shell is zsh
level: Level 1
part: The CLI
section: Zsh
order: 6
summary: Which one you actually have, why Apple chose it, and the standard that makes it worth learning once
keywords: [zsh, echo, shell, unix, posix, apple, licence, linux]
---

# Your shell is zsh

*v0.2.0*

It is **zsh** — the Z shell — and you did not choose it. It is what
every Mac has opened with since 2019. You can confirm it:

```
echo $SHELL
```

It prints `/bin/zsh`.

## Why Apple picked it

Apple switched the default from bash to zsh in 2019. The reason was a
licence change rather than a technical judgement — the newer versions of
bash come with terms Apple would rather not ship, so macOS stayed on an
old bash release for years and then moved to zsh instead of updating
it. You inherited a good shell for a boring reason, and nothing about
the choice reflects on you. Nobody sat down and picked zsh for its
completion or its history; a lawyer somewhere made the decision for
you.

## Unix, and what that actually means

**Unix** is the Bell Labs project that produced `sh` in the first place:
an operating system whose design was so sound that everything since has
copied it. Your Mac is not merely inspired by Unix; it is a genuine
certified descendant, tested against the same specification and
licensed to use the name. Linux is an independent rebuild of the same
design, done in the open rather than certified by anyone — the same
ideas, arrived at without the paperwork. The servers running nearly all
of the internet are in this family somewhere.

## POSIX, and why this is worth learning once

**POSIX** is the written standard that pinned that design down — a
document saying which commands a Unix-like system must provide, and how
each must behave.

That standard is the reason zsh is worth learning at all rather than
merely tolerating. `cd`, `ls`, `grep` and their kin work the same on your
Mac, on a Linux laptop, and on a server in a data centre you will never
see. Nothing you learn typing at this prompt is specific to it. It
travels to any machine you are ever handed, this Mac included only as
one example among many.

> You can still swap zsh for something else if you want to. Almost
> nobody does, and the last article named why: everything written for
> the internet at large assumes you are running bash or zsh, and you
> already are.

That is the shell settled. What you actually do with it — the paths,
the four commands you will use daily, and how to type far less than you
think — is next.

Press `n`.
