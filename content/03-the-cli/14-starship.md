---
id: shell/starship
title: Starship
level: Level 1
part: The CLI
section: Command Lines and Prompts
order: 14
summary: The program that draws your prompt from one readable file, with the branch and the duration already switched on before you touch it
keywords: [starship, prompt, toml, module, preset, git branch, command duration, customise, install, fish]
---

# Starship

*v0.2.9*

You already know Powerline10k stalled. **Starship** is what took its
place, and it fixed the one thing that theme could never fix: it works
with any shell — zsh, bash, fish, all of them — because it does not live
inside any of them. It is a separate, fast program that your shell calls
once per prompt, and prints whatever comes back.

Out of the box, before you have opened its settings even once, it already
shows the folder you are standing in, the branch of any Git repository
underneath you, and how long your last command took — but only once that
takes long enough to be worth knowing.

## One file, not a language of escape codes

Where a hand-written prompt is a string of percent signs and codes,
Starship reads a single file:

```
~/.config/starship.toml
```

Everything in it is a **module** — one for the folder, one for Git, one
for each language it recognises, one for command duration. Each module
carries its own colour, its own symbol and its own rule for when it shows
itself, which is why the prompt lengthens inside a project and shrinks
back outside one.

## Presets, before you build anything

You do not start from a blank file. Starship ships a set of **presets** —
complete configurations, already balanced, that you switch on with one
command rather than assembling from nothing. Trying two or three before
deciding you want something of your own costs nothing: a preset is one
line to apply and one line to undo.

## Modules on, off, and invented

Any module can be turned off — command duration, say, if a stopwatch on
every prompt is a distraction rather than a help. A module can also be
added that Starship does not ship: the Google Drive segment from the last
article is exactly this shape, not a built-in feature but something
somebody wrote and dropped into the file.

You do not need to write any of it yourself. The same sentence to Claude
Code that changes a Ghostty setting changes this one — *"add a segment
for the Python version"*, *"turn the git branch red when there are
uncommitted changes"* — and it edits `starship.toml` directly rather than
sending you off to read a manual.

## Installing it

One command installs Starship, and the same command works whichever shell
it is asked to run inside — there is no separate build for zsh and
another for bash. It adds a single line to your shell's own startup file,
and everything after that is the module list.

---

That is The CLI finished — the shell, the prompt, and everything that now
fills it. Software is next, and it opens with the plainest fact of all:
what you pay for is rarely the code itself, but the wrapper built around
it.

Press `n`.
