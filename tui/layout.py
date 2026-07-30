"""Screen composition: tab bar, sidebar, article pane, status bar.

Turns application state into a frame — the list of styled rows :mod:`term`
paints — and, in the same pass, the hitboxes that make the chrome clickable.
Building both together is what keeps the mouse honest: a tab is clickable at
exactly the columns it was drawn at, with no second layout calculation to
drift out of sync.

    ▌Interface   Setup   Agents   Skills   Subagents
    ────────────────────────────────────────────────────────────────
      The Terminal       │  Paths and the filesystem
    ▌ The Shell          │  ────────────────────────
    ▌1  What is a shell  │  Every file has an address…
     2  Paths            │
     3  Pipes            │
    ────────────────────────────────────────────────────────────────
     Interface 1/5 · The Shell 2/2 · Paths 2/4 · ←→ parts · ⇥ sections
"""

from . import content
from .render import char_width, clip, dwidth, pad, spans_width

MIN_COLS = 60
MIN_ROWS = 15

CHROME_ROWS = 4  # tab bar, rule, rule, status bar


class Frame:
    """A painted frame plus the hitboxes needed to interpret a click."""

    def __init__(self, rows):
        self.rows = rows
        self.tabs = []      # (x0, x1, part_index)
        self.items = []     # (y, kind, item_index)
        self.pane_x = 0
        self.pane_y = 0
        self.pane_w = 0
        self.pane_h = 0

    def tab_at(self, x, y):
        if y != 0:
            return None
        for x0, x1, index in self.tabs:
            if x0 <= x < x1:
                return index
        return None

    def item_at(self, x, y):
        """``(kind, index)`` for the sidebar row at *y*, or ``None``."""
        if x >= self.pane_x:
            return None
        for row_y, kind, index in self.items:
            if row_y == y:
                return kind, index
        return None

    def in_pane(self, x, y):
        return (
            self.pane_x <= x < self.pane_x + self.pane_w
            and self.pane_y <= y < self.pane_y + self.pane_h
        )


