---
id: files/terminal-editors
title: Editors in the terminal
level: Level 1
part: Files
section: Editors
order: 5
summary: Nano and micro behave the way you already expect; vim, neovim and helix trade discoverability for speed you do not need
keywords: [nano, micro, vim, neovim, helix, emacs, terminal editor, modal editing]
---

# Editors in the terminal

*v0.2.0*

An IDE is a program you open. A **terminal editor** is a program you
run — typed at the same prompt as everything else, filling the same
window, closed the same way you close anything else there: finish,
and it hands the terminal back.

## The two that behave the way you expect

**Nano** and **micro** open a file, put the cursor where you would
expect, and let you type, delete and arrow-key around it exactly as
in any text box you have used before. Save with a shortcut printed at
the bottom of the screen; there is nothing to learn beyond that.
Micro is the newer of the two and adds a few conveniences — mouse
support, `Cmd`-based cut and paste — that make it feel closer still
to what you already know.

## The ones that do not

**Vim**, **Neovim** and **Helix** open a file and refuse to let you
type into it. Press a letter and, more often than not, it runs a
command rather than inserting the character — you ask for insertion
explicitly, then ask to leave it again. That is not a missing
feature; it is the whole design. Every action — move ten words on,
delete to the end of a line, replace every instance of one — is a
short sequence of keys typed without lifting your hands off the
letters, and once learned it is faster than reaching for a mouse, or
even for arrow keys, ever again.

The trade is real, and none of it is discoverable — the difficulty of
*GUI and TUI*, sharpened. Each survives because people who write code
all day type in it for years and never go back. That cost buys speed
you have no structural reason to pay for, given the amount of
hand-editing this course actually asks of you.

## Emacs

**Emacs** takes the opposite route from Vim toward a similar
destination: not modal, but built to be endlessly extended and
configured, to the point that some people run their whole working
life — mail, notes, a calendar — inside it. It is closer to a way of
working than an editor, and adopting it is not a decision this course
is asking you to make.

## What to actually reach for

When Claude Code hands you a file to glance at, or opens one for a
quick edit of your own, reach for **nano** or **micro**. Neither asks
anything of you that you have not already done in every text box you
have ever used, and neither is the point of this course — Claude Code
is the one doing the writing. An editor here is for looking, and
occasionally nudging, not for living in.

The next section is version control — what git actually is, and why
every file in this course being plain text is what makes it possible
at all.

Press `n`.
