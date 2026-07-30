// Markdown renderer for the tutor TUI.
//
// Turns markdown into `lines` — a list of rows, each row a list of
// (text, style) spans that term.go knows how to paint.
//
// This is deliberately *not* a general markdown implementation. The course
// content is authored alongside it, so the supported subset is a contract we
// control rather than a guess about arbitrary input:
//
//	headings (#..####)   paragraphs with reflow   fenced code blocks
//	inline `code`        **bold**   *italic*      bullet + ordered lists
//	> blockquotes        --- rules  [links](url)  | pipe | tables |
//	![alt](pic.png)      pictures — PNG only, and only where the terminal
//	                     can actually show them
//
// Anything unrecognised degrades to a plain wrapped paragraph, so unexpected
// syntax is always readable even when it is not pretty.
//
// A line-for-line port of tui/render.py, which remains the reference
// implementation the parity harness diffs against. Where a choice existed
// between idiomatic Go and matching Python's output byte for byte, matching
// won.
package main

import (
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
	"unicode"
)

type span struct {
	text  string
	style string
}

// --------------------------------------------------------------------------
// Width helpers
//
// Shared with layout.go. Terminals measure columns, not characters: combining
// marks occupy none and CJK occupies two. The tables come from Python's
// unicodedata via bin/gen-width.py, so both implementations agree exactly.
// --------------------------------------------------------------------------

func charWidth(r rune) int {
	if inRanges(r, zeroWidth) {
		return 0
	}
	if r < 32 || r == 127 {
		return 0
	}
	if inRanges(r, wideWidth) {
		return 2
	}
	return 1
}

// dwidth is the display width of s in terminal columns.
func dwidth(s string) int {
	w := 0
	for _, r := range s {
		w += charWidth(r)
	}
	return w
}

// clip truncates a span list to width columns, preserving styles.
func clip(spans []span, width int) []span {
	out := []span{}
	used := 0
	for _, sp := range spans {
		if used >= width {
			break
		}
		w := dwidth(sp.text)
		if used+w <= width {
			out = append(out, sp)
			used += w
			continue
		}
		var cut []rune
		for _, ch := range sp.text {
			cw := charWidth(ch)
			if used+cw > width {
				break
			}
			cut = append(cut, ch)
			used += cw
		}
		if len(cut) > 0 {
			out = append(out, span{string(cut), sp.style})
		}
		break
	}
	return out
}

// padSpans extends a span list to exactly width columns.
func padSpans(spans []span, width int, style string) []span {
	spans = clip(spans, width)
	used := 0
	for _, sp := range spans {
		used += dwidth(sp.text)
	}
	if used < width {
		spans = append(spans, span{strings.Repeat(" ", width-used), style})
	}
	return spans
}

func spansWidth(spans []span) int {
	w := 0
	for _, sp := range spans {
		w += dwidth(sp.text)
	}
	return w
}

// mergeSpans collapses adjacent spans sharing a style. Purely a size
// optimisation, but the Python side does it too, so parity requires it.
func mergeSpans(spans []span) []span {
	out := []span{}
	for _, sp := range spans {
		if sp.text == "" {
			continue
		}
		if n := len(out); n > 0 && out[n-1].style == sp.style {
			out[n-1].text += sp.text
			continue
		}
		out = append(out, sp)
	}
	return out
}

// --------------------------------------------------------------------------
// Inline parsing
//
// Python uses one alternation regex with backreferences for the paired
// markers. RE2 has no backreferences, so the scanner below is hand-written —
// but it reproduces the regex's semantics exactly, including the ordering of
// the alternatives and the greedy-then-backtracking backtick run.
// --------------------------------------------------------------------------

type inlineMatch struct {
	kind   string // esc | code | link | strong | em
	start  int
	end    int
	a      string // escaped char, code text, link text, emphasised text
	b      string // link url
	marker string // the emphasis marker actually used
}

func isSpaceRune(r rune) bool { return unicode.IsSpace(r) }

