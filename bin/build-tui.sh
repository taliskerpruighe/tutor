#!/bin/sh
# Cross-compile the reader.
#
#   sh bin/build-tui.sh
#   -> tui/bin/tutor-darwin-arm64   (ad-hoc signed by Go's own linker)
#   -> tui/bin/tutor-darwin-amd64
#   -> bin/tutor-host               (this machine; testing only, never shipped)
#
# CGO_ENABLED=0 keeps the internal linker in play, which is what applies the
# ad-hoc signature on darwin/arm64 — Apple Silicon refuses to execute an
# unsigned Mach-O, and there is no codesign(1) on this machine to do it after
# the fact. `verify` below is the check that this actually happened.

set -eu

ROOT=$(cd "$(dirname "$0")/.." && pwd)
OUT="$ROOT/tui/bin"

# The version-agreement gate. The version lives in three places: version.txt
# (what the reader downloads over HTTPS to check for an update), the compiled
# `const version` in go/main.go (what the shipped binary actually reports),
# and VERSION in tui/tutor.py (the same constant kept in the parity oracle).
# If version.txt drifts from the compiled constant, the update check breaks
# silently in one of two directions: the reader never sees a real update, or
# it loops forever offering an "update" that is exactly what she already has.
# Check this before spending time compiling, not after.
command -v grep >/dev/null 2>&1 && command -v sed >/dev/null 2>&1 || {
    echo "grep and sed are required." >&2
    exit 1
}

VTXT=$(sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' "$ROOT/version.txt")
VGO=$(grep -m1 '^const version = ' "$ROOT/go/main.go" | sed 's/^const version = "\(.*\)"/\1/')
VPY=$(grep -m1 '^VERSION = ' "$ROOT/tui/tutor.py" | sed 's/^VERSION = "\(.*\)"/\1/')

if [ "$VTXT" != "$VGO" ] || [ "$VTXT" != "$VPY" ]; then
    echo "version mismatch:" >&2
    echo "  version.txt        $VTXT" >&2
    echo "  go/main.go         $VGO" >&2
    echo "  tui/tutor.py       $VPY" >&2
    echo "All three must agree before a build." >&2
    exit 1
fi

command -v go >/dev/null 2>&1 || {
    echo "go is not installed." >&2
    exit 1
}

# The test gate. go/splash_test.go is what proves the launch screen's
# artwork stays inside the rune set that is known to render on her Mac, and
# that its layout arithmetic still lands the version tag on the artwork's
# right edge. There is no other harness that runs go/'s tests, so if this
# step is skipped they simply never run, and a later edit could break either
# property without anything here noticing.
(cd "$ROOT" && go test ./go) || {
    echo "go test ./go failed; fix it before compiling." >&2
    exit 1
}

mkdir -p "$OUT"

for arch in arm64 amd64; do
    CGO_ENABLED=0 GOOS=darwin GOARCH=$arch \
        go build -trimpath -ldflags "-s -w" -o "$OUT/tutor-darwin-$arch" "$ROOT/go"
    printf '  %-28s %s\n' "tui/bin/tutor-darwin-$arch" \
        "$(wc -c < "$OUT/tutor-darwin-$arch" | tr -d ' ') bytes"
done

CGO_ENABLED=0 go build -trimpath -o "$ROOT/bin/tutor-host" "$ROOT/go"
printf '  %-28s %s\n' "bin/tutor-host" "$("$ROOT/bin/tutor-host" --version)"

# The signing gate. An unsigned arm64 binary is killed by the kernel on her
# machine, and that failure would arrive with no useful message, so check it
# here where the message can be clear.
python3 - "$OUT/tutor-darwin-arm64" <<'PY'
import struct, sys

path = sys.argv[1]
data = open(path, "rb").read()
magic = struct.unpack("<I", data[:4])[0]
if magic != 0xFEEDFACF:
    sys.exit("not a 64-bit Mach-O: %s (magic %#x)" % (path, magic))
ncmds = struct.unpack("<I", data[16:20])[0]
off = 32
cmds = []
for _ in range(ncmds):
    cmd, size = struct.unpack("<II", data[off:off + 8])
    cmds.append(cmd)
    off += size
if 0x1D not in cmds:            # LC_CODE_SIGNATURE
    sys.exit("%s carries no ad-hoc signature; Apple Silicon will refuse it." % path)
print("  %-28s ad-hoc signed" % "tui/bin/tutor-darwin-arm64")
PY
