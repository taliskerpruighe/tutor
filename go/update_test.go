package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
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

func TestUpdateTagFor(t *testing.T) {
	cases := []struct {
		branch, ver, want string
	}{
		{"main", "0.2.11", "main/MkI_v0.2.11"},
		{"tori", "0.2.11", "tori/MkI_v0.2.11"},
	}
	for _, c := range cases {
		if got := updateTagFor(c.branch, c.ver); got != c.want {
			t.Errorf("updateTagFor(%q, %q) = %q, want %q", c.branch, c.ver, got, c.want)
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
