---
id: claude-code/inside-claude
title: Inside .claude
part: Setup
section: What It Reads
order: 6
summary: A tour of what lives inside .claude — more than you need today, so the names are not strange later.
keywords: [settings, CLAUDE.md, rules, agents, skills, hooks, plugins]
---

# Inside .claude

More than you need for today. You are reading this so that, when the
rest of the course reaches these words, they are not strange.

## The tour

```
.claude/
├── settings.json
├── CLAUDE.md
├── rules/
├── agents/
├── skills/
├── hooks/
└── plugins/
```

| Entry | What it holds |
|---|---|
| `settings.json` | your Claude Code settings |
| `CLAUDE.md` | the "invisible prompt" |
| `rules/` | instructions layered on `CLAUDE.md` |
| `agents/` | your custom agents |
| `skills/` | the skills you write |
| `hooks/` | scripts fired by triggers |
| `plugins/` | bundles that plug into any project |

## Two worth pausing on

`settings.json` is where your preferences live. It is JSON, and JSON is
unforgiving — one missing comma and the whole file stops working. The
right move is not to open it in an editor, but to ask Claude Code to
change it for you: say what you want changed, and let it edit the file.

`CLAUDE.md` is the more interesting one. Claude reads it at the start of
every new session, before you have said anything at all — an **invisible
prompt**, briefing it on how you want things done before you ask. Nothing
else in the directory has that reach. It is the highest-leverage file you
will own.

## The rest, briefly

`rules/` holds further instructions on top of `CLAUDE.md`, one file per
rule, so a single rule can be changed without rewriting everything else.

`agents/` and `skills/` hold what you build over the next two parts of
this course — custom agents, and the skills you write for them. Do not
try to absorb either now; each gets a part of its own.

`hooks/` holds scripts that fire automatically on a trigger during a
session — for when something must happen every time, rather than being
remembered.

`plugins/` holds bundles of agents, skills and settings that plug into
any project, yours or someone else's, in one move.

That is one directory, in one place. The next article is about the fact
that you can have as many of them as you like.

Press `n`.
