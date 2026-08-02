---
id: claude-code/claude-directory
title: The .claude directory
level: Level 2
part: Claude
section: Claude Code setup
order: 8
summary: The harness lives in an ordinary hidden folder called .claude, not on a server.
keywords: [dotfile, hidden file, home directory, global, user-level, config]
---

# The .claude directory

*v0.1.0*

claude.ai is a website. Claude Cowork is a website. Claude Code is not —
*Why Claude Code* explained why: the harness needs your files and your
terminal, so it lives where they are, on your Mac. Only the model is ever
somewhere else.

Everything the harness owns — its settings, and everything you go on to
build over the rest of this course — sits inside one folder, called
`.claude`.

## A dotfile

The leading dot is not decoration. On a Unix system — and macOS is one
underneath — a name starting with a dot is a **hidden file**. Hidden files
do not appear in a normal folder listing or in Finder, so they stay out of
the way of the things you actually go looking for.

It is a convention, not a lock. Nothing stops you opening one, reading it,
or editing it by hand — it is agreed, by long habit, that configuration
lives behind the dot and everything else stays in front of it.

You can see them. In Ghostty:

```
ls -a ~
```

`-a` means "all", including the hidden ones. In Finder, `Cmd-Shift-.`
toggles them on and off in any window.

> `.claude` will not be there until you have run Claude Code at least
> once. It is created the first time it is needed, not before.

## The global one

The `.claude` you have is the **global** one — also called **user-level** —
and it sits at `~/.claude`. `~` is your home folder, so this one applies
everywhere you run Claude Code, whatever you happen to be working on.

The rest of this part is about that directory: what is inside it, and
then the more interesting fact that it is not the only one you can have.

> Plain files, rather than settings buried inside an app, are a deliberate
> choice. A plain file can be read. It can be copied to another machine in
> seconds. And Claude Code can read and edit its own configuration.

Next, a tour of what is inside.

Press `n`.
