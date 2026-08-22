// Self-update: check GitHub for a newer tagged release, and if asked,
// download and install it.
//
// Everything network- and archive-related lives in this file so the rest of
// the tree stays free of it. No shelling out to git/curl/tar/python — the
// end user's Mac has stubbed those to trigger a ~1 GB Xcode CLT download.
// Only net/http, archive/tar, compress/gzip and the rest of stdlib are used
// to fetch and unpack the release; installing the unpacked binaries is left
// to install.sh, which already knows how to shed the quarantine xattr and
// survive ETXTBSY — this file must never copy a binary itself.
package main

import (
	"archive/tar"
	"compress/gzip"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
	"time"
)

// updateBranches is the ordered list of branches the updater will look at,
// first hit wins. "main" leads because it is where this repo is going;
// "tori" trails because every copy installed before v0.2.11 was told to
// look there, and nothing but this list makes the two names interchangeable
// for a reader on either side of the rename. A branch that does not exist
// 404s in milliseconds, so carrying a name that is not there yet costs a
// round trip, not a stall.
var updateBranches = []string{"main", "tori"}

// versionURLFmt is a var rather than a const purely so update_test.go can
// point it at an httptest server; nothing in the programme itself may write
// it.
var versionURLFmt = "https://raw.githubusercontent.com/taliskerpruighe/tutor/%s/version.txt"

// tarballURLFmt is a var rather than a const purely so update_test.go can
// point it at an httptest server; nothing in the programme itself may write
// it. It was a const until the tag-prefix bug, and that is precisely why the
// bug shipped: with no way to redirect a tarball fetch, neither fetchRelease
// nor applyUpdate could be tested at all, and the candidate loop below went
// unexercised.
var tarballURLFmt = "https://codeload.github.com/taliskerpruighe/tutor/tar.gz/refs/tags/%s"

const (
	// Release tags in this repo come in two shapes, because the convention
	// changed mid-flight and the old tags were never renamed.
	//
	// Up through v0.2.11 every tag was namespaced by the trunk it was cut
	// on: "main/MkI_v0.2.11", or "tori/MkI_v0.2.11" on the other side of the
	// rename. From v0.2.12 onward the branch prefix was simply left off and
	// the tags are bare: "MkI_v0.2.12", "MkI_v0.2.13".
	//
	// So neither shape can be assumed. updateTagsFor builds both, namespaced
	// first (every historical release resolves exactly as it always has) and
	// bare last (which is what catches v0.2.12 onward). Emitting only the
	// namespaced form is the bug this pair of constants exists to prevent
	// recurring: the reader would find v0.2.13 in version.txt, correctly
	// announce it, then 404 on both namespaced candidates and report the
	// release missing while it sat on GitHub under the shorter name.
	bareTagPrefix = "MkI_v"
	tagPrefixFmt  = "%s/" + bareTagPrefix

	// A cached remote version is trusted for this long before the network is
	// asked again. Zero disables the cache entirely, so every launch checks.
	updateCacheTTL = 0

	// updateCheckBudget bounds fetchLatestVersion's TOTAL spend across every
	// candidate branch combined, not per request. checkForUpdate runs this on
	// every launch and must never make an offline reader wait longer than
	// this no matter how long updateBranches grows — a naive "timeout per
	// candidate" loop would instead make her wait the sum of every
	// candidate's timeout, and that sum grows every time a branch is added
	// to the list. An unreachable first candidate can still consume the
	// whole budget and starve the fallback, but that only happens when the
	// reader has no network at all, in which case the fallback would have
	// failed too. A branch that merely does not exist 404s fast and leaves
	// the budget almost untouched for the next candidate.
	updateCheckBudget = 2 * time.Second

	// updateFetchBudget is cmdUpdate's budget instead: the reader typed the
	// word "update" herself, so she can afford to wait longer than the
	// silent launch-time check may.
	updateFetchBudget = 10 * time.Second
)

