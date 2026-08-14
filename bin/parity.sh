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

# New-article marker
#
# The read-marks pass above pins a fixture so the tick gets exercised at
# all; the same problem exists one layer up for the green N sidebarRows now
# draws (layout.go's isNewArticle) — no keyboard input means no frame above
# was ever opened against a reader who just upgraded, so nothing has
# compared it either. Two fixtures are needed, not one, because the rule has
# two distinct paths through it rather than one path with an empty case:
#
#   - state-new           read.json, no installed file — the upgrading
#     reader, for whom an absent marker counts as differing from the
#     release. Eligible articles that are unread must draw N here.
#   - state-new-installed  the same read.json, plus an installed file
#     holding the CURRENT version — the fresh-install reader, for whom
#     nothing is new because everything she has arrived in the same
#     release she installed. N must be suppressed everywhere, which is
#     worth diffing on its own: it is a distinct comparison the rule
#     makes (installed != version), not merely the read.json fixture
#     with one file missing.
#
# The sample is read.json's own eligible ids — every article whose indexed
# version is in the allowlist, i.e. every article that CAN draw N — plus a
# scattering of older ones, because a frame that only ever opened on an
# eligible article would never prove an older one stays quiet. Ids are never
# hardcoded: the corpus is still being written as this script is, so the
# eligible set is whatever go/layout.go and content/index.json agree on at
# run time.
#
# The allowlist is GREPPED OUT OF go/layout.go rather than copied here. A
# second hand-maintained list of the same versions is the bin/banner-preview.sh
# failure this repo already documents: nothing would gate the two against each
# other, and the copy would drift on the release after whichever one wrote it.
# Note the consequence — this harness cannot catch the Go list itself being
# wrong, only the Python mirror disagreeing with it, which is exactly the
# division of labour parity.sh has everywhere else.
mkdir -p "$TMP/state-new" "$TMP/state-new-installed"

CURRENT_VERSION=$(sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' "$ROOT/version.txt")

NEW_VERSIONS=$(sed -n 's/^var newVersions = \[\]string{\(.*\)}$/\1/p' "$ROOT/go/layout.go" \
    | tr -d '" ' | tr ',' ' ')
[ -n "$NEW_VERSIONS" ] || {
    echo "could not read newVersions out of go/layout.go — the N-marker fixture has nothing to select on" >&2
    exit 1
}
echo "new-marker allowlist from go/layout.go: $NEW_VERSIONS"

NEW_SAMPLE_IDS=$(python3 - "$TMP/state-new/read.json" "$NEW_VERSIONS" <<'PY'
import json
import sys

out, allow = sys.argv[1], set(sys.argv[2].split())
with open("content/index.json", encoding="utf-8") as fh:
    index = json.load(fh)
articles = [a for part in index.get("parts", []) for a in part.get("articles", [])]
ids = [a["id"] for a in articles]
eligible = [a["id"] for a in articles if a.get("version") in allow]
eligible_set = set(eligible)
older = [i for i in ids if i not in eligible_set]

# The allowlist must not have degenerated into "everything unread is new".
# Without this the marker rule could be broken wide open and every frame
# would still agree between the two implementations, because both would be
# wrong in the same way.
if not older:
    sys.exit("every article in the corpus is in the N allowlist — the rule is not being exercised")

# At least one article from a release well behind the allowlist must be in
# the sample, negatively. v0.2.3 is named rather than merely "some older
# version" because it is the oldest release the marker feature has ever
# seen, and an allowlist that swallowed it would have swallowed everything.
stale = [a["id"] for a in articles if a.get("version") == "v0.2.3"]
if not stale:
    sys.exit("no v0.2.3 article left in the corpus — the N-marker negative assertion is not being made")
older = stale + [i for i in older if i not in set(stale)]
print("stale-negative sample: " + stale[0], file=sys.stderr)

# Marking is decided within the eligible list itself, not by a global
# modulo over every id, so that even a small eligible set still lands at
# least one marked and one unmarked member: every other eligible id is
# read, which is what lets a single frame show a ticked new-release
# article (read wins) sitting beside an unticked one (draws N). A
# scattering of older ids is marked too, on the same every-other rule, so
# the read/unread split is not confined to the new release alone.
marked = sorted(i for n, i in enumerate(eligible) if n % 2 == 0)
marked += sorted(i for n, i in enumerate(older) if n % 2 == 0)
with open(out, "w", encoding="utf-8") as fh:
    json.dump({"read": sorted(marked)}, fh, indent=2, ensure_ascii=False)
    fh.write("\n")

sample = list(eligible)
for n, i in enumerate(older):
    if n % 8 == 0:
        sample.append(i)
for i in sample:
    print(i)
PY
)

cp "$TMP/state-new/read.json" "$TMP/state-new-installed/read.json"
printf '%s\n' "$CURRENT_VERSION" > "$TMP/state-new-installed/installed"

new_sampled=$(printf '%s\n' $NEW_SAMPLE_IDS | grep -c .)
new_total=$(printf '%s\n' $IDS | grep -c .)
if [ "$new_sampled" -eq 0 ]; then
    echo "WARNING: new-marker pass selected 0 articles at versions $NEW_VERSIONS — the N rule was not exercised this run" >&2
else
    echo "new-marker pass: sampling $new_sampled of $new_total articles"
fi

for id in $NEW_SAMPLE_IDS; do
    for size in $SIZES; do
        cols=${size%x*}
        rows=${size#*x}
        # help replaces the whole body and draws no sidebar, same reasoning
        # as the read-marks pass above.
        for mode in normal search; do
            set -- "$cols" "$rows" "$id" "$mode"
            if [ "$mode" = search ]; then
                set -- "$@" shell
            fi
            for state in state-new state-new-installed; do
                TUTOR_STATE="$TMP/$state" python3 -m tui.frame "$@" > "$TMP/py" 2>"$TMP/pyerr" || {
                    echo "python failed on new-marker frame $id $size $mode $state"; cat "$TMP/pyerr"
                    failed=$((failed + 1)); continue; }
                TUTOR_STATE="$TMP/$state" "$GO_BIN" frame "$@" > "$TMP/go"

                checked=$((checked + 1))
                if ! cmp -s "$TMP/py" "$TMP/go"; then
                    failed=$((failed + 1))
                    echo "DIFF  new-marker frame $id  $size  $mode  $state"
                    diff "$TMP/py" "$TMP/go" | head -20 | cat -v
                fi
            done
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
