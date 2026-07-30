"""Markdown renderer for the tutor TUI.

Turns markdown into ``lines`` — a list of rows, each row a list of
``(text, style)`` spans that :mod:`term` knows how to paint.

This is deliberately *not* a general markdown implementation. The course
content is authored alongside it, so the supported subset is a contract we
control rather than a guess about arbitrary input:

    headings (#..####)   paragraphs with reflow   fenced code blocks
    inline `code`        **bold**   *italic*      bullet + ordered lists
    > blockquotes        --- rules  [links](url)  | pipe | tables |
    ![alt](pic.png)      pictures — PNG only, and only where the terminal
                         can actually show them

Anything unrecognised degrades to a plain wrapped paragraph, so unexpected
syntax is always readable even when it is not pretty.

Owning the renderer buys the two things the alternatives could not offer:
correct reflow at any pane width (so a resize is instant, with no subprocess
to re-run) and zero dependencies on the reader's machine.

Headless check:

    python3 -m tui.render content/01-the-terminal/01-foo.md 72
"""

import os
import re
import unicodedata

from . import content

# --------------------------------------------------------------------------
# Width helpers
#
# Shared with layout.py. Terminals measure columns, not characters: combining
# marks occupy none and CJK occupies two.
# --------------------------------------------------------------------------


def char_width(ch):
    if unicodedata.combining(ch):
        return 0
    o = ord(ch)
    if o < 32 or o == 127:
        return 0
    if unicodedata.east_asian_width(ch) in ("W", "F"):
        return 2
    return 1


def dwidth(text):
    """Display width of *text* in terminal columns."""
    if text.isascii():
        return len(text)
    return sum(char_width(c) for c in text)


def clip(spans, width):
    """Truncate a span list to *width* columns, preserving styles."""
    out = []
    used = 0
    for text, style in spans:
        if used >= width:
            break
        w = dwidth(text)
        if used + w <= width:
            out.append((text, style))
            used += w
            continue
        cut = []
        for ch in text:
            cw = char_width(ch)
            if used + cw > width:
                break
            cut.append(ch)
            used += cw
        if cut:
            out.append(("".join(cut), style))
        break
    return out


def pad(spans, width, style="body"):
    """Extend a span list to exactly *width* columns."""
    spans = clip(spans, width)
    used = sum(dwidth(t) for t, _ in spans)
    if used < width:
        spans = spans + [(" " * (width - used), style)]
    return spans


def spans_width(spans):
    return sum(dwidth(t) for t, _ in spans)


def merge(spans):
    """Collapse adjacent spans sharing a style. Purely a size optimisation."""
    out = []
    for text, style in spans:
        if not text:
            continue
        if out and out[-1][1] == style:
            out[-1] = (out[-1][0] + text, style)
        else:
            out.append((text, style))
    return out


# --------------------------------------------------------------------------
# Inline parsing
# --------------------------------------------------------------------------

_INLINE_RE = re.compile(
    r"\\(?P<esc>.)"
    r"|(?P<code>`+)(?P<codetext>.+?)(?P=code)"
    r"|\[(?P<ltext>[^\]]*)\]\((?P<lurl>[^)\s]*)\)"
    r"|(?P<strong>\*\*|__)(?P<strongtext>\S.*?)(?P=strong)"
    r"|(?P<em>[*_])(?P<emtext>\S.*?)(?P=em)",
    re.S,
)

_COMBINE = {
    ("body", "strong"): "bold",
    ("body", "em"): "italic",
    ("bold", "em"): "bolditalic",
    ("italic", "strong"): "bolditalic",
    ("dim", "strong"): "bold",
    ("quote", "strong"): "bold",
    ("quote", "em"): "quote",
}


def _combine(base, kind):
    # Headings and links are already emphatic; nesting inside them is a no-op
    # rather than a colour change that would fight the surrounding style.
    if base.startswith("h") or base in ("link", "tablehead"):
        return base
    return _COMBINE.get((base, kind), base if kind == "em" else "bold")


def _shorten_url(url):
    for prefix in ("https://", "http://"):
        if url.startswith(prefix):
            url = url[len(prefix):]
    return url.rstrip("/")


