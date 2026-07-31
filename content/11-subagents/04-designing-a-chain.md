---
id: subagents/designing
title: Designing a chain
level: Level 2
part: Subagents
section: Chains
order: 4
summary: Three shapes, from generic agents on different models to custom agents each running their own skill — and one rule about not mixing.
keywords: [chain, shapes, model, effort, custom agents, skills, mixing, one skill per spawn]
---

# Designing a chain

*v0.1.0*

Three shapes, easiest to hardest. Each one buys you something the one
before it did not.

## 1. Generic agents, different models

Plain `claude` subagents, spawned as in the last article, except that you
say which model each is to run on.

```
  main agent    opus
    ├──►  claude   sonnet
    ├──►  claude   sonnet
    └──►  claude   haiku
```

Cheapest to reach — you can ask for this in a sentence, today, with
nothing written down anywhere. What you get is the model split and nothing
else: three identical agents, differing only in how much brain each is
running on. Every one of them still needs telling what it is and what it
is for, in full, every time.

## 2. Custom agents, different models

Now the boxes are agents you wrote, each pinned to its model in its own
definition file.

```
  main agent    opus
    ├──►  researcher     sonnet
    ├──►  drafter        sonnet
    └──►  cite-checker   haiku
```

The gain is everything a definition carries — from *The fields that
matter*, that is a role, a briefing, and a `tools` set. The
`cite-checker` cannot write, because you did not give it `Write`. The
`researcher` knows what counts as an authority worth having, because its
body says so. None of that has to be repeated at spawn time, because it
lives in the file.

## 3. Custom agents, different skills

The full shape. Each agent runs a **skill**, and the skill carries the
`effort`.

```
  main agent    opus
    ├──►  researcher     sonnet
    │       /find-authorities    effort: high
    ├──►  drafter        sonnet
    │       /write-brief         effort: high
    └──►  cite-checker   haiku
            /check-cites         effort: low
```

Two dials on every stage, and they live in different places.

**Model on the agent. Effort on the skill.** Not an arbitrary split. An
agent may run different skills across different spawns — that `drafter`
will write your briefs on Monday and your attendance notes on Thursday —
so pinning thinking depth into its definition would fix a value that
definition cannot possibly know. The skill knows: a brief wants `high`,
a citation check wants `low`. That is *The frontmatter* again, and this is
what it was for.

## One skill per subagent

A note from the Boss, learned the hard way. Asking one subagent to use two
skills in the same conversation is trouble.

**Bad.** Spawn one `writer` subagent and ask it to use the `write-brief`
skill for the brief and the `write-affidavit` skill for the affidavit.

**Good.** Spawn one `writer` for the brief with `write-brief`. Then,
separately, another `writer` for the affidavit with `write-affidavit`.

The two skills do not sit side by side in one head. They bleed — the
affidavit comes back argumentative, the brief comes back stiff, and each
document carries traces of the rules written for the other.

So: one skill per subagent. A stage that needs a second skill is a second
spawn. Spawns are cheap and a muddled draft is not.

Three shapes and a rule. What remains is how the chain actually gets
started — and that turns out to be the hardest part.

Press `n`.
