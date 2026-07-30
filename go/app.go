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
	cache        map[cacheKey][][]span
	helpCache    map[int][][]span
	returnTo     *position
}

func NewApp(root string, index Index, query string) *App {
	app := &App{
		root: root, index: index, mode: "normal", running: true,
		paneW: 72, paneH: 20,
		cache:     map[cacheKey][][]span{},
		helpCache: map[int][][]span{},
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
	a.paneW = width
	article, ok := a.article()
	if !ok {
		return render(emptyDoc, width)
	}
	key := cacheKey{article.Path, width}
	if lines, hit := a.cache[key]; hit {
		return lines
	}
	if len(a.cache) > 24 {
		a.cache = map[cacheKey][][]span{}
	}
	lines := render(readArticle(a.root, article), width)
	a.cache[key] = lines
	return lines
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

func (a *App) stepPart(delta int) { a.goTo(a.partI+delta, 0) }

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

// stepSection moves to the neighbouring section's first article. It clamps at
// the part's edges: ← and → are already the way out of a part.
func (a *App) stepSection(delta int) {
	secs, si, ok := a.sections()
	if !ok {
		return
	}
	target := max(0, min(si+delta, len(secs)-1))
	a.goTo(a.partI, secs[target].From)
}

// openSection jumps to a section by index — what a click on its header does.
func (a *App) openSection(index int) {
	secs, _, ok := a.sections()
	if !ok || index < 0 || index >= len(secs) {
		return
	}
	a.goTo(a.partI, secs[index].From)
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
	a.cache = map[cacheKey][][]span{}
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
		a.stepPart(-1)
	case "right", "l":
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
			a.goTo(tab, 0)
		} else if kind, item, ok := frame.itemAt(ev.x, ev.y); ok {
			switch {
			case a.mode == "search":
				if item < len(a.results) {
					a.resultI = item
					a.openResult()
				}
			case kind == "section":
				a.openSection(item)
			default:
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
		t.Draw(frame.rows)

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
