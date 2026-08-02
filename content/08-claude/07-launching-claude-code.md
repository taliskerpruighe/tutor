---
id: claude-code/launching
title: Launching Claude Code
level: Level 2
part: Claude
section: Claude Code setup
order: 7
summary: Type claude and press enter — and understand the one thing that changes what happens next.
keywords: [launch, start, ghostty, ide, cd, working directory, cwd, session]
---

# Launching Claude Code

*v0.1.0*

Open Ghostty. Type this:

```
claude
```

Press Enter. That is the whole ceremony.

## Why from Ghostty

There are other ways in. Claude Code has integrations that put it inside a
code editor, in a panel beside your files. They are good, and they are
built for someone whose day is writing code — the panel earns its place
when you are jumping between the answer and the file it belongs to.

That is not what you are doing. You want the thing in a Ghostty tab of
its own, with the reader in the tab next door, and nothing else on screen
competing for the space. `Cmd-T` gives you the tab; `claude` gives you the
session.

## What makes no difference

A short list, because it is easy to worry about the wrong things:

- **Which shell you are running.** Yours is zsh. It would behave the same
  under any other.
- **What else you have open.** Other apps, other Ghostty tabs, a browser
  full of tabs — none of it reaches Claude Code.
- **Other Claude Code sessions.** You can have several running at once, in
  several tabs. They do not see each other and they do not interfere.

None of that changes a thing about the session you are starting.

## What makes all the difference

One thing does, and it is the thing nobody tells you: **the folder you are
standing in when you press Enter.**

That folder — your working directory, the one `cd` moves you to and the
one `pwd` prints — is where the session takes root. It decides which files
Claude can reach without being told where to look, and, as the articles
after this one explain, it decides which instructions, agents and skills
the session even knows exist.

So the habit is two commands, in this order, every time:

```
cd ~/tutor
claude
```

Or, on one line, which is what you will settle into:

```
cd ~/tutor && claude
```

> Starting in the wrong folder is the single most common reason a session
> behaves worse than you expected. Not a worse model — a worse view. Press
> `q` to quit, `cd` to the right place, and start again. It costs seconds.

Why the folder carries that much weight is the subject of the rest of this
part.

Press `n`.
