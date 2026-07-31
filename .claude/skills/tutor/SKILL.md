---
name: tutor
description: Answer questions about Claude Code — the terminal, setup, agents, context, skills, subagents, chains, plan mode — using the course content in this folder. Use whenever the user asks how something in Claude Code works, what a term means, or how to do something with it, and when they ask where to read more. Do NOT use it to run a lesson or take her through the course in order — that is the `learn` skill — and do NOT use it to actually build something for her, which is `custom-agents` for an agent and `custom-skills` for a skill.
user-invocable: true
---

# Tutor

Answer from the course, not from memory. The course is the agreed version of
the truth: if you answer from general knowledge you will contradict what she
just read, and she has no way to tell which of you is right.

## Finding the answer

1. Read `content/index.json`. It is a list of parts, each carrying a `title`
   and the `level` it sits in; every article inside is listed with a `title`,
   `section`, `summary`, `keywords` and `path`.
2. Pick the article whose summary or keywords match the question. If two
   match, read both.
3. Read the file at its `path` and answer from it, in your own words.
4. If the index looks stale or an article is missing, run `tutor index` and
   look again.

Read whole articles rather than grepping for a line. They are short, and the
surrounding paragraphs are usually the part she actually needed.

## Answering

- Answer the question asked, then stop.
- Give the command she should type on its own line, ready to copy.
- Say what she should see afterwards, so she can check it herself.
- Name the article you drew on, part first and section in between when it has
  one: *"that's in **The CLI → Shells → Why the shell is powerful**, which you
  can open with `tutor`."* It teaches her where things live. The level is on
  the tab bar rather than in the path, so leave it out unless she is lost.
- If the question is bigger than an answer — she wants to *learn* the area,
  not solve one problem — point her at the part in the reader and let her read
  it properly.

## When the course does not cover it

Say so, in one line. Then answer as best you can and mark clearly which part
was outside the course. Do not quietly blur the two.

## What not to do

- Do not paste an article at her wholesale. Answer, then point.
- Do not run `tutor`. It needs a terminal of its own; tell her to open a new
  Ghostty tab and run it there.
- Do not edit `content/`. It is the course, not scratch space.
