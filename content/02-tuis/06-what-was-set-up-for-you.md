---
id: tuis/ghostty-defaults
title: What was set up for you
level: Level 1
part: TUIs
section: Ghostty
order: 6
summary: Someone else chose your colours and your font before you ever opened Ghostty, and none of it is permanent
keywords: [ghostty, config, catppuccin, theme, monospace, font, transparency, title bar, bell]
---

# What was set up for you

*v0.2.0*

You did not configure Ghostty. Someone did it for you, before you ever
opened it, and *Your terminal is Ghostty* said the defaults were sane
without saying what they were.

## What is actually set

- **A dark colour scheme, called Catppuccin Mocha.** Soft, low contrast,
  built to be looked at for hours rather than minutes. It is one of a
  family of themes with the same name and different backgrounds; this
  is the darkest of them.
- **A monospace font called Hack.** *Monospace* means every character —
  `i` and `m`, `.` and `W` — takes exactly the same width. An ordinary
  font does not do this; it narrows an `i` and widens a `w` so a line of
  prose looks even. A terminal cannot afford that: this reader lines up
  columns and draws tables, and none of it holds together unless every
  character occupies the same width as every other one.
- **A little transparency.** The window is very slightly see-through.
  It changes nothing about how the terminal behaves; it is there
  because a solid black rectangle covering half the screen is a harder
  thing to live next to than a slightly soft one.
- **No title bar.** Deliberate, not a fault. You lose the strip of
  space a title bar would have taken and gain nothing you were using —
  the tab itself already tells you what is open.
- **The bell turned off.** Terminals traditionally beep, flash, or
  bounce in the dock when a program wants your attention. Ghostty does
  none of that here. If you have ever worked next to someone whose
  terminal beeps, you know exactly what was switched off and why.

## None of it is fixed

Every setting above lives in one plain text file, and none of it is
owed to the person who wrote it. If the text is too small, the colours
are wrong, or you want the title bar back, that is a sentence to Claude
Code — *"make the Ghostty font bigger"* — not a settings hunt through a
menu you have never seen. It will find the file, make the change, and
tell you what it changed.

The same is true one layer up, of the line you type into rather than the
window it appears in: *Starship*, in *The CLI*, covers changing your
prompt the same way — by describing the outcome and letting Claude Code
find the setting.

Ghostty is the window.

Press `n`.
