package main

import (
	"os"
	"path/filepath"
	"testing"
)

func TestMarksRoundTrip(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "read.json")

	want := map[string]bool{"wiki/about-this-wiki": true, "wiki/this-version": true}
	if err := saveMarks(path, want); err != nil {
		t.Fatalf("saveMarks: %v", err)
	}
	got := loadMarks(path)
	if len(got) != len(want) {
		t.Fatalf("loadMarks returned %d ids, want %d (%v)", len(got), len(want), got)
	}
	for id := range want {
		if !got[id] {
			t.Errorf("loadMarks missing id %q", id)
		}
	}
}

// TestMarksSavedBytes pins the exact on-disk shape: sorted ids, two-space
// indent, no HTML escaping, one trailing newline — the same encoding
// encodeIndex uses for content/index.json, and for the same reason: Go and
// Python must produce identical bytes.
func TestMarksSavedBytes(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "read.json")

	set := map[string]bool{
		"wiki/this-version":    true,
		"wiki/about-this-wiki": true,
	}
	if err := saveMarks(path, set); err != nil {
		t.Fatalf("saveMarks: %v", err)
	}
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("ReadFile: %v", err)
	}
	want := "{\n" +
		"  \"read\": [\n" +
		"    \"wiki/about-this-wiki\",\n" +
		"    \"wiki/this-version\"\n" +
		"  ]\n" +
		"}\n"
	if string(data) != want {
		t.Fatalf("saveMarks bytes = %q, want %q", string(data), want)
	}
}

func TestLoadMarksMissingFile(t *testing.T) {
	dir := t.TempDir()
	got := loadMarks(filepath.Join(dir, "does-not-exist.json"))
	if got == nil {
		t.Fatal("loadMarks on a missing file returned nil, want an empty non-nil map")
	}
	if len(got) != 0 {
		t.Fatalf("loadMarks on a missing file returned %v, want empty", got)
	}
}

// TestLoadMarksGarbage is the same posture image.go's probeImages and
// splash.go's waitForSplash take: a corrupt file must never be the reason
// the reader fails to open, so this must return cleanly rather than panic.
func TestLoadMarksGarbage(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "read.json")
	if err := os.WriteFile(path, []byte("not json at all {{{"), 0o644); err != nil {
		t.Fatalf("WriteFile: %v", err)
	}
	got := loadMarks(path)
	if got == nil {
		t.Fatal("loadMarks on garbage returned nil, want an empty non-nil map")
	}
	if len(got) != 0 {
		t.Fatalf("loadMarks on garbage returned %v, want empty", got)
	}
}

func TestSaveMarksCreatesDirectory(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "nested", "deeper", "read.json")
	if err := saveMarks(path, map[string]bool{"a/b": true}); err != nil {
		t.Fatalf("saveMarks: %v", err)
	}
	if _, err := os.Stat(path); err != nil {
		t.Fatalf("read.json was not created: %v", err)
	}
}

func TestToggleRead(t *testing.T) {
	root := t.TempDir()
	index := Index{Parts: []Part{{
		Slug: "part", Title: "Part",
		Articles: []Article{{ID: "part/one", Title: "One"}},
	}}}

	// No readPath: in-memory only, never writes.
	app := NewApp(root, index, "")
	app.goTo(0, 0)
	if app.read["part/one"] {
		t.Fatal("article starts marked read")
	}
	app.toggleRead()
	if !app.read["part/one"] {
		t.Fatal("toggleRead did not mark the article read")
	}
	app.toggleRead()
	if app.read["part/one"] {
		t.Fatal("toggleRead did not unmark the article")
	}

	// readPath set: writes through.
	app.readPath = filepath.Join(t.TempDir(), "read.json")
	app.toggleRead()
	if _, err := os.Stat(app.readPath); err != nil {
		t.Fatalf("toggleRead with readPath set did not write the file: %v", err)
	}
	onDisk := loadMarks(app.readPath)
	if !onDisk["part/one"] {
		t.Fatalf("read.json does not contain the toggled id: %v", onDisk)
	}
}

// TestTickCharWidth guards the one fact that could have silently broken
// sidebar alignment and bin/parity.sh: if U+2713 CHECK MARK were ever
// measured as two columns instead of one, every article row in the sidebar
// would be a column wider than the fixed-width layout expects, and the tick
// would throw off every frame comparison in the parity harness rather than
// just the ones with a mark in them. Modelled on TestBlockCharWidth in
// splash_test.go, which guards the same property for █.
func TestTickCharWidth(t *testing.T) {
	if w := charWidth('✓'); w != 1 {
		t.Fatalf("charWidth('✓') = %d, want 1", w)
	}
}