// versionURLFor is the per-branch version.txt URL.
func versionURLFor(branch string) string {
	return fmt.Sprintf(versionURLFmt, branch)
}

// updateTagsFor returns every release tag ver might have been published
// under, in the order applyUpdate should try them: one namespaced tag per
// name in updateBranches, then the bare tag last.
//
// The order is the whole point. Namespaced first means a pre-v0.2.12 release
// resolves on the same candidate it always did, so nothing about an older
// reader's update path changes. Bare last means a release tagged without the
// branch prefix is still found, one extra round trip later — and a tag that
// does not exist 404s in milliseconds, so that trip costs essentially
// nothing.
//
// The namespaced entries are derived from updateBranches rather than spelled
// out, so adding a branch stays the one-line change it is today.
func updateTagsFor(ver string) []string {
	tags := make([]string, 0, len(updateBranches)+1)
	for _, branch := range updateBranches {
		tags = append(tags, fmt.Sprintf(tagPrefixFmt, branch)+ver)
	}
	return append(tags, bareTagPrefix+ver)
}

// updateCacheFile is where the last-seen remote version is written after
// every check. It is no longer what makes an ordinary launch skip the
// network — checkForUpdate calls out every time now — but cachedUpdateVersion
// reads this file, and that is what `tutor doctor` relies on, since doctor is
// routinely run from an agent's tool call and must never make a network call
// of its own. ~/.local/share/tutor/ already exists by the time this runs —
// install.sh creates it.
func updateCacheFile() string {
	return filepath.Join(filepath.Dir(pointerFile()), "update-check")
}

// compareVersions compares two dotted numeric version strings. It returns
// -1 if a < b, 0 if equal, 1 if a > b. Comparison is per-component and
// numeric, not lexical: "0.10.0" is newer than "0.9.0". Differing component
// counts are padded with zero ("1.2" == "1.2.0"), and an unparseable
// component is treated as 0.
func compareVersions(a, b string) int {
	as := strings.Split(a, ".")
	bs := strings.Split(b, ".")
	n := len(as)
	if len(bs) > n {
		n = len(bs)
	}
	for i := 0; i < n; i++ {
		var av, bv int
		if i < len(as) {
			av, _ = strconv.Atoi(strings.TrimSpace(as[i]))
		}
		if i < len(bs) {
			bv, _ = strconv.Atoi(strings.TrimSpace(bs[i]))
		}
		if av != bv {
			if av < bv {
				return -1
			}
			return 1
		}
	}
	return 0
}

// looksLikeVersion sanity-checks a would-be version string before it is
// trusted for anything: a captive-portal HTML page must never be mistaken
// for a version string.
func looksLikeVersion(s string) bool {
	if s == "" || len(s) >= 32 {
		return false
	}
	for _, r := range s {
		if (r < '0' || r > '9') && r != '.' {
			return false
		}
	}
	return true
}

// fetchVersionOnce makes the actual network call against a single branch's
// version.txt, bounded by timeout. It is the part of fetchLatestVersion that
// talks to exactly one candidate; the loop in fetchLatestVersion is what
// tries the rest of updateBranches when this returns an error.
func fetchVersionOnce(url string, timeout time.Duration) (string, error) {
	client := &http.Client{Timeout: timeout}
	resp, err := client.Get(url)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("unexpected status: %s", resp.Status)
	}
	body, err := io.ReadAll(io.LimitReader(resp.Body, 1024))
	if err != nil {
		return "", err
	}
	latest := strings.TrimSpace(string(body))
	if !looksLikeVersion(latest) {
		return "", fmt.Errorf("unexpected response body")
	}
	return latest, nil
}

