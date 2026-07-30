// Terminal control for the tutor TUI.
//
// Owns everything that touches the tty: raw mode, the alternate screen, mouse
// reporting, input decoding, resize detection, and frame output.
//
// Two invariants this file exists to guarantee:
//
//  1. The terminal is *always* restored. Raw mode, the alternate screen, the
//     hidden cursor and mouse reporting are undone by a normal exit, a panic,
//     SIGTERM and SIGHUP alike. Leaving a user's shell in raw mode is the one
//     unforgivable bug in a TUI.
//
//  2. A frame is written in a *single* write call. Assembling the whole
//     screen into one string and flushing it once removes tearing without the
//     complexity of cell-level diffing, which these screen sizes do not need.
package main

import (
	"os"
	"os/signal"
	"strconv"
	"strings"
	"syscall"
	"time"
	"unicode/utf8"
)

// --------------------------------------------------------------------------
// Styles
//
// A style is an SGR parameter string (without the leading escape or trailing
// 'm'). The renderer and layout emit (text, style) spans; this table is the
// single place colour is decided. Honours NO_COLOR.
// --------------------------------------------------------------------------

const reset = "\x1b[0m"

var styles = map[string]string{
	"":            "",
	"body":        "38;5;252",
	"dim":         "38;5;245",
	"faint":       "38;5;240",
	"bold":        "1;38;5;255",
	"italic":      "3;38;5;252",
	"bolditalic":  "1;3;38;5;255",
	"h1":          "1;38;5;81",
	"h2":          "1;38;5;80",
	"h3":          "1;38;5;115",
	"h4":          "1;38;5;150",
	"code":        "38;5;215;48;5;236",
	"codeblock":   "38;5;223;48;5;235",
	"codelang":    "38;5;108;48;5;235",
	"link":        "4;38;5;117",
	"linkurl":     "38;5;244",
	"rule":        "38;5;238",
	"quote":       "3;38;5;250",
	"quotebar":    "38;5;72",
	"bullet":      "1;38;5;81",
	"tablehead":   "1;38;5;81",
	"tableborder": "38;5;240",
	// chrome
	"tab_active": "1;4;38;5;81",
	"tab_idle":   "38;5;245",
	"tab_arrow":  "38;5;240",
	"sep":        "38;5;238",
	"sel_bar":    "1;38;5;81",
	"sel_row":    "1;38;5;231;48;5;238",
	"row_num":    "38;5;109",
	"row":        "38;5;250",
	"status":     "38;5;245;48;5;235",
	"status_key": "38;5;81;48;5;235",
	"warn":       "1;38;5;209",
	"search":     "1;38;5;16;48;5;186",
}

var noColor = os.Getenv("NO_COLOR") != ""

// sgr returns the escape sequence that turns style on, or "" if none.
func sgr(style string) string {
	if noColor {
		return ""
	}
	params := styles[style]
	if params == "" {
		return ""
	}
	return "\x1b[" + params + "m"
}

// --------------------------------------------------------------------------
// Input decoding
//
// An event is either a key token ("up", "q", "enter", ...) or a mouse report
// with 0-based coordinates.
// --------------------------------------------------------------------------

type event struct {
	key   string
	mouse bool
	kind  string // click | wheel-up | wheel-down | other
	x, y  int
}

// Terminals disagree about arrow keys: xterm emits CSI A, some emit SS3 A.
var csiKeys = map[rune]string{
	'A': "up", 'B': "down", 'C': "right", 'D': "left",
	'H': "home", 'F': "end", 'Z': "shift-tab",
}

var tildeKeys = map[string]string{
	"1": "home", "3": "delete", "4": "end",
	"5": "pgup", "6": "pgdn", "7": "home", "8": "end",
}

var ctrlKeys = map[rune]string{
	'\r': "enter", '\n': "enter", '\t': "tab",
	'\x7f': "backspace", '\x08': "backspace",
	'\x03': "ctrl-c", '\x04': "ctrl-d", '\x1b': "esc",
}

