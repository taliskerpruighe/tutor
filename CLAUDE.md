# tutor

## Purpose

A crash course on Claude Code, delivered two ways from one corpus: a wiki-style TUI reader and a Claude Code skill that answers from the same articles.

## Layout

- `bin/` — build, packaging, and preview scripts, and the compiled reader
- `content/` — the course articles, one directory per part
- `go/` — the TUI reader's Go source
- `packaging/` — the README/AGENTS/CLAUDE that install.sh swaps into place for a shipped copy
- `tui/` — the Python parity oracle for the TUI reader, and its built binaries

## Commands

- `install.sh` — installs the `tutor` command; invoke with `bash`, not directly

## Quirks

The source repo is also what a reader receives — the reader downloads the GitHub ZIP rather than cloning, since `git` on a non-developer Mac triggers a large Command Line Tools install, and `install.sh` strips the version control and authoring machinery on the way in.

<!-- git-ops:branch -->
## Next

@lab/TODO.md
<!-- /git-ops:branch -->
