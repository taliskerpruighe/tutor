// Application state and the key map.
//
// Everything the reader can do lives here: where they are in the course, how
// far down the page they have scrolled, and what each key means in each of
// the three modes (reading, searching, help).
//
// The design rule throughout is that no key is destructive and no key is a
// dead end — `esc` always backs out, `q` always leaves, and an unknown key is
// silently ignored rather than beeping or bailing.
package main

import (
	"math"
	"time"
)

type position struct {
	partI, articleI, scroll int
}

type cacheKey struct {
	path  string
	width int
}

type App struct {
	root     string
	index    Index
	partI    int
	articleI int
	scroll   int
	mode     string // normal | search | help
	query    string
	results  []located
	resultI  int
	running  bool

	paneW, paneH int
	cache        map[cacheKey]paneRender
	helpCache    map[int][][]span
	returnTo     *position

	// read is the set of article ids marked read, and readPath is where it is
	// written back. An empty readPath means "hold this in memory and do not
	// persist" — which is what cmdFrame wants, for the determinism reason set
	// out there.
	read     map[string]bool
	readPath string

	// images is "pictures can be drawn this session" — probeImages's answer,
	// taken once at startup (main.go's cmdRun) and never rechecked. Default
	// false, so any path that constructs an App without setting it (cmdFrame,
	// notably) gets the safe, deterministic behaviour of no pictures.
	images bool

	// cellW, cellH are the terminal's real cell size in pixels (image.go's
	// cellPixels), taken once at the same time as images. buildFrame is pure
	// arithmetic with no terminal of its own — cmdFrame calls it against no
	// tty at all — so this is how it learns the real cell shape instead of
	// assuming the 1:2 the reservation itself was sized with. Zero means
	// "unknown", which fitBox treats as "trust the reservation as-is".
	cellW, cellH int
}

// paneRender is what paneLines caches: the rendered lines and, alongside
// them, where each picture referenced in the article sits within those
// lines. Caching the pair together — rather than lines alone — is what lets
// buildFrame ask for the image list on every keypress without re-parsing the
// article's markdown just to find it again.
type paneRender struct {
	lines  [][]span
	images []imageBlock
}

func NewApp(root string, index Index, query string) *App {
	app := &App{
		root: root, index: index, mode: "normal", running: true,
		paneW: 72, paneH: 20,
		cache:     map[cacheKey]paneRender{},
		helpCache: map[int][][]span{},
		read:      map[string]bool{},
	}
	if query != "" {
		app.mode = "search"
		app.returnTo = &position{app.partI, app.articleI, app.scroll}
		app.setQuery(query)
	}
	return app
}

// -- current position ------------------------------------------------------

func (a *App) part() (Part, bool) {
	if a.partI >= 0 && a.partI < len(a.index.Parts) {
		return a.index.Parts[a.partI], true
	}
	return Part{}, false
}

func (a *App) article() (Article, bool) {
	part, ok := a.part()
	if !ok {
		return Article{}, false
	}
	if a.articleI >= 0 && a.articleI < len(part.Articles) {
		return part.Articles[a.articleI], true
	}
	return Article{}, false
}

// -- rendering -------------------------------------------------------------

func (a *App) paneLines(width int) [][]span {
	return a.paneRenderAt(width).lines
}

// paneImages is paneLines' companion: the pictures found in whatever article
// paneLines(width) just rendered, keyed the same way. buildFrame calls this
// to place pictures on screen without re-parsing the article's markdown a
// second time on every keypress just to relocate them.
func (a *App) paneImages(width int) []imageBlock {
	return a.paneRenderAt(width).images
}

// paneRenderAt renders — or serves from cache — the current article at
// width, keeping its lines and its picture list together so paneLines and
// paneImages never cause the article to be parsed twice for one keypress.
func (a *App) paneRenderAt(width int) paneRender {
	a.paneW = width
	article, ok := a.article()
	if !ok {
		lines, imgs := renderWithImages(emptyDoc, width)
		return paneRender{lines, imgs}
	}
	key := cacheKey{article.Path, width}
	if pr, hit := a.cache[key]; hit {
		return pr
	}
	if len(a.cache) > 24 {
		a.cache = map[cacheKey]paneRender{}
	}
	lines, imgs := renderWithImages(readArticle(a.root, article), width)
	pr := paneRender{lines, imgs}
	a.cache[key] = pr
	return pr
}