def parse_inline(text, base="body"):
    """Parse inline markup into spans, recursing through nested emphasis."""
    spans = []
    buf = []
    pos = 0

    def flush():
        if buf:
            spans.append(("".join(buf), base))
            del buf[:]

    while pos < len(text):
        m = _INLINE_RE.search(text, pos)
        if not m:
            buf.append(text[pos:])
            break
        if m.start() > pos:
            buf.append(text[pos:m.start()])
        d = m.groupdict()

        if d["esc"] is not None:
            buf.append(d["esc"])
        elif d["code"] is not None:
            flush()
            inner = d["codetext"]
            # One padding space each side, per CommonMark, so `` ` `` works.
            if inner.startswith(" ") and inner.endswith(" ") and inner.strip():
                inner = inner[1:-1]
            spans.append((inner, "code"))
        elif d["ltext"] is not None:
            flush()
            spans.extend(parse_inline(d["ltext"], "link"))
            url = _shorten_url(d["lurl"])
            if url and url != d["ltext"]:
                spans.append((" (" + url + ")", "linkurl"))
        elif d["strong"] is not None:
            flush()
            spans.extend(parse_inline(d["strongtext"], _combine(base, "strong")))
        elif d["em"] is not None:
            marker = d["em"]
            before = text[m.start() - 1] if m.start() else " "
            after_i = m.end()
            after = text[after_i] if after_i < len(text) else " "
            # `snake_case` and `a_b_c` are identifiers, not emphasis. Require
            # underscore emphasis to sit on a word boundary; `*` is unambiguous.
            if marker == "_" and (before.isalnum() or after.isalnum()):
                buf.append(marker)
                pos = m.start() + 1
                continue
            flush()
            spans.extend(parse_inline(d["emtext"], _combine(base, "em")))

        pos = m.end()

    flush()
    return merge(spans)


# --------------------------------------------------------------------------
# Wrapping
# --------------------------------------------------------------------------


def _atoms(spans):
    """Split spans into word atoms, dropping the whitespace between them."""
    out = []
    for text, style in spans:
        parts = re.split(r"(\s+)", text)
        for part in parts:
            if not part:
                continue
            if part.isspace():
                out.append((None, style))  # a break opportunity
            else:
                out.append((part, style))
    return out


def _hard_split(word, style, width):
    """Break a word too long for the pane into width-sized chunks."""
    chunks = []
    cur = ""
    cw = 0
    for ch in word:
        w = char_width(ch)
        if cw + w > width and cur:
            chunks.append((cur, style))
            cur, cw = "", 0
        cur += ch
        cw += w
    if cur:
        chunks.append((cur, style))
    return chunks


def wrap(spans, width, first_prefix=None, rest_prefix=None):
    """Reflow *spans* to *width*, with optional per-line prefixes.

    ``first_prefix``/``rest_prefix`` are span lists themselves, which is what
    makes hanging indents (list bullets, quote bars) fall out for free.
    """
    first_prefix = first_prefix or []
    rest_prefix = rest_prefix if rest_prefix is not None else first_prefix
    atoms = _atoms(spans)
    if not atoms:
        return [list(first_prefix)] if first_prefix else [[]]

    lines = []
    prefix = first_prefix
    avail = max(1, width - spans_width(prefix))
    cur = []
    cur_w = 0
    pending_space = False

    for word, style in atoms:
        if word is None:
            if cur:
                pending_space = True
            continue

        pieces = [(word, style)]
        if dwidth(word) > avail:
            pieces = _hard_split(word, style, avail)

        for piece, pstyle in pieces:
            pw = dwidth(piece)
            need = pw + (1 if pending_space and cur else 0)
            if cur and cur_w + need > avail:
                lines.append(list(prefix) + cur)
                prefix = rest_prefix
                avail = max(1, width - spans_width(prefix))
                cur, cur_w, pending_space = [], 0, False
            if pending_space and cur:
                # The separating space inherits a style only when both sides
                # share one, so `cd ~` keeps an unbroken code background while
                # "the [link]" does not drag the underline onto the space.
                gap = pstyle if cur[-1][1] == pstyle else "body"
                cur.append((" ", gap))
                cur_w += 1
            pending_space = False
            cur.append((piece, pstyle))
            cur_w += pw

    if cur:
        lines.append(list(prefix) + cur)
    return [merge(line) for line in lines]


# --------------------------------------------------------------------------
# Block parsing
# --------------------------------------------------------------------------

_FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})\s*([A-Za-z0-9_+-]*)\s*$")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_RULE_RE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")
_BULLET_RE = re.compile(r"^(\s*)([-*+])\s+(.*)$")
_ORDERED_RE = re.compile(r"^(\s*)(\d+)[.)]\s+(.*)$")
_QUOTE_RE = re.compile(r"^\s*>\s?(.*)$")
_FRONTMATTER_RE = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.S)
_IMAGE_RE = re.compile(r"^\s*!\[([^\]]*)\]\(([^)\s]*)\)\s*$")

# Every glyph the renderer draws has to exist in Menlo and SF Mono, or macOS
# substitutes a font and may give it double width — which would shift every
# column to its right. These three are safe; exotica is not worth the risk.
_BULLETS = ("•", "◦", "-")


def strip_frontmatter(text):
    return _FRONTMATTER_RE.sub("", text, count=1)


def _repo_root():
    """The tutor folder, for resolving picture paths under ``content/``.

    Mirrors frame.py's ``repo_root()`` rather than importing it: frame.py
    imports app.py, which imports this module, so importing frame.py here
    would cycle. ``$TUTOR_HOME`` lets bin/parity.sh pin this to the same
    tree the Go binary resolves, the way frame.py already does for whole
    screens.
    """
    return os.environ.get("TUTOR_HOME") or os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )


def _png_size(path):
    """Read width/height straight from a PNG's IHDR chunk.

    Returns ``(None, None)`` for anything that is not a readable PNG, so the
    picture branch can reserve zero rows without the two languages needing
    to agree on an exception type or error message.
    """
    try:
        with open(path, "rb") as fh:
            head = fh.read(24)
    except OSError:
        return None, None
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n":
        return None, None
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")


def _image_rows(img_w, img_h, pane_w):
    """How many blank terminal rows a picture reserves, cells being ~2:1 (w:h).

    Integer division only, mirroring Go's imageRows(): the two languages
    must land on the exact same row count for every input, and a float
    ceil() is not guaranteed to round identically on both sides.
    """
    return (img_h * pane_w + img_w * 2 - 1) // (img_w * 2)


def _is_table_sep(line):
    line = line.strip()
    if not line or "-" not in line:
        return False
    return bool(re.match(r"^\|?[\s:|-]+\|[\s:|-]*$", line)) and set(line) <= set("|-: \t")


def _split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def render(md, width):
    """Render markdown to a list of styled rows at *width* columns."""
    width = max(20, width)
    md = strip_frontmatter(md.replace("\t", "    "))
    src = md.split("\n")
    out = []
    i = 0
    n = len(src)

    while i < n:
        line = src[i]

        if not line.strip():
            if out and out[-1] != []:
                out.append([])
            i += 1
            continue

        # -- fenced code ---------------------------------------------------
        m = _FENCE_RE.match(line)
        if m:
            fence, lang = m.group(2)[0] * 3, m.group(3)
            i += 1
            body = []
            while i < n and not (src[i].lstrip().startswith(fence) and not src[i].strip().strip(fence[0])):
                body.append(src[i])
                i += 1
            i += 1  # closing fence
            out.extend(_render_code(body, lang, width))
            continue

        # -- heading -------------------------------------------------------
        m = _HEADING_RE.match(line)
        if m:
            level = min(len(m.group(1)), 4)
            style = "h%d" % level
            if out and out[-1] != []:
                out.append([])
            out.extend(wrap(parse_inline(m.group(2), style), width))
            if level <= 2:
                out.append([("─" * width, "rule")])
            out.append([])
            i += 1
            continue

        # -- horizontal rule ----------------------------------------------
        if _RULE_RE.match(line):
            out.append([("─" * width, "rule")])
            out.append([])
            i += 1
            continue

        # -- picture ---------------------------------------------------------
        m = _IMAGE_RE.match(line)
        if m:
            alt, rel = m.group(1), m.group(2)
            rows = 0
            # A missing, unreadable or non-PNG file reserves zero rows rather
            # than erroring, and Go must fail the same way: "just the
            # caption, no picture" is the one shape both sides can produce
            # identically without agreeing on an error message too.
            img_w, img_h = _png_size(os.path.join(content.content_dir(_repo_root()), rel))
            if img_w is not None:
                rows = _image_rows(img_w, img_h, width)
            for _ in range(rows):
                out.append([(" " * width, "imagepad")])
            out.extend(wrap(parse_inline(alt, "dim"), width))
            out.append([])
            i += 1
            continue

        # -- blockquote ----------------------------------------------------
        if _QUOTE_RE.match(line):
            block = []
            # Lazy continuation: an unmarked line keeps the quote going, but a
            # heading, list or fence on the next line starts its own block
            # rather than being swallowed into the quotation.
            while i < n and (
                _QUOTE_RE.match(src[i])
                or (src[i].strip() and block and not _is_block_start(src[i]))
            ):
                m2 = _QUOTE_RE.match(src[i])
                block.append(m2.group(1) if m2 else src[i].strip())
                i += 1
            inner = render("\n".join(block), width - 3)
            bar = [("│ ", "quotebar")]
            for row in inner:
                out.append(bar + [(t, "quote" if s == "body" else s) for t, s in row])
            out.append([])
            continue

        # -- table ---------------------------------------------------------
        if "|" in line and i + 1 < n and _is_table_sep(src[i + 1]):
            header = _split_row(line)
            aligns = _parse_aligns(_split_row(src[i + 1]))
            i += 2
            rows = []
            while i < n and "|" in src[i] and src[i].strip():
                rows.append(_split_row(src[i]))
                i += 1
            out.extend(_render_table(header, aligns, rows, width))
            out.append([])
            continue

        # -- list ----------------------------------------------------------
        if _BULLET_RE.match(line) or _ORDERED_RE.match(line):
            i = _render_list(src, i, width, out)
            out.append([])
            continue

        # -- paragraph -----------------------------------------------------
        para = []
        while i < n and src[i].strip() and not _is_block_start(src[i]):
            para.append(src[i].strip())
            i += 1
        out.extend(wrap(parse_inline(" ".join(para)), width))

    while out and out[-1] == []:
        out.pop()
    return out


