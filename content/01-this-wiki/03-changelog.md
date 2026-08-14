---
id: wiki/changelog
title: Changelog
level: Level 1
part: This Wiki
order: 3
summary: What changed in each version before this one, kept so a returning reader can find the delta
keywords: [changelog, version, history, update, 0.1.0, 0.2.0, 0.2.1, 0.2.2, 0.2.9, 0.2.10]
---

# Changelog

*v0.2.10*

This page exists for exactly one reader: someone who has already been
through this course once, came back after an update, and does not want
to reread all of it to find out what is new. Skip it the first time
through.

## 0.2.10 — other models, and a longer memory for the marker

*This version* covers the shape of the course as it now stands. This
page covers only the difference between that and what was here
before.

New material, not present before:

- **Other Models** is a whole new part, twelve articles, on pointing
  Claude Code at a model that is not Claude and what you give up by
  doing it, with two worked examples at opposite ends of the range —
  Ollama on your own machine, and Kimi, a paid cloud endpoint reached
  over the internet.
- **Agentic AI** gained a new article, *Running one yourself*, in its
  LLMs section — the first mention of Ollama, ahead of the fuller
  treatment it gets in Other Models.
- **Level 2** was reordered: the Claude part now leads with the
  harness itself — Claude Code, then the alternatives, then the
  models — and **Claude Code Setup**, previously a section inside
  that part, is promoted to a part of its own, after Other Models.
- Read marks are kept against an article's own identity, not its
  place in the course, so the renumbering cost nobody a tick.

The green `N` changed alongside it. It used to mark only the newest
version's articles; from this version it marks two versions' worth,
so upgrading to 0.2.10 shows everything added in 0.2.9 and 0.2.10
both, not only the latest batch. A fresh install still shows none.

## 0.2.9 — the parts that grew

*This version* covers the shape of the course as it now stands. This
page covers only the difference between that and what was here
before.

New material, not present before:

- **TMUX** is now a full seven-article section.
- **The CLI** gained six articles on the Zsh tools worth knowing —
  `zoxide`, permanent variables, globbing, `grep`, `ripgrep`, `fzf` —
  and its old prompt-theme article split into *Powerline themes* and
  *Starship*.
- **Agents** gained two whole sections, *Plans and Permissions* and
  *Prompts*, plus standalone articles on `ccstatusline` and *Output
  styles*.
- **Version control** left Level 1's Files part for a part of its own
  in Level 2, joined by three new articles: *Git and the harness*,
  *Worktrees* and *Forking*.
- **Hooks** replaced its single *Worked examples* article with six,
  one per trigger family.

As in every version that adds articles, a green `N` marks exactly the
ones new to a returning reader.

## 0.2.2 — the reader's own marks

No articles were added, removed or moved, so *This version* went on
describing the course untouched.

What changed sits underneath the reading experience: the check for a
new version used to run at most once a day, cached outside the course
folder. It now runs on every launch, so word of a new version reaches
you the next time you type `tutor`.

## 0.2.1 — instructions, and the new marker

*This version* still covers the shape of the course as it stands —
what the parts are and what each is for. This page covers only the
difference between that and what was here before.

New material, not present before:

- **Instructions** — the files that teach an agent how to behave: what
  a `CLAUDE.md` is, how it loads — up from the folder you launch in,
  and again whenever Claude touches a file in its own directory — how
  to write one that actually works, and when to reach for a rule
  instead.

**Claude** also moved, from closing out Level 1 to opening Level 2,
ahead of Instructions. Level 1 is everything Claude Code sits on top
of; Claude Code itself belongs with the level built on it, not the
level underneath it.

The reader also gained a green **N**, sitting beside an article's
number in the same slot the read tick uses. It marks an article this
version added that you have not read yet, and reading the article
replaces it with the tick. It only appears if you upgraded — a reader
starting fresh has nothing new to mark — and every tick already earned
is untouched by it.

## 0.2.0 — the reorganisation

The course was reorganised from a handful of broad parts into fifteen
narrower ones, so a part stays on the tab bar you can actually hold in
your head rather than scrolling past it. Nothing already written was
thrown away; some articles were split where the old organisation had
folded two subjects into one.

New material, not present before:

- **The world underneath Claude Code** — terminals, shells, packages,
  plain files against proprietary ones, and Linux, covered properly
  rather than assumed.
- **What a model and a harness are**, named and explained before Claude
  Code is introduced as one example of each.
- **Workflows, hooks and plugins** — wiring several agents together on
  a script rather than in a conversation, and sharing the result.
- **Headless sessions** — running any of the above with no chat window
  open.
- **Cloud computing**, brought forward from a later version because
  hardware limits come up earlier than expected once agents start
  running several things at once.

The reader also picked up **read marks** in this version. Press `m` on an
article to tick it as read, and press `m` again to clear the tick. The
reader still opens on the first article every time — that has not changed —
but the ticks themselves are kept between sessions, outside the course
folder, so reinstalling or updating this course does not clear them.

## 0.1.0 — the first version

The original release. It covered agents, skills and subagents, and
everything strictly needed to reach them: the terminal, the `.claude`
directory, and installing Claude Code itself. Everything else in the
Mac you were already sitting at — the shell, the software, the files —
was assumed rather than taught, on the reasoning that you had been
using a computer for years and did not need it explained.

It said, at the time, that hooks, MCP and plugins would come in the
version after it, and crons and cloud computing in the one after that.
This version is that promise, restructured rather than simply
renumbered: some of it arrived earlier than planned, and some of it is
still to come.

Later versions add their own entry above this one, oldest at the
bottom, so the whole history stays in one place rather than scattered
across release notes nobody kept.

That is what the course is and how it got here.

Press `n`.
