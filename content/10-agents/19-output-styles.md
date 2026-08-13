---
id: agents/output-styles
title: Output styles
level: Level 2
part: Agents
section: Custom Agents
order: 19
summary: An output style changes the register of the whole session, not any single agent's tools or model
keywords: [output style, register, settings.json, interactive session, headings, diagrams, headless, subagent, definition file]
---

# Output styles

*v0.2.9*

An **output style** changes how the agent talks to you. It does not
change what it can do.

The six fields from the last article live in a definition file and
configure one agent — a separate identity you launch with `--agent` or
hand a job to. An output style is not part of that file at all. It
sets the register of the session you are already sitting in, whatever
agent, or lack of one, is running it. Short, and mostly a matter of
scope.

## Where a style lives

Each one is a small markdown file — a `name`, a `description`, then
plain prose instructions, the way a skill's body reads. Yours go in
`~/.claude/output-styles/`, or a project's own copy for a style you
only want there. Which one is switched on is a single name recorded
in `settings.json`, so a project can carry its own choice without
touching yours — the same split *Location matters* draws for
everything else you build.

Some names are built in and ship with the product. The rest are files
you wrote yourself. Nothing about picking one tells you which kind it
is — you name a style, and the session's register changes underneath
you, the same session, still with the same tools and the same model
it had a moment before.

## What you ask for

The content is a register, not a rule. Ask for headings and replies
come back structured under them where they did not before. Ask for a
diagram and it reaches for one before a paragraph of prose. Tell it to
drop bullet points and write only in sentences, or to give a verdict
in one line before the reasoning behind it, and every reply after that
follows the instruction, not only the next one.

That is the whole difference from typing the same request into a
prompt. Said once, in a style, it holds for the rest of the session
instead of being repeated on every question you ask.

## What it does not touch

A style governs one interactive session and nothing it spawns. A
subagent it dispatches runs on its own definition, style or none, and
never inherits the parent's. A noninteractive run — a script, a hook,
`claude -p` — has no session sitting in front of anyone for a register
to change, so the setting is simply never read.

The Boss keeps one that answers only what he asked and stops there,
and reaches for it on a bad day.

---

You have met both halves now — six fields that decide what an agent
is, and a style that decides how it sounds once it is talking. Next,
the skill that asks four questions and writes an agent's file for you.

Press `n`.
