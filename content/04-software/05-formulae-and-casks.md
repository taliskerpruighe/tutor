---
id: software/formulae-and-casks
title: Formulae and casks
part: Software
section: Homebrew
order: 5
summary: One kind of Homebrew install gives you a command; the other gives you a whole app with a window
keywords: [homebrew, formula, cask, brew install, ghostty, applications, command line]
---

# Formulae and casks

*v0.2.0*

Homebrew installs two different shapes of thing, and calls them by two
different names.

A **formula** is a command-line package — `pandoc`, `ripgrep`,
`tesseract`, everything in *Packages*. No window, no icon in your
Applications folder, nothing to double-click. It exists to be typed.

A **cask** is a whole Mac app. A window, a menu bar, an icon, something
you would otherwise have downloaded from a website and dragged into
Applications. Homebrew installs these too, by the same mechanism, and
tracks them the same way it tracks a formula.

## Two commands, one letter apart

```
brew install pandoc
brew install --cask ghostty
```

The only difference in what you type is `--cask`. Leave it off and
Homebrew looks for a command-line package by that name. Add it and
Homebrew looks for an app, downloads whatever it is packaged as — often
the same `.dmg` you would have got by hand — and installs it into
Applications for you.

Ghostty, your own terminal, is a cask. It has a window, it sits in
Applications, and it is exactly the kind of thing a cask exists for.
Whether yours arrived through Homebrew or by some other route before
you ever opened it, you can put the question to Homebrew directly:

```
brew list --cask
```

That lists every cask Homebrew currently manages on your machine. If
Ghostty is in it, Homebrew installed it, or has since adopted it, and
`brew upgrade --cask ghostty` will keep it current from here on. If it
is not, Ghostty arrived some other way and Homebrew has never heard of
it — which is worth knowing before you go looking for it in the next
article.

## Why the distinction exists at all

A formula and a cask are handled differently under the surface — a
formula usually compiles or links into place, a cask usually just moves
a finished app into Applications — so Homebrew needs to know which kind
of job it is doing before it starts. `--cask` is how you tell it.

The two also live in different places once installed. A formula's
files sit inside Homebrew's own folder, out of sight and out of your
way. A cask ends up exactly where any other Mac app would — in
Applications, in your Dock if you put it there, launchable the way you
already launch everything else. Homebrew is managing it, but it does
not look managed.

You will use `brew install` far more than `brew install --cask`. Most
of what this course points you towards is a command, not an app. But
the distinction is worth having before the next article, which asks
what Homebrew already has installed of both kinds.

Press `n`.
