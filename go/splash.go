// The launch screen for `tutor` — five seconds of block-letter artwork,
// modelled on oh-my-zsh's update banner. At logoThreshold columns and up, a
// braille robot head stands beside the TUTOR wordmark: U+2800-28FF, 2x4
// dots per cell, which buys four times the vertical detail of the half
// blocks the wordmark itself is drawn from. That detail is not free —
// braille is NOT in the Nerd Fonts repertoire (see
// lab/glyph-blowup/NOTES.md), so a terminal draws it out of whatever
// fallback font on the machine does cover it, and coverage on stock macOS
// is unverified. TUTOR_ASCII is therefore no longer a cosmetic opt-in but
// the real escape hatch: it swaps the braille for a printable-ASCII robot
// of the same dimensions.
//
// It is printed in cmdRun before NewTerminal.Start puts the tty into raw
// mode and switches to the alternate screen (term.go:264-291). That ordering
// is deliberate and load-bearing: anything printed here behaves like the
// output of any ordinary command and scrolls into her shell's history, so
// the screen is still there to scroll back to after the reader has opened
// and been quit. Printing it from inside the alternate screen, or after raw
// mode is enabled, would erase it the moment the reader exits and defeat the
// entire point of the feature.
//
// It does not call sgr() (term.go:79). sgr looks a style up by name in the
// styles map, and while four of this screen's five colours have names there
// (h1, h3, h4, warn), 215 exists only inside "code", bundled with a
// background colour that would paint a filled block behind the letter it is
// meant to colour on its own. So this file writes its own "\x1b[...m"
// sequences from the small colour table below, gated on the same noColor
// variable sgr uses, and ends each coloured run with the shared reset
// constant.
package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"syscall"
	"time"
)

// --------------------------------------------------------------------------
// The artwork
//
// Each letter is 8 columns wide and 5 rows tall. They are stored per letter
// and stitched together per row at render time, rather than as five
// ready-made row strings, because every letter in the word takes its own
// colour — a single string per row could not carry that. "T" is shared
// between the word's first and third letters; word gives it two different
// colours by position.
// --------------------------------------------------------------------------

var glyphs = map[byte][5]string{
	'T': {
		"████████",
		"   ██   ",
		"   ██   ",
		"   ██   ",
		"   ██   ",
	},
	'U': {
		"██    ██",
		"██    ██",
		"██    ██",
		"██    ██",
		" ██████ ",
	},
	'O': {
		" ██████ ",
		"██    ██",
		"██    ██",
		"██    ██",
		" ██████ ",
	},
	'R': {
		"███████ ",
		"██    ██",
		"███████ ",
		"██   ██ ",
		"██    ██",
	},
}

// word spells T U T O R. It is the single source of truth for which glyph
// and which colour goes in each of the five positions, so the full artwork
// and the narrow fallback (which prints these same five letters as plain
// text) can never drift apart from each other.
var word = [5]byte{'T', 'U', 'T', 'O', 'R'}

// headColors is one colour per letter, left to right, bold. Every value is
// a colour the reader already uses elsewhere (h1, h3, h4, inline code,
// warn), so the launch screen and the course it introduces read as one
// programme rather than two.
var headColors = [5]int{81, 115, 150, 215, 209}

// tailColors is headColors reversed, plain weight. The subtitle sweeps back
// against the headline above it rather than repeating it.
var tailColors = [5]int{209, 215, 150, 115, 81}

// tagColor is the colour the subtitle's sweep arrives at on its final
// character — the version tag picks up from there rather than restarting
// the palette.
const tagColor = 81

// subtitle is exactly 45 characters, checked by splash_test.go so a future
// edit cannot silently change the bucket math below.
const subtitle = "A G E N T I C   A I   C R A S H   C O U R S E"
const subtitleIndent = 5

// narrowSubtitle is the same words with the letter-spacing removed, for the
// three-line fallback below narrowThreshold columns.
const narrowSubtitle = "AGENTIC AI CRASH COURSE"

