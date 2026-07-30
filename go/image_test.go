// Tests for the picture engine (image.go). Modelled on splash_test.go:
// small, targeted checks of arithmetic and wire format rather than anything
// that needs a real terminal — probeImages itself is untestable here
// because it does a blocking stdin read with no tty behind `go test`, so it
// is exercised only by inspection, the same footnote term_darwin.go already
// carries for its own untested half.
package main

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

// --------------------------------------------------------------------------
// pngSize
// --------------------------------------------------------------------------

func TestPngSizeFixture(t *testing.T) {
	w, h, err := pngSize("testdata/fixture.png")
	if err != nil {
		t.Fatalf("pngSize: %v", err)
	}
	if w != 120 || h != 80 {
		t.Fatalf("pngSize(fixture.png) = %d x %d, want 120 x 80", w, h)
	}
}

func TestPngSizeNotAPng(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "not-a-png.txt")
	// Needs to be at least 24 bytes so the failure is the signature check,
	// not io.ReadFull running out of file first — those are two different
	// failure paths in pngSize and both need covering, but not by the same
	// case.
	if err := os.WriteFile(path, []byte(strings.Repeat("not a png at all, ", 3)), 0o644); err != nil {
		t.Fatal(err)
	}
	if _, _, err := pngSize(path); err == nil {
		t.Fatal("pngSize on a non-PNG file returned no error")
	}
}

func TestPngSizeMissingFile(t *testing.T) {
	if _, _, err := pngSize("testdata/does-not-exist.png"); err == nil {
		t.Fatal("pngSize on a missing file returned no error")
	}
}

func TestPngSizeShortFile(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "short.png")
	// Shorter than the 24-byte header pngSize reads: exercises the
	// io.ReadFull failure path directly, distinct from the signature
	// mismatch TestPngSizeNotAPng covers.
	if err := os.WriteFile(path, []byte{0x89, 'P', 'N', 'G'}, 0o644); err != nil {
		t.Fatal(err)
	}
	if _, _, err := pngSize(path); err == nil {
		t.Fatal("pngSize on a short file returned no error")
	}
}

// --------------------------------------------------------------------------
// imageRows
//
// The table below is hand-checked, not derived from imageRows's own
// formula, at the exact pane widths bin/parity.sh diffs Go against Python
// at: 40, 60, 72, 100, 200.
// --------------------------------------------------------------------------

func TestImageRowsTable(t *testing.T) {
	// A 100 x 50 image is exactly 2:1 (the assumed cell aspect ratio), so
	// rows = paneW * 50 / (100 * 2) = paneW / 4 with no remainder at any of
	// the five widths below — clean enough to check by hand.
	cases := []struct {
		imgW, imgH, paneW, want int
	}{
		{100, 50, 40, 10},
		{100, 50, 60, 15},
		{100, 50, 72, 18},
		{100, 50, 100, 25},
		{100, 50, 200, 50},
	}
	for _, c := range cases {
		if got := imageRows(c.imgW, c.imgH, c.paneW); got != c.want {
			t.Errorf("imageRows(%d, %d, %d) = %d, want %d",
				c.imgW, c.imgH, c.paneW, got, c.want)
		}
	}
}

// TestImageRowsCeiling checks a case that does not divide evenly, so the
// ceiling in the formula is actually exercised rather than coincidentally
// satisfied by a round number. 53 * 72 = 3816; 127 * 2 = 254;
// 3816 / 254 = 15 remainder 6, so the true value rounds up to 16.
func TestImageRowsCeiling(t *testing.T) {
	if got := imageRows(127, 53, 72); got != 16 {
		t.Fatalf("imageRows(127, 53, 72) = %d, want 16", got)
	}
}

func TestImageRowsDegenerate(t *testing.T) {
	cases := []struct {
		imgW, imgH, paneW int
	}{
		{0, 50, 72},   // zero image width
		{100, 0, 72},  // zero image height -> zero rows, not an error
		{100, 50, 0},  // zero pane width
		{-5, 50, 72},  // negative image width
		{100, 50, -5}, // negative pane width
	}
	for _, c := range cases {
		if got := imageRows(c.imgW, c.imgH, c.paneW); got != 0 {
			t.Errorf("imageRows(%d, %d, %d) = %d, want 0", c.imgW, c.imgH, c.paneW, got)
		}
	}
}

// --------------------------------------------------------------------------
// imgTransmit
// --------------------------------------------------------------------------

// bigFile writes n arbitrary bytes to a temp path and returns it.
// imgTransmit never validates that its input is a real PNG — it only ever
// reads and base64's the file — so a synthetic payload is enough to force
// several chunks without committing a large fixture to the repo.
func bigFile(t *testing.T, n int) string {
	t.Helper()
	dir := t.TempDir()
	path := filepath.Join(dir, "payload.bin")
	buf := make([]byte, n)
	for i := range buf {
		buf[i] = byte(i)
	}
	if err := os.WriteFile(path, buf, 0o644); err != nil {
		t.Fatal(err)
	}
	return path
}

