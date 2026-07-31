---
id: files/formats
title: The formats you will meet
part: Files
section: Languages and Scripts
order: 3
summary: A format is the shape plain text gets cut into, and some shapes forgive a typo while others do not
keywords: [yaml, json, toml, jsonl, parquet, format, frontmatter, settings, config, punctuation]
---

# The formats you will meet

*v0.2.0*

Plain text is the material. A **format** is the shape it gets cut
into — a set of conventions for where the commas and colons go, so a
program reading the file knows what each piece means without being
told out loud.

Five formats account for nearly everything you will meet in this
course, and each is reached for a different job.

| Format | Reached for |
|---|---|
| YAML | frontmatter, the block at the top of a file |
| JSON | settings, and most machine configuration |
| TOML | configuration meant to be hand-edited |
| JSONL | logs — one entry per line |
| Parquet | large tables of data, built for speed |

## Frontmatter, in YAML

Every article in this course opens with a block of `key: value` lines
between two `---` fences — that block is **YAML**. `id: files/formats`,
`title: The formats you will meet`: a name, a colon, a value, one per
line. Nothing to close, nothing to count. YAML is the forgiving one —
it reads structure from indentation and line breaks rather than from
punctuation that has to land exactly right.

## Settings, in JSON

**JSON** carries the same idea, name and value, with more ceremony:
curly braces round the whole thing, quotation marks round every name,
a comma between entries and none after the last one. `settings.json`,
which a later part of the course opens, is written this way, and
JSON is the unforgiving one: leave out a single comma, or add one
after the last entry, and it stops parsing altogether.

## TOML, for what you edit by hand

**TOML** does configuration's job with the punctuation JSON leans on
stripped away: section headers in square brackets, values that need
no quotation marks unless they are text. Software you are expected to
open and change yourself often picks TOML over JSON for exactly that
reason — a human editing it is less likely to break it.

## JSONL, for a running record

**JSONL** is JSON with one difference: instead of one structure
covering the whole file, each line is its own complete entry. A log
that grows by one line every time something happens — one request,
one turn of a conversation — is JSONL, because a new entry can be
appended without touching anything already written.

## Parquet, for a lot of it at once

**Parquet** answers a different problem entirely: not text meant to
be read, but a table of data running to millions of rows, stored so a
machine can pull out one column without reading the rest. You will
not open one in an editor. You will ask an agent to.

## Forgiving, and the failure neither warns you about

YAML and TOML tolerate a human hand: a spare space, a missing
quotation mark, and the file still means what you meant. JSON and
JSONL do not — get the punctuation wrong and the file stops opening
at all, which is at least honest about it.

The quieter failure sits underneath all four. None of them checks
that a name is one anything is listening for. Spell a key wrong —
`summary` as `summry` — and the file still opens perfectly. The value
just sits there, attached to a name nothing looks for, doing nothing,
telling you nothing. Skills, later in the course, are built from
frontmatter of exactly this kind, which is worth remembering before
you type one.

Reading and writing any of this needs a program to hold it open in.
That is the next two articles: which kind exists, and which one
actually suits you.

Press `n`.
