---
id: terminal/why-ghostty
title: Why Ghostty
part: Interface
section: The Terminal
order: 5
summary: The terminal you were given, what it does better, and what was set up inside it for you.
keywords: [ghostty, terminal, tabs, config, font, theme, catppuccin]
---

# Why Ghostty

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

## What was set up for you

Someone else wrote your config, so here is what it says, in plain terms:

- **A dark colour scheme**, called Catppuccin Mocha. Soft, low contrast,
  easy on the eyes for long stretches.
- **A font called Hack**, at a comfortable size. It is a *monospace* font,
  meaning every character takes exactly the same width. That is what lets
  this reader line its columns up.
- **A little transparency.** The window is very slightly see-through.
- **No title bar.** This is deliberate, not a fault. You lose nothing and
  gain the space.
- **The bell turned off.** Terminals traditionally beep, flash, and bounce
  in the dock when a program wants attention. Yours does none of that.

None of it is fixed. If the text is too small, the colours are wrong, or
you want the title bar back, that is a sentence to Claude Code rather than
a settings hunt. **The Shell → Starship** has the exact command.

Press `n`.