// splashWidth is the artwork's fixed width: a 1-column left margin, five
// 8-column letters, and three-column gaps between them (1 + 8*5 + 3*4).
const splashWidth = 53

// narrowThreshold is the width below which the full artwork would wrap and
// read as a fault rather than a banner.
const narrowThreshold = 55

// --------------------------------------------------------------------------
// The robot logo
//
// A logoRows x logoCols braille robot head stands beside the TUTOR
// wordmark. Braille (U+2800-28FF) packs 2x4 dots into every cell, so a
// 26x12 cell budget carries a 52x48 dot grid — enough resolution for the
// antenna, the two open eyes, the ear tabs and the "!?" off the robot's
// shoulder to survive downsampling, none of which the previous half-block
// robot could hold.
//
// The cost is font coverage. Braille is not part of the Nerd Fonts
// repertoire and is not in the Block Elements range the wordmark is built
// from, so unlike the half-block robot it CANNOT be assumed to render
// wherever the wordmark does: the terminal falls back to some other
// installed font, at that font's weight and metrics, or draws tofu if no
// installed font covers the range. lab/glyph-blowup/NOTES.md records the
// coverage survey; stock macOS (SF Mono, Menlo, Monaco) is unverified.
// TUTOR_ASCII is the hatch for exactly that case and swaps in a
// printable-ASCII robot of identical dimensions.
// --------------------------------------------------------------------------

// logoRows and logoCols are the logo's cell budget, shared by both art
// tiers and by every loop that walks a composed row. They are named rather
// than repeated as literals because a mismatch between the array bounds
// and a loop bound is exactly the kind of edit that compiles and then
// prints a ragged banner.
const logoRows = 12
const logoCols = 26

// robotArt is the braille robot head, logoRows x logoCols. Source of truth:
// lab/glyph-blowup/full-braille-12r.txt (rendered from Nerd Font U+F169F by
// lab/glyph-blowup/gen.py). Transcribed verbatim by a generator script,
// never retyped by eye — and here that discipline matters more than it did
// for the half blocks: the blank cells are U+2800 BRAILLE PATTERN BLANK,
// not spaces, so a truncated or space-padded row is invisible to the eye,
// to an editor's trailing-whitespace highlighting, and to gofmt alike.
// Only TestArtTableDimensions would catch it.
var robotArt = [logoRows]string{
	"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣦⡀⠀⢀⣤⠀⣤⣤⣤⡀⠀⠀",
	"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⠃⠀⢸⣿⠀⠉⢉⣹⡇⠀⠀",
	"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⠁⠀⠀⢸⣿⠀⠀⣿⡟⠁⠀⠀",
	"⠀⠀⠀⠀⠀⢀⣠⣶⣾⣿⣿⣿⣿⣿⣿⣿⡇⢀⣄⠀⠀⣠⡄⠀⠀⠀",
	"⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣀⣉⣀⣀⣈⠁⠀⠀⠀",
	"⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀",
	"⠀⠀⢸⣿⣿⣿⠿⠛⠻⢿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠿⣿⣿⣿⡇⠀⠀",
	"⣴⣶⣾⣿⣿⠁⠀⠀⠀⠀⢻⣿⣿⣿⣿⡏⠀⠀⠀⠀⠈⣿⣿⣷⣶⣦",
	"⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿",
	"⣿⣿⣿⣿⣿⣷⣤⣤⣤⣴⣿⣿⣿⣿⣿⣿⣦⣤⣤⣤⣾⣿⣿⣿⣿⣿",
	"⠈⠉⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠉⠁",
	"⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀",
}

