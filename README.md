# tutor

A crash course on Claude Code, delivered two ways from one corpus: a
wiki-style TUI you read in your own terminal, and a Claude Code skill that
answers your questions from the same articles.

This is the source repo, and it is also what a reader receives: the
repository is public, and a reader downloads it from GitHub into `~/tutor`
and runs `install.sh`, which strips out the version control and authoring
machinery on the way in.

## Getting the course

Nothing here needs to be built, installed first, or fetched from a command
line — the reader is a self-contained binary that ships inside the download.

1. Press the green **Code** button at the top of this page and choose
   **Download ZIP**.
2. Open the downloaded `tutor-tori.zip`. It unpacks to a folder called
   `tutor-tori`.
3. Rename that folder to `tutor` and move it into your home folder, so it
   sits at `~/tutor`.
4. Open Ghostty and run:

```bash
bash ~/tutor/install.sh
```

That prints what it did and takes a second or two. It writes only inside
your home folder and never asks for a password. Then open a **new** Ghostty
tab and type `tutor`.

Use the browser download rather than `git clone` or a `curl` pipeline: on a
Mac that is not a developer machine, reaching for `git` sets off a ~1 GB
Command Line Tools download before anything else can happen. The installer
already expects a browser download and handles the `com.apple.quarantine`
attribute macOS stamps on everything unpacked that way, which is why it
copies the binary with a shell redirect instead of `cp`.

From then on the course keeps itself current. Every launch checks GitHub for
a newer version — at most once a day, cached in
`~/.local/share/tutor/update-check`, and silent if the network is unreachable
— and offers to update. Answer `y` and it fetches the new tag, swaps the
folder, re-runs `install.sh` and restarts itself. `tutor update` forces the
same check immediately.

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

## The launch screen

`tutor` opens on five rows of block letters, held for five seconds
(`go/splash.go`). It is printed before the terminal goes into raw mode and
before the alternate screen, which is the whole point of it: printed there it
scrolls into shell history like any command's output and is still there to
scroll back to once the reader quits. Printing it inside the alternate screen
would wipe it on exit.

```bash
./bin/tutor-host splash 80      # print it once, no wait
sh bin/banner-preview.sh        # the same design in shell, no rebuild
```

The design is settled — every rejected letterform and colour scheme was
deleted rather than kept as an option — and the Go source wins if the preview
script ever disagrees with it. This is also the one piece of the reader that
has no Python counterpart, so `bin/parity.sh` cannot check it; it is checked
by eye.

The version shown on that screen comes from `const version` in `go/main.go`.
`version.txt` at the root is the copy `tutor update` fetches from GitHub to
compare against, and `tui/tutor.py`'s `VERSION` keeps the same number for the
parity oracle; `sh bin/build-tui.sh` refuses to build unless all three agree.
`bin/banner-preview.sh` hardcodes a fourth copy for the shell preview, and
nothing checks it automatically — eyeball it against the real splash after a
bump. Four files, one number: move all four.

Whatever `version.txt` says must have a tag behind it on GitHub, because
`applyUpdate` turns the number into a tarball URL. Tags here are namespaced by
trunk — `tori/MkI_v0.2.1`, not `MkI_v0.2.1` — which is what `updateTagPrefix`
in `go/update.go` encodes. Raise `version.txt` without cutting and pushing the
matching tag and every reader is offered an update that 404s on acceptance.

## Layout

```
content/            the course; one folder per part, plus a generated index
  ├── images/       the PNGs articles embed
  ├── pipeline.md   which part sits at which level — authoring, not content
  └── _pipeline/    raw authoring notes — gitignored, never published
go/                 the reader, in Go — this is what ships
tui/                the same reader in Python — the parity oracle
.claude/skills/     the four skills that ship with the reader's copy
packaging/          the three root documents that ship, replacing these ones
bin/                build, parity and preview scripts
version.txt         the version `tutor update` compares against GitHub
devlog/             the durable record of spikes
```

`.claude/` is committed on purpose, and the `!/.claude/` line in `.gitignore`
is what makes that possible: this machine's global excludes file ignores
`.claude/` in every repo, and a per-repo negation is what outranks it. Delete
that line and the four skills stop reaching readers, with nothing here
looking any different.

## Usage

**Add an article** — drop a markdown file into `content/NN-part/NN-title.md`
with frontmatter (`id`, `title`, `level`, `part`, `order`, `summary`,
`keywords`, and optionally `section` to group it with its neighbours in the
sidebar). The index rebuilds itself; there is no build step.

The course nests three deep. `level:` is the tab along the top — there are
two, and a level is a run of consecutive parts sharing the value. `part:` and
`section:` are both headings down the left, the part flush and its sections
indented under it, and only the part being read expands.

