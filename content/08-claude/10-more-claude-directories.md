---
id: claude-code/more-directories
title: More .claude directories
part: Claude
section: Claude Code setup
order: 10
summary: You can have as many as you like, one per folder, and each one makes that folder a project.
keywords: [project, project-level, global, layering, multiple, per-folder]
---

# More .claude directories

*v0.1.0*

Here is the fact the last two articles were building towards. `~/.claude`
is not *the* `.claude` directory. It is just the one in your home folder.

You can have another in any folder you like. One per folder, in as many
folders as you want. Nothing special marks them out and nothing registers
them anywhere — a folder either contains a `.claude` or it does not.

## Making one

You do not have to make it by hand. Ask Claude Code:

> *"Set this folder up as its own project with a `.claude` directory and a
> `CLAUDE.md` describing what I do here."*

It will create the folder, write the file, and show you what it wrote. You
can also just make it yourself with `mkdir .claude` if you would rather.

## What that does to the folder

Any folder holding a `.claude` becomes a **project**. That word is not
decoration either — it means the folder has its own:

| Entry | What it holds |
|---|---|
| `settings.json` | settings for work done here |
| `CLAUDE.md` | an invisible prompt for this folder |
| `rules/` | instructions layered on that |
| `agents/` | agents that exist only here |
| `skills/` | skills that exist only here |

Everything from the tour, one level down. A project directory is not a
lesser thing than the global one; it is the same thing in a narrower place.

## It layers, it does not replace

A project's `.claude` sits **on top of** `~/.claude` rather than in place
of it. Instructions from both apply. Agents from both are available.
Skills from both can be chosen.

So the global one is where you put what is true of you everywhere — how
you like to be spoken to, what you never want done without asking. The
project one is where you put what is true of this work only.

> This is also why a project's instructions travel. The `.claude` sits
> inside the folder, so if you send someone that folder, or keep it in
> shared storage, they get the instructions with it.

That is one folder and one directory. Now the interesting part: when you
launch a session, which of them does it actually pick up?

Press `n`.