func (a *App) helpLines(width int) [][]span {
	if lines, ok := a.helpCache[width]; ok {
		return lines
	}
	a.helpCache = map[int][][]span{width: render(helpDoc, width)}
	return a.helpCache[width]
}

func (a *App) currentLines() [][]span {
	if a.mode == "help" {
		return a.helpLines(max(20, a.paneW))
	}
	return a.paneLines(a.paneW)
}

func (a *App) maxScroll() int {
	return max(0, len(a.currentLines())-a.paneH)
}

func (a *App) scrollPercent() int {
	top := a.maxScroll()
	if top <= 0 {
		return 100
	}
	return min(100, int(math.RoundToEven(100*float64(a.scroll)/float64(top))))
}

// -- navigation ------------------------------------------------------------

func (a *App) clampScroll() {
	a.scroll = max(0, min(a.scroll, a.maxScroll()))
}

func (a *App) goTo(partI, articleI int) {
	if len(a.index.Parts) == 0 {
		return
	}
	a.partI = max(0, min(partI, len(a.index.Parts)-1))
	part, _ := a.part()
	a.articleI = max(0, min(articleI, max(0, len(part.Articles)-1)))
	a.scroll = 0
}

func (a *App) toggleRead() {
	article, ok := a.article()
	if !ok {
		return
	}
	if a.read[article.ID] {
		delete(a.read, article.ID)
	} else {
		a.read[article.ID] = true
	}
	if a.readPath != "" {
		// A failure here costs the mark at the next launch and nothing more,
		// so it must not interrupt reading. tutor doctor is where an
		// unwritable state directory is meant to surface.
		_ = saveMarks(a.readPath, a.read)
	}
}

// levels returns the index's levels and which one the cursor is in. Like
// sections, the open level is derived from where the cursor is rather than
// stored, so `n`, a search hit and a click all open the right tab without
// knowing levels exist.
func (a *App) levels() ([]Level, int, bool) {
	lv := indexLevels(a.index)
	if len(lv) == 0 {
		return nil, 0, false
	}
	li, found := levelAt(a.index, a.partI)
	return lv, li, found
}

// stepLevel moves to the neighbouring level's first article — what ← and →
// do now that the tabs along the top are levels rather than parts.
func (a *App) stepLevel(delta int) {
	lv, li, ok := a.levels()
	if !ok {
		return
	}
	target := max(0, min(li+delta, len(lv)-1))
	a.goTo(lv[target].From, 0)
}

// openLevel jumps to a level by index — what a click on a tab does.
func (a *App) openLevel(index int) {
	lv, _, ok := a.levels()
	if !ok || index < 0 || index >= len(lv) {
		return
	}
	a.goTo(lv[index].From, 0)
}

// stepPart moves one part, clamping at the level's edges: ← and → are the way
// out of a level, so `[` and `]` never carry the reader across a tab boundary
// by accident.
func (a *App) stepPart(delta int) {
	lv, li, ok := a.levels()
	if !ok {
		a.goTo(a.partI+delta, 0)
		return
	}
	a.goTo(max(lv[li].From, min(a.partI+delta, lv[li].To-1)), 0)
}

// sections returns the current part's sections, and where the cursor sits in
// them. The open section is derived from articleI rather than stored, so
// every existing way of moving — n, search, a click — opens the right one
// without knowing sections exist.
func (a *App) sections() ([]Section, int, bool) {
	part, ok := a.part()
	if !ok {
		return nil, 0, false
	}
	secs := partSections(part)
	if len(secs) == 0 {
		return nil, 0, false
	}
	si, found := sectionAt(part, a.articleI)
	return secs, si, found
}