Keep each section to nine articles or fewer. The number keys `1`–`9` are the
only way to jump straight to an article, and they count within whatever list
is on screen.

The renderer implements a deliberate subset of markdown, not all of it —
headings, paragraphs, fenced code, inline code, bold, italic, lists,
blockquotes, rules, links, pipe tables and pictures. Anything outside that
renders as a plain paragraph. Code blocks are clipped rather than wrapped, so
keep lines readable at 60 columns.

A picture is `![a caption](images/ghostty.png)` alone on its line, PNG only,
from `content/images/`, and under 500 KB — a test enforces the size, because
the reader downloads the whole repository. Anything else on that line and it
is not recognised at all. Pictures show only in Ghostty; elsewhere, tmux
included, the alt text is all that survives, so write it as a sentence that
stands on its own rather than a label. Heights are never stated: both
renderers work the space out from the picture's own proportions, which is how
parity keeps agreeing on it.

**Preview without a terminal:**

```bash
./bin/tutor-host render content/01-this-wiki/04-how-to-read-this.md 72
./bin/tutor-host frame 80 24 shell/packages
./bin/tutor-host splash 80
```

**How a reader installs it:** download this repository from GitHub into
their home folder as `~/tutor`, run `bash ~/tutor/install.sh`, then `tutor`
from a new tab.

## Read marks

Pressing `m` on an article ticks it as read; pressing it again clears the
tick. The one file that records this lives outside `~/tutor` entirely, at
`~/.local/share/tutor/read.json` — a sorted set of article ids under a
`"read"` key, next to the `home` pointer file `install.sh` already writes
there. It has to live outside the repo folder: `applyUpdate`
(`go/update.go`) renames that whole folder aside and deletes it on every
update, so anything kept inside would not survive one. The set is keyed on
article `id`, not `path`, so renumbering a directory never costs anyone
their marks — this release moved `content/08-claude/` from Level 1 to Level
2, inserted a new `content/09-instructions/` after it, and pushed the seven
parts that followed from `08`–`15` to `10`–`16`, and no reader's ticks moved
with them.

`$TUTOR_STATE` overrides the state directory, and `tutor frame` reads marks
only when that variable is set, never from the real file, so the command
stays deterministic for `bin/parity.sh`. That harness drives no keyboard
input at all, so it cannot see `m` being pressed — it now pins a marks
fixture instead, and samples a second pass of frames against it to cover
the tick.

## The new-article marker

Every article carries a version tag on its own line, just under the
heading — `*v0.2.1*` — and the indexer now reads it into `index.json`
alongside everything else it already derives; it is the same habit that
turned levels and sections from stored fields into derived ones, just with
a new consumer rather than a new copy of the fact. Drop the tag from a new
article and the indexer has nothing to read, so the marker below silently
never appears for it.

That version feeds a second marker in the sidebar: a green `N`, drawn in
the same column the read tick uses. It appears when an article's indexed
version matches the binary being run, the reader has not ticked it read,
and `~/.local/share/tutor/installed` — one line, written by `install.sh`
only on a reader's first-ever install — names an older version than that.
The read tick is checked first and always wins, so a fresh install shows no
`N` at all, an upgrade shows it on exactly what the new release added, and
once the next version ships those articles go quiet again on their own —
nothing expires it and nothing migrates it.

`bin/parity.sh` pins a fixture for this the same way it pins one for the
read tick: the harness never presses a key, so anything only reachable that
way is invisible to it unless a fixture stands in for the key press.

## What ships, and what does not

The reader gets the whole repository, so the trimming happens on her machine
rather than here: `install.sh` prunes the developer-only material after
installing the launcher and before building the content index, so the index
is built from the tree she keeps.

It removes `go/`, `bin/`, `devlog/`, `content/_pipeline/`,
`content/pipeline.md`, `.github/`, `tui/*.py`, `tui/__pycache__`, `.dvc/`,
`.dvcignore`, `.gitignore`, `.claude/settings.json` and
`.claude/settings.local.json`. Stripping the Python reader is the one that
matters, so nothing in the reader's home folder can reach for `python3`;
`pipeline.md` goes because it is authoring scaffolding, and a reader opening
it would find a work list where she expected an article.
`.claude/skills/` stays, being the agent half of the course. Every step is
`rm -rf`/`-f`, so re-running the installer is safe.

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
and how levels and sections are derived rather than stored.

## Contributing

This repo runs GitHub flow. Work happens on short-lived `spike/NNN` branches
A/B'd against the trunk, `tori`, then merged or discarded; every spike gets
an entry in `devlog/SPIKES.md`. A discarded spike's commits vanish with its
branch, which is what the devlog exists to outlive.

The repo is public and its history was squashed to a single commit before it
became so. Assume anything committed here is readable by anyone.
