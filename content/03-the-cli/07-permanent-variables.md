---
id: zsh/permanent-variables
title: Permanent variables
level: Level 1
part: The CLI
section: Zsh
order: 7
summary: A variable typed at the prompt dies with the terminal; the same line in ~/.zshrc survives every one you open after
keywords: [variable, export, environment variable, zshrc, path, permanent, shell, source]
---

# Permanent variables

*v0.2.9*

A **variable** is a name standing in for a piece of text. Set one at the
prompt and it works immediately — and dies the moment you close the
terminal.

```
export CLIENT=okonjo
echo $CLIENT
```

That prints `okonjo`. Open a new tab and ask again, and the variable is
gone. Nothing was saved; it lived in that one terminal and nowhere else.

`export` is doing more than naming a value. Leave it off — `CLIENT=okonjo`
on its own — and the variable still works in `echo $CLIENT`, but nothing
you launch from that shell can see it. `export` is the difference between
a note to yourself and a note pinned up for everything that follows.

## Making one permanent

The fix is the file zoxide already introduced you to. Put the same
`export` line in `~/.zshrc`, and every terminal you open reads it on the
way up, so the variable exists before you have typed a single command:

```
export CLIENT=okonjo
```

Reload the current terminal with `source ~/.zshrc`, or simply open a new
tab — either reads the file again from the top.

## The one you already rely on

`PATH` is a permanent variable already set on your Mac, and it is the
reason typing `ls` or `zoxide` works at all. It holds a list of folders,
and the shell checks every one of them for a program by that name before
it gives up. Installing a program, most of the time, is nothing more than
putting a new file into one of the folders `PATH` already lists.

```
echo $PATH
```

That prints the whole list, colon-separated, longer than you would
guess. You will not need to edit it by hand — an installer does that for
you, appending its own folder to the end.

## A second one worth having

`EDITOR` names the program a terminal tool should hand you a file in when
it needs you to write something — a commit message, a scheduled task, a
note `crontab -e` opens for editing. Left unset, several of these fall
back to something unfamiliar and leave you stuck in a program you do not
know how to leave.

```
export EDITOR=nano
```

Set once in `~/.zshrc`, that answers the question permanently, for every
tool that ever asks it.

## Asking for one

This is the same habit as the alias from *Moving around*: say what you
want remembered and let Claude Code write the line. *"Set a permanent
variable called `MATTER_ROOT` pointing at `~/work`, so every terminal
already knows where matters live."* It will add the export line to
`~/.zshrc` and tell you how to make it live.

A variable is a name for one exact piece of text. The next article is a
different kind of shorthand — one that stands for many filenames at once,
without naming any of them.

Press `n`.
