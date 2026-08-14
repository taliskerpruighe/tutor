# AGENTS.md — tutor

## Repo type

**GitHub flow.** The trunk is `tori` — this repo's trunk was renamed, so
`main` exists nowhere here. Short-lived `spike/NNN` branches are A/B'd
against `tori`, then merged or discarded; a discarded spike takes its history
with it, so this repo keeps a `devlog/` — see `devlog/SPIKES.md`.

The repo is **public**, and its history was squashed to a single commit
before that happened. Anything added here is readable by anyone.

## What this is

A crash course on Claude Code. The reader downloads this repository from
GitHub into `~/tutor`, runs `install.sh`, and reads it two ways:

- **outside Claude Code** — a wiki-style TUI in a terminal of its own, and
- **inside Claude Code** — an agent that answers the reader's questions.

Both read the same corpus. There is no second copy of any fact.

```
content/            the single source of truth
  ├── index.json    generated; regenerates itself when articles change
  ├── images/       the PNGs articles embed; nothing else may be referenced
  ├── pipeline.md   which part sits at which level; authoring, not content
  ├── _pipeline/    gitignored raw authoring notes — not part of the course
  └── NN-part/NN-article.md
go/                 the reader (Go, zero dependencies) — what ships
tui/                the same reader in Python — the parity oracle, see below
  └── bin/          committed build output; the binaries that ship
.claude/skills/     the skills the shipped agent loads — committed, see below
packaging/          the CLAUDE.md, AGENTS.md and README.md that ship in the
                    reader's copy, replacing the ones at this root
install.sh          sets up the reader's copy and prunes developer material
version.txt         the version `tutor update` compares against GitHub
bin/build-tui.sh    go/ -> tui/bin/tutor-darwin-{arm64,amd64}
bin/parity.sh       diffs the two implementations byte for byte —
                    article renders, whole composed frames, and index.json
bin/banner-preview.sh   eyeball the launch screen without rebuilding
devlog/SPIKES.md    the durable record of spikes, merged and discarded
```

`.claude/` is committed here, unlike in every other repo on this machine:
the global excludes file ignores `.claude/` everywhere, so this repo's
`.gitignore` carries a `!/.claude/` negation to outrank it. That line is
load-bearing. The reader gets the agent half of the course only because
`.claude/skills/` sits inside the repository she downloads, and dropping the
negation would stop the skills shipping without breaking anything visible
here. `.claude/settings.local.json` stays ignored — it is machine-local.

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
level: Level 2
part: Skills
section: When To Build One
order: 3
summary: One sentence, shown in search results.
keywords: [skill, frontmatter, description]
---

