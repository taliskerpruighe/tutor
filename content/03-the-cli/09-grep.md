---
id: zsh/grep
title: grep
level: Level 1
part: The CLI
section: Zsh
order: 9
summary: A glob finds files by name; grep finds them by what is written inside, line by line
keywords: [grep, search, pattern, flag, recursive, case-insensitive, regex, contents, line]
---

# grep

*v0.2.9*

Contents are what a glob cannot see. **grep** reads a file line by line
and prints every line containing the pattern you gave it — a search
inside the file rather than a match against its name.

Given a folder instead of a file, the difference between finding a
document and reading every one of them by hand is the whole reason to
learn this. The name is short for *global regular expression print*, a
sentence nobody needs to remember to use it well.

## The shape of a search

```
grep "without prejudice" letter.md
```

Prints each line in `letter.md` containing that phrase, with nothing else
in the file shown. Point it at a folder with `-r` to search recursively,
every file underneath it, not just the one named:

```
grep -r "without prejudice" ~/Documents/okonjo
```

## The flags worth knowing

- **`-i`** — ignore case, so `Acme` and `acme` both match.
- **`-l`** — list only the filenames that matched, not the lines. Faster
  to scan when you want *which* document, not *where*.
- **`-n`** — print the line number alongside each match, useful the
  moment you need to open the file and go straight there.
- **`-v`** — invert the match: every line that does *not* contain the
  pattern.

These combine. `grep -rli "acme corp" ~/Documents` finds every file
mentioning the client, case regardless, and names only the files.

## Grep on a pipe

grep never needed a file. It reads whatever arrives on the left of a
pipe just as happily, line by line — the same *pipe* from *Why the shell
is powerful*, doing here what it did there: feeding one command's output
straight into the next. Your shell keeps every command you have run this
session in a history file, and grep can search that too:

```
history | grep zoxide
```

That surfaces every `z` and `zi` you have typed, in order, without
walking back through `↑` one press at a time. Anything that produces
lines — a log, a list, another command's output — is fair game.

## Beyond a fixed phrase

grep can match a shape rather than exact text — a **regular expression** —
so `grep -E "20(2[3-9]|3[0-9])"` finds any year from 2023 to 2039. That is
a large subject on its own; a fixed phrase in quotation marks is most of
what you will ever type.

`^` and `$` anchor a match to the start or end of a line, which is the
one piece worth carrying away without the rest: `grep "^Dear"` finds
letters by their opening, `grep "regards$"` by their sign-off, and
neither will match the word sitting in the middle of some other
sentence.

grep does the job. It is not the fastest way to do it, and a folder of
real size makes you feel the difference. The next article is the
replacement almost everyone reaches for now.

Press `n`.