// robotAscii is the plain-ASCII robot, same box: the 9x20 half-block-era
// fallback art from lab/title-logo/robot-fallback.txt, centred in the
// larger logoRows x logoCols field with ordinary ASCII spaces (never
// U+2800, which would defeat the entire point of this tier). Same
// transcription discipline as robotArt.
//
// The vertical padding is 2 rows above and 1 below, not the other way
// round: 9 rows of art in a 12-row field leaves 3 rows of slack, and
// putting 2 of them on top lands this robot's own centre on composed row 6,
// the same row the wordmark's middle stripe sits on. Padding the other way
// would leave the wordmark visibly low against the ASCII tier while sitting
// correctly against the braille one.
var robotAscii = [logoRows]string{
	"                          ",
	"                          ",
	"           (__)           ",
	"            ||            ",
	"     .--------------.     ",
	"     |  [o]    [o]  |     ",
	"     |     ====     |     ",
	"     '--------------'     ",
	"    __ .----------. __    ",
	"   |  ||   [##]   ||  |   ",
	"   '--' '--'  '--' '--'   ",
	"                          ",
}

// robotRow picks the active tier's row: half-block by default, plain ASCII
// when TUTOR_ASCII is set.
func robotRow(row int) string {
	if asciiOnly {
		return robotAscii[row]
	}
	return robotArt[row]
}

// robotColors is one colour per robot row, bold. It introduces no colour of
// its own: it is headColors — the wordmark's own five-stop palette — swept
// top to bottom down the logo instead of left to right across the letters,
// using the same bucket arithmetic subtitleColored uses to spread five
// colours over a longer run (i*len/len). So the antenna and crown open on
// 81, the same cyan the T beside them opens on, and the jaw arrives at 209,
// the same amber the R closes on: the logo and the wordmark are two runs of
// one palette crossing at right angles, rather than two separate colour
// schemes that happen to share values.
//
// It is a literal table rather than a loop over headColors so the actual
// per-row values are readable here, and TestRobotColorsPalette pins it to
// the arithmetic.
var robotColors = [logoRows]int{
	81, 81, 81, 115, 115, 150, 150, 150, 215, 215, 209, 209,
}

// composedWidth is the logo screen's row width: a 26-column robot, a
// 3-column gutter, and the 53-column wordmark field.
const composedWidth = 82 // 26 + 3 + splashWidth

// logoThreshold is the terminal width at and above which the robot is
// shown beside the wordmark. This is deliberately NOT composedWidth (82):
// at a real 82-column terminal every composed row (the non-wordmark rows in
// particular, padded with 53 trailing spaces) measures exactly 82
// characters and lands flush on the right margin, where deferred-autowrap
// behaviour is terminal-dependent and can insert a spurious blank line
// between every row. logoThreshold is set two columns higher than
// composedWidth to keep the last printed column off the margin — the same
// two-column slack the original author already used between
// narrowThreshold (55) and splashWidth (53).
//
// Note what this costs, because it is a real narrowing: the braille logo is
// six columns wider than the half-block robot it replaced, so the threshold
// moved 78 -> 84 and detectWidth's 80-column default no longer clears it.
// An 80-column terminal — the stock macOS Terminal default — now gets the
// wordmark-only mid screen, not the logo. Widening the band again means
// narrowing the art, not lowering this number: 26 + 3 + 53 cannot be made
// to fit in 80 columns, and lab/glyph-blowup/gen.py's art() takes an
// explicit cols argument for exactly that kind of re-render.
const logoThreshold = 84

// wordmarkTopRow is the composed row (0-indexed, of logoRows) on which the
// 5-row wordmark starts, centring it against the taller robot. With 12 rows
// and a 5-row wordmark there are 7 rows of slack, which does not divide
// evenly; 4 above and 3 below puts the wordmark's optical centre level with
// the robot's eyes rather than with its jaw, since the braille head carries
// its ink low (rows 7-11 are the solid chin and shoulders).
const wordmarkTopRow = 4

// logoOffset is how far the whole wordmark field sits to the right of where
// it sits on the mid screen: the robot's width plus the gutter. Everything
// that has to stay aligned with the wordmark on the logo screen (the
// subtitle) shifts by exactly this, so the three numbers cannot drift.
const logoOffset = logoCols + len(robotGutter)

// robotGutter is the horizontal gap between the robot's right edge and the
// wordmark field: wide enough (with the field's own 1-column leading
// margin) that the robot cannot read as a sixth letter.
const robotGutter = "   "

