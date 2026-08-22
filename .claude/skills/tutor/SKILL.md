---
name: tutor
description: Answer questions about Claude Code — the terminal, tmux, the shell, software and packages, files and version control including worktrees and forking, Linux, LLMs and harnesses, Claude and its setup, agents, context, permission and plan modes, prompt engineering, skills, subagents, chains, workflows, hooks, plugins, output styles, the status line, headless sessions — using the course content in this folder. Use whenever the user asks how something in Claude Code works, what a term means, or how to do something with it, and when they ask where to read more. Do NOT use it to run a lesson or take them through the course in order — that is the `learn` skill.
user-invocable: true
---

# Tutor

Answer from the course, not from memory. The course is the agreed version of
the truth: if you answer from general knowledge you will contradict what they
just read, and they have no way to tell which of you is right.

## Finding the answer

1. Read `content/index.json`. It is a flat list of parts, each carrying a
   `title` and the `level` it sits in, each holding a flat list of articles —
   a level and a section are both derived, not stored, each one a run of
   consecutive entries sharing the same `level` or `section` string. Every
   article is listed with an `id`, `title`, `section`, `summary`, `keywords`
   and `path`.
2. Pick the article whose summary or keywords match the question. If two
   match, read both.
3. Read the file at its `path` and answer from it, in your own words. Quote
   the article's `id` rather than its `path` if you need to name one
   precisely — the `id` is stable across releases, the `path` is not.
4. If the index looks stale or an article is missing, run `tutor index` and
   look again.

Read whole articles rather than grepping for a line. They are short, and the
surrounding paragraphs are usually the part actually needed.

**Section names repeat across parts.** *Building One* is in both Skills and
Workflows; *What They Are* is in Workflows, Hooks and Plugins; *Using Them*
is in Hooks and Plugins. A few newer names sit close enough to an older one
to be said the same way by mistake: *Prompts* (Agents) next to *Command
Lines and Prompts* (The CLI), *Plans and Permissions* (Agents) next to *The
plans* (Claude → Claude subscriptions), and *Worktrees* (Version Control) —
both a section and the article that opens it — next to Hooks'
*WorktreeCreate and WorktreeRemove*. Never match on `section` alone — carry
the `part` with it, or you will read the wrong article and cite the wrong
place.

## The shape of the course

**Derive it from `content/index.json` every time. Never from memory, and
never from a list written here.** Parts run in the order they appear in the
file. A level is a run of consecutive parts sharing a `level`; a section is a
run of consecutive articles sharing a `section`. Some parts have no sections
at all, and which ones those are changes between releases — read it, do not
recall it.

The same goes for how many parts there are, where a level ends, and where the
course ends. Every one of those is a fact about the file in front of you, and
any count written into this skill is a count that will be wrong later.

Six Party Tricks run through the course and are what it exists for:
content isolation (Claude Code Setup), the three resets and agent
engineering (Agents), skill engineering and always invoking manually
(Skills), and chain engineering (Subagents → Chains). If a question lands on
one, say which it is.

## Answering

- Answer the question asked, then stop.
- Give the command they should type on its own line, ready to copy.
- Say what they should see afterwards, so they can check it themselves.
- Name the article you drew on, part first and section in between when it has
  one: *"that's in **The CLI → Shells → Why the shell is powerful**, which
  you can open with `tutor`."* It teaches where things live. The level is on
  the tab bar rather than in the path, so leave it out unless they are lost.
- If the question is bigger than an answer — they want to *learn* the area,
  not solve one problem — point them at the part in the reader and let them
  read it properly, or say `/learn` will walk them through it a section at a
  time.

## When the course does not cover it

Say so, in one line. Then answer as best you can and mark clearly which part
was outside the course. Do not quietly blur the two.

## What not to do

- Do not paste an article at them wholesale. Answer, then point.
- Do not run `tutor`. It needs a terminal of its own; say to open a new
  Ghostty tab and run it there. Subcommands are fine — `tutor index` and
  `tutor doctor` both run happily from here.
- Do not run `tutor update`. It needs no terminal, so nothing will stop you,
  and it replaces the whole of `~/tutor` while you are working in it.
- Do not edit `content/`. It is the course, not scratch space.
