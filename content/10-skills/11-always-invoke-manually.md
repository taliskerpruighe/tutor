---
id: skills/invoke-manually
title: Always invoke manually
part: Skills
section: Making Them Fire
order: 11
summary: Party Trick #5 — type a slash, pick the skill off the list, and it fires every time.
keywords: [party trick, picker, slash, invoke, manually, custom-skills, tutor, visible, location]
---

# Always invoke manually

*v0.1.0*

> **Party Trick #5 from the Boss: always invoke skills manually.**
> Never wait for a skill to fire by itself. Type `/`, pick it off the
> list, and write your instruction after it. It fires every time, on
> whichever agent you are talking to.

The diagnosis was long. The fix is one character.

## The picker

Start a session with whichever agent you want — the default one, or
one you built:

```bash
cd ~/tutor && claude
```

Then, on an empty prompt, type a single forward slash:

```
/
```

A list opens underneath. It holds the built-in commands and — the
part that matters here — **every skill this session can see**. Keep
typing to narrow it down, or arrow through it. Choose one and it
drops onto your prompt line. Then type what you actually want, after
it, and send.

## What that looks like

Four lines, each one a whole prompt:

```
/custom-skills build me one for LBAs
/custom-agents one that reads disclosure
/tutor what does context rot mean
/letter-before-action one for Hartley
```

The first two are the skills wired into this folder — one builds a
skill, one builds an agent. The third is the skill answering from
these articles. The fourth is yours: a letter-before-action skill you
wrote, told to go and write one.

What you should see next is the reply opening by naming the skill it
has loaded, and then the work starting under that skill's
instructions rather than under Claude's own habits. `/custom-skills`
begins the interview. `/tutor` answers from the course. The last one
produces a letter in your house shape, because that is what you told
it the shape was.

No guessing about whether it fired. You watched it fire.

## It also tells you what is visible

There is a second use for that list, and it is worth the two seconds
it takes.

**If a skill is not in the picker, this session cannot see it.** Not
broken, not badly written — out of reach. Either the skill sits in a
folder this session never walks up through, or you started the
session somewhere other than where you thought. That is *Location
matters* turning up again, and the cure is the same: launch from the
right folder, or move the skill to one that covers you.

One other thing can hide a skill: it only appears in the list if it
was marked user-invocable when it was written. The skill that builds
skills sets that for you, so this is really only a thing to check on
a skill that came from somewhere else.

Check the picker first. It is faster than debugging a skill that was
never there.

The picker only tells you once you have started. The next article is
the line already on your screen that would have told you before.

Press `n`.
