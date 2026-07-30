# CLAUDE.md — tutor

This repo also carries an `AGENTS.md`, written for other coding agents rather
than for you. **Do not read it** unless the user points you at it explicitly.
Everything in it is here too, in your own register.

## Repo type

**GitHub flow.** The trunk is `tori` — this repo's trunk was renamed, so
`main` exists nowhere in it. Work happens on short-lived `spike/NNN`
branches, A/B'd against `tori`, then merged or discarded. A discarded spike
takes its commits with it, which is why there is a `devlog/`: see
`devlog/SPIKES.md` for what has been tried, including what was tried and
thrown away.

The repo is **public**. Its history was squashed to a single commit before
that happened. Assume anything you add here is readable by anyone.

## What this is

A crash course on Claude Code. The reader downloads this repository from
GitHub into `~/tutor`, runs `install.sh`, and reads it two ways:

- **outside Claude Code** — a wiki-style TUI in a terminal of its own
- **inside Claude Code** — an agent that answers questions from the articles

Both read the same corpus. There is no second copy of any fact anywhere.

```
content/            the single source of truth
  ├── index.json    generated; regenerates itself when articles change
  ├── _pipeline/    gitignored raw authoring notes — not part of the course
  └── NN-part/NN-article.md
go/                 the reader (Go, zero dependencies) — what ships
tui/                the same reader in Python — the parity oracle
  └── bin/          committed build output; the binaries that ship
.claude/skills/     the skills the shipped agent loads
packaging/          the CLAUDE.md, AGENTS.md and README.md that ship
install.sh          sets up the reader's copy and prunes developer material
bin/build-tui.sh    go/ -> tui/bin/tutor-darwin-{arm64,amd64}
bin/parity.sh       diffs the two implementations byte for byte
devlog/SPIKES.md    the durable record of spikes, merged and discarded
```

## Two implementations, one of them frozen

`go/` and `tui/*.py` are the same programme written twice. **`go/` is what
ships.** The Python tree is kept, and must keep working, because it is the
reference `bin/parity.sh` diffs against — that harness is the only real
verification available for macOS binaries that cannot be run on this machine.

So: change `go/`, then run `sh bin/parity.sh`. If it reports a difference,
treat the Go side as wrong until you have proven otherwise. Editing
`tui/*.py` to make a diff go away defeats the entire point of having it, and
you should refuse to do that without the user insisting.

## Adding content

Drop a markdown file into `content/NN-part/NN-title.md`. Nothing else is
needed — the index rebuilds itself whenever an article is newer than it.

```markdown
---
id: skills/frontmatter
title: The frontmatter
part: Skills
section: When To Build One
order: 3
summary: One sentence, shown in search results.
keywords: [skill, frontmatter, description]
---

# The frontmatter
```

`part:` is the display name on the tab bar; the directory's number sets the
order. Directory and file number prefixes order everything, and `order:`
overrides that where needed. Missing fields degrade rather than fail: `title`
falls back to the first heading, `part` to a de-slugged directory name.

`section:` is optional and divides a part's articles into the side tabs down
the left. A section is a **run of consecutive articles sharing the value**, so
ordering is what groups them — there is no second directory level. The whole
part stays on show, and numbering restarts inside each section. Leave
`section:` off and the part draws as one plain numbered list.

**Keep each section to nine articles or fewer** — or each part, where a part
has no sections. `1`–`9` are the only keys that jump straight to an article,
and they count within whatever list is on show, so a tenth entry is reachable
only by walking to it with `n`.

`content/_pipeline/` holds raw authoring notes the finished articles are
written from. It is gitignored and excluded from the archive. Do not treat
anything in it as course content, and do not publish from it.

## The markdown contract

`go/render.go` and `tui/render.py` implement a deliberate subset, not general
markdown. It is a contract because both sides are authored here. Stay inside
it:

    headings #..####      paragraphs (reflowed)   fenced code blocks
    inline `code`         **bold**   *italic*     bullet + ordered lists
    > blockquotes         --- rules  [links](url) | pipe | tables |
    ![caption](pic.png)   — PNG, on a line of its own, Ghostty only

