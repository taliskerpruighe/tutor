---
id: skills/how-they-work
title: How skills work
level: Level 2
part: Skills
section: Making Them Fire
order: 10
summary: Writing a good skill is the easy part — getting it to fire when it should, and only then, is the hard part.
keywords: [skill, firing, frontmatter, skills field, skill tool, subagent, main agent, documentation]
---

# How skills work

*v0.1.0*

If they are not managed properly, they do not.

Writing a good skill is the easy part. It takes an afternoon, the
shape is small, and something else writes most of it for you.
Getting Claude to reach for that skill at the moment it should — and
to leave it alone at every moment it should not — is the part that
takes managing. Skip that part and you have a very well-written file
that nothing ever reads.

## What you will be told

Read the official documentation on this, or ask Claude, and you get
the same tidy answer both times. It is all about the
frontmatter of the agent's definition file — the settings block from
*The definition file*. Two routes, depending on what you want:

```
---
name: bundler
skills: house-style
tools: Read, Glob, Grep, Agent, Skill
---
```

- **`skills:`** — name a skill on this line and the agent always
  knows about it and always uses it.
- **`Skill` in `tools:`** — give the agent the tool for loading
  skills and it goes looking on its own, finding the right one only
  when the work calls for it.

Always on, or found when needed. Two settings, one line each.

It is a good story. Most of it does not survive contact with real
work.

## What actually happens

Both routes behave on a **main agent** — the one you are having the
conversation with, the one that answers when you type. There, more
or less, they do what they claim.

Send the work anywhere else and it comes apart. A subagent, called
by your agent to handle a piece of the job, does not reliably pick
the skill up. Nor, when you get to them, does a session running on
its own with nobody watching. The skill is sitting right there on
disk — correctly written, correctly placed, named in the
frontmatter — and nothing loads it.

Nothing tells you, either. The work comes back done the ordinary
way, which is to say done without the thing you wrote to make it
right.

## Which is why `skills:` was not on the list

*The fields that matter* gave you six frontmatter fields that do real
work and told you the rest was decoration. `skills:` was not among
the six. This is the reason.

Nothing in that article changes here. `tools:` is still one of the
six and still does its job — the tool list is what an agent is
allowed to do, and that part is solid. What is shaky is the
*discovery* built on top of it. Putting `Skill` in the list gives an
agent the ability to load a skill; it does not give it the instinct
to do so at the right moment. Ability is reliable. Instinct is not.

And everywhere outside that main-agent case, `skills:` behaves like
the trouble *The definition file* warned you about — a key that goes
unread, failing in silence. No error, no warning, nothing in red.
The line is right there in the file, the file loads perfectly, and
nothing anywhere tells you it did nothing.

## So leave them out?

No — write them in. On a main agent they help, they cost you
nothing, and the skill that builds skills fills them in for you
anyway. Do not treat them as the mechanism. Treat them as a hint that
may or may not be taken.

The mechanism is something else, and the Boss is happy to report it
is one keystroke.

Press `n`.
