#!/bin/sh
# Diff the Go renderer against the Python one, byte for byte.
#
#   sh bin/parity.sh
#
# The macOS binaries cannot be executed on this machine, so this is the
# strongest verification available: everything above the ~30 lines of
# platform-specific ioctl code is shared, and this compares all of it against
# the implementation that was tested interactively.
#
# Both passes matter. Without NO_COLOR the comparison catches style-assignment
# bugs; with it, the escape sequences vanish and any difference left is a
# genuine wrapping or width bug.

set -eu

ROOT=$(cd "$(dirname "$0")/.." && pwd)
GO_BIN=${1:-$ROOT/bin/tutor-host}
WIDTHS="40 60 72 100 200"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

[ -x "$GO_BIN" ] || {
    echo "no binary at $GO_BIN — run: sh bin/build-tui.sh" >&2
    exit 1
}

cd "$ROOT"

# HELP and the empty-part placeholder are rendered strings that no file in
# content/ covers, and both use markdown no article happens to.
python3 - "$TMP" <<'PY'
import sys
sys.path.insert(0, ".")
from tui import layout
from tui.app import _EMPTY_DOC

out = sys.argv[1]
open(out + "/_help.md", "w").write(layout.HELP)
open(out + "/_empty.md", "w").write(_EMPTY_DOC)
PY

FILES=$(find content -name '*.md' | sort)
FILES="$FILES $TMP/_help.md $TMP/_empty.md"

checked=0
failed=0

for file in $FILES; do
    for width in $WIDTHS; do
        for mode in color plain; do
            if [ "$mode" = plain ]; then
                NO_COLOR=1 python3 -m tui.render "$file" "$width" > "$TMP/py" 2>"$TMP/pyerr" || {
                    echo "python failed on $file $width"; cat "$TMP/pyerr"; failed=$((failed + 1)); continue; }
                NO_COLOR=1 "$GO_BIN" render "$file" "$width" > "$TMP/go"
            else
                python3 -m tui.render "$file" "$width" > "$TMP/py" 2>"$TMP/pyerr" || {
                    echo "python failed on $file $width"; cat "$TMP/pyerr"; failed=$((failed + 1)); continue; }
                "$GO_BIN" render "$file" "$width" > "$TMP/go"
            fi

            checked=$((checked + 1))
            if ! cmp -s "$TMP/py" "$TMP/go"; then
                failed=$((failed + 1))
                echo "DIFF  $file  width=$width  $mode"
                diff "$TMP/py" "$TMP/go" | head -20 | cat -v
            fi
        done
    done
done

# Whole screens, not just article bodies. The tab bar, the sectioned sidebar
# and the status line are composed by code the render loop above never
# touches, so without this pass the chrome ships unverified.
#
# TUTOR_HOME is pinned because the two sides find the corpus differently: the
# binary walks $TUTOR_HOME, then next to itself, then a pointer file in
# ~/.local/share, while the Python side resolves from its own __file__. A
# stale pointer would diff two different corpora and look like a bug here.
export TUTOR_HOME="$ROOT"
IDS=$(python3 - <<'PY'
import json
with open("content/index.json", encoding="utf-8") as fh:
    index = json.load(fh)
for part in index.get("parts", []):
    for article in part.get("articles", []):
        print(article["id"])
PY
)
SIZES="60x15 72x24 100x24 200x40"

for id in $IDS "" ; do
    for size in $SIZES; do
        cols=${size%x*}
        rows=${size#*x}
        for mode in normal help search; do
            set -- "$cols" "$rows" "$id" "$mode"
            if [ "$mode" = search ]; then
                set -- "$@" shell
            fi
            python3 -m tui.frame "$@" > "$TMP/py" 2>"$TMP/pyerr" || {
                echo "python failed on frame $id $size $mode"; cat "$TMP/pyerr"
                failed=$((failed + 1)); continue; }
            "$GO_BIN" frame "$@" > "$TMP/go"

            checked=$((checked + 1))
            if ! cmp -s "$TMP/py" "$TMP/go"; then
                failed=$((failed + 1))
                echo "DIFF  frame $id  $size  $mode"
                diff "$TMP/py" "$TMP/go" | head -20 | cat -v
            fi
        done
    done
done

# Read marks
#
# The frame pass above drives no keyboard input at all, so `m` is never
# pressed and every frame it checks is the reader's default, unmarked state.
# The tick sidebarRows draws when app.read says an article is marked
# (layout.go) is real output composed by the same width- and mode-sensitive
# code as every other row, so trusting the pass above to have exercised it
# by accident would be trusting an empty read.json to stand in for a used
# one. This pass gives it a fixture instead: a read.json with marks already
# in it, read back through $TUTOR_STATE the same way TUTOR_HOME pins the
# corpus above, so every frame below carries both a ticked and an unticked
# row to compare.
mkdir -p "$TMP/state"
SAMPLE_IDS=$(python3 - "$TMP/state/read.json" <<'PY'
import json
import sys

out = sys.argv[1]
with open("content/index.json", encoding="utf-8") as fh:
    index = json.load(fh)
ids = [a["id"] for part in index.get("parts", []) for a in part.get("articles", [])]

# Every other id is "read", so every frame below shows both a ticked row and
# an unticked one to compare.
marked = sorted(i for n, i in enumerate(ids) if n % 2 == 0)
with open(out, "w", encoding="utf-8") as fh:
    json.dump({"read": marked}, fh, indent=2, ensure_ascii=False)
    fh.write("\n")

# Roughly every eighth id, about fifteen of them: the tick is composed
# identically for every article, so what varies here is width and mode, not
# which article happens to be open.
for n, i in enumerate(ids):
    if n % 8 == 0:
        print(i)
PY
)

sampled=$(printf '%s\n' $SAMPLE_IDS | grep -c .)
total=$(printf '%s\n' $IDS | grep -c .)
echo "read-marks pass: sampling $sampled of $total articles"

for id in $SAMPLE_IDS; do
    for size in $SIZES; do
        cols=${size%x*}
        rows=${size#*x}
        # help replaces the whole body and draws no sidebar, so there is no
        # tick to compare there — only normal and search draw one.
        for mode in normal search; do
            set -- "$cols" "$rows" "$id" "$mode"
            if [ "$mode" = search ]; then
                set -- "$@" shell
            fi
            TUTOR_STATE="$TMP/state" python3 -m tui.frame "$@" > "$TMP/py" 2>"$TMP/pyerr" || {
                echo "python failed on read-marks frame $id $size $mode"; cat "$TMP/pyerr"
                failed=$((failed + 1)); continue; }
            TUTOR_STATE="$TMP/state" "$GO_BIN" frame "$@" > "$TMP/go"

            checked=$((checked + 1))
            if ! cmp -s "$TMP/py" "$TMP/go"; then
                failed=$((failed + 1))
                echo "DIFF  read-marks frame $id  $size  $mode"
                diff "$TMP/py" "$TMP/go" | head -20 | cat -v
            fi
        done
    done
done

echo
echo "$checked comparisons, $failed differing."
[ "$failed" -eq 0 ] || exit 1

# The index is the other artefact both implementations produce.
python3 tui/tutor.py index > /dev/null
cp content/index.json "$TMP/index-py.json"
"$GO_BIN" index > /dev/null
if cmp -s "$TMP/index-py.json" content/index.json; then
    echo "index.json identical."
else
    echo "index.json DIFFERS:"
    diff "$TMP/index-py.json" content/index.json | head -20
    exit 1
fi
