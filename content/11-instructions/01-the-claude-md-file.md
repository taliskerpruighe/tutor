---
id: instructions/claude-md
title: The CLAUDE.md file
level: Level 2
part: Instructions
section: The CLAUDE.md File
order: 1
summary: Claude collects every CLAUDE.md walking up at startup, then reads one again the moment it reaches that folder
keywords: [claude.md, standing instructions, walk-up rule, startup, subdirectory, project, global, folder, disclosure, mid-session]
---

# The CLAUDE.md file

*v0.2.1*

A `CLAUDE.md` file is the standing instructions an agent reads
before it does anything else, and it is nothing stranger than an
ordinary markdown file sitting in a folder.

The one that reaches every session on the machine lives at
`~/.claude/CLAUDE.md`, inside your home folder. It is not the only
one there will ever be, either — *More .claude directories* already
put a name to that: one per folder, as many as you like.

What neither of those articles covered is how a session actually
finds the ones that apply to it. There are two separate ways, and
the second is the one worth slowing down for, because it will not
occur to you on your own.

## At startup

*What a session sees* already set out the mechanism for `.claude`
directories in general: Claude starts in the folder you launched
from and walks up through the parents, collecting every one it
passes, all the way to your home folder. Apply that rule to
`CLAUDE.md` specifically and nothing about it changes — every
`CLAUDE.md` on that upward path is read before you have typed a
word, and all of them apply together, not only the nearest.

## Whenever it goes near the folder

That covers launch. It does not cover the rest of the session, and
this is the part that will surprise you the first time you see it
happen.

The moment Claude reads or edits a file inside a folder that carries
its own `CLAUDE.md`, that file loads too — there and then,
mid-session, whether or not the folder was ever on the walk-up path.

Say a matter folder holds a `disclosure/` subfolder with a
`.claude/CLAUDE.md` of its own, instructing any agent working in
there to flag privileged material before quoting it. You launch from
the matter folder itself, above `disclosure/`. At startup, the
walk-up rule never sees that instruction — `disclosure/` sits below
you, not on the path up, exactly as *What a session sees* ruled out.
Ask Claude to open a document inside `disclosure/` twenty minutes
later, in the same session, and its `CLAUDE.md` reads itself in
right then.

```
  matter/
  ├── .claude/CLAUDE.md
  │     read at launch, on the walk up
  └── disclosure/
      └── .claude/CLAUDE.md
            read only once a file inside
            disclosure/ is opened
```

Nothing about that second load depends on distance, or on whether
you remembered the subfolder existed. It depends only on Claude
touching a file that lives there.

## Both apply at once

A single session can be carrying instructions collected two
different ways at two different times: the ones gathered at launch,
sitting in context from the first word, and the ones a subfolder
adds later, the moment work actually reaches it. Neither cancels the
other. The `CLAUDE.md` inside a folder is never truly out of reach —
only delayed until Claude goes there.

Press `n`.