func TestImgTransmitChunking(t *testing.T) {
	path := bigFile(t, 10_000) // base64 inflates this past two 4096-char chunks
	var b strings.Builder
	if err := imgTransmit(&b, 42, path); err != nil {
		t.Fatal(err)
	}
	s := b.String()

	starts := strings.Count(s, "\x1b_G")
	ends := strings.Count(s, "\x1b\\")
	if starts != ends {
		t.Fatalf("unbalanced escape sequences: %d starts, %d ends", starts, ends)
	}
	if starts < 2 {
		t.Fatalf("payload of %d encoded bytes should need more than one chunk, got %d", len(s), starts)
	}

	if got := strings.Count(s, "m=0;") + strings.Count(s, "m=0,"); got != 1 {
		t.Fatalf("want exactly one terminating chunk (m=0), got %d", got)
	}

	for _, chunk := range strings.Split(s, "\x1b_G")[1:] {
		semi := strings.Index(chunk, ";")
		end := strings.Index(chunk, "\x1b\\")
		payload := chunk[semi+1 : end]
		if len(payload) > 4096 {
			t.Fatalf("chunk payload of %d bytes exceeds the 4096 limit", len(payload))
		}
	}
}

func TestImgTransmitMissingFile(t *testing.T) {
	var b strings.Builder
	if err := imgTransmit(&b, 1, "testdata/does-not-exist.png"); err == nil {
		t.Fatal("imgTransmit on a missing file returned no error")
	}
}

// --------------------------------------------------------------------------
// q=2 on every command, C=1 on placements
//
// Rule 1 (every kitty command carries q=2) and rule 2 (imgPlace carries
// C=1) are the two load-bearing rules a silent regression could break
// without any visible symptom until a keypress starts misbehaving in a
// live terminal — exactly the kind of bug this test suite exists to catch
// before that terminal is the reader's.
// --------------------------------------------------------------------------

// commandSegments splits s on the APC opener so each element after the
// first is one kitty command's own text (control string plus payload).
func commandSegments(s string) []string {
	parts := strings.Split(s, "\x1b_G")
	if len(parts) > 0 {
		parts = parts[1:]
	}
	return parts
}

func TestQ2OnEveryCommand(t *testing.T) {
	var b strings.Builder
	path := bigFile(t, 200)
	if err := imgTransmit(&b, 5, path); err != nil {
		t.Fatal(err)
	}
	imgClearPlacements(&b)
	imgFreeAll(&b)
	imgPlace(&b, placement{id: 5, path: path, row: 3, col: 21, cols: 40, rows: 10, srcY: 0, srcH: 200})

	for _, seg := range commandSegments(b.String()) {
		control := seg
		if i := strings.Index(seg, ";"); i >= 0 {
			control = seg[:i]
		}
		if !strings.Contains(control, "q=2") {
			t.Fatalf("kitty command missing q=2: %q", control)
		}
	}
}

func TestImgPlaceHasC1(t *testing.T) {
	var b strings.Builder
	imgPlace(&b, placement{id: 5, path: "x.png", row: 3, col: 21, cols: 40, rows: 10, srcY: 0, srcH: 200})
	if !strings.Contains(b.String(), "C=1") {
		t.Fatalf("imgPlace output missing C=1: %q", b.String())
	}
}

func TestImgClearAndFreeDistinctScope(t *testing.T) {
	// imgClearPlacements keeps the transmitted pixels (lowercase d=a);
	// imgFreeAll drops them too (uppercase d=A). Mixing the two up would
	// either leak decoded image data for the whole session or force a
	// needless re-transmit every frame — this pins the case distinction so
	// a future edit cannot invert it silently.
	var clear, free strings.Builder
	imgClearPlacements(&clear)
	imgFreeAll(&free)
	if !strings.Contains(clear.String(), "d=a") {
		t.Fatalf("imgClearPlacements should send d=a, got %q", clear.String())
	}
	if !strings.Contains(free.String(), "d=A") {
		t.Fatalf("imgFreeAll should send d=A, got %q", free.String())
	}
}

// --------------------------------------------------------------------------
// content/images size gate
//
// The reader downloads the whole repository from GitHub, so this is what
// stops the course quietly turning into a large download.
// The directory does not exist yet at the time this file was written; the
// gate goes live the moment the first picture is added under it.
// --------------------------------------------------------------------------

func TestImageAssetsStaySmall(t *testing.T) {
	const maxSize = 500 * 1024

	dir := filepath.Join("..", "content", "images")
	entries, err := os.ReadDir(dir)
	if err != nil {
		t.Skipf("content/images does not exist yet: %v", err)
	}
	if len(entries) == 0 {
		t.Skip("content/images exists but is empty")
	}

	for _, e := range entries {
		if e.IsDir() {
			continue
		}
		if !strings.HasSuffix(strings.ToLower(e.Name()), ".png") {
			t.Errorf("content/images/%s is not a .png file", e.Name())
			continue
		}
		info, err := e.Info()
		if err != nil {
			t.Errorf("content/images/%s: %v", e.Name(), err)
			continue
		}
		if info.Size() > maxSize {
			t.Errorf("content/images/%s is %d bytes, exceeds the %d byte cap",
				e.Name(), info.Size(), maxSize)
		}
	}
}
