---
id: shell/why-it-is-powerful
title: Why the shell is powerful
part: Interface
section: The Shell
order: 7
summary: Clicking does one thing at a time; a typed command does a thousand, from anywhere.
keywords: [power, glob, pipe, find, grep, batch, wildcard]
---

# Why the shell is powerful

Clicking is one thing at a time.

That sounds obvious enough to skip past, so sit with it. To rename thirty
files, you rename one, then the next, then the next. To find which
document mentions a client's name, you open documents until you find it. To
copy last month's invoices out of twelve folders, you visit twelve folders.
The mouse has no way to say *all of them*, and no way to say *the ones
that*.

A typed command says both by default.

## You do not have to go there first

The mouse can only act on what is in front of it, so every task starts with
navigation. Open the folder. Then the subfolder. Then scroll.

A command takes the address as part of the sentence. You can be anywhere:

```
ls ~/Documents/invoices
```

That lists a folder you are not standing in and did not open. Nothing was
navigated. And a command can name several places at once, so *going there*
stops being a step at all.

## The examples worth seeing

Find every PDF anywhere under your home folder, however deeply buried:

```
find ~ -name '*.pdf'
```

Find which files mention a name, without opening any of them:

```
grep -ril "acme corp" ~/Documents
```

Rename is the one that lands hardest. Every file ending `.txt`, at once:

```
for f in *.txt; do mv "$f" "${f%.txt}.md"; done
```

Three files or three thousand — the command is the same length, and takes
about as long to type.

## Things joined to other things

The real multiplier is that commands connect. The `|` character — a
**pipe** — takes what one command produced and feeds it to the next:

```
ls ~/Downloads | grep invoice
```

List the folder, keep the lines mentioning "invoice". Two ordinary
commands, joined, doing something neither does alone. You can keep going:
filter that, count it, sort it, write it to a file.

This is the thing GUIs cannot do. Buttons do not compose. There is no way
to plug the Finder's search into Preview's print dialog. Commands were
designed from the start to be plugged into each other, and almost every
impressive thing you will see done in a terminal is that trick, repeated.

> You are not expected to have absorbed any of that syntax. `${f%.txt}` is
> not obvious and was never meant to be. What matters is knowing the shape
> of what is possible — *"could I rename all of these at once?"* — because
> the answer is nearly always yes, and Claude Code can write the line.

Press `n`.
