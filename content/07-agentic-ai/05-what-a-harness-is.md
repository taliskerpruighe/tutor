---
id: ai/what-a-harness-is
title: What a harness is
level: Level 1
part: Agentic AI
section: Harnesses
order: 5
summary: The model is the brain; a harness is the body that gives it hands
keywords: [harness, loop, model, llm, tool, permission, agent, claude code]
---

# What a harness is

*v0.2.0*

An LLM is a brain in a jar — fluent, well-read, and unable to reach
anything. A **harness** is the body it gets attached to.

The name is agricultural. A horse can pull; a harness is what connects
the pulling to a cart. The animal is unchanged — it is simply now
attached to something. The model is unchanged too. Nothing about a
harness makes it smarter. It makes it able to do anything at all.

## The loop

A harness runs one loop, over and over, for as long as the conversation
lasts:

1. You type a request.
2. It gathers context — your request, the conversation so far, the
   contents of relevant files — and sends the lot to the model.
3. The model replies. Sometimes the reply is prose, for you. Sometimes
   it is a request: *read this file*, *run this command*, *search for
   that*.
4. When it is a request, the harness **carries it out** and sends the
   result back to the model.
5. Round again, until the model has nothing left to ask for.

Step 4 is the entire trick. The model never touched your disk. It
asked, and a plain ordinary program did the work and reported back.
Every impressive thing an agent does in a terminal is that loop,
turning fast.

## What the harness owns

The model only ever sees text and only ever produces text. Everything
either side of that — deciding what the model gets to see, deciding
what it is allowed to touch, actually reading the file or running the
command — is the harness's job, not the model's.

That division is why permission sits where it does. When something
consequential is about to happen, it is the harness that stops and
asks, because the harness is the only one of the two with hands to
stop.

A harness with no model behind it is inert — a body with nothing
directing it. A model with no harness is a brain in a jar. Neither does
anything on its own; the pairing is the whole of what an agent is.

## One word, doing a lot of work

Everything this course has shown you so far — a session answering a
question, a skill firing, an agent reading a file and reporting back —
has been this loop, dressed differently each time. The vocabulary
changes: a request becomes a prompt, a reply becomes an answer, a tool
call becomes *the agent read the file*. Underneath, it is steps one
through five, running once more.

That is worth having a name for, because the next article is about to
show you that this course only ever described one of them.

The next article is what happens once you notice that more than one
harness exists.

Press `n`.
