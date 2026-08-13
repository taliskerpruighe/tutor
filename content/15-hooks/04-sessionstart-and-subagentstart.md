---
id: hooks/sessionstart-and-subagentstart
title: SessionStart and SubagentStart
level: Level 2
part: Hooks
section: Using Them
order: 4
summary: A SessionStart hook briefs an agent before it reads a word, and a SubagentStart hook does the same the instant a subagent spawns
keywords: [sessionstart, subagentstart, context injection, brief, claude.md, settings.json, skill, matter]
---

# SessionStart and SubagentStart

*v0.2.9*

A `SessionStart` hook and a `SubagentStart` hook do the same job at two
different sizes: put text in front of an agent before it has read
anything else in the session. Neither waits for a question, and
neither depends on `CLAUDE.md` already covering the point.

That gap is worth naming plainly. `CLAUDE.md` is fixed the moment a
session opens, and every agent launched from that folder reads the
same file. A `SessionStart` hook is not fixed the same way — it runs
at the moment the session actually starts, and can pull in something
`CLAUDE.md` cannot: a value read from the environment, the output of a
small script, a line that only applies today.

## What CLAUDE.md cannot say

Say one folder runs several ongoing matters through Claude Code, and
the house style in `CLAUDE.md` is written once for all of them. A
`SessionStart` hook can run a short script that reads the matter code
from the environment and prints one line into context: which client's
rules apply this session, and which part of the house style to set
aside for it. `CLAUDE.md` cannot do that — it is read once, the same
way, regardless of which matter is actually open.

```
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "./hooks/brief-matter.sh"
      }]
    }]
  }
}
```

`brief-matter.sh` looks up the matter's exceptions and prints them to
standard output. Claude sees that output as though it were the first
line of the conversation, ahead of your own first message. Nothing
about the script depends on you remembering to say any of it yourself
— the brief is there before the first prompt is even typed.

## The same idea, one layer down

A `SubagentStart` hook injects the same way, scoped to one subagent
rather than the whole session. A review subagent that must run a
clause-extraction skill on every file it opens does not have to be
trusted to remember that unprompted — a `SubagentStart` hook matched
to that agent's name can print the instruction the instant it spawns:
use the skill before reading anything else. The subagent's own prompt
can say the same thing, but the hook says it regardless of whether
that prompt was written carefully enough.

As with the scope in *Scoping a hook*, the trigger can be aimed at one
named subagent rather than every one a project owns, so the injection
lands only where it is needed. A subagent that never touches a
document at all never sees the reminder, and never pays the small
context cost of reading an instruction it had no use for.

## Why the moment matters

An instruction added mid-session competes with everything already
sitting in context. One added at `SessionStart` or `SubagentStart` is
the first thing an agent reads, before it has formed any view of the
task — closer to a standing order than a reminder.

Next, a trigger scoped to something far smaller than a session: one
tool call, and a hook that can refuse to let it run at all.

Press `n`.
