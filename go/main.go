// Entry point for the tutor TUI.
//
//	tutor                 open the course
//	tutor <words>         open it with a search already running
//	tutor index           rebuild content/index.json
//	tutor doctor          check the install and report what is wrong
//	tutor render f.md 72  print one article as the reader would see it
//	tutor frame 80 24     print a whole screen, for the parity harness
//	tutor --version
//
// This is the shipped implementation. tui/*.py is the reference the parity
// harness diffs against; the two must agree byte for byte.
package main

import (
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"
)

const version = "0.2.0"

const usage = `tutor                 open the course
tutor <words>         open it with a search already running
tutor index           rebuild content/index.json
tutor doctor          check the install and report what is wrong
tutor render f.md 72  print one article as the reader would see it
tutor frame 80 24     print a whole screen, for the parity harness
tutor --version`

// --------------------------------------------------------------------------
// Where the course lives
// --------------------------------------------------------------------------

func homeDir() string {
	if h, err := os.UserHomeDir(); err == nil {
		return h
	}
	return os.Getenv("HOME")
}

func pointerFile() string {
	return filepath.Join(homeDir(), ".local", "share", "tutor", "home")
}

// resolveRoot finds the tutor folder.
//
// The installed launcher is a *copy* of the binary in ~/.local/bin, deliberately
// severed from the tree it came from (that is what strips the quarantine
// attribute), so it cannot simply look next to itself. The pointer file
// install.sh writes is what reconnects the two.
func resolveRoot() string {
	candidates := []string{}

	if env := os.Getenv("TUTOR_HOME"); env != "" {
		candidates = append(candidates, env)
	}
	// Next to the executable, so running it straight out of the unpacked
	// folder works before anything has been installed.
	if exe, err := os.Executable(); err == nil {
		if resolved, err := filepath.EvalSymlinks(exe); err == nil {
			exe = resolved
		}
		candidates = append(candidates, filepath.Dir(filepath.Dir(exe)))
	}
	remembered := ""
	if data, err := os.ReadFile(pointerFile()); err == nil {
		remembered = strings.TrimSpace(string(data))
		if remembered != "" {
			candidates = append(candidates, remembered)
		}
	}
	candidates = append(candidates, filepath.Join(homeDir(), "tutor"))

	for _, c := range candidates {
		if info, err := os.Stat(filepath.Join(c, "content")); err == nil && info.IsDir() {
			return c
		}
	}
	// Nothing found. Name the path install.sh remembered rather than whichever
	// candidate happened to be first, so the error tells her where to look.
	if remembered != "" {
		return remembered
	}
	if len(candidates) > 0 {
		return candidates[0]
	}
	return "."
}

func isTTY(f *os.File) bool {
	info, err := f.Stat()
	return err == nil && info.Mode()&os.ModeCharDevice != 0
}

// --------------------------------------------------------------------------
// Subcommands
// --------------------------------------------------------------------------

func cmdIndex(root string) int {
	index, err := writeIndex(root)
	if err != nil {
		fmt.Fprintf(os.Stderr, "could not write the index: %v\n", err)
		return 1
	}
	total := 0
	for _, p := range index.Parts {
		total += len(p.Articles)
	}
	rel, err := filepath.Rel(root, indexPath(root))
	if err != nil {
		rel = indexPath(root)
	}
	fmt.Printf("Indexed %d article%s across %d part%s -> %s\n",
		total, plural(total), len(index.Parts), plural(len(index.Parts)), rel)
	for _, p := range index.Parts {
		fmt.Printf("  %-24s %d\n", p.Title, len(p.Articles))
	}
	return 0
}

func plural(n int) string {
	if n == 1 {
		return ""
	}
	return "s"
}

func cmdDoctor(root string) int {
	type check struct {
		ok        bool
		good, bad string
	}
	checks := []check{}

	checks = append(checks, check{true,
		fmt.Sprintf("tutor %s (%s/%s)", version, runtime.GOOS, runtime.GOARCH), ""})

	dir := contentDir(root)
	info, err := os.Stat(dir)
	okContent := err == nil && info.IsDir()
	checks = append(checks, check{okContent,
		"content/ found at " + dir,
		"no content/ directory — is TUTOR_HOME right?"})

	index := Index{}
	if okContent {
		index = loadIndex(root, true)
	}
	total := 0
	for _, p := range index.Parts {
		total += len(p.Articles)
	}
	checks = append(checks, check{total > 0,
		fmt.Sprintf("%d article%s in %d part%s", total, plural(total),
			len(index.Parts), plural(len(index.Parts))),
		"no articles found under content/"})

	_, err = os.Stat(indexPath(root))
	checks = append(checks, check{err == nil,
		"content/index.json present", "index missing — run: tutor index"})

	launcher := filepath.Join(homeDir(), ".local", "bin", "tutor")
	li, err := os.Stat(launcher)
	okLauncher := err == nil && !li.IsDir()
	checks = append(checks, check{okLauncher,
		"launcher at " + launcher,
		"not installed — run: bash " + filepath.Join(root, "install.sh")})

	binDir := filepath.Dir(launcher)
	okPath := false
	for _, p := range filepath.SplitList(os.Getenv("PATH")) {
		if p == "" {
			continue
		}
		if abs, err := filepath.Abs(p); err == nil && abs == binDir {
			okPath = true
			break
		}
	}
	checks = append(checks, check{okPath,
		binDir + " is on PATH",
		binDir + " is not on PATH — open a new terminal, or run: bash " +
			filepath.Join(root, "install.sh")})

	failures := 0
	for _, c := range checks {
		if c.ok {
			fmt.Printf("  ok    %s\n", c.good)
		} else {
			failures++
			fmt.Printf("  FAIL  %s\n", c.bad)
		}
	}

	// Not a check. An agent runs doctor from a tool call, where there is no tty
	// by definition; counting that as a failure would send it chasing a problem
	// that does not exist.
	if !(isTTY(os.Stdin) && isTTY(os.Stdout)) {
		fmt.Println("  note  no terminal attached here — run `tutor` in a terminal of its own")
	}

	fmt.Println()
	if failures > 0 {
		fmt.Printf("%d check%s failed.\n", failures, plural(failures))
		return 1
	}
	fmt.Println("All good. Run `tutor` to start.")
	return 0
}

