---
id: claude/the-harnesses
title: The harnesses
level: Level 2
part: Claude
section: Claude
order: 2
summary: Three ways to reach Claude — a website, a sandboxed website, and a terminal program on your own machine
keywords: [claude.ai, claude cowork, claude code, harness, website, terminal, sandbox, agent]
---

# The harnesses

*v0.2.0*

A model on its own does nothing — the brain in a jar of *What an LLM is*.
Anthropic ships three different bodies for it, all called some
variant of Claude, and telling them apart matters before anything
else in this part does.

**claude.ai** is a website. You open it in a browser, type, and read
what comes back. It can attach a document to a question, but it has
no persistent access to your files and no way to run a command — a
conversation, not an agent.

**Claude Cowork** is also a website, and it goes further: it can read
files, write files and run commands, the way the rest of this course
describes an agent doing. The difference is where that happens. The
machine doing the work is not yours. Cowork runs each job inside a
sandboxed virtual machine that Anthropic provides, with a fixed slice
of hardware behind it.

**Claude Code** is neither. It is a program you install on your own
Mac and run from the terminal, and the work it does happens there —
your files, your disk, your hardware.

## Why the difference is not cosmetic

Cowork and Claude Code both do the same kind of thing: read, write,
run commands, report back. What separates them is where the machine
sits and, following from that, whose files and whose hardware it
reaches. A sandbox never sees the folder you are actually working in
unless you send a copy into it. A terminal program already stands
inside that folder.

That single fact — local machine against someone else's — is going to
do more work than it looks like it can. It decides what software each
one can reach, how fast each one runs, and how much of what happens
you can actually watch happen. All three follow from the same cause,
and the rest of this part works through them one at a time.

## The one this course teaches

Claude Code, throughout. Not because the others do nothing worth
having — Cowork is a reasonable choice for a job you want running
without your laptop open — but because a terminal on your own machine
is the version with the fewest walls around it, and the fewest walls
is where the rest of this course lives.

Before any of that, the plain economics: what each of these actually
costs to use, and which tier gets you the model this course keeps
recommending.

Press `n`.
