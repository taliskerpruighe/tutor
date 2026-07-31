---
id: headless/what-it-is
title: What a headless session is
part: Headless Sessions
section: Running Without a Chat
order: 1
summary: Type claude -p and a prompt on the same line, and Claude Code answers once and hands the shell straight back
keywords: [headless, print, -p, --print, non-interactive, script, prompt, output, shell, scripting]
---

# What a headless session is

*v0.2.0*

Every session so far has opened the same way. Type `claude`, and it opens
a chat, waits for you to say something, and keeps waiting after you do.
A **headless session** is Claude Code with that waiting removed.

Add `-p`, or written out in full, `--print`, and the prompt itself, all
on one line:

```bash
claude -p "List every dated event in engagement.md"
```

Press return and it works exactly as it would in a chat — reading the
file, thinking, drafting an answer — and then it prints that answer to
your terminal and exits. No chat window opens. There is nothing to
close afterwards, because nothing stayed open.

## Non-interactive means what it says

An ordinary session is a conversation: you can correct it, ask it to go
further, hand it a second file once you have read the first answer. A
headless one gets one prompt and gives one answer. It cannot ask you a
clarifying question, and if it needs one, it guesses rather than waits —
there is no chat for the question to arrive in.

That is not a smaller version of Claude Code. It is the same agent,
reading the same files, capable of the same work. The only thing removed
is the loop.

## What comes back

Only the outcome. Not a transcript, not the thinking that produced it —
the answer, and nothing before or after it. Point it at a shell prompt
and that is exactly what lands there: the three sentences you asked for,
the list, the draft, printed and done.

That is the property the rest of this part is built on. A result that
prints once and stops is a result something else can pick up — a file, a
script, another command — which a chat's back-and-forth never was.

The next article is which jobs actually want that.

Press `n`.
