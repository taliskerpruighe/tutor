---
id: counter/builtin-agents
title: Builtin agents
level: Level 2
part: Counter-Recommendations
order: 1
summary: Turn off the agents Claude Code dispatches on its own initiative and let a custom agent built for the job stand in their place
keywords: [builtin agents, explore, plan, claude_code_disable_explore_plan_agents, settings.json, dispatch, spawn, custom agent, context, boss]
---

# Builtin agents

*v0.2.3*

Claude Code ships with subagents already built in, and you never asked
for them. An `explore` agent and a `plan` agent come bundled with the
program itself, defined by nobody who knows your practice, and the main
agent reaches for one on its own initiative whenever a job looks like
scanning a codebase before answering or turning a request into a plan
before it starts writing. You did not name either one, place it in an
`agents/` folder, or choose which model it runs on — it arrived already
decided, and the choice of when to use it was never yours either.

## Switch them off

The Boss's instruction is flat: turn them off. The setting sits in the
`env` block of your global `~/.claude/settings.json`, so it applies to
every session on the machine rather than one matter folder.

```json
{
  "env": {
    "CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS": "1"
  }
}
```

Set that once and the main agent stops reaching for either builtin
agent, in any session, from any folder you open it in.

## Too dumb to earn the seat

The first reason is quality. A builtin agent is generic by
construction — written to be useful to nobody in particular, which
means it is aimed at no matter, no practice area, no house style. It
does not know your clients, your document conventions or the shape of
your matter folder, and it never will. Anything it can do, a custom
agent you built yourself does better, because yours is aimed at your
own work rather than at an average of everybody's. You already know
how to build one: *Custom agents* and *Building one* cover the whole
of it, and neither takes longer than the interview a skill runs you
through.

## Worse, it dispatches one anyway

The second reason is cost, and it is the larger of the two. The main
agent does not wait to be asked. Mid-answer, it decides for itself
that a question wants exploring or planning, and it hands that piece
off without telling you first. No warning appears, nothing turns
amber, it simply spins up a subagent and waits on it — including for
questions it would have finished faster by itself.

As with the builtin agents generally, the Boss went through this the
hard way, watching one dispatch fire on a question a single sentence
would have settled.

Every one of those dispatches is a spawn: a fresh context window
opened, filled and read back, for work the main agent already had the
room to do unaided. You know from *Context* what that room costs
before a word of the answer is typed. **More is worse** — the one-line
form of the rule *Context* built, and a builtin agent is that rule
spending your context for you, without asking first.

Press `n`.
