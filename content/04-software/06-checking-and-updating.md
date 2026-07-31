---
id: software/checking-and-updating
title: Checking and updating
level: Level 1
part: Software
section: Homebrew
order: 6
summary: One command a week finds everything out of date and brings it current, instead of fifteen separate update dialogs
keywords: [homebrew, brew list, brew search, brew outdated, brew update, brew upgrade, brew doctor, updates]
---

# Checking and updating

*v0.2.0*

Four commands cover nearly everything you will ever ask Homebrew to do
beyond installing something.

## Finding out what is there

```
brew list
```

Lists every formula and cask Homebrew has installed — the whole running
total of what you asked for, going back to the day you set it up.

```
brew search pandoc
```

Searches for a package by name, whether or not you have it. Useful
before an install, to check the spelling exists and see near matches —
`brew search pdf` turns up several tools this course has already
mentioned.

## Keeping it current

```
brew outdated
```

Lists everything Homebrew manages that has a newer version available.
Nothing changes yet — this only reports.

```
brew update
```

Updates Homebrew's own list of what the latest version of everything
is. It does not touch anything on your machine; it refreshes what
Homebrew knows.

```
brew upgrade
```

Installs the newer versions `brew outdated` found, for everything at
once. Run `brew update` first so it is working from a current list, and
then `brew upgrade` does the rest unattended.

## When something is wrong

```
brew doctor
```

Checks Homebrew's own setup for problems — a broken link, a permission
it should have and does not, a leftover file from something removed
badly — and lists exactly what it found and how to fix each one.
Nothing is fixed for you automatically. Run it when something that used
to work stops working, before assuming the package itself is at fault.

## The habit worth forming

Update everything with two lines, run together:

```
brew update && brew upgrade
```

Once a week is plenty. That replaces fifteen separate "an update is
available" dialogs, each interrupting something else you were doing,
with one line you run when it suits you — the same trade the shell
makes everywhere else in this course, applied to the software itself.

---

That is Software: what an app is built from, and the one program on
your Mac that lets you reach the pieces directly rather than through
somebody's wrapper. Files comes next — what a programming language is,
why plain text is the format that survives, and the version control
that keeps every draft you have ever written.

Press `n`.
