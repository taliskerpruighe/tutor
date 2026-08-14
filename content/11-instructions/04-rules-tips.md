---
id: instructions/rules-tips
title: Rules tips
level: Level 2
part: Instructions
section: Rules
order: 4
summary: Import a rule only where it always applies, leave the rest unimported, and use two everyday examples to decide which is which
keywords: [rule, rules tips, at-import, scope, client folder, pdf, flatten, condition, claude.md, import]
---

# Rules tips

*v0.2.1*

A rule earns its place by being short, and by being imported into
exactly the sessions that need it, nowhere else. The first half is
*CLAUDE.md tips* again, restated for a file that only fires when
something names it: keep every rule to the one instruction it exists
for, and nothing more.

The harder question is not length. It is when a rule is the right
answer at all, instead of a line written straight into `CLAUDE.md`.

## Import what always applies, and nothing else

Use an `@`-import for a rule that is specific but always true
wherever the importing `CLAUDE.md` reaches — narrow in what it
governs, not in when it applies. Leave everything else sitting in
`rules/` unimported: a rule you reach for occasionally, on a
document you can see, in a session where you can name it yourself,
costs nothing extra until the day you actually need it.

## The real question

*CLAUDE.md tips* already drew the line in principle: an instruction
that only applies sometimes does not belong in `CLAUDE.md`, it
belongs in a rule. What decides whether that rule then gets
imported, and from where, is what the instruction is conditional on.

Take two rules from your own work, both narrow, both real.

**Make a copy of any file before you edit it — but only inside
client folders.** The condition here is location: which folder you
are in decides whether the rule applies. So the rule lives where the
location does — imported with one line inside
`clients/.claude/CLAUDE.md`, not the global one. A session under
`clients/` always gets it, whatever else is happening. A session
anywhere else never even carries the line.

**Flatten any PDF before you consider it done — regardless of which
folder it turned up in.** This one has no location to hide behind. A
PDF can land in any matter, any week, so there is no folder narrow
enough to scope it to. The condition is the file type, not the
place, so the only `CLAUDE.md` that can always catch it is the
global one — imported once from `~/.claude/CLAUDE.md`, and worth the
one line it costs every session, because nothing about where you are
ever excuses it.

Same shape both times: a rule, kept out of the main file, imported
exactly where the condition it depends on can be trusted to hold.

---

That is Instructions: one file read on every session it can reach, and
a second kind read only when a `CLAUDE.md` names it. Agents are next —
what one actually is, and how everything built in this part reaches
every one of them the moment it starts.

Press `n`.