def _is_block_start(line):
    """Does this line begin a block, and so end the paragraph above it?

    A picture is listed here even though a table is not, and the asymmetry is
    deliberate. A table is several lines long and an author naturally leaves a
    blank line around it; a picture is a single line, and writing it flush
    against the paragraph it illustrates is the obvious thing to do. Without
    this, that spelling would silently print the raw ![alt](path) as body text
    rather than drawing anything — a failure with no error attached to it.
    """
    return bool(
        _FENCE_RE.match(line)
        or _HEADING_RE.match(line)
        or _RULE_RE.match(line)
        or _IMAGE_RE.match(line)
        or _QUOTE_RE.match(line)
        or _BULLET_RE.match(line)
        or _ORDERED_RE.match(line)
    )


def _render_code(body, lang, width):
    """A code block is a solid tinted slab: padded to full width, never wrapped.

    Wrapping code would silently corrupt the thing the reader is meant to
    copy, so long lines are clipped instead and the block keeps its shape.
    """
    lines = []
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()

    indent = min((len(l) - len(l.lstrip()) for l in body if l.strip()), default=0)
    label = ("  " + lang, "codelang") if lang else ("", "codelang")
    lines.append(pad([label] if lang else [], width, "codelang"))
    for raw in body:
        text = raw[indent:] if len(raw) >= indent else raw.lstrip()
        lines.append(pad([("  " + text, "codeblock")], width, "codeblock"))
    lines.append(pad([], width, "codeblock"))
    lines.append([])
    return lines


