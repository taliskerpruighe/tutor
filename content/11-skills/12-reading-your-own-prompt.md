---
id: skills/reading-your-prompt
title: Reading your own prompt
level: Level 2
part: Skills
section: Making Them Fire
order: 12
summary: The picker tells you a skill is missing after you have already started — the directory segment in your prompt can tell you before
keywords: [starship, prompt, directory segment, picker, toml, walk-up rule, location, diagnostic]
---

# Reading your own prompt

*v0.2.0*

*Always invoke manually* named two causes for a skill missing from the
picker. One was that it only appears if it was marked user-invocable.
The other was *"you started the session somewhere other than where you
thought"* — and that one you find out about only after typing `/` and
looking. This article is how to know it before you launch at all.

## What the segment shows

*Your prompt* already told you the one thing worth having on that line
is where you are. On a machine set up with Starship, the folder is
drawn as its own segment — one of the coloured blocks from *Starship
and powerline themes* — and it does not print the whole address. A path
four folders deep shortens to the last few, enough to place you without
running the line off the edge of the terminal on every command.

That shortening is worth knowing about rather than being surprised by.
It means the segment can look the same in two different folders that
happen to share a tail — `writing` under `~/work/mackenzie/drafts` reads
identically to `writing` under `~/work/okonjo/drafts` unless the segment
is wide enough to show the parent too. Glance, do not assume.

## Reading it before you launch

*Moving between folders* had you run `pwd` before `claude`, to confirm
where you are about to start a session. With the directory segment
already on your prompt, that habit costs nothing — the answer is sitting
there on the line before you type a character, in the last place you
looked before you pressed Enter.

That is the whole value of it. `pwd` answers a question you had to
think to ask. The segment answers it without your asking, which is the
difference between checking and simply having already known.

## If it is not there

Not every prompt carries it by default, and the fix is the one
*Starship and powerline themes* already gave you: open a session and
describe what you want, in plain English, rather than editing
`~/.config/starship.toml` by hand.

> *"Add the folder I am in to my prompt, and shorten it if it gets
> long."*

It writes the change, and the next tab you open shows it.

## Why this one is worth having

Every other segment on that line is a comfort — the time a command
took, whether a file has unsaved changes. This one is the difference
between an agent that walked up through the right `.claude` folders and
one that quietly did not, and by the time the picker tells you, you
have already spent a launch finding out the hard way. Put the answer
where you look anyway, and the question stops needing to be asked.

---

That is Skills — writing them, and getting them to fire when they
should. Subagents are next: how one agent hands pieces of a job to
others, how you chain agents and skills together, and how a skill fires
inside a subagent when there is no prompt to type a slash into.

Press `n`.