// findInline finds the next inline construct at or after pos, trying the
// alternatives in the same order Python's alternation does.
func findInline(r []rune, pos int) (inlineMatch, bool) {
	n := len(r)
	for i := pos; i < n; i++ {
		// 1. \X — a backslash escape.
		if r[i] == '\\' && i+1 < n {
			return inlineMatch{kind: "esc", start: i, end: i + 2, a: string(r[i+1])}, true
		}

		// 2. `code` — the opening run is greedy, then backtracks.
		if r[i] == '`' {
			run := 0
			for i+run < n && r[i+run] == '`' {
				run++
			}
			for k := run; k >= 1; k-- {
				// codetext is `.+?`, so it needs at least one rune.
				for j := i + k + 1; j+k <= n; j++ {
					if runOf(r, j, k, '`') {
						return inlineMatch{
							kind: "code", start: i, end: j + k,
							a: string(r[i+k : j]),
						}, true
					}
				}
			}
		}

		// 3. [text](url)
		if r[i] == '[' {
			j := i + 1
			for j < n && r[j] != ']' {
				j++
			}
			if j < n && j+1 < n && r[j+1] == '(' {
				k := j + 2
				for k < n && r[k] != ')' && !isSpaceRune(r[k]) {
					k++
				}
				if k < n && r[k] == ')' {
					return inlineMatch{
						kind: "link", start: i, end: k + 1,
						a: string(r[i+1 : j]), b: string(r[j+2 : k]),
					}, true
				}
			}
		}

		// 4. **strong** or __strong__
		if i+1 < n && (r[i] == '*' || r[i] == '_') && r[i+1] == r[i] {
			marker := string([]rune{r[i], r[i]})
			// \S consumes one non-space rune, then `.*?` is minimal.
			if i+2 < n && !isSpaceRune(r[i+2]) {
				for j := i + 3; j+2 <= n; j++ {
					if r[j] == r[i] && r[j+1] == r[i] {
						return inlineMatch{
							kind: "strong", start: i, end: j + 2,
							a: string(r[i+2 : j]), marker: marker,
						}, true
					}
				}
			}
		}

		// 5. *em* or _em_
		if r[i] == '*' || r[i] == '_' {
			if i+1 < n && !isSpaceRune(r[i+1]) {
				for j := i + 2; j < n; j++ {
					if r[j] == r[i] {
						return inlineMatch{
							kind: "em", start: i, end: j + 1,
							a: string(r[i+1 : j]), marker: string(r[i]),
						}, true
					}
				}
			}
		}
	}
	return inlineMatch{}, false
}

func runOf(r []rune, at, count int, ch rune) bool {
	if at+count > len(r) {
		return false
	}
	for i := 0; i < count; i++ {
		if r[at+i] != ch {
			return false
		}
	}
	return true
}

var combineTable = map[[2]string]string{
	{"body", "strong"}:   "bold",
	{"body", "em"}:       "italic",
	{"bold", "em"}:       "bolditalic",
	{"italic", "strong"}: "bolditalic",
	{"dim", "strong"}:    "bold",
	{"quote", "strong"}:  "bold",
	{"quote", "em"}:      "quote",
}

func combineStyle(base, kind string) string {
	// Headings and links are already emphatic; nesting inside them is a no-op
	// rather than a colour change that would fight the surrounding style.
	if strings.HasPrefix(base, "h") || base == "link" || base == "tablehead" {
		return base
	}
	if s, ok := combineTable[[2]string{base, kind}]; ok {
		return s
	}
	if kind == "em" {
		return base
	}
	return "bold"
}

func shortenURL(url string) string {
	for _, prefix := range []string{"https://", "http://"} {
		if strings.HasPrefix(url, prefix) {
			url = url[len(prefix):]
		}
	}
	return strings.TrimRight(url, "/")
}

func isAlnum(r rune) bool { return unicode.IsLetter(r) || unicode.IsNumber(r) }