def sidebar_width(cols):
    return min(28, max(18, cols // 4))


def pane_width(cols):
    # sidebar, separator, two spaces of gutter, one column of scrollbar.
    return max(20, cols - sidebar_width(cols) - 5)


def too_small(cols, rows):
    return cols < MIN_COLS or rows < MIN_ROWS


def small_frame(cols, rows):
    message = "Please widen this window to at least %d×%d." % (MIN_COLS, MIN_ROWS)
    out = [[] for _ in range(rows)]
    y = max(0, rows // 2 - 1)
    if y < rows:
        text = clip([(message, "warn")], cols)
        left = max(0, (cols - spans_width(text)) // 2)
        out[y] = [(" " * left, "body")] + text
    if y + 2 < rows:
        hint = clip([("Currently %d×%d." % (cols, rows), "dim")], cols)
        left = max(0, (cols - spans_width(hint)) // 2)
        out[y + 2] = [(" " * left, "body")] + hint
    return Frame(out)


# --------------------------------------------------------------------------
# Chrome
# --------------------------------------------------------------------------


def _slice(spans, a, b):
    """The sub-span-list covering columns ``[a, b)`` of a span list."""
    out = []
    x = 0
    for text, style in spans:
        w = dwidth(text)
        if x + w <= a:
            x += w
            continue
        if x >= b:
            break
        piece = []
        for ch in text:
            if a <= x < b:
                piece.append(ch)
            x += char_width(ch)
        if piece:
            out.append(("".join(piece), style))
    return out


def _tab_bar(frame, parts, active, cols):
    labels = [("  " + p["title"] + "  ") for p in parts] or ["  (no content)  "]
    spans = []
    boxes = []
    x = 0
    for i, label in enumerate(labels):
        w = dwidth(label)
        spans.append((label, "tab_active" if i == active else "tab_idle"))
        boxes.append((x, x + w, i))
        x += w
    total = x

    if total <= cols:
        frame.tabs.extend(boxes)
        return pad(spans, cols)

    # Too many parts to show at once: scroll the strip, reserving a column at
    # each end for the « » affordances so it is obvious more exist.
    inner = cols - 2
    ax0, ax1, _ = boxes[active] if active < len(boxes) else (0, 0, 0)
    start = max(0, min(ax1 - inner, total - inner))
    if ax0 < start:
        start = ax0
    row = [("«", "tab_arrow")] + _slice(spans, start, start + inner) + [("»", "tab_arrow")]
    for x0, x1, i in boxes:
        vx0, vx1 = max(1, x0 - start + 1), min(cols - 1, x1 - start + 1)
        if vx1 > vx0:
            frame.tabs.append((vx0, vx1, i))
    return pad(row, cols)


def _status_bar(app, cols):
    if app.mode == "search":
        left = [("/", "status_key"), (app.query, "status"), ("▌", "status_key")]
        right = "%d match%s · enter open · esc cancel" % (
            len(app.results),
            "" if len(app.results) == 1 else "es",
        )
    else:
        part = app.part()
        article = app.article()
        pieces = []
        if part:
            pieces.append("%s %d/%d" % (part["title"], app.part_i + 1, len(app.index["parts"])))
        if article:
            # Inside a section the article counts within it, matching the
            # numbers in the sidebar and the keys that jump to them.
            first, last = 0, len(part["articles"])
            if article.get("section"):
                si = content.section_at(part, app.article_i)
                _title, first, last = content.part_sections(part)[si]
                # No counter on the section: the sidebar already shows how
                # many there are, and the strip is the scarcest row we have.
                pieces.append(article["section"])
            pieces.append("%s %d/%d" % (article["title"],
                                        app.article_i - first + 1, last - first))
        pieces.append("%d%%" % app.scroll_percent())
        left = [(" " + " · ".join(pieces), "status")]
        # Hints are dropped from the right as the window narrows, so the most
        # useful ones survive instead of the whole strip being cut mid-word.
        hints = ["←→ parts", "⇥ sections", "↑↓ scroll", "n next", "/ find", "? help", "q quit"]
        room = cols - spans_width(left) - 3
        while len(hints) > 1 and dwidth(" · ".join(hints)) > room:
            hints.pop(-2 if len(hints) > 1 else 0)
        right = " · ".join(hints)

    right_spans = clip([(right + " ", "status")], max(0, cols - spans_width(left) - 2))
    gap = cols - spans_width(left) - spans_width(right_spans)
    return pad(left + [(" " * max(0, gap), "status")] + right_spans, cols, "status")


def _sidebar_entries(app):
    """Lay the left column out.

    Every section's header, followed by its articles, the whole part on show
    at once. Numbering restarts inside each section, matching the keys —
    ``1``-``9`` count within the section you are in, so a part of more than
    nine articles still has every page one keypress away. A part whose
    articles carry no ``section:`` is a single untitled section, so it draws
    as the plain numbered list it always was. Entries are
    ``(num, title, sub, kind, index, open)``.
    """
    if app.mode == "search":
        entries = [
            ("%d" % (i + 1), a["title"], p["title"], "article", i, False)
            for i, (_pi, _ai, p, a) in enumerate(app.results)
        ]
        return entries, app.result_i

    part = app.part()
    if not part:
        return [], 0
    articles = part.get("articles", [])
    open_i = content.section_at(part, app.article_i)
    entries = []
    selected = 0
    for si, (title, start, stop) in enumerate(content.part_sections(part)):
        if title:
            entries.append(("", title, None, "section", si, si == open_i))
        for ai in range(start, stop):
            if ai == app.article_i:
                selected = len(entries)
            entries.append(
                ("%d" % (ai - start + 1), articles[ai]["title"], None, "article", ai, False)
            )
    return entries, selected


def _sidebar_start(count, selected, height):
    """Scroll the column so the selected row is on screen.

    Without this the list is simply truncated at *height*, which at the
    minimum window size can cut off the article being read.
    """
    if count <= height or height <= 0:
        return 0
    return min(min(max(0, selected - height // 2), count - height), selected)


def _sidebar_rows(frame, app, width, height, top):
    rows = []
    entries, selected = _sidebar_entries(app)
    start = _sidebar_start(len(entries), selected, height)
    if start > 0:
        entries = entries[start:]
        selected -= start

    for i in range(height):
        if i >= len(entries):
            # Blank rows must still occupy their columns, or the separator and
            # everything right of it slides left below the last article.
            rows.append([(" " * width, "body")])
            continue
        num, title, sub, kind, index, is_open = entries[i]
        # A section header is the side tab: styled like the tabs along the
        # top, marked when it is the one standing open.
        if kind == "section":
            marker = ("▌", "sel_bar") if is_open else (" ", "body")
            style = "tab_active" if is_open else "tab_idle"
            rows.append(pad([marker, (" ", "body"), (title, style)], width, "body"))
            frame.items.append((top + i, kind, index))
            continue
        is_sel = i == selected
        marker = ("▌", "sel_bar") if is_sel else (" ", "body")
        num_style = "sel_row" if is_sel else "row_num"
        text_style = "sel_row" if is_sel else "row"
        line = [marker, (num.rjust(2) + "  ", num_style), (title, text_style)]
        if sub:
            line.append(("  " + sub, "dim" if not is_sel else "sel_row"))
        rows.append(pad(line, width, "sel_row" if is_sel else "body"))
        frame.items.append((top + i, kind, index))
    return rows


def _scrollbar(height, total, visible, scroll):
    """A one-column track. Returns a list of ``(char, style)`` per body row."""
    if total <= visible or height <= 0:
        return [(" ", "body")] * height
    thumb = max(1, int(height * visible / total))
    span = height - thumb
    reach = max(1, total - visible)
    start = int(round(span * min(scroll, reach) / reach))
    return [
        ("█", "sep") if start <= i < start + thumb else ("│", "faint")
        for i in range(height)
    ]


# --------------------------------------------------------------------------
# Frame assembly
# --------------------------------------------------------------------------


def _drop_image_pad(lines):
    """Strip the blank rows render.py reserved for a picture.

    The mirror of dropImagePad in go/layout.go, and the one place this
    implementation acknowledges pictures at all. It is unconditional here
    where Go branches on whether the terminal can draw them, because this
    reader never draws one: it exists to be diffed against the Go build by
    bin/parity.sh, and Go's `frame` subcommand — the only half of it parity
    compares — always takes the no-pictures path for exactly that reason.

    Without this, an article carrying a picture would differ between the two
    builds by however many rows it reserved, which is precisely the sort of
    silent drift the harness is here to catch.
    """
    return [ln for ln in lines if not (len(ln) == 1 and ln[0][1] == "imagepad")]


def build(app, cols, rows):
    """Compose the whole screen for the current application state."""
    if too_small(cols, rows):
        return small_frame(cols, rows)

    body_h = rows - CHROME_ROWS
    frame = Frame([])
    out = []

    if app.mode == "help":
        out.append(pad([("  Help", "tab_active")], cols))
        out.append([("─" * cols, "rule")])
        lines = app.help_lines(cols - 4)
        frame.pane_x, frame.pane_y = 2, 2
        frame.pane_w, frame.pane_h = cols - 4, body_h
        for i in range(body_h):
            line = lines[app.scroll + i] if 0 <= app.scroll + i < len(lines) else []
            out.append(([("  ", "body")] + clip(line, cols - 4)) if line else [])
        out.append([("─" * cols, "rule")])
        out.append(_status_bar_help(cols))
        frame.rows = out
        return frame

    sw = sidebar_width(cols)
    pw = pane_width(cols)

    out.append(_tab_bar(frame, app.index.get("parts", []), app.part_i, cols))
    out.append([("─" * cols, "rule")])

    side = _sidebar_rows(frame, app, sw, body_h, len(out))
    lines = _drop_image_pad(app.pane_lines(pw))
    bar = _scrollbar(body_h, len(lines), body_h, app.scroll)

    frame.pane_x = sw + 3
    frame.pane_y = len(out)
    frame.pane_w = pw
    frame.pane_h = body_h

    for i in range(body_h):
        line = lines[app.scroll + i] if 0 <= app.scroll + i < len(lines) else []
        row = side[i] + [("│", "sep"), ("  ", "body")]
        row += pad(clip(line, pw), pw)
        row += [(" ", "body"), bar[i]]
        out.append(row)

    out.append([("─" * cols, "rule")])
    out.append(_status_bar(app, cols))
    frame.rows = out
    return frame


def _status_bar_help(cols):
    left = [("  press ", "status"), ("?", "status_key"), (" or ", "status"),
            ("esc", "status_key"), (" to close", "status")]
    return pad(left, cols, "status")


HELP = """
# Getting around

Nothing here is destructive. Press any key and see what happens.

## Moving between parts

The names across the top are the **parts** of the course. Move between them
with the left and right arrows.

- `←` `→` — previous / next part
- `Tab` — next part
- click a name at the top to jump straight to it

## Moving between sections

Some parts are divided into **sections**, the headings down the left. Each
one numbers its own articles, and the numbers you press are the ones in the
section you are in.

- `⇥` — next section
- `⇧⇥` — previous section
- click a heading to open that section

## Moving between articles

The numbered list down the left is the **articles** in the current section.

- `1` … `9` — jump straight to that numbered article
- `n` `p` — next / previous article, carrying on into the next part
- click an article to open it

## Reading

- `↑` `↓` or `j` `k` — scroll a line
- `Space` `b`, or `PgDn` `PgUp` — scroll a page
- `g` `G` — jump to the top or the bottom
- the mouse wheel scrolls too

## Finding something

Press `/` and start typing. Matches appear in the left margin as you type,
best first. `↑` and `↓` move through them, `Enter` opens one, `Esc` gives up.

## Leaving

`q` quits. So does `Ctrl-C`. Your terminal is put back exactly as it was.
"""
