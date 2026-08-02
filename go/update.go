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

const (
	// Tags in this repo are namespaced by the trunk they were cut on, so the
	// real ref is "tori/MkI_v0.2.0", not "MkI_v0.2.0". Drop the "tori/" and
	// every tarball fetch 404s.
	updateTagPrefix = "tori/MkI_v"
	versionURL      = "https://raw.githubusercontent.com/taliskerpruighe/tutor/tori/version.txt"
	tarballURLFmt   = "https://codeload.github.com/taliskerpruighe/tutor/tar.gz/refs/tags/%s"
	// A cached remote version is trusted for this long before the network is
	// asked again. Zero disables the cache entirely, so every launch checks.
	updateCacheTTL = 0
)

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

// fetchLatestVersion makes the actual network call for the remote version
// string. Callers decide how to handle failure: checkForUpdate swallows it,
// cmdUpdate reports it.
func fetchLatestVersion() (string, error) {
	client := &http.Client{Timeout: 2 * time.Second}
	resp, err := client.Get(versionURL)
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

// checkForUpdate answers "is a newer version available?" for the launch-time
// prompt. It now runs the network call on every launch — the cache file is
// still written below on every check, so it stays fresher than before rather
// than staler, but it is no longer trusted to answer this question; that
// makes cachedUpdateVersion's answer for `tutor doctor` current within one
// launch instead of within a day. Any failure at all — no network, timeout,
// non-200, garbage body, unwritable cache — is silent: it returns ("", false)
// and must never print anything or block startup.
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

	fetched, err := fetchLatestVersion()
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

// applyUpdate downloads the tarball for tag "tori/MkI_v<ver>", unpacks it next to
// root, sanity-checks the result, swaps it in, and delegates the actual
// binary install to install.sh (this function must never copy a binary
// itself — that is install.sh's job, and only it sheds the quarantine xattr
// and survives ETXTBSY correctly).
func applyUpdate(root string, ver string) error {
	tag := updateTagPrefix + ver
	url := fmt.Sprintf(tarballURLFmt, tag)

	client := &http.Client{Timeout: 5 * time.Minute}
	resp, err := client.Get(url)
	if err != nil {
		return fmt.Errorf("downloading %s: %w", tag, err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("downloading %s: unexpected status %s", tag, resp.Status)
	}

	gz, err := gzip.NewReader(resp.Body)
	if err != nil {
		return fmt.Errorf("opening tarball: %w", err)
	}
	defer gz.Close()

	parent := filepath.Dir(root)
	tmpdir, err := os.MkdirTemp(parent, "tutor-update-*")
	if err != nil {
		return fmt.Errorf("creating temp dir: %w", err)
	}
	swapped := false
	defer func() {
		if !swapped {
			os.RemoveAll(tmpdir)
		}
	}()

	absTmp, err := filepath.Abs(tmpdir)
	if err != nil {
		return err
	}

	tr := tar.NewReader(gz)
	for {
		hdr, err := tr.Next()
		if err == io.EOF {
			break
		}
		if err != nil {
			return fmt.Errorf("reading tarball: %w", err)
		}

		// Every entry is prefixed with one directory: GitHub flattens the tag's
		// slash, so tag "tori/MkI_v0.2.0" gives "tutor-tori-MkI_v0.2.0/".
		// Strip exactly one leading path component.
		parts := strings.SplitN(hdr.Name, "/", 2)
		if len(parts) < 2 || parts[1] == "" {
			continue
		}
		rel := parts[1]

		dest := filepath.Join(tmpdir, rel)
		absDest, err := filepath.Abs(dest)
		if err != nil {
			return err
		}
		if absDest != absTmp && !strings.HasPrefix(absDest, absTmp+string(os.PathSeparator)) {
			return fmt.Errorf("tar-slip: entry %q escapes the destination", hdr.Name)
		}

		switch hdr.Typeflag {
		case tar.TypeDir:
			if err := os.MkdirAll(dest, 0o755); err != nil {
				return err
			}
		case tar.TypeReg:
			if err := os.MkdirAll(filepath.Dir(dest), 0o755); err != nil {
				return err
			}
			mode := os.FileMode(hdr.Mode) & 0o777
			f, err := os.OpenFile(dest, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, mode)
			if err != nil {
				return err
			}
			_, err = io.Copy(f, tr)
			f.Close()
			if err != nil {
				return err
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
		return fmt.Errorf("update package looks incomplete: no content/ directory")
	}
	if info, err := os.Stat(filepath.Join(tmpdir, "tui", "bin")); err != nil || !info.IsDir() {
		return fmt.Errorf("update package looks incomplete: no tui/bin directory")
	}

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

	latest, err := fetchLatestVersion()
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
