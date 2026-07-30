# tutor

A crash course on Claude Code, delivered two ways from one corpus: a
wiki-style TUI you read in your own terminal, and a Claude Code skill that
answers your questions from the same articles.

This is the source repo, and it is also what a reader receives: the
repository is public, and a reader downloads it from GitHub into `~/tutor`
and runs `install.sh`, which strips out the version control and authoring
machinery on the way in.

## Setup

You need Go to build the reader. Running it needs nothing at all, which is
the point: the Mac it runs on need not be a developer machine, and anything
that reached for `python3` there would set off a 1 GB Command Line Tools
download before a single word of the course appeared.

```bash
sh bin/build-tui.sh             # cross-compile both macOS binaries
./bin/tutor-host                # run it here (needs a real terminal)
./bin/tutor-host index          # build content/index.json
./bin/tutor-host doctor         # check an installed copy
```

The same programme also exists in Python under `tui/`. It is not a fallback —
it is the reference implementation `bin/parity.sh` diffs the Go build
against, which is the only way to verify macOS binaries on a machine that
cannot run them.

```bash
sh bin/parity.sh                # both renderers, both screen composers, and
                                # both index.json builds — every article,
                                # width and window size
```

If parity reports a difference, the Go side is wrong until proven otherwise.
Changing the Python to make a diff disappear defeats the point of having it.

## Layout

```
content/            the course; one folder per part, plus a generated index
  └── _pipeline/    raw authoring notes — gitignored, never published
go/                 the reader, in Go — this is what ships
tui/                the same reader in Python — the parity oracle
.claude/skills/     the four skills that ship with the reader's copy
packaging/          the three root documents that ship, replacing these ones
bin/                build, parity and preview scripts
devlog/             the durable record of spikes
```

## Usage

**Add an article** — drop a markdown file into `content/NN-part/NN-title.md`
with frontmatter (`id`, `title`, `part`, `order`, `summary`, `keywords`, and
optionally `section` to group it with its neighbours in the sidebar). The
index rebuilds itself; there is no build step.

Keep each section to nine articles or fewer. The number keys `1`–`9` are the
only way to jump straight to an article, and they count within whatever list
is on screen.

The renderer implements a deliberate subset of markdown, not all of it —
headings, paragraphs, fenced code, inline code, bold, italic, lists,
blockquotes, rules, links and pipe tables. Anything outside that renders as a
plain paragraph. Code blocks are clipped rather than wrapped, so keep lines
readable at 60 columns.

**Preview without a terminal:**

```bash
./bin/tutor-host render content/01-interface/02-how-to-read-this.md 72
./bin/tutor-host frame 80 24 shell/packages
```

**How a reader installs it:** download this repository from GitHub into
their home folder as `~/tutor`, run `bash ~/tutor/install.sh`, then `tutor`
from a new tab.

## What ships, and what does not

The reader gets the whole repository, so the trimming happens on her machine
rather than here: `install.sh` prunes the developer-only material after
installing the launcher and before building the content index, so the index
is built from the tree she keeps.

It removes `go/`, `bin/`, `devlog/`, `content/_pipeline/`, `.github/`,
`tui/*.py`, `tui/__pycache__`, `.dvc/`, `.dvcignore`, `.gitignore` and
`.claude/settings.json`. Stripping the Python reader is the one that
matters, so nothing in the reader's home folder can reach for `python3`.
Every step is `rm -rf`/`-f`, so re-running the installer is safe.

The three documents in `packaging/` — `CLAUDE.md`, `AGENTS.md` and
`README.md` — are copied over the three at this root, and `packaging/` is
then deleted. An agent sitting in the reader's `~/tutor` should read
instructions about installing and using the course, not about spike branches
and renderer internals.

`tui/bin/` holds the two macOS binaries and is committed on purpose. The
reader downloads the repository as it stands; without them, that download
would be source code rather than a working reader.

See `CLAUDE.md` for the full architecture notes: the code-signing gate, the
quarantine workaround in `install.sh`, why `glow` and `bat` were rejected,
and how sections are derived rather than stored.

## Contributing

This repo runs GitHub flow. Work happens on short-lived `spike/NNN` branches
A/B'd against the trunk, `tori`, then merged or discarded; every spike gets
an entry in `devlog/SPIKES.md`. A discarded spike's commits vanish with its
branch, which is what the devlog exists to outlive.

The repo is public and its history was squashed to a single commit before it
became so. Assume anything committed here is readable by anyone.
