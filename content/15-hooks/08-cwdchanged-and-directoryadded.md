---
id: hooks/cwdchanged-and-directoryadded
title: CwdChanged and DirectoryAdded
level: Level 2
part: Hooks
section: Using Them
order: 8
summary: CwdChanged fires when an agent's working directory moves and DirectoryAdded fires when a new one enters its reach, both forcing a read that would otherwise wait on chance
keywords: [cwdchanged, directoryadded, cwd, working directory, claude.md, rules, settings, subdirectory]
---

# CwdChanged and DirectoryAdded

*v0.2.9*

A `CwdChanged` hook fires when an agent's own working directory moves
— a `cd` inside a `Bash` call, a subagent launched somewhere other
than the project root. A `DirectoryAdded` hook fires when a new
directory enters the agent's reach at all: one created mid-session, or
one that simply was not there when the session opened. Both exist for
the same reason — to force a read that would otherwise depend on the
agent happening to open the right file first.

## Why "eventually" is not good enough

A subdirectory can carry its own `CLAUDE.md`, its own `rules/`, its
own local settings, and ordinarily those are picked up the moment
Claude reads or edits a file inside that folder. That works, but only
after the first file is touched. Between the `cd` and the first
`Write`, an agent can run several tool calls already carrying
assumptions from wherever it was before — the parent's conventions, or
none at all.

## Reading local rules before the first move

A `CwdChanged` hook closes that gap directly: matched on the shell
tool, it checks the new working directory for a local `CLAUDE.md` or
`rules/` file and prints its contents into context immediately, ahead
of the agent's next tool call rather than after its first mistake
inside the new folder.

```
{
  "hooks": {
    "CwdChanged": [{
      "hooks": [{
        "type": "command",
        "command": "./hooks/brief-local-rules.sh"
      }]
    }]
  }
}
```

A large repository holding several nested projects, each keeping its
own conventions, is exactly where this earns its keep — an agent
working across three of them in one session ought to read three
different files, not one carried over from the first. The hook does
not care whether the move happened because you typed `cd` or because a
subagent was launched somewhere unusual; either counts as the working
directory changing.

## Catching a directory nobody scoped yet

`DirectoryAdded` covers the case `CwdChanged` cannot: a folder that
did not exist a moment ago. A new branch of work creates a fresh
top-level directory, or an agent's own `Write` call makes one for the
first time. Neither has a `CLAUDE.md` to read yet, and a hook matched
on `DirectoryAdded` can say so plainly — flagging the new folder as
unscoped, rather than letting the agent inherit the parent's rules by
default and never notice that it did.

Both triggers protect the same fact: a rule sitting in a file nobody
has read yet is not a rule an agent is following, whatever `CLAUDE.md`
claims about it. That is worth catching precisely because it fails
quietly — an agent working under the wrong rules gives no sign of
doing so, and produces work that reads exactly like work done
correctly, right up until someone checks it.

The last pair in this section watches something further out still —
not a folder gaining a file, but a whole second copy of the repository
appearing beside the first.

Press `n`.
