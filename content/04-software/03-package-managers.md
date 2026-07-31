---
id: software/package-managers
title: Package managers
level: Level 1
part: Software
section: Packages
order: 3
summary: The one program that finds a package, checks it is genuine, fetches everything it needs, and keeps the lot working
keywords: [package manager, homebrew, dnf, apt, pacman, dependency, repository, signed, update, linux]
---

# Package managers

*v0.2.0*

`brew install pandoc` looks like a download. It is closer to a
negotiation, carried out by a **package manager** — a program whose
entire job is finding packages, fetching them, and keeping them
working.

## More than downloading

Three things happen behind that one line, none of them optional.

**It checks the package is genuine.** A package manager installs from a
**signed repository** — a list its maintainers control and
cryptographically sign — rather than whichever website ranked highest
in a search. You are not trusting an installer you found; you are
trusting a list someone is accountable for.

**It resolves dependencies.** Pandoc needs other packages to run, and
those need others in turn. Fetching one by hand would mean fetching
them all, in the right order, and noticing when two of them disagree
about which version of a third they want. The package manager works
that out and fetches the whole tree, silently.

**It remembers what it installed.** Every package on the machine came
in through the same manager, so it can list all of them, and update all
of them, in one command — rather than the fifteen separate "update
available" dialogs a machine full of individually installed apps
produces.

## On a Mac, it is Homebrew

macOS does not ship with a package manager. Nothing does the three jobs
above until you install one, and the one nearly everyone installs is
**Homebrew** — which is what the rest of this part is about.

## On Linux, it is chosen for you

A Linux machine, by contrast, always has one, because it is how the
operating system itself is built and kept up to date — not an add-on
bolted onto a finished machine, but the mechanism the machine was
assembled from. Which one depends on which distribution: `dnf` on
Fedora, `apt` on Debian and Ubuntu, `pacman` on Arch. You do not choose
it any more than you chose Homebrew's design — the distribution chose
it, before you ever sat down at the machine.

That difference — a package manager as an afterthought against a
package manager as the foundation everything else is built from — is
worth holding on to. It is exactly the shape of the bigger comparison a
later part draws between how a Mac is put together and how Linux is.

Homebrew is what you have, so Homebrew is where the rest of this part
goes.

Press `n`.
