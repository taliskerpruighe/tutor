#!/usr/bin/env python3
"""Blow one Nerd Font glyph (U+F169F) up into terminal character art.

Renders the glyph from a Nerd Font at high resolution, box-averages it down
to a coverage map, thresholds that, and packs the resulting dot grid into
either Braille (2x4 dots per cell) or half blocks (1x2 subpixels per cell).

Cell aspect is measured from the font, not assumed: Hack Nerd Font Mono at
size 100 advances 60.2px per cell over a 117px line, i.e. h/w = 1.943.  The
glyph's own ink box is 470x427 (h/w = 0.9085), so R rows of art want
R * 1.943 / 0.9085 = 2.14 * R columns to come out undistorted.

Usage:  python3 gen.py                 # regenerate every art file here
        python3 gen.py 6 braille 0.5   # one-off: rows, tier, threshold
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont

GLYPH = 0xF169F
FONT = "/home/talisker/.local/share/fonts/hack-nerd-font/HackNerdFont-Regular.ttf"
HERE = os.path.dirname(os.path.abspath(__file__))
CELL_ASPECT = 117 / 60.203125          # height/width of one terminal cell
SS = 8                                 # supersample factor per dot

BRAILLE_OFFS = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (0, 3), (1, 3)]


def render(size=1200):
    """Return (mask, bbox) for the glyph at high resolution."""
    f = ImageFont.truetype(FONT, size)
    img = Image.new("L", (size * 2, size * 2), 0)
    ImageDraw.Draw(img).text((size, size), chr(GLYPH), font=f, fill=255, anchor="mm")
    return img.crop(img.getbbox())


def head_only(img):
    """Drop the '!?' marks: keep the largest connected ink blob."""
    w, h = img.size
    px = img.load()
    seen = [[False] * w for _ in range(h)]
    best = None
    for y in range(h):
        for x in range(w):
            if seen[y][x] or px[x, y] < 128:
                continue
            stack, comp = [(x, y)], []
            seen[y][x] = True
            while stack:
                cx, cy = stack.pop()
                comp.append((cx, cy))
                for nx, ny in ((cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)):
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] and px[nx, ny] >= 128:
                        seen[ny][nx] = True
                        stack.append((nx, ny))
            if best is None or len(comp) > len(best):
                best = comp
    out = Image.new("L", (w, h), 0)
    op = out.load()
    for cx, cy in best:
        op[cx, cy] = 255
    return out.crop(out.getbbox())


def dots(img, dot_w, dot_h, threshold):
    """Box-average the mask down to dot_w x dot_h and threshold it."""
    small = img.resize((dot_w * SS, dot_h * SS), Image.LANCZOS).resize(
        (dot_w, dot_h), Image.BOX)
    px = small.load()
    return [[px[x, y] / 255.0 >= threshold for x in range(dot_w)] for y in range(dot_h)]


def to_braille(grid):
    h, w = len(grid), len(grid[0])
    rows = []
    for cy in range(0, h, 4):
        line = ""
        for cx in range(0, w, 2):
            bits = 0
            for i, (dx, dy) in enumerate(BRAILLE_OFFS):
                if cy + dy < h and cx + dx < w and grid[cy + dy][cx + dx]:
                    bits |= 1 << i
            line += chr(0x2800 + bits)
        rows.append(line)
    return rows


HALF = {(0, 0): " ", (1, 0): "▀", (0, 1): "▄", (1, 1): "█"}


def to_half(grid):
    h, w = len(grid), len(grid[0])
    rows = []
    for cy in range(0, h, 2):
        line = ""
        for cx in range(w):
            top = grid[cy][cx]
            bot = grid[cy + 1][cx] if cy + 1 < h else False
            line += HALF[(int(top), int(bot))]
        rows.append(line)
    return rows


def art(img, rows, tier, threshold, cols=None):
    aspect = img.size[1] / img.size[0]          # ink height / ink width
    if cols is None:
        cols = max(1, round(rows * CELL_ASPECT / aspect))
    if tier == "braille":
        grid = dots(img, cols * 2, rows * 4, threshold)
        return to_braille(grid)
    grid = dots(img, cols, rows * 2, threshold)
    return to_half(grid)


BLANKS = " \u2800"


def punctuate(lines, rows):
    """Re-attach the glyph's '!?' as literal characters, top right.

    The marks in the source are already type, so they are set as type rather
    than downsampled: at four rows a bitmap '?' is three columns of noise,
    while a real '?' is a real '?'.  They are laid into the blank cells at
    the top right of the head-only crop -- where they sit in the source --
    and only appended past the right edge if the art is too small to hold
    them.
    """
    keep = max((i + 1 for line in lines for i, c in enumerate(line)
                if c not in BLANKS), default=0)
    out = [line[:keep].ljust(keep) for line in lines]
    marks = "!?"
    at = keep - len(marks)
    if at > 0 and all(c in BLANKS for c in out[0][at:]):
        out[0] = out[0][:at] + marks
        return out
    return [out[0] + " " + marks] + [line + " " * (len(marks) + 1) for line in out[1:]]


def main():
    if len(sys.argv) > 1:
        rows, tier = int(sys.argv[1]), sys.argv[2]
        thr = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
        print("\n".join(art(render(), rows, tier, thr)))
        return
    full = render()
    head = head_only(full)
    full.save(os.path.join(HERE, "source.png"))   # the mask preview.py compares against
    for rows in (4, 6, 8, 12):
        for tier in ("braille", "half"):
            for src, tag in ((full, "full"), (head, "head")):
                lines = art(src, rows, tier, 0.5)
                if tag == "head":
                    lines = punctuate(lines, rows)
                name = f"{tag}-{tier}-{rows}r.txt"
                with open(os.path.join(HERE, name), "w") as fh:
                    fh.write("\n".join(lines) + "\n")
                print(name, len(lines), "rows x", max(len(l) for l in lines), "cols")


if __name__ == "__main__":
    main()
