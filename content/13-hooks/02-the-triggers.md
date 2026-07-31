---
id: hooks/triggers
title: The triggers
part: Hooks
section: What They Are
order: 2
summary: Eight moments a hook can attach to, and knowing the list is what tells you a hook is even possible
keywords: [trigger, event, sessionstart, userpromptsubmit, pretooluse, posttooluse, subagentstart, subagentstop, stop, sessionend]
---

# The triggers

*v0.2.0*

A hook attaches to one of eight moments. The list matters more than it
looks — the question "would a hook help here" only occurs to you once
you know a hook can attach to that particular moment at all.

## Around the session

| Trigger | Fires |
|---|---|
| `SessionStart` | when you launch Claude |
| `UserPromptSubmit` | whenever you send a message |
| `Stop` | when Claude finishes responding |
| `SessionEnd` | when the session closes |

These four bracket the conversation itself, from the moment the window
opens to the moment it closes, with one more either side of every
message you send.

## Around a tool call and a subagent

| Trigger | Fires |
|---|---|
| `PreToolUse` | just before a tool runs |
| `PostToolUse` | just after a tool finishes |
| `SubagentStart` | when a subagent is spawned |
| `SubagentStop` | when a subagent finishes |

Notice the shape of both tables: each pair brackets something. `Pre` and
`Post` bracket a single tool call — `Write`, `Edit`, `Bash`, whatever it
is. `Start` and `Stop` bracket a subagent's entire life, from spawn to
report back. That gives a hook two chances at the same event: one while
it can still be stopped, and one after the result is already sitting on
the table.

`SessionStart` and `SessionEnd` do the same at the widest scale of all
— the session itself is the thing being bracketed.

None of these eight fires because Claude chose to run something. Each
one fires because something happened, the way a doorbell rings because
someone pressed it, not because the house decided to let them in. That
distinction is the whole of the previous article: a rule can be
misread, a skill can go uninvoked, but a trigger firing is not a
judgement call at all.

## Reading the list as a map

Lay the two tables side by side and they cover the entire shape of a
session: opening, message, tool, subagent, tool again, subagent again,
message again, closing. Nothing that happens inside Claude Code
happens outside that sequence, which is why eight is the whole list and
not a sample of it.

`PreToolUse` and `PostToolUse` fire once for every tool call, which in
a long session can be dozens of times. `SessionStart` and `SessionEnd`
fire once each, at the two ends. A hook attached to a frequent trigger
earns its keep quietly, over and over, in the background; a hook
attached to a rare one earns it once, at a moment that matters more for
being the only one.

Eight triggers, and every one of them can be told to fire everywhere in
a session, or in almost none of it.

Press `n`.
