// The content corpus: frontmatter parsing and the generated index.
//
// content/ is the single source of truth for the whole tutor. Two very
// different readers consume it:
//
//   - this TUI, which needs an ordered navigation tree, and
//   - the Claude Code skill, which needs a lookup table to find the one file
//     that answers a question.
//
// Both read content/index.json, generated here. Neither copies prose, so
// there is exactly one place a fact can live and exactly one place to edit it.
//
// The index rebuilds itself whenever any article is newer than it, so
// authoring is "drop a markdown file in and reopen" — there is no build step
// to forget.
package main

import (
	"bytes"
	"encoding/json"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

const indexName = "index.json"

// Article, Part and Index are laid out so encoding/json emits fields in the
// same order Python's dict insertion does. The parity check is byte for byte,
// so field order is load-bearing.
type Article struct {
	ID       string   `json:"id"`
	Title    string   `json:"title"`
	Section  string   `json:"section"`
	Summary  string   `json:"summary"`
	Version  string   `json:"version"`
	Keywords []string `json:"keywords"`
	Path     string   `json:"path"`

	sort sortKey
}

type Part struct {
	Slug     string    `json:"slug"`
	Title    string    `json:"title"`
	Level    string    `json:"level"`
	Articles []Article `json:"articles"`
}

// Section is a run of consecutive articles sharing a `section:` value. It is
// derived at render time rather than stored: the index stays a flat list of
// articles, so search, `flatten` and the Claude Code skill all carry on
// reading it exactly as before.
type Section struct {
	Title    string
	From, To int // [From, To)
}

func (s Section) contains(i int) bool { return s.From <= i && i < s.To }

// partSections groups a part's articles into runs of equal `section:`,
// including the empty one. A part where no article carries `section:` is
// therefore a single untitled run spanning the lot, which draws as the plain
// numbered list it has always been — the sectionless case is not a special
// case, it is the degenerate one.
func partSections(part Part) []Section {
	out := []Section{}
	for i, a := range part.Articles {
		if n := len(out); n > 0 && out[n-1].Title == a.Section && out[n-1].To == i {
			out[n-1].To = i + 1
			continue
		}
		out = append(out, Section{a.Section, i, i + 1})
	}
	return out
}

// sectionAt returns the section holding article i, and whether there is one.
func sectionAt(part Part, i int) (int, bool) {
	for si, s := range partSections(part) {
		if s.contains(i) {
			return si, true
		}
	}
	return 0, false
}

type Index struct {
	Parts []Part `json:"parts"`
}

// Level is a run of consecutive parts sharing a `level:` value — the tabs
// along the top. It is derived the same way Section is, and for the same
// reason: the index stays a flat list of parts holding a flat list of
// articles, so search, `flatten` and the Claude Code skill never learnt that
// levels exist.
type Level struct {
	Title    string
	From, To int // [From, To) over index.Parts
}

func (l Level) contains(i int) bool { return l.From <= i && i < l.To }

// levelOf is a part's level, falling back to its own title. That fallback is
// what makes a corpus carrying no `level:` at all degrade to the old
// behaviour exactly — every part becomes its own single-part level, so the
// tab bar still reads as the list of parts and the sidebar suppresses the
// redundant part heading.
func levelOf(part Part) string {
	if part.Level != "" {
		return part.Level
	}
	return part.Title
}

// indexLevels groups the index's parts into runs of equal `level:`.
func indexLevels(index Index) []Level {
	out := []Level{}
	for i, p := range index.Parts {
		if n := len(out); n > 0 && out[n-1].Title == levelOf(p) && out[n-1].To == i {
			out[n-1].To = i + 1
			continue
		}
		out = append(out, Level{levelOf(p), i, i + 1})
	}
	return out
}

// levelAt returns the level holding part i, and whether there is one.
func levelAt(index Index, i int) (int, bool) {
	for li, l := range indexLevels(index) {
		if l.contains(i) {
			return li, true
		}
	}
	return 0, false
}

type sortKey struct {
	primary int
	numeric int
	title   string
}

func (a sortKey) less(b sortKey) bool {
	if a.primary != b.primary {
		return a.primary < b.primary
	}
	if a.numeric != b.numeric {
		return a.numeric < b.numeric
	}
	return a.title < b.title
}

// Frontmatter is a deliberately tiny subset: `key: scalar` and `key: [a, b]`.
// Hand-parsing it avoids a YAML dependency, which would otherwise be the only
// thing standing between her and a working install.
var (
	fmRe      = regexp.MustCompile(`(?s)\A---\r?\n(.*?)\r?\n---\r?\n?`)
	keyRe     = regexp.MustCompile(`^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$`)
	numRe     = regexp.MustCompile(`^(\d+)`)
	prefixRe  = regexp.MustCompile(`^\d+[-_]`)
	headRe    = regexp.MustCompile(`^#{1,6}\s+(.*?)\s*#*\s*$`)
	versionRe = regexp.MustCompile(`(?m)^\*(v[0-9]+(?:\.[0-9]+)*)\*$`)
)

type frontmatter struct {
	vals  map[string]string
	lists map[string][]string
	order *int
}

func (f frontmatter) get(key string) string { return f.vals[key] }

func (f frontmatter) keywords() []string {
	if l, ok := f.lists["keywords"]; ok {
		return l
	}
	if s, ok := f.vals["keywords"]; ok {
		out := []string{}
		for _, v := range strings.Split(s, ",") {
			if t := strings.TrimSpace(v); t != "" {
				out = append(out, t)
			}
		}
		return out
	}
	return []string{}
}

func unquote(value string) string {
	r := []rune(value)
	if len(r) >= 2 && r[0] == r[len(r)-1] && (r[0] == '"' || r[0] == '\'') {
		return string(r[1 : len(r)-1])
	}
	return value
}

// parseFrontmatter returns the metadata and the body. Missing or malformed
// frontmatter yields empty metadata and the text untouched.
func parseFrontmatter(text string) (frontmatter, string) {
	meta := frontmatter{vals: map[string]string{}, lists: map[string][]string{}}
	loc := fmRe.FindStringSubmatchIndex(text)
	if loc == nil || loc[0] != 0 {
		return meta, text
	}
	block := text[loc[2]:loc[3]]
	for _, line := range strings.Split(block, "\n") {
		line = strings.TrimRightFunc(line, isSpaceRune)
		trimmed := strings.TrimSpace(line)
		if trimmed == "" || strings.HasPrefix(trimmed, "#") {
			continue
		}
		km := keyRe.FindStringSubmatch(line)
		if km == nil {
			continue
		}
		key, raw := km[1], strings.TrimSpace(km[2])
		if strings.HasPrefix(raw, "[") && strings.HasSuffix(raw, "]") {
			inner := strings.TrimSpace(raw[1 : len(raw)-1])
			list := []string{}
			for _, v := range strings.Split(inner, ",") {
				if strings.TrimSpace(v) != "" {
					list = append(list, unquote(strings.TrimSpace(v)))
				}
			}
			meta.lists[key] = list
			delete(meta.vals, key)
			continue
		}
		value := unquote(raw)
		if key == "order" {
			if n, err := strconv.Atoi(value); err == nil {
				meta.order = &n
			}
		}
		meta.vals[key] = value
		delete(meta.lists, key)
	}
	return meta, text[loc[1]:]
}

// deslug turns `01-the-terminal` into `The Terminal`. A fallback, not the rule.
func deslug(slug string) string {
	slug = prefixRe.ReplaceAllString(slug, "")
	words := regexp.MustCompile(`[-_\s]+`).Split(slug, -1)
	out := []string{}
	for _, w := range words {
		if w == "" {
			continue
		}
		r := []rune(w)
		out = append(out, strings.ToUpper(string(r[0]))+string(r[1:]))
	}
	return strings.Join(out, " ")
}

// makeSortKey orders by explicit `order`, then by filename prefix, then title.
func makeSortKey(prefixSource string, order *int, title string) sortKey {
	numeric := 1000000
	if m := numRe.FindStringSubmatch(prefixSource); m != nil {
		if n, err := strconv.Atoi(m[1]); err == nil {
			numeric = n
		}
	}
	primary := numeric
	if order != nil {
		primary = *order
	}
	return sortKey{primary, numeric, strings.ToLower(title)}
}

func contentDir(root string) string { return filepath.Join(root, "content") }
func indexPath(root string) string  { return filepath.Join(contentDir(root), indexName) }

type mdFile struct {
	slug, name, path string
}

func iterMarkdown(root string) []mdFile {
	out := []mdFile{}
	base := contentDir(root)
	entries, err := os.ReadDir(base)
	if err != nil {
		return out
	}
	slugs := []string{}
	for _, e := range entries {
		slugs = append(slugs, e.Name())
	}
	sort.Strings(slugs)
	for _, slug := range slugs {
		partDir := filepath.Join(base, slug)
		info, err := os.Stat(partDir)
		if err != nil || !info.IsDir() || strings.HasPrefix(slug, ".") || strings.HasPrefix(slug, "_") {
			continue
		}
		files, err := os.ReadDir(partDir)
		if err != nil {
			continue
		}
		names := []string{}
		for _, f := range files {
			names = append(names, f.Name())
		}
		sort.Strings(names)
		for _, name := range names {
			if strings.HasSuffix(name, ".md") &&
				!strings.HasPrefix(name, ".") && !strings.HasPrefix(name, "_") {
				out = append(out, mdFile{slug, name, filepath.Join(partDir, name)})
			}
		}
	}
	return out
}

func firstHeading(body string) string {
	for _, line := range strings.Split(body, "\n") {
		if m := headRe.FindStringSubmatch(line); m != nil {
			return strings.TrimSpace(m[1])
		}
	}
	return ""
}

// extractVersion returns an article's own version tag — the italic line
// between the H1 and the first paragraph, e.g. `*v0.2.0*` — including its
// leading "v", or the empty string if no line in the body matches. Only the
// first matching line counts; render.go passes the line through as ordinary
// italic text and must go on doing so, so this never touches rendering.
func extractVersion(body string) string {
	if m := versionRe.FindStringSubmatch(body); m != nil {
		return m[1]
	}
	return ""
}

// buildIndex scans content/ and returns the index structure.
func buildIndex(root string) Index {
	type partAcc struct {
		part *Part
		key  sortKey
	}
	order := []string{}
	parts := map[string]*Part{}

	for _, f := range iterMarkdown(root) {
		raw, err := os.ReadFile(f.path)
		if err != nil {
			continue
		}
		meta, body := parseFrontmatter(string(raw))

		stem := f.name[:len(f.name)-3]
		title := meta.get("title")
		if title == "" {
			title = firstHeading(body)
		}
		if title == "" {
			title = deslug(stem)
		}
		partTitle := meta.get("part")
		if partTitle == "" {
			partTitle = deslug(f.slug)
		}
		id := meta.get("id")
		if id == "" {
			id = prefixRe.ReplaceAllString(f.slug, "") + "/" + stem
		}
		rel, err := filepath.Rel(root, f.path)
		if err != nil {
			rel = f.path
		}
		article := Article{
			ID:       id,
			Title:    title,
			Section:  meta.get("section"),
			Summary:  meta.get("summary"),
			Version:  extractVersion(body),
			Keywords: meta.keywords(),
			Path:     filepath.ToSlash(rel),
			sort:     makeSortKey(f.name, meta.order, title),
		}

		part, ok := parts[f.slug]
		if !ok {
			part = &Part{Slug: f.slug, Title: partTitle, Level: meta.get("level"),
				Articles: []Article{}}
			parts[f.slug] = part
			order = append(order, f.slug)
		}
		// The first article carrying an explicit `part:` names the part; later
		// ones do not get to rename it out from under the earlier files.
		if meta.get("part") != "" && part.Title == deslug(f.slug) {
			part.Title = meta.get("part")
		}
		// `level:` follows the same first-one-wins rule.
		if part.Level == "" {
			part.Level = meta.get("level")
		}
		part.Articles = append(part.Articles, article)
	}

	accs := []partAcc{}
	for _, slug := range order {
		accs = append(accs, partAcc{parts[slug], makeSortKey(slug, nil, parts[slug].Title)})
	}
	sort.SliceStable(accs, func(i, j int) bool { return accs[i].key.less(accs[j].key) })

	index := Index{Parts: []Part{}}
	for _, acc := range accs {
		arts := acc.part.Articles
		sort.SliceStable(arts, func(i, j int) bool { return arts[i].sort.less(arts[j].sort) })
		acc.part.Articles = arts
		index.Parts = append(index.Parts, *acc.part)
	}
	return index
}

// encodeIndex matches Python's json.dump(indent=2, ensure_ascii=False)
// exactly: two-space indent, no HTML escaping, one trailing newline.
func encodeIndex(index Index) ([]byte, error) {
	var buf bytes.Buffer
	enc := json.NewEncoder(&buf)
	enc.SetEscapeHTML(false)
	enc.SetIndent("", "  ")
	if err := enc.Encode(index); err != nil {
		return nil, err
	}
	return buf.Bytes(), nil
}

func writeIndex(root string) (Index, error) {
	index := buildIndex(root)
	data, err := encodeIndex(index)
	if err != nil {
		return index, err
	}
	target := indexPath(root)
	if err := os.MkdirAll(filepath.Dir(target), 0o755); err != nil {
		return index, err
	}
	return index, os.WriteFile(target, data, 0o644)
}

// isStale is true when any article, or the set of articles, is newer than the
// index.
func isStale(root string) bool {
	target := indexPath(root)
	st, err := os.Stat(target)
	if err != nil {
		return true
	}
	stamp := st.ModTime()
	if base, err := os.Stat(contentDir(root)); err == nil && base.ModTime().After(stamp) {
		return true
	}
	for _, f := range iterMarkdown(root) {
		if fi, err := os.Stat(f.path); err == nil && fi.ModTime().After(stamp) {
			return true
		}
		// A rename or deletion changes the directory's own mtime.
		if di, err := os.Stat(filepath.Dir(f.path)); err == nil && di.ModTime().After(stamp) {
			return true
		}
	}
	return false
}

// loadIndex loads the index, regenerating it first if the content has moved on.
func loadIndex(root string, rebuild bool) Index {
	if rebuild && isStale(root) {
		index, err := writeIndex(root)
		if err != nil {
			// A read-only install still works; it just cannot cache.
			return buildIndex(root)
		}
		return index
	}
	data, err := os.ReadFile(indexPath(root))
	if err != nil {
		return buildIndex(root)
	}
	var index Index
	if err := json.Unmarshal(data, &index); err != nil {
		return buildIndex(root)
	}
	return index
}

// readArticle returns the markdown body of an article, frontmatter stripped.
func readArticle(root string, a Article) string {
	path := filepath.Join(root, a.Path)
	raw, err := os.ReadFile(path)
	if err != nil {
		return "# Missing article\n\n`" + a.Path + "` could not be read.\n\n    " +
			err.Error() + "\n"
	}
	_, body := parseFrontmatter(string(raw))
	return body
}

type located struct {
	partI, articleI int
	part            Part
	article         Article
}

// flatten lists all articles in reading order.
func flatten(index Index) []located {
	out := []located{}
	for pi, part := range index.Parts {
		for ai, article := range part.Articles {
			out = append(out, located{pi, ai, part, article})
		}
	}
	return out
}

// searchIndex ranks articles against a query. Title and keyword hits outrank
// body hits, and every term must appear somewhere.
func searchIndex(root string, index Index, query string) []located {
	query = strings.ToLower(strings.TrimSpace(query))
	if query == "" {
		return []located{}
	}
	terms := strings.Fields(query)

	type scored struct {
		score int
		item  located
	}
	results := []scored{}

	for _, item := range flatten(index) {
		haystacks := []string{
			strings.ToLower(item.article.Title),
			strings.ToLower(strings.Join(item.article.Keywords, " ")),
			strings.ToLower(item.article.Summary),
			strings.ToLower(readArticle(root, item.article)),
		}
		weights := []int{10, 6, 4, 1}
		score := 0
		for _, term := range terms {
			hit := 0
			for i, hay := range haystacks {
				if strings.Contains(hay, term) && weights[i] > hit {
					hit = weights[i]
				}
			}
			if hit == 0 {
				score = 0
				break
			}
			score += hit
		}
		if score > 0 {
			results = append(results, scored{score, item})
		}
	}

	sort.SliceStable(results, func(i, j int) bool {
		a, b := results[i], results[j]
		if a.score != b.score {
			return a.score > b.score
		}
		if a.item.partI != b.item.partI {
			return a.item.partI < b.item.partI
		}
		return a.item.articleI < b.item.articleI
	})

	out := []located{}
	for _, r := range results {
		out = append(out, r.item)
	}
	return out
}