// fetchLatestVersion tries each branch in updateBranches in order, first
// success wins. budget bounds the TOTAL time spent across every candidate
// combined: one deadline is computed up front, and each candidate's client
// timeout is whatever remains until that deadline, so the list can grow
// without the launch-path wait growing with it (see updateCheckBudget's
// comment for the full reasoning). Any failure at all — connect error,
// non-200 status, or a looksLikeVersion rejection (the captive-portal
// guard) — advances to the next candidate; if every candidate fails, or the
// budget runs out before one is even tried, the returned error mentions the
// last failure seen. Callers decide how to handle failure: checkForUpdate
// swallows it, cmdUpdate reports it.
func fetchLatestVersion(budget time.Duration) (string, error) {
	deadline := time.Now().Add(budget)
	var lastErr error
	for _, branch := range updateBranches {
		remaining := time.Until(deadline)
		if remaining <= 0 {
			break
		}
		v, err := fetchVersionOnce(versionURLFor(branch), remaining)
		if err != nil {
			lastErr = fmt.Errorf("%s: %w", branch, err)
			continue
		}
		return v, nil
	}
	if lastErr == nil {
		lastErr = fmt.Errorf("budget exhausted before any branch could be tried")
	}
	return "", fmt.Errorf("checking for updates: %w", lastErr)
}

// checkForUpdate answers "is a newer version available?" for the launch-time
// prompt. It now runs the network call on every launch — the cache file is
// still written below on every check, so it stays fresher than before rather
// than staler, but it is no longer trusted to answer this question; that
// makes cachedUpdateVersion's answer for `tutor doctor` current within one
// launch instead of within a day. Any failure at all — no network, timeout,
// non-200, garbage body, unwritable cache — is silent: it returns ("", false)
// and must never print anything or block startup. updateCheckBudget is what
// keeps that promise bounded regardless of how many branches updateBranches
// carries.
func checkForUpdate() (latest string, available bool) {
	cache := updateCacheFile()
	// updateCacheTTL is 0, so this guard is what stops the bare comparison
	// below from misbehaving rather than the comparison being dead code:
	// time.Since(mod) < 0 evaluates true whenever the cache file's mtime sits
	// in the future, which a backwards clock adjustment produces, and
	// without this guard a stale cached version would then be trusted
	// indefinitely. The guard keeps the constant meaning exactly what it
	// says, and keeps the cache usable again if the TTL is ever raised.
	if updateCacheTTL > 0 {
		if info, err := os.Stat(cache); err == nil && time.Since(info.ModTime()) < updateCacheTTL {
			data, err := os.ReadFile(cache)
			if err != nil {
				return "", false
			}
			cached := strings.TrimSpace(string(data))
			if !looksLikeVersion(cached) {
				return "", false
			}
			if compareVersions(cached, version) > 0 {
				return cached, true
			}
			return "", false
		}
	}

	fetched, err := fetchLatestVersion(updateCheckBudget)
	if err != nil {
		return "", false
	}
	// Write the cache regardless of whether it is newer, so
	// cachedUpdateVersion — and with it `tutor doctor` — stays current:
	// doctor should report the same answer this launch just reached, not a
	// stale one left over from whenever the cache was last written.
	_ = os.WriteFile(cache, []byte(fetched), 0o644)

	if compareVersions(fetched, version) > 0 {
		return fetched, true
	}
	return "", false
}

// cachedUpdateVersion reads only the cache file, never the network. It is
// what `tutor doctor` uses, since doctor is routinely run from an agent's
// tool call and must never make a network call of its own.
func cachedUpdateVersion() (latest string, available bool) {
	data, err := os.ReadFile(updateCacheFile())
	if err != nil {
		return "", false
	}
	cached := strings.TrimSpace(string(data))
	if !looksLikeVersion(cached) {
		return "", false
	}
	if compareVersions(cached, version) > 0 {
		return cached, true
	}
	return "", false
}

