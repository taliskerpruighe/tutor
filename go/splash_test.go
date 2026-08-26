// Proof that the launch screen renders correctly on a Mac nobody running
// this test suite can actually see. Nothing enforced its rune set before
// this file, and a later edit could slip in a character whose macOS
// behaviour nobody had reasoned about. These tests fail on the build
// machine instead of on her screen.
//
// The screen's rune set is printable ASCII, the Block Elements repertoire the
// wordmark proves at runtime (█ U+2588, the letters themselves), and the
// Braille Patterns block U+2800-28FF, which the robot logo beside them is
// drawn from. There is no Private Use Area codepoint anywhere in this
// package, but braille is a weaker guarantee than the block elements were:
// it is not in the Nerd Fonts repertoire and not in the range the wordmark
// uses, so it renders out of whatever fallback font the machine happens to
// have (lab/glyph-blowup/NOTES.md), and coverage on the shipped audience's
// stock macOS is unverified. A TUI cannot ask the terminal what its font
// covers, so TUTOR_ASCII is no longer a cosmetic preference but the actual
// remedy: set to any non-empty value, it swaps the braille robot for a
// plain-ASCII one of the same dimensions instead of hiding it.
package main

import (
	"fmt"
	"sort"
	"strings"
	"testing"
	"unicode/utf8"
)

// splashRunes is the launch screen's allow-set: every non-ASCII rune it is
// permitted to print, with the name it is allowed under. Keeping it as a
// map rather than a run of special cases in checkRunes means the gate reads
// as a statement of policy, and the failure message can name the whole set
// without anyone having to keep prose in step with code.
var splashRunes = map[rune]string{
	'█': "U+2588 FULL BLOCK",
	'▀': "U+2580 UPPER HALF BLOCK",
	'▄': "U+2584 LOWER HALF BLOCK",
}

// splashRuneRanges is the allow-set's second half: whole blocks the screen
// may draw from, rather than named individual runes. The robot logo uses
// most of the 256 braille cells and its "blank" cell is U+2800 BRAILLE
// PATTERN BLANK — not a space — so enumerating them one by one would be a
// 256-entry table that says less than one range does.
var splashRuneRanges = []struct {
	lo, hi rune
	name   string
}{
	{0x2800, 0x28FF, "U+2800-28FF BRAILLE PATTERNS"},
}

// inSplashRanges reports whether r falls in any admitted block.
func inSplashRanges(r rune) bool {
	for _, rg := range splashRuneRanges {
		if r >= rg.lo && r <= rg.hi {
			return true
		}
	}
	return false
}