When you write an article:

- **Code blocks are never wrapped** — they are clipped. Keep lines short
  enough to read at 60 columns.
- **Tables take their natural width** and shrink the widest column first; at
  very narrow widths they fall back to labelled stacks. Keep cells terse.
- Nesting a list is two spaces per level, to a depth of three.
- A blank line between list items starts a new list. That is intentional.
- **A picture is a block on its own line**, the same way a rule or a table
  is — `![Ghostty with two tabs open](images/ghostty.png)`. Write nothing
  else on that line: an image folded into a sentence is not recognised and
  is left sitting there as plain text, which is deliberate, not a gap in the
  parser.
- **PNG only, and only from `content/images/`.** Both renderers take PNG
  directly; anything else — webp, jpeg, gif — has to be converted once, by
  hand, before it goes in.
- **Keep a picture under 500 KB.** A test enforces this: the reader
  downloads the whole repository, and a few careless screenshots would turn
  a small course into a large one. Size the file to roughly the width it
  will be shown at — around 1200 pixels is plenty — rather than shipping a
  full-resolution screenshot and trusting the pane to shrink it.
- **Write the alt text as a caption, not a label.** Pictures only appear in
  Ghostty, the terminal the reader is told to use. Anywhere else — notably
  tmux, which swallows the protocol outright — the picture silently
  collapses to its alt text alone. For that reader the alt text is not a
  description of the image, it is the whole of that block, so write it as a
  sentence that stands on its own rather than a filename-style tag.
- **You do not state a height.** The space a picture reserves comes from its
  own proportions, worked out the same way by both renderers so the parity
  harness keeps agreeing on it. A tall, narrow picture reserves a lot of
  rows for not much width, so a wide, short screenshot suits the pane better
  than a tall one does.
- Anything outside the subset renders as a plain paragraph — readable, but
  not what you meant. Preview it before committing.

## Architecture notes

- **Go exists to remove Python.** The reader's Mac is not a developer
  machine, so `/usr/bin/python3` there is a stub that triggers a ~1 GB
  Command Line Tools download the first time anything runs it. A static
  binary is the whole reason the install can be silent.
- **Cross-compiled arm64 binaries are ad-hoc signed by Go's own linker**
  (`NeedCodeSign() = IsDarwin() && IsARM64()`, pure Go, no `codesign`
  needed). Apple Silicon kills unsigned Mach-O binaries, so `build-tui.sh`
  parses the load commands and fails the build if `LC_CODE_SIGNATURE` is
  missing. Keep `CGO_ENABLED=0`; external linking would skip the signing.
- **`install.sh` copies the binary with `cat > file`, never `cp`.** Archive
  Utility stamps `com.apple.quarantine` on everything it extracts, and macOS
  refuses to run a quarantined unsigned binary. `cp` preserves xattrs
  (copyfile), and `xattr -d` is unusable because `/usr/bin/xattr` is itself a
  `#!/usr/bin/python3` script — it would demand the very toolchain being
  avoided. A shell redirect creates a fresh inode with no xattrs at all.
- **The copy goes to a temp name and is renamed into place.** The reader is
  told to keep the TUI open in its own tab, so overwriting the launcher
  directly would hit `ETXTBSY` whenever the installer is re-run.
- **`glow` and `bat` were tested and rejected.** `bat` renders markdown
  *source*, not markdown. `glow` only keeps colour through a pipe under
  `CLICOLOR_FORCE=1`, and then emits an escape sequence around every padding
  space, with wrapping that follows source newlines rather than the pane
  width. Owning the renderer buys correct reflow, instant resize, and no
  dependency on the reader's machine.
- **Sections are derived, not stored.** `index.json` stays a flat list of
  articles carrying a `section` string; `partSections` groups consecutive
  equal values at render time. So search, `flatten` and the skill never
  learnt about sections, and a part with no `section:` anywhere is one
  untitled section spanning the lot — the old behaviour as the degenerate
  case rather than a branch.
