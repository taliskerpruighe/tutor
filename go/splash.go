// The launch screen for `tutor` — five seconds of block-letter artwork,
// modelled on oh-my-zsh's update banner.
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
// The robot crest
//
// robotRune is U+F16A0, nf-md-robot-confused: a Material Design Icons glyph
// carried by Nerd Fonts and by nothing else. It is written here as an
// escape and never as the character itself, so an editor, a patch tool or
// an encoding round trip cannot mangle it into a different Private Use Area
// codepoint that would still render as *something* and so never be caught
// by eye. TestGlyphCodepoint is what enforces that.
//
// The assumption it rests on is that the reader's terminal is set to a Nerd
// Font, which content/03-the-cli/13-powerline-themes.md states outright:
// the terminal is set to Hack Nerd Font rather than plain Hack, and Hack
// Nerd Font contains this codepoint. A TUI cannot query the active font's
// coverage, so there is no detection to do here — TUTOR_ASCII below is the
// single explicit escape hatch.
const robotRune = '\U000F16A0'

// robotGlyph is the same codepoint as a string, for the width arithmetic:
// dwidth takes a string where charWidth takes a rune, and the centring
// below needs the former.
const robotGlyph = string(robotRune)

// asciiOnly drops the robot crest when TUTOR_ASCII is set to any non-empty
// value, leaving the screen exactly as it was before the glyph landed. It
// is read once at package initialisation, the same way noColor reads
// $NO_COLOR (term.go:77) — an os.Getenv call per line would be re-read on
// every render for a value that cannot change mid-process, and a test that
// wanted to exercise this path could not use os.Setenv against an init-time
// read anyway.
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

// glyphPad centres the crest over a field of the given width. The pad is
// always computed, never written down: artworkRowPlain opens with a single
// space, so splashWidth's extra column is a LEADING margin and the visible
// wordmark occupies columns 2 through 53. Centring over the field and
// centring over the wordmark agree at these numbers only by coincidence,
// so if the margin, splashWidth or the glyph's measured width ever moves,
// this expression and the test that mirrors it move together.
func glyphPad(field int) string {
	pad := (field - dwidth(robotGlyph)) / 2
	if pad < 0 {
		pad = 0
	}
	return strings.Repeat(" ", pad)
}

// glyphLinePlain is the crest centred over the full artwork. It is
// deliberately alone on its line and outside every exact-width assertion:
// charWidth measures U+F16A0 as one column (the Private Use Area is in
// neither range table in width_table.go), but a Nerd Font glyph can render
// wider than one cell in some terminals, and a line of its own is the only
// place where that drift cannot pull anything else out of alignment.
func glyphLinePlain() string {
	return glyphPad(splashWidth) + robotGlyph
}

func glyphLineColored() string {
	return glyphPad(splashWidth) + colorRun(robotGlyph, tagColor, true)
}

// narrowGlyphLinePlain centres the crest over the bare five-character word
// the narrow fallback prints, which starts at column 1 with no padding of
// its own.
func narrowGlyphLinePlain() string {
	return glyphPad(dwidth(narrowWord())) + robotGlyph
}

func narrowGlyphLineColored() string {
	return glyphPad(dwidth(narrowWord())) + colorRun(robotGlyph, tagColor, true)
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

func fullSplashPlain() []string {
	lines := []string{""}
	if !asciiOnly {
		lines = append(lines, glyphLinePlain(), "")
	}
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
	if !asciiOnly {
		lines = append(lines, glyphLineColored(), "")
	}
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
	lines := []string{}
	if !asciiOnly {
		lines = append(lines, narrowGlyphLinePlain())
	}
	return append(lines, narrowWord(), narrowSubtitle, versionTag())
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
	lines := []string{}
	if !asciiOnly {
		lines = append(lines, narrowGlyphLineColored())
	}
	return append(lines, wordLine.String(), subLine.String(), verLine)
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

// splashLines picks the full artwork or the narrow fallback for the given
// terminal width.
func splashLines(width int) []string {
	if width < narrowThreshold {
		return narrowSplashColored()
	}
	return fullSplashColored()
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
