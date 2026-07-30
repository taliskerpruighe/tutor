---
id: shell/starship
title: Starship and powerline themes
part: Interface
section: The Shell
order: 10
summary: What draws your prompt, why it needs a special font, and how to have it restyled.
keywords: [starship, powerline, theme, nerd font, colours, toml, customise]
---

# Starship and powerline themes

The previous article said a prompt is a template you can edit. That is
true, and writing one by hand is genuinely unpleasant. The templates are
written in a cryptic little language of percent signs and escape codes, and
a prompt that shows anything interesting quickly becomes something nobody
wants to maintain.

So people stopped writing them. Instead the prompt runs a program.

## Powerline themes

The style you have seen — a prompt in coloured blocks, each one a
different shade, fitting together left to right like a strip of film — is
called a **powerline** theme.

It came from a plugin for a text editor, and the look caught on far beyond
it. The blocks are **segments**. Each segment is one fact: the folder,
the branch, the language version, the time. They only appear when they
apply, so the prompt is longer in a project folder and short outside one.

There is a catch, and it explains a detail of your setup. The seam between
two segments is drawn with a solid arrow-shaped character that no ordinary
font contains. Someone has to add it. **Nerd Fonts** are ordinary fonts
with a few thousand of these extra symbols bolted on — arrows, folders,
logos, brackets — and that is why your terminal is set to a font called
*Hack Nerd Font* rather than plain Hack. Without it the seams would render
as empty boxes.

## Starship

The program drawing your prompt is **Starship**.

It works with any shell — zsh, bash, fish, all of them — which is unusual
and part of why it won. It is quick enough that you will never see the
prompt lag behind you. And it is configured in one readable file rather
than in escape codes:

```
~/.config/starship.toml
```

Everything is a module. There is a module for the folder, one for the
version control state, one for each language it knows, one for how long
the last command ran. Each has its own colour, its own symbol, and its own
rule for when to show itself.

Out of the box it shows what is relevant and hides what is not. That is the
behaviour you are seeing.

## Changing it

You do not need to learn the file.

Somebody set your machine up with an agent that knows how to do this. Open
a new Ghostty window with `Cmd-N` and run:

```
cd ~/retirement_101:setup && claude
```

Then say what you want, in plain English. New colours. A different palette
entirely. A shorter prompt, or a longer one. Something moved from the left
side to the right. It will make the change and you will see it in your next
new tab.

> Worth knowing that this is the pattern, not a special case. Most of what
> follows in this course is the same move — describe the outcome, let the
> agent produce the file. The reason to understand `starship.toml` is to
> know what to ask for, rather than to type it yourself.

Press `n`.