- **The open section is derived from the article index too.** There is no
  second cursor, so `n`, a search hit and a click all open the right section
  without knowing sections exist.
- **Terminal size comes from `ioctl(TIOCGWINSZ)`** on the tty fd, never from
  `$COLUMNS` — a stale exported value would freeze the layout at the size the
  shell started at.
- **Display width comes from a generated table** (`bin/gen-width.py` ->
  `go/width_table.go`), taken from Python's `unicodedata`. Go's `unicode.Mn`
  is a different set from `combining(ch) != 0`, so approximating it would
  break parity silently.
- **The platform delta is three functions.** `go/term_{darwin,linux}.go`
  expose only `getTermios`, `setTermios`, `getWinsize`; BSD spells the ioctls
  `TIOCGETA`/`TIOCSETA` where Linux says `TCGETS`/`TCSETS`. Everything else
  is shared, which matters because the darwin path ships exercised only by
  inspection — the tests run the Linux build.
- **An agent cannot launch the TUI.** Claude Code owns its terminal; `tutor`
  detects the missing tty and prints instructions rather than hanging. This
  applies to you: never run `tutor` from a tool call.

## Commands

```bash
sh bin/build-tui.sh                           # build binaries + signing gate
sh bin/parity.sh                              # Go vs Python, byte for byte
./bin/tutor-host index                        # rebuild the index
./bin/tutor-host doctor                       # check an install
./bin/tutor-host render content/…/x.md 72     # preview a render, no tty needed
./bin/tutor-host frame 80 24 shell/packages   # preview a whole screen
```

`./bin/tutor-host render` and `frame` are the two that work without a
terminal, so they are the ones you can actually use to check your own work.

## What ships

The reader gets the whole repository, so nothing is trimmed before it
reaches her. **`install.sh` does the trimming instead**, in its "prune
developer-only material" section — after the launcher is installed and
before the index is built, so the index is built from the tree she keeps.
Every step is `rm -rf`/`-f` and none depends on a previous one having found
anything, so re-running the installer is safe.

It removes `go/`, `bin/`, `devlog/`, `content/_pipeline/`, `.github/`,
`tui/*.py`, `tui/__pycache__`, `.dvc/`, `.dvcignore` and `.gitignore`. The
`tui/*.py` removal is the one that matters: leave the Python reader in place
and an agent improvising past a problem could run it and set off the ~1 GB
Command Line Tools download.

`.claude/settings.json` goes too, because a plugin enabled here and not
there would only produce an error for the reader. `.claude/skills/` is left
alone — it is how the agent half of the course works.

`packaging/CLAUDE.md`, `packaging/AGENTS.md` and `packaging/README.md` are
copied over the root `CLAUDE.md`, `AGENTS.md` and `README.md`, and then
`packaging/` itself is deleted. The agent sitting in the reader's home
folder should read instructions written for the reader, not for us — this
document, for instance, would only mislead it.

`tui/bin/` is committed deliberately, and `.gitignore` says so. The reader
downloads the repository as it stands; without those binaries in it, that
download would be source code rather than a working reader. `bin/tutor-host`
stays ignored — it is the local build-machine binary.

## Claude-specific

**Skills.** `.claude/skills/` holds four, and they ship:

- `tutor` — answering a question from `content/`. The answer lives in the
  articles; find it and use it rather than answering from memory.
- `learn` — taking the reader through the course one section at a time.
- `custom-agents` — building the reader a custom subagent.
- `custom-skills` — building the reader a custom skill.

These are the shipped copy's skills, not yours to invoke while working in
this repo. They describe behaviour in the reader's `~/tutor`, and reading one
is how you find out what the reader will experience.

**Plugins.** `.claude/settings.json` enables none. Keep it that way, or the
build will ship a setting the reader's machine cannot satisfy.

**Commits.** All commits go through `git-ops commit`. Never run a `git`,
`jj`, `dvc` or `git-ops` command that changes repo state unless the user
tells you to.
