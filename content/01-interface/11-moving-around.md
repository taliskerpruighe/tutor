---
id: shell/moving-around
title: Moving around
part: Interface
section: The Shell
order: 11
summary: Paths, the four commands you need daily, and how to type far less than you think.
keywords: [path, cd, pwd, ls, open, tilde, tab, history, alias, folder]
---

# Moving around

This is the practical one. Everything here you will use on your first day
and keep using.

## A path is an address

Every file and folder on your Mac has an address, written with slashes
between the steps:

```
/Users/you/Documents/notes.md
```

Read it left to right: start at the very top of the disk, go into `Users`,
then your account name, which is where all your own files live, then
`Documents`, and there is the file. The Finder shows you the same thing as a
row of folder icons. The shell writes it as one line.

An address that starts with `/` is **absolute** — it begins at the top and
is true from anywhere. An address that does not is **relative**: it starts
from wherever you are standing right now. `Documents/notes.md` means "the
`Documents` in this folder", which depends entirely on which folder that
is.

## Three shorthands

| Written | Means |
|---|---|
| `~` | your home folder |
| `.` | the folder you are in |
| `..` | the folder above this one |

`~` is the most used character on the terminal. It saves writing
`/Users/your-name` every time, and it is why this course keeps writing
`~/tutor`.

`..` is how you go up. It stacks: `../..` is two levels up. And it combines
with names, so `../Downloads` means "up one, then into Downloads" — a
sideways move, in one step, with no walking through the folder above.

## The four commands

**`pwd`** — where am I?

```
pwd
```

**`ls`** — what is in here?

```
ls
ls ~/Documents
```

**`cd`** — go somewhere.

```
cd ~/tutor
cd ..
cd
```

The last one, on its own, takes you home. Useful when you are lost.

**`open`** — hand something to the Finder or an app.

```
open .
```

That opens a Finder window on the folder you are standing in — the bridge
back to the world of icons, and a good way to convince yourself the shell
and the Finder are looking at the same thing. `open notes.md` opens a file
in whichever app usually handles it.

## How a command is put together

Look at:

```
ls -la ~/Documents
```

Three parts, always in this order:

- **`ls`** — the program's name. Which one to run.
- **`-la`** — options, sometimes called *flags*. They start with a dash and
  change how it behaves. Here: `l` for a long detailed listing, `a` to
  include hidden files.
- **`~/Documents`** — the argument. What to run it on.

Every command you meet has that shape. When you see something impenetrable,
splitting it into those three parts is usually enough to guess what it
does.

## Typing much less

Three habits, worth forming immediately.

**`Tab` finishes things for you.** Type a few letters of a folder or file
name and press `Tab`. If there is only one match it completes it. If there
are several, press `Tab` again to see them. You almost never need to type a
whole name, which also means you almost never misspell one.

**`↑` brings back what you already typed.** Press it repeatedly to walk
back through your history. Nothing you have run is more than a few presses
away, and editing an old command beats retyping it.

**`Ctrl-C` stops whatever is running.** If something is churning, or
printing forever, or you typed half a line and want out — `Ctrl-C`. It is
the escape hatch, it is safe, and it is worth using early rather than
sitting there wondering.

## Making it shorter still

Notice you keep typing the same things. `cd ~/some/long/project/path` every
morning. A command with the same four options every time.

The shell can be taught. An **alias** is a nickname for a command; a
**variable** is a nickname for a piece of text, such as a long path. Once
set up, a whole line collapses to a word you invented, and it works from
anywhere.

This is a good early thing to ask Claude Code for. Open a Ghostty tab and
say what you keep typing and what you would rather type:

```
cd ~/tutor && claude
```

*"Every morning I run `cd ~/Documents/clients/acme`. Give me a shortcut
called `acme`."* It will write it into your shell's config file and tell
you how to make it live.

Press `n`.
