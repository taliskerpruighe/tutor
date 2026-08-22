---
id: challenges/one
title: Challenge one
level: Level 2
part: Challenges
order: 1
summary: A law firm wants a plugin that turns a folder of client documents into a finished naturalization packet, on one command
keywords: [challenge, plugin, naturalization, packet, n-400, command, agents, skills, workflows, examples]
---

# Challenge one

*v0.2.13*

A law firm does naturalization work, and it would like to challenge you.

It wants a plugin it can run on its Claude Code harness to do entire
naturalization packets for it.

## What the firm has given you

A few examples. Each example is one past client, and each client comes with
two things: the **input**, which is what the client gave the firm, and the
**output**, which is the naturalization packet the firm made for that client.

You will notice that the input always looks different. It changes with the
client. An email saying *"my name is such and such, my date of birth is such
and such"*. A spreadsheet the client filled in with the same information. A
tax return.

The output does not look different. It has a rhyme and a reason to it, and
that is the way the firm likes its naturalization packets done. Cover pages
for the tabs and the documents. A table of contents. The documents in a
particular order — the N-400 application form first, then a handful of others
attaching the client's own documents. All of it merged into one PDF.

The firm is also providing a few more client input folders with no output
folder. Those packets still need to be built, and they are there for you to
test and prove your plugin on.

## What the firm would like the plugin to do

- **Run on a Claude Code harness.** The plugin can run on your computer. The
  firm would be all the more impressed if the plugin could be shared with
  them and they could run it on theirs.
- **Turn an input folder into an output folder.** Take the input from any
  given client and turn it into an output as close as possible to what you
  see in the examples the firm provided — the same format, the same
  organisation, the same type of content, down to the merged PDF and the
  font.
- **Work as simply as possible.** One single command on a terminal, with one
  single argument, and that argument is the client folder to be made into a
  naturalization packet. The firm will be all the more impressed if you can
  make that command be the word `naturalize`, followed by the path on the
  given computer to the client's input folder in question.

## Feel free to cheat

The firm would like you to use just the topics covered in Levels 1 and 2 of
this course. Beyond that, feel free. Work smart and not hard: point an agent
running in Claude Code at this challenge, at the rest of the course and at
the materials provided, and it should be able to take you a long way.

Press `n`.
