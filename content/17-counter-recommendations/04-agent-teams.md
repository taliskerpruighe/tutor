---
id: counter/agent-teams
title: Agent teams
level: Level 2
part: Counter-Recommendations
order: 4
summary: Teammates that message each other while they work and still get switched off before anything with a deadline attached
keywords: [agent teams, subagents, teammates, tmux, panes, messaging, claude_code_experimental_agent_teams, settings.json, experimental, boss]
---

# Agent teams

*v0.2.3*

An **agent team** is several agents running at once, not one agent
spawning another and waiting on it. *What a subagent is* settled the
ordinary shape: one instruction in, silence while it works, one
answer back at the end, no conversation possible in between. A team
keeps the conversation running while the work is still open, and a
teammate can message another teammate directly, sideways, the moment
it finds something worth passing on — not saved up for a final
report nobody reads until everything has stopped.

This one takes longer to argue against than the other three.

## A pane each

Run a team and every teammate opens in its own tmux pane, all live
on the same screen at once. *What it is for* already showed two
panes doing this for a run and its watcher; a team fills one pane
per teammate, each scrolling with that agent's own work as it
happens. Nothing else in this course gives you a view like it — an
actual window onto several agents at once, not a transcript to read
once they have all gone quiet.

## The one worth a second look

Every other feature in this part hides what happened, duplicates
work nobody asked for, or spawns agents underneath agents until
nothing can say what ran. Agent teams do the opposite. Teammates
tell each other what they found while it is still useful to know,
and you watch the exchange happen pane by pane, rather than
reconstruct it afterwards from whatever got written down. As with
the rest of this part, the Boss tried this one directly before
saying no to it, not on principle.

## Off anyway

The setting sits in the same `env` block as the rest of this part,
inside your global `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "0"
  }
}
```

Note the value: `"0"`, not `"1"`. This is the one setting in the
part that turns a feature off by setting it to zero rather than by
switching a disable flag on.

The reason is the variable's own name. `EXPERIMENTAL` is not
decoration. It means nobody has committed to what this feature does
next month, only to what it does today, and a matter with a deadline
on it is not where you want to discover that the shape changed
underneath you. Experimental does not warn first. No line appears in
the session to say a teammate's messaging changed, no changelog
arrives before you notice the panes are not saying what they said
yesterday. The failure is quiet, the way every failure in this
course has been quiet — and quiet is a worse trade than the one
genuinely good view on this list.

Watch it on a test matter if you want to see it work. Leave the
setting where it is for anything with a filing date on it.

---

That is Counter-Recommendations, and with it the whole course.
Agents, skills, subagents, workflows, hooks, plugins and headless
sessions are the working half — everything you now know how to
build. This part is the other half: the ledger of what to leave
switched off, and why, so that a feature turning itself on is never
something that happened to you by default. What is still not here
is work that starts on its own with nobody watching at all — crons,
schedules, machines that run while you are asleep. That is not here
yet, on purpose.

Everything up to here, you can build. Go and use it.
