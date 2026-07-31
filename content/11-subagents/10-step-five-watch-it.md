---
id: subagents/step-five
title: Step five — watch it
part: Subagents
section: Build a Chain
order: 10
summary: Read a chain while it runs, fix it in the skill that got it wrong, and the chain is yours.
keywords: [exercise, watch, debug, legible, fix, iterate, corrections, party tricks, chain, workflows]
---

# Step five — watch it

*v0.1.0*

A chain is not a black box. Every step of it is on your screen while it
happens, and that is the whole reason you can fix one.

## Reading the chain

Four things to look at as it runs.

**Which agent, on which model.** Each spawn says what it is and what it
is running on. A `bundle-reader` on Sonnet means the model line in that
agent file is not what you think it is.

**How many spawned.** Three documents should give three readers. Two
means one document was not seen. Four means something was counted twice.
That number is the door's work, so a wrong number is the door's fault
and nobody else's.

**What each one returned.** Not just that it finished — what came back.
A reader returning three events for a document with nine dates in it has
gone wrong quietly, and it is the only place you can catch it, because
by the next stage it is one line in a merged list.

**What the last one was handed.** The consolidator's prompt should hold
every list, written out. If a list is missing there, the entry it would
have produced was never lost — it was never sent.

Read those four and you can always say which of the five parts was
wrong. That is what legible means, and it is worth more than any of it
working first time.

## Fixing it

When a run comes back wrong, there is one rule, and it is the same rule
as everywhere else in this course.

**The fix goes in the skill that got it wrong. Never by hand.**

Correcting the output in front of you feels like the fast way, and it
leaves the next run exactly as broken as this one. You will correct it
again on Thursday. The skill is the only thing that carries forward.

So work out which part failed, from the four things above, then go and
patch that one — `bundle` if the wrong documents were picked up,
`bundle-read` if a reader missed dates, `bundle-consolidate` if the
merge lost or muddled them.

Patch it the way *Iterate with corrections* taught you. Two things,
together:

1. **Say what went wrong**, plainly. *"It listed the date of the letter
   but not the two dates in the second paragraph."*
2. **Show it the right answer.** The actual entries it should have
   produced for that document, written out as they should look.

Then ask it to patch the skill. From the wrong output and the right one
side by side it can work out what the rule actually was — which is
something no amount of explaining the rule tends to achieve.

Two or three rounds is normal. After that the chain is yours, and it
will still be right in March.

---

That is Subagents, and with it everything you can build while sitting in
front of a conversation. You started at a black window with a blinking
cursor. You now have the six Party Tricks, and — more to the point — you
can build. An agent, with the right model on it. A skill, in your own
words, from your own examples, that fires when you type a slash. And a
chain: several of both, in an order you chose, doing a whole job while
you read something else.

None of that was the hard part, in the end. The hard part was knowing
which of them a job wants, and you have now built one of each and seen
where the seams are.

Workflows are next, and they take the driving seat out: the same
pipeline, written down as a script, run ten times over without you
sitting at any of them.

Press `n`.
