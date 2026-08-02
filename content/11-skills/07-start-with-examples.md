---
id: skills/start-with-examples
title: Start with examples
level: Level 2
part: Skills
section: Building One
order: 7
summary: Party Trick #4 — build a skill from your own worked examples, and give it the inputs as well as the outputs.
keywords: [party trick, skill engineering, examples, inputs, outputs, transformation, precedent, assets]
---

# Start with examples

*v0.1.0*

> **Party Trick #4 from the Boss: skill engineering.** Do not write the
> instructions you want in the skill. Hand Claude examples of the work and
> let it write the instructions from those.

The instinct is to explain. Resist it. Throw the files at it instead and
say, in as many words, *"I want it done like that."*

## What a set looks like

Say you are teaching it to write a motion. The useful thing to hand over
is not the motion. It is the whole passage from raw material to filed
document:

```
motion-01/
├── rules.md      what the court requires
├── facts.md      the file as it stood
├── draft-01.md   the first pass
└── filed.md      what actually went in
```

Four files, and between them they carry everything you would have tried to
put into words. The rules explain the shape. The facts explain what was
available. The draft and the filed version, side by side, show what you do
to your own writing before it leaves the building — which is the part
nobody can articulate and everybody can demonstrate.

A letter before action is the same shape:

```
lba-01/
├── instructions.md  what the client told us
├── file-note.md     what we made of it
├── precedent.md     the letter we started from
└── sent.md          the letter as it went out
```

A chronology works the same way — the bundle went in, the chronology came
out, and the choices about what was worth a line are visible in the pair.

**Give it several matched sets if you have them.** One set teaches it your
format. Three teach it your judgement — what you do differently when the
facts are thin, when the other side has already written, when the deadline
is tomorrow.

## Inputs and outputs, not just outputs

This is the part that goes wrong, and it goes wrong quietly.

The easy thing to hand over is finished work product. It is polished, you
are proud of it, and it is sitting in a folder already. So you give it ten
filed motions and nothing else.

What it learns from ten filed motions is what a filed motion looks like.
Ask it to write one and it will produce something that looks exactly right
and says nothing true — because it has never once seen the material a
motion is made out of, and it has no idea which parts of yours came from
the facts and which are just how motions read.

Give it the inputs too and it learns something else entirely: **the
transformation.** This went in, that came out, and here is what happened in
between. That is a skill. The other is a stencil.

The test is simple. For every finished document you hand over, ask yourself
what you had on your desk before you wrote it — and hand that over as well.

Press `n`.