// allowedRunes renders splashRunes for a failure message. Map iteration
// order is random in Go, so the names are sorted — a test that fails with a
// different message each run is a test nobody trusts.
func allowedRunes() string {
	names := make([]string, 0, len(splashRunes)+len(splashRuneRanges))
	for _, name := range splashRunes {
		names = append(names, name)
	}
	for _, rg := range splashRuneRanges {
		names = append(names, rg.name)
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
		if inSplashRanges(r) {
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
//
// All logoRows composed rows are checked in both tier states — half-block default
// and TUTOR_ASCII — because robotRow's branch means each tier exercises a
// different rune set on the very same rows.
func TestSplashRuneWhitelist(t *testing.T) {
	saved := asciiOnly
	defer func() { asciiOnly = saved }()

	for _, tier := range []bool{false, true} {
		asciiOnly = tier
		for row := 0; row < logoRows; row++ {
			checkRunes(t, fmt.Sprintf("composed row %d (asciiOnly=%v)", row, tier), composedRowPlain(row))
		}
	}
	asciiOnly = saved

	for row := 0; row < 5; row++ {
		checkRunes(t, fmt.Sprintf("artwork row %d", row), artworkRowPlain(row))
	}
	checkRunes(t, "subtitle", subtitle)
	checkRunes(t, "narrow word", narrowWord())
	checkRunes(t, "narrow subtitle", narrowSubtitle)
	checkRunes(t, "version tag", versionTag())
}

// TestBlockCharWidth guards the one fact that could have silently broken
// the whole layout: Python's unicodedata classifies U+2588, U+2580 and
// U+2584 all as East Asian Width "Ambiguous", not "Wide". Had this
// codebase's width table counted Ambiguous as wide, every block in the
// wordmark and the robot would measure two columns instead of one, every
// row would come out wider than intended, and the version tag would
// right-align to the wrong column. It does not, but nothing stops a
// regenerated width table from reclassifying any of the three — this test
// is what would catch that the moment it happened.
func TestBlockCharWidth(t *testing.T) {
	for _, r := range []rune{'█', '▀', '▄'} {
		if w := charWidth(r); w != 1 {
			t.Errorf("charWidth(%q) = %d, want 1 (East Asian Width Ambiguous, not Wide)", r, w)
		}
	}
}

// TestBrailleCharWidth is TestBlockCharWidth's twin for the range the robot
// logo is actually drawn from, and it is measured rather than taken on
// trust from a spec note. The whole logoCols budget rests on every braille
// cell being one column wide; U+2800-28FF is East Asian Width "Neutral",
// but the failure mode is identical to the block elements' — one
// reclassification in a regenerated width_table.go and every composed row
// silently measures 82 runes at 164 columns.
//
// The three sampled cells are the ones the layout depends on most: the
// blank that pads every short row, the full cell that fills the robot's
// solid mass, and one mid-density cell from the art itself.
func TestBrailleCharWidth(t *testing.T) {
	for _, r := range []rune{'⠀', '⣿', '⢀'} {
		if w := charWidth(r); w != 1 {
			t.Errorf("charWidth(%q) (U+%04X) = %d, want 1", r, r, w)
		}
	}
}

// TestBrailleBlankIsNotSpace pins the fact that makes the art table's
// "transcribed by a generator, never retyped" rule load-bearing rather than
// stylistic: the pad character in robotArt is U+2800 BRAILLE PATTERN BLANK,
// which looks exactly like a space, measures exactly like a space, and is
// not a space. Anything that "tidies trailing whitespace" leaves it alone;
// anything that retypes a row by eye replaces it with U+0020 and changes
// which font is asked to draw that cell. If a future edit ever does
// normalise them to spaces, this fails and says why.
func TestBrailleBlankIsNotSpace(t *testing.T) {
	saved := asciiOnly
	defer func() { asciiOnly = saved }()
	asciiOnly = false

	found := false
	for row := 0; row < logoRows; row++ {
		for _, r := range robotRow(row) {
			if r == '\u2800' {
				found = true
			}
			if r == ' ' {
				t.Errorf("robotArt row %d contains an ASCII space; braille rows pad with U+2800 BRAILLE PATTERN BLANK", row)
				break
			}
		}
	}
	if !found {
		t.Error("robotArt contains no U+2800 BRAILLE PATTERN BLANK — the art table has been retyped or replaced")
	}
}

// TestRobotColorsPalette proves the claim splash.go makes about the logo's
// colouring: it introduces no colour of its own, it is headColors — the
// wordmark's own five stops — swept down the rows with the same bucket
// arithmetic subtitleColored uses across its characters. Written out as a
// literal table for readability, robotColors could drift from that rule in
// a single mistyped digit and nothing else would notice.
func TestRobotColorsPalette(t *testing.T) {
	for row, got := range robotColors {
		want := headColors[row*len(headColors)/logoRows]
		if got != want {
			t.Errorf("robotColors[%d] = %d, want %d (headColors[%d*%d/%d])",
				row, got, want, row, len(headColors), logoRows)
		}
	}
}

// TestSplashLayout checks the arithmetic the plan specifies: every composed
// row of the logo screen is exactly composedWidth columns, in both tier
// states, and the logo-screen version line matches it; and the mid screen's
// artwork rows and version line still measure splashWidth, unaffected by
// any of this.
func TestSplashLayout(t *testing.T) {
	saved := asciiOnly
	defer func() { asciiOnly = saved }()

	for _, tier := range []bool{false, true} {
		asciiOnly = tier
		for row := 0; row < logoRows; row++ {
			line := composedRowPlain(row)
			if w := dwidth(line); w != composedWidth {
				t.Errorf("composed row %d (asciiOnly=%v) measures %d columns, want %d (%q)", row, tier, w, composedWidth, line)
			}
		}
	}
	asciiOnly = saved

	verLine := versionLineWidePlain()
	if w := dwidth(verLine); w != composedWidth {
		t.Errorf("logo-screen version line measures %d columns, want %d (%q)", w, composedWidth, verLine)
	}

	for row := 0; row < 5; row++ {
		line := artworkRowPlain(row)
		if w := dwidth(line); w != splashWidth {
			t.Errorf("artwork row %d measures %d columns, want %d (%q)", row, w, splashWidth, line)
		}
	}

	midVer := versionLinePlain()
	if w := dwidth(midVer); w != splashWidth {
		t.Errorf("mid-screen version line measures %d columns, want %d (%q)", w, splashWidth, midVer)
	}
}

// artTables lists both robot art tables in a fixed order, name alongside
// value, so the two dimension tests below produce a deterministic log
// (map iteration order is random in Go, and a measurement record whose row
// order changes between runs is not one a reader can check by eye).
var artTables = []struct {
	name  string
	table [logoRows]string
}{
	{"robotArt", robotArt},
	{"robotAscii", robotAscii},
}

// TestArtTableDimensions is this file's proof that transcription of the art
// from lab/glyph-blowup/full-braille-12r.txt and
// lab/title-logo/robot-fallback.txt into splash.go was not corrupted: every
// row of both tables measures exactly dwidth logoCols, in the same shape as
// the SPEC.md §9 measurement record produced against the source files
// themselves — that record's own figures are the superseded 20-column
// half-block art's and are not what this asserts. [logoRows]string array
// types already guarantee the row count at compile time; what needs runtime
// proof is column width, which a byte-level typo could silently change —
// and with U+2800 padding, one that no amount of squinting at the source
// would reveal. Every row is logged (t.Logf, visible under -v) in
// the same shape as SPEC.md §9's record, so this in-process measurement of
// the actual Go values can be read directly against it.
func TestArtTableDimensions(t *testing.T) {
	for _, tt := range artTables {
		for row, line := range tt.table {
			w := dwidth(line)
			t.Logf("%s row %d: runes=%d display_width=%d", tt.name, row, utf8.RuneCountInString(line), w)
			if w != logoCols {
				t.Errorf("%s row %d measures %d display columns, want %d (%q)", tt.name, row, w, logoCols, line)
			}
		}
	}
}

// TestArtTableRuneCount is TestArtTableDimensions' complementary half: rune
// count rather than display width. The failure mode this catches that the
// other test cannot: a row with the wrong number of runes that nonetheless
// happens to measure logoCols display columns — e.g. 19 runes where one of them
// is width-2 (there are none in this codebase's width table for the runes
// in play here, but the two checks are cheap and independent, so a future
// change to width_table.go could not silently make one test redundant
// without the other still catching a corrupted row).
func TestArtTableRuneCount(t *testing.T) {
	for _, tt := range artTables {
		for row, line := range tt.table {
			if n := utf8.RuneCountInString(line); n != logoCols {
				t.Errorf("%s row %d has %d runes, want %d (%q)", tt.name, row, n, logoCols, line)
			}
		}
	}
}

// fillerRows returns the composed rows that carry no wordmark, derived from
// wordmarkTopRow rather than written out. The old hardcoded {0, 1, 7, 8}
// was correct for a 9-row robot with the wordmark on rows 2-6 and silently
// wrong for anything else — with 12 rows and wordmarkTopRow 4, rows 7 and 8
// now carry wordmark and rows 9-11 do not. Deriving it means the two tests
// below cannot disagree with splash.go about where the band sits.
func fillerRows() []int {
	var rows []int
	for row := 0; row < logoRows; row++ {
		if row < wordmarkTopRow || row >= wordmarkTopRow+5 {
			rows = append(rows, row)
		}
	}
	return rows
}

// TestWordmarkCentredOnRobot is the only check on the composed block's
// vertical placement: the 5-row wordmark sits on composed rows
// wordmarkTopRow..wordmarkTopRow+4 and nowhere else. Rows in that band end
// in the exact wordmark row; rows outside it are the robot row, the gutter,
// and nothing but a full splashWidth-space filler — checked by exact
// equality, not just a trailing-space count, since the robot's own rows
// (e.g. row 0's antenna) already end in many blank cells of their own and a
// bare count could not tell "filler" from "coincidentally blank robot art".
// With braille art the distinction is sharper still: the robot's blanks are
// U+2800 and the filler's are U+0020, so a test that counted "blank-looking
// columns" would be measuring two different characters as one.
func TestWordmarkCentredOnRobot(t *testing.T) {
	for k := 0; k < 5; k++ {
		row := wordmarkTopRow + k
		got := composedRowPlain(row)
		want := artworkRowPlain(k)
		if !strings.HasSuffix(got, want) {
			t.Errorf("composed row %d does not end with artwork row %d\n got:  %q\n want suffix: %q", row, k, got, want)
		}
	}

	filler := strings.Repeat(" ", splashWidth)
	for _, row := range fillerRows() {
		got := composedRowPlain(row)
		want := robotRow(row) + robotGutter + filler
		if got != want {
			t.Errorf("composed row %d = %q, want %q (robot + gutter + %d-space filler)", row, got, want, splashWidth)
		}
	}
}

// TestAsciiOnlySwapsTier proves TUTOR_ASCII does what section 5 of the spec
// says it now does: it no longer hides anything, it swaps which robot tier
// is drawn. With asciiOnly set, robotRow itself is pure printable ASCII for
// all logoRows rows (proving the swap happened) and every composed row is
// still exactly composedWidth columns; the line count of the logo screen is identical
// between tiers (no orphaned or missing blank line); the narrow screen
// carries no robot in either state, because it never reaches robotRow at
// all; and the mid screen is byte-identical in both states, since the
// hatch touches nothing but the robot and the mid screen has no robot to
// touch.
//
// This deliberately checks robotRow(row), not the full composedRowPlain(row):
// asciiOnly only ever selects between robotArt and robotAscii (splash.go's
// robotRow) — it does not touch the wordmark's own glyphs table, which is
// built from █ in every tier. The wordmark band therefore always carries █
// regardless of TUTOR_ASCII; that is unchanged, correct behaviour, not
// something this hatch was ever meant to affect, so asserting ASCII-only
// across the *whole* composed row would be a false requirement that fails
// against splash.go working exactly as designed.
//
// The flag is assigned directly rather than through os.Setenv, and restored
// with defer. asciiOnly is evaluated once at package initialisation, the
// same as noColor at term.go:77; setting the environment from inside a test
// function happens long after init and would change nothing at all.
func TestAsciiOnlySwapsTier(t *testing.T) {
	savedAscii := asciiOnly
	defer func() { asciiOnly = savedAscii }()

	asciiOnly = false
	blockLines := logoSplashPlain()

	asciiOnly = true
	asciiLines := logoSplashPlain()

	if len(asciiLines) != len(blockLines) {
		t.Fatalf("TUTOR_ASCII logo screen has %d lines, want %d (same as the half-block tier)", len(asciiLines), len(blockLines))
	}

	for row := 0; row < logoRows; row++ {
		if w := dwidth(composedRowPlain(row)); w != composedWidth {
			t.Errorf("TUTOR_ASCII composed row %d measures %d columns, want %d", row, w, composedWidth)
		}
		for _, r := range robotRow(row) {
			if r < 0x20 || r > 0x7E {
				t.Errorf("TUTOR_ASCII robotRow(%d) contains rune %q (U+%04X), not printable ASCII", row, r, r)
			}
		}
	}

	// The filler rows carry no wordmark (see TestWordmarkCentredOnRobot), so
	// in the ASCII tier the *entire* composed row — robot, gutter and filler
	// alike — is pure printable ASCII, recovering the literal row-level claim
	// for the rows where it actually holds.
	for _, row := range fillerRows() {
		for _, r := range composedRowPlain(row) {
			if r < 0x20 || r > 0x7E {
				t.Errorf("TUTOR_ASCII composed row %d contains rune %q (U+%04X), not printable ASCII", row, r, r)
			}
		}
	}

	asciiOnly = false
	narrowBlock := narrowSplashPlain()
	asciiOnly = true
	narrowAscii := narrowSplashPlain()

	if len(narrowBlock) != len(narrowAscii) {
		t.Fatalf("narrow screen line count differs between tiers: %d vs %d", len(narrowBlock), len(narrowAscii))
	}
	for i := range narrowBlock {
		if narrowBlock[i] != narrowAscii[i] {
			t.Errorf("narrow screen line %d differs between tiers: %q vs %q", i, narrowBlock[i], narrowAscii[i])
		}
		for _, r := range narrowBlock[i] {
			if r == '▀' || r == '▄' || r == '█' || inSplashRanges(r) {
				t.Errorf("narrow screen line %d contains logo art %q — the narrow screen must never carry a robot", i, r)
			}
		}
	}

	asciiOnly = false
	midBlock := fullSplashPlain()
	asciiOnly = true
	midAscii := fullSplashPlain()

	if len(midBlock) != len(midAscii) {
		t.Fatalf("mid screen line count differs between tiers: %d vs %d", len(midBlock), len(midAscii))
	}
	for i := range midBlock {
		if midBlock[i] != midAscii[i] {
			t.Errorf("mid screen line %d differs between tiers: %q vs %q — TUTOR_ASCII must touch nothing but the robot", i, midBlock[i], midAscii[i])
		}
	}
}

// firstContentLine returns the first non-empty line of a splashLines result.
// The logo and mid screens both open with a blank line; the narrow screen
// does not. Measuring the first non-empty line, rather than lines[0], is
// what makes a single width number distinguish all three bands.
func firstContentLine(lines []string) string {
	for _, l := range lines {
		if l != "" {
			return l
		}
	}
	return ""
}

// TestSplashLinesWidthBands is the new test for the three width bands,
// called directly against the unexported splashLines(width int) []string —
// this file is in the same package, so it can, and doing so in-process is
// deterministic in a way that shelling out to the binary is not:
// detectWidth() calls getWinsize on stdout and silently returns 80 when
// stdout is a pipe, which would defeat exactly this kind of check if it ran
// the built binary under a test harness instead.
//
// noColor is pinned true for the duration: splashLines returns the Colored
// forms, and an SGR escape sequence's digits and semicolons are ordinary
// printable ASCII to charWidth, which would inflate every measured width
// well past the numbers below (this is the same reason splash_test.go
// otherwise prefers the Plain forms, documented at splash.go's Colouring
// comment).
//
// Each width's line count and first-content-row width are checked together
// because either alone is ambiguous: 83 and 55 both fall in the mid band
// and share a line count of 9, but only the row width also confirms
// composedWidth wasn't reached; 84 and 100 share both numbers, proving
// anything at or above logoThreshold lands on the same screen.
//
// 80 is in the table on its own account, and it is the one case here that
// asserts a deliberate regression rather than a preserved property: the
// braille logo is too wide for an 80-column terminal (26 + 3 + 53 = 82), so
// detectWidth's default now lands on the mid screen. Anyone who later
// narrows the art to win that band back will find this line failing, which
// is the point — it should be changed knowingly, not drifted past.
func TestSplashLinesWidthBands(t *testing.T) {
	saved := noColor
	defer func() { noColor = saved }()
	noColor = true

	cases := []struct {
		width     int
		wantLines int
		wantWidth int
	}{
		{100, 16, composedWidth}, // well above logoThreshold: logo screen
		{84, 16, composedWidth},  // == logoThreshold: logo screen, exact fit
		{83, 9, splashWidth},     // one below logoThreshold: mid screen
		{80, 9, splashWidth},     // detectWidth's default: mid screen, NOT the logo
		{55, 9, splashWidth},     // == narrowThreshold: mid screen
		{54, 3, 5},               // one below narrowThreshold: narrow screen ("TUTOR")
	}

	for _, c := range cases {
		lines := splashLines(c.width)
		if len(lines) != c.wantLines {
			t.Errorf("splashLines(%d) has %d lines, want %d", c.width, len(lines), c.wantLines)
		}
		first := firstContentLine(lines)
		if w := dwidth(first); w != c.wantWidth {
			t.Errorf("splashLines(%d) first content row measures %d columns, want %d (%q)", c.width, w, c.wantWidth, first)
		}
	}
}
