---
id: terminal/why-ghostty
title: Your terminal is Ghostty
part: TUIs
section: Ghostty
order: 5
summary: The terminal you were given, what it does better than the one your Mac came with, and the four keys worth knowing.
keywords: [ghostty, terminal, tabs, windows, config, cmd-t, macos, graphics chip]
---

# Your terminal is Ghostty

*v0.1.0*

Your terminal is **Ghostty**. Your Mac came with a different one, called
Terminal, and Ghostty was installed alongside it. Terminal still works and
is still there. You have no reason to open it.

## What it does better

**It is quick.** Ghostty draws text using the graphics chip, the same one
that draws games. You will notice this when something prints a lot at once
— a long file, a build, an agent thinking out loud. A slower terminal
stutters through that. This one does not.

**It is a real Mac app.** It behaves the way you expect a Mac app to
behave, because it was written as one rather than wrapped up out of web
pages, which is how a surprising number of desktop apps are made.

**It runs the same on Linux.** One config file, both machines. That matters
less to you today than it does to whoever helps you, but it is why your
setup could be copied over from a machine that is not a Mac at all.

**Its defaults are sane.** Most terminals expect you to spend an evening
configuring them. This one is mostly right out of the box, and its config
file is plain `setting = value` lines rather than a programming language
you have to learn first.

## The keys worth knowing

| Key | What it does |
|---|---|
| `Cmd-T` | new tab |
| `Cmd-N` | new window |
| `Cmd-W` | close the tab |
| `Cmd-,` | open the config file |

`Cmd-T` is the one you will lean on. The intended way to work is two tabs:
this reader in one, Claude Code in the other, switching between them.

You did not choose any of the defaults you are looking at, and the next
article is what they are.

Press `n`.
