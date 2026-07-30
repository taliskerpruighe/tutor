# tutor

A crash course on Claude Code, delivered two ways from one
corpus: a wiki-style TUI you read in your own terminal, and a Claude Code
skill that answers your questions from the same articles.

This is the source repo. What you receive is `dist/tutor.zip`, built by
`bin/build-dist.sh`.

## Setup

You need Go to build the reader; running it needs nothing at all, which is
the point. The Mac it runs on need not be a developer machine, so anything
that reached for `python3` would set off a 1 GB Command Line Tools download
before a single word of the course appeared.

```bash
sh bin/build-tui.sh             # cross-compile both macOS binaries
./bin/tutor-host                # run it here (needs a real terminal)
./bin/tutor-host index          # build content/index.json
./bin/tutor-host doctor         # check an installed copy
```

The same programme also exists in Python under `tui/`. It is not a fallback —
it is the reference implementation `bin/parity.sh` diffs the Go build against,
which is the only way to verify macOS binaries on a machine that cannot run
them.

```bash
sh bin/parity.sh                # both renderers, both screen composers, and
                                # both index.json builds — every article,
                                # width and window size
```

## Usage

**Add an article** — drop a markdown file into `content/NN-part/NN-title.md`
with frontmatter (`id`, `title`, `part`, `order`, `summary`, `keywords`, and
optionally `section` to group it with its neighbours in the sidebar). The
index rebuilds itself; there is no build step.

**Preview without a terminal:**

```bash
./bin/tutor-host render content/01-interface/02-how-to-read-this.md 72
./bin/tutor-host frame 80 24 shell/packages
```

**Build the archive to send:**

```bash
sh bin/build-dist.sh
```

You unzip it into your home folder, run `bash ~/tutor/install.sh`, and then
`tutor` from a new tab.

See `CLAUDE.md` for the markdown subset the renderer supports and the
architecture decisions behind it.

## Contributing

This repo runs GitHub flow. Work happens on short-lived `spike/NNN` branches
A/B'd against the trunk, `tori`, then merged or discarded; every spike gets an entry in
`devlog/SPIKES.md`.
