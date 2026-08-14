---
id: claude/the-harnesses
title: The harnesses
level: Level 2
part: Claude
section: The Claude Code Harness
order: 2
summary: Three ways to reach Claude — a website, a sandboxed website, and a terminal program on your own machine
keywords: [claude.ai, claude cowork, claude code, harness, website, terminal, sandbox, agent]
---

# The harnesses

*v0.2.0*

*Why Claude Code* settled which harness this course teaches, and it
settled it on one fact: the machine doing the work is yours. Anthropic
ships two more harnesses under the same name, Claude, and neither one
stands where Claude Code does.

**claude.ai** is a website — open it, type, read what comes back.
**Claude Cowork** is a website too, but a different shape of one: it
reads files, writes files and runs commands, the same actions Claude
Code takes. What differs, in both cases, is where.

Two comparisons, then, each run against the harness already met.

## claude.ai gives you an answer, not an action

claude.ai can take a document attached to a question, but that is the
limit of it: no persistent access to your files, no way to run a
command of its own. It answers. Claude Code already stands inside the
folder you are working from, so nothing needs attaching — it reads
what is there directly, and can write back to the same place.

## Cowork acts, on a machine that is not yours

Cowork's actions are the same shape as Claude Code's: read a file,
write a file, run a command. That puts it closer to Claude Code than
claude.ai ever gets. What stays different is whose machine carries
them out. Cowork opens each job inside a sandboxed virtual machine
that Anthropic builds and tears down afterwards, with a fixed slice of
hardware behind it and no view of the folder you actually work in
unless you send a copy across the network first. Claude Code needs no
copy sent. It is already standing inside that folder, on hardware
that is yours.

## One variable, not three products

Three harnesses, one axis: whose machine it runs on. That single fact
decides what each one can reach — your files directly, a copy of
them, or nothing beyond what you paste into a box. Nothing about the
three is a difference in features grafted on afterwards. It is a
difference in where the loop happens, and everything else follows
from that.

Press `n`.
