# AGENTS.md — tutor

## Repo type

**GitHub flow.** The trunk is `tori` — this repo's trunk was renamed, so
`main` exists nowhere here. Short-lived `spike/NNN` branches are A/B'd
against `tori`, then merged or discarded; a discarded spike takes its history
with it, so this repo keeps a `devlog/` — see `devlog/SPIKES.md`.

## What this is

A crash course on Claude Code. The reader receives a zip, unpacks
it to `~/tutor`, and reads it two ways:

- **outside Claude Code** — a wiki-style TUI in a terminal of its own, and
- **inside Claude Code** — an agent that answers the reader's questions.

Both read the same corpus. There is no second copy of any fact.

```
content/            the single source of truth
  ├── index.json    generated; regenerates itself when articles change
  └── NN-part/NN-article.md
go/                 the reader (Go, zero dependencies) — what ships
tui/                the same reader in Python — the parity oracle, see below
  └── bin/          gitignored build output; the binaries that ship
.claude/skills/     the skill the agent loads to answer questions
packaging/          the CLAUDE.md and README.md that ship in the reader's copy
bin/build-tui.sh    go/ -> tui/bin/tutor-darwin-{arm64,amd64}
bin/parity.sh       diffs the two implementations byte for byte —
                    article renders, whole composed frames, and index.json
bin/build-dist.sh   repo tree -> dist/tutor.zip
```

## Two implementations, one of them frozen

`go/` and `tui/*.py` are the same programme written twice. **`go/` is what
ships.** The Python tree is kept, and must keep working, because it is the
reference `bin/parity.sh` diffs against — that harness is the only real
verification available for macOS binaries that cannot be run here.

So: change `go/`, then run `sh bin/parity.sh`. If it reports a difference,
the Go side is wrong until proven otherwise. Changing `tui/*.py` to make a
diff go away defeats the entire point of having it.

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
overrides that when needed. Missing fields degrade: `title` falls back to the
first heading, `part` to a de-slugged directory name.

`section:` is optional, and divides a part's articles into the side tabs down
the left. A section is a **run of consecutive articles sharing the value**, so
ordering is what groups them — there is no second directory level. The whole
part stays on show, and numbering restarts inside each section. Leave
`section:` off and the part draws as one plain numbered list, exactly as
before.

**Keep each section to nine articles or fewer — or each part, where a part has
no sections.** `1`–`9` are the only keys that jump straight to an article, and
they count within whatever list is on show, so a tenth entry is reachable only
by walking there with `n`. Nine is also about as long as a section should be
before it wants splitting anyway.

## The markdown contract

`go/render.go` and `tui/render.py` implement a deliberate subset, not general
markdown. It is a contract because we author both sides. Staying inside it:

    headings #..####      paragraphs (reflowed)   fenced code blocks
    inline `code`         **bold**   *italic*     bullet + ordered lists
    > blockquotes         --- rules  [links](url) | pipe | tables |

Notes that matter when writing:

- **Code blocks are never wrapped** — they are clipped. Keep lines short
  enough to read at 60 columns.
- **Tables take their natural width** and shrink the widest column first; at
  very narrow widths they fall back to labelled stacks. Keep cells terse.
- Nesting a list is two spaces per level, to a depth of three.
- A blank line between list items starts a new list. That is intentional.
- Anything outside the subset renders as a plain paragraph — readable, but
  not what you meant. Preview before committing.

## Architecture notes

- **Go exists to remove Python.** The reader's Mac is not a developer
  machine, so `/usr/bin/python3` there is a stub that triggers a ~1 GB Command
  Line Tools download the first time anything runs it. A static binary is the
  whole reason the install can be silent.
- **Cross-compiled arm64 binaries are ad-hoc signed by Go's own linker**
  (`NeedCodeSign() = IsDarwin() && IsARM64()`, pure Go, no `codesign`
  needed). Apple Silicon kills unsigned Mach-O binaries, so `build-tui.sh`
  parses the load commands and fails the build if `LC_CODE_SIGNATURE` is
  missing. Keep `CGO_ENABLED=0`; external linking would skip the signing.
- **`install.sh` copies the binary with `cat > file`, never `cp`.** Archive
  Utility stamps `com.apple.quarantine` on everything it extracts, and macOS
  refuses to run a quarantined unsigned binary. `cp` preserves xattrs
  (copyfile), and `xattr -d` is unusable because `/usr/bin/xattr` is itself a
  `#!/usr/bin/python3` script — it would demand the very toolchain we are
  avoiding. A shell redirect creates a fresh inode with no xattrs at all.
- **The copy goes to a temp name and is renamed into place.** The reader is
  told to keep it open in its own tab, so overwriting the launcher directly
  would hit `ETXTBSY` whenever the agent re-runs the installer.
- **`glow` and `bat` were tested and rejected.** `bat` renders markdown
  *source*, not markdown. `glow` only keeps colour through a pipe under
  `CLICOLOR_FORCE=1`, and then emits an escape sequence around every padding
  space with wrapping that follows source newlines rather than the pane
  width. Owning the renderer buys correct reflow, instant resize, and no
  dependency on the reader's machine.
- **Sections are derived, not stored.** `index.json` stays a flat list of
  articles carrying a `section` string; `partSections` groups consecutive
  equal values at render time. So search, `flatten` and the skill never learnt
  about sections, and a part with no `section:` anywhere is one untitled
  section spanning the lot — the old behaviour as the degenerate case rather
  than a branch.
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
- **The agent cannot launch the TUI.** Claude Code owns its terminal;
  `tutor` detects the missing tty and prints instructions rather than hanging.

## Commands

```bash
sh bin/build-tui.sh                           # build binaries + signing gate
sh bin/parity.sh                              # Go vs Python, byte for byte
./bin/tutor-host index                        # rebuild the index
./bin/tutor-host doctor                       # check an install
./bin/tutor-host render content/…/x.md 72     # preview a render, no tty needed
./bin/tutor-host frame 80 24 shell/packages   # preview a whole screen
sh bin/build-dist.sh                          # -> dist/tutor.zip
```

## What ships

`bin/build-dist.sh` excludes in two ways. Anchored to the repo root —
`bin/`, `go/`, `devlog/`, `packaging/` and `dist/` — because an unanchored
`bin` would also swallow `tui/bin/`, which holds the only thing the reader
actually needs. Dropped wherever they appear instead: `.DS_Store`, `__pycache__`,
`*.pyc`, and `*.py` — the last of these strips the whole Python reader from
the shipped copy, so nothing in the reader's home folder can reach for
`python3` and set off the Command Line Tools download. `.claude/settings.json`
is stripped from the staged copy separately, after the rest is assembled,
because a plugin enabled here and not there would only error for the reader.
`packaging/CLAUDE.md` and `packaging/README.md` replace the root `CLAUDE.md`
and `README.md` in the reader's copy. The reader's agent should read
instructions written for the reader, not for us.
