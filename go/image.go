// The picture engine: transmitting and drawing bitmaps in the terminal using
// the kitty graphics protocol.
//
// This file is deliberately self-contained — it calls nothing else in the
// package, and nothing else in the package needs to know pictures exist
// beyond the calls below. That split is what lets render.go and layout.go
// reserve blank rows for a picture with pure arithmetic (imageRows), on
// both the Go and the Python side, with no terminal in the room, while the
// actual escape sequences only ever get generated later, at draw time, by
// whichever caller owns the screen.
//
// Reference: /tmp/kdemo/main.go, a spike written to answer exactly the
// questions this file answers — chunked transmit, in-place redraw without
// ghosting, and cropping a picture that is half scrolled off the pane. The
// logic below follows it closely.
package main

import (
	"encoding/base64"
	"fmt"
	"io"
	"os"
	"strings"
	"syscall"
	"unsafe"
)

// pngSize reads width and height straight out of a PNG's IHDR chunk. Every
// PNG opens with an 8-byte signature, then an 8-byte chunk header, then
// IHDR's own first two fields: a 4-byte big-endian width and a 4-byte
// big-endian height. So the numbers this program needs are always sitting
// at bytes 16:20 and 20:24, with no need to decode a single pixel — which
// is the point: neither this file nor tui/render.py's mirror of it ever
// imports an image-decoding library.
func pngSize(path string) (w, h int, err error) {
	f, err := os.Open(path)
	if err != nil {
		return 0, 0, err
	}
	defer f.Close()

	// io.ReadFull, not f.Read: a short file can return fewer than 24 bytes
	// with a nil error on a single Read call, and treating that as success
	// would read width/height out of whatever garbage happened to be in the
	// rest of the buffer instead of failing.
	head := make([]byte, 24)
	if _, err := io.ReadFull(f, head); err != nil {
		return 0, 0, fmt.Errorf("%s: %w", path, err)
	}
	if string(head[1:4]) != "PNG" {
		return 0, 0, fmt.Errorf("%s: not a PNG file", path)
	}

	be := func(b []byte) int {
		return int(b[0])<<24 | int(b[1])<<16 | int(b[2])<<8 | int(b[3])
	}
	return be(head[16:20]), be(head[20:24]), nil
}

// imageRows is how many terminal rows a picture reserves at a given pane
// width:
//
//	rows = ceil(imgH * paneW / (imgW * 2))
//
// The 2 assumes terminal cells are twice as tall as wide, which is close
// enough for a reservation: the picture is fitted INSIDE this box at draw
// time using the terminal's real cell size and centred there, so an
// unusual font letterboxes instead of distorting the picture. This has to
// stay pure arithmetic on three ints — no terminal, no float rounding modes
// — because go/render.go and tui/render.py both call it with nothing to
// draw to yet, and the parity harness diffs their reservations byte for
// byte at several pane widths.
func imageRows(imgW, imgH, paneW int) int {
	if imgW <= 0 || paneW <= 0 {
		return 0
	}
	num := imgH * paneW
	den := imgW * 2
	// Integer ceiling division without floating point, so Go and Python can
	// never round a boundary case differently from each other.
	return (num + den - 1) / den
}

// placement is one picture visible on screen this frame.
type placement struct {
	id         int // stable per file path
	path       string
	row, col   int // 1-based screen cell of the top-left corner
	cols, rows int // the cell box to fit the picture inside
	srcY, srcH int // source pixel crop, for a picture half scrolled off
}

