// Screen composition: tab bar, sidebar, article pane, status bar.
//
// Turns application state into a frame — the list of styled rows term.go
// paints — and, in the same pass, the hitboxes that make the chrome
// clickable. Building both together is what keeps the mouse honest: a tab is
// clickable at exactly the columns it was drawn at, with no second layout
// calculation to drift out of sync.
//
//	▌Interface   Setup   Agents   Skills   Subagents
//	────────────────────────────────────────────────────────────────
//	  The Terminal       │  Paths and the filesystem
//	▌ The Shell          │  ────────────────────────
//	▌1  What is a shell  │  Every file has an address…
//	 2  Paths            │
//	 3  Pipes            │
//	────────────────────────────────────────────────────────────────
//	 Interface 1/5 · The Shell 2/2 · Paths 2/4 · ←→ parts · ⇥ sections
package main

import (
	"math"
	"strconv"
	"strings"
)

const (
	minCols    = 60
	minRows    = 15
	chromeRows = 4 // tab bar, rule, rule, status bar
)

type tabBox struct {
	x0, x1, index int
}

type itemBox struct {
	y, index int
	kind     string // "article" | "section"
}

// Frame is a painted frame plus the hitboxes needed to interpret a click.
type Frame struct {
	rows  [][]span
	tabs  []tabBox
	items []itemBox

	paneX, paneY, paneW, paneH int
}

func (f *Frame) tabAt(x, y int) (int, bool) {
	if y != 0 {
		return 0, false
	}
	for _, b := range f.tabs {
		if b.x0 <= x && x < b.x1 {
			return b.index, true
		}
	}
	return 0, false
}

func (f *Frame) itemAt(x, y int) (string, int, bool) {
	if x >= f.paneX {
		return "", 0, false
	}
	for _, b := range f.items {
		if b.y == y {
			return b.kind, b.index, true
		}
	}
	return "", 0, false
}

func sidebarWidth(cols int) int { return min(28, max(18, cols/4)) }

// paneWidth leaves room for the sidebar, separator, two spaces of gutter and
// one column of scrollbar.
func paneWidth(cols int) int { return max(20, cols-sidebarWidth(cols)-5) }

func tooSmall(cols, rows int) bool { return cols < minCols || rows < minRows }

func smallFrame(cols, rows int) *Frame {
	message := "Please widen this window to at least " +
		strconv.Itoa(minCols) + "×" + strconv.Itoa(minRows) + "."
	out := make([][]span, rows)
	for i := range out {
		out[i] = []span{}
	}
	y := max(0, rows/2-1)
	if y < rows {
		text := clip([]span{{message, "warn"}}, cols)
		left := max(0, (cols-spansWidth(text))/2)
		out[y] = append([]span{{strings.Repeat(" ", left), "body"}}, text...)
	}
	if y+2 < rows {
		hint := clip([]span{{"Currently " + strconv.Itoa(cols) + "×" + strconv.Itoa(rows) + ".", "dim"}}, cols)
		left := max(0, (cols-spansWidth(hint))/2)
		out[y+2] = append([]span{{strings.Repeat(" ", left), "body"}}, hint...)
	}
	return &Frame{rows: out}
}

// --------------------------------------------------------------------------
// Chrome
// --------------------------------------------------------------------------

// sliceSpans returns the sub-span-list covering columns [a, b) of spans.
func sliceSpans(spans []span, a, b int) []span {
	out := []span{}
	x := 0
	for _, sp := range spans {
		w := dwidth(sp.text)
		if x+w <= a {
			x += w
			continue
		}
		if x >= b {
			break
		}
		var piece []rune
		for _, ch := range sp.text {
			if a <= x && x < b {
				piece = append(piece, ch)
			}
			x += charWidth(ch)
		}
		if len(piece) > 0 {
			out = append(out, span{string(piece), sp.style})
		}
	}
	return out
}

