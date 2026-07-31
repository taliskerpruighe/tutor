---
id: files/why-plain-text-wins
title: Why plain text wins
part: Files
section: Languages and Scripts
order: 2
summary: A machine can read a plain file without being told how, and almost everything in this course rests on that one fact
keywords: [plain text, file format, md, txt, json, jsonl, doc, xls, diff, search, edit]
---

# Why plain text wins

*v0.2.0*

Because a machine can read it without being told how.

A **plain text file** holds nothing but characters — letters, digits,
punctuation, laid out on lines — and nothing else. `.md`, `.txt`,
`.json` and `.jsonl` are plain text. `.doc` and `.xls` are not: open
either in something that is not Word or Excel and you get either
nothing, or the file's insides — styling codes, compression, private
bookkeeping the format keeps for itself.

That is the whole difference, and a great deal of this course rests
on it.

## What a plain file buys you

Any program that exists can open a plain text file — read it, search
inside it, compare two versions of it, copy it, edit it — because
there is nothing to decode first. Claude Code reads your `CLAUDE.md`
the way you would: it opens the file and there the words are.

- **Read.** No conversion step, no missing plugin, no "this document
  was created in a newer version".
- **Diffed.** Two versions of a plain file can be laid side by side
  and every changed word shown, which is the whole basis of version
  control, coming up later in this part.
- **Searched.** A tool can look inside a thousand plain files for one
  word in under a second. It cannot look inside a thousand `.doc`
  files at all, not without opening each one first.
- **Edited by a machine.** An agent can open a plain file, change one
  line, and save it back, because a line is a real thing in a plain
  file. A `.doc` has no lines — only a rendered page, assembled from a
  format only Word fully understands.

## What proprietary costs you

A **proprietary file** — `.doc`, `.xls`, `.pdf` in its usual form — can
be opened by exactly one program, or a small handful built to imitate
it. Everything about it is designed for a human looking at a screen,
not for another piece of software reading it.

That is not a flaw in Word. Word was built to be looked at. It was
never built to be read by something else, and the moment you want a
program — Claude Code included — to work with a file rather than
merely display it, that becomes the whole problem.

## Why this keeps mattering

Settings, instructions, skills, logs: every one of them, from here on,
is a plain text file, because a plain text file is the only kind an
agent can open, understand and change without help. Reach for it
because it is plain, then reach for the shape that fits the job —
which is what the next article sorts out.

Press `n`.
