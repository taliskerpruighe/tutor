// Proof that the launch screen renders correctly on a Mac nobody running
// this test suite can actually see. Nothing enforced its rune set before
// this file, and a later edit could slip in a character whose macOS
// behaviour nobody had reasoned about. These tests fail on the build
// machine instead of on her screen.
//
// The screen now depends on a font on the reader's machine: the robot crest
// is U+F16A0, which exists only in Nerd Fonts. That assumption holds for
// this reader because content/03-the-cli/13-powerline-themes.md states the
// terminal is set to Hack Nerd Font rather than plain Hack — without it,
// the article notes, the powerline seams would render as empty boxes. Hack
// Nerd Font carries U+F16A0. A TUI cannot ask the terminal what its font
// covers, so there is no detection behind this, only the one explicit
// escape hatch: setting TUTOR_ASCII to any non-empty value omits the crest
// and restores the screen exactly as it was before the glyph landed.
package main

import (
	"fmt"
	"sort"
	"strings"
	"testing"
)

// splashRunes is the launch screen's allow-set: every non-ASCII rune it is
// permitted to print, with the name it is allowed under. Keeping it as a
// map rather than a run of special cases in checkRunes means the gate reads
// as a statement of policy, and the failure message can name the whole set
// without anyone having to keep prose in step with code.
var splashRunes = map[rune]string{
	'█':          "U+2588 FULL BLOCK",
	'\U000F16A0': "U+F16A0 nf-md-robot-confused (Nerd Fonts)",
}

// allowedRunes renders splashRunes for a failure message. Map iteration
// order is random in Go, so the names are sorted — a test that fails with a
// different message each run is a test nobody trusts.
func allowedRunes() string {
	names := make([]string, 0, len(splashRunes))
	for _, name := range splashRunes {
		names = append(names, name)
	}
	sort.Strings(names)
	return strings.Join(names, ", ")
}

// checkRunes walks every rune of s and fails the test on the first one
// outside the set the launch screen is allowed to use: printable ASCII,
// plus whatever splashRunes explicitly admits.
func checkRunes(t *testing.T, label, s string) {
	t.Helper()
	for _, r := range s {
		if _, ok := splashRunes[r]; ok {
			continue
		}
		if r < 0x20 || r > 0x7E {
			t.Fatalf("%s contains rune %q (U+%04X), outside printable ASCII and %s", label, r, r, allowedRunes())
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
	checkRunes(t, "glyph line", glyphLinePlain())
	checkRunes(t, "narrow glyph line", narrowGlyphLinePlain())
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

// TestGlyphCodepoint pins the crest to the exact codepoint it is meant to
// be. U+F16A0 lives in Supplementary Private Use Area-B, where an editor, a
// patch tool or a copy-paste that shifted it by one would still render as
// *something* in a Nerd Font — a different icon entirely, but an icon — so
// the mistake would never be caught by eye. This is the only thing standing
// between a mangled literal and a robot that quietly became a teapot.
func TestGlyphCodepoint(t *testing.T) {
	if robotRune != rune(0xF16A0) {
		t.Fatalf("robotRune = U+%04X, want U+F16A0 (nf-md-robot-confused)", robotRune)
	}
	runes := []rune(robotGlyph)
	if len(runes) != 1 {
		t.Fatalf("robotGlyph is %d runes (%q), want exactly 1 — the literal has been mangled", len(runes), robotGlyph)
	}
	if runes[0] != rune(0xF16A0) {
		t.Fatalf("robotGlyph holds U+%04X, want U+F16A0", runes[0])
	}
}

// TestGlyphCharWidth pins the assumption the centring arithmetic rests on,
// the same way TestBlockCharWidth pins it for the block character. The
// Private Use Area appears in neither range table in width_table.go, so
// U+F16A0 falls through to the default of one column — which is what
// glyphPad divides by two. A regenerated width table that reclassified the
// PUA as wide would silently shift the crest off centre; this is what would
// catch it.
func TestGlyphCharWidth(t *testing.T) {
	if w := charWidth(robotRune); w != 1 {
		t.Fatalf("charWidth(robotRune) = %d, want 1 (the PUA is in neither width range table)", w)
	}
}

// TestGlyphLineCentred is the only check on the crest line's shape. The
// line is deliberately kept out of TestSplashLayout's column-width
// assertions, because a Nerd Font glyph can render wider than the one cell
// charWidth measures it as, and an exact-width assertion would then fail on
// a screen that looked perfectly correct. What can still be asserted is
// what the code computed: the pad is the centring expression itself, not a
// number written down twice, so if splashWidth or the glyph's measured
// width moves, the layout and this test move together instead of
// contradicting each other.
func TestGlyphLineCentred(t *testing.T) {
	cases := []struct {
		label string
		line  string
		want  int
	}{
		{"wide", glyphLinePlain(), (splashWidth - dwidth(robotGlyph)) / 2},
		{"narrow", narrowGlyphLinePlain(), (dwidth(narrowWord()) - dwidth(robotGlyph)) / 2},
	}
	for _, c := range cases {
		lead := len(c.line) - len(strings.TrimLeft(c.line, " "))
		if lead != c.want {
			t.Errorf("%s glyph line has %d leading spaces, want %d (%q)", c.label, lead, c.want, c.line)
		}
		if rest := []rune(strings.TrimLeft(c.line, " ")); len(rest) != 1 {
			t.Errorf("%s glyph line carries %d non-space runes, want exactly 1 (%q)", c.label, len(rest), c.line)
		}
	}
}

// TestAsciiOnlySuppressesGlyph proves the escape hatch is a true escape
// hatch: with TUTOR_ASCII set, the screen is byte-identical to the one this
// repo shipped before the crest existed — nine lines, no glyph, and no
// orphaned blank line where it used to sit. A reader whose font cannot draw
// the robot gets back exactly the screen she had, not a screen with a hole
// in it.
//
// The flag is assigned directly rather than through os.Setenv, and restored
// with defer. asciiOnly is evaluated once at package initialisation, the
// same as noColor at term.go:77; setting the environment from inside a test
// function happens long after init and would change nothing at all.
func TestAsciiOnlySuppressesGlyph(t *testing.T) {
	saved := asciiOnly
	defer func() { asciiOnly = saved }()
	asciiOnly = true

	want := []string{""}
	for row := 0; row < 5; row++ {
		want = append(want, artworkRowPlain(row))
	}
	want = append(want, "", subtitlePlain(), versionLinePlain())

	got := fullSplashPlain()
	if len(got) != len(want) {
		t.Fatalf("TUTOR_ASCII screen has %d lines, want %d", len(got), len(want))
	}
	for i := range want {
		if got[i] != want[i] {
			t.Errorf("TUTOR_ASCII line %d = %q, want %q", i, got[i], want[i])
		}
	}

	narrow := narrowSplashPlain()
	wantNarrow := []string{narrowWord(), narrowSubtitle, versionTag()}
	if len(narrow) != len(wantNarrow) {
		t.Fatalf("TUTOR_ASCII narrow screen has %d lines, want %d", len(narrow), len(wantNarrow))
	}
	for i := range wantNarrow {
		if narrow[i] != wantNarrow[i] {
			t.Errorf("TUTOR_ASCII narrow line %d = %q, want %q", i, narrow[i], wantNarrow[i])
		}
	}
}
