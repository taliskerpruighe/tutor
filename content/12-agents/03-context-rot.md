---
id: agents/context-rot
title: Context rot
level: Level 2
part: Agents
section: Context
order: 3
summary: As the window fills the agent gets worse at everything, and it never tells you.
keywords: [context rot, hallucination, attention, degradation, silent, fifty percent, the boss]
---

# Context rot

*v0.1.0*

The famous problem with AI is **hallucination** — it states something
untrue with total confidence. Everyone knows this. Almost nobody knows
what causes it.

**Context rot.** As the window fills up, the agent's attention span goes.
It is holding more than it can properly attend to, so it starts skimming
its own memory instead of reading it. Hallucination is what that looks
like when it goes wrong loudly.

## The ladder

```
  ████░░░░░░░░░░░░░░░░  20%  sharp
  ████████░░░░░░░░░░░░  40%  noticeably worse
  ██████████░░░░░░░░░░  50%  borderline unusable
  ████████████████░░░░  80%  well past saving
```

Read that as a slope, not a cliff. There is no moment where it breaks.
An agent at 40% is markedly worse than the same agent at 20%, on the same
task, with the same instructions — and both of them will sound fine.

**As a rule: past 50%, a Claude Code agent is borderline unusable.**

## Hallucination is the least of it

The quiet failures are the ones that cost you, because they look like
work.

| It starts | Which looks like |
|---|---|
| rushing | ignoring your `CLAUDE.md`, your rules, your prompt |
| answering unchecked | quoting a clause without reopening the contract |
| forgetting | undoing a correction you made an hour ago |
| confusing sources | attributing your own instruction to the witness |
| hallucinating | citing authority that does not exist |

Every one of those is a thing a tired junior does at 2am. The difference
is that the junior sounds tired.

## It never tells you

There is no warning. No banner, no apology, no drop in fluency. The prose
stays confident, the formatting stays neat, the answers keep arriving
quickly.

```
   what you see          what is happening
  ┌─────────────┐       ┌─────────────┐
  │ confident   │       │ 62% full    │
  │ fluent      │       │ skimming    │
  │ fast        │       │ guessing    │
  └─────────────┘       └─────────────┘
```

The left box never changes. That is the entire danger: the signal you
would naturally trust is the one thing rot does not touch.

Which is why you need the number.

> **From the Boss:** *"This is why apps like claude.ai and Claude Cowork
> will never get you anywhere: you cannot see context. Your agents will
> start rotting, and you will only notice when the work ends up being
> dogshit — or you end up disbarred."*

In Claude Code the number is on your screen, always. That alone is worth
the terminal.

Press `n`.
