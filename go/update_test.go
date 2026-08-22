package main

import (
	"archive/tar"
	"bytes"
	"compress/gzip"
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"
)

// TestCompareVersionsNumericNotLexical is the whole reason compareVersions
// exists rather than strings.Compare: "0.10.0" is a newer release than
// "0.9.0" even though it sorts earlier lexically.
func TestCompareVersionsNumericNotLexical(t *testing.T) {
	if got := compareVersions("0.10.0", "0.9.0"); got != 1 {
		t.Fatalf("compareVersions(%q, %q) = %d, want 1", "0.10.0", "0.9.0", got)
	}
	if got := compareVersions("0.9.0", "0.10.0"); got != -1 {
		t.Fatalf("compareVersions(%q, %q) = %d, want -1", "0.9.0", "0.10.0", got)
	}
}

// TestCompareVersionsPadsShorterWithZero pins "1.2" == "1.2.0": a missing
// trailing component is a zero, not a wildcard and not an error.
func TestCompareVersionsPadsShorterWithZero(t *testing.T) {
	if got := compareVersions("1.2", "1.2.0"); got != 0 {
		t.Fatalf("compareVersions(%q, %q) = %d, want 0", "1.2", "1.2.0", got)
	}
	if got := compareVersions("1.2.0", "1.2"); got != 0 {
		t.Fatalf("compareVersions(%q, %q) = %d, want 0", "1.2.0", "1.2", got)
	}
}

// TestCompareVersionsUnparseableComponentIsZero covers the fallback
// strconv.Atoi is given: a component that isn't a number contributes 0
// rather than aborting the comparison.
func TestCompareVersionsUnparseableComponentIsZero(t *testing.T) {
	if got := compareVersions("1.x.0", "1.0.0"); got != 0 {
		t.Fatalf("compareVersions(%q, %q) = %d, want 0", "1.x.0", "1.0.0", got)
	}
}

func TestCompareVersionsEqual(t *testing.T) {
	if got := compareVersions("0.2.11", "0.2.11"); got != 0 {
		t.Fatalf("compareVersions(%q, %q) = %d, want 0", "0.2.11", "0.2.11", got)
	}
}

func TestLooksLikeVersionAccepts(t *testing.T) {
	if !looksLikeVersion("0.2.11") {
		t.Fatal("looksLikeVersion(\"0.2.11\") = false, want true")
	}
}

func TestLooksLikeVersionRejectsEmpty(t *testing.T) {
	if looksLikeVersion("") {
		t.Fatal("looksLikeVersion(\"\") = true, want false")
	}
}

// TestLooksLikeVersionRejectsLong pins the >=32-char guard, which exists so
// a page-sized garbage response is never mistaken for a version.
func TestLooksLikeVersionRejectsLong(t *testing.T) {
	long := ""
	for i := 0; i < 32; i++ {
		long += "1"
	}
	if looksLikeVersion(long) {
		t.Fatalf("looksLikeVersion(%d-char string) = true, want false", len(long))
	}
}

// TestLooksLikeVersionRejectsCaptivePortal is the guard's namesake case: a
// wifi captive portal answers every GET with an HTML page, and that must
// never be trusted as a version string.
func TestLooksLikeVersionRejectsCaptivePortal(t *testing.T) {
	if looksLikeVersion("<html><head><title>Sign in</title></head></html>") {
		t.Fatal("looksLikeVersion(captive-portal HTML) = true, want false")
	}
}

func TestVersionURLFor(t *testing.T) {
	cases := map[string]string{
		"main": "https://raw.githubusercontent.com/taliskerpruighe/tutor/main/version.txt",
		"tori": "https://raw.githubusercontent.com/taliskerpruighe/tutor/tori/version.txt",
	}
	for branch, want := range cases {
		if got := versionURLFor(branch); got != want {
			t.Errorf("versionURLFor(%q) = %q, want %q", branch, got, want)
		}
	}
}