# The frontmatter
```

The course nests three deep — **level**, **part**, **section** — and only the
level is a tab along the top. Parts and sections are both headings down the
left margin, the part flush and its sections indented under it. Only the part
being read expands; the level's other parts stay as one-line headings.

`level:` is the tab. A level is a **run of consecutive parts sharing the
value**, the same way a section is a run of consecutive articles — so the
directory numbers group parts into levels and there is no second directory
level. `content/pipeline.md` decides which part belongs to which. Leave
`level:` off everywhere and each part becomes its own level, which is the
two-tier reader as it stood before levels existed.

`part:` is the part heading; the directory's number sets the order. Directory
and file number prefixes order everything, and `order:` overrides that when
needed. Missing fields degrade: `title` falls back to the first heading,
`part` to a de-slugged directory name, `level` to the part's own title.

`section:` is optional, and divides a part's articles into the indented
headings beneath it — again a run of consecutive articles sharing the value.
The whole part stays on show, and numbering restarts inside each section.
Leave `section:` off and the part draws as one plain numbered list, exactly as
before.

**Keep each section to nine articles or fewer — or each part, where a part has
no sections.** `1`–`9` are the only keys that jump straight to an article, and
they count within whatever list is on show, so a tenth entry is reachable only
by walking there with `n`. Nine is also about as long as a section should be
before it wants splitting anyway.

`content/_pipeline/` holds raw authoring notes the finished articles are
written from. It is gitignored and excluded from the archive. Nothing in it
is course content, and nothing should be published straight out of it.

## The markdown contract

`go/render.go` and `tui/render.py` implement a deliberate subset, not general
markdown. It is a contract because we author both sides. Staying inside it:

    headings #..####      paragraphs (reflowed)   fenced code blocks
    inline `code`         **bold**   *italic*     bullet + ordered lists
    > blockquotes         --- rules  [links](url) | pipe | tables |
    ![caption](pic.png)   — PNG, on a line of its own, Ghostty only

Notes that matter when writing:

- **Code blocks are never wrapped** — they are clipped. Keep lines short
  enough to read at 60 columns.
- **Tables take their natural width** and shrink the widest column first; at
  very narrow widths they fall back to labelled stacks. Keep cells terse.
- Nesting a list is two spaces per level, to a depth of three.
- A blank line between list items starts a new list. That is intentional.
- **A picture is a block on its own line**, like a rule or a table —
  `![Ghostty with two tabs open](images/ghostty.png)`. Write nothing else on
  that line: an image folded into a sentence is not recognised and is left
  sitting there as plain text, which is deliberate rather than a parser gap.
- **PNG only, and only from `content/images/`.** Both renderers take PNG
  directly; webp, jpeg or gif must be converted by hand before going in.
- **Keep a picture under 500 KB** — `go/image_test.go` enforces it. The
  reader downloads the whole repository, so a few careless screenshots would
  turn a small course into a large one. Size the file to roughly the width it
  is shown at, around 1200 pixels, rather than shipping full resolution.
- **Write the alt text as a caption, not a label.** Pictures appear only in
  Ghostty, the terminal the reader is told to use; anywhere else — notably
  tmux, which swallows the protocol — the picture collapses to its alt text
  alone, which is then the whole of that block. Write a sentence that stands
  on its own, not a filename-style tag.
- **You do not state a height.** The space a picture reserves comes from its
  own proportions, worked out identically by both renderers so the parity
  harness keeps agreeing on it. A wide, short screenshot suits the pane
  better than a tall, narrow one.
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
- **The launch screen is printed before raw mode, on purpose.** `go/splash.go`
  draws five rows of block letters and holds them for five seconds, and
  `cmdRun` prints it *before* `NewTerminal.Start` takes the tty into raw mode
  and switches to the alternate screen. That ordering is the feature: printed
  there it scrolls into the shell's history like any command's output and is
  still there after the reader quits, where printing it inside the alternate
  screen would wipe it on exit. It writes its own `\x1b[…m` sequences instead
  of calling `sgr()`, because one of its five colours (215) exists in the
  styles map only inside `code`, bundled with a background that would paint a
  block behind the letter. `tutor splash [cols]` prints it once with no wait;
  `sh bin/banner-preview.sh` draws the same design in shell for eyeballing
  without a rebuild, and the Go source wins if the two disagree. The design is
  settled — the rejected letterforms and colour schemes were deleted on
  purpose, so there is nothing left to switch to.
- **The splash has no Python counterpart, so parity never sees it.** It is
  the one part of the reader that exists on the Go side alone: changing it
  costs nothing in `tui/` and buys no verification either. Check it by eye.
- **`glow` and `bat` were tested and rejected.** `bat` renders markdown
  *source*, not markdown. `glow` only keeps colour through a pipe under
  `CLICOLOR_FORCE=1`, and then emits an escape sequence around every padding
  space with wrapping that follows source newlines rather than the pane
  width. Owning the renderer buys correct reflow, instant resize, and no
  dependency on the reader's machine.
- **Levels and sections are both derived, not stored.** `index.json` stays a
  flat list of parts holding a flat list of articles; `indexLevels` groups
  consecutive parts by their `level` string and `partSections` groups
  consecutive articles by their `section` string, both at render time. So
  search, `flatten` and the skill never learnt that either exists. Each
  degenerates rather than branching: a part with no `section:` anywhere is one
  untitled section spanning the lot, and a corpus with no `level:` anywhere is
  one part per level — exactly the two-tier reader that preceded them.
- **The open level and the open section are derived from the cursor too.** The
  cursor is still just `(partI, articleI)`; there is no third index and no
  second one. So `n`, a search hit and a click all open the right tab and the
  right section without knowing either exists.
- **Three tiers, three key pairs.** `←`/`→` step level, `[`/`]` step part
  within the level, `⇥`/`⇧⇥` step section. Tab walks the *flattened* list of
  every section in the level, so it carries on into the next part rather than
  stopping dead at a boundary — the left column reads top to bottom the way it
  looks.
- **The sidebar grew two columns to pay for the indent.** `sidebarWidth` went
  from `min(28, max(18, …))` to `min(30, max(20, …))`, which is exactly what
  the extra step of indentation costs an article title, so titles have the
  room they had when parts were tabs.
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
  This applies to you: never run `tutor` from a tool call.
- **Read marks live in exactly one file outside the reader's own tree:**
  `~/.local/share/tutor/read.json`, a sorted set of article `id`s under a
  `"read"` key, sitting beside the `home` pointer file `install.sh` already
  writes there. It has to sit outside the tree because `applyUpdate` in
  `go/update.go` renames the whole repo directory aside and deletes it —
  state kept inside it would not survive a single upgrade.
- **The set is keyed on article `id`, not `path`.** Renumbering a directory
  changes a `path` but not an `id`, so reorganising the course never costs
  anyone their marks — this release moved `content/08-claude/` from Level 1
  to Level 2, inserted a new `content/09-instructions/` after it, and pushed
  the seven parts that followed from `08`–`15` to `10`–`16`, and not one
  reader's ticks moved with them.
- **`$TUTOR_STATE` overrides the state directory, and `tutor frame` reads
  marks only when it is set** — never from the real one — so the command
  stays byte-for-byte deterministic for `bin/parity.sh`, the same reasoning
  already recorded above for `app.images` in `cmdFrame`. `frame` never
  writes marks, only reads them.
- **The sidebar grew one more column to pay for the tick**, on the same
  principle as the two columns it grew for the indent: the column pays for
  it, not the titles.
- **`bin/parity.sh` drives no keyboard input at all, so a key binding is
  invisible to it.** The tick that binding leaves behind is not invisible,
  which is why the harness now pins a marks fixture and runs a second,
  sampled frame pass against it.
- **`index.json` gained a `version` field per article, read off content that
  was already there.** Every article carries a version tag on its own
  italic line between the H1 and the first paragraph — `*v0.1.0*`,
  `*v0.2.0*`, `*v0.2.1*` — and `content/_pipeline/visual-guide.md`
  mandates it across all 114 articles. The indexer takes the first
  whole-line match of `*v` followed by digits and dots followed by `*` and
  stores it, leading `v` included, as `version`. It is the same "derived,
  not stored" habit as levels and sections: a new consumer of a convention
  that already existed, not a second copy of the same fact sitting in the
  frontmatter. The consequence cuts the other way too — the tag is now
  load-bearing, so an article that drops it silently loses its marker.
- **A new state file, `~/.local/share/tutor/installed`,** holds one line:
  the version number, written by `install.sh` only on a first-ever install,
  guarded on `$STATE_DIR/home` not yet existing. That guard is load-bearing
  because `applyUpdate` in `go/update.go` re-runs `install.sh` on every
  update, not just the first one — an unguarded write would restamp every
  upgrade as a fresh install. Nothing in `go/` or `tui/` ever writes this
  file, only reads it, and its absence is itself meaningful: it marks a
  user who was already here before the file existed.
- **The green `N`.** In the sidebar's one-column mark slot — the same slot
  the read tick `✓` occupies — an article draws a green `N` when its
  indexed `version` equals `"v"` plus the binary's own `version` constant,
  the `installed` file's contents differ from that version, and the
  article is not marked read; the tick is checked first and wins outright.
  A fresh install shows no `N` at all, an upgrader sees `N` on exactly the
  articles the new release added, and once the next version ships those
  articles go quiet again on their own, with no migration step and nothing
  to expire.
- **`read.json` was deliberately not extended with a new key for this.** A
  separate file means an upgrading user's existing marks are read by
  exactly the code that reads them today, so their ticks cannot be
  disturbed by anything the marker does.
- **The mark only breaks into its own span when it is a green `N` on an
  unselected row.** A tick or a blank stays inside the number's own span
  exactly as it did before, so the existing invariant — a selected row
  turns `sel_row` in one piece — survives literally, and any frame with
  nothing new in it renders byte-for-byte what it always did.
- **`bin/parity.sh` gained a third fixture pass for the marker**, positive
  and negative, on the same principle the read-marks pass already
  established: the harness drives no keyboard input, so anything reachable
  only by a key press is invisible to it unless a fixture pins it down.
  `cmdFrame` reads `installed` only when `$TUTOR_STATE` is set, never from
  the real state directory — the same determinism rule already recorded
  above for `app.images` and for the read marks themselves.

## Commands

```bash
sh bin/build-tui.sh                           # build binaries + signing gate
sh bin/parity.sh                              # Go vs Python, byte for byte
sh bin/banner-preview.sh                      # the launch screen, no rebuild
./bin/tutor-host index                        # rebuild the index
./bin/tutor-host doctor                       # check an install
./bin/tutor-host render content/…/x.md 72     # preview a render, no tty needed
./bin/tutor-host frame 80 24 shell/packages   # preview a whole screen
./bin/tutor-host splash 80                    # the launch screen, no wait
./bin/tutor-host --version                    # the built-in version constant
```

`render`, `frame` and `splash` are the three that work without a terminal, so
they are the ones to check your own work with. `tutor update` is the reader's
command, not a maintenance one: it fetches the newer version from GitHub and
`applyUpdate` renames the whole `~/tutor` aside and deletes it. Do not run it
from a tool call. `version.txt` is what it compares against, fetched raw from
GitHub and tried against each branch in `updateBranches` in turn until one
answers, while the binary reports `go/main.go`'s `const version` — which
`splash.go` also takes its tag from rather than hardcoding one. The
version lives in four places, not three: `version.txt`, `go/main.go`'s
`const version`, `tui/tutor.py`'s `VERSION`, and `bin/banner-preview.sh`,
which hardcodes a fourth copy for the shell preview. `sh bin/build-tui.sh`
gates agreement across only the first three before it will compile;
`bin/banner-preview.sh` is checked by nothing and drifts silently unless
someone eyeballs `sh bin/banner-preview.sh` against the real splash. Four
files, one number: move all four, and check the fourth by eye.

The version in `version.txt` must have a tag behind it. `applyUpdate` builds
its tarball URL from the tag namespaced to the branch it was cut on —
`tori/MkI_v0.2.2`, not `MkI_v0.2.2` — and fetches that full namespaced tag.
The updater does not name a single branch: `go/update.go` holds
`updateBranches`, an ordered list tried in turn for both the `version.txt`
probe and the tag namespace, first branch to answer wins. A trunk rename, or
a second one added, needs its name added to `updateBranches`, with the old
name left in place until every installed copy has taken a release that
knows the new one — the list ships in the binary, so a copy that knows only
the retired name never sees a `version.txt` cut under the new one, and
readers on it are simply told no update exists at all; the test suite makes
no network call and would not catch it either. Push
`version.txt` ahead of the tag and readers are offered an update that 404s
when they accept it, which is worse than offering none. Bump and tag
together, and push the tag — `git push origin --tags` is separate from
pushing the branch.

## What ships

The reader gets the whole repository, so nothing is trimmed before it
reaches her. `install.sh` does the trimming instead, in its "prune
developer-only material" section — after the launcher is installed and
before the index is built, so the index is built from the tree she keeps.
Every step is `rm -rf`/`-f` and none depends on a previous one having found
anything, so re-running the installer is safe.

It removes `go/`, `bin/`, `devlog/`, `content/_pipeline/`, `.github/`,
`tui/*.py`, `tui/__pycache__`, `.dvc/`, `.dvcignore`, `.gitignore` and
`content/pipeline.md`. The `tui/*.py` removal is the one that matters: leave
the Python reader in place and an agent improvising past a problem could run
it and set off the ~1 GB Command Line Tools download. `pipeline.md` goes
because it is authoring scaffolding — a reader opening it would find a work
list where she expected an article.
`.claude/settings.json` and `.claude/settings.local.json` go too, since they
describe this development environment and a plugin named in one and absent
from her machine would only error; `.claude/skills/` is left alone, since it
is how the agent half of the course works, and it reaches her at all only
because of the `!/.claude/` negation described above.

`packaging/CLAUDE.md`, `packaging/AGENTS.md` and `packaging/README.md` are
copied over the root `CLAUDE.md`, `AGENTS.md` and `README.md`, and then
`packaging/` itself is deleted. The agent in the reader's home folder should
read instructions written for the reader, not for us — this document would
only mislead it, since nothing it describes (spikes, the devlog, `go/`, the
parity harness) exists in that copy.

`tui/bin/` is committed deliberately, and `.gitignore` says so. The reader
downloads the repository as it stands; without those binaries in it, that
download would be source code rather than a working reader. `bin/tutor-host`
stays ignored — it is the local build-machine binary.
