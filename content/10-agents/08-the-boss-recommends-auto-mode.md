---
id: perms/auto-mode
title: The boss recommends: auto mode
level: Level 2
part: Agents
section: Plans and Permissions
order: 8
summary: His own default is auto mode, taught once what counts as sensitive and left alone after that
keywords: [auto mode, default permission mode, settings.json, autoMode.environment, sensitive files, version control, boss]
---

# The boss recommends: auto mode

*v0.2.9*

Five modes were on the table in the last article, and the Boss settled
on one for his own baseline. Not default, and not accept edits — auto,
set once in his global settings, and left there.

Default asks about too much to get through a working day on. Bypass
permissions asks about too little to trust with anything that
matters. Auto sits between the two, and the difference between a
tolerable one and a dangerous one is entirely in what you tell it.

## Set once, not every morning

`Shift-Tab` changes a mode for the session you are sitting in, as
*Changing permission modes* showed. That is fine for an exception. It
is not how the Boss chooses the mode running underneath him five
sessions and three matters into a Tuesday.

Ask an agent to do it.

> *"Set my default permission mode to auto in my global settings."*

Say it in those words, or near enough, and the agent finds the right
key in your global `settings.json` and sets it there. Every session
after that opens already in auto mode, with nothing further asked of
you at the start of the day.

## Teaching it what to be careful with

Auto skips asking against criteria — *The permission modes there are*
said as much — and criteria left unset borrow a judgement the session
does not have. The Boss fills that gap with an `autoMode.environment`
entry in the same settings file, and again an agent writes it for you:
tell it, in plain English, which files or folders deserve a stop and
ask before anything happens to them, deleting especially.

> *"Add an autoMode.environment setting that asks before touching
> anything in my personal notes folder, and always before deleting."*

The sentence does the work. You are not editing JSON by hand and you
are not memorising a schema — you are saying, once, what a colleague
would already know to leave alone.

## Where that matters most

Auto's confidence is mostly borrowed from version control — a bad
edit to a tracked file is a `git diff` away from being undone, and the
willingness to let a session run with less supervision comes from that
safety net sitting underneath it. The exception is anything outside
it: a folder never put under version control, or one that only ever
lived in cloud storage — a client's bundle kept in Google Drive
rather than a repository, say. Name those specifically, and auto mode
asks before it touches them regardless of what its own judgement
would otherwise have allowed.

One mode set as a baseline, and one reached for on purpose. The next
article is the second.

Press `n`.