// TestUpdateTagsFor pins the exact candidate list and its order. The order is
// the contract: namespaced entries first, one per name in updateBranches, so
// no pre-v0.2.12 release changes the candidate it resolves on; the bare tag
// last, because that is the shape v0.2.12 and v0.2.13 were published under
// and the reason a reader could see v0.2.13 in version.txt and still fail to
// download it.
func TestUpdateTagsFor(t *testing.T) {
	got := updateTagsFor("0.2.13")
	want := []string{"main/MkI_v0.2.13", "tori/MkI_v0.2.13", "MkI_v0.2.13"}

	if len(got) != len(want) {
		t.Fatalf("updateTagsFor(%q) = %q, want %q", "0.2.13", got, want)
	}
	for i := range want {
		if got[i] != want[i] {
			t.Errorf("updateTagsFor(%q)[%d] = %q, want %q", "0.2.13", i, got[i], want[i])
		}
	}
}

// TestUpdateTagsForBareTagIsLast states the ordering requirement separately
// from the exact-list check above, so that a future edit to updateBranches
// cannot quietly promote the bare tag ahead of the namespaced ones and take
// the historical releases' resolution with it.
func TestUpdateTagsForBareTagIsLast(t *testing.T) {
	got := updateTagsFor("0.2.13")
	if len(got) == 0 {
		t.Fatal("updateTagsFor returned no candidates")
	}
	if last := got[len(got)-1]; last != "MkI_v0.2.13" {
		t.Errorf("last candidate = %q, want the bare tag %q", last, "MkI_v0.2.13")
	}
	for i, tag := range got[:len(got)-1] {
		if !strings.Contains(tag, "/") {
			t.Errorf("candidate %d = %q, want a namespaced tag before the bare one", i, tag)
		}
	}
}

// TestUpdateTagsForDerivesFromUpdateBranches proves the namespaced entries
// are built from updateBranches rather than hardcoded, so adding a branch
// stays a one-line change in exactly one place.
func TestUpdateTagsForDerivesFromUpdateBranches(t *testing.T) {
	orig := updateBranches
	updateBranches = []string{"alpha", "beta", "gamma"}
	t.Cleanup(func() { updateBranches = orig })

	got := updateTagsFor("1.0.0")
	want := []string{"alpha/MkI_v1.0.0", "beta/MkI_v1.0.0", "gamma/MkI_v1.0.0", "MkI_v1.0.0"}

	if len(got) != len(want) {
		t.Fatalf("updateTagsFor = %q, want %q", got, want)
	}
	for i := range want {
		if got[i] != want[i] {
			t.Errorf("candidate %d = %q, want %q", i, got[i], want[i])
		}
	}
}

// withUpdateBranches points updateBranches and versionURLFmt at a test
// server for the duration of the calling test, restoring both on cleanup so
// no later test in the package observes the override.
func withUpdateBranches(t *testing.T, srv *httptest.Server, branches []string) {
	t.Helper()
	origBranches := updateBranches
	origFmt := versionURLFmt
	updateBranches = branches
	versionURLFmt = srv.URL + "/%s/version.txt"
	t.Cleanup(func() {
		updateBranches = origBranches
		versionURLFmt = origFmt
	})
}

// TestFetchLatestVersionFallsBackPastNotFound covers the ordinary rename
// case: the first candidate branch 404s and the second, reachable one wins.
func TestFetchLatestVersionFallsBackPastNotFound(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		switch r.URL.Path {
		case "/main/version.txt":
			w.WriteHeader(http.StatusNotFound)
		case "/tori/version.txt":
			fmt.Fprint(w, "0.2.11")
		default:
			w.WriteHeader(http.StatusNotFound)
		}
	}))
	defer srv.Close()
	withUpdateBranches(t, srv, []string{"main", "tori"})

	got, err := fetchLatestVersion(2 * time.Second)
	if err != nil {
		t.Fatalf("fetchLatestVersion: %v", err)
	}
	if got != "0.2.11" {
		t.Fatalf("fetchLatestVersion = %q, want %q", got, "0.2.11")
	}
}

// TestFetchLatestVersionStopsAtFirstSuccess is TestFetchLatestVersionFallsBackPastNotFound's
// converse: when the first candidate answers, the second must never even be
// requested.
func TestFetchLatestVersionStopsAtFirstSuccess(t *testing.T) {
	var secondRequested bool
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		switch r.URL.Path {
		case "/main/version.txt":
			fmt.Fprint(w, "0.2.11")
		case "/tori/version.txt":
			secondRequested = true
			fmt.Fprint(w, "0.2.11")
		default:
			w.WriteHeader(http.StatusNotFound)
		}
	}))
	defer srv.Close()
	withUpdateBranches(t, srv, []string{"main", "tori"})

	got, err := fetchLatestVersion(2 * time.Second)
	if err != nil {
		t.Fatalf("fetchLatestVersion: %v", err)
	}
	if got != "0.2.11" {
		t.Fatalf("fetchLatestVersion = %q, want %q", got, "0.2.11")
	}
	if secondRequested {
		t.Fatal("fetchLatestVersion requested the second candidate after the first succeeded")
	}
}

