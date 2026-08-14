---
id: hooks/pretooluse
title: PreToolUse
level: Level 2
part: Hooks
section: Using Them
order: 5
summary: A PreToolUse hook can see a tool call coming and refuse it outright, before a single line changes
keywords: [pretooluse, block, deny, skill, matcher, tool call, permission, settings.json]
---

# PreToolUse

*v0.2.9*

A `PreToolUse` hook fires after Claude has decided to run a tool and
before that tool actually runs — the one window in the whole trigger
list where a decision can still be reversed. Its exit code decides the
outcome: let the call through, or stop it there and hand Claude a
reason instead.

That is a different power. `SessionStart` and `SubagentStart` can only
add words. `PreToolUse` can say no.

## Forcing the skill before the write

Say a matter has a clause-extraction skill built for it, and the house
rule is that no draft gets touched before that skill has run over the
source document. Nothing stops an agent from going straight to `Edit`
on a bad day — nothing except a hook. A `PreToolUse` hook matched on
`Write` and `Edit` can check for the marker the skill leaves behind (a
small file, a line in a log) and refuse the call outright when it is
missing, sending Claude a message naming which skill to run first.

```
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "./hooks/require-extract.sh"
      }]
    }]
  }
}
```

The skill still has to be invoked by Claude's own judgement — this
course has said plainly, since *Start with never*, that the decision
to reach for one is never guaranteed. What the hook adds is not
certainty that Claude chooses well. It is a second check that does not
depend on Claude choosing well, sitting after the decision rather than
trusting it. Where the check fails, the tool call never runs at all —
there is no draft to undo, because nothing was written in the first
place.

## Refusing an edit against a dirty file

A second `PreToolUse` hook on the same two tools can ask a plainer
question first: is the file already committed? Where `git status` or
`jj status` shows it dirty, the hook refuses the edit before it
happens, rather than letting a second uncommitted change land on top
of the first with no clean point left to return to.

That is the insurance *What git is* already named — version control
as the one thing standing between you and an agent's own trigger-happy
edits — moved from something you rely on afterwards to something a
hook checks before the fact.

Both checks sit on the same trigger and the same two tools, and
neither knows the other exists — one hook asks whether the right skill
ran, the other asks whether the file was safe to touch at all, and
either can refuse the call on its own.

Press `n`.