def _render_list(src, i, width, out):
    n = len(src)
    counters = {}
    while i < n:
        line = src[i]
        if not line.strip():
            # A blank line ends the list. A "loose" list separated by blanks
            # therefore renders as one block per item, which reads better than
            # silently welding two adjacent lists into one.
            break

        mb = _BULLET_RE.match(line)
        mo = _ORDERED_RE.match(line)
        if not (mb or mo):
            break

        m = mb or mo
        level = min(len(m.group(1)) // 2, 2)
        for lv in list(counters):
            if lv > level:
                del counters[lv]

        if mo:
            counters[level] = counters.get(level, int(mo.group(2)) - 1) + 1
            marker = "%d." % counters[level]
        else:
            counters.pop(level, None)
            marker = _BULLETS[level]

        body = [m.group(3)]
        i += 1
        # Continuation lines: indented further than the marker, not a new item.
        while i < n and src[i].strip() and not (_BULLET_RE.match(src[i]) or _ORDERED_RE.match(src[i])):
            if len(src[i]) - len(src[i].lstrip()) > len(m.group(1)):
                body.append(src[i].strip())
                i += 1
            else:
                break

        pad_left = "  " * level
        first = [(pad_left + " ", "body"), (marker, "bullet"), (" ", "body")]
        rest = [(" " * (spans_width(first)), "body")]
        out.extend(wrap(parse_inline(" ".join(body)), width, first, rest))
    return i


def _parse_aligns(cells):
    aligns = []
    for c in cells:
        c = c.strip()
        if c.startswith(":") and c.endswith(":"):
            aligns.append("center")
        elif c.endswith(":"):
            aligns.append("right")
        else:
            aligns.append("left")
    return aligns


def _render_table(header, aligns, rows, width):
    ncols = len(header)
    aligns = (aligns + ["left"] * ncols)[:ncols]
    rows = [(r + [""] * ncols)[:ncols] for r in rows]

    gap = 3  # " │ "
    budget = width - 1 - gap * (ncols - 1)
    if budget < ncols * 3:
        # Too narrow for a table: fall back to labelled stacks, which stay
        # readable at any width instead of collapsing into noise.
        return _render_table_stacked(header, rows, width)

    natural = []
    for c in range(ncols):
        natural.append(max([dwidth(header[c])] + [dwidth(r[c]) for r in rows] or [0]))

    widths = _fit_columns(natural, budget)

    def cell_lines(text, col, style):
        lines = wrap(parse_inline(text, style), widths[col])
        return lines or [[]]

    out = []
    out.extend(_table_row(header, aligns, widths, "tablehead"))
    sep = []
    for c in range(ncols):
        if c:
            sep.append(("─┼─", "tableborder"))
        sep.append(("─" * widths[c], "tableborder"))
    out.append([(" ", "body")] + sep)
    for r in rows:
        out.extend(_table_row(r, aligns, widths, "body"))
    return out


def _table_row(cells, aligns, widths, style):
    rendered = [wrap(parse_inline(cells[c], style), widths[c]) or [[]] for c in range(len(widths))]
    height = max(len(r) for r in rendered)
    out = []
    for line_i in range(height):
        row = [(" ", "body")]
        for c in range(len(widths)):
            if c:
                row.append((" │ ", "tableborder"))
            spans = rendered[c][line_i] if line_i < len(rendered[c]) else []
            row.extend(_align(spans, widths[c], aligns[c]))
        out.append(merge(row))
    return out


def _align(spans, width, how):
    used = spans_width(spans)
    slack = max(0, width - used)
    if how == "right":
        return [(" " * slack, "body")] + spans
    if how == "center":
        left = slack // 2
        return [(" " * left, "body")] + spans + [(" " * (slack - left), "body")]
    return spans + [(" " * slack, "body")]


def _fit_columns(natural, budget):
    """Shrink the widest columns first until the table fits the budget."""
    widths = list(natural)
    while sum(widths) > budget:
        widest = max(range(len(widths)), key=lambda c: widths[c])
        if widths[widest] <= 3:
            break
        widths[widest] -= 1
    # Spend any leftover room on the columns that wanted it most.
    slack = budget - sum(widths)
    order = sorted(range(len(widths)), key=lambda c: natural[c] - widths[c], reverse=True)
    idx = 0
    while slack > 0 and order:
        c = order[idx % len(order)]
        if widths[c] < natural[c]:
            widths[c] += 1
            slack -= 1
        elif all(widths[k] >= natural[k] for k in order):
            break
        idx += 1
    return widths


def _render_table_stacked(header, rows, width):
    out = []
    for r in rows:
        for c, cell in enumerate(r):
            label = header[c] if c < len(header) else ""
            first = [(" ", "body"), (label + ": ", "tablehead")]
            rest = [("   ", "body")]
            out.extend(wrap(parse_inline(cell), width, first, rest))
        out.append([])
    return out


# --------------------------------------------------------------------------
# Headless preview: python3 -m tui.render <file.md> [width]
# --------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    from . import term as _term  # noqa: F401  (relative import when run as -m)

    path = sys.argv[1]
    cols = int(sys.argv[2]) if len(sys.argv) > 2 else 72
    with open(path, encoding="utf-8") as fh:
        doc = fh.read()
    for row in render(doc, cols):
        parts = []
        for text, style in row:
            esc = _term.sgr(style)
            parts.append(esc + text + _term.RESET if esc else text)
        print("".join(parts))
