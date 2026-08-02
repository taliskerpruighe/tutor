---
id: claude-code/what-a-session-sees
title: What a session sees
level: Level 2
part: Claude
section: Claude Code setup
order: 11
summary: Claude walks up from the folder you launched in, collecting every .claude on the way.
keywords: [walk up, parent, ancestor, sibling, working directory, discovery, context]
---

# What a session sees

*v0.1.0*

You can have a dozen `.claude` directories scattered across your machine.
A session does not get all of them. It gets the ones it finds, and how it
finds them is a single rule.

## The rule

**Claude starts in the folder you launched from and walks up through the
parent folders, collecting every `.claude` it passes.** The global
`~/.claude` applies throughout, wherever you started.

Up, and only up. A `.claude` in a folder beside you is not on the path
upward from where you started, so it is never seen. Neither is one buried
in a folder below you.

That is the whole mechanism. Everything else in this part is a consequence
of it.

## Three launches, one machine

Take this layout:

```
~/
├── .claude/
└── work/
    ├── .claude/
    ├── research/
    │   └── .claude/
    └── writing/
```

Now launch from three different places.

**From `~/work/research`:**

```
cd ~/work/research && claude
```

Walking up: `research/.claude`, then `work/.claude`, then `~/.claude`.
Three of them, all in play. This session has the most context of any
below.

**From `~/work/writing`:**

```
cd ~/work/writing && claude
```

Walking up: `writing/` has no `.claude`, then `work/.claude`, then
`~/.claude`. Two. Note what is missing — `research/.claude` is a *sibling*
of where you started, not an ancestor, so it never comes into it. Its
agents and skills might be exactly what you needed. The session will never
know they exist.

**From your home folder:**

```
cd ~ && claude
```

One: `~/.claude`. Everything under `work/` is below you, and the walk only
goes up. A session started here is the emptiest one on the machine, which
is not the same as the safest.

## Why this is worth knowing properly

It is tempting to read that as a piece of plumbing. It is not. The model
is the same model in all three sessions — same weights, same training, no
difference at all. What changes between them is the material it has been
handed before you type a word.

Control what the harness sees, and you control how the model performs.

The next article is what to do with that.

Press `n`.
