---
id: zsh/globbing
title: Globbing
level: Level 1
part: The CLI
section: Zsh
order: 8
summary: A pattern stands for many filenames at once, and zsh expands it before the command you typed ever sees it
keywords: [glob, globbing, wildcard, asterisk, pattern, expansion, no matches, filename]
---

# Globbing

*v0.2.9*

*Why the shell is powerful* already showed you `*.pdf` and `*.txt`
without explaining what made them work. This is the explanation.

A **glob** is a pattern that stands for a set of filenames. `*` matches
any run of characters, including none; `?` matches exactly one; `[abc]`
matches any single character from the set inside the brackets.

None of this touches what is written inside a file. A glob only ever asks
about names — which files exist, not what they say — which is the
distinction the next two articles turn on.

## Expanded before anyone sees it

The pattern is not something `ls` or `mv` understands. zsh reads it,
finds every filename in the current folder that matches, and hands the
command a plain list of names — the program never knows a pattern was
involved at all.

```
ls draft-*.docx
```

If three files match, `ls` receives three ordinary filenames, typed out
in full, as though you had listed them yourself. `*` inside quotation
marks is not expanded — `"*.docx"` is four characters, literally, which
is how you hand a program a pattern instead of a result.

## Combining and narrowing

Character sets narrow a match without spelling out every filename:

```
mv exhibit-0[1-9].pdf ~/bundle
```

That moves `exhibit-01.pdf` through `exhibit-09.pdf` and nothing numbered
higher. `?` is for exactly one unknown character — `report-202?.md`
matches `report-2023.md` but not `report-2023-final.md`.

## Going down, not just along

A single `*` stops at the next slash — it will not walk into a subfolder
for you. zsh has a second form, `**`, that does:

```
ls ~/work/**/*.pdf
```

That finds every PDF anywhere under `~/work`, however many folders deep,
in one line — no `find`, no visiting each matter in turn. bash needs a
setting switched on before `**` behaves this way; zsh simply does it.

## When nothing matches

Here zsh and bash part ways, and it is worth knowing which one you have.
bash, finding nothing, hands the command the literal pattern as though
you had typed the asterisk yourself — silently wrong, and the command
usually fails somewhere downstream with no clue why. zsh refuses
outright:

```
zsh: no matches found: *.docx
```

Nothing runs. The failure is loud instead of quiet, which is the shell
you were given rather than the one most tutorials assume — and it is
worth knowing before you meet it for the first time mid-command, rather
than treating it as something broken.

> A pattern copied from a forum post assumes bash unless it says
> otherwise. Try it, and if zsh refuses with *no matches found* where the
> post promised a result, the pattern was never wrong — you are simply
> the shell it was not written for.

A glob narrows filenames. The next article narrows what is written
inside them.

Press `n`.
