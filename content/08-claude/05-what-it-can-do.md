---
id: claude-code/what-it-can-do
title: What it can do that the others cannot
part: Claude
section: Claude Code
order: 5
summary: Standing inside your own machine is not only safer, it is more capable — real software and real hardware, not a fixed slice of someone else's
keywords: [claude code, claude cowork, package, homebrew, hardware, cores, sandbox, m1]
---

# What it can do that the others cannot

*v0.2.0*

The last article made the local-and-visible arrangement sound like a
matter of trust: you can see what Claude Code does because it does it
on your own machine. That same fact also makes it more capable, not
only more watchable, and this is where that argument goes.

## It uses your software

Claude Code stands inside a Mac that already has a package manager, a
shell, and whatever you have installed over the years — the world
*Packages* described. Ask it for a chronology from a bundle of
scanned PDFs and it can reach for tesseract to read the scans and
pandoc to reshape the output, pulling whichever package does the job
best, fastest and at no cost, the same way you would if you knew the
names to type.

Claude Cowork cannot do that, not because it is a worse harness but
because of where it runs. Each job opens inside a sandboxed virtual
machine that Anthropic controls, built fresh and torn down afterward,
carrying only what came installed in it. It cannot go looking through
a wider software world the way Claude Code can, because there is no
wider world inside the sandbox — only what shipped with it.

## It uses your hardware

The same difference shows up in raw speed. Claude Cowork's sandbox is
capped at four cores of processing — about half of what a base-model
2020 M1 Air shipped with. Claude Code has no cap of its own: it runs
on whatever Mac you actually own, and a heavier machine means a script
that finishes in minutes rather than an hour, with nobody's policy
deciding otherwise.

Buy a better machine and Claude Code gets faster the same day. Cowork
does not, because the ceiling was never yours to raise.

## Why this only makes sense now

Neither of these is a fact about permissions or about trust. They are
facts about which computer is doing the work, and they only mean
anything once you know what a computer like yours can already do —
which packages exist, what a package manager pulls in a single line,
what a difference in cores or memory actually costs in time. A course
that opened with this article would have been telling you Claude Code
can "use your software" before you knew what software on a Mac even
looks like underneath the icons. Now you do.

Locality bought two different things, and it is worth being precise
about which is which. The last article's case was privacy: nothing
leaves your machine that you did not send. This article's case is
capability: the same standing-inside-your-files arrangement also
means there is more of your machine for it to use. Both are true at
once, and neither depends on the other.

That is Claude settled — the models, the harnesses, what an account
costs, and why this one. What follows is getting it running: the
install, the first launch, and the folder on your disk where
everything it learns actually lives.

Press `n`.
