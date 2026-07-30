---
id: linux/you-are-the-system
title: You are the system
part: Interface
section: Linux
order: 15
summary: Every layer of a Linux machine is a choice you make — and Claude Code is what makes making that choice practical.
keywords: [linux, window manager, desktop environment, wayland, x11, init, customise, sway, gnome]
---

# You are the system

The packages article showed the terminal replacing apps: `diff` instead
of tracked changes, `pandoc` instead of a conversion tool. That is real
power, and it has a ceiling. On your Mac, the operating system
underneath all of it stays closed. You can replace what runs on top of
macOS. You cannot replace macOS.

You cannot swap out how windows are managed. You cannot change what
draws the login screen. You cannot alter how the machine boots. Those
are Apple's decisions, shipped once, and no terminal command reaches
that far in.

## On Linux, every layer is a decision

Because it is open source top to bottom, none of those layers is fixed.
Each one is a separate piece of software, and each has competing
options built by different people with different opinions — you pick.

| Layer | What it does | Some options |
|---|---|---|
| Display protocol | pixels reach the screen | Wayland, X11 |
| Window manager | arranges and draws windows | Sway, Hyprland, i3 |
| Desktop environment | the whole desktop, or none | GNOME, KDE, none |
| Shell | your typed interface | zsh, fish, bash |
| Terminal | the window the shell sits in | Ghostty, Alacritty, kitty |
| Init system | what starts first at boot | systemd, runit |
| Package manager | how software arrives | apt, dnf, pacman |

None of these is a plugin or a setting buried in a preferences pane.
Each is a real, independent piece of software installed in place of
another, and the combinations behave differently enough that people
have genuine, argued preferences about the whole stack.

## The consequence

A Mac is shaped the way a product manager guessed you work. A Linux
machine ends up shaped the way you actually work, because every layer
that disagreed with you was replaceable.

## Why this used to not happen

None of this was ever secret. It cost a weekend of forum posts per
decision — reading which window manager other people preferred, editing
a configuration file in a syntax invented for exactly that program, and
finding out what broke. Most people, reasonably, did not spend the
weekend.

That cost is what Claude Code removes. You do not read the forum posts
or learn the config syntax. You say what you want the machine to do, in
plain English, and it finds the file, edits it, and tells you what
changed. *"Make the terminal launch full screen and move the clock to
the other side"* is a sentence, not a research project.

That is the reason this subsection sits inside a Claude Code course at
all. Knowing Linux exists is background. Being able to ask for what you
want from it is the actual point.

---

That is Interface. Setup is next — what Claude Code actually is, and
where it lives on your machine.

Press `n`.
