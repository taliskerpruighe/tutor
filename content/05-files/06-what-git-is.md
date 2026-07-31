---
id: files/what-git-is
title: What git is
level: Level 1
part: Files
section: Version Control
order: 6
summary: A tool that keeps every version of every file, with a note explaining why each one changed
keywords: [git, version control, commit, history, diff, draft, plain text]
---

# What git is

*v0.2.0*

**Git** keeps every version of every file, with a note attached to each
one explaining why it changed. Not a backup of the current state — the
whole sequence of states, kept on purpose.

You already do a version of this badly. `agreement-v2.docx`,
`agreement-v3.docx`, `agreement-v3-final.docx`,
`agreement-v3-final-actually.docx` — a version history, hand-rolled, with
the notes on why each one changed living nowhere but your memory of that
Tuesday. Git is that same instinct, done properly.

## The note is the point

A **commit** is one saved version plus a sentence saying why it exists:
*added the indemnity clause opposing counsel asked for*. Comparing two
files tells you what moved. The commit message is the only place that
tells you why, and six months later why is what you need.

Nothing is committed automatically. You decide when a version is worth
keeping and you write the note yourself — which means a sloppy note
(`updates`) is exactly as useless in git as it was on the filename. The
tool does not fix the habit. It only gives the habit somewhere durable
to live.

## Every version, not just the last one

Delete a paragraph on Tuesday, need it back on Friday — a folder of
files only ever shows you Friday's version. Git keeps Tuesday's too,
and every version between, so you can open the file exactly as it stood
at any commit and see it, not remember it.

A few pages back, a table of what a package replaces put git against
"drive version history" and left it there. This is what earned it the
row: cloud sync keeps the current state and a short recent history it
prunes on its own timetable. Git keeps the whole thing, indefinitely,
under your control.

## Where it works, and where it does not

Git compares versions by looking at the text inside a file, line by
line — which is why it belongs in the same conversation as *Why plain
text wins*. A `.md` file, a `.txt` file, a `.json` file: git can show
you precisely which line changed. A `.docx` or a `.pdf` is a sealed
binary parcel as far as git is concerned, so it can tell you the file
is different, never what moved inside it.

That does not rule documents out. It rules out expecting git to read
them the way it reads plain text.

## What it is not

Git is not a place your files live and not a syncing service. It does
not watch a folder and save versions as you type, the way a cloud drive
does. It is a log laid on top of a folder that is already there,
recording only the moments you tell it to.

Nor is it automatic backup. If the folder itself is destroyed and
nothing else holds a copy, the log goes with it — which is exactly the
gap the next article's remote closes.

That is the tool. The next article is the model underneath it — commits,
history and branches — and what actually happens when you run it.

Press `n`.