// decode pulls one event off the front of buf.
//
// The bool is false when buf holds only the prefix of an incomplete escape
// sequence and the caller should wait for more bytes.
func decode(buf []rune) (event, []rune, bool) {
	if len(buf) == 0 {
		return event{}, buf, false
	}

	if buf[0] != '\x1b' {
		ch := buf[0]
		if k, ok := ctrlKeys[ch]; ok {
			return event{key: k}, buf[1:], true
		}
		if ch < ' ' {
			return event{key: "ctrl-" + string(rune(ch+96))}, buf[1:], true
		}
		return event{key: string(ch)}, buf[1:], true
	}

	// Lone ESC with nothing after it yet: the caller decides whether to wait.
	if len(buf) == 1 {
		return event{}, buf, false
	}

	// SGR mouse report: CSI < button ; col ; row (M=press, m=release)
	if len(buf) >= 3 && buf[1] == '[' && buf[2] == '<' {
		nums, final, end, ok := parseParams(buf, 3)
		if !ok {
			return event{}, buf, false
		}
		if len(nums) == 3 && (final == 'M' || final == 'm') {
			button, col, row := nums[0], nums[1], nums[2]
			ev := event{mouse: true, x: col - 1, y: row - 1}
			switch {
			case button == 64:
				ev.kind = "wheel-up"
			case button == 65:
				ev.kind = "wheel-down"
			case final == 'M' && button&0b11000011 == 0:
				ev.kind = "click"
			default:
				ev.kind = "other"
			}
			return ev, buf[end:], true
		}
		return event{key: "unknown"}, buf[end:], true
	}

	// SS3: ESC O final
	if buf[1] == 'O' {
		if len(buf) < 3 {
			return event{}, buf, false
		}
		if k, ok := csiKeys[buf[2]]; ok {
			return event{key: k}, buf[3:], true
		}
		return event{key: "unknown"}, buf[3:], true
	}

	// CSI: ESC [ params intermediates final
	if buf[1] == '[' {
		i := 2
		start := i
		for i < len(buf) && (buf[i] == ';' || buf[i] == '?' || (buf[i] >= '0' && buf[i] <= '9')) {
			i++
		}
		params := string(buf[start:i])
		for i < len(buf) && buf[i] >= ' ' && buf[i] <= '/' {
			i++
		}
		if i >= len(buf) {
			return event{}, buf, false
		}
		final := buf[i]
		if final < '@' || final > '~' {
			return event{key: "unknown"}, buf[i+1:], true
		}
		rest := buf[i+1:]
		if final == '~' {
			head := strings.Split(params, ";")[0]
			if k, ok := tildeKeys[head]; ok {
				return event{key: k}, rest, true
			}
			return event{key: "unknown"}, rest, true
		}
		// Modified keys arrive as CSI 1;5A etc. Modifiers are ignored; the
		// base key is what the keymap acts on.
		if k, ok := csiKeys[final]; ok {
			return event{key: k}, rest, true
		}
		return event{key: "unknown"}, rest, true
	}

	// ESC followed by a plain key: alt-modified. Treated as a bare ESC so that
	// pressing escape twice quickly never gets swallowed.
	return event{key: "esc"}, buf[1:], true
}

// parseParams reads `n;n;n` followed by a final byte, starting at i.
func parseParams(buf []rune, i int) (nums []int, final rune, end int, ok bool) {
	cur := ""
	for i < len(buf) {
		c := buf[i]
		switch {
		case c >= '0' && c <= '9':
			cur += string(c)
			i++
		case c == ';':
			n, _ := strconv.Atoi(cur)
			nums = append(nums, n)
			cur = ""
			i++
		default:
			n, _ := strconv.Atoi(cur)
			nums = append(nums, n)
			return nums, c, i + 1, true
		}
	}
	return nil, 0, i, false
}

// --------------------------------------------------------------------------
// Terminal
// --------------------------------------------------------------------------

type Terminal struct {
	fd       int
	saved    *termios
	mouse    bool
	buf      []rune
	raw      []byte
	bytesCh  chan []byte
	winchCh  chan os.Signal
	termCh   chan os.Signal
	restored bool

	// sent maps a picture's file path to the id it was transmitted under.
	// imgTransmit's own bytes — the picture's whole PNG, base64'd — are the
	// expensive part, so this is what keeps them going over the wire once
	// per session instead of on every keypress; imgPlace, which IS cheap
	// enough to repeat every frame, is all that runs on a cache hit.
	sent map[string]int
}