func tabBar(frame *Frame, parts []Part, active, cols int) []span {
	labels := []string{}
	for _, p := range parts {
		labels = append(labels, "  "+p.Title+"  ")
	}
	if len(labels) == 0 {
		labels = []string{"  (no content)  "}
	}

	spans := []span{}
	boxes := []tabBox{}
	x := 0
	for i, label := range labels {
		w := dwidth(label)
		style := "tab_idle"
		if i == active {
			style = "tab_active"
		}
		spans = append(spans, span{label, style})
		boxes = append(boxes, tabBox{x, x + w, i})
		x += w
	}
	total := x

	if total <= cols {
		frame.tabs = append(frame.tabs, boxes...)
		return padSpans(spans, cols, "body")
	}

	// Too many parts to show at once: scroll the strip, reserving a column at
	// each end for the « » affordances so it is obvious more exist.
	inner := cols - 2
	ax0, ax1 := 0, 0
	if active < len(boxes) {
		ax0, ax1 = boxes[active].x0, boxes[active].x1
	}
	start := max(0, min(ax1-inner, total-inner))
	if ax0 < start {
		start = ax0
	}
	row := append([]span{{"«", "tab_arrow"}}, sliceSpans(spans, start, start+inner)...)
	row = append(row, span{"»", "tab_arrow"})
	for _, b := range boxes {
		vx0, vx1 := max(1, b.x0-start+1), min(cols-1, b.x1-start+1)
		if vx1 > vx0 {
			frame.tabs = append(frame.tabs, tabBox{vx0, vx1, b.index})
		}
	}
	return padSpans(row, cols, "body")
}

func statusBar(app *App, cols int) []span {
	var left []span
	var right string

	if app.mode == "search" {
		left = []span{{"/", "status_key"}, {app.query, "status"}, {"▌", "status_key"}}
		plural := "es"
		if len(app.results) == 1 {
			plural = ""
		}
		right = strconv.Itoa(len(app.results)) + " match" + plural + " · enter open · esc cancel"
	} else {
		part, hasPart := app.part()
		article, hasArticle := app.article()
		pieces := []string{}
		if hasPart {
			pieces = append(pieces, part.Title+" "+strconv.Itoa(app.partI+1)+"/"+
				strconv.Itoa(len(app.index.Parts)))
		}
		if hasArticle {
			// Inside a section the article counts within it, matching the
			// numbers in the sidebar and the keys that jump to them.
			first, last := 0, len(part.Articles)
			if article.Section != "" {
				si, _ := sectionAt(part, app.articleI)
				sec := partSections(part)[si]
				first, last = sec.From, sec.To
				// No counter on the section: the sidebar already shows how
				// many there are, and the strip is the scarcest row we have.
				pieces = append(pieces, article.Section)
			}
			pieces = append(pieces, article.Title+" "+strconv.Itoa(app.articleI-first+1)+"/"+
				strconv.Itoa(last-first))
		}
		pieces = append(pieces, strconv.Itoa(app.scrollPercent())+"%")
		left = []span{{" " + strings.Join(pieces, " · "), "status"}}
		// Hints are dropped from the right as the window narrows, so the most
		// useful ones survive instead of the whole strip being cut mid-word.
		hints := []string{"←→ parts", "⇥ sections", "↑↓ scroll", "n next", "/ find", "? help", "q quit"}
		room := cols - spansWidth(left) - 3
		for len(hints) > 1 && dwidth(strings.Join(hints, " · ")) > room {
			hints = append(hints[:len(hints)-2], hints[len(hints)-1])
		}
		right = strings.Join(hints, " · ")
	}

	rightSpans := clip([]span{{right + " ", "status"}}, max(0, cols-spansWidth(left)-2))
	gap := cols - spansWidth(left) - spansWidth(rightSpans)
	row := append([]span{}, left...)
	row = append(row, span{strings.Repeat(" ", max(0, gap)), "status"})
	row = append(row, rightSpans...)
	return padSpans(row, cols, "status")
}

func statusBarHelp(cols int) []span {
	left := []span{
		{"  press ", "status"}, {"?", "status_key"}, {" or ", "status"},
		{"esc", "status_key"}, {" to close", "status"},
	}
	return padSpans(left, cols, "status")
}

type sidebarEntry struct {
	num, title, sub string
	kind            string // "article" | "section"
	index           int    // article index, or section index for a header
	open            bool   // set on the header of the expanded section
}