// asciiOnly selects the plain-ASCII robot tier when TUTOR_ASCII is set to
// any non-empty value; the default is the half-block tier. It is read once
// at package initialisation, the same way noColor reads $NO_COLOR
// (term.go:77) — an os.Getenv call per line would be re-read on every
// render for a value that cannot change mid-process, and a test that
// wanted to exercise this path could not use os.Setenv against an
// init-time read anyway.
var asciiOnly = os.Getenv("TUTOR_ASCII") != ""

// --------------------------------------------------------------------------
// Colouring
// --------------------------------------------------------------------------

// colorRun wraps text in an SGR foreground sequence, or returns it unchanged
// when NO_COLOR is set. See the package comment for why this writes its own
// sequence instead of calling sgr().
func colorRun(text string, color int, bold bool) string {
	if noColor {
		return text
	}
	esc := "\x1b[38;5;" + strconv.Itoa(color) + "m"
	if bold {
		esc = "\x1b[1;38;5;" + strconv.Itoa(color) + "m"
	}
	return esc + text + reset
}

// --------------------------------------------------------------------------
// Full-width layout (53 columns and up)
//
// Every line has a "Plain" builder with no escape sequences at all, and a
// "Colored" builder on top of it. splash_test.go measures the Plain forms
// with dwidth, since an embedded escape sequence's digits and semicolons
// are ordinary printable ASCII to charWidth (only ESC itself, being below
// 0x20, measures as zero) and would inflate a coloured row's measured width
// well past 53. The Colored forms are what actually reach the terminal;
// the Plain forms exist so layout can be checked independently of colour.
// --------------------------------------------------------------------------

func artworkRowPlain(row int) string {
	var b strings.Builder
	b.WriteByte(' ')
	for i, letter := range word {
		if i > 0 {
			b.WriteString("   ")
		}
		b.WriteString(glyphs[letter][row])
	}
	return b.String()
}

func artworkRowColored(row int) string {
	var b strings.Builder
	b.WriteByte(' ')
	for i, letter := range word {
		if i > 0 {
			b.WriteString("   ")
		}
		b.WriteString(colorRun(glyphs[letter][row], headColors[i], true))
	}
	return b.String()
}

// composedRowPlain builds one row (0..logoRows-1) of the logo screen: the robot row,
// the gutter, then either the wordmark row (rows wordmarkTopRow through
// wordmarkTopRow+4) or a full 53-space filler. The filler rows are
// deliberately full splashWidth-space strings so every one of the 9
// composed rows measures exactly composedWidth, keeping the layout check a
// single uniform assertion.
func composedRowPlain(row int) string {
	right := strings.Repeat(" ", splashWidth)
	if row >= wordmarkTopRow && row < wordmarkTopRow+5 {
		right = artworkRowPlain(row - wordmarkTopRow)
	}
	return robotRow(row) + robotGutter + right
}

// composedRowColored is composedRowPlain's coloured twin. It wraps only the
// robot row in its own colour; the wordmark's existing per-letter colouring
// in artworkRowColored is untouched.
func composedRowColored(row int) string {
	right := strings.Repeat(" ", splashWidth)
	if row >= wordmarkTopRow && row < wordmarkTopRow+5 {
		right = artworkRowColored(row - wordmarkTopRow)
	}
	return colorRun(robotRow(row), robotColors[row], true) + robotGutter + right
}

func subtitlePlain() string {
	return strings.Repeat(" ", subtitleIndent) + subtitle
}

func subtitleColored() string {
	var b strings.Builder
	b.WriteString(strings.Repeat(" ", subtitleIndent))
	runes := []rune(subtitle)
	for i, r := range runes {
		color := tailColors[i*len(tailColors)/len(runes)]
		b.WriteString(colorRun(string(r), color, false))
	}
	return b.String()
}

// versionTag is "v" plus the version constant, never hardcoded, so it can
// never drift from what the binary actually reports.
func versionTag() string {
	return "v" + version
}

