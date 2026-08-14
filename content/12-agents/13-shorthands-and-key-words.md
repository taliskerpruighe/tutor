---
id: prompt/shorthands-and-key-words
title: Shorthands and key words
level: Level 2
part: Agents
section: Prompts
order: 13
summary: A word set once in settings.json means the same thing in every prompt after it, the way a variable means the same thing in every line of a script.
keywords: [shorthand, key word, env, settings.json, variable, persistent, dollar sign, matter folder]
---

# Shorthands and key words

*v0.2.9*

You do not have to type the same phrase out in full every time. Set a
word once, and Claude Code treats it as standing for whatever you told
it to — a **shorthand**, kept in the `env` block of your `settings.json`,
global or local depending on how widely it should apply.

This works exactly like a variable in a shell script: you assign a
word to a value once, and every later line that uses the word gets the
value substituted in without being told again.

## Setting one

The same habit *Long prompts* named for `settings.json` applies here
too: ask, rather than hand-edit. *"Set a shorthand called `$BUNDLE`
that means the Mackenzie disclosure bundle folder"* is enough — Claude
Code writes the entry itself.

```json
{
  "env": {
    "BUNDLE": "~/work/mackenzie/bundle"
  }
}
```

Put it in the matter's local `settings.json` and only sessions started
inside that folder ever see `$BUNDLE`. Put it in your global one and
every session on the machine does — the walk-up rule from *Location
matters*, applied to a shorthand rather than a file. **More is worse**
still holds: a shorthand that only one matter needs belongs in that
matter, not on every session you will ever run.

## What people actually use them for

Two shapes cover most of it. The first is a folder or file you name
constantly — a bundle, a template letter, a precedents drive — so you
stop retyping a path you already know by heart.

The second is an instruction you give often, but not on every single
prompt: a tone, a formatting rule, a reminder to flag anything that
touches a particular clause. Set `$FIRM_TONE` once to the paragraph
that describes it, and drop the word into a prompt only on the
occasions it is actually relevant, rather than repeating the whole
paragraph or leaving it out of `CLAUDE.md` where it would apply to
everything.

`$CITE_CHECK` can stand for "verify every case citation against the
official transcript before relying on it" — worth invoking on a
skeleton argument, not worth carrying into every routine email.
`CLAUDE.md` is for the instruction that always applies. A shorthand is
for the one that sometimes does.

## Keep it marked

Prefix every shorthand with `$` — the Boss's habit, adopted so that a
word standing in for something never gets mistaken for a word that
happens to appear in the sentence anyway. `$BUNDLE` is unmistakably a
substitution; `bundle` on its own is ordinary English.

That one habit is the whole of the convention. Nothing else about a
shorthand is special — it is a value sitting in a settings file,
waiting to be read.

Press `n`.
