---
id: claude-code/what-it-is
title: What Claude Code is
part: Setup
section: How It Works
order: 1
summary: Claude is the model; Claude Code is the machinery that gives it hands.
keywords: [llm, model, harness, claude, agent, tools, loop]
---

# What Claude Code is

Two things with confusingly similar names.

**Claude** is the model. **Claude Code** is the program in your terminal
that puts the model to work. Almost everything that follows depends on
keeping those apart, so it is worth a few minutes.

## What a model is

A **large language model** — an LLM — is a very large mathematical function
with one job: given some text, produce what plausibly comes next.

That is the whole of it. Not a lookup. Not a search of the internet. It was
built by working through an enormous quantity of writing and adjusting
billions of internal numbers until its guesses about the next word got very
good. Learning to write well enough to be indistinguishable from a person
who understands the subject turns out, in practice, to require a great deal
of actual understanding along the way.

Now, the limitation that matters. A model, by itself, cannot *do* anything.
It reads text and it writes text. It has no way to see a file on your disk,
no way to run a command, no way to remember what you told it yesterday. It
receives a stretch of writing, returns a plausible continuation, and stops.

An LLM on its own is a brain in a jar. Fluent, well-read, and unable to
reach anything.

## What a harness is

A **harness** is the program that gives it hands.

The name is agricultural. A horse can pull; a harness is what connects the
pulling to a cart. The animal is unchanged — it is simply now attached to
something.

Here is what the harness does, in a loop:

1. You type a request.
2. It gathers context — your request, the conversation so far, the
   contents of relevant files — and sends the lot to the model.
3. The model replies. Sometimes the reply is prose for you. Sometimes it
   is a request: *read this file*, *run this command*, *search for that*.
4. When it is a request, the harness **carries it out** and sends the
   result back to the model.
5. Round again, until the model has nothing left to ask for.

Step 4 is the entire trick. The model never touched your disk. It asked,
and a plain ordinary program did the work and reported back. Every
impressive thing you will see happen in this terminal is that loop, turning
fast.

## So, Claude Code

Claude Code is that harness, running on your Mac.

It owns the loop. It decides what the model gets to see and what it is
allowed to touch. It reads and writes files, runs commands, searches your
project, and asks your permission before anything consequential. Then it
hands the results back to the model and goes round again.

| | What it is | Where it runs |
|---|---|---|
| Claude | the model | Anthropic's data centres |
| Claude Code | the harness | your Mac |

The next article is about why it is split that way.

Press `n`.