// versionPad is the left padding that lands the tag's last character on
// column splashWidth, shared by the plain and coloured forms so they can
// never disagree about where the tag sits.
func versionPad() string {
	pad := splashWidth - dwidth(versionTag())
	if pad < 0 {
		pad = 0
	}
	return strings.Repeat(" ", pad)
}

func versionLinePlain() string {
	return versionPad() + versionTag()
}

func versionLineColored() string {
	return versionPad() + colorRun(versionTag(), tagColor, false)
}

// --------------------------------------------------------------------------
// Logo screen (logoThreshold columns and up) — robot beside the wordmark
// --------------------------------------------------------------------------

// subtitleWidePlain is the subtitle shifted right by logoOffset columns
// from its mid-screen position, so it keeps its position relative to the
// wordmark now that the wordmark's visible letters start at column 31 (26
// robot + 3 gutter + 1 field margin + 1) instead of column 2.
func subtitleWidePlain() string {
	return strings.Repeat(" ", subtitleIndent+logoOffset) + subtitle
}

func subtitleWideColored() string {
	var b strings.Builder
	b.WriteString(strings.Repeat(" ", subtitleIndent+logoOffset))
	runes := []rune(subtitle)
	for i, r := range runes {
		color := tailColors[i*len(tailColors)/len(runes)]
		b.WriteString(colorRun(string(r), color, false))
	}
	return b.String()
}

// versionPadWide is versionPad's logo-screen twin: it lands the tag's last
// character on column composedWidth (82) — the wordmark's right edge in
// the wider field — instead of splashWidth (53).
func versionPadWide() string {
	pad := composedWidth - dwidth(versionTag())
	if pad < 0 {
		pad = 0
	}
	return strings.Repeat(" ", pad)
}

func versionLineWidePlain() string {
	return versionPadWide() + versionTag()
}

func versionLineWideColored() string {
	return versionPadWide() + colorRun(versionTag(), tagColor, false)
}

// logoSplashPlain is the 16-line logo screen: a blank line, the logoRows
// composed rows (robot beside the vertically-centred wordmark), a blank
// line, the subtitle, and the version tag.
func logoSplashPlain() []string {
	lines := []string{""}
	for row := 0; row < logoRows; row++ {
		lines = append(lines, composedRowPlain(row))
	}
	return append(lines, "", subtitleWidePlain(), versionLineWidePlain())
}

func logoSplashColored() []string {
	if noColor {
		return logoSplashPlain()
	}
	lines := []string{""}
	for row := 0; row < logoRows; row++ {
		lines = append(lines, composedRowColored(row))
	}
	return append(lines, "", subtitleWideColored(), versionLineWideColored())
}

// --------------------------------------------------------------------------
// Mid screen (narrowThreshold up to logoThreshold columns) — wordmark only,
// no robot: the band is too narrow for one that would not read as a smudge.
// --------------------------------------------------------------------------

func fullSplashPlain() []string {
	lines := []string{""}
	for row := 0; row < 5; row++ {
		lines = append(lines, artworkRowPlain(row))
	}
	return append(lines, "", subtitlePlain(), versionLinePlain())
}

func fullSplashColored() []string {
	if noColor {
		return fullSplashPlain()
	}
	lines := []string{""}
	for row := 0; row < 5; row++ {
		lines = append(lines, artworkRowColored(row))
	}
	return append(lines, "", subtitleColored(), versionLineColored())
}

// --------------------------------------------------------------------------
// Narrow fallback (below narrowThreshold columns)
// --------------------------------------------------------------------------

// narrowWord is "TUTOR" as plain text, derived from word so the fallback can
// never spell something the artwork above it does not.
func narrowWord() string {
	return string(word[:])
}

func narrowSplashPlain() []string {
	return []string{narrowWord(), narrowSubtitle, versionTag()}
}

