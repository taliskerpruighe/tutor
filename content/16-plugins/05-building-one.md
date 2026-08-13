---
id: plugins/building
title: Building one
level: Level 2
part: Plugins
section: Using Them
order: 5
summary: You do not hand-write a manifest or a marketplace listing; you tell Claude what to bundle and it writes both
keywords: [plugin, build, ask claude, manifest, marketplace, custom-agents, custom-skills]
---

# Building one

*v0.2.0*

You have not been shown how to write `.claude-plugin/plugin.json` by
hand, and you are not going to be. The rule here is the same one
*Inside `.claude`* gave you for `settings.json`: do not open it in an
editor, ask for it.

## What to say

Point Claude Code at whatever you want turned into a plugin and say
so plainly:

> *"Turn the bundle-reader agent and the bundle-read skill into a
> plugin I can install in other projects."*

Say what belongs in it, the way *Building one* had you say what an
agent was for. If you are starting from nothing rather than existing
assets, say that instead — describe the suite you want, and let Claude
Code build the agents and skills first, the way it always has, before
folding them into a plugin around them.

## What it does with that

It writes the manifest, builds the `.claude-plugin/` folder around it,
and moves or writes the agents, skills and hooks you named into place
next to it — the layout from *What is inside one*, assembled rather
than typed. If no marketplace exists yet for it to sit in, it can
write a small one for you, listing just this plugin, which is enough
to install it anywhere you like.

It will also ask the same question every build in this course asks
sooner or later: global, or one project — this time about where the
plugin gets installed once it exists, not about the plugin's own
files. Answer it the way you always have, with the narrowest scope
that still covers what you need.

## Why this one is not a checklist

*Step two — the workers* could give you exact answers to type, because
building an agent or a skill is the same four or five questions every
time. A plugin is not that — it is an assembly of things you have
already built, in whatever combination this suite happens to need, so
there is no fixed script to hand you.

What there is instead: ask for it, describe what goes in it, answer
the scope question, and let it write the two files that turn a folder
into something installable.

Now, doing that for real.

Press `n`.
