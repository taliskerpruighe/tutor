---
id: claude/the-models
title: The models
level: Level 1
part: Claude
section: Claude
order: 1
summary: Four Claude models exist, and choosing between them is a trade-off between speed and depth, not a favourite
keywords: [claude, model, haiku, sonnet, opus, fable, speed, cost, parameter, size]
---

# The models

*v0.2.0*

**Claude** is not one model. It is a family of four, named Haiku,
Sonnet, Opus and Fable, and the family exists because no single size
is right for every question.

A model's size is measured in **parameters** — the billions of
internal numbers it was trained by adjusting. Anthropic does not
publish the counts, and anyone quoting an exact figure is guessing.
What is known, and what matters, is the order: Haiku is the smallest
and fastest, Sonnet sits in the middle, and Opus and Fable are the
largest and slowest of the four.

## Haiku

The cheapest and quickest model in the family, and the one built for
volume rather than depth. It answers a well-defined question fast:
classify this document, extract these five fields, summarise this
email. Asked something that needs real reasoning across a pile of
unfamiliar material, it will still answer — the guess is simply weaker.

## Sonnet

The default. This is the model most of your work runs on, and the one
the rest of this course assumes unless it says otherwise. It reasons
well, reads and writes at length, and does it fast enough that waiting
for it is rarely the bottleneck. Most solicitors will spend most of
their time here.

## Opus and Fable

The two largest models, kept for the questions Sonnet gets visibly
wrong: a contract with clauses that interact in unexpected ways, a
chronology built from a bundle that contradicts itself, a piece of
reasoning with several steps where one wrong turn early on ruins
everything after it. Fable is the newer of the two and the more
capable; both are slower than Sonnet and cost more to run.

Reach for either when the job is hard rather than long. A long,
straightforward job is still Sonnet's — more text is not the same
problem as harder text.

## What decides the choice

| Model | Reach for it when |
|---|---|
| Haiku | the question is simple and there are many of them |
| Sonnet | most days, most matters |
| Opus | the reasoning is the hard part |
| Fable | the reasoning is the hard part and it matters most |

There is a second number attached to every model — how much it can
hold in view at once, called its **context window**. That number
belongs to a later article, once you have met the idea of a session
filling up as it goes. For now, size and purpose are enough to choose
by.

None of these four does anything on its own. A model only ever reads
text and writes text back — what turns that into a program that reads
your files and runs your commands is a separate piece, and it is
what the next article names.

Press `n`.
