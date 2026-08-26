#!/usr/bin/env python3
"""Render character art at real terminal cell size and contact-sheet it.

Art that looks fine blown up on a page can be mush at 10px per cell, so
every candidate here is rasterised at a terminal-like cell size in the same
monospace font a reader would see, then the whole sheet is magnified with
nearest-neighbour for inspection.  Magnifying the sheet, rather than
drawing the art large in the first place, keeps what you judge identical to
what a terminal would show.

Usage: python3 preview.py out.png label:file.txt [label:source.png@ROWS ...]

A .png source is pasted in scaled to the pixel height ROWS of art occupies,
so art and original can be compared at the same physical size.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

MONO = "/usr/share/fonts/adwaita-mono-fonts/AdwaitaMono-Regular.ttf"
PT = 20                       # ~12px cell width: a normal terminal
ZOOM = 3


def tile(label, path):
    lines = open(path).read().rstrip("\n").split("\n")
    f = ImageFont.truetype(MONO, PT)
    lab = ImageFont.truetype(MONO, 12)
    cw = f.getlength("M")
    a, d = f.getmetrics()
    ch = a + d
    w = int(cw * max(len(l) for l in lines)) + 8
    h = int(ch * len(lines)) + 22
    img = Image.new("L", (max(w, 120), h), 255)
    dr = ImageDraw.Draw(img)
    dr.text((4, 2), label, font=lab, fill=100)
    for i, line in enumerate(lines):
        dr.text((4, 16 + i * ch), line, font=f, fill=0)
    return img


def image_tile(label, path, rows):
    """The source glyph, scaled to the pixel height `rows` of art occupies."""
    f = ImageFont.truetype(MONO, PT)
    a, d = f.getmetrics()
    src = Image.open(path).convert("L")
    h = int((a + d) * rows)
    w = int(src.size[0] * h / src.size[1])
    img = Image.new("L", (max(w + 8, 120), h + 22), 255)
    ImageDraw.Draw(img).text((4, 2), label, font=ImageFont.truetype(MONO, 12), fill=100)
    img.paste(Image.eval(src.resize((w, h), Image.LANCZOS), lambda v: 255 - v), (4, 16))
    return img


def main():
    out, specs = sys.argv[1], sys.argv[2:]
    tiles = []
    for s in specs:
        label, path = s.split(":", 1)
        path, _, rows = path.partition("@")          # label:file.png@ROWS
        if path.endswith(".png"):
            tiles.append(image_tile(label, path, int(rows or 8)))
        else:
            tiles.append(tile(label, path))
    pad = 10
    W = max(t.size[0] for t in tiles) + pad * 2
    H = sum(t.size[1] + pad for t in tiles) + pad
    sheet = Image.new("L", (W, H), 255)
    y = pad
    for t in tiles:
        sheet.paste(t, (pad, y))
        y += t.size[1] + pad
    sheet.resize((W * ZOOM, H * ZOOM), Image.NEAREST).save(out)
    print(out, sheet.size)


if __name__ == "__main__":
    main()
