---
id: shell/your-shell-zsh
title: Your shell is zsh
part: Interface
section: The Shell
order: 8
summary: Which shell you have, where it came from, and what the others are.
keywords: [zsh, bash, sh, unix, posix, fish, nushell, powershell]
---

# Your shell is zsh

There is more than one shell. Yours is called **zsh** — the Z shell — and
you did not choose it. It is what every Mac has opened with since 2019.

You can confirm it:

```
echo $SHELL
```

It prints `/bin/zsh`.

## The family tree

Shells are unusually well behaved about ancestry. Almost all of them
descend from one program.

**sh** — the Bourne shell, 1977, written at Bell Labs. It established what
a shell is: a prompt, commands, arguments, output piped from one to the
next. Everything since is a reply to it.

**bash** — 1989. A free rewrite of `sh` with the good ideas of the 1980s
folded in, and the shell nearly all published instructions assume. The name
is a pun: *Bourne again shell*.

**zsh** — 1990. A cousin rather than a child. It took what worked from
bash and from the other shells of the day and added better completion,
better history, and a great deal of polish.

What matters practically: **bash and zsh understand each other.** Commands
are typed the same way, and instructions written for bash work in yours.
Any difference you are likely to meet lives in configuration files, not in
the everyday commands.

> Apple switched the default from bash to zsh in 2019. The reason was a
> licence change rather than a technical judgement — the newer bash comes
> with terms Apple would rather not ship. You inherited a good shell for a
> boring reason.

## Unix and POSIX

Two words that will come up.

**Unix** is that same Bell Labs project from the 1970s: an operating system
whose design was so sound that everything since has copied it. Your Mac is
not merely inspired by Unix; it is a genuine certified descendant. Linux is
an independent rebuild of the same design. The servers running nearly all
of the internet are in this family.

**POSIX** is the written standard that pinned the design down — a document
saying which commands a Unix-like system must provide and how each must
behave.

That standard is why this is worth learning once. `cd`, `ls`, `grep` and
their kin work the same on your Mac, on a Linux laptop, and on a server in
a data centre you will never see. The knowledge travels.

## The other shells

You have no need to switch. It is worth knowing they exist.

| Shell | Its pitch |
|---|---|
| `fish` | friendliest; suggests as you type |
| `nushell` | output as tables, for data work |
| `bash` | the lowest common denominator |

`fish` breaks the POSIX rules deliberately in exchange for being pleasant,
which means instructions written for bash sometimes fail in it. `nushell`
treats command output as structured data rather than lines of text, which
is either revelatory or beside the point depending on your work.

Then there is **PowerShell**, Microsoft's, for Windows.

> The Boss asks that his considered technical assessment be recorded here
> in full: *PowerShell is dogshit.*

Press `n`.
