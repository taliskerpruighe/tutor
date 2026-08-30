#!/usr/bin/env python3
"""
render_pdf.py -- Markdown-to-contract-PDF renderer for the challenge-two
teaching corpus (reportlab-pdf producer lane).

Usage:
    python3 render_pdf.py <input.md> <output.pdf>

Deliberately uses margins, a font family, a font size, and a leading that
are visibly different from LibreOffice's defaults, so that a later check
can distinguish "reportlab-pdf" output from "soffice-pdf" output by
inspecting the extracted text layer's font metadata (e.g. via PyMuPDF's
page.get_text("dict")). LibreOffice's default export uses a serif face
(Liberation Serif) at ~12pt with ~1 inch margins; this renderer uses a
sans-serif face (Helvetica) at 10.5pt with asymmetric, unusual margins
(1.35in / 0.95in) and a 15.5pt leading that does not match any common
default.

Markdown handling is intentionally minimal -- it supports exactly what
the challenge-two contract sources need:
    - a single H1 (`# Title`) treated as the document title
    - ALL-CAPS lines (optionally preceded by `##`) treated as section
      headings
    - ordinary paragraphs (blank-line separated)
    - a signature block, triggered by a line that is exactly
      `<!-- signature-block -->`, after which each remaining
      blank-line-separated paragraph is rendered as a signature line
      with extra spacing above it

The output always contains a real, selectable text layer -- never a
rasterized image.
"""
import re
import sys
from pathlib import Path

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.pdfbase.pdfmetrics import stringWidth  # noqa: F401  (kept for future width checks)


# --- deliberately distinct visual metrics -----------------------------
FONT_NAME = "Helvetica"
FONT_NAME_BOLD = "Helvetica-Bold"
FONT_SIZE = 10.5
LEADING = 15.5
MARGIN_LEFT = 1.35 * inch
MARGIN_RIGHT = 0.95 * inch
MARGIN_TOP = 1.1 * inch
MARGIN_BOTTOM = 1.0 * inch

TITLE_SIZE = 14.5
HEADING_SIZE = 11.5


def is_all_caps_heading(line: str) -> bool:
    stripped = line.strip().lstrip("#").strip()
    if not stripped:
        return False
    letters = [c for c in stripped if c.isalpha()]
    if not letters:
        return False
    return all(c.isupper() for c in letters) and len(stripped) > 2


def parse_markdown(text: str):
    """Return a list of ('title'|'heading'|'para'|'sig', content) tuples."""
    lines = text.replace("\r\n", "\n").split("\n")
    blocks = []
    buf = []
    in_signature = False

    def flush():
        nonlocal buf
        if buf:
            joined = " ".join(s.strip() for s in buf if s.strip())
            if joined:
                blocks.append(("sig" if in_signature else "para", joined))
        buf = []

    for raw in lines:
        line = raw.rstrip()
        if line.strip() == "<!-- signature-block -->":
            flush()
            in_signature = True
            continue
        if not line.strip():
            flush()
            continue
        if line.startswith("# "):
            flush()
            blocks.append(("title", line[2:].strip()))
            continue
        if line.startswith("## "):
            # Any explicit "## " heading is treated as a heading, whether
            # or not it happens to be ALL-CAPS -- only the bare (no "##")
            # ALL-CAPS check below needs the case test, since that's the
            # only signal available for an unmarked heading line.
            flush()
            blocks.append(("heading", line[3:].strip()))
            continue
        if is_all_caps_heading(line):
            flush()
            blocks.append(("heading", line.strip()))
            continue
        buf.append(line)
    flush()
    return blocks


def build_styles():
    base = ParagraphStyle(
        "Body",
        fontName=FONT_NAME,
        fontSize=FONT_SIZE,
        leading=LEADING,
        alignment=TA_LEFT,
        spaceAfter=8,
    )
    title = ParagraphStyle(
        "Title",
        parent=base,
        fontName=FONT_NAME_BOLD,
        fontSize=TITLE_SIZE,
        leading=TITLE_SIZE + 4,
        alignment=TA_CENTER,
        spaceAfter=18,
    )
    heading = ParagraphStyle(
        "Heading",
        parent=base,
        fontName=FONT_NAME_BOLD,
        fontSize=HEADING_SIZE,
        leading=HEADING_SIZE + 4,
        spaceBefore=12,
        spaceAfter=6,
    )
    sig = ParagraphStyle(
        "Signature",
        parent=base,
        spaceBefore=18,
        spaceAfter=4,
    )
    return {"title": title, "heading": heading, "para": base, "sig": sig}


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def render(input_path: Path, output_path: Path) -> None:
    text = input_path.read_text(encoding="utf-8")
    blocks = parse_markdown(text)
    styles = build_styles()

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=LETTER,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        title=input_path.stem,
    )

    story = []
    for kind, content in blocks:
        safe = escape(content)
        if kind == "title":
            story.append(Paragraph(safe, styles["title"]))
        elif kind == "heading":
            story.append(Paragraph(safe, styles["heading"]))
        elif kind == "sig":
            story.append(Paragraph(safe, styles["sig"]))
        else:
            story.append(Paragraph(safe, styles["para"]))

    if not story:
        story.append(Paragraph("(empty document)", styles["para"]))

    doc.build(story)


def main(argv):
    if len(argv) != 3:
        print(f"usage: {argv[0]} <input.md> <output.pdf>", file=sys.stderr)
        return 2
    input_path = Path(argv[1])
    output_path = Path(argv[2])
    if not input_path.exists():
        print(f"error: input file does not exist: {input_path}", file=sys.stderr)
        return 1
    output_path.parent.mkdir(parents=True, exist_ok=True)
    render(input_path, output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
