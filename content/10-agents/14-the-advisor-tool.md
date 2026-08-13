---
id: prompt/the-advisor-tool
title: The advisor tool
level: Level 2
part: Agents
section: Prompts
order: 14
summary: A second model reads the whole transcript and says whether the first one is about to get it wrong, at a cost that is not always worth paying.
keywords: [advisor, advisormodel, opus, review, second opinion, settings.json, dual edged, the boss]
---

# The advisor tool

*v0.2.9*

The **advisor** tool hands your entire transcript — every message, every
file it opened, every command it ran — to a second model and asks it to
judge the work before it goes any further. Not a spell-check. A
colleague reading over the shoulder of the one doing the drafting.

Which model reads over that shoulder is a setting, and which model does
the drafting stays whatever it already was.

## The setting

`advisorModel` in `settings.json` names the reviewer:

```json
{
  "advisorModel": "opus"
}
```

Set it to Opus — the Boss's standing recommendation, on the reasoning
that a reviewer no stronger than the model it is checking will only
agree with the mistakes it was meant to catch.

## What it is good for

Called before the agent commits to an interpretation, or before it
declares a piece of work finished, the advisor catches exactly the
errors that are invisible from inside the task: an assumption nobody
checked, a document skimmed rather than read, a fix that solved the
symptom named rather than the fault underneath it. An agent halfway
through a chronology, about to declare the limitation date settled, is
exactly the moment a second reader earns its keep — it sees the whole
transcript, including the paragraph the first agent skimmed past
three exchanges ago and never returned to. Course correction before
delivery, not after — and never a substitute for reading the result
yourself once it lands.

## The other edge

> **From the Boss:** *"It is a dual-edged sword. It genuinely stops
> agents handing you something terrible — and then it turns around and
> calls itself for reviewing a basic file search, which was never in
> any doubt, and you are paying for both runs."*

The advisor is slow and it is not cheap: a full second reading of
everything so far, on a model chosen for strength rather than speed.
An agent left to decide for itself when to call it will call it too
often, on work that carried no real risk of being wrong.

## Where it is worth it

Reserve it for the judgement calls — the moment before an
interpretation hardens into an approach, the moment before a finished
piece of work is handed back. Not for confirming that a search found
what a search was always going to find.

You will not always be the one deciding. An agent working alone often
makes the call itself, mid-task, without asking first — which is
exactly why the setting matters more than the habit. You cannot stop
an agent reaching for the advisor too often, but you can make sure
that, when it does, the reviewer it reaches is one worth the cost.

This section has been about shaping what you say to an agent. Next,
the subject turns to the agent itself, starting with the one you have
been talking to the whole time without ever naming it — *The default
agent*.

Press `n`.
