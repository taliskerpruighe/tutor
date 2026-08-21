# Visual and style guide

How a new article should LOOK. The counterpart to the voice guide, which
covers how it should sound. Everything here is drawn from the fifty
articles already on disk — they are the reference, not this document.

The renderer (`go/render.go`, mirrored by `tui/render.py`) implements a
deliberate SUBSET of markdown. Anything outside it renders as a plain
wrapped paragraph: readable, but not what you meant. Stay inside it.

---

## The shape of a file

Every article is the same five things in the same order:

1. Frontmatter, between `---` fences.
2. A blank line, then the H1 — the same text as `title:`.
3. A blank line, the version tag alone on its line, a blank line.
4. The body: opening prose, then H2 sections.
5. The sign-off line — the word Press, the key `n` in backticks, a stop.

Wrap the SOURCE prose at about 74 columns. The renderer reflows to the
pane width, so source wrapping is for the author's benefit only — but
the whole corpus does it, and a 200-column paragraph is a diff hazard.

## Frontmatter

Exactly these seven keys, in exactly this order. `section` is the only
optional one, and it is present in all fifty articles.

```
---
id: agents/context
title: Context
part: Agents
section: Context
order: 3
summary: Every agent has a fixed amount of brainspace, and everything it touches fills a little of it.
keywords: [context, context window, tokens, brainspace, model, haiku, sonnet, opus, fable, size]
---
```

- **id** — `area/slug`, lowercase, hyphenated. The area prefix is the
  subject, not the directory number (`shell/`, `agents/`, `skills/`,
  `subagents/`, `terminal/`, `wiki/`). Stable: it is what the skill and
  search cite. Never reuse one.
- **title** — sentence case, no trailing period. Matches the H1 word for
  word. Em dashes are fine: `Step two — the workers`.
- **part** — the display name on the tab bar, Title Case
  (`The CLI`, `TUIs`, `Agents`). Identical string for every article in
  the directory; a typo splits the part in two.
- **section** — the side-tab group, Title Case
  (`Command Lines and Prompts`, `Build a Chain`). A section is a RUN OF
  CONSECUTIVE ARTICLES sharing the value; there is no second directory
  level.
- **order** — an integer, and it is **part-global and monotonic**. It is
  NEVER restarted per section, because sections are formed by grouping
  consecutive equal `section` values — restarting the count would
  interleave the runs and shatter the sections. `The CLI` runs 1, 2, 3,
  4, 7 across three sections; the numbering carries straight through.
  Gaps are fine. Match the file's number prefix.
- **summary** — one sentence, no trailing period, shown in search
  results. It states what the reader gets, in the article's own voice,
  not a topic label. Good: *Clicking does one thing at a time; a typed
  command does a thousand, from anywhere.* Bad: *An overview of shell
  capabilities.*
- **keywords** — a flow-style list, lowercase, 6 to 12 entries. Mix
  three kinds: the formal terms (`context window`, `kernel`), the words
  a beginner would actually type (`brainspace`, `folder`, `party
  trick`), and the literal names of any command, file, model or flag the
  article discusses (`cd`, `haiku`, `toml`). Multi-word entries need no
  quotes.

## The version tag

Every article carries one, alone on its line between the H1 and the
first paragraph, blank line either side, italic with single asterisks
and nothing else on the line. The fifty existing articles all read
`*v0.1.0*`. **Every article written now carries `*v0.2.0*`.**

Worked example — the whole opening of a new article:

```
---
id: hooks/what-a-hook-is
title: What a hook is
part: Hooks
section: Hooks
order: 1
summary: A command that fires by itself when the agent does something, without anyone asking
keywords: [hook, trigger, event, settings, automation, pretooluse]
---

# What a hook is

*v0.2.0*

A hook is a command you leave lying in wait.
```

## Structure

- **Length**: 374 to 912 words, median 589. Aim 450–700. Under 350 is a
  stub; over 900 should be two articles.
- **H2s**: two to five is the norm (seven at the outside, and only for a
  numbered walkthrough). Their text is a short phrase, sentence case,
  and it carries meaning — `Everything means everything`,
  `Where the settings landed` — not a label like `Overview`.