// levelSections flattens every section of every part in the current level into
// one list, so ⇥ walks the left column top to bottom the way it looks — on
// into the next part's first section rather than stopping dead at a part
// boundary. It clamps at the level's edges, because ← and → are the way out.
func (a *App) levelSections() ([]position, int) {
	lv, li, ok := a.levels()
	if !ok {
		return nil, 0
	}
	out, here := []position{}, 0
	for pi := lv[li].From; pi < lv[li].To; pi++ {
		part := a.index.Parts[pi]
		for _, sec := range partSections(part) {
			if pi == a.partI && sec.contains(a.articleI) {
				here = len(out)
			}
			out = append(out, position{pi, sec.From, 0})
		}
	}
	return out, here
}

// stepSection moves to the neighbouring section's first article.
func (a *App) stepSection(delta int) {
	secs, here := a.levelSections()
	if len(secs) == 0 {
		return
	}
	target := secs[max(0, min(here+delta, len(secs)-1))]
	a.goTo(target.partI, target.articleI)
}

// stepArticle moves one article, carrying on into the neighbouring part at
// the ends. Linear reading is the whole point of a course, so `n` should never
// stop dead at a part boundary.
func (a *App) stepArticle(delta int) {
	flat := flatten(a.index)
	if len(flat) == 0 {
		return
	}
	here := 0
	for k, item := range flat {
		if item.partI == a.partI && item.articleI == a.articleI {
			here = k
			break
		}
	}
	target := max(0, min(here+delta, len(flat)-1))
	a.goTo(flat[target].partI, flat[target].articleI)
}

// -- search ----------------------------------------------------------------

func (a *App) setQuery(query string) {
	a.query = query
	a.results = searchIndex(a.root, a.index, query)
	a.resultI = 0
	a.previewResult()
}

// previewResult shows the highlighted match immediately, so search is a live
// preview rather than a commitment.
func (a *App) previewResult() {
	if len(a.results) == 0 {
		return
	}
	a.resultI = max(0, min(a.resultI, len(a.results)-1))
	r := a.results[a.resultI]
	a.partI, a.articleI, a.scroll = r.partI, r.articleI, 0
}

func (a *App) openResult() {
	if len(a.results) > 0 {
		a.previewResult()
	}
	a.mode = "normal"
	a.returnTo = nil
}

func (a *App) cancelSearch() {
	if a.returnTo != nil {
		a.partI, a.articleI, a.scroll = a.returnTo.partI, a.returnTo.articleI, a.returnTo.scroll
	}
	a.mode = "normal"
	a.query = ""
	a.results = nil
	a.returnTo = nil
}

func (a *App) reload() {
	a.index = loadIndex(a.root, true)
	a.cache = map[cacheKey]paneRender{}
	a.goTo(a.partI, a.articleI)
}

// -- events ----------------------------------------------------------------

func (a *App) handle(ev event, frame *Frame) bool {
	if ev.mouse {
		return a.handleMouse(ev, frame)
	}
	switch a.mode {
	case "search":
		return a.handleSearch(ev.key)
	case "help":
		return a.handleHelp(ev.key)
	}
	return a.handleNormal(ev.key)
}

func (a *App) page() int { return max(1, a.paneH-2) }

