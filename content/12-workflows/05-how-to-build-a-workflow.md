---
id: workflows/how-to-build
title: How to build a workflow
level: Level 2
part: Workflows
section: Building One
order: 5
summary: Ask the main agent for a workflow the same way you ask for a chain, on the effort level built for it
keywords: [workflow, ultracode, effort, main agent, ask, chain, script]
---

# How to build a workflow

*v0.2.0*

Do not attempt to write a workflow by hand. It is a script wired
through the same machinery as an agent or a skill, and the reliable way
to get one right is the way every other asset in this course got built:
ask.

## The ask itself

You already know the shape of this from *Designing a chain*. Describe
the pipeline to your main agent in the same terms — what goes in, what
stages it passes through, what comes out — and let it work out the
agents, the models and the script that drives them.

> *"Build me a workflow that reads a book, summarises it, and reviews
> the summary against the text. I want to run it against ten books,
> and I do not want to babysit any of it."*

That last clause is not filler. It is what tells the main agent it is
building a workflow rather than a chain: something that runs the
pipeline itself, ten times, with nobody at the keyboard between runs.

## The effort level built for this

The main agent has an effort level of its own, separate from the ones a
skill carries, called **ultracode**, meant specifically for writing and
managing workflows. Set it before you ask:

```
/effort
```

pick `ultracode` from the list, and then make the ask above. Writing a
script that spawns agents correctly, in the right order, with the right
prompts baked in, is exactly the kind of work that effort level exists
to slow down and get right.

Leave it at the default and you can still get a working workflow back —
the difference shows up later, in how much of it you end up rebuilding
once you have read it properly. A script gets one honest shot at being
correct before it is running unattended against ten books; that is
worth the slower answer.

## What comes back

The main agent designs the pipeline, writes the script, and tells you
where it put it — inside `.claude`, next to the agents and skills it is
built out of, the way *What a workflow is* already told you to expect.
From there it is a file like any other: yours to read, yours to hand
back with a correction, and yours to run.

Getting the first version right is one round of this. Getting it lean
is the next one, and that is not the same conversation.

Press `n`.
