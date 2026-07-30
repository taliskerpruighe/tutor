---
id: shell/your-prompt
title: Your prompt
part: Interface
section: The Shell
order: 9
summary: The text before the cursor is a status display, and it can say whatever is useful to you.
keywords: [prompt, command prompt, cursor, path, pwd, customise]
---

# Your prompt

The line the shell prints before it waits for you is the **prompt**. It is
prompting you — asking for a command.

It is easy to read past it as decoration, or as part of the window. It is
neither. The prompt is written by your shell, freshly, every time it is
ready for you, and it can be made to say anything at all.

## It really can say anything

A shell prompt is not a fixed thing that ships with the machine. It is a
setting: a short template the shell fills in and prints. Change the
template and the prompt changes.

People have made prompts that say `$`. People have made prompts that print
the time, the weather, or a different insult on every line. There is no
technical difference between those and a useful one. The shell prints what
it is told.

Which leaves the only question worth asking: what would actually help you?

## The one thing worth having in it

**Where you are.**

Commands act on the folder you are standing in. `ls` lists *this* folder.
`rm *` deletes the files in *this* folder. Nothing else on screen makes it
obvious which folder that is — no title bar, no breadcrumb, no window to
glance at.

Without it you are working blind, and every few minutes you have to stop
and ask:

```
pwd
```

*Print working directory.* It answers the question, and having to ask is
the annoyance. A prompt that carries the answer retires the question for
good. Yours does.

## And then, gradually, more

Once the prompt is a place to put information, the habit takes hold. It is
the one thing you look at before every command, which makes it the best
display you own.

People end up putting things there they want to know without asking:

- which project folder this is, and whether it has unsaved work
- which version of a language this folder expects
- how long the last command took, when it took long enough to matter
- whether the last command failed

None of that needs adding today. It is the direction of travel: a prompt
starts as a `$` and becomes, slowly, the dashboard.

Yours already does some of it, because someone set it up for you. The next
article is what that is, and how to change it.

Press `n`.
