---
id: agents/what-it-is
title: What an agent is
part: Agents
section: Context
order: 1
summary: Every separate conversation is a separate agent, and it knows nothing about the others.
keywords: [agent, conversation, session, separate, fresh, parallel, terminal]
---

# What an agent is

*v0.1.0*

**AI agent** is a phrase that means something different everywhere you
read it. Ignore all of that. In Claude Code it has one meaning, and it is
simpler than the phrase suggests.

**Every time you start a separate conversation, you are talking to a
separate agent.**

That is the whole definition. Open a Ghostty tab, type `claude`, and you
have made an agent. Open another and you have made a second one.

## Same in every way, still separate

The two can be identical. Same model. Started from the same folder. Handed
the same `CLAUDE.md`, the same rules, the same skills. None of that makes
them one agent.

```
  Ghostty tab 1     Ghostty tab 2     Ghostty tab 3
  ┌──────────┐      ┌──────────┐      ┌──────────┐
  │ claude   │      │ claude   │      │ claude   │
  │          │      │          │      │          │
  │ agent A  │      │ agent B  │      │ agent C  │
  └──────────┘      └──────────┘      └──────────┘
       └─────────────────┴─────────────────┘
             same ~/work/writing/.claude
```

Three agents. One set of instructions between them. Tell agent A that the
client's name is spelled *Mackenzie*, not *McKenzie*, and agents B and C
will never hear about it.

## What is shared and what is not

The split is exact, and it is worth holding in your head:

| Shared by all three | Private to each one |
|---|---|
| the model | everything you typed |
| `CLAUDE.md` and rules | everything it replied |
| the skills it can reach | which files it opened |
| the folder it started in | every correction you made |

The left column is what was handed over at launch. The right column is
everything that happened afterwards.

## Each one starts from nothing

An agent begins knowing only what the walk-up rule collected for it — the
`.claude` directories between where you launched and your home folder, as
in *What a session sees*. Nothing else.

It has no memory of yesterday's conversation. It cannot look sideways at
the conversation you have open in the next window. There is no shared pool
somewhere that they all draw on.

If two agents need to know the same thing, you either write it down where
both will walk past it, or you tell both of them.

## You can run as many as you like

There is no limit but your machine. Want three going at once — one reading
a bundle, one drafting, one checking citations? Open three Ghostty tabs
and start three conversations.

Whether that is a good idea is a separate question, and the rest of this
part is the answer to it.

Press `n`.
