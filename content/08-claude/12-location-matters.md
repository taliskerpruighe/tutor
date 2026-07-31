---
id: claude-code/location-matters
title: Location matters
part: Claude
section: Claude Code setup
order: 12
summary: More is worse — so split what you build across folders and launch from the right one.
keywords: [content isolation, context, too many, agents, skills, layout, party trick]
---

# Location matters

*v0.1.0*

Now the consequence, and it is not the one people expect.

More is worse.

## More is worse

The more rules Claude has to read before it starts, the more agents it can
see, and the more skills it has to weigh, the worse it gets. Not slower —
*worse*. Every extra option is another thing to consider and another
chance to pick wrong, and it pays that cost on every single question,
including the ones where none of it was relevant.

Put fifty agents and two hundred skills in `~/.claude` and you will have a
tool that reaches for the case-law agent to help you rewrite a birthday
message. Everyone who builds a lot arrives at this, usually by building a
lot first.

The fix follows straight from the walk-up rule, and it is the first real
technique in this course.

> **Party Trick #1 from the Boss: content isolation.** Put each thing
> where only the sessions that need it will walk past it.

## The bad layout

A working solicitor, everything piled in two places:

```
~/
├── .claude/
│   ├── agents/  web, assistant
│   └── skills/  web-search, email,
│                calendar
└── work/
    └── .claude/
        ├── agents/  research, writer,
        │            reviewer, work-asst
        └── skills/  case-law, regs, memo,
                     briefs, motion,
                     bluebook, adversarial,
                     checker, work-email,
                     work-cal
```

Nothing here is wrong on its own. The problem is that every session
started anywhere under `work/` gets all four work agents and all ten work
skills — plus the personal ones from the global directory, which are on
the way up. Drafting a memo, it can see the bluebooking skill, the
adversarial reviewer, your calendar and your personal email.

## The good layout

Same agents, same skills. Moved.

```
~/
├── .claude/
│   ├── agents/  web
│   └── skills/  web-search
├── personal/
│   └── .claude/
│       ├── agents/  assistant
│       └── skills/  email, calendar
└── work/
    ├── .claude/
    │   ├── agents/  work-asst
    │   └── skills/  work-email,
    │                work-cal
    ├── research/
    │   └── .claude/
    │       ├── agents/  research
    │       └── skills/  case-law,
    │                    regs
    └── writing/
        └── .claude/
            ├── agents/  writer,
            │            reviewer
            └── skills/  memo, briefs,
                         motion,
                         bluebook,
                         adversarial,
                         checker
```

The web agent stays global because looking something up is useful
everywhere. Everything else has dropped to the narrowest folder that still
covers every session needing it.

## What each session gets

| Launch from | It sees |
|---|---|
| `~/personal` | web, assistant — and nothing about law |
| `~/work` | web, work-asst — email and diary for work |
| `~/work/research` | web, work-asst, research |
| `~/work/writing` | web, work-asst, writer, reviewer |

Read the third and fourth rows against each other. The research session
has no idea the writing skills exist, and the writing session has no idea
about case-law. Each is missing things — deliberately. Each is sharper for
it.

And nothing was thrown away. Everything is still on the machine, one `cd`
away. You are not choosing what to own. You are choosing what to walk past.

## The habit

When you write something new — a rule, an agent, a skill — the question is
not *is this good?* but **where does this belong?**

Ask it as: *which sessions need this, and what is the deepest folder they
all sit under?* That folder is the answer. If the honest answer is "every
session I ever run", it goes in `~/.claude`, and that should feel like a
rare event rather than a default.

Get this right and everything in the rest of the course compounds. Get it
wrong and it accumulates instead.

---

That is Claude, and with it everything this course had to put underneath
Claude Code before it could start teaching it — the terminal, the shell,
the software, the files, Linux, and what a model and a harness actually
are. All of it was groundwork. From here the course only builds.

Agents are next: what one actually is, the single thing that decides
whether it does good work, and how to make your own. Then skills, which
teach an agent something once and keep it taught, and subagents, which
put several of them on one job.

Press `n`.