func narrowSplashColored() []string {
	if noColor {
		return narrowSplashPlain()
	}
	var wordLine strings.Builder
	for i, letter := range word {
		wordLine.WriteString(colorRun(string(letter), headColors[i], true))
	}
	var subLine strings.Builder
	runes := []rune(narrowSubtitle)
	for i, r := range runes {
		color := tailColors[i*len(tailColors)/len(runes)]
		subLine.WriteString(colorRun(string(r), color, false))
	}
	verLine := colorRun(versionTag(), tagColor, false)
	return []string{wordLine.String(), subLine.String(), verLine}
}

// --------------------------------------------------------------------------
// Entry points
// --------------------------------------------------------------------------

// detectWidth reads the terminal directly by fd, the same free function
// Terminal.Size wraps (term.go:347-353), because this runs before any
// Terminal exists. On error it assumes 80, matching Terminal.Size's own
// fallback.
func detectWidth() int {
	cols, _, err := getWinsize(int(os.Stdout.Fd()))
	if err != nil || cols <= 0 {
		return 80
	}
	return cols
}

// splashLines picks the logo screen, the mid (wordmark-only) screen, or the
// narrow fallback for the given terminal width. Do NOT raise
// narrowThreshold to make room for logoThreshold — demoting 55-to-77-column
// terminals to the plain-text fallback would be a new bug shipped with
// this one.
func splashLines(width int) []string {
	switch {
	case width >= logoThreshold:
		return logoSplashColored()
	case width >= narrowThreshold:
		return fullSplashColored()
	default:
		return narrowSplashColored()
	}
}

// printSplash writes the launch screen for width columns.
func printSplash(width int) {
	for _, line := range splashLines(width) {
		fmt.Println(line)
	}
}

// waitForSplash holds the screen for five seconds, or until a keypress cuts
// it short, using termios alone — no goroutine, timer, channel or signal
// handler that could outlive the wait or leak past it.
//
// VMIN=0, VTIME=50 (tenths of a second) makes a single Read block until
// either five seconds pass with nothing typed, or the first byte arrives;
// term.go:279-280 already writes this same Cc pair for a different purpose,
// so this is an established pattern rather than a new one.
//
// ISIG is cleared for the duration, so Ctrl-C never reaches the process as
// SIGINT and instead arrives as the ordinary byte 0x03 in the read buffer.
// The bool return tells the caller that happened, so it can exit without
// ever opening the reader — leaving ISIG on would let SIGINT kill the
// process while echo is still disabled, which would leave her shell
// silently broken until she typed "reset".
//
// The saved termios is restored on every path, including both fallbacks,
// via defer: a launch screen must never be the reason the terminal is left
// in a bad state, or the reason the reader fails to open.
func waitForSplash() (ctrlC bool) {
	fd := int(os.Stdin.Fd())

	saved, err := getTermios(fd)
	if err != nil {
		// No termios to restore, so nothing to defer. Sleeping plainly means a
		// keypress can no longer cut the wait short, but the reader still opens
		// on schedule, which is the property that must never break.
		time.Sleep(5 * time.Second)
		return false
	}

	raw := *saved
	raw.Lflag &^= syscall.ICANON | syscall.ECHO | syscall.ISIG
	raw.Cc[syscall.VMIN] = 0
	raw.Cc[syscall.VTIME] = 50
	if err := setTermios(fd, setFlush, &raw); err != nil {
		time.Sleep(5 * time.Second)
		return false
	}
	defer func() {
		_ = setTermios(fd, setDrain, saved)
	}()

	buf := make([]byte, 8)
	n, _ := os.Stdin.Read(buf)
	for i := 0; i < n; i++ {
		if buf[i] == 0x03 {
			return true
		}
	}
	return false
}

// cmdSplash is the `tutor splash [cols]` subcommand: it prints the screen
// and returns immediately with no five-second wait. This is the only way
// the screen can be checked from a tool call — the real wait needs a tty,
// which an agent's tool call never has (main.go's isTTY check in cmdRun
// would simply refuse to run at all).
func cmdSplash(args []string) int {
	width := detectWidth()
	if len(args) > 0 {
		if n, err := strconv.Atoi(args[0]); err == nil {
			width = n
		}
	}
	printSplash(width)
	return 0
}