// cmdRender mirrors `python3 -m tui.render <file> [width]` so the two
// implementations can be diffed byte for byte.
func cmdRender(args []string) int {
	if len(args) == 0 {
		fmt.Fprintln(os.Stderr, "usage: tutor render <file.md> [width]")
		return 1
	}
	cols := 72
	if len(args) > 1 {
		if n, err := strconv.Atoi(args[1]); err == nil {
			cols = n
		}
	}
	data, err := os.ReadFile(args[0])
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		return 1
	}
	var out strings.Builder
	for _, row := range render(string(data), cols) {
		for _, sp := range row {
			if esc := sgr(sp.style); esc != "" {
				out.WriteString(esc + sp.text + reset)
			} else {
				out.WriteString(sp.text)
			}
		}
		out.WriteString("\n")
	}
	os.Stdout.WriteString(out.String())
	return 0
}

// cmdFrame mirrors `python3 -m tui.frame <cols> <rows> [id] [mode] [query]`.
// Article renders are only half the screen; this dumps the whole composed
// frame — tab bar, sidebar, status line — so the parity harness can diff the
// chrome too, which is otherwise verified by nothing.
func cmdFrame(root string, args []string) int {
	if len(args) < 2 {
		fmt.Fprintln(os.Stderr, "usage: tutor frame <cols> <rows> [article-id] [mode] [query]")
		return 1
	}
	cols, err1 := strconv.Atoi(args[0])
	rows, err2 := strconv.Atoi(args[1])
	if err1 != nil || err2 != nil {
		fmt.Fprintln(os.Stderr, "cols and rows must be numbers")
		return 1
	}
	id, mode, query := "", "normal", ""
	if len(args) > 2 {
		id = args[2]
	}
	if len(args) > 3 {
		mode = args[3]
	}
	if len(args) > 4 {
		query = strings.Join(args[4:], " ")
	}

	app := NewApp(root, loadIndex(root, false), "")
	if id != "" {
		for _, item := range flatten(app.index) {
			if item.article.ID == id {
				app.goTo(item.partI, item.articleI)
				break
			}
		}
	}
	app.paneW, app.paneH = paneWidth(cols), max(1, rows-chromeRows)
	switch mode {
	case "help":
		app.mode = "help"
	case "search":
		app.mode = "search"
		app.setQuery(query)
	}

	var out strings.Builder
	for _, row := range buildFrame(app, cols, rows).rows {
		for _, sp := range row {
			if esc := sgr(sp.style); esc != "" {
				out.WriteString(esc + sp.text + reset)
			} else {
				out.WriteString(sp.text)
			}
		}
		out.WriteString("\n")
	}
	os.Stdout.WriteString(out.String())
	return 0
}

func cmdRun(root, query string) int {
	if !(isTTY(os.Stdin) && isTTY(os.Stdout)) {
		// Claude Code owns its own terminal, so an agent calling this from a
		// tool would otherwise hang forever waiting on a keypress. Say what to
		// do instead of failing silently.
		fmt.Fprint(os.Stderr,
			"tutor needs a terminal of its own.\n\n"+
				"Open a new terminal window or tab and run:\n\n"+
				"    tutor\n\n")
		return 1
	}
	if info, err := os.Stat(contentDir(root)); err != nil || !info.IsDir() {
		fmt.Fprintf(os.Stderr,
			"The tutor folder has moved or been deleted:\n    %s\n"+
				"Put it back, or re-run install.sh from wherever it now lives.\n", root)
		return 1
	}

	index := loadIndex(root, true)
	t := NewTerminal(true)
	if err := t.Start(); err != nil {
		fmt.Fprintf(os.Stderr, "could not take over the terminal: %v\n", err)
		return 1
	}
	defer func() {
		// A panic must never leave her shell in raw mode.
		if r := recover(); r != nil {
			t.Restore()
			fmt.Fprintln(os.Stderr, r)
			os.Exit(1)
		}
		t.Restore()
	}()
	NewApp(root, index, query).Run(t)
	return 0
}

// --------------------------------------------------------------------------

func main() {
	os.Exit(run(os.Args[1:]))
}

func run(argv []string) int {
	root := resolveRoot()

	if len(argv) > 0 {
		switch argv[0] {
		case "-h", "--help", "help":
			fmt.Println(usage)
			return 0
		case "-V", "--version", "version":
			fmt.Println("tutor " + version)
			return 0
		case "index":
			return cmdIndex(root)
		case "doctor":
			return cmdDoctor(root)
		case "render":
			return cmdRender(argv[1:])
		case "frame":
			return cmdFrame(root, argv[1:])
		case "run":
			argv = argv[1:]
		}
	}

	return cmdRun(root, strings.Join(argv, " "))
}
