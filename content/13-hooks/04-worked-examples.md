---
id: hooks/worked-examples
title: Worked examples
part: Hooks
section: Using Them
order: 4
summary: Eight triggers against eight jobs, so the abstract list from two articles ago turns into things worth building
keywords: [example, sessionstart, userpromptsubmit, pretooluse, posttooluse, subagentstart, subagentstop, stop, sessionend, workflow]
---

# Worked examples

*v0.2.0*

Eight triggers were a list two articles ago. Here they are against eight
jobs, so the list turns into things worth building rather than names to
remember.

## Session-level

- **`SessionStart`** — tell one custom agent to ignore part of your
  `CLAUDE.md`, or to follow special rules that apply on this project
  and nowhere else.
- **`UserPromptSubmit`** — remind the agent, on every message, to answer
  in two languages, without retyping the reminder yourself each time.
- **`Stop`** — have Claude rewrite its own answer if it blew a word
  limit, rather than trusting it to notice.
- **`SessionEnd`** — save the transcript somewhere of your choosing the
  moment the session closes, before it is only a scrollback you have to
  remember to copy.

Four hooks, none of them touching a tool call. They watch the
conversation itself: its start, its messages, its answers, its end.

## Tool and subagent-level

- **`PreToolUse`** — on `Write`, `Edit` or `Bash`, check that the file
  being touched is already committed, before the tool is allowed to run
  at all.
- **`PostToolUse`** — on `Write` or `Edit`, fire a subagent to review
  what was just written, the moment it lands.
- **`SubagentStart`** — preload a skill for a subagent the instant it
  spawns, rather than trusting its own instructions to reach for one.
- **`SubagentStop`** — confirm a subagent actually used the skill it
  was supposed to, in the middle of a large workflow where nobody is
  reading every report by hand.

These four sit closer to the machinery: a tool about to run, a tool
that just finished, a subagent starting, a subagent finishing. That is
the same bracket from *The triggers*, doing real work.

## Reading the split

Notice which four you would reach for on a single conversation, and
which four only start to matter once a chain or a workflow is running
several agents at once. `PreToolUse` checking that a file is committed
protects you whether you are typing yourself or a script is doing it
for you. `SubagentStop` confirming a skill was used has no purpose at
all outside a chain — there is no subagent to check when you are the
one doing the work.

That is the pattern from *What a hook is* again: the bigger the
pipeline, the more of these eight you need, because the more of it you
cannot see directly.

None of the eight above needs writing by hand. Ask for a hook the way
you asked for an agent or a skill — say the trigger, say the job, say
where it should be scoped — and let Claude produce the script and the
`settings.json` entry together. The value of knowing the eight triggers
and the two scopes is not that you can write the JSON yourself. It is
that you now know which of these eight jobs is worth asking for, and
where in the tree to put it once it exists.

---

That is Hooks. Plugins come next — the same agents, skills and hooks
you have just built, packaged so they travel to another project, or
another machine, without being rebuilt from nothing each time.

Press `n`.