// TestFetchLatestVersionAllCandidatesFail pins that exhausting every branch
// is an error, not a silent empty success.
func TestFetchLatestVersionAllCandidatesFail(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
	}))
	defer srv.Close()
	withUpdateBranches(t, srv, []string{"main", "tori"})

	_, err := fetchLatestVersion(2 * time.Second)
	if err == nil {
		t.Fatal("fetchLatestVersion returned no error when every candidate 404s")
	}
}

// TestFetchLatestVersionRejectsCaptivePortalThenFallsBack covers the
// captive-portal guard as a per-candidate rejection: the first candidate
// answers 200 with an HTML body, looksLikeVersion rejects it, and the loop
// moves on to the second candidate exactly as it would after a network
// error or a 404.
func TestFetchLatestVersionRejectsCaptivePortalThenFallsBack(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		switch r.URL.Path {
		case "/main/version.txt":
			fmt.Fprint(w, "<html><head><title>Sign in</title></head></html>")
		case "/tori/version.txt":
			fmt.Fprint(w, "0.2.11")
		default:
			w.WriteHeader(http.StatusNotFound)
		}
	}))
	defer srv.Close()
	withUpdateBranches(t, srv, []string{"main", "tori"})

	got, err := fetchLatestVersion(2 * time.Second)
	if err != nil {
		t.Fatalf("fetchLatestVersion: %v", err)
	}
	if got != "0.2.11" {
		t.Fatalf("fetchLatestVersion = %q, want %q", got, "0.2.11")
	}
}

// TestFetchLatestVersionBudgetIsTotalNotPerCandidate is what proves budget
// bounds the whole call, not each candidate: the first candidate blocks
// well past the budget, and the assertion is that fetchLatestVersion still
// returns in comfortably under twice the budget rather than waiting out
// both candidates' timeouts in full. The budget is kept small so the test
// stays fast, and the blocking handler exits via a channel closed by
// t.Cleanup so the server can shut down cleanly instead of leaking a
// goroutine wedged in a sleep.
func TestFetchLatestVersionBudgetIsTotalNotPerCandidate(t *testing.T) {
	const budget = 200 * time.Millisecond
	unblock := make(chan struct{})

	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		switch r.URL.Path {
		case "/main/version.txt":
			select {
			case <-unblock:
			case <-time.After(2 * time.Second):
			}
			w.WriteHeader(http.StatusNotFound)
		case "/tori/version.txt":
			fmt.Fprint(w, "0.2.11")
		default:
			w.WriteHeader(http.StatusNotFound)
		}
	}))
	// Registration order matters here: t.Cleanup runs LIFO, and srv.Close
	// blocks until every outstanding handler returns. Registering it before
	// the unblock-closer means the closer (registered second, so run first)
	// releases the blocked handler before Close is asked to wait for it —
	// the reverse order would make Close sit out the full 2-second sleep
	// below on every run of this test.
	t.Cleanup(func() { srv.Close() })
	t.Cleanup(func() { close(unblock) })
	withUpdateBranches(t, srv, []string{"main", "tori"})

	start := time.Now()
	fetchLatestVersion(budget)
	elapsed := time.Since(start)

	if elapsed >= 2*budget {
		t.Fatalf("fetchLatestVersion took %v with a %v budget, want comfortably under %v", elapsed, budget, 2*budget)
	}
}

// withTarballURL points tarballURLFmt at a test server for the duration of
// the calling test, restoring it on cleanup so no later test in the package
// observes the override. It is the sibling of withUpdateBranches above, and
// it is the reason tarballURLFmt is a var: while it was a const, nothing
// below this line could be written at all, and the tag-prefix bug shipped
// through exactly that hole.
func withTarballURL(t *testing.T, srv *httptest.Server) {
	t.Helper()
	orig := tarballURLFmt
	tarballURLFmt = srv.URL + "/tar/%s"
	t.Cleanup(func() { tarballURLFmt = orig })
}

