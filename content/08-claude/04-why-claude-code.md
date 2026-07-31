---
id: claude-code/why-claude-code
title: Why Claude Code
part: Claude
section: Claude Code
order: 4
summary: The model lives in a data centre and the harness lives on your Mac, and that split is what this article is really about
keywords: [claude code, harness, model, terminal, local, permission, taught, data centre]
---

# Why Claude Code

*v0.2.0*

Two names, easy to blur together. **Claude** is the model — the brain
in a jar from a few articles back. **Claude Code** is the harness: the
program that gives that brain hands, and the one this course actually
teaches.

## Where each one lives

|  | What it is | Where it runs |
|---|---|---|
| Claude | the model | a data centre |
| Claude Code | the harness | your Mac |

Claude Code owns the loop described two parts ago: it decides what
the model gets to see, carries out what the model asks for, and
decides what needs your permission first. The model never touches
your files directly. It only ever sees what the harness sends it, and
only ever acts through the harness sending the result back.

That split means everything touching your machine happens on your
machine. Your files are read locally. Commands run locally.
Permission is asked locally. The only thing that ever crosses the
network is text — what the model needs to see of a question, and what
it says back. And it means the heavy part is somebody else's problem:
you are not buying graphics cards or leaving a laptop running hot
overnight. The largest models Anthropic builds answer you from a
terminal window on a machine that could not begin to hold them.

## Why this one, among the harnesses

Beyond the model itself, which is a choice you make separately, four
things make Claude Code the one worth learning first.

**It is a terminal program.** No separate app to switch to, no editor
to adopt. It sits in the same window your work already happens in and
reaches the same files, with nothing standing between you and it.

**You watch it work.** Every file it reads and every command it runs
is printed as it happens, in order, on the screen in front of you.
When something goes wrong you can see exactly where, rather than
being handed a finished answer with no way back into how it got
there.

**It asks first.** Anything consequential — writing a file, running a
command that changes something — stops and waits for you before it
happens, not after.

**It can be taught.** Not once, in a settings menu, but continuously:
agents, skills and chains of them, which the rest of this course is
about, are all ways of writing down how you want a job done so you
stop explaining it from scratch every time.

That local-and-visible arrangement is also, separately, a question of
raw capability — what a machine standing inside your own files and
your own hardware can do that one sealed inside someone else's
cannot. That is the next article.

Press `n`.
