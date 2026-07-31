// Read marks: the one thing tutor writes outside its own folder.
//
// Everything else this reader touches — content/, content/index.json, the
// caches in app.go — lives inside the tutor tree, because the tree itself is
// disposable: applyUpdate (update.go:268-291) renames the whole thing aside
// and os.RemoveAlls it on every upgrade. A mark file kept inside that tree
// would be destroyed the moment she updated, which defeats the entire point
// of remembering what she has read.
//
// So marks live in $TUTOR_STATE if set, else ~/.local/share/tutor — the
// directory install.sh already creates (its STATE_DIR) and already writes
// one file into, the "home" pointer main.go's resolveRoot reads back.
// read.json sits beside it. $TUTOR_STATE is the counterpart to the existing
// $TUTOR_HOME: it exists so bin/parity.sh can pin state the same deterministic
// way it already pins the corpus.
package main

import (
	"bytes"
	"encoding/json"
	"os"
	"path/filepath"
	"sort"
)

// marksFile is the on-disk shape of read.json. It is an object rather than a
// bare array of ids so that a later key — a saved scroll position, say — can
// be added without breaking the format.
type marksFile struct {
	Read []string `json:"read"`
}

func stateDir() string {
	if env := os.Getenv("TUTOR_STATE"); env != "" {
		return env
	}
	return filepath.Join(homeDir(), ".local", "share", "tutor")
}

func marksPath() string {
	return filepath.Join(stateDir(), "read.json")
}

// loadMarks reads the set of read article ids, keyed on Article.ID
// (content.go:35) rather than Path, because an id survives renumbering a
// directory and a path does not.
//
// A missing file, an unreadable one, or malformed JSON all return an empty,
// non-nil map rather than an error: a corrupt marks file must never be the
// reason the reader fails to open. There is precedent for that posture
// elsewhere in this codebase — probeImages's "a false here costs nothing but
// a picture" (image.go:249), waitForSplash's "a launch screen must never be
// the reason the reader fails to open" (splash.go:307), and loadIndex's "a
// read-only install still works; it just cannot cache" (content.go:465).
//
// Ids naming articles that no longer exist are kept, not pruned: nothing
// looks them up against the current index, and pruning would lose marks made
// against a temporary checkout of an older corpus.
func loadMarks(path string) map[string]bool {
	out := map[string]bool{}
	data, err := os.ReadFile(path)
	if err != nil {
		return out
	}
	var mf marksFile
	if err := json.Unmarshal(data, &mf); err != nil {
		return out
	}
	for _, id := range mf.Read {
		out[id] = true
	}
	return out
}

// saveMarks writes the set back, sorted so the file is stable and diffable
// from one save to the next.
//
// Encoding matches encodeIndex (content.go:410-419) exactly — json.NewEncoder
// into a bytes.Buffer, SetEscapeHTML(false), SetIndent("", "  ") — for the
// same reason: Go and Python must produce identical bytes.
//
// The write itself goes to path+".new" and is then renamed into place, the
// same insurance install.sh takes over the launcher (it writes
// $LAUNCHER.new, then mv -f's it into place) — a crash or a power cut mid
// write leaves the old, still-valid file where it was instead of a
// half-written one.
func saveMarks(path string, set map[string]bool) error {
	ids := make([]string, 0, len(set))
	for id := range set {
		ids = append(ids, id)
	}
	sort.Strings(ids)

	var buf bytes.Buffer
	enc := json.NewEncoder(&buf)
	enc.SetEscapeHTML(false)
	enc.SetIndent("", "  ")
	if err := enc.Encode(marksFile{Read: ids}); err != nil {
		return err
	}

	if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil {
		return err
	}
	tmp := path + ".new"
	if err := os.WriteFile(tmp, buf.Bytes(), 0o644); err != nil {
		return err
	}
	return os.Rename(tmp, path)
}
