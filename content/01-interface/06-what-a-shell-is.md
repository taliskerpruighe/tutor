---
id: shell/what-a-shell-is
title: What a shell is
part: Interface
section: The Shell
order: 6
summary: The program that greets you when a terminal opens, and what sits underneath it.
keywords: [shell, kernel, operating system, prompt, command, zsh]
---

# What a shell is

Open Ghostty and something is already there, waiting. A line of text,
then a block cursor sitting after it, doing nothing until you type.

The terminal did not write that. The terminal is only a window. The thing
waiting inside it is a separate program called a **shell**, and it is the
program you are actually talking to.

## Why it is called that

Because of what it wraps around.

Your Mac is built in layers. At the bottom is the **kernel** — the piece of
software that talks directly to the hardware. Everything physical goes
through it: reading the disk, putting pixels on the screen, sending packets
over wifi, handing each running program its slice of memory. Nothing else
is allowed near the metal.

The kernel has no words. It offers a few hundred very precise operations
and expects to be addressed in machine terms. You cannot have a
conversation with it.

So there is a program that sits around it and translates. You type
something close to English; it turns that into the exact operations the
kernel wants; the kernel does them. That wrapper is the shell. The name is
literal — it is the shell around the kernel.

> Everything you think of as "the operating system" — the desktop, the
> Finder, the menu bar, the dock, System Settings — sits on the same
> arrangement. It is a shell too, of a different kind: a graphical one.
> Drag a file to the trash and something, eventually, asks the kernel to
> unlink a file. You have been using this machinery all along.

## So it is the typed version of clicking

That is the whole idea. Things you do by pointing, you can do by typing:

| Pointing | Typing |
|---|---|
| open a folder | `cd` |
| see what is in it | `ls` |
| open a file | `open` |
| trash something | `rm` |
| Spotlight | `find` |
| Shut Down | `shutdown` |

Neither route is more real than the other. They are two doors into the same
building, and the shell is the older one.

The next article is about why anybody would choose the older door.

Press `n`.
