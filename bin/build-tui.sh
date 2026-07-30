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

command -v go >/dev/null 2>&1 || {
    echo "go is not installed." >&2
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
