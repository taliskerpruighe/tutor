---
id: plugins/exercises
title: Exercises
part: Plugins
section: Using Them
order: 6
summary: Take something you already built, turn it into a plugin, and prove it by installing it somewhere else
keywords: [plugin, exercise, bundle-reader, bundle-read, marketplace, install, second project]
---

# Exercises

*v0.2.0*

One exercise, and it is the whole test of this part: a plugin is only
worth having if it turns up somewhere it did not start.

## The build

Use whatever you already have lying in one project's `.claude` — the
`bundle-reader` agent and `bundle-read` skill from *Step two — the
workers* are ready-made for this if you built them, but any agent or
skill you have written works just as well. Open a session in that
project and say what you want:

> *"Turn the bundle-reader agent and the bundle-read skill into a
> plugin."*

Let it write the manifest, assemble the folder, and set up a
marketplace listing for it, the way the last article described.

## The proof

Building the plugin is not the exercise. Installing it somewhere else
is. Open — or make — a second project, one that has never seen either
of these files, and install the plugin into it alone, not globally.
Then open a session there and check for both halves. The picker from
*Always invoke manually* is the fast check for the skill — type `/` in
the second project and look for `bundle-read` on the list. For the
agent, run `claude --agent bundle-reader` from that same folder and
confirm it starts.

If both answer, you have proved the point of this entire part in one
move: something built once, in one folder, now reachable from a folder
that never had it written into its own `.claude` at all.

## Then take it apart

Disable the plugin in that second project's own settings only, and
confirm the first project still has it. That is the layering from *How
a plugin works* made concrete rather than described — off in exactly
the place you switched it off, live everywhere else.

---

That is Plugins: what one is, when it earns the extra step over
writing straight into a project, what is inside it, and how installing
one is the same scope question you have been answering since *Location
matters*. Headless Sessions is next, and it is the last part of this
course — running an agent with nobody watching, and how you get its
work back out without being there for it.

Press `n`.