- **H3 is never used.** Not once in fifty articles. If you want one, you
  want a second article. `####` renders but has no place here.
- **Opening**: two or three short paragraphs before the first H2, no
  heading of their own, putting the idea in plain words.
- **Closing**: the final H2's last paragraph, then the last line —
  the word Press, the key `n` in backticks, a full stop, bare. Nothing
  goes between them, and nothing in that last paragraph points at the
  next article. Only the last article of a part ends otherwise: a `---`
  rule and a paragraph naming the part coming, which names parts and
  never counts them.
- **Blockquote asides**: about half of all articles have one or two.
  They hold material the reader can skip — history, a back-reference to
  an earlier article, an encouragement — never a fact the next paragraph
  depends on. Two to four lines. Often the last block before the
  sign-off.

## The markdown subset

Recognised, and nothing else:

    # ## ### ####     paragraphs (reflowed)    ```fenced code```
    `inline code`     **bold**  *italic*       - bullets  1. ordered
    > blockquotes     --- rules   [text](url)  | pipe | tables |
    ![caption](images/x.png)  — PNG, alone on its line, Ghostty only

`H1` and `H2` draw a full-width rule under themselves automatically. Do
not add `---` after a heading; you will get two rules.

**Code blocks are CLIPPED, never wrapped.** A long line is silently
truncated at the pane edge. Keep every line inside a fence to **60
columns**; the corpus maximum is 58. The block is painted as a solid
tinted slab, common leading indent stripped, so it also serves for ASCII
diagrams and worked output, not only commands. A language tag prints as
a small label; most blocks in the corpus carry none.

**Tables** take their natural width and shrink the widest column first;
below roughly `3 × columns` they collapse into labelled stacks. So keep
cells to a word or a short phrase, two or three columns, five rows or
fewer. `|---|---|` is the whole separator you need. An empty first
header cell is fine and is how a comparison table is labelled down its
left edge.

**Lists**: `-` for bullets, `1.` for ordered. Nesting is **two spaces
per level, to a depth of three**; the corpus never nests, so consider
whether you need to. A **blank line between items ends the list and
starts a new one** — deliberate, and it means a list is a tight block of
adjacent lines. A continuation line indented past the marker joins the
item above.

**Inline**: `**bold**` for a term being defined on first use — this is
the corpus's heaviest inline habit. `*italic*` for the titles of other
articles (*Location matters*) and for light emphasis. Backticks for
anything typed: commands, filenames, keys, flags, model names in a
command. Links render as text plus a shortened URL in parentheses, so do
not write "click here".

**Rules** (`---`) separate nothing in the corpus; headings already rule
themselves. Use one only for a genuine hard break.

## Pictures

One picture exists in the whole corpus, and its handling is the pattern:

    ![This reader itself, drawn entirely out of characters: the parts of
    the course run across the top, the articles down the left, and the
    article fills the rest.](images/the-reader.png)

(on ONE line in the file — wrapped here only to fit this page.)

- **PNG only**, from `content/images/`, referenced as `images/name.png`.
- **Alone on its line.** An image folded into a sentence is not
  recognised and prints as raw text.
- **Under 500 KB**, and a test enforces it. Size the file to about the
  width it will be shown at — 1200px is plenty.
- **Alt text is a caption, not a label.** Pictures only draw in Ghostty;
  in tmux and everywhere else the reader gets the alt text ALONE, so
  write a sentence that stands on its own without the picture.
- **No height is stated.** Rows are reserved from the picture's own
  proportions, so a wide short screenshot suits the pane far better than
  a tall narrow one.

## Exemplars

Open these before drafting:

- `content/12-agents/02-context.md` — a table, two ASCII-diagram code
  blocks, five H2s. The model of a mixed article.
- `content/14-subagents/07-step-two-the-workers.md` — a numbered
  walkthrough: short command fences, bold-led bullet lists, H2 per step.
- `content/06-linux/03-why-it-is-better.md` — plain prose, no code, no
  table, five H2s. Proof that an article needs no furniture.
- `content/02-tuis/02-gui-and-tui.md` — the picture, a three-row
  comparison table, a closing blockquote aside.
