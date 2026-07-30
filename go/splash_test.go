// Proof that the launch screen renders correctly on a Mac nobody running
// this test suite can actually see — the rune set is one this codebase
// already ships (splash.go's package comment and the plan behind it explain
// why), but nothing enforced that before this file, and a later edit could
// have slipped in a character whose macOS behaviour nobody had reasoned
// about. These tests fail on the build machine instead of on her screen.
package main

import (
	"fmt"
	"testing"
)

// checkRunes walks every rune of s and fails the test on the first one
// outside the set the launch screen is allowed to use: printable ASCII, and
// the single block character the artwork draws with.
func checkRunes(t *testing.T, label, s string) {
	t.Helper()
	for _, r := range s {
		if r == '█' {
			continue
		}
		if r < 0x20 || r > 0x7E {
			t.Fatalf("%s contains rune %q (U+%04X), outside printable ASCII and U+2588 FULL BLOCK", label, r, r)
		}
	}
}

// TestSplashRuneWhitelist is the check the user asked for. Every string the
// launch screen ever prints is tested here in its Plain form, deliberately
// bypassing colorRun: an SGR escape sequence's leading ESC (0x1b) would
// itself fail this whitelist, so testing the plain, uncoloured content is
// what actually answers "will the characters render", not an artifact of
// how they are coloured.
func TestSplashRuneWhitelist(t *testing.T) {
	for row := 0; row < 5; row++ {
		checkRunes(t, fmt.Sprintf("artwork row %d", row), artworkRowPlain(row))
	}
	checkRunes(t, "subtitle", subtitle)
	checkRunes(t, "narrow word", narrowWord())
	checkRunes(t, "narrow subtitle", narrowSubtitle)
	checkRunes(t, "version tag", versionTag())
}

// TestBlockCharWidth guards the one fact that could have silently broken
// the whole layout: Python's unicodedata classifies U+2588 as East Asian
// Width "Ambiguous", not "Wide". Had this codebase's width table counted
// Ambiguous as wide, every block in the artwork would measure two columns
// instead of one, every row would come out twice as wide as intended, and
// the version tag would right-align to the wrong column. It does not, but
// nothing stopped a regenerated width table from reclassifying it — this
// test is what would catch that the moment it happened.
func TestBlockCharWidth(t *testing.T) {
	if w := charWidth('█'); w != 1 {
		t.Fatalf("charWidth('█') = %d, want 1 (U+2588 is East Asian Width Ambiguous, not Wide)", w)
	}
}

// TestSplashLayout checks the arithmetic the plan specifies: every artwork
// row is exactly splashWidth columns, and the version tag's last character
// lands on splashWidth too, so the tag stays flush with the artwork's right
// edge regardless of how long the version string itself is.
func TestSplashLayout(t *testing.T) {
	for row := 0; row < 5; row++ {
		line := artworkRowPlain(row)
		if w := dwidth(line); w != splashWidth {
			t.Errorf("artwork row %d measures %d columns, want %d (%q)", row, w, splashWidth, line)
		}
	}

	verLine := versionLinePlain()
	if w := dwidth(verLine); w != splashWidth {
		t.Errorf("version line measures %d columns, want %d (%q)", w, splashWidth, verLine)
	}
}