// imgTransmit sends a picture's own PNG bytes, base64'd, in chunks of at
// most 4096 base64 characters — the practical per-command limit the kitty
// protocol expects a client to respect. It runs once per picture per
// session; imgPlace is the cheap call that runs every frame instead of
// repeating this.
//
// f=100 tells the terminal the payload IS a whole PNG file, so the
// terminal does its own decoding. That is the reason this program never
// imports image/png: the same freedom imageRows already has from never
// touching a pixel.
//
// q=2 on every chunk, including the continuation ones, is rule 1: every
// kitty command in this program must carry it, because without it the
// terminal writes an OK/error acknowledgement back down the pipe, and
// go/term.go's decode() would receive that as keystrokes.
func imgTransmit(b *strings.Builder, id int, path string) error {
	png, err := os.ReadFile(path)
	if err != nil {
		return err
	}
	enc := base64.StdEncoding.EncodeToString(png)

	const chunkSize = 4096
	first := true
	for len(enc) > 0 {
		n := chunkSize
		if n > len(enc) {
			n = len(enc)
		}
		part := enc[:n]
		enc = enc[n:]

		more := 0
		if len(enc) > 0 {
			more = 1
		}

		if first {
			fmt.Fprintf(b, "\x1b_Ga=t,f=100,i=%d,q=2,m=%d;%s\x1b\\", id, more, part)
			first = false
		} else {
			// Continuation chunks carry only m (more-to-come) and q — the
			// terminal already knows the id, format and action from the
			// first chunk of this transmission.
			fmt.Fprintf(b, "\x1b_Gq=2,m=%d;%s\x1b\\", more, part)
		}
	}
	return nil
}

// imgPlace draws an already-transmitted picture. It is small enough — about
// eighty bytes, none of it the picture's own pixels — to re-emit on every
// keypress, which is what the reader's full-redraw draw model requires:
// term.go's Draw rewrites every row every frame, with no per-cell diffing
// to spare this call.
//
// C=1 is rule 2: without it, placing a picture also moves the cursor past
// it, which scrolls the pane and corrupts the very frame being drawn.
//
// y/h crop the source picture vertically to p.srcY:p.srcY+p.srcH; x and w
// are left unset, which the kitty protocol defaults to 0 and the full
// image width, since a picture in this reader only ever scrolls off the
// top or bottom of a pane, never off a side.
//
// The leading cursor-position sequence (rule 5) is required because kitty
// places a picture relative to the cursor, not by absolute coordinates of
// its own.
func imgPlace(b *strings.Builder, p placement) {
	fmt.Fprintf(b, "\x1b[%d;%dH", p.row, p.col)
	fmt.Fprintf(b, "\x1b_Ga=p,i=%d,p=1,c=%d,r=%d,y=%d,h=%d,C=1,q=2\x1b\\",
		p.id, p.cols, p.rows, p.srcY, p.srcH)
}

// imgClearPlacements removes what was drawn last frame but keeps the
// transmitted pixels, so the next frame does not have to send them again.
//
// This has to run before the frame's text is written. go/term.go's Draw
// clears every line with \x1b[2K on every frame, and that erases text but
// not a picture placement — they live in different planes as far as the
// terminal is concerned. Skip this call and a picture from a previous
// frame is left ghosted underneath whatever now scrolls past where it was.
//
// d=a (lowercase: placements only, image data kept) is unscoped by id
// because a frame can hold more than one picture and this runs once per
// frame regardless of how many are on screen.
func imgClearPlacements(b *strings.Builder) {
	fmt.Fprintf(b, "\x1b_Ga=d,d=a,q=2\x1b\\")
}

// imgFreeAll deletes placements AND frees the transmitted pixels. Called
// from Terminal.Restore on the way out, so a picture-heavy session does not
// leave megabytes of decoded image data sitting in the terminal after the
// reader has closed.
//
// d=A is imgClearPlacements's d=a with the case flipped: uppercase is what
// tells kitty to also drop the underlying image data, not just what is
// currently placed.
func imgFreeAll(b *strings.Builder) {
	fmt.Fprintf(b, "\x1b_Ga=d,d=A,q=2\x1b\\")
}

// --------------------------------------------------------------------------
// Capability probing
//
// probeImages is called once, before Terminal.Start (term.go:264), while
// nothing else is reading stdin. That ordering is load-bearing: the
// capability query below does its own blocking read of stdin, and running
// it after Start would race Start's own input goroutine (term.go:307-322)
// for the same bytes.
// --------------------------------------------------------------------------

// winsizePixels mirrors struct winsize from <sys/ioctl.h>, keeping the
// pixel fields that go/term_linux.go's and go/term_darwin.go's own
// getWinsize helper does not expose (it only returns cols/rows). This file
// defines its own copy instead of reaching into those, both because
// image.go must not depend on anything else in the package, and because
// those two files are owned by another worker's edits at the same time as
// this one.
type winsizePixels struct{ Row, Col, Xpixel, Ypixel uint16 }

