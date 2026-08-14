---
id: ai/what-an-llm-is
title: What an LLM is
level: Level 1
part: Agentic AI
section: LLMs
order: 1
summary: A model is a mathematical function that guesses the next word, and that turns out to be enough and not enough
keywords: [llm, model, large language model, token, prediction, brain in a jar, training, weights]
---

# What an LLM is

*v0.2.0*

A **large language model** — an **LLM** — is a very large mathematical
function with one job: given some text, produce what plausibly comes
next.

That is the whole of it. Not a lookup. Not a search of the internet. It
was built by working through an enormous quantity of writing and
adjusting billions of internal numbers until its guesses about the next
word got very good. Learning to write well enough to be indistinguishable
from a person who understands the subject turns out, in practice, to
require a great deal of actual understanding along the way.

## Guessing, done well enough to matter

Ask it to continue *"Dear Sirs, we write further to your letter of"* and
it does not retrieve a template from anywhere. It calculates, word by
word, what a solicitor's letter plausibly says next, drawing on the
shape of every such letter it absorbed while it was being built. Do that
convincingly enough, across enough kinds of writing, and the result
reads as understanding — because producing text a lawyer would recognise
as competent turns out, in practice, to need something close to it.

Ask it something outside anything it was ever shown, and the same
mechanism runs anyway. It still produces the most plausible next word.
Plausible and correct are not the same claim, and the model has no way
to tell you which one it just gave you. It will state a made-up case
citation with exactly the same confidence as a real one, because
confidence was never part of what it is calculating.

## What it cannot do

Now the limitation that matters. A model, by itself, cannot *do*
anything. It reads text and it writes text. It has no way to see a file
on your disk, no way to run a command, no way to remember what you told
it yesterday. It receives a stretch of writing, returns a plausible
continuation, and stops.

An LLM on its own is a brain in a jar. Fluent, well-read, and unable to
reach anything. It cannot open the bundle you are asking about. It
cannot check whether the case it just cited exists, or save the letter
it just drafted. Whatever it is that lets an agent do those things, it
is not the model — the model is only ever the half that thinks.

## Same shape, every time

Every LLM — the one you are about to meet, and every rival to it — is
built this same way: a function trained on text, guessing the next
piece of it, with no hands of its own. Nothing about that changes from
one to the next. What differs is the choices made while building the
function, and how good its guesses turn out to be.

Press `n`.
