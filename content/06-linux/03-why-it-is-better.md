---
id: linux/why-it-is-better
title: Why it is better
level: Level 1
part: Linux
section: Why its better
order: 3
summary: Faster, safer by construction, and honest about what it lacks — before the article that makes the real case.
keywords: [linux, performance, security, virus, privacy, tui, claude code]
---

# Why it is better

*v0.1.0*

Better is doing some work in that title. Better at some things, and
this article says which — and then what it costs — because the real
case for Linux is not any of these. It is *You are the system*.

## Lighter

A fresh install runs close to bare kernel plus what you asked for.
There is no vendor dashboard checking in, no trial software you never
launched, no background process updating an app you deleted months ago.
The consequence shows up on old hardware most clearly: a ten-year-old
laptop that struggles under Windows or macOS can run Linux at a
perfectly reasonable clip, because nothing is running that you did not
put there.

## Effectively no viruses

Not zero, but close enough that most Linux users never install
antivirus software at all. Three things earn that, not luck:

- **Small desktop share.** Malware is written for the largest audience,
  and Windows is that audience.
- **A stricter permissions model.** Ordinary programs cannot touch
  system files without you explicitly granting it, each time — not a
  box ticked once during setup and forgotten.
- **Signed repositories.** A package manager installs from a list its
  maintainers control and cryptographically sign. You are not
  downloading an installer from whichever website ranked first.

## Private

Nothing phones home unless you told it to. There is no company on the
other end of your desktop collecting telemetry by default, because
there is no company — an open source project has no product team
deciding what to collect.

## Built for exactly what you are doing right now

You are reading this in a TUI — a program that lives entirely in the
terminal. Linux is where that style of software is native, not ported
in. The terminal is the primary interface there, not a fallback for
when the graphical one is inconvenient, and much of what Claude Code
touches — the shell, the packages from *Packages*, the editors
developers reach for — was built on Linux first and adapted to macOS
and Windows afterward.

## What is worse

Be honest about the other side. Some commercial software does not
exist for Linux at all — no Word, no Acrobat, no Adobe suite. Some
hardware needs coaxing a Mac never asks for: a printer driver missing,
a fingerprint reader unsupported, a webcam that only half works. None
of that is really an argument for Linux, and that is not what is coming
next.

The actual point is not speed, or safety, or privacy. It is what you
get to decide.

Press `n`.
