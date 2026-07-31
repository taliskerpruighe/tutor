---
id: ai/model-differences
title: What makes one model different from another
part: Agentic AI
section: LLMs
order: 2
summary: Size, architecture and speciality are the three axes, and only one of them is the number everyone quotes
keywords: [parameters, size, mixture of experts, dense model, speciality, fine-tuning, price, speed]
---

# What makes one model different from another

*v0.2.0*

Every model is the same shape. What varies is size, how it is built
inside that shape, and what it was tuned to be good at. Three axes,
and the first is the one that gets quoted and tells you the least.

## Size

A model's **parameters** are the billions of internal numbers it
adjusted while learning to predict text. A parameter count is quoted
the way horsepower is quoted for a car — a real number, and not the
whole story. A larger model has more room to have learned something
subtle. It does not follow that it did, and training a large model
badly beats training a small one well every time it is tried.

Treat the number as a rough size class, not a scoreboard. Two models
can be quoted at roughly the same size and behave nothing alike, for
reasons that have nothing to do with size at all.

## Dense or mixture-of-experts

A **dense** model uses every one of its parameters on every question
you put to it. That is expensive and slow in direct proportion to how
big the model is.

A **mixture-of-experts** model — **MoE** — is built from many smaller
sub-networks, with a router that picks a handful of them for any given
question. Most of the model sits idle on any one answer. That is
cheaper to run and faster to answer from, for a model of the same
overall size.

The distinction rarely shows up in the answer itself. It shows up in
what you pay for it and how long you wait — a mixture-of-experts model
competing with a dense one of similar size is usually the cheaper,
quicker of the two, not the better one.

## Speciality

Beyond size and architecture, a model is **tuned** — trained further,
after the general reading, on a narrower diet chosen to make it good
at something specific. One tuned hard on code writes better code and
worse poetry than one tuned on neither. One tuned for cautious,
hedged answers refuses more than one tuned for a research lab's own
internal use.

None of that is visible from the parameter count. Two models the same
size, built the same way, can behave entirely differently because of
what they were shown last. A model tuned on customer-support chat logs
and one tuned on legal drafting will hand back different sentences to
the identical question, without either one being wrong.

Put those three together — size, architecture, and what a model was
tuned for — and you can place any model you are handed. Here is the
actual list of them.

Press `n`.
