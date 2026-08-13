---
id: zsh/fzf
title: fzf
level: Level 1
part: The CLI
section: Zsh
order: 11
summary: rg narrows a search before you look; fzf hands you the list and narrows it live as you type against it
keywords: [fzf, fuzzy finder, ctrl-r, ctrl-t, pipe, interactive, filter, history]
---

# fzf

*v0.2.9*

`rg` narrows a search before you see anything. **fzf** — the fuzzy
finder — narrows one after you are looking at it: give it a list, type a
few characters, and it filters the list live, on every keystroke, until
one line is left.

Nothing about it is specific to files. Anything that can be listed can be
filtered — history, running programs, branches, folders — and this is
the article where the whole section's habit of chaining one small
command into the next pays off hardest.

## Typing a fragment, not a phrase

"Fuzzy" means the letters need not be consecutive. Typing `okjrpt`
against a list of filenames still surfaces `okonjo-report-final.docx`,
ranked above weaker matches, with the matched letters highlighted as you
type. You are narrowing, not spelling.

## Not a rival to searching

`rg` and `grep` narrow by asking a question in advance — a pattern
written before you see a single result. fzf narrows by looking and
deciding as you go, which suits a different moment: not *"which files
mention this clause"*, but *"which of these fourteen things I am already
looking at is the one I want."*

## The two habits worth having

Set up once, fzf takes over two keys:

- **`Ctrl-R`** — fuzzy search through your command history instead of
  walking it one `↑` at a time. Type a fragment of a command you ran last
  week and it is there.
- **`Ctrl-T`** — fuzzy-find a file or folder and drop its path at the
  cursor, with no `cd` or `ls` first.

## Or feed it anything

Piped in, fzf filters whatever a command produces:

```
ls ~/Documents/clients | fzf
```

That opens an interactive list of client folders, narrows as you type,
and prints the one you pick when you press Return — the same *pipe* that
chains any two commands, doing it here with a filter you drive by hand
instead of a pattern written in advance.

The output usually goes somewhere rather than sitting on screen. Wrapped
in `$(...)`, whatever fzf prints becomes an argument to another command:

```
cd $(ls ~/work | fzf)
```

Type a few letters of the matter, press Return, and `cd` runs against
whichever folder you picked — one line doing the work of listing,
choosing and moving, none of it typed out in full.

## Getting it

```
brew install fzf
```

Then run `$(brew --prefix)/opt/fzf/install` once, which is the step that
wires up `Ctrl-R` and `Ctrl-T` — the plain install does not do it for
you.

That is the shell itself: moving through it, remembering it, searching
it, filtering it. The next article turns to the line that greets you
before any of that runs — *Your prompt*, and what it can be made to say.

Press `n`.
