// Screen composition: tab bar, sidebar, article pane, status bar.
//
// Turns application state into a frame — the list of styled rows term.go
// paints — and, in the same pass, the hitboxes that make the chrome
// clickable. Building both together is what keeps the mouse honest: a tab is
// clickable at exactly the columns it was drawn at, with no second layout
// calculation to drift out of sync.
//
//	  Level 1     Level 2
//	────────────────────────────────────────────────────────────────
//	  This Wiki            │  Paths and the filesystem
//	  The CLI              │  ────────────────────────
//	▌   The Shell          │  Every file has an address…
//	▌  1  What is a shell  │
//	   2  Paths            │
//	     Zsh               │
//	  Software             │
//	────────────────────────────────────────────────────────────────
//	 The CLI 2/8 · The Shell · Paths 2/3 · ←→ levels · [] parts
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
	kind     string // "article" | "section" | "part"
}

// Frame is a painted frame plus the hitboxes needed to interpret a click.
type Frame struct {
	rows   [][]span
	tabs   []tabBox
	items  []itemBox
	images []placement

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

// sidebarWidth is two columns wider than it was before the column grew a
// second tier of heading, so an article title has exactly the room it had
// when parts were tabs: the extra indent is paid for by the sidebar, not by
// the titles. It is one column wider again for the read tick, bought on
// exactly the same principle — the column pays for the mark, not the title.
func sidebarWidth(cols int) int { return min(31, max(21, cols/4)) }

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

func tabBar(frame *Frame, levels []Level, active, cols int) []span {
	labels := []string{}
	for _, l := range levels {
		labels = append(labels, "  "+l.Title+"  ")
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
			// The part counts within its level, not within the whole course:
			// the level is what the tab bar is showing, so "3/8" answers the
			// question the reader can actually see being asked.
			first, total := 0, len(app.index.Parts)
			if lv, li, ok := app.levels(); ok {
				first, total = lv[li].From, lv[li].To-lv[li].From
			}
			pieces = append(pieces, part.Title+" "+strconv.Itoa(app.partI-first+1)+"/"+
				strconv.Itoa(total))
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
		// Position matters here: the drop loop below removes from
		// len(hints)-2, so entries earlier in the slice survive a narrower
		// window than the ones placed after them.
		hints := []string{"←→ levels", "[] parts", "⇥ sections", "↑↓ scroll", "n next", "m mark", "/ find", "? help", "q quit"}
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
	kind            string // "article" | "section" | "part"
	index           int    // part index on a part header, else an article index
	open            bool   // set on the header standing open
	read            bool   // article marked read; never set on a heading
	isNew           bool   // article introduced by the version just installed; never set on a heading
}

// isNewArticle applies the "N" rule once, for both call sites in
// sidebarEntries below that build an article entry: an article is new when
// it belongs to the release this binary IS (its own `version` field equals
// "v" + the version constant in main.go), the reader's installed marker
// differs from that release — an absent marker counts as differing, which is
// every reader who predates this feature — and it has not been read. Read
// wins outright by construction: a read article can never also satisfy
// this, so "N" and "✓" never contend for the same slot.
func isNewArticle(article Article, read bool, installed string) bool {
	return !read && article.Version == "v"+version && installed != version
}

// sidebarEntries lays the left column out. It carries two tiers of heading
// now that the tabs along the top are levels: every part in the level is
// listed, and the one standing open expands into its sections and all of
// their articles — the whole part on show at once, exactly as it was when a
// part was a tab.
//
// Numbering restarts inside each section, matching the keys — `1`-`9` count
// within the section you are in, so a part of more than nine articles still
// has every page one keypress away. A part whose articles carry no `section:`
// is a single untitled section, so it draws as the plain numbered list it
// always was; and a level holding a single part drops the part heading, which
// is what makes a corpus with no `level:` at all look exactly as it did
// before levels existed.
func sidebarEntries(app *App) ([]sidebarEntry, int) {
	entries := []sidebarEntry{}
	selected := 0

	if app.mode == "search" {
		for i, r := range app.results {
			read := app.read[r.article.ID]
			entries = append(entries, sidebarEntry{
				strconv.Itoa(i + 1), r.article.Title, r.part.Title, "article", i, false,
				read, isNewArticle(r.article, read, app.installed),
			})
		}
		return entries, app.resultI
	}

	lv, li, hasLevel := app.levels()
	from, to := app.partI, app.partI+1
	if hasLevel {
		from, to = lv[li].From, lv[li].To
	}
	for pi := from; pi < to; pi++ {
		if pi < 0 || pi >= len(app.index.Parts) {
			continue
		}
		part := app.index.Parts[pi]
		if to-from > 1 {
			entries = append(entries, sidebarEntry{
				"", part.Title, "", "part", pi, pi == app.partI, false, false,
			})
		}
		if pi != app.partI {
			continue
		}
		openI, _ := sectionAt(part, app.articleI)
		for si, sec := range partSections(part) {
			if sec.Title != "" {
				entries = append(entries, sidebarEntry{
					"", sec.Title, "", "section", sec.From, si == openI, false, false,
				})
			}
			for ai := sec.From; ai < sec.To; ai++ {
				if ai == app.articleI {
					selected = len(entries)
				}
				read := app.read[part.Articles[ai].ID]
				entries = append(entries, sidebarEntry{
					strconv.Itoa(ai - sec.From + 1), part.Articles[ai].Title, "", "article", ai, false,
					read, isNewArticle(part.Articles[ai], read, app.installed),
				})
			}
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
		// The two heading tiers are side tabs: styled like the tabs along the
		// top, marked when they are the ones standing open. Indentation is
		// what separates them — a part sits flush, its sections one step in,
		// and its articles one step further.
		if e.kind == "part" || e.kind == "section" {
			marker := span{" ", "body"}
			style := "tab_idle"
			if e.open {
				marker = span{"▌", "sel_bar"}
				style = "tab_active"
			}
			indent := " "
			if e.kind == "section" {
				indent = "   "
			}
			rows = append(rows, padSpans([]span{marker, {indent, "body"}, {e.title, style}}, width, "body"))
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
		// Search results are a flat list under no heading at all, so they keep
		// the left margin the headings would otherwise have earned.
		indent := "  "
		if app.mode == "search" {
			indent = ""
		}
		// The tick rides inside the number's own span rather than getting one
		// of its own, so a selected row still turns sel_row in one piece. An
		// unselected new-and-unread row gets a green N in a span of its own
		// instead — the one case that must draw in a colour numStyle does
		// not carry. A read row's tick already occupies the slot, so
		// isNewArticle can never be true there; "!isSel" is what is left to
		// check. Selected is special-cased rather than folded into that same
		// green span because breaking a selected row apart would let the
		// highlight stop short of the letter — so a selected new row gets
		// its N right inside the number's own span instead, sel_row like the
		// rest of the row, the same way a selected read row's tick already
		// does. Every other row keeps the exact single-span shape this code
		// has always emitted, byte for byte.
		var line []span
		if !isSel && !e.read && e.isNew {
			line = []span{
				marker,
				{indent + num + " ", numStyle},
				{"N", "row_new"},
				{" ", numStyle},
				{e.title, textStyle},
			}
		} else {
			mark := " "
			switch {
			case e.read:
				mark = "✓"
			case e.isNew:
				mark = "N"
			}
			line = []span{marker, {indent + num + " " + mark + " ", numStyle}, {e.title, textStyle}}
		}
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

	levels, activeLevel, _ := app.levels()
	out = append(out, tabBar(frame, levels, activeLevel, cols))
	out = append(out, []span{{strings.Repeat("─", cols), "rule"}})

	side := sidebarRows(frame, app, sw, bodyH, len(out))
	lines := app.paneLines(pw)

	frame.paneX = sw + 3
	frame.paneY = len(out)
	frame.paneW = pw
	frame.paneH = bodyH

	if app.images {
		frame.images = visibleImages(app, pw, bodyH, frame.paneX, frame.paneY)
	} else {
		// No pictures this session: strip the reserved blank rows so a
		// caption sits flush under the text before it rather than leaving a
		// stretch of blank lines where a picture would have gone. This is
		// the only place that branches on app.images — paneLines, its cache
		// and the scroll math never learn pictures exist at all.
		lines = dropImagePad(lines)
	}

	bar := scrollbar(bodyH, len(lines), bodyH, app.scroll)

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

// --------------------------------------------------------------------------
// Pictures
//
// The reference for the arithmetic below is /tmp/kdemo/main.go, a spike
// written to answer exactly this question: how does a picture placed in the
// kitty graphics protocol survive the reader's existing draw model — full
// redraw of every line, on every keypress, inside the alternate screen —
// without flicker, without ghosts, and with correct cropping when it is
// half scrolled off the pane.
// --------------------------------------------------------------------------

// dropImagePad strips the blank rows render.go reserved for a picture,
// identified the same way term.go's Draw recognises them: a row that is
// nothing but a single "imagepad"-styled span. Used only when app.images is
// false — see buildFrame above for why that is the one branch point.
func dropImagePad(lines [][]span) [][]span {
	out := make([][]span, 0, len(lines))
	for _, line := range lines {
		if len(line) == 1 && line[0].style == "imagepad" {
			continue
		}
		out = append(out, line)
	}
	return out
}

// visibleImages turns each picture in the current article into a placement,
// or drops it if none of the rows it reserved are on screen this frame.
// paneX/paneY are the pane's own top-left cell within this frame — the same
// values already computed as frame.paneX/frame.paneY just above the call.
func visibleImages(app *App, paneW, bodyH, paneX, paneY int) []placement {
	var out []placement
	visTop, visBot := app.scroll, app.scroll+bodyH

	for _, img := range app.paneImages(paneW) {
		// Intersect the picture's reserved row range with the pane's visible
		// window. An empty intersection means no part of it is on screen.
		if img.start >= visBot || img.start+img.rows <= visTop || img.rows <= 0 {
			continue
		}
		topCut, botCut := 0, 0
		if img.start < visTop {
			topCut = visTop - img.start
		}
		if img.start+img.rows > visBot {
			botCut = (img.start + img.rows) - visBot
		}
		showRows := img.rows - topCut - botCut
		if showRows <= 0 {
			continue
		}

		// Fit the picture inside the visible slice of its reserved box at
		// its own true aspect ratio, using the terminal's real cell pixel
		// size rather than the 1:2 the reservation assumed — a real font is
		// rarely exactly that shape, and filling the box edge to edge on
		// that assumption would distort the picture instead of just leaving
		// a slightly generous margin.
		cols, rows := fitBox(img.imgW, img.imgH, paneW, showRows, app.cellW, app.cellH)
		if cols <= 0 || rows <= 0 {
			continue
		}

		// The source pixel crop is proportional to the reservation's own row
		// count, not the fitted box's — topCut and showRows describe how much
		// of the RESERVED range scrolled off, and that same fraction of the
		// picture's own pixel height is what a half-scrolled picture must
		// lose, regardless of how large the fitted box ends up being.
		srcY := topCut * img.imgH / img.rows
		srcH := showRows * img.imgH / img.rows
		if srcH <= 0 {
			continue
		}

		out = append(out, placement{
			path: img.path,
			// +1 on both: frame.paneX/paneY and the row/scroll arithmetic
			// below are 0-based indices into this frame's own rows and
			// columns, but placement.row/col are 1-based absolute screen
			// cells, the coordinate kitty's own cursor-relative positioning
			// expects.
			row:  paneY + 1 + (img.start + topCut - app.scroll),
			col:  paneX + 1 + (paneW-cols)/2, // centred horizontally in the pane
			cols: cols, rows: rows,
			srcY: srcY, srcH: srcH,
		})
	}
	return out
}

// fitBox scales (imgW, imgH) to fit inside a boxCols x boxRows cell box,
// each cell cellW x cellH pixels, preserving the picture's own aspect ratio,
// and returns the result in cells. A zero cell size means the terminal never
// reported one (image.go's cellPixels), so the box is used as-is — the same
// 1:2 assumption the reservation itself was already sized with.
func fitBox(imgW, imgH, boxCols, boxRows, cellW, cellH int) (cols, rows int) {
	if imgW <= 0 || imgH <= 0 || boxCols <= 0 || boxRows <= 0 {
		return 0, 0
	}
	if cellW <= 0 || cellH <= 0 {
		return boxCols, boxRows
	}
	boxPxW, boxPxH := boxCols*cellW, boxRows*cellH
	// Compare imgW*boxPxH against imgH*boxPxW instead of dividing, so the
	// tighter dimension is found with integers only — the same reasoning
	// imageRows already uses to keep Go and Python rounding identically.
	if boxPxW*imgH <= boxPxH*imgW {
		// Width is the binding constraint.
		cols = boxCols
		rows = max(1, imgH*boxPxW/imgW/cellH)
	} else {
		rows = boxRows
		cols = max(1, imgW*boxPxH/imgH/cellW)
	}
	return min(cols, boxCols), min(rows, boxRows)
}

const helpDoc = `
# Getting around

Nothing here is destructive. Press any key and see what happens.

## The three sizes of thing

The course nests three deep. **Levels** are the two or three names across the
top. Each level holds **parts**, the headings down the left margin. Each part
holds **sections**, the headings indented under the part standing open. The
numbered list is the **articles** themselves.

## Moving between levels

- ` + "`←`" + ` ` + "`→`" + ` — previous / next level
- click a name at the top to jump straight to it

## Moving between parts

Every part in the level is listed down the left. Only the one you are in
opens up.

- ` + "`[`" + ` ` + "`]`" + ` — previous / next part
- click a part's name to open it

## Moving between sections

Each section numbers its own articles, and the numbers you press are the ones
in the section you are in. ` + "`⇥`" + ` walks the left column top to bottom, on into
the next part when it runs out of sections.

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

## Marking what you have read

Nothing is marked for you. ` + "`m`" + ` puts a tick beside the article you are on, and
` + "`m`" + ` again takes it off. The ticks sit in the left margin next to the numbers,
and they are remembered between sessions — quitting, reinstalling and
updating all leave them where they are.

## Finding something

Press ` + "`/`" + ` and start typing. Matches appear in the left margin as you type,
best first. ` + "`↑`" + ` and ` + "`↓`" + ` move through them, ` + "`Enter`" + ` opens one, ` + "`Esc`" + ` gives up.

## Leaving

` + "`q`" + ` quits. So does ` + "`Ctrl-C`" + `. Your terminal is put back exactly as it was.
`
