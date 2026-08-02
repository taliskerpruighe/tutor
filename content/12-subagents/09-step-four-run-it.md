---
id: subagents/step-four
title: Step four — run it
level: Level 2
part: Subagents
section: Build a Chain
order: 9
summary: One line, five parts, and a chronology out the other end — with a way to tell whether it is right.
keywords: [exercise, run, picker, slash, spawn, haiku, sonnet, chronology, checking]
---

# Step four — run it

*v0.1.0*

Start a fresh session, so nothing you have been doing is still in the
way:

```bash
cd ~/tutor/bundle && claude
```

On an empty prompt, type a single forward slash:

```
/
```

The list opens. Somewhere in it are three names you did not have an hour
ago — `bundle`, `bundle-read`, `bundle-consolidate` — sitting beside
`tutor`, `custom-agents` and `custom-skills`, which came with the
course. Six skills, three of them yours, all visible because this
session walks up through both folders.

Your two agents are **not** in that list, and should not be. Agents are
not invoked; they are spawned. The door does that.

## The one line

Pick `bundle` and tell it where to look:

```
/bundle the three documents in this folder
```

Send it, and watch.

## What you should see

In this order:

1. **The door names itself.** The reply opens by saying it has loaded
   `bundle`, then lists the three documents it found.
2. **Three spawns at once.** Three `bundle-reader` subagents appear
   together, not one after another, each running on **Haiku** and each
   handed one document.
3. **Three lists come back.** Each subagent finishes and returns its
   dated events. You may see them as they land.
4. **One more spawn.** A single `bundle-consolidator`, on **Sonnet**,
   with all three lists in its prompt.
5. **The chronology.** Dates in order, sources beside them, undated
   items at the end.

The models are worth watching for by name. Three cheap workers reading
in parallel and one better one making the judgement is the shape you
chose in step two, and here it is happening.

## How to tell it worked

A chronology appearing is not the test. A chronology can appear and be
invented.

Open the documents and check. Take three or four entries at random and
find the date in the document the entry names. It should be there, in
those words, saying that. Then look for something you know is in the
papers and check it made the list.

If the dates are real and the list is complete, the chain works. If an
entry cites a date that is not in the document it names, or a whole
document is missing from the output, that is the next article.

## The thing worth noticing

You typed one line.

Five things you built ran in order — a skill that spawned two kinds of
agent, each of which loaded a skill of its own, on two different models
at two different depths of thinking — and you touched none of them while
it happened. You did not tell the readers to start, or hand their output
to the consolidator, or decide when to stop.

That is the sixth Party Trick doing what it was advertised to do. And
`~/tutor/bundle` is a folder you made this morning.

One step left: how to read a chain while it is running, and what to do
on the day it comes back wrong.

Press `n`.