// parseInline parses inline markup into spans, recursing through nested
// emphasis.
func parseInline(text, base string) []span {
	r := []rune(text)
	spans := []span{}
	var buf []rune

	flush := func() {
		if len(buf) > 0 {
			spans = append(spans, span{string(buf), base})
			buf = buf[:0]
		}
	}

	pos := 0
	for pos < len(r) {
		m, ok := findInline(r, pos)
		if !ok {
			buf = append(buf, r[pos:]...)
			break
		}
		if m.start > pos {
			buf = append(buf, r[pos:m.start]...)
		}

		switch m.kind {
		case "esc":
			buf = append(buf, []rune(m.a)...)
		case "code":
			flush()
			inner := m.a
			// One padding space each side, per CommonMark, so `` ` `` works.
			if strings.HasPrefix(inner, " ") && strings.HasSuffix(inner, " ") &&
				strings.TrimSpace(inner) != "" {
				inner = inner[1 : len(inner)-1]
			}
			spans = append(spans, span{inner, "code"})
		case "link":
			flush()
			spans = append(spans, parseInline(m.a, "link")...)
			url := shortenURL(m.b)
			if url != "" && url != m.a {
				spans = append(spans, span{" (" + url + ")", "linkurl"})
			}
		case "strong":
			flush()
			spans = append(spans, parseInline(m.a, combineStyle(base, "strong"))...)
		case "em":
			before := ' '
			if m.start > 0 {
				before = r[m.start-1]
			}
			after := ' '
			if m.end < len(r) {
				after = r[m.end]
			}
			// `snake_case` and `a_b_c` are identifiers, not emphasis. Require
			// underscore emphasis to sit on a word boundary; `*` is
			// unambiguous.
			if m.marker == "_" && (isAlnum(before) || isAlnum(after)) {
				buf = append(buf, []rune(m.marker)...)
				pos = m.start + 1
				continue
			}
			flush()
			spans = append(spans, parseInline(m.a, combineStyle(base, "em"))...)
		}

		pos = m.end
	}

	flush()
	return mergeSpans(spans)
}

// --------------------------------------------------------------------------
// Wrapping
// --------------------------------------------------------------------------

type atom struct {
	word  string // "" marks a break opportunity
	style string
	brk   bool
}

// atoms splits spans into word atoms, dropping the whitespace between them.
func atomize(spans []span) []atom {
	out := []atom{}
	for _, sp := range spans {
		r := []rune(sp.text)
		i := 0
		for i < len(r) {
			j := i
			sp0 := isSpaceRune(r[i])
			for j < len(r) && isSpaceRune(r[j]) == sp0 {
				j++
			}
			if sp0 {
				out = append(out, atom{style: sp.style, brk: true})
			} else {
				out = append(out, atom{word: string(r[i:j]), style: sp.style})
			}
			i = j
		}
	}
	return out
}

// hardSplit breaks a word too long for the pane into width-sized chunks.
func hardSplit(word, style string, width int) []span {
	chunks := []span{}
	cur := ""
	cw := 0
	for _, ch := range word {
		w := charWidth(ch)
		if cw+w > width && cur != "" {
			chunks = append(chunks, span{cur, style})
			cur, cw = "", 0
		}
		cur += string(ch)
		cw += w
	}
	if cur != "" {
		chunks = append(chunks, span{cur, style})
	}
	return chunks
}

