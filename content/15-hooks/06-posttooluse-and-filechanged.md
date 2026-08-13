---
id: hooks/posttooluse-and-filechanged
title: PostToolUse and FileChanged
level: Level 2
part: Hooks
section: Using Them
order: 6
summary: PostToolUse fires once Claude's own tool call is done, and FileChanged fires when a file changes for any reason at all, including one Claude was never told about
keywords: [posttooluse, filechanged, git, jj, commit, save, review, subagent, settings.json]
---

# PostToolUse and FileChanged

*v0.2.9*

A `PostToolUse` hook fires the instant a tool call Claude made
finishes — the edit has already landed, and the hook is reacting to a
fact rather than a plan. A `FileChanged` hook fires on the same fact
from a wider door: any change to a file's contents, whether Claude
wrote it, a background script did, or you opened the file yourself
and saved it.

Between them they cover writing that happens inside the conversation
and writing that does not.

## Saving the work, not writing it

`Write` and `Edit` change a file on disk. They do not, on their own,
put that change anywhere durable — a version-controlled repository
still needs a commit, and nothing forces one just because a tool call
succeeded. A `PostToolUse` hook matched on `Write` and `Edit` can run
the commit itself, the moment the tool finishes, so every edit is
captured on its own rather than sitting beside the next one with no
line drawn between them.

```
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "./hooks/save-change.sh"
      }]
    }]
  }
}
```

`save-change.sh` runs `jj commit -m "wip"`, or the `git` equivalent,
and nothing else. It does not write a proper message; that is a job
for a person, not a script reacting in the background. A rough commit
on every edit still beats no commit at all — it gives you a point to
return to, even one you would never have written by hand.

## Catching what Claude never touched

`FileChanged` covers ground `PostToolUse` cannot reach. Open the same
file in an editor tab, change three lines by hand, and save it — no
tool call happened, so no `PostToolUse` hook fires, but the file
changed all the same. A `FileChanged` hook watching that path runs the
identical save script regardless of who made the change, which
matters precisely because *What a hook is* never said the change had
to come from Claude. The safety net is the file, not the tool call
that touched it.

## Reviewing on the way past

The same trigger can do a second job on the same event: a
`PostToolUse` hook matched on `Write` can spawn a small review
subagent the moment a file lands, checking it against house style
before anyone reads it by eye. Saving and reviewing are two separate
hooks on the same trigger, not one script doing both — each stays
small, and each can fail without taking the other down with it.

Two triggers, one blind spot removed between them. Next, the pair
that checks whether the work itself held up, once the session or the
subagent that produced it has already gone quiet.

Press `n`.