func (a *App) handleNormal(key string) bool {
	switch key {
	case "q", "ctrl-c", "quit":
		a.running = false
	case "?":
		a.mode = "help"
		a.returnTo = &position{a.partI, a.articleI, a.scroll}
		a.scroll = 0
	case "/":
		a.mode = "search"
		a.returnTo = &position{a.partI, a.articleI, a.scroll}
		a.setQuery("")
	case "left", "h":
		a.stepLevel(-1)
	case "right", "l":
		a.stepLevel(1)
	case "[":
		a.stepPart(-1)
	case "]":
		a.stepPart(1)
	case "shift-tab":
		a.stepSection(-1)
	case "tab":
		a.stepSection(1)
	case "n":
		a.stepArticle(1)
	case "p":
		a.stepArticle(-1)
	case "down", "j":
		a.scroll++
	case "up", "k":
		a.scroll--
	case " ", "pgdn", "ctrl-f":
		a.scroll += a.page()
	case "b", "pgup", "ctrl-b":
		a.scroll -= a.page()
	case "g", "home":
		a.scroll = 0
	case "G", "end":
		a.scroll = a.maxScroll()
	case "r":
		a.reload()
	case "m":
		a.toggleRead()
	default:
		// 1-9 count within the open section, so a part with more than nine
		// articles in it still has every page one keypress away.
		if len(key) == 1 && key[0] >= '1' && key[0] <= '9' {
			if part, ok := a.part(); ok {
				wanted := int(key[0] - '1')
				first, last := 0, len(part.Articles)
				if secs, si, hasSec := a.sections(); hasSec {
					first, last = secs[si].From, secs[si].To
				}
				if first+wanted < last {
					a.goTo(a.partI, first+wanted)
				}
			}
		}
	}
	a.clampScroll()
	return a.running
}

func (a *App) handleSearch(key string) bool {
	switch key {
	case "esc":
		a.cancelSearch()
	case "enter":
		a.openResult()
	case "backspace":
		r := []rune(a.query)
		if len(r) > 0 {
			a.setQuery(string(r[:len(r)-1]))
		} else {
			a.setQuery("")
		}
	case "down", "ctrl-n":
		a.resultI++
		a.previewResult()
	case "up", "ctrl-p":
		a.resultI--
		a.previewResult()
	case "ctrl-c":
		a.running = false
	default:
		if r := []rune(key); len(r) == 1 && r[0] >= ' ' {
			a.setQuery(a.query + key)
		}
	}
	a.clampScroll()
	return a.running
}

func (a *App) handleHelp(key string) bool {
	switch key {
	case "esc", "?", "q":
		a.mode = "normal"
		if a.returnTo != nil {
			a.partI, a.articleI, a.scroll = a.returnTo.partI, a.returnTo.articleI, a.returnTo.scroll
			a.returnTo = nil
		}
	case "ctrl-c":
		a.running = false
	case "down", "j":
		a.scroll++
	case "up", "k":
		a.scroll--
	case " ", "pgdn":
		a.scroll += a.page()
	case "b", "pgup":
		a.scroll -= a.page()
	case "g", "home":
		a.scroll = 0
	case "G", "end":
		a.scroll = a.maxScroll()
	}
	a.clampScroll()
	return a.running
}

func (a *App) handleMouse(ev event, frame *Frame) bool {
	switch ev.kind {
	case "wheel-up":
		a.scroll -= 3
	case "wheel-down":
		a.scroll += 3
	case "click":
		if tab, ok := frame.tabAt(ev.x, ev.y); ok {
			if a.mode == "search" {
				a.cancelSearch()
			}
			a.openLevel(tab)
		} else if kind, item, ok := frame.itemAt(ev.x, ev.y); ok {
			switch {
			case a.mode == "search":
				if item < len(a.results) {
					a.resultI = item
					a.openResult()
				}
			case kind == "part":
				// A part header carries the part's own index, so clicking a
				// collapsed one opens it at its first article.
				a.goTo(item, 0)
			default:
				// Section headers and articles both carry an article index
				// within the part standing open, so one branch serves both.
				a.goTo(a.partI, item)
			}
		}
	}
	a.clampScroll()
	return a.running
}

// -- main loop -------------------------------------------------------------

func (a *App) Run(t *Terminal) {
	for a.running {
		cols, rows := t.Size()
		a.paneW = paneWidth(cols)
		a.paneH = max(1, rows-chromeRows)
		a.clampScroll()
		frame := buildFrame(a, cols, rows)
		t.Draw(frame.rows, frame.images)

		ev, ok := t.ReadEvent(time.Duration(0))
		if !ok {
			continue // resize: fall through and repaint
		}
		a.handle(ev, frame)
	}
}

const emptyDoc = `
# Nothing here yet

This part has no articles in it.

Content lives in ` + "`content/`" + `, one folder per part and one markdown file per
article. Add a file there and press ` + "`r`" + ` to reload.
`