// wrapSpans reflows spans to width, with optional per-line prefixes.
//
// firstPrefix/restPrefix are span lists themselves, which is what makes
// hanging indents (list bullets, quote bars) fall out for free.
func wrapSpans(spans []span, width int, firstPrefix, restPrefix []span) [][]span {
	if restPrefix == nil {
		restPrefix = firstPrefix
	}
	atoms := atomize(spans)
	if len(atoms) == 0 {
		if len(firstPrefix) > 0 {
			return [][]span{append([]span{}, firstPrefix...)}
		}
		return [][]span{{}}
	}

	lines := [][]span{}
	prefix := firstPrefix
	avail := max(1, width-spansWidth(prefix))
	cur := []span{}
	curW := 0
	pendingSpace := false

	for _, a := range atoms {
		if a.brk {
			if len(cur) > 0 {
				pendingSpace = true
			}
			continue
		}

		pieces := []span{{a.word, a.style}}
		if dwidth(a.word) > avail {
			pieces = hardSplit(a.word, a.style, avail)
		}

		for _, piece := range pieces {
			pw := dwidth(piece.text)
			need := pw
			if pendingSpace && len(cur) > 0 {
				need++
			}
			if len(cur) > 0 && curW+need > avail {
				lines = append(lines, append(append([]span{}, prefix...), cur...))
				prefix = restPrefix
				avail = max(1, width-spansWidth(prefix))
				cur, curW, pendingSpace = []span{}, 0, false
			}
			if pendingSpace && len(cur) > 0 {
				// The separating space inherits a style only when both sides
				// share one, so `cd ~` keeps an unbroken code background while
				// "the [link]" does not drag the underline onto the space.
				gap := "body"
				if cur[len(cur)-1].style == piece.style {
					gap = piece.style
				}
				cur = append(cur, span{" ", gap})
				curW++
			}
			pendingSpace = false
			cur = append(cur, piece)
			curW += pw
		}
	}

	if len(cur) > 0 {
		lines = append(lines, append(append([]span{}, prefix...), cur...))
	}
	out := make([][]span, len(lines))
	for i, line := range lines {
		out[i] = mergeSpans(line)
	}
	return out
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

// --------------------------------------------------------------------------
// Block parsing
// --------------------------------------------------------------------------

var (
	fenceRe       = regexp.MustCompile("^(\\s*)(`{3,}|~{3,})\\s*([A-Za-z0-9_+-]*)\\s*$")
	headingRe     = regexp.MustCompile(`^(#{1,6})\s+(.*?)\s*#*\s*$`)
	ruleRe        = regexp.MustCompile(`^\s*(?:-{3,}|\*{3,}|_{3,})\s*$`)
	bulletRe      = regexp.MustCompile(`^(\s*)([-*+])\s+(.*)$`)
	orderedRe     = regexp.MustCompile(`^(\s*)(\d+)[.)]\s+(.*)$`)
	quoteRe       = regexp.MustCompile(`^\s*>\s?(.*)$`)
	frontmatterRe = regexp.MustCompile(`(?s)\A---\r?\n.*?\r?\n---\r?\n`)
	tableSepRe    = regexp.MustCompile(`^\|?[\s:|-]+\|[\s:|-]*$`)
	imageRe       = regexp.MustCompile(`^\s*!\[([^\]]*)\]\(([^)\s]*)\)\s*$`)
)

// Every glyph the renderer draws has to exist in Menlo and SF Mono, or macOS
// substitutes a font and may give it double width — which would shift every
// column to its right. These three are safe; exotica is not worth the risk.
var bullets = [3]string{"•", "◦", "-"}

func stripFrontmatter(text string) string {
	if loc := frontmatterRe.FindStringIndex(text); loc != nil && loc[0] == 0 {
		return text[loc[1]:]
	}
	return text
}

func isTableSep(line string) bool {
	line = strings.TrimSpace(line)
	if line == "" || !strings.Contains(line, "-") {
		return false
	}
	if !tableSepRe.MatchString(line) {
		return false
	}
	for _, r := range line {
		if !strings.ContainsRune("|-: \t", r) {
			return false
		}
	}
	return true
}

func splitRow(line string) []string {
	line = strings.TrimSpace(line)
	line = strings.TrimPrefix(line, "|")
	line = strings.TrimSuffix(line, "|")
	cells := strings.Split(line, "|")
	for i := range cells {
		cells[i] = strings.TrimSpace(cells[i])
	}
	return cells
}

// isBlockStart reports whether a line begins a block, and so must not be
// swallowed into the paragraph or blockquote being accumulated above it.
//
// A picture is listed here even though a table is not, and the asymmetry is
// deliberate. A table is several lines long and an author naturally leaves a
// blank line around it; a picture is a single line, and writing it flush
// against the paragraph it illustrates is the obvious thing to do. Without
// this, that spelling would silently print the raw ![alt](path) as body text
// rather than drawing anything — a failure with no error attached to it.
func isBlockStart(line string) bool {
	return fenceRe.MatchString(line) ||
		headingRe.MatchString(line) ||
		ruleRe.MatchString(line) ||
		imageRe.MatchString(line) ||
		quoteRe.MatchString(line) ||
		bulletRe.MatchString(line) ||
		orderedRe.MatchString(line)
}

// imageBlock is one picture found while rendering, and where its reserved
// rows ended up in the output.
//
// render() emits a picture as nothing but blank rows — that is what keeps
// tui/render.py able to produce byte-identical output without knowing what a
// picture is. This struct is the Go-only side channel that says which file
// belongs in which of those gaps, so layout.go can put a real bitmap there
// later. Nothing the parity harness compares ever sees it.
type imageBlock struct {
	path       string // absolute path to the PNG on disk
	start      int    // index of its first reserved row within the rendered rows
	rows       int    // how many rows it reserves
	imgW, imgH int    // the picture's own pixel size, for the aspect fit at draw time
}

// render turns markdown into a list of styled rows at width columns.
//
// A thin wrapper over renderWithImages, kept so the five existing callers —
// and the blockquote recursion below — carry on unchanged, and so the
// signature tui/render.py mirrors stays exactly as it was.
func render(md string, width int) [][]span {
	rows, _ := renderWithImages(md, width)
	return rows
}

// renderWithImages is render plus the picture side channel. Go-only: there is
// deliberately no Python counterpart, because pictures are drawn by the live
// reader and the live reader is the one thing bin/parity.sh never runs.
func renderWithImages(md string, width int) ([][]span, []imageBlock) {
	imgs := []imageBlock{}
	width = max(20, width)
	md = stripFrontmatter(strings.ReplaceAll(md, "\t", "    "))
	src := strings.Split(md, "\n")
	out := [][]span{}
	i := 0
	n := len(src)

	blank := func() {
		if len(out) > 0 && len(out[len(out)-1]) != 0 {
			out = append(out, []span{})
		}
	}

	for i < n {
		line := src[i]

		if strings.TrimSpace(line) == "" {
			blank()
			i++
			continue
		}

		// -- fenced code ---------------------------------------------------
		if m := fenceRe.FindStringSubmatch(line); m != nil {
			fence := strings.Repeat(string(m[2][0]), 3)
			lang := m[3]
			i++
			body := []string{}
			for i < n {
				t := strings.TrimSpace(src[i])
				if strings.HasPrefix(strings.TrimLeftFunc(src[i], unicode.IsSpace), fence) &&
					strings.Trim(t, string(fence[0])) == "" {
					break
				}
				body = append(body, src[i])
				i++
			}
			i++ // closing fence
			out = append(out, renderCode(body, lang, width)...)
			continue
		}

		// -- heading -------------------------------------------------------
		if m := headingRe.FindStringSubmatch(line); m != nil {
			level := min(len(m[1]), 4)
			style := "h" + strconv.Itoa(level)
			blank()
			out = append(out, wrapSpans(parseInline(m[2], style), width, nil, nil)...)
			if level <= 2 {
				out = append(out, []span{{strings.Repeat("─", width), "rule"}})
			}
			out = append(out, []span{})
			i++
			continue
		}

		// -- horizontal rule ----------------------------------------------
		if ruleRe.MatchString(line) {
			out = append(out, []span{{strings.Repeat("─", width), "rule"}})
			out = append(out, []span{})
			i++
			continue
		}

		// -- picture --------------------------------------------------------
		if m := imageRe.FindStringSubmatch(line); m != nil {
			alt, rel := m[1], m[2]
			rows := 0
			// A missing, unreadable or non-PNG file reserves zero rows rather
			// than erroring, and Python must fail the same way: "just the
			// caption, no picture" is the one shape both sides can produce
			// identically without agreeing on an error message too.
			abs := filepath.Join(contentDir(resolveRoot()), rel)
			imgW, imgH := 0, 0
			if w, h, err := pngSize(abs); err == nil {
				imgW, imgH = w, h
				rows = imageRows(w, h, width)
			}
			if rows > 0 {
				// Recorded before the rows are appended, so start is the index
				// of the first reserved row rather than the one past the last.
				imgs = append(imgs, imageBlock{
					path: abs, start: len(out), rows: rows, imgW: imgW, imgH: imgH,
				})
			}
			for r := 0; r < rows; r++ {
				out = append(out, []span{{strings.Repeat(" ", width), "imagepad"}})
			}
			out = append(out, wrapSpans(parseInline(alt, "dim"), width, nil, nil)...)
			out = append(out, []span{})
			i++
			continue
		}

		// -- blockquote ----------------------------------------------------
		if quoteRe.MatchString(line) {
			block := []string{}
			// Lazy continuation: an unmarked line keeps the quote going, but a
			// heading, list or fence on the next line starts its own block
			// rather than being swallowed into the quotation.
			for i < n {
				m2 := quoteRe.FindStringSubmatch(src[i])
				cont := strings.TrimSpace(src[i]) != "" && len(block) > 0 && !isBlockStart(src[i])
				if m2 == nil && !cont {
					break
				}
				if m2 != nil {
					block = append(block, m2[1])
				} else {
					block = append(block, strings.TrimSpace(src[i]))
				}
				i++
			}
			inner := render(strings.Join(block, "\n"), width-3)
			for _, row := range inner {
				line := []span{{"│ ", "quotebar"}}
				for _, sp := range row {
					st := sp.style
					if st == "body" {
						st = "quote"
					}
					line = append(line, span{sp.text, st})
				}
				out = append(out, line)
			}
			out = append(out, []span{})
			continue
		}

		// -- table ---------------------------------------------------------
		if strings.Contains(line, "|") && i+1 < n && isTableSep(src[i+1]) {
			header := splitRow(line)
			aligns := parseAligns(splitRow(src[i+1]))
			i += 2
			rows := [][]string{}
			for i < n && strings.Contains(src[i], "|") && strings.TrimSpace(src[i]) != "" {
				rows = append(rows, splitRow(src[i]))
				i++
			}
			out = append(out, renderTable(header, aligns, rows, width)...)
			out = append(out, []span{})
			continue
		}

		// -- list ----------------------------------------------------------
		if bulletRe.MatchString(line) || orderedRe.MatchString(line) {
			i, out = renderList(src, i, width, out)
			out = append(out, []span{})
			continue
		}

		// -- paragraph -----------------------------------------------------
		para := []string{}
		for i < n && strings.TrimSpace(src[i]) != "" && !isBlockStart(src[i]) {
			para = append(para, strings.TrimSpace(src[i]))
			i++
		}
		out = append(out, wrapSpans(parseInline(strings.Join(para, " "), "body"), width, nil, nil)...)
	}

	for len(out) > 0 && len(out[len(out)-1]) == 0 {
		out = out[:len(out)-1]
	}
	return out, imgs
}

// renderCode paints a code block as a solid tinted slab: padded to full
// width, never wrapped.
//
// Wrapping code would silently corrupt the thing the reader is meant to copy,
// so long lines are clipped instead and the block keeps its shape.
func renderCode(body []string, lang string, width int) [][]span {
	lines := [][]span{}
	for len(body) > 0 && strings.TrimSpace(body[0]) == "" {
		body = body[1:]
	}
	for len(body) > 0 && strings.TrimSpace(body[len(body)-1]) == "" {
		body = body[:len(body)-1]
	}

	indent := 0
	seen := false
	for _, l := range body {
		if strings.TrimSpace(l) == "" {
			continue
		}
		d := len([]rune(l)) - len([]rune(strings.TrimLeftFunc(l, unicode.IsSpace)))
		if !seen || d < indent {
			indent, seen = d, true
		}
	}

	if lang != "" {
		lines = append(lines, padSpans([]span{{"  " + lang, "codelang"}}, width, "codelang"))
	} else {
		lines = append(lines, padSpans(nil, width, "codelang"))
	}
	for _, raw := range body {
		r := []rune(raw)
		text := ""
		if len(r) >= indent {
			text = string(r[indent:])
		} else {
			text = strings.TrimLeftFunc(raw, unicode.IsSpace)
		}
		lines = append(lines, padSpans([]span{{"  " + text, "codeblock"}}, width, "codeblock"))
	}
	lines = append(lines, padSpans(nil, width, "codeblock"))
	lines = append(lines, []span{})
	return lines
}

func renderList(src []string, i, width int, out [][]span) (int, [][]span) {
	n := len(src)
	counters := map[int]int{}
	for i < n {
		line := src[i]
		if strings.TrimSpace(line) == "" {
			// A blank line ends the list. A "loose" list separated by blanks
			// therefore renders as one block per item, which reads better than
			// silently welding two adjacent lists into one.
			break
		}

		mb := bulletRe.FindStringSubmatch(line)
		mo := orderedRe.FindStringSubmatch(line)
		if mb == nil && mo == nil {
			break
		}
		m := mb
		if m == nil {
			m = mo
		}

		level := min(len([]rune(m[1]))/2, 2)
		for lv := range counters {
			if lv > level {
				delete(counters, lv)
			}
		}

		var marker string
		if mo != nil {
			if _, ok := counters[level]; !ok {
				start, _ := strconv.Atoi(mo[2])
				counters[level] = start - 1
			}
			counters[level]++
			marker = strconv.Itoa(counters[level]) + "."
		} else {
			delete(counters, level)
			marker = bullets[level]
		}

		body := []string{m[3]}
		i++
		// Continuation lines: indented further than the marker, not a new item.
		for i < n && strings.TrimSpace(src[i]) != "" &&
			!bulletRe.MatchString(src[i]) && !orderedRe.MatchString(src[i]) {
			d := len([]rune(src[i])) - len([]rune(strings.TrimLeftFunc(src[i], unicode.IsSpace)))
			if d > len([]rune(m[1])) {
				body = append(body, strings.TrimSpace(src[i]))
				i++
			} else {
				break
			}
		}

		padLeft := strings.Repeat("  ", level)
		first := []span{{padLeft + " ", "body"}, {marker, "bullet"}, {" ", "body"}}
		rest := []span{{strings.Repeat(" ", spansWidth(first)), "body"}}
		out = append(out, wrapSpans(parseInline(strings.Join(body, " "), "body"), width, first, rest)...)
	}
	return i, out
}

func parseAligns(cells []string) []string {
	aligns := []string{}
	for _, c := range cells {
		c = strings.TrimSpace(c)
		switch {
		case strings.HasPrefix(c, ":") && strings.HasSuffix(c, ":") && len(c) >= 2:
			aligns = append(aligns, "center")
		case strings.HasSuffix(c, ":"):
			aligns = append(aligns, "right")
		default:
			aligns = append(aligns, "left")
		}
	}
	return aligns
}

func renderTable(header, aligns []string, rows [][]string, width int) [][]span {
	ncols := len(header)
	for len(aligns) < ncols {
		aligns = append(aligns, "left")
	}
	aligns = aligns[:ncols]
	for i := range rows {
		for len(rows[i]) < ncols {
			rows[i] = append(rows[i], "")
		}
		rows[i] = rows[i][:ncols]
	}

	gap := 3 // " │ "
	budget := width - 1 - gap*(ncols-1)
	if budget < ncols*3 {
		// Too narrow for a table: fall back to labelled stacks, which stay
		// readable at any width instead of collapsing into noise.
		return renderTableStacked(header, rows, width)
	}

	natural := make([]int, ncols)
	for c := 0; c < ncols; c++ {
		w := dwidth(header[c])
		for _, r := range rows {
			if d := dwidth(r[c]); d > w {
				w = d
			}
		}
		natural[c] = w
	}

	widths := fitColumns(natural, budget)

	out := [][]span{}
	out = append(out, tableRow(header, aligns, widths, "tablehead")...)
	sep := []span{}
	for c := 0; c < ncols; c++ {
		if c > 0 {
			sep = append(sep, span{"─┼─", "tableborder"})
		}
		sep = append(sep, span{strings.Repeat("─", widths[c]), "tableborder"})
	}
	out = append(out, append([]span{{" ", "body"}}, sep...))
	for _, r := range rows {
		out = append(out, tableRow(r, aligns, widths, "body")...)
	}
	return out
}

func tableRow(cells, aligns []string, widths []int, style string) [][]span {
	rendered := make([][][]span, len(widths))
	height := 0
	for c := range widths {
		lines := wrapSpans(parseInline(cells[c], style), widths[c], nil, nil)
		if len(lines) == 0 {
			lines = [][]span{{}}
		}
		rendered[c] = lines
		if len(lines) > height {
			height = len(lines)
		}
	}
	out := [][]span{}
	for li := 0; li < height; li++ {
		row := []span{{" ", "body"}}
		for c := range widths {
			if c > 0 {
				row = append(row, span{" │ ", "tableborder"})
			}
			var spans []span
			if li < len(rendered[c]) {
				spans = rendered[c][li]
			}
			row = append(row, alignSpans(spans, widths[c], aligns[c])...)
		}
		out = append(out, mergeSpans(row))
	}
	return out
}

func alignSpans(spans []span, width int, how string) []span {
	used := spansWidth(spans)
	slack := max(0, width-used)
	switch how {
	case "right":
		return append([]span{{strings.Repeat(" ", slack), "body"}}, spans...)
	case "center":
		left := slack / 2
		out := append([]span{{strings.Repeat(" ", left), "body"}}, spans...)
		return append(out, span{strings.Repeat(" ", slack-left), "body"})
	}
	return append(append([]span{}, spans...), span{strings.Repeat(" ", slack), "body"})
}

// fitColumns shrinks the widest columns first until the table fits the budget.
func fitColumns(natural []int, budget int) []int {
	widths := append([]int{}, natural...)
	sum := func() int {
		t := 0
		for _, w := range widths {
			t += w
		}
		return t
	}
	for sum() > budget {
		widest := 0
		for c := range widths {
			if widths[c] > widths[widest] {
				widest = c
			}
		}
		if widths[widest] <= 3 {
			break
		}
		widths[widest]--
	}
	// Spend any leftover room on the columns that wanted it most.
	slack := budget - sum()
	order := make([]int, len(widths))
	for i := range order {
		order[i] = i
	}
	// Stable sort by (natural - width) descending, matching Python's sorted().
	for i := 1; i < len(order); i++ {
		for j := i; j > 0; j-- {
			a, b := order[j-1], order[j]
			if natural[b]-widths[b] > natural[a]-widths[a] {
				order[j-1], order[j] = b, a
			} else {
				break
			}
		}
	}
	idx := 0
	for slack > 0 && len(order) > 0 {
		c := order[idx%len(order)]
		if widths[c] < natural[c] {
			widths[c]++
			slack--
		} else {
			all := true
			for _, k := range order {
				if widths[k] < natural[k] {
					all = false
					break
				}
			}
			if all {
				break
			}
		}
		idx++
	}
	return widths
}

func renderTableStacked(header []string, rows [][]string, width int) [][]span {
	out := [][]span{}
	for _, r := range rows {
		for c, cell := range r {
			label := ""
			if c < len(header) {
				label = header[c]
			}
			first := []span{{" ", "body"}, {label + ": ", "tablehead"}}
			rest := []span{{"   ", "body"}}
			out = append(out, wrapSpans(parseInline(cell, "body"), width, first, rest)...)
		}
		out = append(out, []span{})
	}
	return out
}