// sidebarEntries lays the left column out: every section's header followed by
// its articles, the whole part on show at once. Numbering restarts inside
// each section, matching the keys — `1`-`9` count within the section you are
// in, so a part of more than nine articles still has every page one keypress
// away. A part whose articles carry no `section:` is a single untitled
// section, so it draws as the plain numbered list it always was.
func sidebarEntries(app *App) ([]sidebarEntry, int) {
	entries := []sidebarEntry{}
	selected := 0

	if app.mode == "search" {
		for i, r := range app.results {
			entries = append(entries, sidebarEntry{
				strconv.Itoa(i + 1), r.article.Title, r.part.Title, "article", i, false,
			})
		}
		return entries, app.resultI
	}

	part, ok := app.part()
	if !ok {
		return entries, 0
	}
	openI, _ := sectionAt(part, app.articleI)
	for si, sec := range partSections(part) {
		if sec.Title != "" {
			entries = append(entries, sidebarEntry{"", sec.Title, "", "section", si, si == openI})
		}
		for ai := sec.From; ai < sec.To; ai++ {
			if ai == app.articleI {
				selected = len(entries)
			}
			entries = append(entries, sidebarEntry{
				strconv.Itoa(ai - sec.From + 1), part.Articles[ai].Title, "", "article", ai, false,
			})
		}
	}
	return entries, selected
}

// sidebarStart scrolls the column so the selected row is on screen. Without
// it the list is simply truncated at `height`, which at the minimum window
// size can cut off the article being read.
func sidebarStart(count, selected, height int) int {
	if count <= height || height <= 0 {
		return 0
	}
	start := min(max(0, selected-height/2), count-height)
	return min(start, selected)
}

func sidebarRows(frame *Frame, app *App, width, height, top int) [][]span {
	rows := [][]span{}
	entries, selected := sidebarEntries(app)
	start := sidebarStart(len(entries), selected, height)
	if start > 0 {
		entries = entries[start:]
		selected -= start
	}

	for i := 0; i < height; i++ {
		if i >= len(entries) {
			// Blank rows must still occupy their columns, or the separator and
			// everything right of it slides left below the last article.
			rows = append(rows, []span{{strings.Repeat(" ", width), "body"}})
			continue
		}
		e := entries[i]
		isSel := e.kind == "article" && i == selected
		// A section header is the side tab: styled like the tabs along the
		// top, marked when it is the one standing open.
		if e.kind == "section" {
			marker := span{" ", "body"}
			style := "tab_idle"
			if e.open {
				marker = span{"▌", "sel_bar"}
				style = "tab_active"
			}
			rows = append(rows, padSpans([]span{marker, {" ", "body"}, {e.title, style}}, width, "body"))
			frame.items = append(frame.items, itemBox{top + i, e.index, e.kind})
			continue
		}
		marker := span{" ", "body"}
		numStyle, textStyle := "row_num", "row"
		if isSel {
			marker = span{"▌", "sel_bar"}
			numStyle, textStyle = "sel_row", "sel_row"
		}
		num := e.num
		for len([]rune(num)) < 2 {
			num = " " + num
		}
		line := []span{marker, {num + "  ", numStyle}, {e.title, textStyle}}
		if e.sub != "" {
			subStyle := "dim"
			if isSel {
				subStyle = "sel_row"
			}
			line = append(line, span{"  " + e.sub, subStyle})
		}
		fill := "body"
		if isSel {
			fill = "sel_row"
		}
		rows = append(rows, padSpans(line, width, fill))
		frame.items = append(frame.items, itemBox{top + i, e.index, e.kind})
	}
	return rows
}

// scrollbar draws a one-column track, one (char, style) per body row.
func scrollbar(height, total, visible, scroll int) []span {
	if total <= visible || height <= 0 {
		out := make([]span, height)
		for i := range out {
			out[i] = span{" ", "body"}
		}
		return out
	}
	thumb := max(1, height*visible/total)
	spanLen := height - thumb
	reach := max(1, total-visible)
	// Python rounds half to even; match it so the thumb sits identically.
	start := int(math.RoundToEven(float64(spanLen) * float64(min(scroll, reach)) / float64(reach)))
	out := make([]span, height)
	for i := range out {
		if start <= i && i < start+thumb {
			out[i] = span{"█", "sep"}
		} else {
			out[i] = span{"│", "faint"}
		}
	}
	return out
}

