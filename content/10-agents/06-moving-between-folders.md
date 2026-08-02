---
id: agents/moving-between-folders
title: Moving between folders
level: Level 2
part: Agents
section: Context
order: 6
summary: The walk-up rule makes the folder you launch from a decision, and cd, pwd and Tab are how you get it right
keywords: [cd, pwd, tab completion, ctrl-c, walk-up rule, exit, folder, matter, launch]
---

# Moving between folders

*v0.2.0*

`/exit` ended the last article on one line: `cd ~/work/okonjo && claude`.
That line did not get explained, because it did not need to be — *Moving
around* already gave you `cd`, `pwd`, `~`, `..`, `Tab` and `Ctrl-C`. What
changed is what getting it wrong now costs.

Before this part, launching from the wrong folder was a nuisance. Now it
is a Claude Code problem. The walk-up rule from *What a session sees*
means the folder you launch from decides everything the agent can see —
which rules it reads, which agents and skills are on its path. Land in
the wrong one and you have not just wasted a `cd`. You have started an
agent that is missing what it needed, and it will not tell you.

## The sideways move

Matters mostly sit next to each other, not inside each other:

```
~/work/
├── mackenzie/
├── okonjo/
└── hartley/
```

Moving from one to another is rarely a walk down through folders you
know. It is a step sideways: `cd ../okonjo` goes up one from wherever
you are inside `mackenzie` and straight into `okonjo`, no need to know
the full path or go via home first. `~/work/okonjo` does the same job
from anywhere, in one line, if you would rather write the whole address.

## Confirm before you launch

`pwd` before `claude`, not after. Once the agent starts it has already
walked up from wherever you stood, and finding out you stood in the
wrong place is a mid-conversation `/exit`, not a quick correction.

For a long matter path, `Tab` earns its keep here specifically: a
half-typed `cd ~/work/mack` completed for you is a path you know is
right, rather than one you typed by hand and hope you spelled correctly.
A folder name mistyped by one letter does not error — `cd` into a folder
that does not exist just fails quietly and leaves you standing where you
were, which is easy to miss if you are not the one who checked.

## What the other two are for here

`↑` brings back this morning's launch line — useful the moment you
realise you are re-opening a matter you already had open once today, and
do not want to retype the path from memory. `Ctrl-C` is the way out of a
`cd` you started typing and changed your mind about halfway through,
before it runs against the wrong folder.

Neither is new. Both matter more now that a wrong folder is not just a
wrong `ls` — it is an agent quietly working with rules and skills that
are not the ones you meant it to have.

## The habit

Before `claude`, ask where you are — `pwd`, or read it straight off your
prompt if it carries the path, as *Your prompt* said it should — and
confirm it is the matter you mean to be in. That is the whole discipline.
It takes less time to do than it took to read this paragraph.

---

That is context engineering — everything above is about the agent you
already have. The next section is about making your own: the agent every
one of those launches gives you, and where it stops being enough.

Press `n`.
