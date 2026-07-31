---
id: skills/what-a-skill-is
title: What a skill is
part: Skills
section: When To Build One
order: 2
summary: A folder holding a SKILL.md and its supporting files — think of it as a custom, much longer prompt you only write once.
keywords: [skill, folder, SKILL.md, supporting files, claude directory, global, project, prompt]
---

# What a skill is

*v0.1.0*

The easiest way to think of a skill is as a **custom, longer prompt**.

Everything you would have typed — the standing instructions, the house
rules, the four things you explain every morning before the work can
start — written out properly, once, and kept somewhere the agent can
find it. When the job comes up, that prompt arrives with it. You did
not type it and you cannot forget half of it.

And like a custom agent, it is smaller than it sounds. A skill is a
**folder** with two things in it:

- a `SKILL.md` file — the instructions, and the settings that say when
  they apply, and
- supporting files — the templates, the checklists, the precedent
  wording, anything the instructions point at.

Only the first is compulsory. A perfectly good skill can be one file
in a folder of its own.

## Where the folder goes

Inside a `.claude` directory, in a `skills/` folder. You already know
there can be many `.claude` directories, and which one you choose is
the whole of the decision.

In the **global** directory, reachable from anywhere on the machine:

```
~/
└── .claude/
    └── skills/
        └── proofread/
            └── SKILL.md
```

Or in a **project** directory, reachable only from that folder down:

```
~/work/mackenzie/
└── .claude/
    └── skills/
        └── chronology/
            ├── SKILL.md
            └── references/
                └── date-rules.md
```

`proofread` applies to any document you will ever open, so it lives at
the top and every session can see it. `chronology` knows the shape of
one matter's bundle — its date conventions, which exhibits are which,
what "the record" means here — so it lives in the Mackenzie folder,
and a session opened anywhere else neither sees it nor pays for it.

That is the walk-up rule from *Location matters*, and it applies to
skills exactly as written. **More is worse.** A skill goes in the
narrowest folder that still covers every session needing it. Global
should feel like a decision you took, not the place things end up.

## The two halves, and what they cost

The split matters more than it looks, so it is worth having early:

| Part | When it is read |
|---|---|
| `SKILL.md` settings | always |
| `SKILL.md` instructions | when the skill fires |
| supporting files | only when pointed at |

Read down that column and the design of a skill falls out of it. The
settings are written to be found, the instructions are written short,
and anything heavy — the sixty-page style guide, the precedent letter,
the checklist of forty items — goes in a file that is opened only on
the day it is needed.

Each of those three gets an article. The settings first.

Press `n`.