// cellPixels returns the pixel size of one terminal cell, or 0,0 if the
// terminal does not report it. A zeroed Xpixel/Ypixel is not an error case
// — plenty of terminals, and every tmux pane, simply leave those fields at
// zero — so this returns a zero value rather than an error for the caller
// to check plainly.
func cellPixels(fd int) (w, h int) {
	var ws winsizePixels
	_, _, errno := syscall.Syscall(syscall.SYS_IOCTL, uintptr(fd),
		uintptr(syscall.TIOCGWINSZ), uintptr(unsafe.Pointer(&ws)))
	if errno != 0 || ws.Col == 0 || ws.Row == 0 || ws.Xpixel == 0 || ws.Ypixel == 0 {
		return 0, 0
	}
	return int(ws.Xpixel) / int(ws.Col), int(ws.Ypixel) / int(ws.Row)
}

// probeCapabilityID is the transmission id the capability query below
// reuses on every call. It is never placed and never left behind — the
// query (t=d) asks the terminal to decode and discard, not to keep
// anything under this id.
//
// firstImageID is where term.go starts numbering real pictures, chosen far
// enough above the probe's id that the two can never meet even if some
// terminal did keep the queried pixels around. Relying on the paragraph
// above would probably be fine; a constant costs nothing and the bug it
// forecloses — a picture silently replaced by a 1x1 probe pixel — would be
// blamed on almost anything before it was traced back to here.
const (
	probeCapabilityID = 1
	firstImageID      = 100
)

// probeImages decides whether pictures can be drawn at all this session.
// Every check below returns false cheaply, in order of how expensive it is
// to find out: an environment variable, a syscall, then an actual
// round-trip to the terminal. A false here costs nothing but a picture —
// imageRows still reserves the rows, they just draw blank — so this
// function must never be the reason a session starts in a broken state.
func probeImages(fd int) bool {
	// tmux swallows the kitty graphics protocol outright; it does not even
	// pass the escape sequences through to the terminal underneath it. This
	// check matters here specifically because the developer's own daily
	// terminal usage is inside tmux.
	if os.Getenv("TMUX") != "" {
		return false
	}

	if w, h := cellPixels(fd); w == 0 || h == 0 {
		return false
	}

	return probeCapability(fd)
}

// probeCapability sends a query image (a=q, t=d — decode and discard,
// display nothing) and waits briefly for the terminal's reply, which
// contains "OK" when the terminal understands the protocol. This is the
// only reliable signal available: there is no terminfo capability or
// environment variable that announces kitty graphics support.
//
// Note this query deliberately omits q=2, unlike every other command in
// this file. q=2 suppresses the terminal's response entirely, including
// the "OK" this function exists to read — so the one exception to rule 1
// is the one command whose entire purpose is to be answered.
//
// The termios handling — save, clear ICANON/ECHO/ISIG, set VMIN=0 so a
// single Read returns after VTIME tenths of a second even if nothing
// arrives, restore on every exit path via defer — is the same pattern
// splash.go's waitForSplash uses for the same reason: one blocking Read,
// no goroutine, timer or signal handler that could outlive this call.
func probeCapability(fd int) bool {
	saved, err := getTermios(fd)
	if err != nil {
		return false
	}
	raw := *saved
	raw.Lflag &^= syscall.ICANON | syscall.ECHO | syscall.ISIG
	raw.Cc[syscall.VMIN] = 0
	raw.Cc[syscall.VTIME] = 3 // 0.3s: generous for a local pty, short enough not to stall startup
	if err := setTermios(fd, setFlush, &raw); err != nil {
		return false
	}
	defer func() {
		_ = setTermios(fd, setDrain, saved)
	}()

	payload := base64.StdEncoding.EncodeToString([]byte{0, 0, 0})
	query := fmt.Sprintf("\x1b_Gi=%d,s=1,v=1,a=q,t=d,f=24;%s\x1b\\", probeCapabilityID, payload)
	if _, err := os.Stdout.WriteString(query); err != nil {
		return false
	}

	buf := make([]byte, 256)
	n, _ := os.Stdin.Read(buf)
	return strings.Contains(string(buf[:n]), "OK")
}
