---
id: subagents/the-door
title: The door
level: Level 2
part: Subagents
section: Chains
order: 5
summary: One skill you type a slash into whose only job is to spawn the chain, with every worker skill fired by a slash command on line one of its spawn prompt.
keywords: [door, door skill, spawn prompt, slash, user-invocable, effort, chain, silent failure]
---

# The door

*v0.1.0*

*How skills work* left you with a problem. A skill fires reliably on the
agent you are talking to and nowhere else — and a **subagent does not
reliably pick a skill up**. Named in the frontmatter, sitting right there
on disk, and nothing loads it. No error either.

*Always invoke manually* solved that for the agent in front of you: type
`/` and fire the skill yourself. This article is the same trick, one level
down.

## What a door is

A **door** is a skill you invoke with `/`, whose entire job is to spawn
the chain. It does none of the work itself.

```
  /bundle
      │
      ├──►  bundle-reader        /bundle-read
      ├──►  bundle-reader        /bundle-read
      └──►  bundle-consolidator  /bundle-consolidate
```

You type one thing. The door reads its own instructions — which are a list
of spawns, in order — and puts the chain up. Its body is not prose about
what a good summary looks like; that lives in the worker skills. Its body
is the running order.

One door, one keystroke, one chain.

## The line that does the work

Here is the whole trick, and it is a formatting rule.

Every spawn prompt the door writes **opens with the worker skill's slash
command on line one**, then a blank line, then the values that spawn
needs:

```
/bundle-read

document: disclosure/2019-03-11-letter.md
```

That opener is the subagent's `/`. It fires the skill inside the subagent
exactly as your own slash does at your prompt — and it is what carries
the skill's `effort` through to the model, so the `high` you set on the
drafting skill is the depth the drafting actually runs at.

Write it any other way and you lose that. A spawn prompt that names the
skill in prose — *"use the bundle-read skill on this document"* — runs at
whatever effort the session happened to inherit, and the request is lost
**in silence**. No error, no warning, nothing in red. The work comes back
done the ordinary way. Precisely the failure *How skills work* warned you
about, one storey lower.

## Two consequences

**Every worker skill needs `user-invocable: true`.** That is the field
that makes a skill something a slash can fire, and if a skill has not got
it the door cannot reach it. It is set on everything you build, so in
practice this costs you nothing — it is just worth knowing which field is
holding the whole arrangement up. The door and every skill it fires want
to sit in one folder together, which is *Location matters* asking its
usual question about a chain instead of a single skill.

**Everything a subagent needs goes in its spawn prompt, in full.** The
first article in this part said it and the door is where it bites: the
filename, the matter reference, the deadline, the format you want back.
The subagent inherits nothing and cannot ask. A door that forgets a value
does not get a question — it gets a confident answer to a slightly
different job.

---

That is the chain, from the top of it to the keystroke that starts it.
The next section puts it in your hands: a series of exercises building a
chain of your own, agents and skills and a door, and running it.

Press `n`.