// pinUpdateBranches fixes updateBranches for the duration of the calling
// test, restoring it on cleanup. The tarball tests below spell out the exact
// tags they expect a server to be asked for, so they must not silently change
// meaning — or start failing — the day a name is added to updateBranches.
// That the real list stays derivable is TestUpdateTagsForDerivesFromUpdateBranches'
// job, not theirs.
func pinUpdateBranches(t *testing.T, branches ...string) {
	t.Helper()
	orig := updateBranches
	updateBranches = branches
	t.Cleanup(func() { updateBranches = orig })
}

// fakeReleaseTarball builds, in memory, a gzipped tar shaped the way GitHub
// serves one: every entry under a single leading directory named after the
// flattened tag. It carries the two directories fetchRelease's completeness
// check insists on (content/ and tui/bin/) plus an install.sh, so a tree
// unpacked from it can survive applyUpdate all the way through.
func fakeReleaseTarball(t *testing.T, prefix string) []byte {
	t.Helper()
	var buf bytes.Buffer
	gz := gzip.NewWriter(&buf)
	tw := tar.NewWriter(gz)

	dirs := []string{prefix + "/", prefix + "/content/", prefix + "/tui/", prefix + "/tui/bin/"}
	for _, d := range dirs {
		if err := tw.WriteHeader(&tar.Header{Name: d, Typeflag: tar.TypeDir, Mode: 0o755}); err != nil {
			t.Fatalf("writing tar dir %q: %v", d, err)
		}
	}

	files := map[string]string{
		prefix + "/content/index.md": "# fake\n",
		prefix + "/tui/bin/tutor":    "#!/bin/sh\nexit 0\n",
		prefix + "/install.sh":       "#!/bin/bash\nexit 0\n",
		prefix + "/version.txt":      "0.2.13\n",
	}
	for name, body := range files {
		hdr := &tar.Header{Name: name, Typeflag: tar.TypeReg, Mode: 0o755, Size: int64(len(body))}
		if err := tw.WriteHeader(hdr); err != nil {
			t.Fatalf("writing tar header %q: %v", name, err)
		}
		if _, err := tw.Write([]byte(body)); err != nil {
			t.Fatalf("writing tar body %q: %v", name, err)
		}
	}

	if err := tw.Close(); err != nil {
		t.Fatalf("closing tar: %v", err)
	}
	if err := gz.Close(); err != nil {
		t.Fatalf("closing gzip: %v", err)
	}
	return buf.Bytes()
}

// releaseServer serves a fake tarball for exactly one tag and 404s every
// other, recording the tags it was asked for in the order they arrived.
func releaseServer(t *testing.T, serveTag string, asked *[]string) *httptest.Server {
	t.Helper()
	return httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		tag := strings.TrimPrefix(r.URL.Path, "/tar/")
		*asked = append(*asked, tag)
		if tag != serveTag {
			w.WriteHeader(http.StatusNotFound)
			return
		}
		w.Header().Set("Content-Type", "application/gzip")
		_, _ = w.Write(fakeReleaseTarball(t, "tutor-"+strings.ReplaceAll(tag, "/", "-")))
	}))
}

// TestFetchReleaseAcceptsBareTag is the regression test for the bug itself.
// v0.2.13 was published as the bare tag "MkI_v0.2.13", and a fetch for it
// must succeed and unpack a usable tree.
func TestFetchReleaseAcceptsBareTag(t *testing.T) {
	var asked []string
	srv := releaseServer(t, "MkI_v0.2.13", &asked)
	defer srv.Close()
	withTarballURL(t, srv)

	dir, err := fetchRelease(t.TempDir(), "MkI_v0.2.13")
	if err != nil {
		t.Fatalf("fetchRelease on the bare tag failed: %v", err)
	}
	if info, err := os.Stat(filepath.Join(dir, "content")); err != nil || !info.IsDir() {
		t.Errorf("unpacked tree has no content/ directory: %v", err)
	}
	if info, err := os.Stat(filepath.Join(dir, "tui", "bin")); err != nil || !info.IsDir() {
		t.Errorf("unpacked tree has no tui/bin directory: %v", err)
	}
}

