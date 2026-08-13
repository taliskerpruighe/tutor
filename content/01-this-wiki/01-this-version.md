---
id: wiki/this-version
title: This version
level: Level 1
part: This Wiki
order: 1
summary: What this version of the course covers, what it leaves out on purpose, and what a later one adds
keywords: [version, roadmap, agents, skills, subagents, workflows, hooks, plugins, headless, version control, prompts, permissions, changelog]
---

# This version

*v0.2.9*

This is version 0.2.9, and it still covers the whole path from opening
a terminal for the first time to running an agent that works
unattended, with nobody watching it. The path has not changed. The
ground it covers along the way has grown considerably, and this
article is about where.

The course now runs to 152 articles across eighteen parts, up from
122.

## What's new

**TMUX** is now a full nine-article section: the prefix key,
sessions, windows and panes, detaching and reattaching, the config
file, copy mode, the status bar. **The CLI** gained six articles on
the Zsh tools worth actually knowing — `zoxide`, exporting permanent
variables, globbing, `grep`, `ripgrep`, `fzf` — and split its old
prompt-theme article in two, *Powerline themes* standing apart from
*Starship* rather than sharing a page with it.

**Agents** picked up two whole new sections. *Plans and Permissions*
covers the permission modes sitting at the bottom of every interactive
session and what plan mode is for; *Prompts* covers writing one that
actually works. Two standalone articles joined them: `ccstatusline`,
the status line the Boss uses rather than writing one by hand, and
*Output styles*.

**Version control** left Level 1's Files part and became a part of
its own, in Level 2. The four articles that lived there — *What git
is*, *How git works*, *Jujutsu*, *GitHub* — moved with it, joined by
three new ones: *Git and the harness*, *Worktrees* and *Forking*.
**Hooks** replaced its single *Worked examples* article with six, one
per trigger family, rather than asking one page to stand in for all
of them.

None of that is a reading assignment. A green `N` sits in the margin
beside exactly the articles this version added, in the same slot the
read tick occupies, and it clears the moment you read the article or
the moment the next version ships, whichever comes first.

## What's next

Three further levels are sketched, not built. **Level 3** is
automation and integration — plugging Claude Code into databases,
MCPs, LSPs, APIs, external hooks and channels, and the agent SDK
underneath all of it, so that it runs against your own systems rather
than only your own terminal. **Level 4** is machine learning — cloud
sessions and remotes, cron, loops and goals, an agent that trains and
improves itself rather than waiting to be asked each time. **Level 5**
is putting all of it to work in business applications.

None of that has a date attached, and nothing here is a promise about
one. It is the shape of where this course is going, not a schedule for
getting there.

The next article is *About this wiki* — what this course is, who
writes it, and how it differs from Anthropic's own documentation.

Press `n`.
