---
id: plugins/what-it-is
title: What a plugin is
part: Plugins
section: What They Are
order: 1
summary: A plugin is a portable .claude directory, built once and installed anywhere rather than written into one project
keywords: [plugin, portable, install, marketplace, project, global, bundle, agents, skills]
---

# What a plugin is

*v0.2.0*

Several parts back, the tour of `.claude` named a `plugins/` folder and
moved on before saying what fills it. Here is what fills it.

A **plugin** is a remote, portable `.claude` directory. Everything you
already know how to build — agents, skills, hooks — normally gets
written straight into one project's `.claude`, where it stays put. A
plugin is the same material, written instead into an ordinary folder
of its own, with nothing tying it to any particular matter.

## The move that matters

Once that folder exists, it does not have to live inside a project at
all. You install it — into one project, into several, into every
session on the machine, or onto somebody else's machine entirely.

```
  ordinary folder
  agents/  skills/  hooks/
        │
        ├──▶ project A's .claude
        ├──▶ project B's .claude
        ├──▶ every session (global)
        └──▶ a colleague's machine
```

That is the whole shift. Writing into `.claude` ties the work to the
folder it sits in. Writing into a plugin keeps the work independent of
any one folder, so it can turn up in as many of them as you like,
without being copied and re-copied by hand.

## Not a new kind of asset

Nothing inside a plugin is a new thing to learn. An agent inside one
is still exactly the agent from *Custom agents* — same file, same
fields. A skill is still the skill from *Start with never*, built the
same way for the same reasons. A plugin does not change what any of
these are; it changes where they live and how far they travel.

That distinction is worth holding onto through the rest of this part.
Nothing here replaces anything you have already built. It is a second
place to keep it — one that is not stuck to a single project the way
`.claude` is.

It is also not a default. Most of what you build in this course will
never become a plugin, and should not — a chronology skill built for
one bundle has no reason to travel anywhere else, and putting it in a
plugin would only add a folder nobody needed to find it in.

The next article is when it is worth the extra step.

Press `n`.
