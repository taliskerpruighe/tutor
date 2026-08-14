---
id: prompt/dos-and-donts
title: Prompt dos and donts
level: Level 2
part: Agents
section: Prompts
order: 10
summary: A quality target gives an agent nothing to check its own work against; an objective does.
keywords: [prompt, objective, instruction, quality target, milestone, benchmark, dos and donts, skill, the boss]
---

# Prompt dos and donts

*v0.2.9*

A prompt is not an instruction. It is a description of what finished
looks like, and most of what goes wrong in a session traces back to a
prompt that skipped that step.

The commonest failure is the **quality target**: a sentence that names
the outcome you want without saying how the agent would know it got
there. "Fix the code." "Make this sound like me." Neither is false,
exactly. Neither is usable either — not without a battle-tested skill
sitting behind it, which is a later problem.

This one is short.

## The bad version

"Fix the code" gives the agent a direction and no distance. It stops
when its own judgement says the code looks fixed, which is not the
same moment your judgement would have stopped at. "Make this sound
like me" fails the same way: sound like you, according to what
standard, checked against what?

Neither sentence is wrong to say out loud to a colleague, who shares
your assumptions without being told them and fills the gaps from
experience. An agent does not have your assumptions, and it does not
fill gaps quietly and correctly — it fills them quietly and however
its training suggests. It has the sentence, and nothing behind it.

## The good version

An **objective** is the same request with a finish line attached — a
milestone or benchmark the agent can test its own work against, rather
than a mood it has to guess at.

> *"Fix the code until you see the columns align when the window
> opens."*

> *"Make this sound like me until another agent cannot tell the
> difference from this sample."*

Each one names a check that runs without you in the room. The columns
either align or they do not. Another agent is either fooled or it is
not. Writing it this way costs nothing extra — it is the same
sentence, aimed rather than gestured.

Nobody arrives at this by instinct. Giving objectives instead of
instructions, and giving them in pieces rather than all at once, is a
habit the Boss built by watching plausible, wrong answers come back
from sentences that sounded perfectly clear at the time.

## The best version

An objective alone still leaves the agent guessing at everything
around the task — why it matters, what to avoid, what already failed
last time. Tell it the letter is a chaser on an unanswered LBA, not a
first approach, and tell it not to soften the deadline paragraph, and
the same objective stops needing a second look before it goes out.
That is context and a trap either side of it, and the full shape adds
both as standing pieces rather than afterthoughts bolted on when the
first draft comes back wrong.

## Why the gradient matters

Bad, good and best are not three separate techniques to pick between
on a whim. Each one sits strictly above the last: an objective already
contains everything a quality target had, and the full shape already
contains everything the objective had. Nothing is thrown away moving
up the gradient, and nothing here works moving down it.

Press `n`.
