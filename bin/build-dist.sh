#!/bin/sh
# Build the archive that actually gets sent.
#
# What lives in this repo and what the reader receives are not the same tree:
# the reader gets a plain folder in their home directory, with none of the
# version control or authoring machinery. This script is the boundary between
# the two.
#
#   sh bin/build-dist.sh
#   -> dist/tutor.zip   (unzips to ~/tutor)

set -eu

ROOT=$(cd "$(dirname "$0")/.." && pwd)
DIST="$ROOT/dist"
STAGE="$DIST/tutor"

# Two lists, because the distinction matters: TOP names are anchored to the
# repo root, ANY names are dropped wherever they appear. `bin` has to be
# anchored — an unanchored exclude would also swallow `tui/bin/`, which holds
# the one thing the reader actually needs.
#
# `*.py` drops the Python reader from the end user's copy. It is kept in the
# repo as the oracle bin/parity.sh diffs against, but shipping it would leave
# a live tripwire in the reader's home folder: an agent improvising past a
# problem could run `python3 ~/tutor/tui/tutor.py` and set off the 1 GB
# Command Line Tools dialog this whole rewrite exists to prevent. The
# fallback cannot help the reader anyway — no usable python3 is precisely the
# case it would fire in.
#
# `outline.md` and `rest.md` are working notes kept at the root; they are the
# raw material the articles are written from, not part of the course.
# `content/_pipeline` holds the same kind of raw authoring material one level
# down: draft notes the finished articles are written from, not part of the
# course either.
# `go/` is the reader's source: the reader gets the compiled binary, not the
# code.
TOP=".git .jj .dvc .dvcignore .gitignore devlog bin dist packaging outline.md rest.md go go.mod go.sum content/_pipeline"
ANY=".DS_Store __pycache__ *.pyc *.py"

command -v zip >/dev/null 2>&1 || {
    echo "zip is not installed." >&2
    exit 1
}

# The binaries are never committed, so build them now. This also runs the
# signing gate: an unsigned arm64 binary would be refused by the reader's machine.
sh "$ROOT/bin/build-tui.sh"
echo

rm -rf "$STAGE" "$DIST/tutor.zip"
mkdir -p "$STAGE"

if command -v rsync >/dev/null 2>&1; then
    set --
    for pattern in $TOP; do
        set -- "$@" --exclude "/$pattern"
    done
    for pattern in $ANY; do
        set -- "$@" --exclude "$pattern"
    done
    rsync -a "$@" "$ROOT/" "$STAGE/"
else
    tar_excludes=""
    for pattern in $TOP; do
        tar_excludes="$tar_excludes --exclude=./$pattern"
    done
    for pattern in $ANY; do
        tar_excludes="$tar_excludes --exclude=$pattern"
    done
    # shellcheck disable=SC2086
    (cd "$ROOT" && tar cf - $tar_excludes .) | (cd "$STAGE" && tar xf -)
fi

# The reader's copy gets instructions written for the reader. The repo's
# CLAUDE.md and README.md talk about spike branches and renderer internals,
# which would only mislead the agent sitting in the reader's home folder.
cp "$ROOT/packaging/CLAUDE.md" "$STAGE/CLAUDE.md"
cp "$ROOT/packaging/README.md" "$STAGE/README.md"

# Plugins enabled here are not enabled there; shipping the setting would only
# produce an error about a plugin the reader does not have.
rm -f "$STAGE/.claude/settings.json"

# Regenerate the index inside the staged copy so the archive is complete on
# arrival: the reader can read before installing. Built with the Go indexer,
# which is the one that will run on the reader's machine.
TUTOR_HOME="$STAGE" "$ROOT/bin/tutor-host" index >/dev/null
find "$STAGE" -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
chmod +x "$STAGE/install.sh"
chmod +x "$STAGE"/tui/bin/*

(cd "$DIST" && zip -qr tutor.zip tutor)
rm -rf "$STAGE"

# Check the artefact the reader actually receives, not the one that was linked.
# build-tui.sh proved the binary was signed in the repo; this proves nothing
# between there and the zip disturbed it. An ad-hoc signature is self-contained,
# so byte-identical is the whole proof.
VERIFY=$(mktemp -d)
trap 'rm -rf "$VERIFY"' EXIT
(cd "$VERIFY" && unzip -q "$DIST/tutor.zip")
for arch in arm64 amd64; do
    cmp -s "$ROOT/tui/bin/tutor-darwin-$arch" "$VERIFY/tutor/tui/bin/tutor-darwin-$arch" || {
        echo "tutor-darwin-$arch changed between the build and the archive." >&2
        exit 1
    }
done
if find "$VERIFY/tutor" -name '*.py' | grep -q .; then
    echo "Python leaked into the archive:" >&2
    find "$VERIFY/tutor" -name '*.py' >&2
    exit 1
fi
echo "  archive verified   binaries intact, no Python"
echo

echo "Built $DIST/tutor.zip"
echo
echo "Send it with these instructions:"
echo "  1. Unzip it into your home folder, giving you ~/tutor"
echo "  2. Run:  bash ~/tutor/install.sh"
echo "  3. Open a new terminal tab and run:  tutor"
