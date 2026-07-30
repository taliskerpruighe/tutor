---
id: terminal/what-a-tui-is
title: What a TUI is
part: Interface
section: The Terminal
order: 4
summary: An app made of text and driven by the keyboard, which is what everything was before it was made of pictures.
keywords: [tui, gui, interface, keyboard, text, mouse]
---

# What a TUI is

You already know one kind of app: the kind with windows, buttons, and
icons, which you drive by pointing at things and clicking. That kind has a
name — a **GUI**, for *graphical user interface*.

The other kind is a **TUI**: a *text user interface*. An app made entirely
of characters, drawn inside a terminal, driven mostly by the keyboard.

This reader is one. The parts along the top are not really tabs — they are
words in a row, coloured to look like tabs. The line down the middle is a
column of `│` characters. It is all text, arranged carefully.

![This reader itself, drawn entirely out of characters: the parts of the course run across the top, the articles down the left, and the article fills the rest.](images/the-reader.png)

Claude Code is one too.

## Which came first

TUIs did, by a long way. Text was all the early machines could draw. The
graphical desktop — windows, a pointer, a trash can — arrived later and was
built on top of the text one, not instead of it.

That order still shows. Underneath your Mac's desktop, the text layer is
running, unchanged in its essentials, and the terminal is the door to it.

## What the difference means in practice

| | GUI | TUI |
|---|---|---|
| Made of | pictures | characters |
| Driven by | the mouse | the keyboard |
| You learn it by | looking | being told |

That last row is the honest one, and the reason this course exists.

A GUI shows you what it can do. Every capability is a button, sitting
there, waiting to be noticed. You can learn a GUI by poking at it.

A TUI shows you almost nothing. The capabilities are commands, and a
command that nobody has told you about is invisible. This is the whole
difficulty of the terminal, and it is not a difficulty of intelligence — it
is a difficulty of *discovery*. Nobody works out `grep` by staring at a
prompt.

The upside is what you get once you have been told. A button does one
thing. A command can be aimed at one file or ten thousand, combined with
another command, saved and reused, and handed to something else to run
while you do something different. Buttons cannot be combined. Commands do
almost nothing else.

> Being told is what the Claude Code tab is for. When you know the shape of
> what you want but not the words for it, describe it in English and let the
> agent produce the command. Watching it do that is one of the faster ways
> to learn the vocabulary.

Press `n`.
