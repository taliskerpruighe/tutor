---
id: agents/managing
title: Managing context
level: Level 2
part: Agents
section: Context
order: 4
summary: The three resets — compact, clear, exit — and how to pick between them.
keywords: [compact, clear, exit, reset, party trick, auto-compact, context management, slash command]
---

# Managing context

*v0.1.0*

Two things are true and neither is negotiable.

**An agent will not manage its own context.** It cannot see the problem
from the inside; the faculty that would notice is the faculty that is
degrading.

**The harness barely helps.** Claude Code will auto-compact a conversation
when you run out — at **80%**.

```
  ████████████████░░░░  80%  auto-compact fires
  ██████████░░░░░░░░░░  50%  it was already unusable here
```

By the time the safety net catches you, you have been getting bad work for
half the conversation. Treat auto-compact as evidence you made a mistake,
not as a feature.

So the job is yours. It is three keystrokes.

> **Party Trick #2 from the Boss: the three resets.**

## Which one

| Reset | Conversation | Folder | Use when |
|---|---|---|---|
| `/compact` | summarised | same | step 4 needs step 1 |
| `/clear` | gone | same | new task, same matter |
| `/exit` | gone | new | different matter |

Two questions get you the right one. *Do I need what was said earlier?*
If yes, `/compact`. If no — *am I staying in this folder?* Stay, `/clear`.
Leave, `/exit`.

## `/compact` — when the thread matters

You are drafting a settlement agreement clause by clause. The definitions
in clause 1 bind clause 4. The indemnity has to sit against the cap. The
agent must still know what it wrote an hour ago.

```
  clause 1  definitions ──┐
  clause 2  payment    ───┤
  clause 3  cap        ───┼── all still binding
  clause 4  indemnity  ───┘

  four clauses in   ██████████████░░░░░░  70%
        │
        │  /compact
        ▼
  thread kept       ████░░░░░░░░░░░░░░░░  20%
```

`/compact` replaces the transcript with a summary of itself. The thread
survives; the bulk does not. Everything the agent needs stays, and the
forty pages it read to get there go.

Use it in any run of work where step four depends on step one — a long
document in parts, a chain of research, a negotiation you are tracking.

## `/clear` — when the thread does not

Bundle review, finished. Sixty documents read, a list of the relevant ones
in your hand. Next job is drafting the memo, in the same matter folder.

```
  bundle review   ██████████░░░░░░░░░░  50%   done with
        │
        │  /clear
        ▼
  draft the memo  ██░░░░░░░░░░░░░░░░░░   0%   same folder
```

Nothing from the review needs to be in the agent's head — you have the
list. `/clear` throws the whole conversation away and leaves you exactly
where you were: same folder, same rules, same skills, fresh agent.

This is the one people underuse. New task, `/clear` first. It costs
nothing.

## `/exit` — when the folder changes

Mackenzie is put to bed. You are picking up Okonjo, which lives somewhere
else.

```
  ~/work/mackenzie   ████████████░░░░░░░░  60%
        │
        │  /exit
        ▼
  cd ~/work/okonjo && claude          ██░░░░░░░░░░░░░░░░░░
```

`/clear` would have kept you in the wrong folder — and by the walk-up
rule, the wrong folder means the wrong rules, the wrong skills, the wrong
agents on the path. Moving is the point. `/exit` and start again where the
work is.

## The habit

Watch the number. When it climbs, ask the two questions and hit one of the
three. You will do this a dozen times a day and it will stop feeling like
a decision.

Everything else in this course assumes an agent that is actually paying
attention. This is how you get one.

Press `n`.