// fetchRelease downloads and unpacks the tarball for tag into a fresh temp
// directory created under parent, and sanity-checks the unpacked tree. On
// success it returns that directory's path and the caller owns it from
// there.
//
// On ANY error return, fetchRelease removes the tmpdir it created before
// returning ("", err) — it does not leave that to the caller. This matters
// because applyUpdate now calls fetchRelease once per candidate tag: if
// a candidate failed partway through, mid-download or mid-untar, and left
// its cleanup to whoever eventually accepts a different candidate's
// directory, every failed candidate before the winner would strand a
// tutor-update-* directory in the reader's home — one per failed tag, on
// every single update that needed more than one try. So this function's
// self-cleanup is implemented with a defer guarded on a named `ok bool`,
// set true just before the one successful return; every other return path
// leaves `ok` false and the defer removes the directory. applyUpdate keeps
// its own separate `swapped` guard, but that one covers only the single
// tmpdir it ends up accepting, never a rejected candidate's.
func fetchRelease(parent, tag string) (tmpdir string, err error) {
	url := fmt.Sprintf(tarballURLFmt, tag)

	client := &http.Client{Timeout: 5 * time.Minute}
	resp, err := client.Get(url)
	if err != nil {
		return "", fmt.Errorf("downloading %s: %w", tag, err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("downloading %s: unexpected status %s", tag, resp.Status)
	}

	gz, err := gzip.NewReader(resp.Body)
	if err != nil {
		return "", fmt.Errorf("opening tarball: %w", err)
	}
	defer gz.Close()

	tmpdir, err = os.MkdirTemp(parent, "tutor-update-*")
	if err != nil {
		return "", fmt.Errorf("creating temp dir: %w", err)
	}
	ok := false
	defer func() {
		if !ok {
			os.RemoveAll(tmpdir)
		}
	}()

	absTmp, err := filepath.Abs(tmpdir)
	if err != nil {
		return "", err
	}

	tr := tar.NewReader(gz)
	for {
		hdr, err := tr.Next()
		if err == io.EOF {
			break
		}
		if err != nil {
			return "", fmt.Errorf("reading tarball: %w", err)
		}

		// Every entry is prefixed with exactly one directory, whichever tag
		// shape produced it: GitHub flattens a namespaced tag's slash, so
		// "main/MkI_v0.2.11" gives "tutor-main-MkI_v0.2.11/" and
		// "tori/MkI_v0.2.11" gives "tutor-tori-MkI_v0.2.11/", while a bare
		// tag like "MkI_v0.2.13" simply gives "tutor-MkI_v0.2.13/". The
		// slash is flattened, never preserved, so the depth is one in every
		// case. Strip exactly one leading path component regardless.
		parts := strings.SplitN(hdr.Name, "/", 2)
		if len(parts) < 2 || parts[1] == "" {
			continue
		}
		rel := parts[1]

		dest := filepath.Join(tmpdir, rel)
		absDest, err := filepath.Abs(dest)
		if err != nil {
			return "", err
		}
		if absDest != absTmp && !strings.HasPrefix(absDest, absTmp+string(os.PathSeparator)) {
			return "", fmt.Errorf("tar-slip: entry %q escapes the destination", hdr.Name)
		}

		switch hdr.Typeflag {
		case tar.TypeDir:
			if err := os.MkdirAll(dest, 0o755); err != nil {
				return "", err
			}
		case tar.TypeReg:
			if err := os.MkdirAll(filepath.Dir(dest), 0o755); err != nil {
				return "", err
			}
			mode := os.FileMode(hdr.Mode) & 0o777
			f, err := os.OpenFile(dest, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, mode)
			if err != nil {
				return "", err
			}
			_, err = io.Copy(f, tr)
			f.Close()
			if err != nil {
				return "", err
			}
		default:
			// No symlinks, no devices — skip anything that isn't a plain
			// file or a directory.
			continue
		}
	}

	// Sanity-check the unpacked tree before touching anything real: a
	// truncated or wrong download must not replace a working install.
	if info, err := os.Stat(filepath.Join(tmpdir, "content")); err != nil || !info.IsDir() {
		return "", fmt.Errorf("update package looks incomplete: no content/ directory")
	}
	if info, err := os.Stat(filepath.Join(tmpdir, "tui", "bin")); err != nil || !info.IsDir() {
		return "", fmt.Errorf("update package looks incomplete: no tui/bin directory")
	}

	ok = true
	return tmpdir, nil
}

// applyUpdate tries each tag in updateTagsFor(ver) in turn — the namespaced
// ones first, the bare one last — asking fetchRelease to download and unpack
// the tarball for it and taking the first that succeeds. If every tag fails,
// it returns an error naming every one it tried, which is what tells a reader
// whether the release is genuinely missing or merely tagged in a shape this
// list does not cover. From there — swapping the accepted directory in,
// rolling back on failure, delegating to install.sh — nothing changed: this
// function must never copy a binary itself, that is install.sh's job, and
// only it sheds the quarantine xattr and survives ETXTBSY correctly.
func applyUpdate(root string, ver string) error {
	parent := filepath.Dir(root)

	var tmpdir string
	var triedTags []string
	var lastErr error
	for _, tag := range updateTagsFor(ver) {
		triedTags = append(triedTags, tag)
		dir, err := fetchRelease(parent, tag)
		if err != nil {
			lastErr = err
			continue
		}
		tmpdir = dir
		break
	}
	if tmpdir == "" {
		return fmt.Errorf("fetching release (tried %s): %w", strings.Join(triedTags, ", "), lastErr)
	}

	// swapped covers only the tmpdir this loop accepted — every other
	// candidate's directory was already cleaned up by fetchRelease itself
	// on its own error path, per the comment on that function.
	swapped := false
	defer func() {
		if !swapped {
			os.RemoveAll(tmpdir)
		}
	}()

	oldPath := root + ".old"
	if err := os.Rename(root, oldPath); err != nil {
		return fmt.Errorf("moving %s aside: %w", root, err)
	}
	if err := os.Rename(tmpdir, root); err != nil {
		if rbErr := os.Rename(oldPath, root); rbErr != nil {
			return fmt.Errorf("swap failed (%v) and rollback failed too (%v)", err, rbErr)
		}
		return fmt.Errorf("swapping in the update: %w", err)
	}
	swapped = true

	cmd := exec.Command("bash", filepath.Join(root, "install.sh"))
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	if err := cmd.Run(); err != nil {
		os.RemoveAll(root)
		if rbErr := os.Rename(oldPath, root); rbErr != nil {
			return fmt.Errorf("install.sh failed (%v) and rollback failed too (%v)", err, rbErr)
		}
		return fmt.Errorf("install.sh failed: %w", err)
	}

	os.RemoveAll(oldPath)
	return nil
}

// cmdUpdate is the explicit `tutor update` subcommand: the reader typed the
// word "update", so it always fetches, and it refreshes the cache file
// afterward so cachedUpdateVersion, and with it `tutor doctor`, stay current.
func cmdUpdate(root string) int {
	fmt.Printf("Installed version: %s\n", version)

	latest, err := fetchLatestVersion(updateFetchBudget)
	if err != nil {
		fmt.Fprintf(os.Stderr, "could not check for updates: %v\n", err)
		return 1
	}
	// Refresh the cache while we're here, purely for cachedUpdateVersion's
	// sake: `tutor doctor` reads that file, never the network, and this
	// keeps its answer as current as the check this command just made.
	_ = os.WriteFile(updateCacheFile(), []byte(latest), 0o644)

	fmt.Printf("Latest version:    %s\n", latest)

	if compareVersions(latest, version) <= 0 {
		fmt.Println("already up to date")
		return 0
	}

	if err := applyUpdate(root, latest); err != nil {
		fmt.Fprintf(os.Stderr, "update failed: %v\n", err)
		return 1
	}
	fmt.Println("updated to " + latest)
	return 0
}
