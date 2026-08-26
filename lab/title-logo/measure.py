#!/usr/bin/env python3
"""Measure title-logo art files: per line, rune count and display width.

Display width mirrors go/width_table.go (generated from Python unicodedata):
East Asian Width W/F count 2, everything else printable counts 1, and
East Asian Ambiguous counts 1 — the same policy TestBlockCharWidth pins.

Usage: measure.py FILE EXPECT_HEIGHT EXPECT_WIDTH TIER
  TIER is 'halfblock' (repertoire: space + U+2580/2584/2588) or
  'ascii' (printable ASCII only). Exits non-zero on any violation.
"""
import sys, unicodedata

HALFBLOCK = set(" ▀▄█")

def cwidth(ch):
    if unicodedata.east_asian_width(ch) in ("W", "F"):
        return 2
    if unicodedata.combining(ch):
        return 0
    return 1

def main():
    path, want_h, want_w, tier = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    lines = open(path, encoding="utf-8").read().split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    ok = True
    print(f"{path}  (want {want_h} rows x {want_w} cols, tier={tier})")
    for i, line in enumerate(lines):
        runes = len(line)
        width = sum(cwidth(c) for c in line)
        bad = []
        if width != want_w:
            bad.append(f"width {width} != {want_w}")
        for c in line:
            if tier == "halfblock" and c not in HALFBLOCK:
                bad.append(f"rune U+{ord(c):04X} outside half-block repertoire"); break
            if tier == "ascii" and not (0x20 <= ord(c) <= 0x7E):
                bad.append(f"rune U+{ord(c):04X} outside printable ASCII"); break
        flag = "  FAIL: " + "; ".join(bad) if bad else ""
        print(f"  row {i}: runes={runes:2d} display_width={width:2d}{flag}")
        if bad:
            ok = False
    if len(lines) != want_h:
        print(f"  FAIL: {len(lines)} rows, want {want_h}")
        ok = False
    print("  OK" if ok else "  FAILED")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
