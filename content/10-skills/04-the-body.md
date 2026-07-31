---
id: skills/body
title: The body
part: Skills
section: When To Build One
order: 4
summary: Where the instructions go — and why you will not be writing them yourself.
keywords: [body, instructions, steps, skill writing, custom-skills, techniques, length, order]
---

# The body

*v0.1.0*

Everything after the closing `---` is the body. It is where the
instructions live: what the skill does, in what order, and what it
must not do.

There is no format. Prose, headings, lists, whatever fits the job —
written to the agent that will run it, in the second person, the way
*The definition file* had you brief a new paralegal.

Two things about it are worth knowing before anything else.

**It is read in order, and order is the point.** A skill that lists
things to bear in mind is much weaker than one that lists steps. How
you actually do the job — first this, then that, and check this before
sending — is the skill. The considerations are the part you already
had.

**It is paid for on every turn.** Once the skill fires, the whole body
sits in the context for the rest of that session. So it stays short:
under five hundred lines, and shorter than that if it can be. When it
runs long the answer is not tighter sentences, it is asking which part
belongs in a supporting file instead — the next article.

## You are not going to write it

Writing a good body is a course of its own, and a real one. Anthropic
and a good many data scientists have tested this exhaustively: what
phrasing survives, what an instruction has to contain to generalise
past the example, where a model stops reading, why a rule with its
reason attached holds up and a bare rule does not.

The Boss has packaged all of that into a skill of his own, called
`custom-skills`. It sits in this folder.

So the sequence is not *learn the techniques, then write the
instructions*. It is:

> *"Use the custom-skills skill to build me a skill."*

It interviews you, and then it writes the body — in the order you
described the job, with the reasons attached, at the length that
survives. You supply the knowledge. It supplies the shape.

The questions it asks are worth expecting. What the job is, and how
you do it today: that answer is usually the skill itself, because the
steps you take in order are the thing that has never been written
down. What you already have in writing: your style note, a precedent,
the checklist. And then the name, the effort level, and which folder
it belongs in.

None of those are questions about writing. They are questions about
your practice, which is the half of this that only you have.

That conversation is the whole of *Building your first skill*, a
little further on. For now the only thing to hold on to is that the
body is where
your way of working goes, and that getting it in there is a matter of
describing your job to something that already knows how to write it
down.

Press `n`.
