---
id: headless/piping
title: Piping
part: Headless Sessions
section: Running Without a Chat
order: 3
summary: The one shell operator Moving around left out on purpose, and the reason a headless session needed it first
keywords: [pipe, piping, shell, stdin, stdout, redirect, claude -p, pbcopy, cat, grep]
---

# Piping

*v0.2.0*

*Moving around* named the four commands you would use every day and
stopped there. One piece of shell grammar was missing from it, on
purpose: the pipe. It needed a job worth doing before it earned its
place, and a headless session is that job.

## The operator

`|` takes the output of the command on its left and hands it to the
command on its right, as if you had typed it in yourself:

```bash
cat matter.md | wc -l
```

`cat` prints the file; instead of landing on your screen, that text
goes straight into `wc -l`, which counts lines. Neither command knows
the other exists. Each reads whatever arrives and writes whatever it
produces, and the pipe is the join between them. Chain more than two
and the same rule applies at every join.

## Feeding a headless session

A file, or the output of another command, can be the thing on the left:

```bash
cat bundle.md | claude -p "Summarise in three sentences"
```

```bash
grep -l "privileged" *.md | claude -p "List these in order"
```

The first hands it a whole document. The second hands it a list of
filenames a `grep` already narrowed down — the search doing the finding,
the headless session doing the reading, neither one built to do the
other's job.

## Sending the answer onward

The same operator works on the way out, because a headless session's
answer is plain text landing on standard output, exactly like `cat`'s:

```bash
claude -p "Draft a subject line for this email" | pbcopy
```

`pbcopy` is the Mac's own clipboard command; whatever reaches it is
sitting on your clipboard the moment the prompt returns. Or send it to a
file instead, with `>` rather than `|`:

```bash
claude -p "Summarise this bundle" > summary.txt
```

## Why this waited

A chat has nothing to pipe. Its answer sits inside a window, meant for
you to read, not for the next command to consume. A headless session's
answer is a single block of text with nothing before or after it — which
is exactly what a pipe needs on either side of it. That is the property
*What a headless session is* set up, and this is what it was for.

Piping tells you what went in and what came out. It says nothing about
what happened while it ran. Next, watching that.

Press `n`.
