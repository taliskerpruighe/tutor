---
id: agents/default
title: The default agent
part: Agents
section: Custom Agents
order: 5
summary: Every plain `claude` gives you the same type of agent — the default one, which has no definition behind it.
keywords: [default agent, claude, type, definition, same, plain, launch]
---

# The default agent

You already know that every conversation is a separate agent. Here is the
part that was left out.

They are all the **same kind** of agent.

Type `claude` in a Ghostty tab and you get one. Type it in another tab and
you get a second one — separate context, separate memory of the
conversation, no knowledge of the first. But cut them open and they are
identical. Same model. Same instructions. Same tools. Same everything.

```
  tab 1   claude ──▶ agent  ┐
  tab 2   claude ──▶ agent  ├─ all the same type
  tab 3   claude ──▶ agent  ┘
```

Claude Code has a name for that type. It calls it **`claude`** — the
**default agent**.

## What "default" actually means

It is the one you get when you have not asked for anything else. Nothing
more mysterious than that.

And it has a property worth pausing on: **there is no file behind it.**
Look through `~/.claude` for the thing that defines the default agent and
you will not find it, because it does not exist. The default agent is
built into Claude Code itself.

| | Default agent |
|---|---|
| How you launch it | `claude` |
| Model | whatever your account defaults to |
| Instructions | your `CLAUDE.md` and rules, nothing more |
| Tools | all of them |
| Definition file | none |

## Why that is a limit

That table is the whole problem. Every session you have run so far has
been the same agent, doing everything.

The same agent reads your case law and drafts your correspondence. It runs
on one model whether the task is hard or trivial. It holds every tool it
has, including the ones you would rather it never touched on a Tuesday
afternoon in a live matter.

Say you want an agent that only ever reads and reports, never writes. Or
one that runs on a cheap model because all it does is check citations. You
cannot get either by launching `claude` differently — there is nothing to
change, because there is no file to change it in.

So you write one. That is the next article.

Press `n`.
