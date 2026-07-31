---
id: cli/the-shells-there-are
title: The shells there are
level: Level 1
part: The CLI
section: Shells
order: 5
summary: One family of programs, mostly interchangeable, plus a Boss's opinion of the one that is not
keywords: [shell, bash, zsh, sh, fish, nushell, powershell, unix, family tree]
---

# The shells there are

*v0.2.0*

Everything demonstrated so far ran in one particular program. It is not
the only one. Shells are a family, and knowing the rest of it tells you
which parts of what you have learned travel and which do not.

This matters more than it sounds like it should. Search a problem online
and the answer assumes a shell — usually not yours — and a line copied
from the wrong one can simply fail, with no clue in the error that the
mismatch was the cause.

## The family tree

Shells are unusually well behaved about ancestry. Almost all of them
descend from one program.

**sh** — the Bourne shell, 1977, written at Bell Labs. It established
what a shell is: a prompt, commands, arguments, output piped from one to
the next. Everything since is a reply to it.

**bash** — 1989. A free rewrite of `sh` with the good ideas of the 1980s
folded in, and the shell nearly all published instructions assume. The
name is a pun: *Bourne again shell*.

**zsh** — 1990. A cousin rather than a child. It took what worked from
bash and from the other shells of the day and added better completion,
better history, and a great deal of polish.

What matters practically: **bash and zsh understand each other.**
Commands are typed the same way, and instructions written for bash work
in zsh too. Any difference you are likely to meet lives in configuration
files, not in the everyday commands — so a tutorial written for bash in
2015 is still, for your purposes, a tutorial.

## The other shells

You have no need to switch. It is worth knowing they exist.

| Shell | Its pitch |
|---|---|
| `fish` | friendliest; suggests as you type |
| `nushell` | output as tables, for data work |
| `bash` | the lowest common denominator |

`fish` breaks the usual conventions deliberately in exchange for being
pleasant, which means instructions written for bash sometimes fail in
it. `nushell` treats command output as structured data rather than lines
of text, which is either revelatory or beside the point depending on
your work. Neither is wrong to choose. Both cost you the fact that
almost everything published online assumes bash or zsh, so every guide
needs a small mental translation you do not need with your own shell.

Then there is **PowerShell**, Microsoft's, for Windows.

> The Boss asks that his considered technical assessment be recorded
> here in full: *"PowerShell is dogshit."*

One of the shells in this family is the one your Mac actually gave you.
Which, and why, is next.

Press `n`.
