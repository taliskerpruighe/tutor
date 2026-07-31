---
id: ai/the-harnesses-there-are
title: The harnesses there are
part: Agentic AI
section: Harnesses
order: 6
summary: Claude Code is one harness among a growing field of them, sorted by where they live
keywords: [harness, claude code, antigravity, qwen code, kimi code, opencode, cli, tui, gui, online]
---

# The harnesses there are

*v0.2.0*

The last article defined **harness** and then named exactly one. That
was not the whole picture — it was the one this course teaches. Here is
what else answers to the word.

Every harness runs the same loop: gather context, send it to a model,
carry out what comes back. What differs is where it lives and what it
looks like while it works.

## Online

A harness running on somebody else's server, reached through a browser.
You type into a page; the loop happens on a machine you never see. No
install, no terminal, and no visibility into what it did along the way
— a limitation the next part of this course returns to.

Convenient for exactly that reason: nothing to set up, nothing to
learn about your own machine first. The cost is everything you cannot
see. A step you did not ask for, a file it never mentions touching —
none of that is a fault peculiar to one product. It is what happens
everywhere the loop runs somewhere else.

## Desktop and GUI

A harness running as an ordinary application, with windows, panels and
a mouse. **Antigravity**, Google's entry, is one of these: an editor
with the loop built into it, so the agent's changes appear as coloured
diffs in the same window you are already looking at. Comfortable for
someone who wants the agent's work to look like the rest of the screen,
and closer to the terminal shape below than to the online one above —
it does sit on your machine, reading and writing real files.

## CLI and TUI

A harness running in a terminal, with nothing between you and the loop
but text. Alibaba's **qwen code**, Moonshot's **kimi code**, and the
open-source **opencode** all take this shape — each wired to a
different model or set of models, each running the same five-step loop
underneath. **Claude Code** is one of these, wired to Claude.

## Why it matters which one

The loop is identical everywhere. What changes is what the harness lets
you see, what it lets you reach, and how much of your own machine it is
willing to touch. An online harness cannot read your disk at all — there
is no disk to read. A desktop one reads the project open in its window.
A terminal one, run from the right folder, can reach anything a plain
command line could reach, which turns out to be most of what a working
day involves.

That is not a small difference dressed up as three flavours of the same
thing. Where the harness lives sets a hard ceiling on what it can ever
be asked to do, before a single word of the conversation happens.

The next article is what a harness of this shape actually needs from
the machine underneath it.

Press `n`.
