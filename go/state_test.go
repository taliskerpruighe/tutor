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

// TestNCharWidth is TestTickCharWidth's counterpart for the new marker: the
// mark slot is a single column, shared by the tick and the N, so a glyph
// measuring two columns there would shift every article title in the
// sidebar one column right of where the fixed-width layout expects it.
func TestNCharWidth(t *testing.T) {
	if w := charWidth('N'); w != 1 {
		t.Fatalf("charWidth('N') = %d, want 1", w)
	}
}

func TestLoadInstalledMissingFile(t *testing.T) {
	dir := t.TempDir()
	got := loadInstalled(filepath.Join(dir, "does-not-exist"))
	if got != "" {
		t.Fatalf("loadInstalled on a missing file = %q, want empty", got)
	}
}

func TestLoadInstalledTrimsWhitespace(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "installed")
	if err := os.WriteFile(path, []byte("0.2.1\n"), 0o644); err != nil {
		t.Fatalf("WriteFile: %v", err)
	}
	got := loadInstalled(path)
	if got != "0.2.1" {
		t.Fatalf("loadInstalled(%q) = %q, want %q", path, got, "0.2.1")
	}
}

// TestLoadInstalledWhitespaceOnly pins the equivalence loadInstalled's own
// comment promises: a file holding nothing but whitespace must come back as
// "", exactly as a missing file does. That equivalence is load-bearing
// rather than incidental — absence of the installed marker is what marks a
// reader who predates this feature, and a whitespace-only file must not be
// mistaken for one who has it recorded.
func TestLoadInstalledWhitespaceOnly(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "installed")
	if err := os.WriteFile(path, []byte("  \n\t \n"), 0o644); err != nil {
		t.Fatalf("WriteFile: %v", err)
	}
	got := loadInstalled(path)
	if got != "" {
		t.Fatalf("loadInstalled on whitespace-only = %q, want empty", got)
	}
}

// TestIsNewArticleDrawsWhenUnreadAndJustInstalled covers the upgrading
// reader: the article's version matches this release, nothing has recorded
// an earlier install, and the article has not been read, so it draws N.
func TestIsNewArticleDrawsWhenUnreadAndJustInstalled(t *testing.T) {
	article := Article{ID: "part/one", Version: "v" + version}
	if !isNewArticle(article, false, "") {
		t.Fatal("isNewArticle = false, want true for an unread article of the current version with no installed marker")
	}
}

// TestIsNewArticleReadWins mirrors the comment on isNewArticle itself: read
// beats new by construction, so marking the article read must suppress the
// N even though nothing else about the article changed.
func TestIsNewArticleReadWins(t *testing.T) {
	article := Article{ID: "part/one", Version: "v" + version}
	if isNewArticle(article, true, "") {
		t.Fatal("isNewArticle = true for a read article, want false")
	}
}

// TestIsNewArticleOlderVersionNeverNew is the ordinary case: most of the
// corpus predates the releases in newVersions, and none of it should ever
// draw N regardless of what the installed marker says. v0.2.3 is used
// rather than the current version's predecessor precisely because the rule
// is now a two-version allowlist — the release before this one still draws
// N, and the test below asserts that on purpose.
func TestIsNewArticleOlderVersionNeverNew(t *testing.T) {
	article := Article{ID: "part/one", Version: "v0.2.3"}
	if isNewArticle(article, false, "") {
		t.Fatal("isNewArticle = true for an article from an older release, want false")
	}
}

// TestIsNewArticlePreviousReleaseStillNew is the companion, and the whole
// point of the allowlist: a reader upgrading across a release boundary is
// shown everything added since she last looked, not merely the batch this
// release added. Every version in newVersions must draw N, including the
// one that is no longer current.
func TestIsNewArticlePreviousReleaseStillNew(t *testing.T) {
	for _, v := range newVersions {
		article := Article{ID: "part/one", Version: v}
		if !isNewArticle(article, false, "") {
			t.Fatalf("isNewArticle = false for %s, want true: every version in newVersions draws N", v)
		}
	}
	if len(newVersions) < 2 {
		t.Fatal("newVersions holds fewer than two releases; the allowlist has degenerated to the equality rule it replaced")
	}
}

// TestIsNewArticleSuppressedOnFreshInstall is the whole reason
// $STATE_DIR/installed exists: a reader who installs THIS release for the
// first time has every article at the current version, and none of them
// arrived as an update she has not seen yet — install.sh records the
// version she installed at precisely so this case is distinguishable from
// the upgrading reader above.
func TestIsNewArticleSuppressedOnFreshInstall(t *testing.T) {
	article := Article{ID: "part/one", Version: "v" + version}
	if isNewArticle(article, false, version) {
		t.Fatal("isNewArticle = true when installed equals the current version, want false")
	}
}