func NewTerminal(mouse bool) *Terminal {
	return &Terminal{fd: int(os.Stdin.Fd()), mouse: mouse, sent: map[string]int{}}
}

// Start puts the tty into raw mode and switches to the alternate screen.
func (t *Terminal) Start() error {
	saved, err := getTermios(t.fd)
	if err != nil {
		return err
	}
	t.saved = saved

	// The same transformation Python's tty.setraw applies, so both builds put
	// the terminal into precisely the same state.
	raw := *saved
	raw.Iflag &^= syscall.BRKINT | syscall.ICRNL | syscall.INPCK | syscall.ISTRIP | syscall.IXON
	raw.Oflag &^= syscall.OPOST
	raw.Cflag &^= syscall.CSIZE | syscall.PARENB
	raw.Cflag |= syscall.CS8
	raw.Lflag &^= syscall.ECHO | syscall.ICANON | syscall.IEXTEN | syscall.ISIG
	raw.Cc[syscall.VMIN] = 1
	raw.Cc[syscall.VTIME] = 0
	if err := setTermios(t.fd, setFlush, &raw); err != nil {
		return err
	}

	out := "\x1b[?1049h\x1b[?25l\x1b[2J\x1b[H"
	if t.mouse {
		// 1000 = button events, 1006 = SGR coordinates (needed above 223
		// columns, which any modern terminal exceeds).
		out += "\x1b[?1000h\x1b[?1006h"
	}
	t.write(out)

	t.winchCh = make(chan os.Signal, 1)
	signal.Notify(t.winchCh, syscall.SIGWINCH)

	// Go's signal channel replaces Python's self-pipe: a select over the input
	// and resize channels is the whole mechanism, with no PEP 475 restart
	// problem to work around.
	t.termCh = make(chan os.Signal, 1)
	signal.Notify(t.termCh, syscall.SIGTERM, syscall.SIGHUP)
	go func() {
		<-t.termCh
		t.Restore()
		os.Exit(0)
	}()

	t.bytesCh = make(chan []byte, 8)
	go func() {
		b := make([]byte, 4096)
		for {
			n, err := os.Stdin.Read(b)
			if n > 0 {
				chunk := make([]byte, n)
				copy(chunk, b[:n])
				t.bytesCh <- chunk
			}
			if err != nil {
				close(t.bytesCh)
				return
			}
		}
	}()
	return nil
}

// Restore undoes every terminal mutation. Safe to call more than once.
func (t *Terminal) Restore() {
	if t.saved == nil || t.restored {
		return
	}
	t.restored = true
	var b strings.Builder
	if len(t.sent) > 0 {
		// Frees the pixels a picture-heavy session decoded, so they do not sit
		// in the terminal's memory after the reader has closed. Harmless (and
		// skipped) when nothing was ever transmitted this session.
		imgFreeAll(&b)
	}
	if t.mouse {
		b.WriteString("\x1b[?1006l\x1b[?1000l")
	}
	b.WriteString("\x1b[?25h\x1b[?1049l" + reset)
	t.write(b.String())
	_ = setTermios(t.fd, setDrain, t.saved)
}

func (t *Terminal) write(s string) {
	_, _ = os.Stdout.WriteString(s)
}

// Size asks the tty itself. $COLUMNS and $LINES are never consulted: a stale
// exported value would freeze the layout at the size the shell started at.
func (t *Terminal) Size() (int, int) {
	cols, rows, err := getWinsize(t.fd)
	if err != nil || cols <= 0 || rows <= 0 {
		cols, rows = 80, 24
	}
	return max(cols, 1), max(rows, 1)
}

