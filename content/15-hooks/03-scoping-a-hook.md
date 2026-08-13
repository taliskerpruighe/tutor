---
id: hooks/scoping
title: Scoping a hook
level: Level 2
part: Hooks
section: What They Are
order: 3
summary: A hook obeys the same placement rule as everything else, plus one further axis — which agent, or which tool
keywords: [scope, settings.json, project, plugin, agent, matcher, customisation, location matters]
---

# Scoping a hook

*v0.2.0*

As with everything else you have built in this course, the
customisation is the point. A hook that fires for every agent, in every
project, on every tool call, is rarely the one you actually want.

That is the same rule as *content isolation*, applied one level finer:
put each thing where only the sessions that need it will walk past it.

## The coarse scope

Where a hook's `settings.json` lives decides the coarse scope, the same
way it did back in *Location matters*. Write it into a project's
`.claude`, and the hook fires only for sessions launched from that
project. Write it into your global `~/.claude`, and it fires everywhere
you ever launch Claude. Write it into a plugin, and it travels with the
plugin — into whichever projects and machines that plugin gets
installed on, and nowhere else.

## The finer scope

Inside that, a hook can be narrowed further: to a particular tool, so
`PreToolUse` only watches `Write` and `Bash` rather than everything, or
to a particular subagent, so `SubagentStart` only fires for the two
agents doing a sensitive job rather than every agent the project owns.

Put the two together and a hook can be aimed as precisely as an agent
or a skill can — narrower than the project, narrower than the folder,
down to the one tool or the one subagent it was written for.

## Why this beats editing CLAUDE.md

Say two custom agents in one project need to behave differently — one
should ignore part of your house style, the other should follow a rule
specific to this matter. Editing `CLAUDE.md` cannot do that: every agent
launched in that project reads the same file, so a change there changes
both of them, and every other session besides.

A hook scoped to the one agent does not have that problem. It fires
only when that agent starts, and the rest of the project never sees it
— not because it was told to ignore something, but because the hook was
never in its way to begin with. `CLAUDE.md` cannot be selective about
its audience. A hook, scoped this way, is nothing else.

## The habit this repeats

This is the third time the course has made the same point, in three
different files. `CLAUDE.md` and `rules/` are read by whoever launches
from that folder. An agent or a skill sits where only the sessions that
need it will find it. A hook now joins them, with the same question
attached: not *would this help*, but *who exactly should this reach,
and no further*.

Get the scope wrong in either direction and the cost is quiet. Scope it
too wide and a hook meant for one sensitive agent starts firing on
every session in the project, slowing all of them for a check that
only ever mattered to one. Scope it too narrow and the one session that
needed it launches without the hook at all, and the thing it was meant
to catch goes uncaught — with nothing in red to tell you so.

Now the triggers and the two scopes together, in cases you can
copy.

Press `n`.
