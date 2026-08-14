---
id: instructions/rules
title: Rules
level: Level 2
part: Instructions
section: Rules
order: 3
summary: A rule is a single instruction kept in its own file, invisible to every session until a CLAUDE.md names it
keywords: [rule, rules, at-import, import, scope, scoping, claude.md, instruction, condition, chronology]
---

# Rules

*v0.2.1*

A **rule** is an instruction kept in a file of its own, separate
from `CLAUDE.md`, and it does nothing at all until something invites
it in.

The global ones live at `~/.claude/rules/`, one file per rule —
*Inside .claude* already named the pattern: a single instruction
changed without rewriting anything else in the directory. Every
`.claude` directory can carry a `rules/` of its own, which means
there can be more than one set on a machine at once: the rules under
your home folder, and, separately, the rules under any project.

None of that happens on its own, though. A rule sitting in `rules/`
is inert until you tell a `CLAUDE.md` to read it, and how you do
that is the rest of this article.

## The import line

The line that does it starts with `@` and gives the path —
`@rules/copy-before-edit.md`, written straight into a `CLAUDE.md`.
That line is what pulls the rule's contents into the session, at the
same moment `CLAUDE.md` itself loads.

Leave the line out and the rule file goes unread, in every session,
for as long as the line stays missing — however correct it is,
however carefully you wrote it.
Put the same import in two different `CLAUDE.md` files and the rule
reaches both of them, unedited, from the one source.

## What that buys you

A `CLAUDE.md` can carry as many import lines as it needs, one per
rule. Which sessions see a given rule comes down to nothing more
than which `CLAUDE.md` files import it, and that is the whole of
scoping.

Say you keep a rule for how you want a chronology laid out — column
order, date format, undated documents at the end. Import it from
`~/.claude/CLAUDE.md` and every session on the machine gets it, a
personal matter as much as a work one. Import it instead only from
`~/work/.claude/CLAUDE.md`, and only sessions launched under `work/`
ever see it — the walk-up rule from *What a session sees* decides
exactly who that is, and a session in your personal folder never
comes near it.

## More than one at a time

Nothing stops a `CLAUDE.md` importing several rules at once, each
handling one condition the main file never mentions. The two are not
competing for the same job — `CLAUDE.md` stays the short,
always-true summary from *CLAUDE.md tips*, and each rule handles
exactly the one condition that kept it out.

Press `n`.
