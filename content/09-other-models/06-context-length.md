---
id: other-models/context-length
title: Context length
level: Level 2
part: Other Models
section: Ollama
order: 6
summary: Ollama's default context window is a fraction of Claude's, and it runs out before the first prompt arrives
keywords: [context length, context window, ollama, OLLAMA_CONTEXT_LENGTH, ollama ps, vram, gpu, cpu, tokens, cloud]
---

# Context length

*v0.2.10*

A model can only hold so much in its head at once. Everything a
session touches — its own instructions, every file it opens, every
line you type — goes into that fixed amount of room. What that room
is called, and what happens as it fills, is a subject the course
comes back to.

Here it just has a number, and the number is what breaks things.
Ollama sizes its default to whatever VRAM is on the machine:

```
  < 24 GiB VRAM     4,000 tokens
  24-48 GiB VRAM   32,000 tokens
  >= 48 GiB VRAM  256,000 tokens
```

A small machine gets the top row. The Claude models already met carry
200,000 at the low end and 1,000,000 at the high end. Four thousand
against either is not a difference of degree.

## Already spoken for

A session is not empty before you type. Its own instructions and the
definition of every tool it can call are already sitting in the room
before your first prompt reaches the model — none of that is
Ollama-specific, it just usually goes unnoticed because the room is
large enough to absorb it without anyone counting.

At 4,000 tokens the room is not large enough. Those instructions and
tool definitions alone can exhaust the window before you have typed
anything, which makes this the likeliest reason a correctly
configured setup looks broken.

## Raising it

Agents and coding tools want more room, not less. Ollama's own
documentation puts the floor at 64,000 tokens for exactly that class
of work, and raising it is set where the daemon starts, not where the
model runs:

```
OLLAMA_CONTEXT_LENGTH=64000 ollama serve
```

## What actually got allocated

Setting the variable is not the same as confirming it took. `ollama
ps` lists the `CONTEXT` a running model was actually given, alongside
`PROCESSOR`, which shows whether the model fits on the GPU or has
been pushed onto the CPU because the context asked for did not fit in
the VRAM available:

```
NAME    SIZE     PROCESSOR    CONTEXT
qwen3   6.2 GB   100% GPU     64000
```

A `CONTEXT` figure lower than the one you set is the window shrinking
to fit the hardware, not a typo.

## The problem cloud models do not have

None of this touches a cloud model. Cloud models are set to their
maximum context length by default — there is no VRAM to size
against, so there is nothing to raise and nothing to check. Context
length is a local-model problem from top to bottom.

What fills that room besides instructions, and what happens to a
session as it fills, has its own part later in the course.

Press `n`.
