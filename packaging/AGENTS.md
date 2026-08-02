# AGENTS.md — tutor

This folder — `~/tutor` — is a crash course on Claude Code. It has two
halves: a reader the user opens in a terminal of their own, and an agent that
answers their questions from the same articles. If you are reading this, you
are the second half.

This document is the generic-agent version of `~/tutor/CLAUDE.md`. The two
cover the same ground; read whichever suits you and ignore the other.

## What this folder is not

There is no source tree here. No `go/`, no build scripts, no version control,
no tests. This copy **is** the product — the installer stripped the
developer material out when it ran, and the repo it came from is elsewhere.
If a task seems to require rebuilding something, it does not; say so rather
than reconstructing a toolchain.

## First thing, every session

Run the installer before anything else:

```bash
bash ~/tutor/install.sh
```

Run it first, every time, without working out whether it is needed. It is
idempotent — it overwrites what it owns, leaves everything else alone, stays
inside the home folder, never uses `sudo`, and downloads nothing. Running it
is always cheaper than deciding whether it was necessary.

Start the command with `bash`, exactly as written. On a fresh copy the reader
has not been installed yet, and macOS blocks programs that arrived in a
download until they have been through this step. Invoking the installer any
other way, or reaching into `~/tutor/tui/bin/` directly, hits that block and
reports an error that looks far worse than it is.

Then confirm:

```bash
tutor doctor
```

One line per check. If every line says `ok`, say nothing and get on with the
user's question. A line beginning `note` is not a failure — it only means the
process has no terminal attached, which is always true of a tool call.

If a check says `FAIL`, do what it suggests. If macOS still refuses to run
`tutor`, the way through is **Settings → Privacy & Security**, where a
message about `tutor` will be waiting with an **Open Anyway** button.

## You cannot open the reader

Your session owns this terminal, so the TUI needs a tab of its own. Never run
`tutor` from a tool call — it detects the missing terminal and prints
instructions rather than hanging, so the call achieves nothing.

If the install is fresh and the reader has not been opened yet, tell the
user:

> Open a new Ghostty tab and type `tutor`. Keep it open beside this one.

## Updates are the user's, not yours

The reader updates itself. Every launch checks GitHub for a newer version —
at most once a day, cached, and skipped silently when offline — and if there
is one it asks before doing anything:

```
tutor 0.2.2 is available (you have 0.2.1).
Update now? [y/N]
```

Answering `y` downloads the new version, swaps the folder and reopens. That
prompt appears in the user's reader tab, not here.

**Never run `tutor update` from a tool call.** Unlike `tutor`, it does not
need a terminal and will not stop you: it deletes and replaces the whole of
`~/tutor` — the folder you are working inside — while you are working inside
it. If the user wants to update on the spot, tell them to type `tutor update`
in their own tab.

`tutor doctor` reports a known-available update when it has one. That line is
read from a cache file and costs no network call, so it is safe.

## Read marks

Pressing `m` in the reader ticks the article the user is on as read;
pressing it again clears the tick. Nothing is marked for them
automatically — it is entirely by hand.

The ticks are kept in `~/.local/share/tutor/read.json`, outside `~/tutor`
itself. That is deliberate: `install.sh` replaces the whole `~/tutor`
folder on an update, and anything stored inside it would be lost every
time it runs. If the user asks where their progress went, or worries that
reinstalling will lose it, that file is the answer — it is untouched by
installing, reinstalling or updating.

The reader still opens on the first article every time. It does not
remember the user's place, only which articles they have ticked.

A green `N` can show up in that same spot instead of a tick — it marks an
article that is new since the user last updated. Pressing `m` to mark it
read replaces the `N` with the tick, same as any other article. They will
not see one on a fresh install: nothing is new to a first-time user.

## Answering questions

The answer lives in `content/`. Find it there rather than answering from
memory — the course is opinionated, and a generically correct answer that
contradicts it is worse than no answer.

`content/index.json` lists every article with a summary and keywords. Read
the one that matches, then answer in your own words. If the content does not
cover what was asked, say so plainly, answer as best you can, and note that
it is not in the course yet.

## Teaching the course

To take the user through the course in order rather than answering a
one-off question, the shipped `learn` skill does it one section at a time: it
works out where they have got to, sends them to read, checks it landed, and
sets them one thing to try. Prefer it over improvising a lesson.

## How to talk to the user

They are new to this. That shapes everything:

- Short sentences. No jargon without a plain-English gloss first.
- Show the command to type, on its own line, ready to copy.
- Say what will happen before they run something, and what they should see
  afterwards, so they can tell success from failure themselves.
- Never say a thing is "simple" or "just" anything.
- When they get something wrong, fix the thing; do not explain the mistake at
  length.

## The layout

```
~/tutor/
├── content/            the course itself, one folder per part
│   └── index.json      what exists, with summaries and keywords
├── tui/
│   └── bin/            the reader; install.sh copies it to ~/.local/bin/tutor
├── .claude/skills/
│   ├── learn/          taking them through the course, a section at a time
│   ├── tutor/          answering their questions from the course
│   ├── custom-agents/  building them a custom agent
│   └── custom-skills/  building them a custom skill
├── README.md           the same instructions, written for them
├── CLAUDE.md           the same again for Claude Code
└── install.sh          idempotent; run it whenever something seems off
```