// --------------------------------------------------------------------------
// Frame assembly
// --------------------------------------------------------------------------

// buildFrame composes the whole screen for the current application state.
func buildFrame(app *App, cols, rows int) *Frame {
	if tooSmall(cols, rows) {
		return smallFrame(cols, rows)
	}

	bodyH := rows - chromeRows
	frame := &Frame{}
	out := [][]span{}

	if app.mode == "help" {
		out = append(out, padSpans([]span{{"  Help", "tab_active"}}, cols, "body"))
		out = append(out, []span{{strings.Repeat("─", cols), "rule"}})
		lines := app.helpLines(cols - 4)
		frame.paneX, frame.paneY = 2, 2
		frame.paneW, frame.paneH = cols-4, bodyH
		for i := 0; i < bodyH; i++ {
			var line []span
			if idx := app.scroll + i; idx >= 0 && idx < len(lines) {
				line = lines[idx]
			}
			if len(line) > 0 {
				out = append(out, append([]span{{"  ", "body"}}, clip(line, cols-4)...))
			} else {
				out = append(out, []span{})
			}
		}
		out = append(out, []span{{strings.Repeat("─", cols), "rule"}})
		out = append(out, statusBarHelp(cols))
		frame.rows = out
		return frame
	}

	sw := sidebarWidth(cols)
	pw := paneWidth(cols)

	out = append(out, tabBar(frame, app.index.Parts, app.partI, cols))
	out = append(out, []span{{strings.Repeat("─", cols), "rule"}})

	side := sidebarRows(frame, app, sw, bodyH, len(out))
	lines := app.paneLines(pw)
	bar := scrollbar(bodyH, len(lines), bodyH, app.scroll)

	frame.paneX = sw + 3
	frame.paneY = len(out)
	frame.paneW = pw
	frame.paneH = bodyH

	for i := 0; i < bodyH; i++ {
		var line []span
		if idx := app.scroll + i; idx >= 0 && idx < len(lines) {
			line = lines[idx]
		}
		row := append([]span{}, side[i]...)
		row = append(row, span{"│", "sep"}, span{"  ", "body"})
		row = append(row, padSpans(clip(line, pw), pw, "body")...)
		row = append(row, span{" ", "body"}, bar[i])
		out = append(out, row)
	}

	out = append(out, []span{{strings.Repeat("─", cols), "rule"}})
	out = append(out, statusBar(app, cols))
	frame.rows = out
	return frame
}

const helpDoc = `
# Getting around

Nothing here is destructive. Press any key and see what happens.

## Moving between parts

The names across the top are the **parts** of the course. Move between them
with the left and right arrows.

- ` + "`←`" + ` ` + "`→`" + ` — previous / next part
- ` + "`Tab`" + ` — next part
- click a name at the top to jump straight to it

## Moving between sections

Some parts are divided into **sections**, the headings down the left. Each
one numbers its own articles, and the numbers you press are the ones in the
section you are in.

- ` + "`⇥`" + ` — next section
- ` + "`⇧⇥`" + ` — previous section
- click a heading to open that section

## Moving between articles

The numbered list down the left is the **articles** in the current section.

- ` + "`1`" + ` … ` + "`9`" + ` — jump straight to that numbered article
- ` + "`n`" + ` ` + "`p`" + ` — next / previous article, carrying on into the next part
- click an article to open it

## Reading

- ` + "`↑`" + ` ` + "`↓`" + ` or ` + "`j`" + ` ` + "`k`" + ` — scroll a line
- ` + "`Space`" + ` ` + "`b`" + `, or ` + "`PgDn`" + ` ` + "`PgUp`" + ` — scroll a page
- ` + "`g`" + ` ` + "`G`" + ` — jump to the top or the bottom
- the mouse wheel scrolls too

## Finding something

Press ` + "`/`" + ` and start typing. Matches appear in the left margin as you type,
best first. ` + "`↑`" + ` and ` + "`↓`" + ` move through them, ` + "`Enter`" + ` opens one, ` + "`Esc`" + ` gives up.

## Leaving

` + "`q`" + ` quits. So does ` + "`Ctrl-C`" + `. Your terminal is put back exactly as it was.
`