// Draw paints rows: a list of rows, each a list of (text, style) spans, plus
// the pictures visible this frame.
//
// Rows beyond the list are blanked, so callers never have to pad the frame to
// the full screen height themselves.
//
// Everything — the placement clear, the text, the pictures — goes into the
// one strings.Builder this function already used, and out in the one write
// call at the bottom. That single write is what keeps the screen from
// tearing; splitting the picture calls into writes of their own would
// reintroduce it.
func (t *Terminal) Draw(rows [][]span, images []placement) {
	_, height := t.Size()
	var b strings.Builder
	b.WriteString("\x1b[H")

	// Clearing placements has to happen before any text is written. The
	// per-line \x1b[2K below erases text but not a picture — they live in
	// different planes as far as the terminal is concerned — so a picture
	// left over from the previous frame would otherwise ghost underneath
	// whatever now scrolls past where it was.
	imgClearPlacements(&b)

	for y := 0; y < height; y++ {
		b.WriteString("\x1b[" + strconv.Itoa(y+1) + ";1H\x1b[2K")
		if y < len(rows) {
			for _, sp := range rows[y] {
				if sp.text == "" {
					continue
				}
				if esc := sgr(sp.style); esc != "" {
					b.WriteString(esc + sp.text + reset)
				} else {
					b.WriteString(sp.text)
				}
			}
		}
	}
	b.WriteString("\x1b[" + strconv.Itoa(height) + ";1H")

	// Pictures are placed last, after the text and the final cursor move, so
	// their own cursor-relative positioning (image.go's imgPlace) lands
	// against the frame just painted rather than wherever the cursor was
	// before this call began.
	for _, p := range images {
		id, sent := t.sent[p.path]
		if !sent {
			// Transmitted once per path per session — the expensive part, the
			// picture's own PNG bytes — and never again; only the cheap
			// imgPlace call below repeats on every keypress.
			//
			// Numbered from firstImageID rather than from 1 so that no
			// picture can ever collide with probeCapabilityID, the id
			// image.go's startup query borrows. That query asks the terminal
			// to decode and discard rather than to keep anything, so in
			// principle id 1 is free the moment it returns — but the cost of
			// not relying on that is one constant, and the failure it would
			// cause (a picture silently replaced by a 1x1 probe pixel) is
			// exactly the kind that would be blamed on anything but this.
			id = firstImageID + len(t.sent)
			if err := imgTransmit(&b, id, p.path); err != nil {
				continue // unreadable file: draw nothing, same fallback render.go uses
			}
			t.sent[p.path] = id
		}
		p.id = id
		imgPlace(&b, p)
	}

	t.write(b.String())
}

// ReadEvent blocks for one event. The bool is false on timeout or a pending
// resize, which simply means "redraw and ask again".
func (t *Terminal) ReadEvent(timeout time.Duration) (event, bool) {
	for {
		if ev, rest, ok := decode(t.buf); ok {
			t.buf = rest
			return ev, true
		}

		// A lone ESC in the buffer is ambiguous: it may be the start of a
		// sequence still in flight, or the escape key. Poll briefly; if
		// nothing follows, it was the key.
		poll := timeout
		if len(t.buf) > 0 {
			poll = 50 * time.Millisecond
		}
		var timerC <-chan time.Time
		var timer *time.Timer
		if poll > 0 {
			timer = time.NewTimer(poll)
			timerC = timer.C
		}
		stop := func() {
			if timer != nil {
				timer.Stop()
			}
		}

		select {
		case <-t.winchCh:
			stop()
			return event{}, false // the caller repaints at the new size

		case <-timerC:
			if len(t.buf) > 0 {
				t.buf = t.buf[1:]
				return event{key: "esc"}, true
			}
			return event{}, false

		case chunk, ok := <-t.bytesCh:
			stop()
			if !ok {
				return event{key: "quit"}, true
			}
			t.raw = append(t.raw, chunk...)
			// Decode conservatively so a multi-byte character split across
			// reads is not mangled into replacement characters.
			if utf8.Valid(t.raw) {
				t.buf = append(t.buf, []rune(string(t.raw))...)
				t.raw = t.raw[:0]
			} else if len(t.raw) > 8 {
				t.buf = append(t.buf, []rune(string(t.raw))...)
				t.raw = t.raw[:0]
			}
		}
	}
}
