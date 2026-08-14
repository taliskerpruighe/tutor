---
id: shell/moving-around
title: Moving around
level: Level 1
part: The CLI
section: Zsh
order: 5
summary: Paths, the four commands you need daily, and the fastest way from one folder to a neighbour rather than a stranger
keywords: [path, cd, pwd, ls, open, tilde, tab, alias, folder, sideways]
---

# Moving around

*v0.2.9*

A path is the address of whatever you want the shell to act on — a file, a
folder, a client's matter. Nothing later in this course works until you can
write one, read one, and get from it to another without stopping to think.

This is the article that earns its keep: three shorthands, four commands,
and how to type a great deal less than you think.

## A path is an address

Every file and folder has one, written left to right with slashes between
the steps:

```
/Users/you/Documents/notes.md
```

Start at the top of the disk, into `Users`, into your account, into
`Documents`, and there is the file. An address beginning with `/` is
**absolute** — true from anywhere. One that does not is **relative**,
measured from wherever you are standing, so `Documents/notes.md` means
something different in every folder you type it from.

Three shorthands cover most of it:

| Written | Means |
|---|---|
| `~` | your home folder |
| `.` | the folder you are in |
| `..` | the folder above this one |

`~` saves writing `/Users/your-name` every time. `..` stacks — `../..` is
two levels up — and it combines with names, so `../Downloads` means up one,
then into `Downloads`, without passing through the folder in between.

## The sideways move

Client folders mostly sit next to each other, not inside one another:

```
~/work/
├── mackenzie/
├── okonjo/
└── hartley/
```

Getting from one to another is rarely a walk down through folders you
already know — it is a step sideways. `cd ../okonjo` goes up one from
wherever you are inside `mackenzie` and straight into `okonjo`, with no
need to know the full address or go home first. `~/work/okonjo` does the
identical job from anywhere, in one line, if you would rather write the
whole thing.

## The four commands

**`pwd`** tells you where you are, on its own, no argument. **`ls`** tells
you what is there — plain for here, `ls ~/Documents` for somewhere else.
**`cd`** takes you somewhere: `cd ~/tutor`, `cd ..`, or `cd` by itself,
which takes you home from anywhere and is worth remembering the moment you
are lost. **`open .`** hands the folder you are standing in to the
Finder — the bridge back to icons, and proof the shell and the Finder are
looking at the same folders.

## Typing far less than you think

`Tab` finishes what you are typing. A few letters of a folder name, then
`Tab`, and it completes — which matters more than it sounds like it
should, because a folder name mistyped by one letter does not error. `cd`
into a folder that does not exist fails, quietly, and leaves you
standing exactly where you were, easy to miss if nobody else is watching.
A completed path is a path you know is right.

`↑` walks back through what you have already typed, so returning to a
folder you had open this morning is a few presses, not a retyped address.
`Ctrl-C` gets you out of a `cd` you started typing and changed your mind
about, before it runs against the wrong folder.

## Making it shorter still

Notice you keep typing the same thing — `cd ~/Documents/clients/acme-corp`,
every morning. An **alias** is a nickname for a command, and the shell can
be taught one.

This is a good early thing to ask Claude Code for: open a chat and say
what you keep typing and what you would rather type instead. *"Every
morning I run `cd ~/Documents/clients/acme-corp`. Give me a shortcut
called `acme`."* It will write the alias into your shell's config file and
tell you how to make it live.

`cd` only ever takes you exactly where you type.

Press `n`.