// TestFetchReleaseCleansUpOnFailure holds fetchRelease to the self-cleanup
// contract its doc comment promises: a candidate that 404s must not strand a
// tutor-update-* directory, or every failed candidate before the winner would
// leave one behind on every update that needed more than one try.
func TestFetchReleaseCleansUpOnFailure(t *testing.T) {
	var asked []string
	srv := releaseServer(t, "MkI_v0.2.13", &asked)
	defer srv.Close()
	withTarballURL(t, srv)

	parent := t.TempDir()
	if _, err := fetchRelease(parent, "main/MkI_v0.2.13"); err == nil {
		t.Fatal("fetchRelease succeeded on a tag the server 404s")
	}
	entries, err := os.ReadDir(parent)
	if err != nil {
		t.Fatalf("reading parent: %v", err)
	}
	if len(entries) != 0 {
		t.Errorf("failed fetch stranded %d entries in parent: %v", len(entries), entries)
	}
}

// TestApplyUpdateWalksPastNamespacedTagsToBareTag is the end-to-end proof
// that the candidate loop does what updateTagsFor's ordering promises: both
// namespaced tags are tried and 404, and the bare tag — the shape v0.2.13 was
// actually published under — is reached and installed. Against the pre-fix
// code this test cannot even compile, and against a fix that emitted only the
// namespaced tags it fails on the error applyUpdate returns.
func TestApplyUpdateWalksPastNamespacedTagsToBareTag(t *testing.T) {
	var asked []string
	srv := releaseServer(t, "MkI_v0.2.13", &asked)
	defer srv.Close()
	withTarballURL(t, srv)
	pinUpdateBranches(t, "main", "tori")

	parent := t.TempDir()
	root := filepath.Join(parent, "tutor")
	if err := os.MkdirAll(filepath.Join(root, "content"), 0o755); err != nil {
		t.Fatalf("seeding root: %v", err)
	}

	if err := applyUpdate(root, "0.2.13"); err != nil {
		t.Fatalf("applyUpdate failed on a release published under the bare tag: %v", err)
	}

	want := []string{"main/MkI_v0.2.13", "tori/MkI_v0.2.13", "MkI_v0.2.13"}
	if len(asked) != len(want) {
		t.Fatalf("server was asked for %q, want %q", asked, want)
	}
	for i := range want {
		if asked[i] != want[i] {
			t.Errorf("request %d was for %q, want %q", i, asked[i], want[i])
		}
	}

	// The swap really happened: the tree now on disk is the downloaded one.
	if _, err := os.Stat(filepath.Join(root, "tui", "bin", "tutor")); err != nil {
		t.Errorf("root was not replaced by the downloaded tree: %v", err)
	}
	if _, err := os.Stat(root + ".old"); !os.IsNotExist(err) {
		t.Errorf("the .old rollback directory was left behind")
	}
}

// TestApplyUpdateReportsEveryTagItTried covers the failure path a reader
// actually sees. When no candidate resolves, the error must name all three,
// because that message is what distinguishes a genuinely missing release from
// one tagged in a shape the candidate list does not cover — the distinction
// nobody could make while the bug was live.
func TestApplyUpdateReportsEveryTagItTried(t *testing.T) {
	var asked []string
	srv := releaseServer(t, "no-such-tag", &asked)
	defer srv.Close()
	withTarballURL(t, srv)
	pinUpdateBranches(t, "main", "tori")

	parent := t.TempDir()
	root := filepath.Join(parent, "tutor")
	if err := os.MkdirAll(root, 0o755); err != nil {
		t.Fatalf("seeding root: %v", err)
	}

	err := applyUpdate(root, "0.2.13")
	if err == nil {
		t.Fatal("applyUpdate succeeded with no resolvable tag")
	}
	for _, tag := range []string{"main/MkI_v0.2.13", "tori/MkI_v0.2.13", "MkI_v0.2.13"} {
		if !strings.Contains(err.Error(), tag) {
			t.Errorf("error %q does not name tried tag %q", err, tag)
		}
	}
	// A failed update must leave the existing install untouched.
	if _, err := os.Stat(root); err != nil {
		t.Errorf("failed update destroyed the existing root: %v", err)
	}
}
