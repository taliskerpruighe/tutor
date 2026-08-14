---
id: hooks/sessionend-and-subagentstop
title: SessionEnd and SubagentStop
level: Level 2
part: Hooks
section: Using Them
order: 7
summary: SessionEnd closes out a whole conversation and SubagentStop checks a single subagent's work, both asking whether what was supposed to happen actually did
keywords: [sessionend, subagentstop, transcript, skill check, chain, workflow, audit, settings.json]
---

# SessionEnd and SubagentStop

*v0.2.9*

A `SessionEnd` hook fires once, when the session closes. A
`SubagentStop` hook fires once for every subagent a chain spawns, the
moment each one finishes. Both look backwards at a transcript that
already exists, asking the same question at two different scales: did
the work that was supposed to happen actually happen.

Neither trigger can change anything at this point — the session or the
subagent is already done. What they can do is refuse to let that go
unnoticed.

## Auditing the whole conversation

A `SessionEnd` hook can read the transcript on its way out and check
it against a short list: did a particular skill run at all, did a
named file get touched, did a commit happen before the session closed.
Where the answer is no, the hook writes that finding somewhere you
will actually see it — a log file, a line printed to the terminal —
rather than letting the session end and the gap go unremarked.

```
{
  "hooks": {
    "SessionEnd": [{
      "hooks": [{
        "type": "command",
        "command": "./hooks/audit-session.sh"
      }]
    }]
  }
}
```

That is also where the transcript itself is worth keeping in the
first place: `audit-session.sh` can copy it somewhere of your choosing
before the window closes and it is only scrollback you have to
remember to save by hand. Nothing about the audit needs a person to
trigger it, which is the entire point — the check that only runs when
someone remembers to run it is the check that gets skipped on the
afternoon it mattered most.

## Checking one subagent before it is trusted

`SubagentStop` asks the identical question at the size of a single
subagent, inside a chain nobody is reading line by line. A worker in
the middle of a five-agent workflow reports success; a `SubagentStop`
hook scoped to that agent can check its own slice of the transcript
for the one skill it was meant to invoke, and fail the step outright
where the check comes up empty, rather than letting a false report of
success carry forward into whatever agent picks it up next.

That is the gap named back in *Scoping a hook*: a chain with no
`SubagentStop` check has no way to catch a skipped skill except
reading every subagent's output by hand, and nobody does that on the
tenth run of a workflow that worked the first nine times.

## Two ends, one habit

A session and a subagent both produce a transcript nobody re-reads by
default. `SessionEnd` and `SubagentStop` are the same discipline
pointed at two different sizes of that transcript, catching what
silent success would otherwise hide.

Press `n`.
