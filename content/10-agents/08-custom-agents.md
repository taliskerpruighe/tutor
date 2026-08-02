---
id: agents/custom
title: Custom agents
level: Level 2
part: Agents
section: Custom Agents
order: 8
summary: A custom agent is one file in a `.claude/agents/` folder, launched with `claude --agent`.
keywords: [custom agent, agents folder, definition, --agent, global, project, launch]
---

# Custom agents

*v0.1.0*

A **custom agent** is an agent you defined. Different instructions, a
different model, a narrower set of tools — whatever the role needs.

And it is smaller than it sounds. A custom agent is **one file**. Nothing
is installed, nothing is registered, nothing is configured. You put a file
in a folder and the agent exists.

## Where the file goes

In an `agents/` folder inside a `.claude` directory. You already know
there can be many of those.

```
~/
├── .claude/
│   └── agents/
│       └── researcher.md      ← from anywhere
└── work/
    └── mackenzie/
        └── .claude/
            └── agents/
                └── bundler.md ← only in here
```

`researcher.md` sits in the global directory, so every session on the
machine can reach it. `bundler.md` sits inside the Mackenzie folder, so
only sessions launched from there — or below it — will ever see it.

That is the walk-up rule again, and *Location matters* applies here
exactly as written. **More is worse.** An agent goes in the narrowest
folder that still covers every session needing it, and a global agent
should feel like a rare decision rather than the default one.

## How you launch it

The filename, without `.md`, is the agent's name. You pass it to `claude`:

```bash
claude --agent researcher
```

Same as before in every other respect — a terminal, a conversation, a
context bar. What changed is which agent answers.

| You type | You get |
|---|---|
| `claude` | the default agent |
| `claude --agent researcher` | your researcher |
| `claude --agent bundler` | your bundler |

## What it looks like in practice

Mackenzie is in disclosure. Three roles, three files, all inside the
matter folder:

```
work/mackenzie/.claude/agents/
├── bundler.md     reads the bundle, lists what
│                  is relevant. Reads only.
├── drafter.md     writes the sections, given
│                  the list.
└── checker.md     checks citations and
                   references to the record.
```

Three agents, three jobs, none of them holding the others' tools or
instructions. `bundler` cannot write a file even if it wanted to, because
you did not give it the ability. `checker` runs on a cheap model because
matching a citation is not hard work.

None of that is possible with one agent doing everything.

Now, what actually goes inside the file.

Press `n`.
